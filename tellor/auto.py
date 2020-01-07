# override with env WEB3_HTTP_PROVIDER_URI
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from tellor.constants import Network
from tellor.contract import Tellor

network = Network(int(w3.eth.chainId))
tellor = Tellor(network)

if network == Network.RINKEBY:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
