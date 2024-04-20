import base64
import json
import pprint

import requests
import xmltodict


def encode_base64(data: str):
    return base64.b64encode(data.encode('utf-8'))


def xml_to_dict(text):
        return xmltodict.parse(text)


def test():
    url = 'http://app.wenku8.com/android.php'
    response = requests.post(
        url=url,
        data={
            'request': 'YWN0aW9uPWJvb2smZG89bWV0YSZhaWQ9Mjc0MiZ0PTA='
        },
        allow_redirects=False
    )
    return response.text


if __name__ == '__main__':
    # print(encode_base64('action=book&do=meta&aid=1973&t=0'))
    # print(xml_to_dict())
    res = xml_to_dict(test())
    pprint.pprint(res)