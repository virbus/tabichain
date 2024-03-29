from data.config import FAUCET_MIN_BALANCE, MIN_TRANSFER_COUNT


def main_menu():
    print(f"[1] Claim TABI faucet")
    print(f"[2] Transfer TABI for random wallets")
    print(f"[3] Exit")


def choose_faucet_menu():
    print(f"Choose activity for faucet:")
    print(f"[1] Claim TABI for all wallets")
    print(f"[2] Claim TABI for wallets with balance <= {FAUCET_MIN_BALANCE} TABI")
    print(f"[3] Back to main menu")


def choose_transfer_menu():
    print(f"Choose activity for transfer:")
    print(f"[1] Transfer TABI for all wallets")
    print(f"[2] Transfer TABI for wallets with transfer < {MIN_TRANSFER_COUNT} times")
    print(f"[3] Back to main menu")
