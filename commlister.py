import sys
import csv
import time
import requests
timestamp = time.strftime("%m%d%y-%I%M%S")
from configparser import ConfigParser
config = ConfigParser()
config.read("config.cfg")
token = config.get("auth", "token")
domain = config.get("instance", "domain")
headers = {"Authorization": "Bearer %s" % token}
comm_type = "email"
csv_file = sys.argv[1]
f = open(csv_file, 'rU')
output_file = open('comm_channels' + timestamp + '.csv', 'w')
output_file.write('user_id,address' + '\n')
studentreader = csv.DictReader(f)

def getLoginId(id):
    uri = domain + "/api/v1/users/%d/profile" % int(id)
    r = requests.get(uri, headers=headers)
    raw = r.json()
    return raw.get('login_id')

for student in studentreader:
    login_id = getLoginId(student['id'])
    uri = domain + "/api/v1/users/%s/communication_channels" % student["id"]
    r = requests.get(uri, headers=headers)
    all_channels = r.json()
    for comm in all_channels:
        if comm['type'] == comm_type:
            output_file.write(login_id + "," + comm['address'] + "\n")


f.close()
output_file.close()
