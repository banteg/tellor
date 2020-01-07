from dataclasses import dataclass, field
from typing import List

from tellor.types import Tributes


@dataclass
class Value:
    request_id: int
    timestamp: int
    miners: List[str] = None
    values: List[int] = None


@dataclass
class Dispute:
    """
    Detailed info about a dispute.

    Attributes:
        dispute_id: Dispute id.
        hash: Dispute hash, i.e. ``keccak256(miner+request_id+timestamp)``.
        executed: Whether the dispute has been finalized with ``tallyVotes``.
        dispute_vote_passed: Whether the dispute ended in favour of reporter.
        is_prop_fork: Whether the fork to another implementation contract is proposed.
        reported_miner: The miner who is disputed.
        reporting_party: The reporter who opened the dispute.
        proposed_fork_address: Address of proposed implementation contract.
        tally: Difference of votes for and against.
        request_id: Request id of the disputed value.
        timestamp: Timestamp of the disputed value.
        value: Disputed value submitted by the miner.
        min_execution_date: When the votes can be tallied. Disputes last for exactly 7 days.
        number_of_votes: Number of voters.
        block_number: Block number when the reported value was submitted. Voting power comes from balance snapshot at this block.
        miner_slot: Miner slot where the disputed value is located. Use :py:class:`Value` to see adjacent values.
        quorum: Sum of votes for and against.
        fee: Reporter deposit. They get it back if they win the dispute or lose it to the disputed miner otherwise.
    """

    dispute_id: int
    hash: bytes = field(repr=False)
    executed: bool
    dispute_vote_passed: bool
    is_prop_fork: bool
    reported_miner: str
    reporting_party: str
    proposed_fork_address: str
    tally: Tributes
    request_id: int
    timestamp: int
    value: int
    min_execution_date: int
    number_of_votes: int
    block_number: int
    miner_slot: int
    quorum: Tributes
    fee: Tributes

    def __post_init__(self):
        self.tally = Tributes(self.tally)
        self.quorum = Tributes(self.quorum)
        self.fee = Tributes(self.fee)

    @property
    def yays(self):
        return Tributes((self.quorum + self.tally) // 2)

    @property
    def nays(self):
        return Tributes(self.quorum - self.yays)
