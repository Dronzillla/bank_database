from models import session, Person, Bank, Account, Query
from random_words import RandomNicknames, RandomWords
from random import randint, choice
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def subtract_years(date_obj: datetime, years: int) -> datetime:
    # Subtract years from the given date object
    new_date = date_obj - relativedelta(years=years)
    return new_date


def generate_random_date() -> str:
    # Get start date in str format
    start_date = "1990-01-01"

    # Get end date in str format
    today = datetime.now()
    today_minus_18_years = subtract_years(today, 18)
    end_date = datetime.strftime(today_minus_18_years, "%Y-%m-%d")

    # Convert start and end dates to datetime objects
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    # Calculate the difference between start and end dates
    delta = end_datetime - start_datetime

    # Generate a random number of days within the date range
    random_days = randint(0, delta.days)

    # Generate a random date by adding the random number of days to the start date
    random_date = start_datetime + timedelta(days=random_days)

    return random_date.strftime("%Y-%m-%d")


def generate_random_bank_name() -> str:
    rw = RandomWords()
    word = rw.random_word(min_letter_count=5)
    bank_name = word.capitalize() + " bank"
    return bank_name


def generate_random_address() -> str:
    cities = [
        "Beach city",
        "Panama city",
        "Gardens city",
        "Strouks city",
        "Fleetwood city",
    ]
    country = "Country"

    rw = RandomWords()
    street = rw.random_word().capitalize()

    house_number = str(randint(1, 500))

    city = choice(cities)

    address = street + " st. " + house_number + ", " + city + ", " + country
    return address


def generate_random_bank_code() -> str:
    code = ""
    for _ in range(5):
        code += str(randint(0, 9))
    return code


def generate_random_swift_code(name: str, bank_code: str) -> str:
    beggining = name[:4].upper()
    country = "CT"
    swift_code = beggining + country + bank_code
    return swift_code


def generate_random_nickname(gender: str) -> str:
    rn = RandomNicknames()
    return rn.random_nick(gender=gender)


def generate_random_personal_code() -> str:
    # Get random birthday of a person
    birthday = generate_random_date()
    year, month, day = birthday.split("-")

    # Get first number of personal code
    if int(year) >= 2001:
        begining = str(randint(5, 6))
    else:
        begining = str(randint(3, 4))

    # Get the middle part of personal code
    year = year[2:]
    middle = year + month + day

    # Get 4 random ending digits
    ending = ""
    for _ in range(4):
        number = randint(0, 9)
        ending += str(number)

    # Generate random personal code
    personal_code = begining + middle + ending
    return personal_code


def generate_random_telephone() -> str:
    telephone = "+3706"
    randint(0, 9)
    for _ in range(7):
        telephone += str(randint(0, 9))
    return telephone


def generate_new_persons(count: int) -> None:
    generated_count = 0
    while True:
        # Break when enough records are generated
        if generated_count == count:
            break

        # Create new personal code
        personal_code = generate_random_personal_code()
        person = (
            session.query(Person).filter_by(personal_code=personal_code).one_or_none()
        )

        # Get random telephone
        phone = generate_random_telephone()
        person_phone = session.query(Person).filter_by(phone=phone).one_or_none()

        # Check if personal code does not exist
        if person is None and person_phone is None:
            generated_count += 1

            # Create name
            if personal_code[0] == "3" or personal_code[0] == "5":
                name = generate_random_nickname("m")
            else:
                name = generate_random_nickname("f")
            # Create surname
            surname = generate_random_nickname("u")
            surname_ending = randint(0, 1)
            if surname_ending == 0 and surname[-1] != "s":
                surname += "s"
            # Create new person in db
            person = Person(
                name=name, surname=surname, personal_code=personal_code, phone=phone
            )
            session.add(person)
            session.commit()


def get_valid_person_ids_from_db() -> list[int]:
    persons = session.query(Person).all()
    persons_ids = [person.id for person in persons]
    return persons_ids


def get_valid_bank_ids_from_db() -> list[int]:
    banks = session.query(Bank).all()
    banks_ids = [bank.id for bank in banks]
    return banks_ids


def generate_new_accounts(count: int) -> None:
    generated_count = 0
    balances = [0, 100, 500, 1000, 5000, 10000]

    # Check if there are any records created in person table
    person_ids = get_valid_person_ids_from_db()
    if len(person_ids) == 0:
        print(
            "ERROR. Unable to create new accounts. There are no persons in database. "
        )
        return

    # Check if there are any records created in bank table
    bank_ids = get_valid_bank_ids_from_db()
    if len(bank_ids) == 0:
        print("ERROR. Unable to create new accounts. There are no banks in database. ")
        return

    while True:
        if generated_count == count:
            break
        generated_count += 1

        # Get random balance
        balance = choice(balances)
        # Get random person_id
        person_id = choice(person_ids)
        # Get random bank_id
        bank_id = choice(bank_ids)

        # Create new account in db
        account = Account(balance=balance, person_id=person_id, bank_id=bank_id)
        session.add(account)
        session.commit()


def generate_new_banks(count: int) -> None:
    generated_count = 0

    while True:
        # Break when enough records are created1
        if generated_count == count:
            break

        # Create bank code
        code = generate_random_bank_code()
        bank = session.query(Bank).filter_by(code=code).one_or_none()

        if bank is None:
            generated_count += 1
            name = generate_random_bank_name()
            address = generate_random_address()
            swift = generate_random_swift_code(name, code)
            # Create new bank in db
            bank = Bank(name=name, address=address, code=code, swift=swift)
            session.add(bank)
            session.commit()


def main():

    print(generate_random_bank_name())
    print(generate_random_personal_code())
    print(generate_random_telephone())

    print("")
    bank_name = generate_random_bank_name()
    bank_code = generate_random_bank_code()
    print(generate_random_address())
    swift = generate_random_swift_code(bank_name, bank_code)
    print(swift)


if __name__ == "__main__":
    main()
