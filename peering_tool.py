import argparse
from peering_functions import compare, configure, list_IX
from prettytable import PrettyTable
import argparse
from peering_calls import get_asn_ips

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="PeeringDB Checking Application.")
    parser.add_argument("--list", nargs='+', type=str, help="List PeeringDB IXs for AS Number, takes AS Number as argument.")
    parser.add_argument("--compare", nargs='+', type=str, help="Get common IXs for our ASN, takes 1 AS Number as arguments.")
    parser.add_argument("--get_as_per_ix", type=str, help="Get a list of AS,s per IX, takes the IX name as argument.")
    parser.add_argument("--configure", nargs='+', type=str, help="Takes AS as argument 1 and optional md5 key as argument 1.")


    args = parser.parse_args()
    if args.list:
        if len(args.list) != 1:
            print("ERROR: Takes exactly 1 argument.")
        else:
            list_IX(args.list[0])
    if args.compare:
        if len(args.compare) != 1:
            print("ERROR: Takes exactly 1 argument")
        else:
            #print(len(args.compare))
            cEight_As = "14537"
            shared_ix = compare(cEight_As, args.compare[0])
            print()
            print("*" * 20 + " IX WHERE BOTH AS ARE PRESENT " + "*" * 20 + "\n")
            print(*shared_ix, sep="\n")
            print()
            ip_details = get_asn_ips(args.compare[0])
            #print(ip_details)
            #print(type(ip_details))
            #print(shared_ix)
            x = PrettyTable()
            x.field_names = ["Exchange", "Peer IPv4", "Peer IPv6"]
            for common in shared_ix:
                for ix in ip_details:
                    if common == ix[0]:
                        exchange, peer_ipv4, peer_ipv6 = ix[0], ix[1], ix[2]
                        x.add_row([exchange, peer_ipv4, peer_ipv6])
                        #print(*ix)
            print(x)

    if args.configure:
        if len(args.configure) != 1:
            print("ERROR: Takes exactly 1 argument")
        else:
            cEight_As = "14537"
            configure(cEight_As, args.configure[0])