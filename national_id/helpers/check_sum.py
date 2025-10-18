def validate_check_sum(national_id: str) -> bool:
    weights = [2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    total = sum(int(digit) * weights[i] for i, digit in enumerate(national_id[:13]))

    check_digit = 11 - (total % 11)
    check_digit = check_digit % 10

    return check_digit == int(national_id[-1])
