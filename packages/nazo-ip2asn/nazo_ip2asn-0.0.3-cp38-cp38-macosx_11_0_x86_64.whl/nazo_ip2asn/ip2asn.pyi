class Ip2Asn:
    def __init__(self, ipv4file: str, ipv6file: str) -> None:
        """初始化Ip2Asn类

        Args:
            ipv4file (str): ipv4数据库文件路径
            ipv6file (str): ipv6数据库文件路径
        """
        ...
    def lookup(self, ip: bytes) -> tuple:
        """查询IP地址的ASN信息

        Args:
            ip (bytes): 欲查询的IP地址

        Returns:
            tuple: ASN信息, 格式为(AS, ISP)
        """
        ...
