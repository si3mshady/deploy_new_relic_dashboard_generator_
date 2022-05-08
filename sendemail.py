
 def send_email(to,from, subject, filename):
        ses = boto3.client('ses')
        '''documentation = https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html '''
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = subject
        msg['From'] = from
        msg['To'] = to

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open(filename, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename=filename)

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        msg.attach(att)
        # print(msg)
        response = ses.send_raw_email(
                Source=from,
                Destinations=[to],
                RawMessage={
                    'Data': msg.as_string(),
                }
            )
