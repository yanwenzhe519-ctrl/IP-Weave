from src.chain.reader import OnChainIPReader
reader = OnChainIPReader()

def read_ip_data(ip_name="", contract=""):
    """读取链上 IP 数据"""
    return reader.fetch(ip_name=ip_name, contract=contract)
