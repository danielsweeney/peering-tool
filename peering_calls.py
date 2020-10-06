import ssl
from urllib.request import urlopen, HTTPError
import json


def get_asn_ix(asn):
    ix = {}
    context = ssl._create_unverified_context()  # Hacky way to get round SSL Verification Failure below
    # urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)>
    try:
        # Call to peeringDB API with ASN Number, returns json format details
        http_obj = urlopen("https://peeringdb.com/api/net?asn=%s" % asn, context=context)
        #"https://<username>:<password>@peeringdb.com/api/net?asn=%s"
        http_obj_dict = json.load(http_obj) # Load the recived data into json format for manipulation
        net_id = http_obj_dict["data"][0]["id"] # ID is the peeringDB index for an AS Number
        #print("ID: {}".format(net_id))
        net_http_obj = urlopen("https://peeringdb.com/api/net/%s" % net_id, context=context)    # Using this ID, API call to peeringDB to get more detailed info
        net_http_obj_dict = json.load(net_http_obj) # Load the received data into json format for manipulation
        com_http_obj = urlopen("https://peeringdb.com/api/net/%s" % net_id, context=context)
        com_http_obj_dict = json.load(com_http_obj)

        # Populate a dictionary of IX name and ID per AS
        for ixlan in net_http_obj_dict["data"][0]["netixlan_set"]:
            ix[ixlan["ix_id"]] =  ixlan["name"]

        return ix
    except HTTPError as e:
        print(e)
        return

def get_asn_ips(asn):
    ip_dets = {}
    ip_details = []
    context = ssl._create_unverified_context()  # Hacky way to get round SSL Verification Failure below
    # urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)>
    try:
        # Call to peeringDB API with ASN Number, returns json format details
        http_obj = urlopen("https://peeringdb.com/api/net?asn=%s" % asn, context=context)
        #"https://<username>:<password>@peeringdb.com/api/net?asn=%s"
        http_obj_dict = json.load(http_obj) # Load the recived data into json format for manipulation
        net_id = http_obj_dict["data"][0]["id"] # ID is the peeringDB index for an AS Number
        #print("ID: {}".format(net_id))
        net_http_obj = urlopen("https://peeringdb.com/api/net/%s" % net_id, context=context)    # Using this ID, API call to peeringDB to get more detailed info
        net_http_obj_dict = json.load(net_http_obj) # Load the received data into json format for manipulation
        com_http_obj = urlopen("https://peeringdb.com/api/net/%s" % net_id, context=context)
        com_http_obj_dict = json.load(com_http_obj)

        # Populate a dictionary of IX name and ID per AS
        for ixlan in net_http_obj_dict["data"][0]["netixlan_set"]:
            ip_dets[ixlan["id"]] =  ixlan["name"] , ixlan["ipaddr4"], ixlan["ipaddr6"]
            ip_details.append(ip_dets[ixlan["id"]])

        return ip_details

    except HTTPError as e:
        print(e)
        return

def get_prefix_and_name(asn):
    context = ssl._create_unverified_context()  # Hacky way to get round SSL Verification Failure below
    # urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)>
    try:
        # Call to peeringDB API with ASN Number, returns json format details
        http_obj = urlopen("https://peeringdb.com/api/net?asn=%s" % asn, context=context)
        #"https://<username>:<password>@peeringdb.com/api/net?asn=%s"
        http_obj_dict = json.load(http_obj) # Load the recived data into json format for manipulation
        net_id = http_obj_dict["data"][0]["id"] # ID is the peeringDB index for an AS Number
        #print("ID: {}".format(net_id))
        net_http_obj = urlopen("https://peeringdb.com/api/net/%s" % net_id, context=context)    # Using this ID, API call to peeringDB to get more detailed info
        net_http_obj_dict = json.load(net_http_obj) # Load the received data into json format for manipulation

        desc = net_http_obj_dict["data"][0]["name"]
        ipv4Prefixes = net_http_obj_dict["data"][0]["info_prefixes4"]
        ipv6Prefixes = net_http_obj_dict["data"][0]["info_prefixes6"]

        return desc, ipv4Prefixes, ipv6Prefixes

    except HTTPError as e:
        print(e)
        return

