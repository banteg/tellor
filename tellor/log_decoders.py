import logging
from copy import deepcopy
from functools import partial

from eth_abi.exceptions import DecodingError
from eth_utils import event_abi_to_log_topic
from web3._utils.events import get_event_data
from web3.auto import w3

from tellor.constants import TELLOR_ABI

logger = logging.getLogger(__name__)


def get_log_decoders():
    decoders = {
        event_abi_to_log_topic(abi): partial(get_event_data, w3.codec, abi)
        for abi in TELLOR_ABI if abi['type'] == 'event'
    }
    # fix for byte nonce in events
    nonce_string_abi = next(x for x in TELLOR_ABI if x.get('name') == 'NonceSubmitted')
    nonce_string_topic = event_abi_to_log_topic(nonce_string_abi)
    nonce_bytes_abi = deepcopy(nonce_string_abi)
    nonce_bytes_abi['inputs'][1]['type'] = 'bytes'
    decoders[nonce_string_topic] = partial(decode_log_with_fallback, [nonce_string_abi, nonce_bytes_abi])
    return decoders


def decode_log_with_fallback(abis_to_try, log):
    for abi in abis_to_try:
        try:
            log_with_replaced_topic = deepcopy(log)
            log_with_replaced_topic['topics'][0] = event_abi_to_log_topic(abi)
            return get_event_data(w3.codec, abi, log_with_replaced_topic)
        except DecodingError:
            logger.debug('trying fallback log decoder')
    raise DecodingError('could not decode log')


def decode_logs(logs, decoders):
    result = []
    for log in logs:
        topic = log['topics'][0]
        if topic in decoders:
            try:
                decoded = decoders[topic](log)
                result.append(decoded)
            except DecodingError as e:
                logger.error('could not decode log')
                logger.error(log)
                logger.error(e)
    return result
