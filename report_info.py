import requests
import time
import csv
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'token')
domain = config.get('instance', 'prod')
account = config.get('accounts', 'prod')
headers = {'Authorization': 'Bearer {}'.format(token)}

# Get report names

uri = '{}/api/v1/accounts/{}/reports'.format(domain, account)
r = requests.get(uri, headers=headers)
raw = r.json()
with open('reports.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'title', 'parameters']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for report in raw:
        if not report['parameters']:
            writer.writerow({'name': report['report'], 'title': report['title'], 'parameters': 'None'})
        else:
            param_list = ', '.join([parameter for parameter in report['parameters']])
            writer.writerow({'name': report['report'], 'title': report['title'], 'parameters': param_list})
print('Done')
