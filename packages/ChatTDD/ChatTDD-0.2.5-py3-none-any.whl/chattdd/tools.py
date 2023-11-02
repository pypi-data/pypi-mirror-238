import json
import os
import base64
import ast

CONFIG_FILE_PATH = os.path.join(os.getcwd(), 'chattdd_config.json')


def write_to_file(content, filename):
    config = load_config()
    output_folder = config['OUTPUTFOLDER']
    file_path = os.path.join(output_folder, filename)
    
    # Ensure the directory exists
    directory_path = os.path.dirname(file_path)
    os.makedirs(directory_path, exist_ok=True)
    
    # Check if __init__.py exists in the directory
    init_file_path = os.path.join(directory_path, '__init__.py')
    if not os.path.exists(init_file_path):
        with open(init_file_path, 'w') as init_file:
            pass  # create an empty __init__.py file
    
    # Write the provided content to the specified file
    with open(file_path, 'w') as file:
        file.write(content)

def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        # Create config file with default values if it doesn't exist
        default_config = {
            "CHATTDD_MODEL": "text-davinci-003",
            "OUTPUTFOLDER": "ChatTDDgenerated"
        }
        with open(CONFIG_FILE_PATH, 'w') as file:
            json.dump(default_config, file, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE_PATH, 'r') as file:
            return json.load(file)


def update_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config, file, indent=4)

def is_valid_syntax(code_str):
    try:
        compile(code_str, '<string>', 'exec')
        return True
    except SyntaxError:
        return False

def parse_string_to_dict(input_str: str) -> dict:
    try:
        # First, attempt to convert the string into a Python object using ast.literal_eval
        result = ast.literal_eval(input_str)
        
        # Check if the result is a dictionary
        if isinstance(result, dict):
            # Trim whitespaces for string values
            for key, value in result.items():
                if isinstance(value, str):
                    result[key] = value.strip()
            return result

    except (ValueError, SyntaxError):
        pass

    try:
        # If ast.literal_eval fails, then try parsing as JSON
        result = json.loads(input_str)
        
        if isinstance(result, dict):
            # Trim whitespaces for string values
            for key, value in result.items():
                if isinstance(value, str):
                    result[key] = value.strip()
            return result

    except json.JSONDecodeError:
        return {"comment": input_str}

    return {"comment": input_str}

