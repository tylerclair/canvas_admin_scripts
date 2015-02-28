__author__ = 'Tyler'
import sys
import csv
import requests
import logging
import time
# Setup logging
timestamp = time.strftime("%m%d%y-%I%M%S")
new_logging_file = timestamp + '.log'
logging.basicConfig(filename=new_logging_file, level=logging.INFO)
# Read Config Settings
from configparser import ConfigParser
config = ConfigParser()
config.read("config.cfg")
token = config.get("auth", "token")
domain = config.get("instance", "domain")
headers = {"Authorization": "Bearer %s" % token}
# Get input file from argument
csv_file = sys.argv[1]
logging.info('CSV file: ' + csv_file)
f = open(csv_file, 'rU')
output_file = open('enrollments-' + timestamp + '.csv', 'w')
output_file.write('user_id,role,section_id,status' + '\n')
enrollmentreader = csv.DictReader(f)
for student in enrollmentreader:
    uri = domain + "/api/v1/sections/sis_section_id:%s/enrollments?user_id=%s" % (student['section_id'], student['canvas_id'])
    r = requests.get(uri, headers=headers)
    if r.status_code == 200:
        raw = r.json()
        logging.info(uri + " " + str(r.status_code))
        for enrollment in raw:
            if enrollment["sis_import_id"]:
                    currentstudent = enrollment['user']['sis_user_id'] + ',student,' + student['section_id'] + ',deleted' + '\n'
                    output_file.write(currentstudent)
                    # print enrollment['user']['sis_user_id'] + ",", student['section_id']
                    # print student['section_id'], ",", student['canvas_id']

    else:
        logging.warning('Bad request for student ' + student['canvas_id'] + ' in ' + student['section_id'])
        logging.warning(uri + " " + str(r.status_code))
f.close()
output_file.close()