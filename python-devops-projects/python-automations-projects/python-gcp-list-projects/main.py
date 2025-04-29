from google.cloud import resourcemanager_v3

def get_folders(parent_id="organizations/ORGANIZATION_ID", folders=None):
    """
    Recursively retrieves a list of folder IDs for all folders and subfolders within the given parent ID.

    Args:
        parent_id (str): The ID of the parent organization or folder. Defaults to "organizations/ORGANIZATION_ID".
        folders (list, optional): A list to store the folder IDs. Defaults to None.

    Returns:
        list: A list of folder IDs.
    """
    # Initialize the folders list if it is None
    if folders is None:
        folders = []

    # Create a client for the Resource Manager v3 API
    client = resourcemanager_v3.FoldersClient()
    
    # Create a request to list folders under the specified parent
    request = resourcemanager_v3.ListFoldersRequest(parent=parent_id)

    # Execute the request and get the results
    page_result = client.list_folders(request=request)
    for pages in page_result:
        # Append each folder ID to the folders list
        folders.append(pages.name)
        # Recursively call get_folders for each subfolder
        get_folders(parent_id=pages.name, folders=folders)

    return folders

def search_projects(folder_id):
    """
    Retrieves a list of project objects under a given folder ID.

    Args:
        folder_id (str): The ID of the folder to search for projects.

    Returns:
        list: A list of project objects.
    """
    # Create a client for the Resource Manager v3 API
    client = resourcemanager_v3.ProjectsClient()

    # Create a query to search for projects within the specified folder
    query = f"parent:{folder_id}"
    request = resourcemanager_v3.SearchProjectsRequest(query=query)

    # Execute the request and get the results
    page_result = client.search_projects(request=request)
    search_result = []
    for pages in page_result:
        # Append each project object to the search_result list
        search_result.append(pages)

    return search_result

def list_projects():
    """
    Retrieves a list of all active project IDs within the organization.

    Returns:
        list: A list of active project IDs.
    """
    active_project = []
    # Get all folders and subfolders within the organization
    for folders in get_folders(parent_id="organizations/ORGANIZATION_ID", folders=None):
        # Search for projects within each folder
        for projects in search_projects(folders):
            # Check if the project is active and append its ID to the active_project list
            if str(projects.state) == "State.ACTIVE":
                active_project.append(projects.project_id)

    return active_project

if __name__ == "__main__":
    # Print the list of all active project IDs
    print(list_projects())
