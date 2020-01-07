import pytest
from hexbytes import HexBytes
from web3.datastructures import AttributeDict

from tellor.auto import tellor

receipt_good = [
    AttributeDict(
        {
            "address": "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5",
            "topics": [
                HexBytes("0xe6d63a2aee0aaed2ab49702313ce54114f2145af219d7db30d6624af9e6dffc4"),
                HexBytes("0x000000000000000000000000913a158846d0c5d972a3a78720a1c388d4d748e2"),
                HexBytes("0x0000000000000000000000000000000000000000000000000000000000000001"),
            ],
            "data": "0x0000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000002bcbeee9303678d75b2ac5f2e0b75624dadefa43c647d760c91a05b7151839bafdb31000000000000000000000000000000000000000000000000000000000000002535383038313431333937393838383130393136323536303434333135363434353036303535000000000000000000000000000000000000000000000000000000",
            "blockNumber": 8655809,
            "transactionHash": HexBytes("0x7e6567ecb0a696be6dc25fd80b8c8928a83c480f539e5207ab78ed6216b6d6a0"),
            "transactionIndex": 36,
            "blockHash": HexBytes("0x51ae1b4e34c24825488c19cc1ee47a3dae07a1ba07923e4479bac86b91ac6006"),
            "logIndex": 26,
            "removed": False,
        }
    )
]

receipt_bad = [
    AttributeDict(
        {
            "address": "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5",
            "topics": [
                HexBytes("0xe6d63a2aee0aaed2ab49702313ce54114f2145af219d7db30d6624af9e6dffc4"),
                HexBytes("0x0000000000000000000000005f10929536565c74eba8f3ca13cd5bbc0c385954"),
                HexBytes("0x0000000000000000000000000000000000000000000000000000000000000001"),
            ],
            "data": "0x0000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000002baac40bc60ab6023465efe775e2750a7a4f57a3003cfa2179672ac74515f3b694a8e000000000000000000000000000000000000000000000000000000000000000a123cbc62dc000000000000000000000000000000000000000000000000000000",
            "blockNumber": 8653055,
            "transactionHash": HexBytes("0x168ed1b9c67b827553010c2899fd8dd40e1bb8c6ec322f231bee41ae01f0d48c"),
            "transactionIndex": 54,
            "blockHash": HexBytes("0x20c7000fb330b9d9345035e8074a6e2dbe2d3002f9903e2329b05be970d53fa4"),
            "logIndex": 38,
            "removed": False,
        }
    )
]

events_good = [
    AttributeDict(
        {
            "args": AttributeDict(
                {
                    "_miner": "0x913a158846D0C5d972A3a78720a1c388d4d748E2",
                    "_requestId": 1,
                    "_nonce": "5808141397988810916256044315644506055",
                    "_value": 179390,
                    "_currentChallenge": b"\xee\x93\x03g\x8du\xb2\xac_.\x0bubM\xad\xef\xa4<d}v\x0c\x91\xa0[qQ\x83\x9b\xaf\xdb1",
                }
            ),
            "event": "NonceSubmitted",
            "logIndex": 26,
            "transactionIndex": 36,
            "transactionHash": HexBytes("0x7e6567ecb0a696be6dc25fd80b8c8928a83c480f539e5207ab78ed6216b6d6a0"),
            "address": "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5",
            "blockHash": HexBytes("0x51ae1b4e34c24825488c19cc1ee47a3dae07a1ba07923e4479bac86b91ac6006"),
            "blockNumber": 8655809,
        }
    )
]
events_bad = [
    AttributeDict(
        {
            "args": AttributeDict(
                {
                    "_miner": "0x5F10929536565C74eba8f3CA13cD5BBC0c385954",
                    "_requestId": 1,
                    "_nonce": b"\x12<\xbcb\xdc\x00\x00\x00\x00\x00",
                    "_value": 178860,
                    "_currentChallenge": b"@\xbc`\xab`#F^\xfew^'P\xa7\xa4\xf5z0\x03\xcf\xa2\x17\x96r\xactQ_;iJ\x8e",
                }
            ),
            "event": "NonceSubmitted",
            "logIndex": 38,
            "transactionIndex": 54,
            "transactionHash": HexBytes("0x168ed1b9c67b827553010c2899fd8dd40e1bb8c6ec322f231bee41ae01f0d48c"),
            "address": "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5",
            "blockHash": HexBytes("0x20c7000fb330b9d9345035e8074a6e2dbe2d3002f9903e2329b05be970d53fa4"),
            "blockNumber": 8653055,
        }
    )
]


@pytest.mark.parametrize("logs,events", [(receipt_good, events_good), (receipt_bad, events_bad)])
def test_decode_logs(logs, events):
    assert tellor.decode_logs(logs) == events


fn_good = HexBytes(
    "0x68c180d500000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000002bcbe000000000000000000000000000000000000000000000000000000000000002535383038313431333937393838383130393136323536303434333135363434353036303535000000000000000000000000000000000000000000000000000000"
)
fn_bad = HexBytes(
    "0x68c180d500000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000002bc96000000000000000000000000000000000000000000000000000000000000000a123eb44e1e000000000000000000000000000000000000000000000000000000"
)
fn_tip = HexBytes(
    "0x752d49a100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000"
)

fn_good_decoded = (
    "submitMiningSolution",
    {"_nonce": "5808141397988810916256044315644506055", "_requestId": 1, "_value": 179390},
)
fn_bad_decoded = (
    "submitMiningSolution",
    {"_nonce": b"\x12>\xb4N\x1e\x00\x00\x00\x00\x00", "_requestId": 1, "_value": 179350},
)
fn_tip_decoded = (
    "addTip",
    {"_tip": 0, "_requestId": 1},
)


@pytest.mark.parametrize("data,decoded", [
    (fn_good, fn_good_decoded),
    (fn_bad, fn_bad_decoded),
    (fn_tip, fn_tip_decoded),
])
def test_decode_func(data, decoded):
    assert tellor.decode_func(data) == decoded
