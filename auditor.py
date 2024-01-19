import os
import requests
import json
import sys

portal_token = os.environ.get('PORTAL_TOKEN')
portal_url = os.environ.get('PORTAL_URL')
sequence = os.environ.get('SEQUENCE')
repo_name = os.environ.get('REPO_NAME')

api_url = f"{portal_url}/api/v1"
group_and_name = repo_name.split('/')
product_name = group_and_name[1]
product_type = group_and_name[0]
repo_ssh_url = f"git@github.com:{product_type}/{product_name}.git"

headers={"Content-Type": "application/json", "Authorization": "Token " + portal_token}

def get_product_id():
    api_response = requests.get(
        url=f'{api_url}/products/?name={product_name}',
        headers=headers
    ) 
    if api_response.json().get('results'):
        id = [elem['id'] for elem in api_response.json().get('results')]
        print("Product name: " + product_name)
    if not api_response.json().get('results'):
        body = {
                "name": product_name,
                "product_type": product_type_id,
                "jira_settings": {} ,
            }
        r = requests.post(
            url=f'{api_url}/products/',
            headers=headers,
            json=body
        )
        print("Product " + product_name + " was created.")
        id = [r.json().get('id')]
        create_asset_body = {
            "product": r.json().get('id'),
            "value": repo_ssh_url,
            "asset_type": 0
        } 
        r = requests.post(
            url=f'{api_url}/product-assets/',
            headers=headers,
            json=create_asset_body
        )
    return id

def get_product_type_id():
    api_response = requests.get(
        url=f'{api_url}/product-type/?name={product_type}',
        headers=headers
    ) 
    if api_response.json():
        id = [elem['id'] for elem in api_response.json()][0]
        print("Product type: " + product_type)
    if not api_response.json():
        body = {
                "name": product_type
            }
        r = requests.post(
        url=f'{api_url}/product-type/',
        headers=headers,
        json=body
        )
        print("Product type " + product_type + " was created.")
        id = r.json().get('id')
    return id
    
def get_sequence_id():
    api_response = requests.get(
        url=f'{api_url}/job-sequences',
        headers=headers
    )

    for item in api_response.json():
        if sequence is None:
            if item["title"] == 'Default':
                id = item["id"] 
                break
        else:
            if item["title"] == sequence:
                id = item["id"] 
                break
    return id

def run_audit(sequence_id, product_id):
    body = {
                "job_sequence": sequence_id,
                "products": product_id
            }
    r = requests.post(
        url=f'{api_url}/auditor/pipelines/run/',
        headers=headers,
        json=body
    )
    print(r.text)
    print(r.status_code)

product_type_id = get_product_type_id()
print("Product type id: ")
print(product_type_id)

product_id = get_product_id()
print("Product id: ")
print(product_id) 

sequence_id = get_sequence_id()

run_audit(sequence_id, product_id)
