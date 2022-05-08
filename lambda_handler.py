import boto3,requests, wget, subprocess
import send_email from 'send_email.py'
import shutil

TMP = '/tmp'
guid = "MzI1NzMxNnxWSVp8REFTSEJPQVJEfDQzMTQyMjE"
api_key=  "NRAK-Z0BW4QHNPVDOQ8FRBXLCW8KPMCW"

query = {"query":"mutation {\n  dashboardCreateSnapshotUrl(guid: \"MzI1NzMxNnxWSVp8REFTSEJPQVJEfDQzMTQyMjE\")\n}\n", "variables":""}
graph_ql_endpoint = "https://api.newrelic.com/graphql"
headers = { 'Content-Type': 'application/json', 'API-KEY': api_key}
kwargs = {"url":graph_ql_endpoint,"params":query,"headers": headers}


def post_request():
    r = requests.post(**kwargs)
    return r.json().get('data').get('dashboardCreateSnapshotUrl')



def download_digital_dashboard(url):
    local_filename 'digital_dash.pdf'
    with requests.get(url, stream=True) as r:
        with open(TMP + '/' + local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename



def lambda_handler():
    url = post_request()
    name = download_digital_dashboard(url)
    

     # send_email(to,from, subject, filenam



#
# curl https://api.newrelic.com/graphql \
#   -H 'Content-Type: application/json' \
#   -H 'API-Key: NRAK-Z08888W8KPMCW' \
#   --data-binary '{"query":"mutation {\n  dashboardCreateSnapshotUrl(guid: \"MzI18888SEJPQVJEfDQzMTQyMjE\")\n}\n", "variables":""}'
# # https://api.newrelic.com/graphql
#
#
#     # https://docs.newrelic.com/docs/apis/nerdgraph/get-started/introduction-new-relic-nerdgraph/#explorer
