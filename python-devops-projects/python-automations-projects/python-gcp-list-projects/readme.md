This Python script leverages Google Cloud's Resource Manager v3 API to list all active projects within a specified organization. It defines three main functions: get_folders to recursively fetch all folder IDs, search_projects to retrieve projects within a given folder, and list_projects to compile a list of active project IDs. By running this script, users can easily identify and manage active projects across their organization's hierarchy.

Here is the Medium blog with the instruction:

https://medium.com/living-devops/exploring-google-resource-manager-with-python-v1-0-ea0aeab57c53


# Google Cloud Resource Manager Script

This Python script helps in identifying and listing all active projects within a specified Google Cloud organization. It leverages Google Cloud's Resource Manager v3 API to traverse through folders and subfolders, gathering information on all active projects.

## Features

- Recursively fetches all folder IDs within an organization.
- Retrieves a list of project objects under each folder.
- Compiles a list of active project IDs across the entire organization.

## Prerequisites

- Python 3.7 or higher
- Google Cloud SDK
- `google-cloud-resource-manager` Python package

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/akhileshmishrabiz/python-for-devops
    cd python-gcp-list-projects
    ```

2. Install the required packages:
    ```sh
    pip install google-cloud-resource-manager
    ```

3. Authenticate with Google Cloud:
    ```sh
    gcloud auth application-default login
    ```

## Usage

1. Update the script with your organization ID by replacing `"organizations/ORGANIZATION_ID"` with your actual organization ID.
2. Run the script:
    ```sh
    python script.py
    ```

## Code Overview

- **get_folders**: Recursively retrieves all folder IDs under a specified parent organization or folder.
- **search_projects**: Retrieves a list of project objects within a given folder ID.
- **list_projects**: Compiles and returns a list of active project IDs by traversing through all folders and subfolders.

## Example

```sh
python script.py
