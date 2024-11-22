from web3 import AsyncWeb3
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from web3.exceptions import Web3Exception


class Client:
    private_key: str
    rpc: str
    w3: AsyncWeb3
    account: LocalAccount

    def __init__(self, private_key: str, rpc: str):
        self.private_key = private_key
        self.rpc = rpc
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
        self.account = self.w3.eth.account.from_key(private_key)

    async def send_transaction(
                self,
                to: str | ChecksumAddress,
                data: HexStr | None = None,
                from_: str | ChecksumAddress | None = None,
                increase_gas: float = 1,
                value: int | None = None,
                eip1559: bool = True,
                max_priority_fee_per_gas: int | None = None
        ) -> HexBytes | None:
            if not from_:
                from_ = self.account.address

            tx_params = {
                'chainId': await self.w3.eth.chain_id,
                'nonce': await self.w3.eth.get_transaction_count(self.account.address),
                'from': AsyncWeb3.to_checksum_address(from_),
                'to': AsyncWeb3.to_checksum_address(to),
            }

            if eip1559:
                if max_priority_fee_per_gas is None:
                    max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
                base_fee = (await self.w3.eth.get_block('latest'))['baseFeePerGas']
                max_fee_per_gas = base_fee + max_priority_fee_per_gas
                tx_params['maxFeePerGas'] = max_fee_per_gas  
                tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas  
            else:
                tx_params['gasPrice'] = await self.w3.eth.gas_price

            if data:
                tx_params['data'] = data
            if value:
                tx_params['value'] = value

            gas = await self.w3.eth.estimate_gas(tx_params)
            tx_params['gas'] = int(gas * increase_gas)

            sign = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
            return await self.w3.eth.send_raw_transaction(sign.rawTransaction)
    

    async def verif_tx(self, tx_hash: HexBytes, timeout: int = 200) -> str:
        data = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        if data.get('status') == 1:
            return tx_hash.hex()
        raise Web3Exception(f'transaction failed {data["transactionHash"].hex()}')
