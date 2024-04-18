"""Get the works of a researcher from ORCID
"""

import requests
import datetime
from .model import Work
from crossref.restful import Works as crossref_works
from argparse import ArgumentParser

BASE_URL = "https://pub.orcid.org"

def get_works(researcher_id: str, api_version: str ="v3.0") -> dict:
    """Get the works of a researcher from ORCID

    Args:
        researcher_id (str): researcher's ORCID
        api_version (str, optional): ORCID API version. Defaults to "v3.0".
        
    Returns:
        dict: JSON response from ORCID API
    """
    url = f"{BASE_URL}/{api_version}/{researcher_id}/works"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_doi(work: dict) -> str:
    """Get the DOI of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: DOI of the work
    """
    for external_id in work["external-ids"]["external-id"]:
        if external_id["external-id-type"] == "doi":
            return external_id["external-id-value"].replace('https://', '').replace('doi.org/', '')
        return None

def get_created_at(work: dict) -> str:
    """Get the created_at of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: unix timestamp of the work
    """
    ret = work["work-summary"][0]["created-date"]["value"]
    return ret

def get_created_at_date(work: dict) -> str:
    """Get the created_at of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: date of the work
    """
    ret = work["work-summary"][0]["created-date"]["value"]
    date = datetime.datetime.fromtimestamp(int(ret)/1000)
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    return date_str

def get_title(work: dict) -> str:
    """Get the title of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: title of the work
    """
    return work["work-summary"][0]["title"]["title"]["value"]

def get_journal_title(work: dict) -> str:
    """Get the journal title of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: journal title of the work
    """
    if work["work-summary"][0]["journal-title"] is None:
        return None
    return work["work-summary"][0]["journal-title"]["value"]

def get_authors(work: dict) -> str:
    """Get the names of authors of a work

    Args:
        work (dict): work response from ORCID API

    Returns:
        str: names of authors of the work
    """
    authors = ""
    
    if get_doi(work) is None:
        return "No Data"
    
    else:
        doi_url = 'https://doi.org/' + str(get_doi(work))
        crossref_work = crossref_works()
        paper = crossref_work.doi(doi_url)
        
        if type(paper) != dict:
            authors += "No Data"
            return authors
        
        else:            
            if 'author' not in paper.keys():
                authors += "No Data"
                return authors
            else:
                for author in paper['author']:
                    first_name = author['family']
                    given_name = author['given']
                    authors += f'{given_name} {first_name}, '

                return authors[:-2]

    


def collect_works(researcher_id: str) -> list:
    """Collect the works of a researcher from ORCID

    Args:
        researcher_id (str): researcher's ORCID

    Returns:
        list: list of Work objects
    """
    ret_works = get_works(researcher_id)
    works = []
    for work in ret_works["group"]:
        doi = get_doi(work)
        title = get_title(work)
        created_at = get_created_at_date(work)
        journal = get_journal_title(work)
        authors = get_authors(work)
        work = Work(doi, title, created_at, journal, authors)
        works.append(work)
        
    works = sorted(works, key=lambda x: x.created_at, reverse=True)
    return works

def out(works: list[Work], filepath: str):
    """Output the works to a file

    Args:
        works (list[Work]): list of Work objects
        filepath (str): file path
    """
    with open(filepath, "w") as f:
        f.write("authors,doi,title,created_at,journal\n")
        for work in works:
            f.write(f'"{work.authors}","{work.doi}","{work.title}","{work.created_at}","{work.journal}"\n')

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--researcher_id", "-r", help="researcher's ORCID")
    arg_parser.add_argument("--out", "-o", help="output file path")
    args = arg_parser.parse_args()
    researcher_id = args.researcher_id
    filepath = args.out
    
    works = collect_works(researcher_id)
    out(works, filepath)
    