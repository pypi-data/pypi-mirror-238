from zippy_form.celery import app
import requests

from zippy_form.models import Webhook
from zippy_form.utils import WEBHOOK_STATUS


def get_user_account_webhooks(account_id):
    """
    Get User Account Webhooks
    """
    user_account_webhooks = Webhook.objects.filter(account=account_id, status=WEBHOOK_STATUS[1][0])

    webhook_urls = []

    # Get User Account Webhooks
    for user_account_webhook in user_account_webhooks:
        temp = {'webhook_id': user_account_webhook.id, 'endpoint_url': user_account_webhook.endpoint_url}

        webhook_urls.append(temp)

    return webhook_urls


@app.task
def handle_webhook_queue(data):
    """
    Handle Webhook Queue
    """
    account_id = data['account']['id']
    webhooks = get_user_account_webhooks(account_id)

    webhook_response = []

    # Loop all the Webhooks & send event data to the URL provided by user
    for webhook in webhooks:
        response = {}

        try:
            webhook_info = requests.post(webhook['endpoint_url'], data=data)
            response['status'] = "success"
            response['status_code'] = webhook_info.status_code
            response['webhook'] = {}
            response['webhook']['id'] = str(webhook['webhook_id'])
            response['webhook']['url'] = str(webhook['endpoint_url'])
            response['account_id'] = account_id
        except Exception as e:
            response['status'] = "error"
            response['webhook'] = {}
            response['webhook']['id'] = str(webhook['webhook_id'])
            response['webhook']['url'] = str(webhook['endpoint_url'])
            response['account_id'] = account_id
            response['data'] = str(e)

        webhook_response.append(response)

    return webhook_response
