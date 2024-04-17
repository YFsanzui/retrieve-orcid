# retrieve-orcid
Retrieve academic data stored in ORCID using the ORCID public API

## Requirements
- Python 3.6 or later

## Installation
```bash
pip install git+https://github.com/yfsanzui/retrieve-orcid.git -r requirements.txt
```

## How to use
CLI and Python script are available to retrieve researcher's works from ORCID.

### CLI
Run the following command in your terminal. Replace `{researcher_id}` with the ORCID ID of the researcher you want to retrieve works from and `{path/to/output_file}` with the path to the file where you want to save the retrieved data. This command will retrieve the works of the researcher and save the data to a file.

```bash
python -m retrieve_orcid.get_works -r {researcher_id} -o {path/to/output_file}
```

### Your python script
```python
from retrieve_orcid.get_works import collect_works, out

# Retrieve ORCID data
works = collect_works('0123-4567-8901-2345')

# Save retrieved works to a file
out(works, 'works.csv')
```

### LICENSE
MIT
