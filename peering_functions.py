from peering_calls import get_asn_ix, get_asn_ips, get_prefix_and_name
import ssl
from urllib.request import urlopen, HTTPError
import json
import xlsxwriter 

def compare(asn1, asn2):
    local_ix = get_asn_ix(asn1)
    target_ix = get_asn_ix(asn2)

    shared_ix =[]
    if local_ix and target_ix:
        for shared in set(local_ix).intersection(target_ix):
            shared_ix.append(local_ix[shared])
    return shared_ix

def list_IX(asn):
    ixlan = {}
    context = ssl._create_unverified_context()
    try:
        obj = urlopen("https://www.peeringdb.com/api/netixlan?asn=%s" % asn, context=context)
        ixlan_dict = json.load(obj)
        for line in ixlan_dict["data"]:
            ixlan[line["ixlan_id"]] = line["name"]
        #print(ixlan)
        peerlist = {}
        #with open('peers.csv', 'w', encoding='utf-8') as f:
        #peer_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  lineterminator = '\n')
        
        workbook = xlsxwriter.Workbook('Peers-AS' + asn + '.xlsx')
        #worksheet = workbook.add_worksheet('All Peers IX')

        for ixlan_id_key in ixlan:
            ixlan_obj = urlopen("https://www.peeringdb.com/api/net?ixlan_id=%s" % str(ixlan_id_key), context=context)
            ixlan_obj_dict = json.load(ixlan_obj)
            #f.write("Exchange: %s" % ixlan[ixlan_id_key] + "\n")
            #peer_writer.writerow(["Exchange", ixlan[ixlan_id_key]])
            #peer_writer.writerow(["ASN", "Name", "Peering Policy", "IPv4 Prefixes", "IPv6 Prefixes", "IRR_AS-SET"])
            row = 0
            col = 0
            ixname = ixlan[ixlan_id_key]
            #print(ixname)
            tab_name = ''.join(e for e in ixname if e.isalnum())
            final_tab_name = tab_name[:25]
            #print(tab_name)
            #print(final_tab_name)
            #worksheet = workbook.add_worksheet(ixlan[ixlan_id_key])
            worksheet = workbook.add_worksheet(final_tab_name)
            for line in ixlan_obj_dict["data"]:
                #print (line["name"] + "," + line["asn"])
                #print(line["asn"])
                #f.write(line["asn"] , "," , line["name"] + "\n")
                #f.write("{0},{1}\n".format(line["asn"], line["name"]))
                #peer_writer.writerow([line["asn"], line["name"], line["policy_general"], line["info_prefixes4"], line["info_prefixes6"], line["irr_as_set"]])
                worksheet.write(row, col, line["asn"])
                worksheet.write(row, col + 1, line["name"])
                worksheet.write(row, col + 2, line["policy_general"])
                worksheet.write(row, col + 3, line["info_prefixes4"])
                worksheet.write(row, col + 4, line["info_prefixes6"])
                worksheet.write(row, col + 5, line["irr_as_set"])
                row +=1
                peerlist[line["asn"]] = line["name"], ixlan_id_key
                #print(peerlist)
        workbook.close()
        print('Peers-AS' + asn + '.xlsx has been created in the local directory.')
    except HTTPError as e:
        print(e)
        return

