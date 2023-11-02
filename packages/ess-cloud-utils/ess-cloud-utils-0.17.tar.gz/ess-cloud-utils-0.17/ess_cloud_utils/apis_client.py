#!/usr/bin/env python
import requests
from .eureka import Eureka


class ApisClient(object):
    session = requests.Session()

    @staticmethod
    def get(service_name, endpoint, headers=None, timeout=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = ApisClient.session.get(url, headers=headers, timeout=timeout).json()
        return response

    @staticmethod
    def post(service_name, endpoint, body=None, headers=None, json=None, files=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = ApisClient.session.post(url, data=body, headers=headers, json=json, files=files)
        return response

    @staticmethod
    def put(service_name, endpoint, body=None, headers=None, json=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = ApisClient.session.put(url, data=body, headers=headers, json=json)
        return response

    @staticmethod
    def delete(service_name, endpoint, body=None, headers=None, json=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = ApisClient.session.delete(url, data=body, headers=headers, json=json)
        return response

