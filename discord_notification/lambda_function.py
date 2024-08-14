from discord import SyncWebhook
import os
    
#test    
def lambda_handler(event, context):
    URL = os.environ.get("DISCORD_URL")
    message = event.get('message')
    webhook = SyncWebhook.from_url(URL)
    webhook.send(message)
    return {
        'statusCode': 200,
        'body': 'message was successfully sent.'
    }
