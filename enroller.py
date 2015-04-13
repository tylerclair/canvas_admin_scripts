import requests
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'token')
domain = config.get('instance', 'domain')
headers = {'Authorization': 'Bearer %s' % token}
courses = []
user_id = 12345
payload = {'enrollment[user_id]': 'sis_login_id:' + user_id,
           'enrollment[type]': 'DesignerEnrollment',
           'enrollment[enrollment_state]': 'active'}

for course in courses:
    uri = domain + "/api/v1/courses/%d/enrollments" % course
    r = requests.post(uri, headers=headers, data=payload)
    print("{0}, {1}, {2}".format(r.status_code,course,uri))