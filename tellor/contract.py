from eth_abi.packed import encode_abi_packed
from typing import List, Optional, Tuple
from web3.auto import w3
from tellor.constants import Network, TELLOR_GENESIS, TELLOR_ABI, TELLOR_ADDRESS
from tellor.dispute import Dispute, Value
from tellor import func_decoders, log_decoders
from tellor.types import Tributes, CurrentVariables, StakerStatus


class Tellor:
    """
    Tellor contract wrapper which implements most of the useful getters.

    Note:
        You can also access to the underlying web3 contract interface as a fallback.
    """

    def __init__(self, network: Network):
        self.network = network
        self.genesis = TELLOR_GENESIS[network]
        self.address = TELLOR_ADDRESS[network]
        self.contract = w3.eth.contract(self.address, abi=TELLOR_ABI)
        self.call = self.contract.caller()
        self.func_decoders = func_decoders.get_func_decoders(self.contract)
        self.logs_decoders = log_decoders.get_log_decoders()

    def __getattr__(self, item):
        return getattr(self.contract, item)

    def decode_func(self, data) -> Tuple[str, dict]:
        """
        Decodes transaction input data.

        Returns:
            Function name and arguments.
        """
        return func_decoders.decode_fn_input(data, self.func_decoders)

    def decode_logs(self, logs) -> List[dict]:
        """
        Decodes logs with ``topics`` and ``data`` to events.

        Returns:
            Events containing ``event`` and ``args``.
        """
        return log_decoders.decode_logs(logs, self.logs_decoders)

    def get_logs(self, **kwds) -> List[dict]:
        """
        Get contract events by querying logs.

        Args:
            **kwds: Additional args to ``w3.eth.getLogs``

        Returns:
            Decoded events from matching logs.
        """
        logs = w3.eth.getLogs({'address': self.address, **kwds})
        return self.decode_logs(logs)

    def did_mine(self, challenge, miner) -> bool:
        """
        Returns:
            Whether a miner has mined a certain challenge already.
        """
        return self.call.didMine(challenge, miner)

    def did_vote(self, dispute_id, address) -> bool:
        """
        Returns:
            Return whether an address has cast a vote in a dispute.

        Tip:
            To get an actual vote power, use :py:meth:`balance_of_at` with ``block_number`` of the dispute.
            To figure out whether the vote was for or against, well, you have to resort to events.
        """
        return self.call.didVote(dispute_id, address)

    @property
    def owner(self) -> str:
        """
        Address which is the beneficiary of the 10% devshare.
        """
        return self._address_var('_owner')

    @property
    def deity(self) -> str:
        """
        Address which controls the backdoor to change the implementation without the governance process.
        """
        return self._address_var('_deity')

    @property
    def implementation(self) -> str:
        """
        Address of the current contract implementation where all calls are delegated to.
        """
        return self._address_var('tellorContract')

    def get_dispute(self, dispute_id) -> Optional[Dispute]:
        """
        Returns:
            Detailed info about a :py:class:`~tellor.dispute.Dispute`.
        """
        data = self.call.getAllDisputeVars(dispute_id)
        data.extend(data.pop(7))  # append disputeUintVars
        dispute = Dispute(dispute_id, *data)
        if any(dispute.hash):
            return dispute

    def get_dispute_by(self, miner, request_id, timestamp) -> Optional[Dispute]:
        """
        Args:
            miner: Disputed miner address
            request_id: Disputed request id
            timestamp: Disputed value timestamp

        Returns:
            Detailed info about a :py:class:`~tellor.dispute.Dispute`.
        """
        dispute_hash = w3.keccak(encode_abi_packed(["address", "uint256", "uint256"], [miner, request_id, timestamp]))
        dispute_id = self.call.getDisputeIdByDisputeHash(dispute_hash)
        if dispute_id:
            return self.get_dispute(dispute_id)

    def get_value(self, request_id, timestamp) -> Optional[Value]:
        """

        Args:
            request_id: value request id
            timestamp: value timestamp

        Returns:
            Detailed info about a :py:class:`~tellor.dispute.Value` with miners and the values they submitted.
        """
        miners = self.call.getMinersByRequestIdAndTimestamp(request_id, timestamp)
        values = self.call.getSubmissionsByTimestamp(request_id, timestamp)
        if any(values):
            return Value(request_id, timestamp, miners, values)

    def balance_of(self, address) -> Tributes:
        """
        Returns:
            Tribute balance of address in wei.
        """
        return Tributes(self.call.balanceOf(address))

    def balance_of_at(self, address, block_number) -> Tributes:
        """
        Returns:
            Tribute balance snapshot of address in wei.
        """
        return Tributes(self.call.balanceOfAt(address, block_number))

    def allowance(self, address, spender) -> Tributes:
        """
        Returns:
            How many tributes spender is allowed to spend on behalf of address.
        """
        return Tributes(self.call.allowance(address, spender))

    @property
    def current_variables(self) -> CurrentVariables:
        """
        Current contract state from miner's perspective
        :py:class:`~tellor.types.CurrentVariables`
        """
        return CurrentVariables(*self.call.getCurrentVariables())

    def staker_status(self, address) -> StakerStatus:
        """
        Returns:
            :py:class:`~tellor.types.StakerStatus`
        """
        return StakerStatus(self.call.getStakerInfo(address)[0])

    @property
    def total_supply(self) -> Tributes:
        """
        Total supply of tributes. New tributes are printed every block.
        """
        return Tributes(self.call.totalSupply())

    @property
    def dispute_fee(self) -> Tributes:
        """
        Deposit a reporter must put to open a dispute.
        If they lose the case, this deposit is forfeited and is given to the miner.
        """
        return Tributes(self._uint_var('disputeFee'))

    @property
    def dispute_count(self) -> int:
        """
        The ever-increasing number of disputes across the network.
        """
        return self._uint_var('disputeCount')

    @property
    def staker_count(self) -> int:
        """
        Current number of active stakers.
        """
        return self._uint_var('stakerCount')

    @property
    def difficulty(self) -> int:
        """
        Current network difficulty.
        The difficulty is automatically adjusted for a target of 10-minute block time.
        """
        return self._uint_var('difficulty')

    @property
    def slot_progress(self) -> int:
        """
        Number of already mined slots in the current blocks. This value can be 0–4.
        """
        return self._uint_var('slotProgress')

    def _address_var(self, name):
        return self.call.getAddressVars(w3.keccak(text=name))

    def _uint_var(self, name):
        return self.call.getUintVar(w3.keccak(text=name))
