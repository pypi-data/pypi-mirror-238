import os
from pathlib import Path
from typing import Dict

import pandas as pd
import requests
from rich.progress import track

from extractor.checks import StandardCheck
from extractor.logger import logger
from extractor.render import Requirements

URLBASE = "https://pypi.org/pypi"


def get_raw_data(project: str) -> Dict[str, str]:
    """
    Retrieve raw metadata for a project from a given URL.

    Args:
        project: The name of the project.

    Returns:
        A dictionary containing the raw metadata of the project.
    """
    try:
        r = requests.get(
            f"{URLBASE}/{project}/json", headers={"Accept": "application/json"}
        )
    except Exception as e:
        logger.error(e)
    else:
        if r.status_code == 404:
            logger.error(f"Project {project} not found")
            return {}
        return r.json()["info"]


def filter_data(raw_data: Dict[str, str], version: str) -> Dict[str, str]:
    """
    Filter relevant metadata from raw data.

    Args:
        raw_data: The raw metadata of a project.
        version: The version of the project.

    Returns:
        A dictionary containing filtered metadata.
    """
    if raw_data:
        project_name = raw_data["name"]
        project_url = raw_data["project_url"]
        project_urls = raw_data["project_urls"]
        project_version = version or raw_data["version"]
        check = StandardCheck()
        pypi_url = f"https://pypi.org/project/{project_name}/{project_version}/"
        gh_url_pattern = r"(https:\/\/|http:\/\/)github\.com"
        filtered_data = {
            "name": project_name,
            "version": project_version,
            "license": check.licenses(raw_data),
            # "homepage": raw_data["home_page"],
            "pypi_release_url": pypi_url,
            "project_url": check.project_url(gh_url_pattern, project_url, project_urls),
        }

        logger.info(f"Searching GitHub url for: {project_name}")

        filtered_data = check.version(version, gh_url_pattern, filtered_data)
        del filtered_data["project_url"]
        return filtered_data

    return {}


def extract_data(source_path: Path, format: str) -> None:
    """
    Extract data based on the specified requirements format.

    Args:
        source_path: The path to the requirements file.
        format: The format of the requirements file.

    Returns:
        pd.DataFrame
    """
    logger.info("Starting process")
    logger.debug(f"Retrieving: {source_path}")
    result = Requirements().render(source_path, format)
    custom_columns_order = ["license", "name"]
    pkgs_raw_metadata = []
    for pkg in track(result):
        filtered_data = filter_data(
            get_raw_data(pkg[0]), pkg[1] if len(pkg) > 1 else None
        )
        if filtered_data:
            pkgs_raw_metadata.append(filtered_data)
    return pd.DataFrame(pkgs_raw_metadata).sort_values(by=custom_columns_order)


def save_data(data: pd.DataFrame, output: Path):
    # Extract directory from the output string
    output_directory = os.path.dirname(output)
    logger.info(f"Storing into: {output}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if str(output).endswith(".csv"):
        data.to_csv(output, index=False)
        logger.info("All done! Have a Great day")
    elif str(output).endswith(".xlsx"):
        data.to_excel(output, index=False)
        logger.info("All done! Have a Great day")
    else:
        logger.error("Not supported format.")
