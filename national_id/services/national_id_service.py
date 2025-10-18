from datetime import datetime
from logging import Logger
from national_id.constants.constants import GOVERNORATE_NAME_BY_CODE
from national_id.helpers.check_sum import validate_check_sum
from national_id.helpers.dates import calculate_age


class NationalIdService():
    @staticmethod
    def validate_national_id(national_id: str) -> tuple[bool, str]:
        """
        Validates a national ID.

        Args:
            national_id (str): The national ID to be validated.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating whether the national ID is valid and a string describing the 
            reason for invalidity if the national ID is invalid.
        """

        try:
            governorate_code = national_id[7:9]
            if governorate_code not in GOVERNORATE_NAME_BY_CODE:
                return False, "Invalid governorate code"

            century = "19" if national_id[0] == "2" else "20"
            year = int(century + national_id[1:3])
            month = int(national_id[3:5])
            day = int(national_id[5:7])
            
            now = datetime.now()
            try:
                birth_date = datetime(year, month, day)
                if birth_date > now:
                    return False, "Birth date is in the future"
            except ValueError:
                return False, "Invalid birth date"

            isValid = validate_check_sum(national_id)
            if not isValid:
                return False, "Invalid check digit"

            return True, "valid"
        except Exception as e:
            Logger.error(f"[NationalIdService][validate_national_id] Unexpected error: {e}")
            return False, "Unexpected error"

    @staticmethod
    def extract_data_from_national_id(national_id: str) -> dict:
        """
        Extracts data from a national ID.

        Args:
            national_id (str): The national ID to extract data from.

        Returns:
            tuple[dict, str]: A tuple containing a dictionary of extracted data and a string describing the reason for invalidity if the national ID is invalid.
        """
        try:    
            isValidNationalId = NationalIdService.validate_national_id(national_id)
            if not isValidNationalId[0]:
                return {
                    "is_valid_national_id": False,
                    "reason": isValidNationalId[1]
                }

            governorate_code = national_id[7:9]
            governorate_name = GOVERNORATE_NAME_BY_CODE[governorate_code]

            century = "19" if national_id[0] == "2" else "20"
            year = int(century + national_id[1:3])
            month = int(national_id[3:5])
            day = int(national_id[5:7])
            birth_date = datetime(year, month, day)

            ageDetails = calculate_age(birth_date)
            parsedAge = f"{ageDetails[0]} years, {ageDetails[1]} months, {ageDetails[2]} days"

            gender = "Male" if int(national_id[12]) % 2 == 1 else "Female"

            return {
                "birth_governorate_name": governorate_name,
                "birth_date": birth_date,
                "age": parsedAge,
                "gender": gender
            }
        except Exception as e:
            print(e)
            Logger.error(f"[NationalIdService][extract_data_from_national_id] Unexpected error: {e}")
            return False, "Unexpected error"