import logging
from copy import deepcopy
from functools import partial

from eth_abi.exceptions import DecodingError, InsufficientDataBytes
from eth_utils import function_abi_to_4byte_selector, decode_hex
from web3._utils.abi import get_abi_input_names, get_abi_input_types, map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.auto import w3

from tellor.constants import TELLOR_ABI

logger = logging.getLogger(__name__)


def get_func_decoders(contract):
    def decode_func_wrapper(data):
        func, args = contract.decode_function_input(data)
        return func.fn_name, args

    decoders = {
        function_abi_to_4byte_selector(abi): partial(decode_func_wrapper)
        for abi in TELLOR_ABI if abi['type'] == 'function'
    }
    # fix for byte nonce in function input
    nonce_string_abi = next(x for x in TELLOR_ABI if x.get('name') == 'submitMiningSolution')
    nonce_string_sig = function_abi_to_4byte_selector(nonce_string_abi)
    nonce_bytes_abi = deepcopy(nonce_string_abi)
    nonce_bytes_abi['inputs'][0]['type'] = 'bytes'
    decoders[nonce_string_sig] = partial(decode_func_with_fallback, [nonce_string_abi, nonce_bytes_abi])
    return decoders


def decode_func_with_fallback(abis_to_try, data):
    for abi in abis_to_try:
        try:
            selector, params = data[:4], data[4:]
            names = get_abi_input_names(abi)
            types = get_abi_input_types(abi)
            decoded = w3.codec.decode_abi(types, params)
            normalized = map_abi_data(BASE_RETURN_NORMALIZERS, types, decoded)
            return abi['name'], dict(zip(names, normalized))
        except DecodingError:
            logger.debug('trying fallback fn input decoder')
    raise DecodingError('could not decode fn input')


def decode_fn_input(data, decoders):
    if isinstance(data, str):
        data = decode_hex(data)
    try:
        if data[:4] in decoders:
            return decoders.get(data[:4])(data)
        else:
            logger.error(f'no function input decoder for {data[:4].hex()}')
    except (ValueError, InsufficientDataBytes, DecodingError) as e:
        logger.error('could not decode fn args')
        logger.error(e)
    return '', {}
