import requests
import json
from pprint import pprint
import pandas as pd
import math

# Various calls to endpoints which I find most useful

def get_company_id(access_token, base_url):
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/companies?page=1&per_page=4', headers=headers)
    response_json = response.json()[0]
    return response_json['id']


def get_my_user_id(access_token, base_url):
    headers = {
      'Authorization': f'Bearer {access_token}',}

    response = requests.request("GET", f'{base_url}/rest/v1.0/me', headers=headers)
    response_json = response.json()
    return response_json['id']


def get_project_id(access_token, base_url, project_name):
    company_id = get_company_id(access_token, base_url)
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/companies/{company_id}/projects', headers=headers)
    response_json = response.json()
    for proj in response_json:
        if proj['name'] == project_name and proj['status_name'] == 'Active':
            return proj['id']

    print(f'project {project_name} not found.')
    print(f'Valid Options Include:\n')
    for proj in response_json:
        print(proj['name'])

def get_project_users(access_token, base_url, project_name):
    project_id = get_project_id(access_token, base_url, project_name)
    headers = {
      'Authorization': f'Bearer {access_token}'}

    response = requests.request("GET", f'{base_url}/rest/v1.0/projects/{project_id}/users', headers=headers)
    print(response)
    response_json = response.json()
    return response_json

def get_prime_contract(access_token, base_url, project_id):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.request("GET", f'{base_url}/rest/v1.0/prime_contract?project_id={project_id}', headers=headers)
    response_json = response.json()
    return response_json

def get_project_dates(access_token, base_url, project_id):
    headers = {
      'Authorization': f'Bearer {access_token}'}

    response = requests.request("GET", f'{base_url}/rest/v1.0/projects/{project_id}/project_dates', headers=headers)
    response_json = response.json()
    return response_json

