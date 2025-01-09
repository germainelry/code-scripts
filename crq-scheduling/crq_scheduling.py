import json
import os
from datetime import datetime, timedelta
import re
import logging
import secrets  # Import the secrets.py file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_DIRECTORY = "C:\\Users\\OPSRO1\\Desktop\\code\\CRQ Scheduling\\created-crqs" # input directory to save .json files to
DEFAULT_EMAILS = secrets.DEFAULT_EMAILS  # Use the email list from secrets.py


def clean_input(input_string: str, default_list: list = None, to_lowercase: bool = False) -> list:
    if default_list is None:
        default_list = []
    cleaned_list = re.split(r'[,;\t ]+', input_string.strip())
    cleaned_list = [item.strip().strip('"').strip("'") for item in cleaned_list if item.strip()]
    if to_lowercase:
        cleaned_list = [item.lower() for item in cleaned_list]
    seen = set()
    return [item for item in default_list + cleaned_list if not (item in seen or seen.add(item))]


def clean_servers(input_string: str, naming_pattern: str = r'[a-z]+[a-z]{2}[a-z]?[a-z]{2}[v]?\d+') -> list:
    """
    Cleans and splits server input based on the organization's naming convention.
    Extracts server names matching the provided regex pattern.

    Parameters:
    - input_string: Raw input containing server names.
    - naming_pattern: Regex pattern to match valid server names.

    Returns:
    - A list of valid server names.
    """
    # Find all matches for server names in the concatenated string
    servers = re.findall(naming_pattern, input_string.strip().lower())
    # Remove duplicates while preserving order
    seen = set()
    return [server for server in servers if not (server in seen or seen.add(server))]

def clean_recipes(input_string: str, cookname: str) -> list:
    """
    Cleans and processes recipe input to generate a list of recipes in JSON format.
    Each recipe is prefixed by the provided cookbook name (cookname).
    If no specific recipes are provided, defaults to just the cookname.
    """
    if not input_string.strip():
        return [cookname]  # Default to cookname if no recipes are specified
    recipes = re.split(r'[,;\t ]+', input_string.strip())
    recipes = [recipe.strip() for recipe in recipes if recipe.strip()]
    return [f"{cookname}::{recipe}" for recipe in recipes]


def validate_json(data: dict) -> bool:
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError) as e:
        logging.error(f"JSON validation error: {e}")
        return False


def get_schedule() -> tuple:
    current_time = datetime.now()
    default_run_date = current_time.strftime("%d/%m/%Y")
    default_start_time = (current_time + timedelta(hours=1)).strftime("%H:%M")
    default_end_time = (current_time + timedelta(hours=3)).strftime("%H:%M")

    while True:
        run_date = input(f"Enter run date (DD/MM/YYYY) [Default: {default_run_date}]: ") or default_run_date
        try:
            datetime.strptime(run_date, "%d/%m/%Y")
        except ValueError:
            logging.error("Invalid date format. Use DD/MM/YYYY.")
            continue

        start_time = input(f"Enter start time (HH:MM) [Default: {default_start_time}]: ") or default_start_time
        end_time = input(f"Enter end time (HH:MM) [Default: {default_end_time}]: ") or default_end_time

        try:
            start_dt = datetime.strptime(f"{run_date} {start_time}", "%d/%m/%Y %H:%M")
            end_dt = datetime.strptime(f"{run_date} {end_time}", "%d/%m/%Y %H:%M")
            if (end_dt - start_dt).total_seconds() < 3600:
                logging.error("End time must be at least 1 hour after start time.")
            else:
                return run_date, start_time, end_time
        except ValueError:
            logging.error("Invalid time format. Use HH:MM.")


def get_recipe_schedules(recipes: list) -> list:
    """
    Prompts the user to specify unique schedules for each recipe or use default values.
    Parameters:
    - recipes: List of recipes to schedule.

    Returns:
    - A list of dictionaries, each containing a recipe and its schedule.
    """
    schedules = []
    default_run_date = datetime.now().strftime("%d/%m/%Y")
    default_start_time = (datetime.now() + timedelta(hours=1)).strftime("%H:%M")
    default_end_time = (datetime.now() + timedelta(hours=3)).strftime("%H:%M")

    for recipe in recipes:
        print(f"\nConfiguring schedule for recipe: {recipe}")
        use_default = input("Do you want to use the default schedule? (y/n): ").strip().lower()

        if use_default == 'y':
            # Use static defaults for the schedule
            run_date = default_run_date
            start_time = default_start_time
            end_time = default_end_time
        else:
            # Prompt user for a custom schedule
            while True:
                run_date = input(f"Enter run date for {recipe} (DD/MM/YYYY): ").strip()
                try:
                    datetime.strptime(run_date, "%d/%m/%Y")
                except ValueError:
                    print("Invalid date format. Use DD/MM/YYYY.")
                    continue

                start_time = input(f"Enter start time for {recipe} (HH:MM): ").strip()
                end_time = input(f"Enter end time for {recipe} (HH:MM): ").strip()

                try:
                    start_dt = datetime.strptime(f"{run_date} {start_time}", "%d/%m/%Y %H:%M")
                    end_dt = datetime.strptime(f"{run_date} {end_time}", "%d/%m/%Y %H:%M")
                    if (end_dt - start_dt).total_seconds() >= 3600:
                        break  # Valid schedule
                    else:
                        print("Error: End time must be at least 1 hour after start time.")
                except ValueError:
                    print("Invalid time format. Use HH:MM.")

        # Append schedule for the recipe
        schedules.append({
            "run_date": run_date,
            "start_time": start_time,
            "end_time": end_time,
            "recipes": recipe
        })

    return schedules


def generate_json():
    crq = input("Enter the CRQ number (e.g., CRQ000000913562): ").strip()
    if not re.match(r"^CRQ\d+$", crq):
        logging.error("Invalid CRQ format.")
        return

    purpose = input("Enter the purpose of the deployment: ").strip()
    cookname = input("Enter the Chef cookbook name: ").strip()

    additional_emails = input("Enter additional email addresses (separated by commas): ")
    emails = clean_input(additional_emails, default_list=DEFAULT_EMAILS)
    email_string = ",".join(emails)

    server_input = input("Enter the list of servers (can include pasted column data or no delimiters): ")
    servers = clean_servers(server_input)

    specific_recipe_input = input(f"Enter specific recipes for '{cookname}' (separated by commas, spaces, etc.) or press Enter to skip: ")
    recipes = clean_recipes(specific_recipe_input, cookname)

    # Handle scheduling for recipes
    recipe_schedules = get_recipe_schedules(recipes)

    json_data = {
        "CRQ": crq,
        "purpose": purpose,
        "type": "cookbook",
        "cookname": cookname,
        "email": email_string,
        "servers": servers,
        "schedules": recipe_schedules
    }

    if not validate_json(json_data):
        logging.error("Generated JSON is invalid.")
        return

    os.makedirs(DEFAULT_DIRECTORY, exist_ok=True)
    file_path = os.path.join(DEFAULT_DIRECTORY, f"{crq}.json")

    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        logging.info(f"JSON file saved: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON file: {e}")


if __name__ == "__main__":
    generate_json()
