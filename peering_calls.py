import ssl
from urllib.request import urlopen, HTTPError
import json
import requests


def get_asn_ix(asn):
    ix = {}
    try:
        # REST API Calls
        obj = requests.get("https://peeringdb.com/api/net?asn=%s" % asn)
        obj_dict = obj.json()
        net_id = obj_dict["data"][0]["id"] # ID is the peeringDB index for an AS Number
        net_obj = requests.get("https://peeringdb.com/api/net/%s" % net_id) # Using this ID, API call to get more detailed information
        net_obj_dict = net_obj.json()

        # Populate a dictionary of IX name and ID per AS
        for ixlan in net_obj_dict["data"][0]["netixlan_set"]:
            ix[ixlan["ix_id"]] =  ixlan["name"]

        return ix
    except HTTPError as e:
        print(e)
        return

def get_asn_ips(asn):
    ip_dets = {}
    ip_details = []
    try:
        # REST API Calls
        # Call to peeringDB API with ASN Number, returns json format
        obj = requests.get("https://peeringdb.com/api/net?asn=%s" % asn)
        obj_dict = obj.json()
        net_id = obj_dict["data"][0]["id"] # ID is the peeringDB index for the AS Number
        net_obj = requests.get("https://peeringdb.com/api/net/%s" % net_id)
        net_obj_dict = net_obj.json()

        # Populate a dictionary of IX id with Name, IPv4 and IPv6
        for ixlan in net_obj_dict["data"][0]["netixlan_set"]:
            ip_dets[ixlan["id"]] = ixlan["name"], ixlan["ipaddr4"], ixlan["ipaddr6"]
            ip_details.append(ip_dets[ixlan["id"]])

        return ip_details

    except HTTPError as e:
        print(e)
        return

def get_prefix_and_name(asn):
    try:
        # REST API Calls
        obj = requests.get("https://peeringdb.com/api/net?asn=%s" % asn)
        obj_dict = obj.json()
        net_id = obj_dict["data"][0]["id"] # ID is the peeringDB index for an AS Number
        net_obj = requests.get("https://peeringdb.com/api/net/%s" % net_id)
        net_obj_dict = net_obj.json()

        desc = net_obj_dict["data"][0]["name"]
        ipv4Prefixes = net_obj_dict["data"][0]["info_prefixes4"]
        ipv6Prefixes = net_obj_dict["data"][0]["info_prefixes6"]

        return desc, ipv4Prefixes, ipv6Prefixes

    except HTTPError as e:
        print(e)
        return

