__author__ = 'Tyler'
import requests
from configparser import ConfigParser
import csv
import time
import sys
timestamp = time.strftime("%m%d%y-%I%M%S")
config = ConfigParser()
config.read("config.cfg")
token = config.get("auth", "token")
domain = config.get("instance", "domain")
headers = {"Authorization": "Bearer %s" % token}
csv_file = sys.argv[1]
f = open(csv_file, 'rU')
output_file = open('canvasids' + timestamp + '.csv', 'w')
output_file.write('id' + '\n')
studentreader = csv.DictReader(f)
for student in studentreader:
    uri = domain + "/api/v1/users/sis_user_id:%s/profile" % student['user_id']
    r = requests.get(uri, headers=headers)
    raw = r.json()
    output_file.write(str(raw.get('id')) + '\n')

f.close()
output_file.close()
