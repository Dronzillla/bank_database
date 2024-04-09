from utils import seperate_string
from models import session, Person, Bank, Account, Query, engine
from sqlalchemy import create_engine, MetaData, Table

# TODO update this variable with more data types
SQL_TYPE_PYTHON = {"VARCHAR": str, "INTEGER": int, "FLOAT": float}


# Functions to make copy of sql database to mongodb database
def get_sql_table_names() -> list[str]:
    """get_sql_table_names _summary_

    Returns:
        list[str]: A list of sql database table names.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables = metadata.tables.keys()
    return list(tables)


def get_sql_column_names(table_name: str) -> dict:
    """get_sql_column_names _summary_

    Args:
        table_name (str): Table name in sql database.

    Returns:
        dict: Returns a dictionary with key as column name and value as python data type.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    # table type is sqlalchemy.sql.schema.Table
    table = metadata.tables[table_name]

    result = {}
    for column in table.columns:
        column_name = column.name
        column_type = column.type
        column_type_str = str(column_type)
        # Map sql data type with python data type
        data_type = SQL_TYPE_PYTHON[column_type_str]
        # Create dictionary for each column, key - column name, value - python data type
        result[column_name] = result.get(column_name, data_type)
    return result


def return_table_data(table_name: str) -> list[tuple]:
    """return_table_data _summary_

    Args:
        table_name (str): Table name in sql database.

    Returns:
        list[tuple]: Returns a list of records as tuples.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    # table type is sqlalchemy.sql.schema.Table
    table = metadata.tables[table_name]
    data = session.query(table).all()
    return data


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


def main():
    return_table_data("bank")


if __name__ == "__main__":
    main()
