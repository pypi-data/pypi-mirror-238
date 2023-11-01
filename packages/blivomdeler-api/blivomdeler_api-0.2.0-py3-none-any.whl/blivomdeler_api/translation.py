MONTHS_DANISH_TO_ENGLISH: dict[str, str] = {
    "januar": "january",
    "februar": "february",
    "marts": "march",
    "april": "april",
    "maj": "may",
    "juni": "june",
    "juli": "july",
    "august": "august",
    "september": "september",
    "oktober": "october",
    "november": "november",
    "december": "december",
}


def translate(string: str, table: dict[str, str], casefold: bool = False) -> str:
    if casefold:
        string = string.casefold()
    for original, replacement in zip(tuple(table.keys()), tuple(table.values())):
        string = string.replace(
            original if not casefold else original.casefold(),
            replacement if not casefold else replacement.casefold(),
        )
    return string
