import requests
import csv
from configparser import ConfigParser
config = ConfigParser()
config.read("config.cfg")
token = config.get("auth", "token")
domain = config.get("instance", "domain")
headers = {"Authorization" : "Bearer %s" % token}
source_course_id = 311693
csv_file = ""
payload = {'migration_type': 'course_copy_importer', 'settings[source_course_id]': source_course_id}
with open(csv_file, 'rb') as courses:
    coursesreader = csv.reader(courses)
    for course in coursesreader:
        uri = domain + "/api/v1/courses/sis_course_id:%s/content_migrations" % course
        r = requests.post(uri, headers=headers,data=payload)
        print r.status_code + " " + course