def get_project_name(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/companies/{company_id}/projects', headers=headers)
    response_json = response.json()

    print('\nAvailable project names are:\n')
    for project in response_json:
        print(project['name'])
    return input('\nPaste chosen name:  ')

def get_company_projects(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/companies/{company_id}/projects', headers=headers)
    response_json = response.json()

    return response_json

def get_change_events(access_token, base_url):
    project_name = get_project_name(access_token, base_url)
    print(f'Project name is {project_name}')
    project_id = get_project_id(access_token, base_url, project_name)
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/change_events?project_id={project_id}&page=1&per_page=500', headers=headers)
    response_json = response.json()
    return response_json

def get_company_active_users(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.request("GET",f'{base_url}/rest/v1.0/companies/{company_id}/users',headers=headers)
    response_json = response.json()
    return response_json

def get_company_inactive_users(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.request("GET",f'{base_url}/rest/v1.0/companies/{company_id}/users/inactive',headers=headers)
    response_json = response.json()
    return response_json

def update_default_user_permissions(access_token, base_url, user_id, template_id, company_id):
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    payload = {
            "updates": [
                {
                    "id": user_id,
                    "default_permission_template_id": template_id

                }
            ]
        }

    response = requests.patch(f'{base_url}/rest/v1.0/companies/{company_id}/users/sync', data=json.dumps(payload), headers=headers)
    response_json = response.json()


def update_project_user_permissions(access_token, base_url, user_id, template_id, project_name):
    project_id = get_project_id(access_token,base_url,project_name)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    payload = {
  "permission_template_assignments": {
    "user_id": user_id,
    "permission_template_id": template_id
  }
}

    response = requests.patch(f'{base_url}/rest/v1.0/projects/{project_id}/permission_template_assignments', data=json.dumps(payload), headers=headers)
    print(response)
    response_json = response.json()
    print(response_json)


def update_user_company(access_token, base_url, user_id, vendor_id):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    payload = {
            "updates": [
                {
                    "id": user_id,
                    'vendor_id': vendor_id

                }
            ]
        }

    response = requests.patch(f'{base_url}/rest/v1.0/companies/{company_id}/users/sync', data=json.dumps(payload), headers=headers)
    print(response)
    print('User was associated with a company')


def get_company_permission_templates(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = { 'Authorization': f"Bearer {access_token}" }

    response = requests.request("GET", f'{base_url}/rest/v1.0/companies/{company_id}/permission_templates', headers=headers)
    response_json = response.json()
    return response_json

def inactivate_user(access_token, base_url, company_id, payload):
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    '''payload = {
            "updates": [
                {
                    "id": user_id,
                    'is_active': False

                }
            ]
        }'''

    response = requests.patch(f'{base_url}/rest/v1.0/companies/{company_id}/users/sync', data=json.dumps(payload), headers=headers)
    print(response)
    response_json = response.json()


def create_new_user_trade_ids(access_token, base_url, new_user, vendors):

    trade_types_ids = {}
    for vendor in vendors:
        for trade in vendor['trades']:
            trade_id = trade['id']

            name = trade['name']
            trade_types_ids[name] = trade_id


    trade_types = []
    if not pd.isna(new_user['Trade 1']):
        trade_types.append(new_user['Trade 1'])
        if not pd.isna(new_user['Trade 2']):
            trade_types.append(new_user['Trade 2'])
            if not pd.isna(new_user['Trade 3']):
                trade_types.append(new_user['Trade 3'])

    trade_ids = []

    for trade in trade_types:
        trade_ids.append(trade_types_ids[trade])

    return trade_ids

def add_vendor_to_project_directory(access_token, base_url, vendor_id, project_id):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}


    response = requests.post(f'{base_url}/rest/v1.0/projects/{project_id}/vendors/{vendor_id}/actions/add', headers=headers)
    print(response)
    response_json = response.json()
    print(response_json)
    print(f'Added vendor to project directory.')
    return response_json


def add_vendor_to_company_directory(access_token, base_url, new_user, vendor_dic, vendors):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    trade_ids = create_new_user_trade_ids(access_token, base_url, new_user, vendors)

    vendor_dic['is_active'] = True
    vendor_dic["authorized_bidder"] = True
    vendor_dic["country_code"] = 'US'
    vendor_dic['trade_ids'] = trade_ids

    payload = {
    "company_id": company_id,
        "vendor": vendor_dic
    }

    response = requests.post(f'{base_url}/rest/v1.0/vendors', data=json.dumps(payload), headers=headers)
    print(response)
    response_json = response.json()
    print(response_json)
    vendor_id = response_json['id']
    print(f'Added {new_user["Vendor Company"]} to company directory.')
    return response_json


def get_project_vendors(access_token, base_url, project_id):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    response = requests.get(f'{base_url}/rest/v1.0/projects/{project_id}/vendors', headers=headers)
    response_json = response.json()
    print('\nReturned Project Vendors')
    return response_json

def get_template_id(access_token, base_url, template_name):
    permission_templates = get_company_permission_templates(access_token,base_url)
    for temp in permission_templates:
        if temp['name'] == template_name:
            return temp['id']

    for permission_template in permission_templates:
        print(permission_template)


    raise ValueError(f'template_name {template_name} did not match any choices.')


def add_user_to_company_directory(access_token, base_url, new_user, vendor_id):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}
    # payload doesn't have to be within the function, it could be given as an argument for efficiently uploading many people at once
    default_permissions_template_id = get_template_id(access_token, base_url,new_user['Suggested Template'])


    payload = {
        "user": {
            "first_name": new_user['Contact First Name'],
            "last_name": new_user['Contact Last Name'],
            "email_address": new_user['Email'],
            "is_active": True,
            "is_employee": False, # you could add a check to see if the person is an internal employee or or not
            "default_permission_template_id": default_permissions_template_id,
            "company_permission_template_id": 811636, # this is the template id for No Administrative Rights (at least on my company's site.)
            "vendor_id": vendor_id
        }
    }

    response = requests.post(f'{base_url}/rest/v1.1/companies/{company_id}/users', data=json.dumps(payload), headers=headers)
    print(response)
    response_json = response.json()
    print(f'Added user {new_user["Email"]} to company directory')
    return response_json


def add_user_to_project_directory(access_token, base_url, new_user, vendor_id, emp_id):
    project_id = get_project_id(access_token, base_url, new_user['Project Name'])
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}
    # payload doesn't have to be within the function, it could be given as an argument for efficiently uploading many people at once
    default_permissions_template_id = get_template_id(access_token, base_url,new_user['Suggested Template'])

    payload = {
        "user": {
            "first_name": new_user['Contact First Name'],
            "last_name": new_user['Contact Last Name'],
            "email_address": new_user['Email'],
            "is_active": True,
            "is_employee": False,
            "permission_template_id": default_permissions_template_id,
            "vendor_id": vendor_id,
            "employee_id" : emp_id
        }
    }

    response = requests.post(f'{base_url}/rest/v1.0/projects/{project_id}/users', data=json.dumps(payload), headers=headers)
    print(response)
    response_json = response.json()
    print(f'Added user {new_user["Email"]} to project {new_user["Project Name"]} directory')
    return response_json


def invite_user_to_procore(access_token, base_url, user):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    print(user)
    user_id = user['id']
    user_name = user['name']
    response = requests.patch(f'{base_url}/rest/v1.1/companies/{company_id}/users/{user_id}/invite', headers=headers)
    print(response)
    response_json = response.json()
    print(f'Invited user {user_name} to procore')
    return response_json


def get_company_vendors(access_token, base_url):
    company_id = get_company_id(access_token, base_url)
    headers = {'Authorization': f'Bearer {access_token}',
               'content-type': "application/json"}

    payload = {
        'company_id': company_id
    }
    response = requests.get(f'{base_url}/rest/v1.0/vendors',data=json.dumps(payload), headers=headers)
    response_json = response.json()
    print('\nReturned Company Vendors')
    return response_json
