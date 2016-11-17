from configparser import ConfigParser
import sys
import requests
import hashlib
import hmac
import base64
import datetime
from pprint import pprint
config = ConfigParser()
config.read('config/config.cfg')
# request pieces
cd_key = config.get('auth', 'canvas_data_key')
cd_secret = config.get('auth', 'canvas_data_secret')
method = 'GET'
cd_host = config.get('instance', 'data')
hostname = 'portal.inshosteddata.com'
path = '/api/schema/latest'
currentTime = datetime.datetime.utcnow()
timestamp = currentTime.strftime('%a, %d %b %Y %H:%M:%S GMT')

# Build request message
requestParts = [
    method,
    hostname,
    '',  # Content Type
    '',  # Content MD5
    path,
    '',
    timestamp,
    cd_secret
]

# Build Request

requestMessage = '\n'.join(requestParts)
hmacObject = hmac.new(cd_secret.encode(encoding='UTF-8'), digestmod=hashlib.sha256)
hmacObject.update(requestMessage.encode(encoding='UTF-8'))
hmac_digest = hmacObject.digest()
sig = base64.standard_b64encode(hmac_digest)
sig2 = sig.decode(encoding='UTF-8')
headers = {'Authorization': 'HMACAuth {}:{}'.format(cd_key, sig2),
           'Date': timestamp}
r = requests.get('{}{}'.format(cd_host, path), headers=headers)
raw = r.json()
pprint(raw)
