import json
import os
import subprocess as sp
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, TypedDict

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from minio import Minio, MinioAdmin
from pydantic import SecretStr
from typing_extensions import Self


class StorageType(Enum):
    MINIO = "minio"
    AZURE = "azure"


class WorkspaceAdapter(ABC):
    """
    The WorkspaceAdapter is an abstract class that defines the minimum
    interface for interacting with workspaces. It abstracts away the
    underlying storage system, so that the EODC API can be used with
    different providers.
    """

    @staticmethod
    def create_adapter(
        tenant_url: str = None,
        storage_type: StorageType = StorageType.MINIO,
        parameters: dict[str, Any] = {},
    ) -> Self:
        if storage_type == StorageType.MINIO:
            return MinIOAdapter(
                url=tenant_url,
                access_key=parameters["access_key"],
                secret_key=parameters["secret_key"],
                mc_bin_path=parameters["mc_bin_path"],
            )
        elif storage_type == StorageType.AZURE:
            return AzureAdapter(
                url=tenant_url,
                access_key=parameters["client_id"],
                secret_key=parameters["client_secret"],
            )
        else:
            return None

    @abstractmethod
    def create_user_workspace(
        self, workspace_name: str, user_name: str, cwd: str
    ) -> None:
        pass

    @abstractmethod
    def delete_user_workspace(self, workspace_name: str):
        pass

    @abstractmethod
    def workspace_exists(self, workspace_name: str) -> bool:
        pass

    @abstractmethod
    def list_workspaces(self) -> list[str]:
        pass

    @abstractmethod
    def list_workspace_files(self, workspace_name: str):
        pass

    @abstractmethod
    def upload_file(self, workspace_name: str, file_path: str):
        pass

    @abstractmethod
    def upload_stream(self, workspace_name: str, stream: Any, file_name: str):
        pass

    @abstractmethod
    def delete_file(self, workspace_name: str, file_name: str):
        pass

    @abstractmethod
    def download_file(self, workspace_name: str, file_name: str, path: str):
        pass

    @abstractmethod
    def download_stream(self, workspace_name: str, file_name: str):
        pass


