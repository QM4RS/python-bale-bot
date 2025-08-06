from __future__ import annotations

"""bale.payments.precheckoutquery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Module containing :class:`PreCheckoutQuery`, representing an incoming *pre‑checkout* query that **must be answered by the bot within 10 seconds**.

This file follows the style conventions of the existing *python‑bale‑bot* code‑base –
all public attributes are explicitly declared inside ``__init__`` and a ``from_dict``
constructor delegates to :class:`BaleObject` after preparing nested objects.
"""

from typing import Optional, Dict, TYPE_CHECKING

from bale import BaleObject, User

if TYPE_CHECKING:  # pragma: no cover
    from bale import Bot

__all__: tuple[str, ...] = (
    "PreCheckoutQuery",
)


class PreCheckoutQuery(BaleObject):
    """Information about an invoice payment that is about to be *finalised*.

    Attributes
    ----------
    id : str
        Unique identifier for this query.
    from_user : :class:`bale.User`
        The user who is about to complete the payment.
    currency : str
        ISO‑4217 currency code – for Bale payments always ``"IRR"``.
    total_amount : int
        Total price in the *smallest* units of the currency (Toman × 10).
    invoice_payload : str
        Payload specified by the bot in :meth:`bale.Bot.send_invoice`.
    """

    __slots__ = (
        "_id",
        "id",
        "from_user",
        "currency",
        "total_amount",
        "invoice_payload",
    )

    def __init__(
        self,
        id: str,
        from_user: "User",
        currency: str,
        total_amount: int,
        invoice_payload: str,
    ) -> None:
        super().__init__()

        # Public / private aliases (keep in sync with existing models)
        self._id: str = id
        self.id: str = id
        self.from_user: "User" = from_user

        self.currency: str = currency
        self.total_amount: int = int(total_amount)
        self.invoice_payload: str = invoice_payload

    # ------------------------------------------------------------------
    # Convenience aliases
    # ------------------------------------------------------------------

    @property
    def user(self) -> "User":
        """Alias for :attr:`from_user`."""
        return self.from_user

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(
        cls, data: Optional[Dict], bot: "Bot"
    ) -> Optional["PreCheckoutQuery"]:
        """Create a :class:`PreCheckoutQuery` from API dictionary."""
        data = BaleObject.parse_data(data)
        if not data:
            return None

        # Convert nested objects ------------------------------------------------
        data["from_user"] = User.from_dict(data.pop("from", None), bot)

        return super().from_dict(data, bot)
