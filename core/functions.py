import time
import random
import requests
from web3 import Web3
from core.logger import logger
from requests.sessions import Session
from fake_useragent import UserAgent
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider
from data.config import RPC, TRANSFER_AMOUNT, SLEEP, EXPLORER


def extract_ip_from_proxy(proxy):
    if proxy.startswith("http://"):
        proxy = proxy[7:]
    elif proxy.startswith("https://"):
        proxy = proxy[8:]
    at_split = proxy.split("@")[-1]
    ip = at_split.split(":")[0]
    return ip


def create_session(proxy=None, check_proxy=False):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": UserAgent().random,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://faucet.testnet.tabichain.com",
            "Connection": "keep-alive",
            "Referer": "https://faucet.testnet.tabichain.com/",
        }
    )
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    if check_proxy and proxy:
        try:
            proxy_ip = extract_ip_from_proxy(proxy)
            actual_ip = session.get("https://api.ipify.org").text
            if actual_ip != proxy_ip:
                raise Exception(
                    f"Error: Proxy IP ({proxy_ip}) does not match actual IP ({actual_ip}). Stopping script."
                )
            else:
                print(f"Proxy check passed: {actual_ip}")
        except requests.RequestException as e:
            raise Exception(f"Error during proxy check: {e}")
    return session


def create_web3_with_proxy(rpc_endpoint, proxy=None):
    if proxy is None:
        return Web3(Web3.HTTPProvider(rpc_endpoint))
    proxy_settings = {
        "http": proxy,
        "https": proxy,
    }
    session = Session()
    session.proxies = proxy_settings
    custom_provider = HTTPProvider(rpc_endpoint, session=session)
    web3 = Web3(custom_provider)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3


def estimate_gas_and_send(name, web3, tx, private_key, tx_name):
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    logger.info(f"{name} | Waiting {tx_name} {round(web3.from_wei(tx['value'], 'ether'), 6)} TABI to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        logger.error(f"{name} | Transaction {transaction_hash} failed!")
        time.sleep(SLEEP)
        return False
    logger.success(f"{name} | {tx_name} hash: {EXPLORER}/{transaction_hash}")
    time.sleep(SLEEP)
    return True


def create_transaction(name, web3, private_key, tx_name, to, value, data):
    account = web3.eth.account.from_key(private_key)
    tx = {
        "from": account.address,
        "to": web3.to_checksum_address(to),
        "value": value,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": 9789,
        "data": data,
    }
    result = estimate_gas_and_send(name, web3, tx, private_key, tx_name)
    return result


def claim_faucet(name, private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy=proxy, check_proxy=False)
    response = session.post(
        "https://faucet-api.testnet.tabichain.com/api/faucet",
        json={
            "address": account.address,
        },
    )
    if response.status_code == 200:
        response = response.json()
        logger.success(f"{name} | {response['message']} | tx: {EXPLORER}/{response['hash']}")
        time.sleep(SLEEP)
        return response
    else:
        logger.error(f"{name} | Error status code: {response.status_code}")
        time.sleep(SLEEP)


def faucet(name: str, private_key: str, amount=0, proxy=None):
    if amount == 0:
        return claim_faucet(name, private_key, proxy)
    else:
        web3 = create_web3_with_proxy(RPC, proxy)
        account = web3.eth.account.from_key(private_key)
        balance = web3.eth.get_balance(account.address)
        human_balance = round(web3.from_wei(balance, 'ether'), 6)
        logger.warning(f"{name} | Balance {human_balance} TABI")
        if human_balance <= amount:
            return claim_faucet(name, private_key, proxy)


def transfer(name: str, private_key: str, private_key_to: str, proxy=None) -> bool:
    web3 = create_web3_with_proxy(RPC, proxy)
    send_value = random.uniform(*TRANSFER_AMOUNT)
    result = create_transaction(
        name=name,
        web3=web3,
        private_key=private_key,
        tx_name="Transfer",
        to=web3.eth.account.from_key(private_key_to).address,
        value=web3.to_wei(send_value, "ether"),
        data="0x",
    )
    return result
