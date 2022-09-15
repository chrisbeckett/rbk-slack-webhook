# Rubrik Security Cloud Slack Connector

## What does it do?

This connector runs as an Azure Function and provides a webhook URL for Rubrik Security Cloud (RSC, formerly Polaris) to send alerts to. This provides simple connectivity to Slack as it sends alert information as cards into a Slack channel.

![alt text](https://github.com/chrisbeckett/rbk-slack-webhook/blob/main/slack-event.png "Slack screenshot")

## How does it work?

Create a new webhook in the RSC "Security Settings" page (can be accessed via the gear icon in the top right hand corner) and filter out the required events and severity. For example, to send backup operations events to Slack, you may wish to select the "Backup", "Diagnostic", "Maintenance" and "System" event types with the "Critical" and "Warning" severities.

![alt text](https://github.com/chrisbeckett/dome9-Slack-connector/blob/master/slack-connector-architecture.png "Architecture overview")

## What do I need to get started?

- An RSC tenant
- A Slack account
- A Slack channel to send alerts to
- A Slack webhook URL (https://api.slack.com/messaging/webhooks)
- Python 3.7/3.8/3.9 (3.10 is not currently supported by Azure Functions)
- Git

## Obtaining the code

Run **git clone https://github.com/chrisbeckett/rbk-slack-connector.git**

## Deploying the Azure Function

Click the "Deploy to Azure" button and fill out the deployment form

- Both the **Azure Function** name and the **Storage Account** name **must be globally unique or deployment will fail (if a new storage account is created)**
- Once the ARM template deployment is complete, open a command prompt and navigate to the **rbk-slack-connector** folder
- Install the Azure Functions command line tools (*https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash*)
- Run **func init**
- Run **func azure functionapp publish _functname_** where the functname is your function name from the "**Deploy to Azure**" workflow
- When this is complete, you will need the HTTP trigger URL (Function overview, "Get Function URL" button)

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fchrisbeckett%2Frbk-slack-connector%2Fmain%2Fdeployment-template.json)
