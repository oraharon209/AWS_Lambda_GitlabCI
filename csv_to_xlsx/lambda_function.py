import base64
import boto3
import pandas as pd
import io

# 1Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Retrieve the base64-encoded CSV from the event
    encoded_csv = event['csv_content']
    file_name = event.get('file_name')
    # Decode the base64 string back into CSV format
    decoded_csv = base64.b64decode(encoded_csv).decode()

    # Convert CSV to DataFrame
    df = pd.read_csv(io.StringIO(decoded_csv), delimiter=';', encoding='utf-8')
    
    # Convert DataFrame to Excel
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    # Define S3 bucket and key
    bucket_name = 'python-scripts-funcs'
    key = f'{file_name}.xlsx'

    # Upload Excel file to S3
    s3.put_object(Body=excel_buffer, Bucket=bucket_name, Key=key)
    url = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': key})
    return {
        'statusCode': 200,
        'body': 'Excel file uploaded to S3 successfully',
        'download_link': url
    }
