import requests
import time
from configparser import ConfigParser
config = ConfigParser()
config.read('config/config.cfg')
token = config.get('auth', 'token')
domain = config.get('instance', 'prod')
account = config.get('accounts', 'prod')
headers = {'Authorization': 'Bearer {}'.format(token)}


def start_report(report, parameters=None, term=None):
    if term and parameters:
        term_parameters = {'parameters[enrollment_term_id]': 'sis_term_id:{}'.format(term)}
        report_parameters = term_parameters.copy()
        report_parameters.update(parameters)
        uri = '{}/api/v1/accounts/{}/reports/{}'.format(domain, account, report)
        r = requests.post(uri, data=report_parameters, headers=headers)
        raw = r.json()
        return raw['id']
    elif term and not parameters:
        term_parameters = {'parameters[enrollment_term_id]': 'sis_term_id:{}'.format(term)}
        report_parameters = term_parameters
        uri = '{}/api/v1/accounts/{}/reports/{}'.format(domain, account, report)
        r = requests.post(uri, data=report_parameters, headers=headers)
        raw = r.json()
        return raw['id']
    elif parameters and not term:
        report_parameters = parameters
        uri = '{}/api/v1/accounts/{}/reports/{}'.format(domain, account, report)
        r = requests.post(uri, data=report_parameters, headers=headers)
        raw = r.json()
        return raw['id']
    else:
        uri = '{}/api/v1/accounts/{}/reports/{}'.format(domain, account, report)
        r = requests.post(uri, headers=headers)
        raw = r.json()
        return raw['id']


def check_progress(report, report_id):
    uri = '{}/api/v1/accounts/{}/reports/{}/{}'.format(domain, account, report, report_id)
    r = requests.get(uri, headers=headers)
    raw = r.json()
    return raw['progress']


def download_report(report, report_id):
    ri_uri = '{}/api/v1/accounts/{}/reports/{}/{}'.format(domain, account, report, report_id)
    ri_r = requests.get(ri_uri, headers=headers)
    ri_raw = ri_r.json()
    rd_uri = ri_raw['attachment']['url']
    rd_r = requests.get(rd_uri, allow_redirects=True)
    rd_filename = ri_raw['attachment']['filename']
    with open('downloaded_reports/' + rd_filename, 'w+b') as filename:
        filename.write(rd_r.content)
    return 'report downloaded as {}'.format(rd_filename)


if __name__ == '__main__':

    rpt_params = {'parameters[enrollments]': True,
                  'parameters[created_by_sis]': True}
    report_name = 'sis_export_csv'
    rpt_id = start_report(report_name, rpt_params, 201640)
    print('Report ID: {}'.format(rpt_id))
    time.sleep(1)
    print ('checking progress')
    rpt_status = check_progress(report_name, rpt_id)
    while rpt_status < 100:
        rpt_status = check_progress(report_name, rpt_id)
        print('Progress: {}'.format(rpt_status))
        time.sleep(5)
    print('report ready to download')
    save_report = download_report(report_name, rpt_id)
    print(save_report)
