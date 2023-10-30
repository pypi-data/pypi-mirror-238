from typing import Any, Dict, Optional
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name, validate_name


class KongWorkspace:
    """Represents a Workspace entity in the Kong Gateway."""

    def __init__(self, data: ResponseObject) -> None:
        """Initializes the KongWorkspace object.

        Args:
            data (ResponseObject): The response data containing workspace details.

        Raises:
            ValueError: If the `id` is not present in the data.
        """
        self.id: str = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.comment: Optional[str] = data.get("comment")
        self.config: Dict[str, Any] = data.get("config", {})
        self.created_at: Optional[int] = data.get("created_at")
        self.meta: Dict[str, Any] = data.get("meta", {})

        if not self.id:
            raise ValueError("Workspace ID is not present in the provided data.")

    def __repr__(self) -> str:
        """Provides a string representation of the KongWorkspace instance.

        Returns:
            str: A string representation of the KongWorkspace.
        """
        return f"<KongWorkspace(id={self.id}, name={self.name})>"


class WorkspaceMetadata:
    """Represents metadata of a Workspace entity in the Kong Gateway."""

    def __init__(self, data: ResponseObject) -> None:
        """Initializes the WorkspaceMetadata object.

        Args:
            data (ResponseObject): The response data containing workspace
            metadata details.

        Raises:
            ValueError: If the `counts` is not present in the data.
        """
        self.counts: Dict[str, int] = data.get("counts")

        if not self.counts:
            raise ValueError("Counts data is not present in the provided metadata.")

    def __repr__(self) -> str:
        """Provides a string representation of the WorkspaceMetadata instance.

        Returns:
            str: A string representation of the WorkspaceMetadata.
        """
        return f"<WorkspaceMetadata(counts={self.counts})>"


class Workspace:
    """
    Workspace class to interact with Kong's Workspace entities.
    """

    ENTITY_PATH = "/workspaces"

    def __init__(self, client: KongClient):
        """
        Initializes the Workspace instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    @validate_name
    def create(self, name: str) -> KongWorkspace:
        """
        Create a new workspace in Kong.

        Args:
        - name (str): The name of the workspace.

        Returns:
        - KongWorkspace: Response from Kong.
        """
        if not name:
            raise ValueError("Workspace name should be provided and non-empty.")

        data = {"name": name}

        response_data = self.client.request("POST", self.ENTITY_PATH, False, json=data)
        return KongWorkspace(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongWorkspace:
        """
        Retrieve a workspace from Kong by its name or ID.

        Args:
        - id_or_name (str): The name or ID of the workspace.

        Returns:
        - KongWorkspace: Response from Kong.
        """
        response_data = self.client.request(
            "GET", f"{self.ENTITY_PATH}/{id_or_name}", False
        )
        return KongWorkspace(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str) -> bool:
        """
        Delete a workspace in Kong by its name or ID.

        Args:
        - id_or_name (str): The name or ID of the workspace.

        Returns:
        - KongWorkspace: Response from Kong.
        """
        response_data = self.client.request(
            "DELETE", f"{self.ENTITY_PATH}/{id_or_name}", False
        )
        return response_data

    @validate_id_or_name
    def get_metadata(self, id_or_name: str) -> WorkspaceMetadata:
        """
        Retrieve metadata of a workspace from Kong by its name or ID.

        Args:
        - id_or_name (str): The name or ID of the workspace.

        Returns:
        - WorkspaceMetadata: Metadata response from Kong.
        """
        response_data = self.client.request(
            "GET",
            f"{self.ENTITY_PATH}/{id_or_name}/meta",
            False,
        )
        return WorkspaceMetadata(response_data)

    @validate_id_or_name
    def patch(self, id_or_name: str, comment: Optional[str] = None) -> KongWorkspace:
        """
        Update the comment of a workspace in Kong by its name or ID.

        Args:
        - id_or_name (str): The name or ID of the workspace to update.
        - comment (Optional[str]): A string describing the workspace. If None,
                                   no changes are made.

        Returns:
        - KongWorkspace: Updated workspace response from Kong.
        """
        data = {}
        if comment is not None:
            data["comment"] = comment

        response_data = self.client.request(
            "PATCH", f"{self.ENTITY_PATH}/{id_or_name}", False, json=data
        )
        return KongWorkspace(response_data)

    @validate_id_or_name
    def put(self, id_or_name: Optional[str], name: str) -> KongWorkspace:
        """
        Update an existing workspace by its ID or create a new workspace if ID
        is not provided.

        Args:
        - workspace_id (Optional[str]): The ID of the workspace to update. If None,
                                        a new workspace will be created.
        - name (str): The name of the workspace.

        Returns:
        - KongWorkspace: Response from Kong.
        """
        data = {"name": name}

        endpoint = (
            self.ENTITY_PATH
            if id_or_name is None
            else f"{self.ENTITY_PATH}/{id_or_name}"
        )

        response_data = self.client.request("PUT", endpoint, False, json=data)
        return KongWorkspace(response_data)