class MinIOAdapter(WorkspaceAdapter):
    """
    The system on which this is running needs to have the mc (Minio Client)
    CLI tool installed

    This Adapter implements the MinIO API for the EODC Tenant, for local workspaces
    our API needs to be more extensive than for external workspaces, as we need to
    create and delete workspaces, as well as manage users and policies. For external
    workspaces, we only need to manage files.

    Workspaces are implemented as buckets, and files are implemented as objects.
    """

    alias: str

    minio_client: Minio
    minio_admin_client: MinioAdmin

    def __init__(
        self,
        url: str,
        access_key: SecretStr,
        secret_key: SecretStr,
        mc_bin_path: Any = None,
        alias: str = "MINIO_EODC",
    ):
        self.alias = alias

        self.minio_client = Minio(
            url,
            access_key=access_key.get_secret_value(),
            secret_key=secret_key.get_secret_value(),
            secure=True,
        )

        self.minio_admin_client = MinioAdmin(target=self.alias, binary_path=mc_bin_path)

        sp.run(
            f"mc config host add {self.alias} https://{url}/ \
            {access_key.get_secret_value()} {secret_key.get_secret_value()}",
            capture_output=True,
            shell=True,
        )

    def register_user(self, user_name: str) -> dict[str, str]:
        generated_secret_key: uuid = uuid.uuid4()
        self.minio_admin_client.user_add(user_name, str(generated_secret_key))
        return {"access_key": user_name, "secret_key": str(generated_secret_key)}

    def register_user_with_secret_key(self, user_name: str, secret_key: str):
        self.minio_admin_client.user_add(user_name, str(secret_key))
        return {"access_key": user_name, "secret_key": str(secret_key)}

    def remove_user(self, user_name: str):
        self.minio_admin_client.user_remove(user_name)

    def create_user_workspace(
        self, workspace_name: str, user_name: str, cwd: str
    ) -> None:
        self._create_workspace(workspace_name=workspace_name)
        self._grant_workspace_to_user(
            workspace_name=workspace_name, user_name=user_name, cwd=cwd
        )

    def delete_user_workspace(self, workspace_name: str):
        self._remove_workspace_policy(workspace_name=workspace_name)
        self._delete_workspace(workspace_name=workspace_name)

    def workspace_exists(self, workspace_name: str) -> bool:
        return self.minio_client.bucket_exists(workspace_name)

    def list_workspaces(self) -> list[str]:
        buckets = self.minio_client.list_buckets()
        return [bucket.name for bucket in buckets]

    def create_policy(self, policy_builder: "MinioPolicyBuilder"):
        self.minio_admin_client.policy_add(
            policy_name=policy_builder.policy_name,
            policy_file=policy_builder.write_policy_file(
                policy_name=policy_builder, path=os.getcwd()
            ),
        )
        return policy_builder.policy_name

    def grant_policy_to_user(self, user_name: str, policy_name: str):
        self.minio_admin_client.policy_set(policy_name=policy_name, user=user_name)

    def grant_policy_to_group(self, group_name: str, policy_name: str):
        self.minio_admin_client.policy_set(policy_name=policy_name, group=group_name)

    def grant_new_policy_to_user(
        self, user_name: str, policy_builder: "MinioPolicyBuilder"
    ):
        self.minio_admin_client.policy_set(
            policy_name=self.create_policy(policy_builder=policy_builder),
            user=user_name,
        )

    def grant_new_policy_to_group(
        self, group_name: str, policy_builder: "MinioPolicyBuilder"
    ):
        self.minio_admin_client.policy_set(
            policy_name=self.create_policy(policy_builder=policy_builder),
            group=group_name,
        )

    def list_workspace_files(self, workspace_name: str):
        return [
            obj.object_name for obj in self.minio_client.list_objects(workspace_name)
        ]

    def update_workspace(self, workspace_name: str, **kwargs):
        if "user_name" in kwargs.keys():
            self._grant_workspace_to_user(
                workspace_name=workspace_name,
                user_name=kwargs["user_name"],
                cwd=os.getcwd(),
            )

    def revoke_policy_from_user(self, policy_name: str, user_name: str):
        self.minio_admin_client.policy_unset(policy_name=policy_name, user=user_name)

    def revoke_policy_from_group(self, policy_name: str, group_name: str):
        self.minio_admin_client.policy_unset(policy_name=policy_name, group=group_name)

    def remove_policy(self, policy_name: str):
        for user in self.minio_admin_client.user_list():
            if "policyName" in user.keys() and policy_name in user["policyName"].split(
                ","
            ):
                self.revoke_policy_from_user(
                    policy_name=policy_name, user_name=user["accessKey"]
                )
        for group in self.minio_admin_client.group_list()[0]["groups"]:
            group_info = self.minio_admin_client.group_info(group)
            if "groupPolicy" in group_info.keys() and policy_name in group_info[
                "groupPolicy"
            ].split(","):
                self.revoke_policy_from_group(policy_name=policy_name, group_name=group)
        self.minio_admin_client.policy_remove(policy_name=policy_name)

    def list_users(self):
        return self.minio_admin_client.user_list()

    def list_groups(self):
        return self.minio_admin_client.group_list()

    def group_info(self, group_name: str):
        return self.minio_admin_client.group_info(group_name=group_name)

    def upload_file(self, workspace_name: str, file_path: str):
        self.minio_client.fput_object(
            bucket_name=workspace_name,
            object_name=file_path.split("/")[-1],
            file_path=file_path,
        )

    def upload_stream(self, workspace_name: str, stream: Any, file_name: str):
        self.minio_client.put_object(
            bucket_name=workspace_name, object_name=file_name, data=stream
        )

    def delete_file(self, workspace_name: str, file_name: str):
        self.minio_client.remove_object(
            bucket_name=workspace_name, object_name=file_name
        )

    def download_file(self, workspace_name: str, file_name: str, path: str):
        self.minio_client.fget_object(
            bucket_name=workspace_name, object_name=file_name, file_path=path
        )

    def download_stream(self, workspace_name: str, file_name: str):
        return self.minio_client.get_object(
            bucket_name=workspace_name, object_name=file_name
        )

    def _remove_workspace_policy(self, workspace_name: str):
        policy_name: str = f"BASIC_{workspace_name.upper()}"
        self.remove_policy(policy_name=policy_name)

    def _grant_workspace_to_user(self, workspace_name: str, user_name: str, cwd: str):
        policy_name: str = self._create_workspace_full_access_policy(
            workspace_name=workspace_name, cwd=cwd
        )
        self.minio_admin_client.policy_set(policy_name=policy_name, user=user_name)

    def _delete_workspace(self, workspace_name: str):
        """
        raises S3Error
        """
        self.minio_client.remove_bucket(workspace_name)

    def _create_workspace_full_access_policy(
        self, workspace_name: str, cwd: str
    ) -> str:
        policy_name: str = f"BASIC_{workspace_name.upper()}"
        policy_builder = MinioPolicyBuilder(policy_name=policy_name)
        self.minio_admin_client.policy_add(
            policy_name=policy_name,
            policy_file=policy_builder.add_workspaces_full_privileges(
                workspace_names=[workspace_name]
            ).write_policy_file(policy_name=policy_name, path=cwd),
        )
        return policy_name

    def _create_workspace(self, workspace_name: str):
        """
        raises S3Error
        """
        self.minio_client.make_bucket(workspace_name)


