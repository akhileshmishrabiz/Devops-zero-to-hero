import os
import subprocess
from typing import List

def run_pipreqs(folder: str):
    """Run the pipreqs command for a given folder."""
    try:
        result = subprocess.run(["pipreqs", folder], check=True, capture_output=True, text=True)
        print(f"Successfully ran pipreqs for {folder}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run pipreqs for {folder}")
        print(e.stderr)

def find_subfolders(base_folder: str) -> List[str]:
    """Find all subfolders one level down in the specified base folder."""
    subfolders = []
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            subfolder = os.path.join(root, dir_name)
            if os.path.dirname(subfolder) == base_folder:  # Ensure only one level down
                subfolders.append(subfolder)
        break  # Prevents descending into subdirectories
    return subfolders

def read_requirements_file(file_path: str) -> List[str]:
    """Read a requirements.txt file and return its contents as a list of lines."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def remove_empty_requirements(file_path: str):
    """Remove a requirements.txt file if it is empty."""
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        os.remove(file_path)
        print(f"Removed empty {file_path}")

def main():
    base_folder = "lambda"
    subfolders = find_subfolders(base_folder)
    consolidated_requirements = []

    # Run pipreqs for each subfolder
    for folder in subfolders:
        run_pipreqs(folder)
        requirements_file = os.path.join(folder, "requirements.txt")
        if os.path.exists(requirements_file):
            # Read the contents of the requirements.txt file
            requirements = read_requirements_file(requirements_file)
            if requirements:
                consolidated_requirements.extend(requirements)
            # Remove the requirements.txt file if it is empty
            remove_empty_requirements(requirements_file)

    # Print the consolidated output of all requirements.txt files
    if consolidated_requirements:
        print("\nConsolidated requirements.txt content:")
        print("".join(consolidated_requirements))

if __name__ == "__main__":
    main()
