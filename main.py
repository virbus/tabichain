from core.file import load_file, save_file
from core.menu import *
from data.config import DATA_FILE, DATA_SHEET, FAUCET_MIN_BALANCE, MIN_TRANSFER_COUNT, SHUFFLE
from core.functions import *
def main():
    while True:
        accounts = load_file(debug=False, file=DATA_FILE, sheet=DATA_SHEET)
        if SHUFFLE:
            accounts = accounts.sample(frac=1)
        main_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            while True:
                choose_faucet_menu()
                faucet_choice = input("Enter activity choice for faucet: ")
                if faucet_choice == "1":
                    start_time = time.time()
                    for i, row in accounts.iterrows():
                        if isinstance(row['Faucet'], int) is False:
                            row['Faucet'] = 0
                        try:
                            result = faucet(row['Name'], row['Private'], 0, row['Proxy'])
                            if result:
                                accounts.loc[i, 'Faucet'] = row['Faucet'] + 1
                        except Exception as e:
                            logger.error(f"{row['Name']} | Error in function: {e}")
                    save_file(accounts, 1, 2, DATA_FILE, DATA_SHEET)
                    end_time = time.time()
                    logger.success(f"Script execution time: {round(end_time - start_time, 2)} seconds")
                elif faucet_choice == "2":
                    start_time = time.time()
                    for i, row in accounts.iterrows():
                        if isinstance(row['Faucet'], int) is False:
                            row['Faucet'] = 0
                        try:
                            result = faucet(row['Name'], row['Private'], FAUCET_MIN_BALANCE, row['Proxy'])
                            if result:
                                accounts.loc[i, 'Faucet'] = row['Faucet'] + 1
                        except Exception as e:
                            logger.error(f"{row['Name']} | Error in function: {e}")
                    save_file(accounts, 1, 2, DATA_FILE, DATA_SHEET)
                    end_time = time.time()
                    logger.success(f"Script execution time: {round(end_time - start_time, 2)} seconds")
                elif faucet_choice == "3":
                    break
        elif choice == "2":
            while True:
                choose_transfer_menu()
                transfer_choice = input("Enter activity choice for transfer: ")
                if transfer_choice == "1":
                    start_time = time.time()
                    for i, row in accounts.iterrows():
                        if isinstance(row['Send'], int) is False:
                            row['Send'] = 0
                        try:
                            send_to = accounts.sample(n=1)
                            send_to_private = send_to['Private'].values[0]
                            result = transfer(row['Name'], row['Private'], send_to_private, row['Proxy'])
                            if result:
                                accounts.loc[i, 'Send'] = row['Send'] + 1
                        except Exception as e:
                            logger.error(f"{row['Name']} | Error in function: {e}")
                    save_file(accounts, 1, 2, DATA_FILE, DATA_SHEET)
                    end_time = time.time()
                    logger.success(f"Script execution time: {round(end_time - start_time, 2)} seconds")
                elif transfer_choice == "2":
                    start_time = time.time()
                    for i, row in accounts.iterrows():
                        if isinstance(row['Send'], int) is False:
                            row['Send'] = 0
                        if row['Send'] < MIN_TRANSFER_COUNT:
                            try:
                                send_to = accounts.sample(n=1)
                                send_to_private = send_to['Private'].values[0]
                                result = transfer(row['Name'], row['Private'], send_to_private, row['Proxy'])
                                if result:
                                    accounts.loc[i, 'Send'] = row['Send'] + 1
                            except Exception as e:
                                logger.error(f"{row['Name']} | Error in function: {e}")
                    save_file(accounts, 1, 2, DATA_FILE, DATA_SHEET)
                    end_time = time.time()
                    logger.success(f"Script execution time: {round(end_time - start_time, 2)} seconds")
                elif transfer_choice == "3":
                    break
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
