from slack_sdk.webhook import WebhookClient
import azure.functions as func
import dateutil.parser
import logging
import os
import requests
import re


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Set and log environment variables for both Slack webhook URL and RSC tenant
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    rsc_tenant_url = os.environ['RSC_TENANT_URL']

    if slack_webhook_url and rsc_tenant_url:
        logging.info(f'Slack webhook URL set to {slack_webhook_url}')

        logging.info(
            f'Rubrik Security Cloud tenant URL set to {rsc_tenant_url}')
    else:
        logging.error(
            f'Environment variables not set correctly, please review RSC and Slack webhook settings')

    # Check the RSC URL is reachable
    rsc_url_status = requests.get(rsc_tenant_url)
    if rsc_url_status.status_code != 200:
        logging.info(
            f'RSC tenant URL does not seem to be responding, please check the environment variable')

    # Validate the Slack webhook URL is the correct syntax using RegEx
    slack_webhook_url_check = re.search(
        "https://hooks.slack.com/services/T[0-9A-Z]{10}/B[0-9A-Z]{10}/[a-zA-Z0-9]{24}", slack_webhook_url)
    if slack_webhook_url_check:
        logging.info(f'Slack URL appears to be correctly formed')
    else:
        logging.error(
            f'Slack URL appears to be malformed - please check and remediate')

    source_message = req.get_json()

    if source_message:
        logging.info(f'Finding alert summary content is - {source_message}')
        alert_summary = source_message.get('summary')
        alert_severity = source_message.get('severity')
        alert_timestamp = source_message.get('timestamp')
        alert_class = source_message.get('class')
        alert_event_id = source_message['custom_details']['seriesId']
        alert_object_name = source_message['custom_details']['objectName']
        alert_object_type = source_message['custom_details']['objectType']
        alert_cluster_id = source_message['custom_details']['clusterId']
        alert_formatted_timestamp = dateutil.parser.parse(alert_timestamp)
        alert_display_timestamp = alert_formatted_timestamp.ctime()
        review_findings_url = rsc_tenant_url + "/events"
        logging.info(f'Building Slack message...')
        slack_webhook = WebhookClient(slack_webhook_url)
        slack_webhook_response = slack_webhook.send(
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": "Rubrik Security Cloud " + alert_severity + " severity event notification",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":bell: *Event Information*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Event summary_* :\t" + alert_summary
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Severity_* :\t" + alert_severity
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Type_* :\t" + alert_class
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Event ID_* :\t" + alert_event_id
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Object Name_* :\t" + alert_object_name
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Object Type_* :\t" + alert_object_type
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Cluster ID_* :\t" + alert_cluster_id
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Time_* :\t" + alert_display_timestamp
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":mag: *Recent events can be viewed in a browser by clicking the button*"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Latest Events",
                            "emoji": True
                        },
                        "value": "recent_events",
                        "url": review_findings_url,
                        "action_id": "button-action"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        )
        logging.info(f'Slack message sent successfully ')
        return func.HttpResponse(status_code=200)
    else:
        logging.error(f'Empty message payload recieved ')
        return func.HttpResponse(status_code=400)
