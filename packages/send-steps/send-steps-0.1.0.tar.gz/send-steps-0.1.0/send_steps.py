import importlib
import json
import logging
import os
import sys
from glob import glob

import click
import requests
from dotenv import load_dotenv
from gitlab import Gitlab
from radish.customtyperegistry import CustomTypeRegistry
from radish.stepregistry import StepRegistry

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="[%(levelname)s] %(message)s")

REPO_PREFIX_LENGTH = 23
URL_PREFIX_LENGTH = 8
SERVER_URL = os.environ.get("SERVER_URL", "http://127.0.0.1:54321")


def get_link_to_repo(step, repo_url, ref):
    """Return the link to the exact location from the step in gitlab"""
    project_name = repo_url.split("/")[-1]
    code = step.__code__
    file_path = code.co_filename
    steps_file = file_path.split(project_name)[-1]
    link = f"{repo_url}/-/blob/{ref}{steps_file}"
    line = str(code.co_firstlineno)
    link = "#L".join([link, line])
    return link


def send_custom_types(custom_types):
    json_data = json.dumps(custom_types)
    url = f"{SERVER_URL}/send_custom_types"
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        logger.info("custom_types sent succesfully")
    else:
        logger.error("Error while sending custom_types", response.status_code)


def send_steps(steps, repo_url):
    repo = {"repo_name": f"{repo_url[URL_PREFIX_LENGTH:]}"}
    repo.update(steps)
    json_data = json.dumps(repo)
    url = f"{SERVER_URL}/send_steps"
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        logger.info("Steps sent succesfully")
    else:
        logger.error("Error while sending steps", response.status_code)


def get_project(gl, repo_url):
    try:
        project = gl.projects.get(f"{repo_url[REPO_PREFIX_LENGTH:]}")
        return project
    except Exception as e:
        logger.error(f"The project with URL {repo_url} could not be retrieved: {e}")
        sys.exit()


@click.command
@click.argument("repo_url")
@click.option(
    "--path",
    default=".",
    help="Path to the directory containing Python files. Default is the current directory.",
)
def main(repo_url, path):
    """
    This script sends all the radish steps and custom types, from the python-files in the current directory or in the
    directory you provide, to the server.

    Arguments:
        REPO_URL : str : URL of the repository.

    Options:
        --path : str : Path to the directory containing Python files. Default is the current directory.
    """
    absolute_path = os.path.abspath(path)
    sys.path.append(f"{absolute_path}")

    if not path.endswith("/"):
        path += "/"

    if glob(f"{path}*.py") == []:
        logger.error(f"There are no files in the path {path}")
        sys.exit()

    for filename in glob(f"{path}*.py"):
        module_name = os.path.basename(filename)[:-3]
        try:
            importlib.import_module(module_name)
        except Exception as e:
            logger.error(f"{module_name} can't be imported, because {e}")
            sys.exit()

    load_dotenv()
    GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
    gl = Gitlab("https://code.roche.com", private_token=GITLAB_TOKEN)
    gl.auth()
    project = get_project(gl, repo_url)
    ref = project.default_branch

    steps = StepRegistry().steps
    custom_types = CustomTypeRegistry().custom_types

    for key, value in custom_types.items():
        custom_types[key] = value.pattern
    send_custom_types(custom_types)

    for key, value in steps.items():
        name = value.__name__
        doc = value.__doc__
        link = get_link_to_repo(value, repo_url, ref)
        steps[key] = [name, doc, link]
    send_steps(steps, repo_url)


if __name__ == "__main__":
    main()
