# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lightecho_stellar_oracle']
install_requires = \
['stellar-sdk==9.0.0b0']

setup_kwargs = {
    'name': 'lightecho-stellar-oracle',
    'version': '0.6.0',
    'description': 'Python SDK for the Lightecho Stellar Oracle',
    'long_description': '**Python SDK for the Lightecho Stellar Oracle**\n\n```\npip install lightecho_stellar_oracle\n```\n\nExample:\n```\nfrom lightecho_stellar_oracle import OracleClient, TESTNET_CONTRACT_XLM\nfrom stellar_sdk.keypair import Keypair\n\noracle_client = OracleClient(\n    contract_id=TESTNET_CONTRACT_XLM,\n    signer=Keypair.from_secret("SAES4O3NXUE2CPIB7YH3O5ROAONADPZRXOEYFC4JPLNY6STOBM2RYLGH"),\n    network="testnet",\n)\n# list the assets\nprint(oracle_client.assets())\n\n# show the base Currency\nprint(oracle_client.base())\n\n# get the last price\ntx_id, result = oracle_client.lastprice("other", "USD")\nprint(tx_id)\nprint(result)\n\n# Printing the updated result\nprint(result)\n\n#RESULT\n#{\'price\': 0.11, \'timestamp\': 1698240296}\n```\n\nFor more information see [https://github.com/bp-ventures/lightecho-stellar-oracle](https://github.com/bp-ventures/lightecho-stellar-oracle).\n',
    'author': 'BP Ventures',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bp-ventures/lightecho-stellar-oracle/tree/trunk/oracle-sdk/python',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
