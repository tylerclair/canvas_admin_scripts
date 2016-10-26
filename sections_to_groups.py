# MIT License
#
# Copyright (c) [2016] [Tyler Clair]
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

# Python 3 script
import requests
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'token')
domain = config.get('instance', 'prod')
headers = {'Authorization': 'Bearer {}'.format(token)}

# Configuration
course_id = 267049
group_name = 'Section Groups'


# Create new Group category
def create_group_category(w_course_id, w_group_name):
    uri = '{}/api/v1/courses/{}/group_categories'.format(domain, w_course_id)
    payload = {'name': w_group_name}
    r = requests.post(uri, data=payload, headers=headers)
    raw = r.json()
    return raw['id']


# Create new group
def create_group(cat_id, name):
    uri = '{}/api/v1/group_categories/{}/groups'.format(domain, cat_id)
    payload = {'name': name}
    r = requests.post(uri, data=payload, headers=headers)
    raw = r.json()
    return raw


# Create group membership
def create_group_membership(group_id, user_id):
    payload = {'user_id': user_id}
    uri = '{}/api/v1/groups/{}/memberships'.format(domain, group_id)
    r = requests.post(uri, data=payload, headers=headers)
    raw = r.json()
    return raw


# Get list of sections and students
def get_sections_students(w_course_id):
    section_info = []
    uri = '{}/api/v1/courses/{}/sections'.format(domain, w_course_id)
    # Change the include[] param to 'include[]': ['students', 'enrollments'] if you want enrollments as well.
    # Enrollments include param is not needed for this script but I am including it for syntax reference.
    params = {'include[]': 'students',
              'per_page': 100}
    r = requests.get(uri, params=params, headers=headers)
    raw = r.json()
    for w_section in raw:
        section_info.append(w_section)
    return section_info

if __name__ == '__main__':
    # Create new category called Section Groups, you can change the name to anything you want.
    # Change the group_name variable in the Configuration section
    group_cat_id = create_group_category(course_id, group_name)
    # Get a list of sections with included students.
    # Change the course_id variable in the Configuration section
    sections = get_sections_students(course_id)
    # For each section in the course create a group with the same name as the section name and print results.
    # This loop will also create the student's membership in the group.
    for section in sections:
        new_group = create_group(group_cat_id, section['name'])
        print('-- Created group named: {} with id {}'.format(new_group['name'], new_group['id']))
        # For each student in the section make them a member of the newly created group based off of the section.
        for student in section['students']:
            create_group_membership(new_group['id'], student['id'])
            print('{} is now a member of the {} group'.format(student['name'], new_group['name']))
