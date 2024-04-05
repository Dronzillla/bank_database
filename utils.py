from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def seperate_string(func: callable):
    def wrapper(*args, **kwargs):
        print("-+-" * 3)
        result = func(*args, **kwargs)
        print("-+-" * 3)
        return result

    return wrapper


def subtract_years(date_obj: datetime, years: int) -> datetime:
    # Subtract years from the given date object
    new_date = date_obj - relativedelta(years=years)
    return new_date


def main(): ...


if __name__ == "__main__":
    main()
