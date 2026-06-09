import requests

url = "https://noatyhntldvoisaqxvip.supabase.co/rest/v1/sensor_data?select=*"

headers = {
    "apikey": "sb_publishable_684X-Ts6e7ozMww6pI4dbA_Nwa4f4hz"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text[:500])