![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue?logo=python&logoColor=blue)
[![Build](https://github.com/ParthDevWorks/insightpkg/actions/workflows/daily_pypi_ingest_cronjob.yml/badge.svg)](https://github.com/ParthDevWorks/insightpkg/actions/workflows/daily_pypi_ingest_cronjob.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


# Insight Package Manager

Insight Package Manager (insightpkg) is a powerful command-line tool designed to provide insights and analysis for Python packages. It offers features for data processing, logging, and interaction with external services like GitHub.

## Features

- [**PyPi Ingestion**](#pypi-ingestion): This project implements a daily ingestion pipeline that retrieves newly uploaded packages from PyPI and enriches them with metadata sourced from their corresponding GitHub repositories. The enriched data is then persisted to a PostgreSQL database. For production use, the system leverages Supabase as the managed Postgres backend.

## Worflow Steps

### <a name="pypi-ingestion"></a>PyPi Ingestion
Workflow Steps:
1.	Daily Ingestion: Automatically fetches the latest packages published on PyPI.
2.	Metadata Enrichment: Extracts relevant metadata such as repository stars, forks from GitHub (when linked in the package metadata).
3.	Storage Layer: Stores the processed and enriched package data into a PostgreSQL database.
	
    • <u>Production</u> : Uses Supabase for scalable, hosted Postgres with REST and GraphQL APIs.
	
    • <u>Development</u> : Can be configured to use a local Postgres instance.


## 🛠️ Prerequisites

Before you get started, make sure you have the following tools installed and configured:

1. **[Poetry](https://python-poetry.org/docs/#installation)**  Used for dependency management and packaging. 

2.	PostgreSQL (for local development)
Required to store ingested package data.

    •	Install from [here](https://www.postgresql.org/download/)

    •	After installation, ensure `psql` is accessible in your terminal.

3.	Supabase (for production deployment): Supabase provides a hosted Postgres backend with REST and GraphQL APIs.
	
    •	Create an account at [supabase.com](https://supabase.com/)

	•	Set up a new project and database

	•	Click on `Connect` then `Type` - `Python`. Under `Transaction Pooler` you will find information to add in our `config.ini` file. Username and Password is provided when you create the Project


## Installation

1. For Production Purpose, using [Poetry]:

        poetry add insightpkg

2. For Development Purpose, you can clone the repository and install it locally:

        git clone https://github.com/ParthDevWorks/insightpkg.git 
        cd insightpkg 
        poetry install


## Configuration

1. Insightpkg uses a configuration file (`config.ini`) to store project related settings. You can find a template in `config.ini.template`. 
    
    Set `CONFIG_INI_FILE_PATH` as Environment Variable after you have saved the config.ini file.
        
        export CONFIG_INI_FILE_PATH=path/to/config.ini

2. You can set where the logs should be downloaded by setting Environment Variable `LOG_DIR`. Default is at `Root Level of the Repo`
        
        export LOG_DIR=/path/where/you/want/to/store

3. Set `REQUEST_TOKEN` as Environment variable to perform api requests to Github. Without this token, [only 60 requests/hr can be made](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28#primary-rate-limit-for-unauthenticated-users).

    [How to Generate Personal Access Token on Github](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
    
        export REQUEST_TOKEN=personal_access_token

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the need for efficient package management insights.
- It makes heavy use of Python's standard library and third-party packages like `requests` for GitHub interactions.
