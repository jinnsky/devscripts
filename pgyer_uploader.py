#!/usr/bin/python
#coding=utf-8

import os
import requests
import time
import re
from datetime import datetime

# configuration for pgyer
API_KEY = "fe4bd35868df9840a9b4984d1881608e"
USER_KEY = "8443cf610ab30c30e0e0180ee2990798"
PGYER_UPLOAD_URL = "https://www.pgyer.com/apiv1/app/upload"


def parseUploadResult(jsonResult):
    print 'post response: %s' % jsonResult
    resultCode = jsonResult['code']

    if resultCode != 0:
        print "Upload Fail!"
        raise Exception("Reason: %s" % jsonResult['message'])

    return jsonResult['data']

def uploadIpaToPgyer(ipaPath, updateDescription):
    # refer to https://www.pgyer.com/doc/api#uploadApp
    print "Begin to upload ipa to Pgyer: %s" % ipaPath

    headers = {'enctype': 'multipart/form-data'}
    payload = {
        'uKey': USER_KEY,
        '_api_key': API_KEY,
        'publishRange': '2',
        'isPublishToPublic': '2',
        'updateDescription': updateDescription
    }

    try_times = 0
    while try_times < 5:
        try:
            print "uploading ... %s" % datetime.now()

            ipa_file = {'file': open(ipaPath, 'rb')}
            response = requests.post(PGYER_UPLOAD_URL,
                headers = headers,
                files = ipa_file,
                data = payload
            )
            assert response.status_code == requests.codes.ok
            result = response.json()
            print "Upload Success"

            json_data = parseUploadResult(result)
            print "appDownloadPage: https://www.pgyer.com/%s" % json_data['appShortcutUrl']

            return json_data
        except requests.exceptions.ConnectionError:
            print "requests.exceptions.ConnectionError occured!"
            time.sleep(60)
            print "try again ... %s" % datetime.now()
            try_times += 1
        except Exception as e:
            print "Exception occured: %s" % str(e)
            time.sleep(60)
            print "try again ... %s" % datetime.now()
            try_times += 1

        if try_times >= 5:
            raise Exception("Failed to upload ipa to Pgyer, retried 5 times.")

def saveQRCodeImage(appQRCodeURL, output_folder):
    response = requests.get(appQRCodeURL)
    qr_image_file_path = os.path.join(output_folder, 'QRCode.png')
    if response.status_code == 200:
        with open(qr_image_file_path, 'wb') as file:
            file.write(response.content)
    print 'Save QRCode image to file: %s' % qr_image_file_path
