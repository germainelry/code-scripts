import json
from datetime import datetime, timedelta

def generate_json():
    # Prompting user for inputs
    crq = input("Enter the CRQ number (e.g., CRQ000000913562): ")
    purpose = input("Enter the purpose of the deployment: ")
    cookname = input("Enter the Chef cookbook name (cookname): ")
    email = input("Enter the email addresses (comma-separated): ")
    servers = input("Enter the list of servers (comma-separated): ").split(",")
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
        "email": email,
        "servers": [server.strip() for server in servers],
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
    file_name = f"CRQ_{crq}.json"
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