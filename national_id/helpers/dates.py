from datetime import date, datetime

def calculate_age(birth_date: date) ->  tuple[int, int, int]:
    """
    Calculates the age from a birth date.

    Args:
        birth_date (date): The birth date.

    Returns:
        tuple[int, int, int]: A tuple containing the age in years, months, and days.
    """
    now = datetime.now()
    
    years = now.year - birth_date.year
    months = now.month - birth_date.month
    days = now.day - birth_date.day

    # Adjust days and months if negative
    if days < 0:
        # borrow days from previous month
        months -= 1
        # get number of days in previous month
        prev_month = (now.month - 1) if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        # days in previous month
        days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - datetime(prev_year, prev_month, 1)).days
        days += days_in_prev_month

    if months < 0:
        months += 12
        years -= 1

    return years, months, days
