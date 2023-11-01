class FormattedDistributorInfo:
    def __init__(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        pay_number: str | None = None,
        email: str | None = None,
        primary_phone: str | None = None,
        secondary_phone: str | None = None,
        zip_code: int | str | None = None,
        street_name: str | None = None,
        house_number: int | str | None = None,
        house_letter: str | None = None,
        house_floor: int | str | None = None,
        house_side: str | None = None,
        city_name: str | None = None,
    ) -> None:
        self.__first_name = (
            first_name.title()
            if isinstance(first_name, str) and len(first_name) > 0
            else None
        )
        self.__last_name = (
            first_name.title()
            if isinstance(last_name, str) and len(last_name) > 0
            else None
        )
        self.__pay_number = (
            pay_number if isinstance(pay_number, str) and len(pay_number) > 0 else None
        )
        self.__email = email if isinstance(email, str) and len(email) > 0 else None
        self.__primary_phone = (
            primary_phone
            if isinstance(primary_phone, str) and len(primary_phone) > 0
            else None
        )
        self.__secondary_phone = (
            secondary_phone
            if isinstance(secondary_phone, str) and len(secondary_phone) > 0
            else None
        )
        self.__zip_code = self.__safe_string_to_int(zip_code)
        self.__street_name = (
            street_name.title()
            if isinstance(street_name, str) and len(street_name) > 0
            else None
        )
        self.__house_number = self.__safe_string_to_int(house_number)
        self.__house_letter = (
            house_letter.upper()
            if isinstance(house_letter, str) and len(house_floor) > 0
            else None
        )
        self.__house_floor = (
            self.__safe_string_to_int(house_floor)
            if isinstance(house_floor, str) and len(house_floor) > 0
            else None
        )
        self.__house_side = (
            house_side.upper()
            if isinstance(house_side, str) and len(house_side) > 0
            else None
        )
        self.__city_name = (
            city_name.title()
            if isinstance(city_name, str) and len(first_name) > 0
            else None
        )

    @property
    def first_name(self) -> str | None:
        return self.__first_name

    @property
    def last_name(self) -> str | None:
        return self.__last_name

    @property
    def pay_number(self) -> str | None:
        return self.__pay_number

    @property
    def email(self) -> str | None:
        return self.__email

    @property
    def primary_phone(self) -> str | None:
        return self.__primary_phone

    @property
    def secondary_phone(self) -> str | None:
        return self.__secondary_phone

    @property
    def zip_code(self) -> str | None:
        return self.__zip_code

    @property
    def street_name(self) -> str | None:
        return self.__street_name

    @property
    def house_number(self) -> str | None:
        return self.__house_number

    @property
    def house_letter(self) -> str | None:
        return self.__house_letter
    
    @property
    def house_floor(self) -> str | None:
        return self.__house_floor

    @property
    def house_side(self) -> str | None:
        return self.__house_side

    @property
    def city_name(self) -> str | None:
        return self.__city_name

    @property
    def address(self) -> str | None:
        if self.__street_name == None and self.__house_number == None:
            return None

        return f"{self.__street_name} {self.__house_number}{self.__house_letter if self.__house_letter != None else ""}{f" {self.__house_floor}" if self.__house_floor != None else ""}{f" {self.__house_side}" if self.__house_side != None else ""}{f", {self.__zip_code}" if self.__zip_code != None else ""}{f", {self.__city_name}" if self.__city_name != None else ""}"

    @property
    def full_name(self) -> str | None:
        full_name = (
            f"{self.__first_name} "
            if self.__first_name != None
            else "" + self.__last_name
            if self.__last_name != None
            else ""
        )
        if len(full_name) > 0:
            return full_name
        return None

    @staticmethod
    def __safe_string_to_int(string: str) -> str | int:
        try:
            return int(string)
        except (ValueError, TypeError):
            return string
        
    def __repr__(self) -> str:
        return "FormattedDistributorInfo" + str(self.__dict__)
