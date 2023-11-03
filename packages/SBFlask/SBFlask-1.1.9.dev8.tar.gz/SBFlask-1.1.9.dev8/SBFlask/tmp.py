import json

response = {}
response['Success'] = ['192.168.1.2', '192.168.1.3']
x = json.dumps(response, indent=4)

print(x)