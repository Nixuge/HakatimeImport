import os
import re


def replace_base_path(file_path: str):
        # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Define the pattern to search for the base path section
    pattern = r'# START BASE PATH\nBASE_PATH = ".*"\n# END BASE PATH'

    # Create the replacement string
    replacement = f'# START BASE PATH\nBASE_PATH = "{os.getcwd()}"\n# END BASE PATH'

    # Replace the old base path with the new one
    new_content = re.sub(pattern, replacement, content)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)