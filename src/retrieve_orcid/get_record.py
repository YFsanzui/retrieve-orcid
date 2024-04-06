"""Retrieve ORCID record from ORCID API
"""
import requests
import datetime
from .model import Work
from argparse import ArgumentParser

BASE_URL = "https://pub.orcid.org"

def get_record(researcher_id: str, api_version: str ="v3.0") -> dict:
    """Get the record of a researcher from ORCID

    Args:
        researcher_id (str): researcher's ORCID
        api_version (str, optional): ORCID API version. Defaults to "v3.0".

    Returns:
        dict: JSON response from ORCID API
    """
    url = f"{BASE_URL}/{api_version}/{researcher_id}/record"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("researcher_id", help="ORCID of the researcher")
    args = parser.parse_args()
    record = get_record(args.researcher_id)
    print(record)