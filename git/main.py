from web3 import AsyncWeb3
import asyncio
from client import Client
from web3.contract.async_contract import AsyncContract


TokenABI = [
    {
        'constant': True,
        'inputs': [],
        'name': 'name',
        'outputs': [{'name': '', 'type': 'string'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'symbol',
        'outputs': [{'name': '', 'type': 'string'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        "inputs": [],
        "name": "mint",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'totalSupply',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'decimals',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': 'who', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
        'name': 'allowance',
        'outputs': [{'name': 'remaining', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
        'name': 'approve',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
        'name': 'transfer',
        'outputs': [], 'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }
]

# async def main():

#     token_address = AsyncWeb3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955')
#     spender = AsyncWeb3.to_checksum_address('0x000000000022D473030F116dDEE9F6B43aC78BA3')

#     client = Client(
#         private_key='',
#         rpc='https://1rpc.io/bnb'
#     )


#     contract = client.w3.eth.contract(
#         address=token_address,
#         abi=TokenABI
#     )

#     decimals = await contract.functions.decimals().call()
#     token_balance = await contract.functions.balanceOf(client.account.address).call()
#     approved_amount = await contract.functions.allowance(client.account.address, spender).call()

#     print('decimals:', decimals)
#     print('token_balance:', token_balance / 10 ** decimals)
#     print('approved_amount:', approved_amount / 10 ** decimals)

#     if approved_amount < token_balance:
#         tx_hash = await client.send_transaction(
#             to=token_address,
#             data=contract.encodeABI('approve',
#                                     args=(
#                                         spender,
#                                         token_balance
#                                     ))
#         )
#         if tx_hash:
#             try:
#                 await client.verif_tx(tx_hash=tx_hash)
#                 print(f'Transaction success!! tx_hash: {tx_hash.hex()}')
#             except Exception as err:
#                 print(f'Transaction error!! tx_hash: {tx_hash.hex()}; error: {err}')
#         else:
#             print(f'Transaction error!!')
#     else:
#         print('Already approved')


    
async def mint():

    address_contract = AsyncWeb3.to_checksum_address('0x26E9934024cdC7fcc9f390973d4D9ac1FA954a37')

    client = Client(
        private_key='',
        rpc='https://arbitrum.llamarpc.com'
    )

    contract: AsyncContract = client.w3.eth.contract(
        address= address_contract,
        abi= TokenABI
    )
    mint_price = await contract.functions.fee().call()
    
    tx_hash_bytes = await client.send_transaction(
        to=address_contract,
        data=contract.encode_abi(
            name='mint',
            args=(),
        ),
        value=mint_price
    )

    return await client.verif_tx(tx_hash_bytes)



if __name__ == '__main__':
    asyncio.run(mint())
