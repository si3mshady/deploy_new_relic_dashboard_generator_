import boto3,requests, wget, subprocess
from  sendemail import  send_email
import shutil

TMP = '/tmp'
guid = "MzI1NzMxNnxWxxxEJPQVJEfDQzMTQyMjE"
api_key=  "NRAK-Z0BW4QHxxxxNPVDOQ8FRBXLCW8KPMCW"

query = {"query":"mutation {\n  dashboardCreateSnapshotUrl(guid:\
 \"MzI1NzMxNnxxxxFTSEJPQVJEfDQzMTQyMjE\")\n}\n", "variables":""}

graph_ql_endpoint = "https://api.newrelic.com/graphql"
headers = { 'Content-Type': 'application/json', 'API-KEY': api_key}
kwargs = {"url":graph_ql_endpoint,"params":query,"headers": headers}


def post_request():
    r = requests.post(**kwargs)
    url = r.json().get('data').get('dashboardCreateSnapshotUrl')
    print(url)
    return url



def download_digital_dashboard(url):
    local_filename = TMP + '/' + 'digital_dash.pdf'
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename



def lambda_handler(event,context):
    url = post_request()
    filename = download_digital_dashboard(url)

    kwargs = {"to":"d3vops.shop@gmail.com", "url":url, "frm":"el.genesis.block@gmail.com", "subject":"dailyDashboard", "filename": filename}
    send_email(**kwargs)


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
