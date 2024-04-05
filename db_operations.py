from utils import seperate_string
from models import session, Person, Bank, Account, Query


# MAIN MENU
# 1. Central banking operations
# 2. View database data
@seperate_string
def show_banks() -> None:
    banks = session.query(Bank).order_by(Bank.name)
    for bank in banks:
        print(bank)


@seperate_string
def show_persons() -> None:
    persons = session.query(Person).order_by(Person.name, Person.surname)
    for person in persons:
        print(person)


@seperate_string
def show_accounts() -> None:
    accounts = (
        session.query(Account, Bank, Person)
        .join(Bank, Account.bank_id == Bank.id)
        .join(Person, Account.person_id == Person.id)
        .order_by(Bank.name, Person.personal_code)
    )
    for account, bank, person in accounts:
        print(
            f"{bank.name} - Account id: {account.id}, Account balance: {account.balance}, Person surname: {person.surname}, Person personal code: {person.personal_code}"
        )


# MAIN MENU.
# 2. Personal bank operations
# 1. Validate identity
def personal_code_exists(personal_code: str) -> bool:
    person_exists = (
        session.query(Person).filter_by(personal_code=personal_code).one_or_none()
    )
    if person_exists is not None:
        return True
    return False


def greet_person(personal_code: str) -> None:
    person = session.query(Person).filter_by(personal_code=personal_code).one_or_none()
    greeting = f"~Welcome {person.name} {person.surname}, {person.phone}~"
    print(greeting)


# 1. View accounts
@seperate_string
def show_personal_accounts(personal_code: str) -> None:
    results = (
        session.query(Person, Account, Bank)
        .filter_by(personal_code=personal_code)
        .join(Account, Person.id == Account.person_id)
        .join(Bank, Account.bank_id == Bank.id)
    ).order_by(Bank.name)

    # print(f"Account information for person with personal code: '{personal_code}': ")
    for person, account, bank in results:
        print(
            f"{bank.name} - Account id: {account.id}, Account balance: {account.balance}"
        )


# Select account (for withdraw and deposit operations)
def select_account(personal_code: str, id: int) -> Query:
    # Select account
    account = (
        session.query(Account, Person)
        .filter_by(id=id)
        .join(Person, Account.person_id == Person.id)
        .filter_by(personal_code=personal_code)
        .one_or_none()
    )

    if account is None:
        return None
    else:
        return account[0]


# 2. Withdraw money
def withdraw(account: Query, amount: float) -> None:
    account.balance = round(account.balance - amount, 2)
    session.commit()


# 3. Desposit money
def deposit(account: Query, amount: float) -> None:
    account.balance = round(account.balance + amount, 2)
    session.commit()


def main(): ...


if __name__ == "__main__":
    main()
