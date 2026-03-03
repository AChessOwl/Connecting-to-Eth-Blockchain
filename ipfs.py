import requests
import json

PROJECT_ID = "BL4gYbdukv1ZDL6yZLlzVKREfkXaR_TZe8QRs_VrdWhj_PT7zEoS9KTDKJLpiEKnkQAefon3zxIwNZUBDg7qDoA"
PROJECT_SECRET = "607fc8ff69aee6fb2f5a179411dcc37fe5bcd5f9d380cb46354e42e815e4925a"

def _get_auth_header():
    auth = base64.b64encode(f"{PROJECT_ID}:{PROJECT_SECRET}".encode()).decode()
    return {
        "Authorization": f"Basic {auth}"
    }

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"
    
    # Convert dictionary to JSON string
    json_data = json.dumps(data)
    
    url = "https://ipfs.infura.io:5001/api/v0/add"
    
    files = {
        "file": ("data.json", json_data)
    }
    
    headers = _get_auth_header()
    
    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    
    # Infura returns CID under "Hash"
    cid = result["Hash"]
    
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"
    
    url = f"https://ipfs.infura.io:5001/api/v0/cat?arg={cid}"
    
    headers = _get_auth_header()
    
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    
    raw_content = response.content.decode()
    
    if content_type == "json":
        data = json.loads(raw_content)
    else:
        data = raw_content
    
    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    
    return data