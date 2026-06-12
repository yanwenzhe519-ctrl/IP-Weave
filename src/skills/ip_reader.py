
from src.chain.reader import OnChainIPReader
reader = OnChainIPReader()

def read_ip(ip_name=""):
    return {"chain_data": reader.fetch(ip_name=ip_name)}
