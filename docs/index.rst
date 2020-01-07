Tellor Python Tools
==================================

A collection of Python tools to interact with Tellor_ decentralized oracle.

Quickstart
----------

If you are running a local node, you can simply use :py:mod:`tellor.auto` to get a wrapper instance configured for the network your node is on. Both mainnet and rinkeby are supported.

.. code-block:: python

    from tellor.auto import tellor

If your node uses a non-standard configuration or you use Infura, update the ``WEB3_HTTP_PROVIDER_URI`` environment variable.

.. code-block:: python

    >>> tellor.network
    <Network.MAINNET: 1>
    >>> tellor.address
    '0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5'

    # Wei values transform to a readable form when printed
    >>> tellor.total_supply
    520910000000000000000000
    >>> print(tellor.total_supply)
    520910 trb

    # Disputes and oracle values are fully supported
    >>> print(tellor.get_dispute(tellor.dispute_count))
    dispute_id = 19
    executed = False
    dispute_vote_passed = False
    is_prop_fork = False
    reported_miner = 0x103348C47fFc3254aFf761894e7C13cA0C680465
    reporting_party = 0xbABca74dB0D4dBCb7EBC89728452CeAC807615A0
    tally = 80352.476817699999998 trb
    request_id = 3
    timestamp = 1572377640
    value = 187880
    min_execution_date = 1572985087
    number_of_votes = 2
    block_number = 8836057
    miner_slot = 4
    quorum = 80352.476817699999998 trb
    fee = 510 trb
    can be executed in 2d19h16m in favor of reporter

    >>> print(tellor.get_value(3, 1572377640))
    request_id = 3
    timestamp = 1572377640
    0 0x5522eCa38e7C376F96d29F963ae9eEAE14F27a47 20739
    1 0xF1989cc4492Fe704f846c70Ff068fa554C904901 20739
    2 0xe060aE2E078ffd811D9fc7d613976d6EFe7f071F 20739
    3 0xFcEB7885efAEa565262e0e87CbDC1DCC8E0cCB4D 20739
    4 0x103348C47fFc3254aFf761894e7C13cA0C680465 187880



.. toctree::
   :maxdepth: 4

   tellor


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Tellor: https://tellor.io/
