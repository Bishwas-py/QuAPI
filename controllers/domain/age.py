from core import essentials
import requests

def post(request: essentials.Request):
    domain_name = request.body.get("name")
    if domain_name:
        response = requests.get(f'https://ipty.de/domage/api.php?domain={domain_name}&mode=full')
        data = response.json()
    else:
        data = {
            "error": "No domain name provided"
        }
    return data
    