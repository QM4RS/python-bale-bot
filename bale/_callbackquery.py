# An API wrapper for Bale written in Python
# Copyright (c) 2022-2024
# Kian Ahmadian <devs@python-bale-bot.ir>
# All rights reserved.
#
# This software is licensed under the GNU General Public License v2.0.
# See the accompanying LICENSE file for details.
#
# You should have received a copy of the GNU General Public License v2.0
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-2.0.html>.
from __future__ import annotations
from bale import BaleObject, User, Message
from typing import Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from bale import Bot

__all__ = (
    "CallbackQuery"
)


class CallbackQuery(BaleObject):
    """
    This object represents an incoming callback query from a callback button in an inline keyboard.

    Attributes
    ----------
        id: :obj:`str`
            Unique identifier for this query.
        from_user: :class:`bale.User`
            Sender.
        message: :class:`bale.Message`, optional
            Message with the callback button that originated the query.
            Note that message content and message date will not be available if the message is too old.
        inline_message_id: :obj:`str`, optional
            Identifier of the message sent via the bot in inline mode, that originated the query.
        data: :obj:`str`, optional
             Data associated with the callback button.
             Be aware that the message, which originated the query, can contain no callback buttons with this data.
    """
    __slots__ = (
        "id",
        "from_user",
        "message",
        "inline_message_id",
        "data"
    )

    def __init__(
            self, callback_id: str, from_user: "User", data: Optional[str] = None,
            message: Optional["Message"] = None, inline_message_id: Optional[str] = None
    ) -> None:
        super().__init__()
        self._id = callback_id
        self.id = callback_id
        self.from_user = from_user

        self.data = data
        self.message = message
        self.inline_message_id = inline_message_id

    @property
    def user(self):
        """Aliases for :attr:`from_user`"""
        return self.from_user

    @classmethod
    def from_dict(cls, data: Optional[Dict], bot: "Bot"):
        data = BaleObject.parse_data(data)
        if not data:
            return None

        data["callback_id"] = data.pop("id")
        data["from_user"] = User.from_dict(data.pop("from", None), bot)
        data["message"] = Message.from_dict(data.get("message"), bot)

        return super().from_dict(data, bot)

    def answer(
            self,
            text: Optional[str] = None,
            show_alert: bool = False,
            cache_time: Optional[int] = None
    ):
        """
        Respond to the callback query to remove the loading state and optionally display an alert.

        Args:
            text: Text of the notification. If not set, no notification is shown.
            show_alert: If True, displays an alert popup instead of a toast.
            cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side.
        """
        payload: Dict[str, object] = {"callback_query_id": self.id}
        if text is not None:
            payload["text"] = text
        if show_alert:
            payload["show_alert"] = True
        if cache_time is not None:
            payload["cache_time"] = cache_time

        # Use internal request method to call Bale API
        return self.bot.answer_callback_query(self.id, text, show_alert, cache_time)