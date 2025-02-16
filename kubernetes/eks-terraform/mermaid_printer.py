#!/usr/bin/env python3
import argparse
import sys
import os

def read_mermaid_file(file_path):
    """
    Read and validate a Mermaid diagram file.
    
    Args:
        file_path (str): Path to the Mermaid diagram file
    
    Returns:
        str: Content of the Mermaid file
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, 'r') as file:
            content = file.read()
            
        return content
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

def print_mermaid_diagram(content):
    """
    Print the Mermaid diagram with proper formatting.
    
    Args:
        content (str): The Mermaid diagram content
    """
    print("```mermaid")
    print(content)
    print("```")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Print a Mermaid diagram from a file with proper formatting.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
  python mermaid_printer.py diagram.mmd
  python mermaid_printer.py -f diagram.mmd
  python mermaid_printer.py --file diagram.mmd
        '''
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help='Path to the Mermaid diagram file'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Read and print the diagram
        content = read_mermaid_file(args.file)
        print_mermaid_diagram(content)
    except (FileNotFoundError, IOError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# chmod +x mermaid_printer.py
# python mermaid_printer.py -f your_diagram.mmd