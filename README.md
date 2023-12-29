# OCW OER Export

This is a demonstration project for showing how to use MIT Open API. Specifically, this project extracts MIT OpenCourseWare courses' data and creates a CSV file to be exported to OER Commons [according to their requirements](https://help.oercommons.org/support/solutions/articles/42000046853-import-resources-with-the-bulk-import-template).

**SECTIONS**

1. [Initial Setup & Usage](#initial-setup)
1. [Requirements](#requirements)
1. [Tests](#tests)
1. [Committing & Formatting](#committing-&-formatting)


## Initial Setup & Usage

_ocw_oer_export_ is available [on PyPI](link). To install:

```
pip install ocw_oer_export
```

To use it:

```
from ocw_oer_export import create_csv
create_csv()
```
By default, the `create_csv` function accepts `source="api"` and `output_file="ocw_oer_export.csv"` parameters, allowing customization of data sources and output filenames. The output file is generated in the current directory.

The source parameter can be changed to `source="json"` if a JSON file is available. JSON can be created as:

```
from ocw_oer_export import create_json
create_json()
```

This command generates a JSON file in the current directory. It can then be used as:

```
create_csv(source="json")
```

A CLI interface is available as well, which can be used in a similar manner:

```
python3 main.py --create_csv
```
OR

```
python3 main.py --create_json
python3 main.py --create_csv(source=json)
```

## Requirements
To ensure successful execution and correct output, confirm the presence of the following fields in the [MIT Open's API](https://mit-open-rc.odl.mit.edu//api/v1/courses/?platform=ocw):

`title`, `url`, `description`, `topics`, `course_feature`, `runs: instructors`

Additionally, ensure that the `mapping_files` are up-to-date. For example, if OCW introduces a new topic not mapped in `ocw_oer_export/mapping_files/ocw_topic_to_oer_subject.csv`, it results in `null` entries for that topic in the CSV (`CR_SUBJECT`).

## Tests

To run unit tests:

```
python -m tests discover
```

## Committing & Formatting

To ensure commits to GitHub are safe, first install [pre-commit](https://pre-commit.com/):

```
pip install pre_commit
pre-commit install
```

Running pre-commit can confirm your commit is safe to be pushed to GitHub and correctly formatted:

```
pre-commit run --all-files
```
