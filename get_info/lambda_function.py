import wikipedia
import boto3

# 1Initialize S3 client
s3 = boto3.client('s3')

def wiki_search(wiki_topic):
    """
    Fetches the top section of a Wikipedia topic.
    """
    try:
        top_section = wikipedia.summary(wiki_topic)
        return top_section
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation error: '{wiki_topic}' may refer to multiple pages.")
        return None
    except wikipedia.exceptions.PageError:
        print(f"Page error: The page '{wiki_topic}' does not exist.")
        return None

def check_if_object_exists(bucket_name, key):
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def lambda_handler(event, context):
    user_name = event.get('user_name')
    topic = event.get('topic')
    # Define S3 bucket and key
    bucket_name = 'python-scripts-funcs'
    key = f'{user_name}.txt'
    data_to_add = wiki_search(topic)

    if data_to_add is None:
        return {
            'statusCode': 400,
            'body': f"Failed to retrieve data for the topic '{topic}'."
        }
     
    if check_if_object_exists(bucket_name, key):
        # Download the existing object
        response = s3.get_object(Bucket=bucket_name, Key=key)
        existing_data = response['Body'].read().decode('utf-8')
        updated_data = existing_data + '\n' + data_to_add
    else:
        # Create new data
        updated_data = data_to_add

    # Upload the updated or new data
    s3.put_object(Bucket=bucket_name, Key=key, Body=updated_data.encode('utf-8'))

    return {
        'statusCode': 200,
        'body': 'Excel file uploaded to S3 successfully'
    }
