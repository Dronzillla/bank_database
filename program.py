import sys
from populate import generate_new_banks, generate_new_persons, generate_new_accounts
from populate import NoPersonsError, NoBanksError
from db_operations import show_banks, show_persons, show_accounts
from db_operations import (
    personal_code_exists,
    greet_person,
    show_personal_accounts,
    select_account,
    deposit,
    withdraw,
)


class Program:
    def __init__(self):
        self.running = False

    # Main program loop
    def start(self):
        self.running = True
        while self.running:
            # Show main menu
            main_menu_choice = self.show_main_menu()
            # A menu for central bank operations
            if main_menu_choice == "1. Central bank operations":
                self.handle_central_bank_operations()
            # A menu for personal bank operations
            elif main_menu_choice == "2. Personal bank operations":
                self.handle_personal_bank_operations()
            # Exit from program
            elif main_menu_choice == "3. Exit from program":
                self.stop()

    def handle_central_bank_operations(self) -> None:
        while True:
            sub_menu_choice = self.show_central_bank_menu()

            if sub_menu_choice == "1. Populate database with new data":
                while True:
                    sub_sub_menu_choice = self.show_central_bank_1_menu()
                    if sub_sub_menu_choice == "1. Add random new banks":
                        count = self.get_not_negative_integer()
                        generate_new_banks(count)
                        print(f"Adding {count} new bank(s) to a database. ")
                        print("-" * 30)
                    elif sub_sub_menu_choice == "2. Add random new persons":
                        count = self.get_not_negative_integer()
                        generate_new_persons(count)
                        print(f"Adding {count} new person(s) to a database. ")
                        print("-" * 30)
                    elif sub_sub_menu_choice == "3. Add random new accounts":
                        count = self.get_not_negative_integer()
                        try:
                            generate_new_accounts(count)
                        except (NoPersonsError, NoBanksError) as e:
                            print(f"{e.args[0]}")
                        else:
                            print(f"Adding {count} new account(s) to a database. ")
                            print("-" * 30)
                    elif sub_sub_menu_choice == "4. Back to menu":
                        break
                    # TODO: Implement Create new bank, person, account

            elif sub_menu_choice == "2. View database data":
                while True:
                    sub_sub_menu_choice = self.show_central_bank_2_menu()
                    if sub_sub_menu_choice == "1. View banks":
                        show_banks()
                    elif sub_sub_menu_choice == "2. View persons":
                        show_persons()
                    elif sub_sub_menu_choice == "3. View accounts":
                        show_accounts()
                    elif sub_sub_menu_choice == "4. Back to menu":
                        break

            elif sub_menu_choice == "3. Back to main menu":
                break

    def handle_personal_bank_operations(self) -> None:
        while True:
            sub_menu_choice = self.show_personal_bank_menu()

            if sub_menu_choice == "1. Validate identity":
                personal_code = input("PERSONAL CODE: ")
                if not personal_code_exists(personal_code):
                    print("ERROR. Person with provided personal code does not exist. ")
                    continue
                else:
                    greet_person(personal_code)
                    while True:
                        sub_sub_menu_choice = self.show_personal_bank_1_menu()
                        # TODO procceed with operations
                        if sub_sub_menu_choice == "1. View accounts":
                            show_personal_accounts(personal_code)
                        elif sub_sub_menu_choice == "2. Withdraw money":
                            # Get account id to withdraw money from and validate data type
                            try:
                                account_id = self.get_user_id()
                            except ValueError:
                                print("ERROR. Invalid data type. ")
                                continue

                            # Else get account from db and check if account id is assigned to a person
                            account = select_account(personal_code, account_id)
                            if account is None:
                                print(
                                    f"ERROR. You don't have an account with account id: {account_id}. "
                                )
                            else:
                                # Get the amount to withdraw
                                amount = self.get_not_negative_amount()

                                # Withdraw money
                                if account.balance >= amount:
                                    withdraw(account, amount)
                                    print(
                                        f"Withdrawing {amount} from account with account id: {account_id}. "
                                    )
                                else:
                                    print("ERROR. Balance is not enough. ")

                        elif sub_sub_menu_choice == "3. Deposit money":
                            # Get account id to deposit money and validate data type
                            try:
                                account_id = self.get_user_id()
                            except ValueError:
                                print("ERROR. Invalid data type. ")
                                continue

                            # Else get account from db and check if account id is assigned to a person
                            account = select_account(personal_code, account_id)
                            if account is None:
                                print(
                                    f"ERROR. You don't have an account with account id: {account_id}. "
                                )
                            else:
                                # Get the amount to deposit
                                amount = self.get_not_negative_amount()

                                # Deposit money
                                deposit(account, amount)
                                print(
                                    f"Depositing {amount} to account with account id: {account_id}. "
                                )
                                print("-" * 30)
                        elif sub_sub_menu_choice == "4. Back to menu":
                            break

            elif sub_menu_choice == "2. Back to main menu":
                break

    def stop(self):
        self.running = False
        sys.exit("Exiting from program. ")

    def get_user_id(self) -> int:
        user_id = input("Account id: ")
        user_id = int(user_id)
        return user_id

    def get_not_negative_amount(self) -> float:
        while True:
            amount = input("Amount: ")
            # Validate user entered non negative integer
            try:
                amount = float(amount)
            except ValueError:
                print("ERROR. Invalid data type. ")
                continue
            else:
                if amount < 0:
                    print("ERROR. Enter non negative number. ")
                    continue
                return amount

    def get_not_negative_integer(self) -> int:
        while True:
            integer = input("NEW RECORDS COUNT: ")

            # Validate user entered non negative integer
            try:
                integer = int(integer)
            except ValueError:
                print("ERROR. Invalid data type. ")
                continue
            else:
                if integer < 0:
                    print("ERROR. Enter non negative integer. ")
                    continue
                return integer

    def is_valid_choice(self, choice: str, max_len: int) -> bool:
        try:
            choice = int(choice)
        except ValueError:
            return False
        else:
            if choice > 0 and choice <= max_len:
                return True
            return False

    def make_menu_choice(self, menu: list) -> int:
        menu_len = len(menu)
        while True:
            choice = input("Selection: ")
            print("")
            if not self.is_valid_choice(choice, menu_len):
                print("ERROR. Select valid menu item. ")
                continue
            return int(choice)

    def select_menu_item(self, menu: list) -> str:
        # Print menu
        for item in menu:
            print(item)
        print("-" * 30)
        # Get user choice
        choice = self.make_menu_choice(menu)
        # print(f"{menu[choice - 1]} selected. ")
        return menu[choice - 1]

    def show_main_menu(self) -> str:
        print("MAIN MENU: ")
        menu = [
            "1. Central bank operations",
            "2. Personal bank operations",
            "3. Exit from program",
        ]
        # Print menu and get user selection
        return self.select_menu_item(menu)

    def show_central_bank_menu(self) -> str:
        print("CENTRAL BANK OPERATIONS MENU: ")
        menu = [
            "1. Populate database with new data",
            "2. View database data",
            "3. Back to main menu",
        ]
        # Print menu and get user selection
        return self.select_menu_item(menu)

    def show_central_bank_1_menu(self) -> str:
        print("POPULATE DATABASE WITH NEW DATA MENU: ")
        menu = [
            "1. Add random new banks",
            "2. Add random new persons",
            "3. Add random new accounts",
            "4. Back to menu",
        ]
        # Print menu and get user selection
        return self.select_menu_item(menu)

    def show_central_bank_2_menu(self) -> str:
        print("VIEW DATABASE DATA MENU: ")
        menu = [
            "1. View banks",
            "2. View persons",
            "3. View accounts",
            "4. Back to menu",
        ]
        # Print menu and get user selection
        return self.select_menu_item(menu)

    def show_personal_bank_menu(self) -> str:
        print("PERSONAL BANK OPERATIONS MENU")
        menu = ["1. Validate identity", "2. Back to main menu"]
        # Print menu and get user selection
        return self.select_menu_item(menu)

    def show_personal_bank_1_menu(self) -> str:
        print("PERSONAL BANK OPERATIONS MENU: ")
        menu = [
            "1. View accounts",
            "2. Withdraw money",
            "3. Deposit money",
            "4. Back to menu",
        ]
        return self.select_menu_item(menu)


def main(): ...


if __name__ == "__main__":
    main()