class MinioPolicyBuilder:
    class PolicyEntry(TypedDict):
        Effect: bool
        Action: list[str]
        Resource: list[str]
        Condition: Optional[dict[str, Any]]

    class Policy(TypedDict):
        Version: str
        Statement: list["MinioPolicyBuilder.PolicyEntry"]

    policy_name: str = ""

    policy: Policy = {"Version": "2012-10-17", "Statement": []}

    @classmethod
    def make_policy_entry(
        cls,
        resource_names: list[str],
        actions: list[str],
        conditions: dict[str, Any] = None,
        allow: bool = True,
    ) -> PolicyEntry:
        return {
            "Effect": "Allow" if allow else "Deny",
            "Action": [action for action in actions],
            "Resource": [f"arn:aws:s3:::{resource}" for resource in resource_names],
            **({"Condition": conditions} if conditions is not None else {}),
        }

    def __init__(self, policy_name: str):
        self.policy_name = policy_name

    def build(self) -> Policy:
        return self.policy

    def write_policy_file(self, policy_name: str, path: str) -> str:
        abs_path = os.path.abspath(os.path.join(path, f"{policy_name}.json"))

        with open(abs_path, "w") as f:
            json.dump(self.policy, f)

        return abs_path

    def add_workspaces_reads_privileges(self, workspace_names: list[str]) -> Self:
        return self._add_workspaces_privileges(
            workspace_names=workspace_names,
            privileges=["s3:GetObject", "s3:ListBucket"],
        )

    def add_workspaces_write_privileges(self, workspace_names: list[str]) -> Self:
        return self._add_workspaces_privileges(
            workspace_names=workspace_names, privileges=["s3:PutObject"]
        )

    def add_workspaces_delete_privileges(self, workspace_names: list[str]) -> Self:
        return self._add_workspaces_privileges(
            workspace_names=workspace_names, privileges=["s3:DeleteObject"]
        )

    def add_workspaces_full_privileges(self, workspace_names: list[str]) -> Self:
        return self._add_workspaces_privileges(
            workspace_names=workspace_names,
            privileges=[
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
            ],
        )

    def add_objects_read_privileges(
        self, workspace_name: str, object_paths: list[str]
    ) -> Self:
        return self._add_objects_privileges(
            workspace_name=workspace_name,
            object_paths=object_paths,
            privileges=["s3:GetObject"],
        )

    def add_objects_write_privileges(
        self, workspace_name: str, object_paths: list[str]
    ) -> Self:
        return self._add_objects_privileges(
            workspace_name=workspace_name,
            object_paths=object_paths,
            privileges=["s3:PutObject"],
        )

    def add_objects_delete_privileges(
        self, workspace_name: str, object_paths: list[str]
    ) -> Self:
        return self._add_objects_privileges(
            workspace_name=workspace_name,
            object_paths=object_paths,
            privileges=["s3:DeleteObject"],
        )

    def add_objects_full_privileges(self, workspace_name: str):
        return self._add_workspaces_privileges(
            workspace_names=workspace_name,
            privileges=[
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
            ],
        )

    def add_workspaces_ip_ban(self, workspace_names: list[str], ip_address: str):
        return self._add_workspaces_privileges(
            workspace_names=workspace_names,
            privileges=["s3:*"],
            conditions={"IpAddress": {"aws:SourceIp": ip_address}},
            allow=False,
        )

    def _add_workspaces_privileges(
        self,
        workspace_names: list[str],
        privileges: list[str],
        conditions: dict[str, Any] = None,
        allow: bool = True,
    ) -> Self:
        self.policy["Statement"].append(
            MinioPolicyBuilder.make_policy_entry(
                resource_names=[
                    resource_name
                    for workspace_name in workspace_names
                    for resource_name in (workspace_name, f"{workspace_name}/*")
                ],
                actions=privileges,
                conditions=conditions,
                allow=allow,
            )
        )
        return self

    def _add_objects_privileges(
        self,
        workspace_name: str,
        object_paths: list[str],
        privileges: list[str],
        conditions: dict[str, Any],
        allow: bool = True,
    ) -> Self:
        self.policy["Statement"].append(
            MinioPolicyBuilder.make_policy_entry(
                resource_names=[
                    f"{workspace_name}{object_path}"
                    if object_path[0] == "/"
                    else f"{workspace_name}/{object_path}"
                    for object_path in object_paths
                ],
                actions=privileges,
                conditions=conditions,
                allow=allow,
            )
        )
        return self


