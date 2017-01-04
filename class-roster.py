# The MIT License (MIT)
#
# Copyright (c) 2017 Tyler Clair
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import requests
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'teacher_token')
domain = config.get('instance', 'prod')
headers = {'Authorization': 'Bearer {}'.format(token)}
# Change the course id to the id of your course i.e. https://abc.instructure.com/courses/12345
course = 12345
roster = []
uri = '{}/api/v1/courses/{}/users'.format(domain, course)
params = {
    'per_page': 100,
    'enrollment_type': ['student'],
    'include[]': 'email'
}
r = requests.get(uri, headers=headers, params=params)
raw = r.json()
for student in raw:
    roster.append(student)

while r.links['current']['url'] != r.links['last']['url']:
    r = requests.get(r.links['next']['url'], headers=headers)
    raw = r.json()
    for student in raw:
        roster.append(student)

print('Name,A-number,Email')
for student in roster:
    if 'sis_login_id' in student:
        print('\"{}\",{},{}'.format(student['sortable_name'], student['sis_login_id'], student['email'].lower()))
    else:
        print('\"{}\",{},{}'.format(student['sortable_name'], student['login_id'], student['email'].lower()))
