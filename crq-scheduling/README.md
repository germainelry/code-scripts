# CRQ Scheduling Script

This Python script is designed to automate the generation of JSON files for scheduling Chef cookbook deployments based on user input. The script facilitates the creation of deployment schedules for multiple servers and recipes, which are used to trigger Chef run lists for Infrastructure as Code (IaC) deployments.

## Features

- Clean user inputs (e.g., email addresses, server names, recipes).
- Schedule Chef cookbook deployments with flexible time configurations.
- Generate a JSON file with deployment details, including CRQ number, email recipients, servers, recipes, and schedules.
- Logs user activity for troubleshooting and auditing purposes.
- Default directory for saving generated JSON files.

## Requirements

- Python 3.x
- Basic understanding of Chef, CRQ scheduling, and JSON file generation.
- A terminal or command-line interface to run the script.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/crq-scheduling.git
    ```

2. Navigate into the project directory:

    ```bash
    cd crq-scheduling
    ```

3. (Optional) Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```
4. How to Stop Tracking a Sensitive File in Git

    If you do not want to track a sensitive file (such as `your-sensitive-file.json`), follow these steps:
    
    1. Add the file to `.gitignore`:
       - Open the `.gitignore` file in your project root. If it doesn't exist, create a new file named `.gitignore`.
       - Add the following line to ignore your sensitive file (replace `your-sensitive-file.json` with the actual file name):
         ```
         your-sensitive-file.json
         ```
       - Save the `.gitignore` file.
    
    2. Stop Git from Tracking the File:
       If the file is already being tracked by Git, you'll need to remove it from Git's index. Run the following command in your terminal (replace `your-sensitive-file.json` with the actual file name):
       ```
       git rm --cached your-sensitive-file.json
       ```
       This will stop Git from tracking the file, but it will remain on your local machine.
    
    3. Commit the Changes:
       After updating the `.gitignore` file and removing the file from tracking, commit the changes:
       ```
       git add .gitignore
       git commit -m "Stop tracking your-sensitive-file.json"
       ```
    
    4. Push the Changes:
       Finally, push the changes to the remote repository:
       ```
       git push
       ```
    After completing these steps, Git will no longer track `your-sensitive-file.json` (or any sensitive file you specify), and it will be ignored in      future commits.

5. Ensure you have any required dependencies (if applicable).

## Usage

1. Run the script:

    ```bash
    python crq_scheduling.py
    ```

2. The script will prompt you for the following inputs:
    - **CRQ number**: A unique identifier for the change request.
    - **Purpose**: The reason for the deployment.
    - **Cookbook name**: The name of the Chef cookbook to be scheduled.
    - **Email addresses**: Additional email addresses (if applicable).
    - **Server list**: A list of servers for the deployment.
    - **Specific recipes**: Optional recipes that should be included in the Chef run.
    - **Scheduling details**: The date and time for the deployment.

3. After inputting all the required information, the script generates a JSON file with the provided data and saves it in the default directory.

4. Logs will be printed to the terminal, providing feedback and error messages if needed.

## Logging

The script logs important events and errors using the Python logging module. By default, logs will be printed to the terminal, including:
- **INFO** messages for successful operations.
- **ERROR** messages for invalid inputs or failures.

## Customization

- You can modify the default directory and email list by editing the `DEFAULT_DIRECTORY` and `DEFAULT_EMAILS` variables in the script.
- If you wish to store sensitive information like email addresses or API keys, it's recommended to store them in a separate `secrets.py` file. This file should not be committed to version control (e.g., add `secrets.py` to `.gitignore`).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to your branch (`git push origin feature-branch`).
6. Open a pull request.

## Acknowledgements

- Python for automating the scheduling process.
- Chef for providing the infrastructure automation platform.
