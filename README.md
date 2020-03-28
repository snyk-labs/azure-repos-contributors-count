Count contributing developers to an Azure DevOps organization in the last 90 days.

## Usage
Install virtual environment with:
`pipenv install`

- Count contributing developers for Azure Devops Services
  - ```bash
       pipenv run python3 azure-repos-contributors-count.py --organization=[Azure DevOps Organization] --username=[Azure DevOps Username] --pat=[Azure DevOps Personal Access Token]
    ```
- Count contributing developers for Azure Devops Server (setup on premises)
  - ```bash
       pipenv run python3 azure-repos-contributors-count.py --on-prem=True --instance=[Azure DevOps Instance] --collection=[Azure DevOps Collection] --username=[Azure DevOps Username] --pat=[Azure DevOps Personal Access Token]
    ```

(Or use alternate Python 3 environment as required)