def configure(asn1, asn2):

    our_IX = {
    "NYIIX": ["nwk-router", "nyiix-peers", "nyiix-na-only", "ipv6-nyiix-peers", "ipv6-nyiix-na-only"],
    "LINX LON1: Main": ["lthn-router", "LINX-Peers", "LINX-Peers-for-eu-only", "ipv6-LINX-Peers", "NO REGIONAL IPV6"],
    "TorIX": ["tor1-router", "torix-peers", "torix-na-only", "ipv6-torix-peers", "ipv6-torix-na-only"],
    "JPIX TOKYO": ["jpn1-router", "jpix-peers", "jpix-asia-only", "ipv6-jpix-peers", "ipv6-jpix-asia-only"],
    "MIX-IT": ["mil1-router", "MIX-Peers", "MIX-Peers-for-eu-only", "ipv6-Mix-Peers", "NO REGIONAL IPV6"],
    "HKIX: HKIX Peering LAN": ["hkg1-router", "hkix-peers", "hkix-asia-only", "ipv6-hkix-peers", "ipv6-hkix-asia-only"],
    "INEX LAN1: INEX LAN1": ["dub2-router", "inex-peers", "inex-peers-for-eu-only", "ipv6-inex-peers", "NO REGIONAL IPV6"],
    "JPNAP Tokyo: Peering": ["jpn1-router", "jpnap-peers", "jpnap-asia-only", "ipv6-jpnap-peers", "ipv6-jpnap-asia-only"],
    "Equinix Hong Kong": ["hkg1-router", "equinix-peers", "equinix-asia-only", "ipv6-equinix-peers", "ipv6-equinix-asia-only"],
    "CoreSite - Any2 California": ["lax1-router", "any2-peers", "any2-na-only", "ipv6-any2-peers", "ipv6-any2-na-only"],
    "Equinix Singapore": ["sgp1-router", "equinix-peers", "equinix-asia-only", "NO IPV6", "NO REGIONAL IPV6"],
    "Equinix Tokyo": ["jpn1-router", "equinix-peers", "equinix-asia-only", "ipv6-equinix-peers", "ipv6-equinix-asia-only"],
    "Equinix Paris: Equinix IX - PA Metro": ["pth2-router", "equinix-peers", "equinix-peers-for-eu-only", "ipv6-equinix-peers", "NO REGIONAL IPV6"],
    "DE-CIX New York: DE-CIX New York Peering LAN": ["nwk1-router", "decix-peers", "decix-na-only", "ipv6-decix-peers", "ipv6-decix-na-only"],
    "TPIX-TW": ["twn1-router", "tpix-peers", "tpix-asia-only", "ipv6-tpix-peers", "ipv6-tpix-asia-only"],
    "Equinix Chicago": ["chi1-router", "equinix-peers", "equinix-na-only", "ipv6-equinix-peers", "ipv6-equinix-na-only"],
    "BIX.BG: Main": ["sof1-router", "bix-peers", "bix-peers-for-eu-only", "ipv6-bix-peers", "NO REGIONAL IPV6"],
    "AMS-IX": ["ams1-router", "amsix-peers", "amsix-peers-for-eu-only", "ipv6-amsix-peers", "NO REGIONAL IPV6"]
    }
    #print(our_IX["NYIIX"])

    common_ix = compare(asn1, asn2)
    neighbour_ips = get_asn_ips(asn2)
    desc, ipv4Prefixes, ipv6Prefixes = get_prefix_and_name(asn2)
    #print(neighbours)
    #print(type(neighbours))
    #print(neighbour_ips)
    ans = input("Regional or Global? (R/G): ").lower()
    with open('config', 'w') as f:
        if ans == "g":
            for common in common_ix:
                for ix in neighbour_ips:
                    #print(ix)
                    #print(type(ix))
                    if common == ix[0]:
                        ix_name, ipv4, ipv6 = ix[0], ix[1], ix[2]
                        group = our_IX[ix_name]

                        #print("ON ROUTER {}".format(group[0]))
                        #print('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"'.format(group[1], ipv4, asn2, desc))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit maximum {2}".format(group[1], ipv4, ipv4Prefixes))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown 80".format(group[1], ipv4))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown idle-timeout 60".format(group[1], ipv4))
                        #print("set protocols bgp group {0} neighbor {1} peer-as {2}".format(group[1], ipv4, asn2))

                        f.write("ON ROUTER: {}\n".format(group[0]))

                        f.write('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"\n'.format(group[1], ipv4, asn2, desc))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit maximum {2}\n".format(group[1], ipv4, ipv4Prefixes))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown 80\n".format(group[1], ipv4))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown idle-timeout 60\n".format(group[1], ipv4))
                        f.write("set protocols bgp group {0} neighbor {1} peer-as {2}\n".format(group[1], ipv4, asn2))

                        f.write('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"\n'.format(group[3], ipv6, asn2, desc))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit maximum {2}\n".format(group[3], ipv6, ipv6Prefixes))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit teardown 80\n".format(group[3], ipv6))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit teardown idle-timeout 60\n".format(group[3], ipv6))
                        f.write("set protocols bgp group {0} neighbor {1} peer-as {2}\n".format(group[3], ipv6, asn2))
            print("Config File generated in local folder")
        elif ans == 'r':
            for common in common_ix:
                for ix in neighbour_ips:
                    if common == ix[0]:
                        ix_name, ipv4, ipv6 = ix[0], ix[1], ix[2]
                        group = our_IX[ix_name]
                        
                        #print("ON ROUTER {}".format(group[0]))
                        #print('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"'.format(group[2], ipv4, asn2, desc))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit maximum {2}".format(group[2], ipv4, ipv4Prefixes))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown 80".format(group[2], ipv4))
                        #print("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown idle-timeout 60".format(group[2], ipv4))
                        #print("set protocols bgp group {0} neighbor {1} peer-as {2}".format(group[2], ipv4, asn2))

                        f.write("ON ROUTER: {}\n".format(group[0]))

                        f.write('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"\n'.format(group[2], ipv4, asn2, desc))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit maximum {2}\n".format(group[2], ipv4, ipv4Prefixes))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown 80\n".format(group[2], ipv4))
                        f.write("set protocols bgp group {0} neighbor {1} family inet any prefix-limit teardown idle-timeout 60\n".format(group[2], ipv4))
                        f.write("set protocols bgp group {0} neighbor {1} peer-as {2}\n".format(group[2], ipv4, asn2))

                        f.write('set protocols bgp group {0} neighbor {1} description "AS{2} ({3})"\n'.format(group[4], ipv6, asn2, desc))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit maximum {2}\n".format(group[4], ipv6, ipv6Prefixes))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit teardown 80\n".format(group[4], ipv6))
                        f.write("set protocols bgp group {0} neighbor {1} family inet6 any prefix-limit teardown idle-timeout 60\n".format(group[4], ipv6))
                        f.write("set protocols bgp group {0} neighbor {1} peer-as {2}\n".format(group[4], ipv6, asn2))
            print("Config File generated in local folder")
