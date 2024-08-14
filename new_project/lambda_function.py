import os
import gitlab
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
#test
def create_project(proj_name, giturl):
    TOKEN = os.environ.get("PRIVATE_TOKEN")
    gl = gitlab.Gitlab(url=giturl, private_token=TOKEN)
    try:
        project = gl.projects.create({'name': proj_name})
    except Exception:
        project = gl.projects.list(search=proj_name)[0]

    access_token = project.access_tokens.create({"name": f"{proj_name}", "scopes": ["api"], "expires_at": "2025-06-03"})
    return {"project_path": project.path_with_namespace, "token": access_token.token}

def generate_code_file(filename, access_token_name, PRIVATE_TOKEN, GITLAB_URL, project_path, project_name, file_extension):
    tmp_filename = os.path.join('/tmp', filename)
    code = f"""
import os
import subprocess

def create_project(project_name, file_extension, project_path):
    os.makedirs(project_name, exist_ok=True)
    file_path = os.path.join(project_name, f"main.{file_extension}")
    with open(file_path, 'w') as file:
        pass

    http_url = f"http://{access_token_name}:{PRIVATE_TOKEN}@{GITLAB_URL[7:]}/{project_path}.git"
    os.system(f'cd {project_name} && git init && git remote add origin {{http_url}}')
    os.system(f'cd {project_name} && git add . && git commit -m "Initial commit" && git push -u origin master')

    subprocess.run(['code', project_name])

if __name__ == "__main__":
    project_name = '{project_name}'
    file_extension = '{file_extension}'
    project_path = '{project_path}'
    create_project(project_name, file_extension, project_path)
    """
    with open(tmp_filename, 'w') as file:
        file.write(code)

def upload_to_s3(file_name, bucket_name, s3_file_name, region_name=None):
    try:
        session = boto3.Session(region_name=region_name)
        s3 = session.client('s3')
        s3.upload_file(file_name, bucket_name, s3_file_name)
        print(f"File {file_name} uploaded to {bucket_name}/{s3_file_name} successfully.")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def get_presign_url(bucket_name, s3_file_name):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': s3_file_name})
    return url

def lambda_handler(event, context):
    TOKEN = os.environ.get("PRIVATE_TOKEN")
    project_name = event.get('project_name')
    file_extension = event.get('file_extension')
    GIT_URL = os.environ.get('GITLAB_SERVER')
    dictionary_values = create_project(project_name, GIT_URL)

    TOKEN = dictionary_values.get('token')
    access_token_name = project_name
    project_path = dictionary_values.get('project_path')
    py_file = "agent_setup.py"
    generate_code_file(py_file, access_token_name, TOKEN, GIT_URL, project_path, project_name, file_extension)

    file_name = f'/tmp/{py_file}'
    bucket_name = 'python-scripts-funcs'
    s3_file_name = 'script.py'
    region_name = 'eu-north-1' 

    upload_to_s3(file_name, bucket_name, s3_file_name, region_name)
    url = get_presign_url(bucket_name, s3_file_name)
    
    return {
        'statusCode': 200,
        'body': 'Project created successfully',
        'download_link': url
    }
