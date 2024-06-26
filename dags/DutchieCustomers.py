"""
DutchieCustomers
DAG auto-generated by Astro Cloud IDE.
"""

from airflow.decorators import dag
from astro import sql as aql
import pandas as pd
import pendulum

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # container_client = blob_service_client.get_blob_client

    # print(container_client)

except Exception as ex:
    print('Exception:')
    print(ex)

@aql.dataframe(task_id="python_1")
def python_1_func():
    import requests
    import tempfile
    from uuid import uuid4
    
    users = requests.get("https://api.pos.dutchie.com/customer/customers", headers={
        'Authorization': 'Basic MDZhYzI1MDhlM2VlNDNmMzhjNTVkMmMwYTY1YTRhMTA='
    })
    
    blob_name = f"{uuid4()}.json"
    
    with tempfile.NamedTemporaryFile(mode='w+') as f:
        f.write(users.content.decode('utf-8'))
        container_client = blob_service_client.get_blob_client(container="users", blob=blob_name)
        f.seek(0)
        container_client.upload_blob(users.content)
    
    return blob_name
    

default_args={
    "owner": "zach@pincanna.com,Open in Cloud IDE",
}

@dag(
    default_args=default_args,
    schedule="0 0 * * *",
    start_date=pendulum.from_format("2024-05-24", "YYYY-MM-DD").in_tz("UTC"),
    catchup=False,
    owner_links={
        "zach@pincanna.com": "mailto:zach@pincanna.com",
        "Open in Cloud IDE": "https://cloud.astronomer.io/clwk2mbov00ue01nqnntx2key/cloud-ide/clwk2zzh800vu01nqlbgqvx46/clwk35sbx00wd01nq7sh2bv39",
    },
)
def DutchieCustomers():
    python_1 = python_1_func()

dag_obj = DutchieCustomers()
