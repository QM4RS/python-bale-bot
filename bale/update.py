from __future__ import annotations

"""bale.update
~~~~~~~~~~~~~~~
Updated ``Update`` model to support *pre‑checkout* queries.

This file **overrides** the original ``Update`` definition included in
``python-bale-bot``. Only the diff‑relevant sections are rewritten to keep
compatibility while adding the following:

* ``PRE_CHECKOUT_QUERY`` constant.
* ``pre_checkout_query`` attribute + slot.
* Parsing logic in :py:meth:`from_dict`.
"""

from typing import TYPE_CHECKING, ClassVar, Dict, Optional

from bale import BaleObject, CallbackQuery, Message  # type: ignore
from bale.payments import PreCheckoutQuery  # newly added sub‑package

if TYPE_CHECKING:  # pragma: no cover
    from bale import Bot

__all__: tuple[str, ...] = ("Update",)


class Update(BaleObject):
    """Represents an incoming update from Bale servers (extended)."""

    # ---------------------------------------------------------------------
    # Event name constants
    # ---------------------------------------------------------------------

    PRE_CHECKOUT_QUERY: ClassVar[str] = "pre_checkout_query"
    CALLBACK_QUERY: ClassVar[str] = "callback_query"
    MESSAGE: ClassVar[str] = "message"
    EDITED_MESSAGE: ClassVar[str] = "edited_message"

    # ---------------------------------------------------------------------
    # Slots
    # ---------------------------------------------------------------------

    __slots__ = (
        "_id",
        "update_id",
        "pre_checkout_query",
        "callback_query",
        "message",
        "edited_message",
    )

    # ---------------------------------------------------------------------
    # Init
    # ---------------------------------------------------------------------

    def __init__(
        self,
        update_id: int,
        *,
        pre_checkout_query: Optional[PreCheckoutQuery] = None,
        callback_query: Optional[CallbackQuery] = None,
        message: Optional[Message] = None,
        edited_message: Optional[Message] = None,
    ) -> None:
        super().__init__()

        self._id: int = update_id
        self.update_id: int = int(update_id)

        self.pre_checkout_query: Optional[PreCheckoutQuery] = pre_checkout_query
        self.callback_query: Optional[CallbackQuery] = callback_query
        self.message: Optional[Message] = message
        self.edited_message: Optional[Message] = edited_message

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(cls, data: Optional[Dict], bot: "Bot") -> Optional["Update"]:
        data = BaleObject.parse_data(data)
        if not data:
            return None

        # Nested conversions ----------------------------------------------------
        data[cls.PRE_CHECKOUT_QUERY] = PreCheckoutQuery.from_dict(
            data.pop(cls.PRE_CHECKOUT_QUERY, None), bot
        )
        data[cls.CALLBACK_QUERY] = CallbackQuery.from_dict(
            data.pop(cls.CALLBACK_QUERY, None), bot
        )
        data[cls.MESSAGE] = Message.from_dict(data.pop(cls.MESSAGE, None), bot)
        data[cls.EDITED_MESSAGE] = Message.from_dict(
            data.pop(cls.EDITED_MESSAGE, None), bot
        )

        return super().from_dict(data, bot)

    # ------------------------------------------------------------------
    # Comparisons – preserve behaviour
    # ------------------------------------------------------------------

    def __eq__(self, other):  # noqa: D401 – keep original semantics
        if not isinstance(other, Update):
            return NotImplemented
        return self.update_id == other.update_id

    def __lt__(self, other):  # noqa: D401
        if not isinstance(other, Update):
            return NotImplemented
        return self.update_id < other.update_id

    def __le__(self, other):  # noqa: D401
        if not isinstance(other, Update):
            return NotImplemented
        return self.update_id <= other.update_id

    def __gt__(self, other):  # noqa: D401
        if not isinstance(other, Update):
            return NotImplemented
        return self.update_id > other.update_id

    def __ge__(self, other):  # noqa: D401
        if not isinstance(other, Update):
            return NotImplemented
        return self.update_id >= other.update_id
