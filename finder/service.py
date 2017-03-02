import re
import requests
from requests import RequestException

from finder.ext.exceptions import FieldEqualError, FieldNameError, ArgsError
from finder.ext.redis_init import redis_db


class Finder(object):
    key = 'F_FINDER'

    @staticmethod
    def send_request(url, timeout=3):
        """
        http[s]://addr/ping
        :param url:
        :param timeout:
        :rtype: dict
        {
            "error_code":0,
        }
        :return:
        """
        if url.split("/")[-1] == "":
            url += "ping"
        else:
            url += "/ping"
        try:
            requests.get(url, timeout=timeout)
            return True
        except RequestException:
            return False

    @classmethod
    def ls(cls):
        """
        返回所有可用
        :return:
        :rtype: list

        [
            "ip1",
            ...
        ]
        """
        rs = []
        ips = [redis_db.hget(cls.key, i) for i in redis_db.hkeys(cls.key)]
        if not ips:
            return rs
        return [rs.append(ip.decode()) for ip in ips if cls.send_request(ip.decode())]

    @classmethod
    def check(cls):
        """
        检查所有，然后返回可用的和不可用的
        {
            "active":[

            ],
            "inactive":[

            ]
        }

        :return:
        """
        rs = {
            "active": [],
            "inactive": []
        }
        ips = [redis_db.hget(cls.key, i) for i in redis_db.hkeys(cls.key)]
        if not ips:
            return rs
        [rs["active"].append(ip.decode()) if cls.send_request(ip.decode()) else rs["inactive"].append(ip.decode())
            for ip in ips]
        return rs

    @classmethod
    def register(cls, field, value, force=False, **kwargs):
        """
            添加，不做可用性检查
        :param field: K_EMAIL_
        :param value: "http[s]://addr:port"
        :param force: 强制性覆盖
        :return:
        """
        if (not field) or (not value):
            raise ArgsError
        p = re.compile("^[A-Z]_[A-Z]{1,20}_")
        if not p.match(field):
            raise FieldNameError
        if force not in (True, "True", "true"):
            fields = (i.decode() for i in redis_db.hkeys(cls.key))
            for f in fields:
                if f == field:
                    raise FieldEqualError
        redis_db.hset(cls.key, field, value)

    @classmethod
    def get(cls, field):
        """
        返回此field对应的信息，不做可用性检查
        :type field: str
        :param field:
        :return: None or url
        """
        return redis_db.hget(cls.key, field)

    @classmethod
    def remove(cls, field):
        """
        删除此field
        :param field:
        :return: 1:True 0:False
        """
        return redis_db.hdel(cls.key, field)
