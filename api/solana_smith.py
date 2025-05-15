import base64 
import requests
import json
from django.conf import settings
from solders.keypair import Keypair



def deploy_coin(name: str, ticker: str, image_path: str, description: str):
    mint_keypair = Keypair()

    form_data = {
        'name': name,
        'symbol': ticker,
        'description': description
    }

    with open(image_path, 'rb') as f:
        file_content = f.read()

    files = {
        'file': ('example.png', file_content, 'image/png')
    }

    metadata_response = requests.post("https://pump.fun/api/ipfs", data=form_data, files=files)
    metadata_response_json = metadata_response.json()
    
    token_metadata = {
        'name': form_data['name'],
        'symbol': form_data['symbol'],
        'uri': metadata_response_json['metadataUri']
    }

    response = requests.post(
        f"https://pumpportal.fun/api/trade?api-key={settings.PUMP_API_KEY}",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'action': 'create',
            'tokenMetadata': token_metadata,
            'mint': str(mint_keypair),
            'denominatedInSol': 'true',
            'amount': 0.0001,
            'slippage': 10,
            'priorityFee': 0.0005,
            'pool': 'pump'
        })
    )

    if response.status_code == 200:
        data = response.json()

        return f"https://solscan.io/tx/{data['signature']}", base64.b64encode(file_content).decode('utf-8')

    error = f'STATUS CODE: {response.status_code} :: REASON: {str(response.reason)}'
    raise Exception(error)