class AzureAdapter(WorkspaceAdapter):
    """
    This Adapter implements the Azure API for the Workspaces API.

    Workspaces are implemented as containers, and files are implemented
    as blobs.
    """

    blob_service_client: BlobServiceClient

    def __init__(
        self,
        url: str,
        client_id: SecretStr,
        client_secret: SecretStr,
    ):
        self.blob_service_client = BlobServiceClient(
            account_url=url,
            credential=DefaultAzureCredential(
                client_id=client_id.get_secret_value(),
                client_secret=client_secret.get_secret_value(),
            ),
        )

    def workspace_exists(self, workspace_name: str) -> bool:
        return self.blob_service_client.get_container_client(
            container=workspace_name
        ).exists()

    def list_workspaces(self) -> list[str]:
        return [
            container.name for container in self.blob_service_client.list_containers()
        ]

    def list_workspace_files(self, workspace_name: str):
        return [
            blob.name
            for blob in self.blob_service_client.get_container_client(
                container=workspace_name
            ).list_blobs()
        ]

    def upload_file(self, workspace_name: str, file_path: str):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_path.split("/")[-1]
        ).upload_blob(file_path)

    def upload_stream(self, workspace_name: str, stream: Any, file_name: str):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).upload_blob(stream)

    def delete_file(self, workspace_name: str, file_name: str):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).delete_blob()

    def download_file(self, workspace_name: str, file_name: str, path: str):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).download_blob().readinto(open(path, "wb"))

    def download_stream(self, workspace_name: str, file_name: str):
        return (
            self.blob_service_client.get_blob_client(
                container=workspace_name, blob=file_name
            )
            .download_blob()
            .readall()
        )
