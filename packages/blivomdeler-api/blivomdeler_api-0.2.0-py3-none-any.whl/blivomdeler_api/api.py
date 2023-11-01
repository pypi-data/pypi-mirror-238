from .links import POINTS_URL, GIFTS_URL, LOGOUT_URL, LOGIN_URL, INFO_URL
from .exceptions import InvalidResponseException, InternalAPIException
from .exceptions import InvalidCredentialsError, LoginRequiredError
from .translation import MONTHS_DANISH_TO_ENGLISH, translate
from .giftshop_item import item_from_dict, GiftshopItem
from .distributor_info import FormattedDistributorInfo
from typing import NoReturn, Iterable, Literal, Any
from requests import JSONDecodeError, Session
from .login_result import LoginResult
from bs4 import BeautifulSoup, Tag
from .delivery import Delivery
from warnings import warn
from datetime import date


class APISession:
    def __init__(self) -> None:
        """login: Either the salary number or the phone number.
        password: Password for the account."""
        self.__user = None
        self.__password = None

        self.__is_logged_in = False
        if self.__user != None and self.__password != None:
            self.login(self.__user, self.__password)

        self.__worker_type = None
        self.__session = Session()

    def change_information(
        self,
        new_email: str | None = None,
        new_password: str | None = None,
        new_primary_phone: str | None = None,
        new_secondary_phone: str | None = None,
    ) -> None:
        """new_email: The new email for your account.
        new_password: The new password for your account.
        new_primary_phone: The new primary phone number for your account.
        new_secondary_phone: The new secondary phone number for your account.
        """
        self.__check_logged_in()

        post_data = self.get_distributor_info(raw=True)
        for key in post_data.keys():
            if post_data.get(key) == None:
                post_data[key] = ""

        post_data["submit_person"] = ""
        if new_email != None:
            post_data["email"] = new_email
        if new_password != None:
            post_data["password"] = new_password
            post_data["repeat_password"] = new_password
        else:
            post_data["password"] = ""
            post_data["repeat_password"] = ""
        if new_primary_phone != None:
            post_data["mobile_number"] = new_primary_phone.replace(" ", "")
        if new_secondary_phone != None:
            post_data["phone_number"] = new_secondary_phone.replace(" ", "")

        get_response = self.__session.get(INFO_URL)
        page_soup = BeautifulSoup(get_response.text, "html.parser")
        wpnonce = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"name": "_wpnonce"}
        )
        referer = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"name": "_wp_http_referer"}
        )
        if referer == None:
            referer = "/min-side/stamdata-og-ansaettelsesaftale/"  # i have never seen it change, so might as well try
        if wpnonce == None:
            self.__raise_invalid_response()
        post_data["_wp_http_referer"] = referer
        post_data["_wpnonce"] = wpnonce
        post_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        post_response = self.__session.post(
            INFO_URL, data=post_data, headers=post_headers
        )

        if post_response.status_code != 200:
            self.__raise_unsupported_status_code(post_response.status_code)

        if "Ugyldig e-mail adresse" in post_response.text:
            raise ValueError("invalid email")
        elif "Dit password skal minimum indeholde" in post_response.text:
            raise ValueError("password too short")
        elif "<strong>Mobilnr.:</strong>" in post_response.text:
            raise ValueError("invalid primary phone")
        elif "<strong>Sekundær mobilnr.:</strong>" in post_response.text:
            raise ValueError("invalid secondary phone")

        with open("out.html", "wb") as file:
            file.write(post_response.content)

    def get_distributor_info(
        self, raw: bool = False
    ) -> FormattedDistributorInfo | dict[str, str | None]:
        self.__check_logged_in()

        response = self.__session.get(INFO_URL)

        if response.status_code != 200:
            self.__raise_unsupported_status_code(response.status_code)

        page_soup = BeautifulSoup(response.text, "html.parser")

        first_name = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "firstname"}
        )
        last_name = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "lastname"}
        )
        pay_number = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "p-nummer"}
        )
        email = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "email"}
        )
        primary_phone = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "mobile_number"}
        )
        secondary_phone = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "phone_number"},
        )
        zip_code = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "zipcode"},
        )
        street_name = self.__safe_find_element_attribute(
            page_soup, "value", "input", {"id": "street"}
        )
        house_number = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "street_number"},
        )
        house_letter = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "street_letter"},
        )
        house_floor = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "street_floor"},
        )
        house_side = self.__safe_find_element_attribute(
            page_soup,
            "value",
            "input",
            {"id": "street_side"},
        )
        try:
            city_name = page_soup.find("div", {"class": "city-name"}).text
        except AttributeError:
            city_name = None

        with open("change_info_get.html", "wb") as file:
            file.write(response.content)

        if not raw:
            return FormattedDistributorInfo(
                first_name,
                last_name,
                pay_number,
                email,
                primary_phone,
                secondary_phone,
                zip_code,
                street_name,
                house_number,
                house_letter,
                house_floor,
                house_side,
                city_name,
            )
        return {
            "firstname": first_name,
            "lastname": last_name,
            "p-nummer": pay_number,
            "email": email,
            "mobile_number": primary_phone,
            "phone_number": secondary_phone,
            "zipcode": zip_code,
            "street": street_name,
            "street_number": house_number,
            "street_letter": house_letter,
            "street_floor": house_floor,
            "street_side": house_side,
        }

    def get_point_history(
        self, target_years: Iterable[int] | Literal["all", "latest"] = "all"
    ) -> dict[int, dict[str, dict[str, int | list[Delivery]]]]:
        """target_years: Years to gather information for, example: (2020, 2021, 2023), 'latest' getting information for the latest/current year, and 'all' meaning to gather information for all years possible."""
        self.__check_logged_in()

        response = self.__session.get(POINTS_URL)

        if response.status_code != 200:
            self.__raise_unsupported_status_code(response.status_code)

        page_soup = BeautifulSoup(response.text, "html.parser")
        year_holders: Iterable[Tag] = page_soup.find_all(
            "div",
            {"class": "kc-pointoversigt__year-repeater"},
        )
        if target_years == "latest":
            target_years = (date.today().year,)
        elif target_years == "all":
            target_years = tuple(range(1965, date.today().year + 1))
        elif not isinstance(target_years, Iterable) and not isinstance(
            target_years, str
        ):
            raise TypeError(
                f"target_years must be either an iterable with ints, 'all', or 'latest'"
            )

        years_skipped = 0
        results: dict[int, dict[str, dict[str, int | list[Delivery]]]] = {}
        for year_holder in year_holders:
            try:
                current_year = int(
                    year_holder.find("span", {"class", "dynamic-year"}).text
                )
            except (ValueError, TypeError):
                years_skipped += 1
                continue
            if current_year not in target_years:
                continue

            results[current_year] = {}
            results[current_year]["total"] = 0
            month_holders: Iterable[Tag] = year_holder.find_all(
                "div", {"class": "kc-pointoversigt__month-repeater"}
            )
            for month_holder in month_holders:
                current_month = translate(
                    month_holder.find("div", {"class": "month"}).text,
                    MONTHS_DANISH_TO_ENGLISH,
                    True,
                )
                results[current_year][current_month] = {}
                try:
                    results[current_year][current_month]["total"] = int(
                        month_holder.find("span", {"class": "no"}).text
                    )
                except (ValueError, TypeError):
                    self.__raise_invalid_response()
                week_holders: Iterable[Tag] = month_holder.find_all(
                    "div", {"class": "kc-pointoversigt__week-repeater"}
                )
                results[current_year][current_month]["deliveries"]: list[
                    Delivery
                ] = self.__extract_deliveries(current_year, week_holders)
                results[current_year]["total"] += sum(
                    [
                        delivery.total_points
                        for delivery in results[current_year][current_month][
                            "deliveries"
                        ]
                    ]
                )
                results[current_year]["total_recieved"] += sum(
                    [
                        delivery.total_points
                        for delivery in results[current_year][current_month][
                            "deliveries"
                        ]
                        if delivery.verified
                    ]
                )

        if years_skipped:
            warn(f"{years_skipped} years were skipped because of parsing errors")
        return results

    def get_giftshop_items(
        self,
        only_return_affordable: bool = False,
    ) -> list[GiftshopItem]:
        """only_return_affordable: Only return items that you can afford."""
        self.__check_logged_in()
        data = {"action": "get_products", "language": "da"}
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

        response = self.__session.post(GIFTS_URL, data=data, headers=headers)

        if response.status_code != 200:
            self.__raise_unsupported_status_code(response.status_code)

        try:
            response_json: dict[str, Any] = response.json()
        except JSONDecodeError:
            self.__raise_invalid_response()

        product_dicts: tuple[
            dict[str, int | str | tuple[dict[str, str]]]
        ] = response_json.get("products")
        self.__check_not_none(product_dicts)

        items: list[GiftshopItem] = [
            item_from_dict(product) for product in product_dicts
        ]

        if not only_return_affordable:
            return items

        try:
            points: int = int(response_json.get("user", {}).get("points"))
        except (ValueError, TypeError):
            points = None
        if points == None:
            warn("giftshop items were not filtered", Warning)
            return items
        return [item for item in items if item.price <= points]

    def get_earned_points(self) -> int:
        self.__check_logged_in()
        data = {"action": "get_products", "language": "da"}
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

        response = self.__session.get(GIFTS_URL, data=data, headers=headers)

        if response.status_code != 200:
            self.__raise_unsupported_status_code(response.status_code)

        try:
            response_json: dict[str, Any] = response.json()
        except JSONDecodeError:
            self.__raise_invalid_response()

        try:
            points = int(response_json["user"]["points"])
        except (ValueError, TypeError, KeyError):
            self.__raise_invalid_response()
        return points

    def logout(self) -> None:
        self.__check_logged_in()

        self.__session.get(LOGOUT_URL)
        self.__is_logged_in = False

    def login(self, user: str, password: str) -> LoginResult:
        """password: Password for the account.
        login: Either the salary number or the phone number."""
        self.__ensure_session_id()
        data = {
            "action": "disy_login",
            "remember_loennr": "0",
            "language": "da",
            "loennr": user,
            "password": password,
        }
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        response = self.__session.post(LOGIN_URL, data=data, headers=headers)
        try:
            response_json: dict[str, Any] = response.json()
        except JSONDecodeError:
            self.__raise_invalid_response()

        if response.status_code == 200:
            if not response_json.get("success"):
                raise InvalidCredentialsError(f"invalid user or password")
        else:
            self.__raise_unsupported_status_code(response.status_code)

        self.__user = user
        self.__password = password
        self.__worker_type = response_json.get("medarbejdertype")
        self.__is_logged_in = True

        return LoginResult(self.__user, self.__password, self.__worker_type)

    def __extract_deliveries(
        self,
        current_year: int,
        week_holders: Iterable[Tag],
    ) -> list[Delivery]:
        results: list[Delivery] = []
        for week_holder in week_holders:
            # whether the delivery has been verified
            verified = "på vej" not in week_holder.text

            # delivery start date and deadlines
            try:
                current_delivery_date = week_holder.find(
                    "div", {"class": "month"}
                ).text.split(" ")[2:]
            except AttributeError:
                self.__raise_invalid_response()
            current_delivery_date[1:2] = []  # remove the middle
            start_date_as_string = current_delivery_date[0].split("/")
            end_date_as_string = current_delivery_date[1].split("/")
            try:
                start_date = date(
                    current_year,
                    int(start_date_as_string[1]),
                    int(start_date_as_string[0]),
                )
                end_date = date(
                    current_year,
                    int(end_date_as_string[1]),
                    int(end_date_as_string[0]),
                )
            except (ValueError, TypeError):
                self.__raise_invalid_response()

            info_holders: Iterable[Tag] = week_holder.find_all(
                "div", {"class": "info-repeater"}
            )

            # bundle count
            try:
                for info_holder in info_holders:
                    if "Antal bundter" in info_holder.text:
                        bundle_points = int(info_holder.attrs.get("data-total"))
                        bundles = int(
                            info_holder.find("span", {"class": "title"}).text.split(
                                " "
                            )[2]
                        )
            except (ValueError, TypeError, AttributeError):
                self.__raise_invalid_response()

            # distributed routes
            try:
                distribution_points = 0
                distributed_routes = 0
                for info_holder in info_holders:
                    if "Antal omdelte ruter" in info_holder.text:
                        distribution_points = int(info_holder.attrs.get("data-total"))
                        distributed_routes = int(
                            info_holder.find("span", {"class": "title"}).text.split(
                                " "
                            )[3]
                        )
            except (ValueError, TypeError, AttributeError):
                self.__raise_invalid_response()

            # experience
            try:
                experience_points = 0
                experience_weeks = 0
                for info_holder in info_holders:
                    if "Erfaringspoint" in info_holder.text:
                        experience_points = int(info_holder.attrs.get("data-total"))
                        experience_weeks = int(
                            info_holder.find("span", {"class": "title"}).text.split(
                                " "
                            )[1]
                        )
            except (ValueError, TypeError, AttributeError):
                self.__raise_invalid_response()

            # extra points
            try:
                extra_points = 0
                for info_holder in info_holders:
                    if not any(
                        [
                            string in info_holder.text
                            for string in (
                                "Erfaringspoint",
                                "Antal omdelte ruter",
                                "Antal bundter",
                            )
                        ]
                    ):
                        extra_points = int(info_holder.attrs.get("data-total"))
            except (ValueError, TypeError, AttributeError):
                self.__raise_invalid_response()

            results.append(
                Delivery(
                    verified,
                    start_date,
                    end_date,
                    bundles,
                    bundle_points,
                    distributed_routes,
                    distribution_points,
                    experience_weeks,
                    experience_points,
                    extra_points,
                )
            )
        return results

    def __safe_find_element_attribute(
        self,
        soup: BeautifulSoup,
        attribute_name: str,
        element_name: str | None = None,
        required_element_attributes: dict[str, str] | None = None,
        recursive_search: bool = True,
        default_return_value: Any = None,
    ) -> str | None:
        try:
            return soup.find(
                element_name, required_element_attributes, recursive_search
            ).attrs[attribute_name]
        except (AttributeError, KeyError, ValueError, TypeError):
            return default_return_value

    def __check_logged_in(self) -> None:
        if not self.__is_logged_in:
            raise LoginRequiredError("you have to be logged in to do this action")
        if not self.has_session_id:
            raise LoginRequiredError("you have no session id, try to login again")

    def __ensure_session_id(self) -> None:
        if not self.has_session_id:
            self.__session.get(
                LOGIN_URL
            )  # going to the login page retrieves a session id

    @staticmethod
    def __raise_invalid_response() -> NoReturn:
        raise InvalidResponseException(
            "invalid response from api, try to update the module or submit an issue on https://github.com/objectiveSquid/blivomdeler-api"
        )

    @staticmethod
    def __raise_unsupported_status_code(status_code: int) -> NoReturn:
        raise InternalAPIException(f"unhandled response code {status_code} from server")

    @staticmethod
    def __check_not_none(object: Any) -> None:
        if object == None:
            raise InvalidResponseException("invalid response from api")

    @property
    def has_session_id(self) -> bool:
        return "PHPSESSID" in self.__session.cookies.keys()

    @property
    def user(self) -> str:
        return self.__user

    @property
    def password(self) -> str:
        return self.__password

    @property
    def worker_type(self) -> str:
        return self.__worker_type

    @property
    def http_session(self) -> Session:
        return self.__session

    @property
    def is_logged_in(self) -> bool:
        return self.__is_logged_in
