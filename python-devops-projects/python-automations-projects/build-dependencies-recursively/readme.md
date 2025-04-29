## Blog: Automating Dependency Management for Lambda Functions

In the dynamic world of software development, managing dependencies is a crucial aspect that ensures the smooth functioning of applications. Imagine you're working on a project that involves multiple AWS Lambda functions, each residing in its own directory. As the project grows, so does the complexity of managing dependencies for each function. Manually maintaining `requirements.txt` files for each Lambda function can be a tedious and error-prone process.

To address this challenge, automation comes to the rescue. By leveraging tools like `pipreqs`, which generates `requirements.txt` files based on the imports in your code, we can streamline the process. However, running `pipreqs` individually for each Lambda function folder and consolidating the results still requires some manual effort.

This blog post introduces a Python script that automates the entire process. It traverses through the Lambda function directories, runs `pipreqs`, removes any empty `requirements.txt` files, and prints a consolidated list of all dependencies. This not only saves time but also reduces the likelihood of errors, ensuring that your Lambda functions have the necessary dependencies defined.

Let's dive into the solution and see how you can automate dependency management for your Lambda functions.

---

## Automated Dependency Management for AWS Lambda Functions

### Introduction
This script automates the generation and management of `requirements.txt` files for multiple AWS Lambda function directories. It uses `pipreqs` to generate the dependency files based on the imports in your code, removes any empty `requirements.txt` files, and prints a consolidated list of all dependencies.

### Prerequisites
- Python 3.x
- `pipreqs` package (`pip install pipreqs`)

### Script Overview
The script performs the following tasks:
1. **Finds Subfolders**: Traverses through the specified base folder (`lambda`) and finds all subfolders one level down.
2. **Runs pipreqs**: Executes the `pipreqs` command for each subfolder to generate `requirements.txt` files.
3. **Removes Empty Files**: Deletes any empty `requirements.txt` files.
4. **Consolidates Dependencies**: Prints a consolidated list of dependencies from all `requirements.txt` files.

### Usage
Save the script in a file, for example `generate_requirements.py`, and run it from the root directory of your project.

```python
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
```

### How It Works
1. **Initialization**: The script starts by defining the base folder (`lambda`) where the Lambda function directories are located.
2. **Finding Subfolders**: It traverses the base folder to find all subfolders one level down.
3. **Running pipreqs**: For each subfolder, it runs `pipreqs` to generate the `requirements.txt` file.
4. **Removing Empty Files**: It checks if the generated `requirements.txt` file is empty and removes it if so.
5. **Consolidating Dependencies**: It reads the contents of all `requirements.txt` files and prints a consolidated list of dependencies.

### Conclusion
This script automates the management of dependencies for multiple AWS Lambda functions, ensuring that each function has the necessary dependencies defined in its `requirements.txt` file. By removing empty files and consolidating dependencies, it provides a clean and efficient way to handle dependencies for your Lambda functions.
