from typing import Iterable, Literal
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class GiftshopItem:
    id: int
    disyid: int | str
    sku: str
    price: int
    category: str
    title: str
    description_html: str
    image_url: str
    deliver_via_gls: bool
    deliver_via_sms: bool
    deliver_via_email: bool
    options: Iterable[dict[str, str]] | None = None

    @property
    def description_plaintext(self) -> str:
        return BeautifulSoup(self.description_html, "html.parser").get_text()

    def __str__(self) -> str:
        return f"{self.title}: price={self.price}, category={self.category}"


def item_from_dict(
    target_dict: dict[
        Literal[
            "id",
            "disyid",
            "sku",
            "price",
            "category",
            "title",
            "desc",
            "image",
            "gls",
            "sms",
            "email",
        ],
        int | str | tuple[dict[str, str]],
    ]
) -> GiftshopItem:
    try:
        return GiftshopItem(
            target_dict["id"],
            target_dict["disyid"],
            target_dict["sku"],
            target_dict["price"],
            target_dict["category"],
            target_dict["title"],
            target_dict["desc"],
            target_dict["image"],
            target_dict["gls"],
            target_dict["sms"],
            target_dict["email"],
            target_dict.get("options"),
        )
    except KeyError:
        raise ValueError("invalid keys in dictionary target_dict")
