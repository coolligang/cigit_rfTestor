# encoding=utf-8
import requests
import json
import re
import base64
from jsonpath_rw import parse
from unittest.util import safe_repr
import hashlib
import time


class RfeLibrary:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    longMessage = False

    def __init__(self):
        self.s = requests.session()

    def _formatMessage(self, msg, standardMsg):
        """Honour the longMessage attribute when generating failure messages.
        If longMessage is False this means:
        * Use only an explicit message if it is provided
        * Otherwise use the standard message for the assert

        If longMessage is True:
        * Use the standard message
        * If an explicit message is provided, plus ' : ' and the explicit message
        """
        if not self.longMessage:
            return msg or standardMsg
        if msg is None:
            return standardMsg
        try:
            # don't switch to '{}' formatting in Python 2.X
            # it changes the way unicode input is handled
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return '%s : %s' % (safe_repr(standardMsg), safe_repr(msg))

    def assertJson(self, expected, actual, assertType=1, msg=None):
        """
        Checks whether actual is a superset of expected. \n
        :param expected:  \n
        :param actual:  \n
        :param assertType: 0 模糊匹配  1 精确匹配  \n
        :param msg:  \n
        :return:  \n
        """
        expected = json.loads(expected)
        actual = json.loads(actual)
        assertType = int(assertType)
        missing = []
        mismatched = []
        for key, value in expected.iteritems():
            if key not in actual:
                missing.append(key)
            elif value != actual[key]:
                if assertType == 0 and type(value) == type(actual[key]):
                    continue
                mismatched.append(
                    '%s(expected: %s, actual: %s)' % (safe_repr(key), safe_repr(value), safe_repr(actual[key])))
        if not (missing or mismatched):
            return
        standardMsg = ''
        if missing:
            standardMsg = 'Missing: %s' % ','.join(safe_repr(m) for m in missing)
        if mismatched:
            if standardMsg:
                standardMsg += '; '
            standardMsg += 'Mismatched values: %s' % ','.join(mismatched)
        raise AssertionError(self._formatMessage(msg, standardMsg))

    def getValueFromJson(self, str_json, jsonpath):
        """
        获取json中某个key对应的value\n
        :param str_json: str json\n
        :param jsonpath: str jsonpath\n
        :return: obj 通过jsonpath在json中得到的value 可能是 int str obj ...\n
        """
        jsonxpr = parse(jsonpath)
        return jsonxpr.find(json.loads(str_json))[0].value

    def reqByJson(self, method, url, json=None, headers=None, cookies=None):
        """
        通过 Json 的方式发起请求\n
        :param method: post\get\...\n
        :param url: str\n
        :param form: dictionary\n
        :param headers: dictionary\n
        :param cookies: response_obj
        :return: response_obj
        """
        res = self.s.request(method.upper(), url, json=json, headers=headers, cookies=cookies)
        return res

    def getFile(self, path):
        with open(path, 'r') as fin:
            data = fin.read()
            return data

    def toBase64(self, img_path):
        """
        将图片转为base64编码  \n
        :param img_path: 图片路径  \n
        :return:  \n
        """
        with open(img_path, 'rb') as fin:  # 二进制方式打开图片
            image_data = fin.read()
            base64_data = base64.b64encode(image_data)
            return base64_data

    def toMD5(self, str_content):
        """
        将传入字符串进行md5加密  \n
        :param str: 要加密的字符串  \n
        :return: \n
        """
        m = hashlib.md5()
        m.update(str_content)
        str_encoding = m.hexdigest()
        return str_encoding

    def getTimestamp(self):
        """
        返回毫秒级时间戳 \n
        :return:
        """
        return int(round(time.time() * 1000))
