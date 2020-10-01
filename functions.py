from data import *
import requests


def test(endpoint,option,tokenAPI):
    url = endpoint+"/"+option+"?tokenAPI="+tokenAPI
    print(requests.get(url))

option="safes"
test(endpoint,option,tokenAPI)