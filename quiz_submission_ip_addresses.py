import requests
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'token')
domain = config.get('instance', 'domain')
headers = {'Authorization': 'Bearer %s' % token}
uri = domain + '/api/v1/courses/course_id:/quizzes/quiz_id:/submissions?per_page=10'

data_set = []
r = requests.get(uri, headers=headers)
raw = r.json()
for item in raw['quiz_submissions']:
    data_set.append(item)

while r.links['current']['url'] != r.links['last']['url']:
    r = requests.get(r.links['next']['url'], headers=headers)
    raw = r.json()
    for item in raw['quiz_submissions']:
        data_set.append(item)

for item in data_set:
    uri2 = domain + '/api/v1/users/{0}/page_views?start_time={1}&end_time={2}'.format(item['user_id'], item['started_at'], item['finished_at'])
    r = requests.get(uri2, headers=headers)
    raw = r.json()
    try:
        uri3 = domain + '/api/v1/users/{0}/profile'.format(item['user_id'])
        r1 = requests.get(uri3, headers=headers)
        raw2 = r1.json()
        print("\"{0}\",{1},{2},{3},{4}".format(raw2['name'], raw2['sis_login_id'], item['started_at'], item['finished_at'], raw[0]['remote_ip']))
    except KeyError:
        print(item['user_id'], 'Check Manually')
        continue