#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: audit
@time: 2023/10/30
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import base64
import hmac
import hashlib
import datetime
import json
from urllib import parse
import uuid
import requests
import pytz




def build_audit_url(audit_url, secret, accessKeyId, appid):
    fmt = "%Y-%m-%dT%H:%M:%S%z"
    uid = uuid.uuid4()

    timestamp = datetime.datetime.now(tz=pytz.utc).timestamp()

    aware_datetime = datetime.datetime.fromtimestamp(timestamp, pytz.utc)

    ts = aware_datetime.strftime(fmt)
    params = {
        "appId": appid,
        "accessKeyId": accessKeyId,
        "utc": ts,
        "uuid": str(uid),
    }
    params = dict(sorted(params.items()))
    string = parse.urlencode(params)
    signature_sha = hmac.new(secret.encode('utf-8'), string.encode('utf-8'), digestmod=hashlib.sha1).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    s = string + "&signature={}".format(signature_sha)
    request_url = audit_url + "?" + s
    return request_url


