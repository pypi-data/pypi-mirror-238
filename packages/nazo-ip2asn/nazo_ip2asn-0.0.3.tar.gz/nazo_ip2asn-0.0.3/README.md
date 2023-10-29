# ip2asn

a [iptoasn](https://iptoasn.com/) tools

Please download the latest version and unzip：
[ip2asn-v4.tsv](https://iptoasn.com/data/ip2asn-v4.tsv.gz) && [ip2asn-v6.tsv](https://iptoasn.com/data/ip2asn-v6.tsv.gz)

## Quickstart

```python

from nazo_ip2asn import Ip2Asn

ip2asn = Ip2Asn(ipv4file="ip2asn-v4.tsv", ipv6file="ip2asn-v6.tsv")

print(ip2asn.lookup(b"8.8.8.8"))

```