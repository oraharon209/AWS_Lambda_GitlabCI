import pandas as pd
import re
import gitlab
import os

def convert_google_sheet_url(url):
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    replacement = lambda m: (f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' +
                             (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv')
    new_url = re.sub(pattern, replacement, url)
    return new_url

def parse_sheet_data(url):
    new_url = convert_google_sheet_url(url)
    df = pd.read_csv(new_url)
    user_data = df.to_dict(orient='records')
    return user_data

def create_user_from_sheet(gl, user_data):
    try:
        user = gl.users.create({'email': user_data['email'],
                                'password': user_data['password'],
                                'username': user_data['username'],
                                'name': user_data['name']})
    except gitlab.exceptions.GitlabCreateError:
        print(f"User {user_data['username']} already exists")
        user = gl.users.list(username=user_data['username'])[0]
    finally:
        return user

def create_group_gitlab(gl, group_name):
    try:
        group = gl.groups.create({'name': group_name, 'path': 'potatoes'})
        group.description = "Group for all the potatoes"
        group.save()
    except gitlab.exceptions.GitlabCreateError:
        print(f"Group {group_name} already exists")
        group = gl.groups.list(search=group_name)[0]  # Assign an existing group if it exists
    return group  # Always return the group, whether newly created or existing2


def add_user_to_group(group, user):
    try:
        group.members.create({'user_id': user.id,
                              'access_level': gitlab.const.AccessLevel.REPORTER})
    except gitlab.exceptions.GitlabCreateError:
        print(f"User {user.name} already in group")

def create_user_project(gl, group, user):
    project = None
    try:
        project = gl.projects.create({'name': user.name, 'namespace_id': group.id})
    except gitlab.exceptions.GitlabCreateError:
        print(f"Project named {group.name}/{user.name} already exists")
        project = gl.projects.list(search=f"{group.name}/{user.name}")[0]
    finally:
        return project

def lambda_handler(event, context):
    GITLAB_SERVER = os.getenv('GITLAB_SERVER')
    PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')
    URL = event['google_sheet_url']
    gl = gitlab.Gitlab(GITLAB_SERVER, private_token=PRIVATE_TOKEN)
    
    data = parse_sheet_data(URL)
    group_name = 'lambda'
    group = create_group_gitlab(gl, group_name)
    
    for user_data in data:
        user = create_user_from_sheet(gl, user_data)
        add_user_to_group(group, user)
        create_user_project(gl, group, user)

    return {
        'statusCode': 200,
        'body': 'Users and projects created successfully.'
    }
