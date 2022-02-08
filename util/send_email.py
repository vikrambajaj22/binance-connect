
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os

from google.cloud import secretmanager
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send(message_html):
    if os.getenv('ENVIRONMENT') == 'local':
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    elif os.getenv('ENVIRONMENT') == 'gcp':
        # for GCP environment, secrets are stored in Secret Manager
        client = secretmanager.SecretManagerServiceClient()
        sendgrid_api_key_secret = 'projects/binance-connect-22/secrets/SENDGRID_API_KEY/versions/1'
        sendgrid_api_key = client.access_secret_version(
            request={"name": sendgrid_api_key_secret}).payload.data.decode("UTF-8")

    message = Mail(
        from_email='vikrambajaj@nyu.edu',
        to_emails='vikrambajaj@nyu.edu',
        subject='Alert from Binance Connect App',
        html_content=message_html)
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print('email sent')
    except Exception as e:
        print('exception while sending email: {}'.format(repr(e)))
