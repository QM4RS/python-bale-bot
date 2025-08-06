from __future__ import annotations

from typing import Optional, Dict, Any
from bale import BaleObject, User


class PreCheckoutQuery(BaleObject):
    """This object contains information about an incoming pre-checkout query.

    Attributes
    ----------
    id : str
        Unique transaction identifier.
    from_user : User
        User who is paying.
    currency : str
        Three-letter ISO 4217 currency code (always "IRR" for Bale).
    total_amount : int
        Total price in the smallest units of the currency.
    invoice_payload : str
        Bot-specified invoice payload passed in send_invoice.
    """

    __slots__ = (
        "id",
        "from_user",
        "currency",
        "total_amount",
        "invoice_payload",
    )

    def __init__(
        self,
        id: str,
        from_user: User,
        currency: str,
        total_amount: int,
        invoice_payload: str,
    ) -> None:
        super().__init__()
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self._lock()

    @classmethod
    def from_dict(
        cls,
        data: Optional[Dict[str, Any]],
        bot,
    ) -> Optional[PreCheckoutQuery]:  # type: ignore[return]
        data = BaleObject.parse_data(data)
        if not data:
            return None
        data["from_user"] = User.from_dict(data.pop("from", None), bot)
        return super().from_dict(data, bot)
