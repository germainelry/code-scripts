import json
from datetime import datetime, timedelta
import re

def clean_input(input_string, default_list=None, to_lowercase=False):
    """
    Cleans and validates a user input string, splitting it into a list of cleaned values.
    Accepts delimiters like commas, semicolons, spaces, line breaks, and tabs.
    Converts items to lowercase if 'to_lowercase' is True.
    """
    if default_list is None:
        default_list = []
    # Split by common delimiters (comma, semicolon, space, line break, tab)
    cleaned_list = re.split(r'[,\n;\t ]+', input_string.strip())
    # Remove empty strings and duplicates
    cleaned_list = [item.strip() for item in cleaned_list if item.strip()]
    # Convert to lowercase if required
    if to_lowercase:
        cleaned_list = [item.lower() for item in cleaned_list]
    return list(set(default_list + cleaned_list))

def generate_json():
    # Prompting user for inputs
    crq = input("Enter the CRQ number (e.g., CRQ000000913562): ")
    purpose = input("Enter the purpose of the deployment: ")
    cookname = input("Enter the Chef cookbook name (cookname): ")
    
    # Default emails
    default_emails = ["sggpisinfraautomationprocessengineering@uobgroup.com"]
    additional_emails = input("Enter additional email addresses (separated by commas, semicolons, spaces, or line breaks). Press Enter if none: ")
    emails = clean_input(additional_emails, default_list=default_emails)
    
    server_input = input("Enter the list of servers (separated by commas, semicolons, spaces, or line breaks): ")
    servers = clean_input(server_input, to_lowercase=True)
    
    specific_recipe = input(f"Do you want a specific recipe different from '{cookname}'? Enter recipe name or press Enter to use default: ")

    # Default values for schedules
    current_time = datetime.now()
    run_date = current_time.strftime("%d/%m/%Y")
    start_time = (current_time + timedelta(hours=1)).strftime("%H:%M")
    end_time = (current_time + timedelta(hours=3)).strftime("%H:%M")
    recipes = [specific_recipe.strip()] if specific_recipe else [cookname]

    # Creating the JSON structure
    json_data = {
        "CRQ": crq,
        "purpose": purpose,
        "type": "cookbook",
        "cookname": cookname,
        "email": emails,
        "servers": servers,
        "schedules": [
            {
                "run_date": run_date,
                "start_time": start_time,
                "end_time": end_time,
                "recipes": recipes
            }
        ]
    }

    # Path to save the file
    file_directory = "/Users/germaineluah/Documents/Documents - Germaine’s MacBook Air/code/uob-code/created-crqs/"
    file_name = f"{crq}.json"
    file_path = file_directory + file_name

    try:
        # Saving JSON to a file
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON file has been successfully saved to {file_path}")
    except FileNotFoundError:
        print(f"Error: Could not save the file. Ensure the directory '{file_directory}' exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_json()