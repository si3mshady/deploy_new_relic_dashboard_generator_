import boto3,requests, wget, subprocess

TMP = '/tmp'
guid = "MzI1NzMxNnxWSVp8REFTSEJPQVJEfDQzMTQyMjE"
api_key=  "NRAK-Z0BW4QHNPVDOQ8FRBXLCW8KPMCW"

query = {"query":"mutation {\n  dashboardCreateSnapshotUrl(guid: \"MzI1NzMxNnxWSVp8REFTSEJPQVJEfDQzMTQyMjE\")\n}\n", "variables":""}
graph_ql_endpoint = "https://api.newrelic.com/graphql"
headers = { 'Content-Type': 'application/json', 'API-KEY': api_key}
kwargs = {"url":graph_ql_endpoint,"params":query,"headers": headers}

 def send_email(self):
        '''documentation = https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html '''
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = ''
        msg['From'] = 'd3vops.shop@gmail.com'
        msg['To'] = 'el.genesis.block@gmail.com'

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open('traffic.png', 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename="traffic.png")

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        msg.attach(att)
        # print(msg)
        response = ses.send_raw_email(
                Source='d3vops.shop.com',
                Destinations=['si3mshady@gmail.com'],
                RawMessage={
                    'Data': msg.as_string(),
                }
            )



def post_request():
    r = requests.post(**kwargs)
    return r.json().get('data').get('dashboardCreateSnapshotUrl')


def download_dashboard(url):



def lambda_handler():
    pass



#
# curl https://api.newrelic.com/graphql \
#   -H 'Content-Type: application/json' \
#   -H 'API-Key: NRAK-Z0BW4QHNPVDOQ8FRBXLCW8KPMCW' \
#   --data-binary '{"query":"mutation {\n  dashboardCreateSnapshotUrl(guid: \"MzI1NzMxNnxWSVp8REFTSEJPQVJEfDQzMTQyMjE\")\n}\n", "variables":""}'
# # https://api.newrelic.com/graphql
#
#
#     # https://docs.newrelic.com/docs/apis/nerdgraph/get-started/introduction-new-relic-nerdgraph/#explorer
