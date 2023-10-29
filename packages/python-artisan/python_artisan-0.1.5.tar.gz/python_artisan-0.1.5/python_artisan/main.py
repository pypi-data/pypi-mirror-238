import io
import os
import re
import shutil
import subprocess
import zipfile

import requests
import typer
from alembic import command
from alembic.config import Config

alembic_cfg = Config("alembic.ini")

app = typer.Typer()
model_app = typer.Typer()
app.add_typer(model_app, name="model")

handler_app = typer.Typer()
app.add_typer(handler_app, name="handler")

migrate_app = typer.Typer()
app.add_typer(migrate_app, name="migrate")

request_app = typer.Typer()
app.add_typer(request_app, name="request")

response_app = typer.Typer()
app.add_typer(response_app, name="response")

db_app = typer.Typer()
app.add_typer(db_app, name="db")


def run_poetry_command(command):
    try:
        result = subprocess.run(
            ["poetry", command], capture_output=True, text=True, check=True
        )

        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command output:", e.output)


def is_valid_folder_name(name):
    """
    Check if a given string is a valid folder name.
    """

    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-")

    return all(char in valid_chars for char in name)


@model_app.command("create")
def model_create(name: str):
    home_directory = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(home_directory, "stubs", "model")

    source_file_name = "default.stub"
    source_file_name = os.path.join(result, source_file_name)

    current_directory = os.getcwd()
    source_file_path = source_file_name

    user_input_filename = name + ".py"
    destination_filename = re.sub(r"\d", "", user_input_filename).lower()
    parent_folder = "app"
    destination_folder = "models"
    destination_folder = os.path.join(parent_folder, destination_folder)

    destination_file_path = os.path.join(
        current_directory, destination_folder, destination_filename
    )

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created '{destination_folder}' folder.")

        if not os.path.exists(destination_file_path):
            with open(source_file_path, "r") as source_file:
                handler_stub_content = source_file.read()

            updated_content = handler_stub_content.replace(
                "{{name}}", name.capitalize()
            )

            with open(destination_file_path, "w") as destination_file:
                destination_file.write(updated_content)

            print(f"File '{destination_file_path}' created successfully.")
        else:
            print(f"File '{destination_file_path}' already exists. Skipping creation.")

    except FileNotFoundError:
        print(f"File '{source_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@model_app.command("delete")
def model_delete(file_name: str):
    parent_folder = "app"
    folder_path = "models"
    folder_path = os.path.join(parent_folder, folder_path)
    file_name = file_name + ".py"
    file_name = os.path.join(folder_path, file_name)
    file_path = os.path.join(os.getcwd(), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(
            f'File "{file_path}" in the current working directory deleted successfully.'
        )
    else:
        print(
            f'File "{file_path}" in the current working directory does not exist. No deletion needed.'
        )


@handler_app.command("create")
def handler_create(
    name: str,
    subscribe: str = typer.Option(None, "--subscribe", "-s", help="Subscribe option"),
    publish: str = typer.Option(None, "--publish", "-p", help="Publish option"),
):
    home_directory = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(home_directory, "stubs", "handler")

    if subscribe and publish:
        source_file_name = "sqs_both.stub"
    elif subscribe:
        source_file_name = "sqs_subscribe.stub" if subscribe == "sqs" else "sns.stub"
    elif publish:
        source_file_name = "sqs_publish.stub"
    else:
        source_file_name = "default.stub"
        print("No specific option chosen.")

    source_file_name = os.path.join(result, source_file_name)
    current_directory = os.getcwd()
    source_file_path = source_file_name

    user_input_filename = name + ".py"
    destination_filename = re.sub(r"\d", "", user_input_filename).lower()
    destination_folder = "handlers"
    destination_file_path = os.path.join(
        current_directory, destination_folder, destination_filename
    )

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created '{destination_folder}' folder.")

        # Check if destination file already has the needed code
        if os.path.exists(destination_file_path):
            with open(destination_file_path, "r") as dest_file:
                dest_content = dest_file.read()

                if "{{ sqs_listen }}" in dest_content and subscribe:
                    print(
                        "Destination already has SQS subscription placeholder. Consider updating manually."
                    )
                    return

                if "{{ sqs_publish }}" in dest_content and publish:
                    print(
                        "Destination already has SQS publishing placeholder. Consider updating manually."
                    )
                    return

        with open(source_file_path, "r") as source_file:
            handler_stub_content = source_file.read()

            if subscribe or (subscribe and publish):
                match_subscribe = re.search(
                    r"^( *)\{\{ sqs_listen \}\}", handler_stub_content, re.MULTILINE
                )
                if match_subscribe:
                    indentation = match_subscribe.group(1)
                    with open(
                        os.path.join(result, "sqs_listen.stub"), "r"
                    ) as insert_file:
                        code_to_insert = insert_file.read()
                    indented_code_to_insert = indentation + code_to_insert.replace(
                        "\n", "\n" + indentation
                    )
                    handler_stub_content = handler_stub_content.replace(
                        match_subscribe.group(0), indented_code_to_insert, 1
                    )

            if publish or (subscribe and publish):
                match_publish = re.search(
                    r"^( *)\{\{ sqs_trigger \}\}", handler_stub_content, re.MULTILINE
                )
                if match_publish:
                    indentation = match_publish.group(1)
                    with open(
                        os.path.join(result, "sqs_trigger.stub"), "r"
                    ) as insert_file:
                        code_to_insert = insert_file.read()
                    indented_code_to_insert = indentation + code_to_insert.replace(
                        "\n", "\n" + indentation
                    )
                    handler_stub_content = handler_stub_content.replace(
                        match_publish.group(0), indented_code_to_insert, 1
                    )

        with open(destination_file_path, "w") as destination_file:
            destination_file.write(handler_stub_content)

        print(f"File '{destination_file_path}' updated successfully.")

    except FileNotFoundError:
        print(f"File '{source_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@handler_app.command("delete")
def handler_delete(file_name: str):
    folder_path = "handlers"
    file_name = file_name + ".py"
    file_name = os.path.join(folder_path, file_name)
    file_path = os.path.join(os.getcwd(), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(
            f'File "{file_path}" in the current working directory deleted successfully.'
        )
    else:
        print(
            f'File "{file_path}" in the current working directory does not exist. No deletion needed.'
        )


@request_app.command("create")
def request(name: str):
    home_directory = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(home_directory, "stubs", "request")

    source_file_name = "default.stub"
    source_file_name = os.path.join(result, source_file_name)

    current_directory = os.getcwd()
    source_file_path = source_file_name

    user_input_filename = name + ".py"
    destination_filename = re.sub(r"\d", "", user_input_filename).lower()
    parent_folder = "app"
    destination_folder = "requests"
    destination_folder = os.path.join(parent_folder, destination_folder)
    destination_file_path = os.path.join(
        current_directory, destination_folder, destination_filename
    )

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created '{destination_folder}' folder.")

        if not os.path.exists(destination_file_path):
            with open(source_file_path, "r") as source_file:
                handler_stub_content = source_file.read()

            updated_content = handler_stub_content.replace(
                "{{name}}", name.capitalize()
            )

            with open(destination_file_path, "w") as destination_file:
                destination_file.write(updated_content)

            print(f"File '{destination_file_path}' created successfully.")
        else:
            print(f"File '{destination_file_path}' already exists. Skipping creation.")

    except FileNotFoundError:
        print(f"File '{source_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@request_app.command("delete")
def request_delete(file_name: str):
    parent_folder = "app"
    folder_path = "requests"
    folder_path = os.path.join(parent_folder, folder_path)
    file_name = file_name + ".py"
    file_name = os.path.join(folder_path, file_name)
    file_path = os.path.join(os.getcwd(), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(
            f'File "{file_path}" in the current working directory deleted successfully.'
        )
    else:
        print(
            f'File "{file_path}" in the current working directory does not exist. No deletion needed.'
        )


@migrate_app.command("upgrade")
def migrate_upgrade():
    command.upgrade(alembic_cfg, "head")

    print("Migration installed")


@migrate_app.command("create")
def migrate_create(
    message: str = typer.Option("", "--message", "-m", help="Message option"),
):
    command.revision(alembic_cfg, message=message)

    print("Migration created")


@migrate_app.command("downgrade")
def migrate_downgrade():
    command.downgrade(alembic_cfg, "base")

    print("Migration erased")


@migrate_app.command("refresh")
def migrate_refresh():
    print("Refresh migration data")


@migrate_app.command("rollback")
def migrate_refresh():
    print("Rollback migration data")


@db_app.command("drop")
def db_drop():
    print("Dropping the database")


@db_app.command("seed")
def db_seed():
    print("Seeding the database")


@db_app.command("wipe")
def db_wipe():
    print("Wiping the database")


@app.command("serve")
def serve(port: int = typer.Option(8000, "--port", "-p", help="Set port number")):
    poetry_command = f"poetry run uvicorn public.main:app --reload --port {port}"

    try:
        subprocess.run(poetry_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running serving the app")


@app.command("init")
def app_create(project_name: str):
    repository_name = "artisan-framework"

    if os.path.exists(project_name):
        print(f"The {project_name} folder already exists. Aborting.")
    elif not is_valid_folder_name(project_name):
        print(f"{project_name} is not a valid project name. Aborting.")
    else:
        release_url = f"https://github.com/nerdmonkey/{repository_name}/archive/refs/heads/main.zip"

        response = requests.get(release_url)

        if response.status_code == 200:
            zip_data = io.BytesIO(response.content)

            temp_folder = "temp_extracted_folder"
            with zipfile.ZipFile(zip_data, "r") as zip_ref:
                zip_ref.extractall(temp_folder)

            extracted_files = os.listdir(temp_folder)
            if len(extracted_files) == 1 and os.path.isdir(
                os.path.join(temp_folder, extracted_files[0])
            ):
                extracted_folder = os.path.join(temp_folder, extracted_files[0])
                os.rename(extracted_folder, project_name)

                print(f"Successfully setup the project to {project_name}.")

                shutil.rmtree(temp_folder)

                print(f"\nTODO:")
                print(f"-----")
                print(f"cd {project_name}")
                print(f"pip install")
                print(f"copy the .env.example and save it as .env")
                print(f"uvicorn public.main:app --reload")
            else:
                print("Error: The ZIP file should contain a single top-level folder.")
        else:
            print(f"Failed to setup the project. Status code: {response.status_code}")


@response_app.command("create")
def response_create(name: str):
    home_directory = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(home_directory, "stubs", "response")

    source_file_name = "default.stub"
    source_file_name = os.path.join(result, source_file_name)

    current_directory = os.getcwd()
    source_file_path = source_file_name

    user_input_filename = name + ".py"
    destination_filename = re.sub(r"\d", "", user_input_filename).lower()
    parent_folder = "app"
    destination_folder = "responses"
    destination_folder = os.path.join(parent_folder, destination_folder)
    destination_file_path = os.path.join(
        current_directory, destination_folder, destination_filename
    )

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created '{destination_folder}' folder.")

        if not os.path.exists(destination_file_path):
            with open(source_file_path, "r") as source_file:
                handler_stub_content = source_file.read()

            updated_content = handler_stub_content.replace("{{file_name}}", name)
            updated_content = updated_content.replace("{{name}}", name.capitalize())

            with open(destination_file_path, "w") as destination_file:
                destination_file.write(updated_content)

            print(f"File '{destination_file_path}' created successfully.")
        else:
            print(f"File '{destination_file_path}' already exists. Skipping creation.")

    except FileNotFoundError:
        print(f"File '{source_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@response_app.command("delete")
def request_delete(file_name: str):
    parent_folder = "app"
    folder_path = "responses"
    folder_path = os.path.join(parent_folder, folder_path)
    file_name = file_name + ".py"
    file_name = os.path.join(folder_path, file_name)
    file_path = os.path.join(os.getcwd(), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(
            f'File "{file_path}" in the current working directory deleted successfully.'
        )
    else:
        print(
            f'File "{file_path}" in the current working directory does not exist. No deletion needed.'
        )


if __name__ == "__main__":
    app()
