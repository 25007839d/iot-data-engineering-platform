import requests

url = "https://noatyhntldvoisaqxvip.supabase.co/rest/v1/sensor_data_v1?select=*"

headers = {
    "apikey": "sb_publishable_684X-Ts6e7ozMww6pI4dbA_Nwa4f4hz"
}

r = requests.get(url, headers=headers, timeout=60)

print(r.status_code)
print(r.text[:500])