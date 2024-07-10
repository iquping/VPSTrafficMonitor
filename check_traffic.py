import requests
import telegram
import yaml

with open("config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

API_KEYS = config['api_keys']
TELEGRAM_TOKEN = config['telegram']['token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']
API_URLS = config['api_urls']
INSTANCE_IDS = config['instance_ids']

def check_traffic_and_shutdown():
    for provider, api_key in API_KEYS.items():
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(API_URLS[provider], headers=headers)
        if response.status_code == 200:
            data = response.json()
            remaining_traffic = parse_traffic_data(provider, data)
            if remaining_traffic <= 0:
                for instance_id in INSTANCE_IDS[provider]:
                    shutdown_vm(provider, api_key, instance_id)
                send_notification(provider)
        else:
            print(f"Failed to get data from {provider}: {response.status_code}")

def parse_traffic_data(provider, data):
    if provider == 'vultr':
        return data['account']['balance']
    elif provider == 'digital_ocean':
        return data['droplets'][0]['disk']
    elif provider == 'linode':
        return data['data']['transfer_pool']['quota']
    return 0

def shutdown_vm(provider, api_key, instance_id):
    if provider == 'vultr':
        shutdown_url = f'https://api.vultr.com/v2/instances/{instance_id}/halt'
    elif provider == 'digital_ocean':
        shutdown_url = f'https://api.digitalocean.com/v2/droplets/{instance_id}/actions'
    elif provider == 'linode':
        shutdown_url = f'https://api.linode.com/v4/linode/instances/{instance_id}/shutdown'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(shutdown_url, headers=headers)
    if response.status_code in [200, 202, 204]:
        print(f"{provider} VM {instance_id} shut down successfully.")
    else:
        print(f"Failed to shut down {provider} VM {instance_id}: {response.status_code}")

def send_notification(provider):
    send_telegram(provider)

def send_telegram(provider):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"The {provider} VMs have been shut down due to no remaining traffic.")

if __name__ == "__main__":
    check_traffic_and_shutdown()
