
'''
TODO: Run these from the command line before following these steps

conda install -c conda-forge/label/cf202003 google-cloud-sdk
conda install -c conda-forge/label/cf202003 google-api-core
conda install -c conda-forge/label/cf202003 google-auth-oauthlib
conda install pandas-gbq --channel conda-forge

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
'''

# TODO: Save a service key locally in this repo and edit for local file path
key_path = "/Users/natashamathur/QTH_scripts/bigquery/ornate-variety-314119-de324fcebc28.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

# TODO: Make or find dataset to be uploaded

test_records = [
    {
        "title": u"The Meaning of Life",
        "release_year": 1983,
        "length_minutes": 112.5,
    },
    {
        "title": u"Monty Python and the Holy Grail",
        "release_year": 1975,
        "length_minutes": 91.5,
    }
]
test_df = pd.DataFrame(
    test_records,
    columns=[
        "title",
        "release_year",
        "length_minutes",
    ]
)

# TODO: Indicate the project and table id you want to use
project_id = "ornate-variety-314119"
table_id = "haze_analytics.test"

pandas_gbq.to_gbq(test_df, table_id, project_id=project_id, if_exists='replace')
