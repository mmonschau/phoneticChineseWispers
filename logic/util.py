# coding=utf-8
from time import time
from uuid import uuid4


def unique_prefix():
    unixtimestamp = int(time())
    randomUUID = uuid4()
    return str(unixtimestamp) + "_" + str(randomUUID).replace("-", "_")
