from typing import TYPE_CHECKING, Union

from tarina import lang
from nonebot.adapters import Bot, Message

from ..segment import Card, File, Text, Image, Video
from ..export import Target, MessageExporter, SerializeFailed, export

if TYPE_CHECKING:
    from nonebot.adapters.ntchat.message import MessageSegment


class NTChatMessageExporter(MessageExporter["MessageSegment"]):
    def get_message_type(self):
        from nonebot.adapters.ntchat.message import Message

        return Message

    @classmethod
    def get_adapter(cls) -> str:
        return "ntchat"

    @export
    async def text(self, seg: Text, bot: Bot) -> "MessageSegment":
        ms = self.segment_class

        return ms.text(seg.text)

    @export
    async def res(self, seg: Union[Image, File, Video], bot: Bot) -> "MessageSegment":
        ms = self.segment_class

        name = seg.__class__.__name__.lower()
        method = {
            "image": ms.image,
            "video": ms.video,
            "file": ms.file,
        }[name]
        if seg.path:
            return method(seg.path)
        elif seg.raw:
            return method(seg.raw_bytes)
        elif seg.url or seg.id:
            return method(seg.url or seg.id)
        else:
            raise SerializeFailed(lang.require("nbp-uniseg", "invalid_segment").format(type=name, seg=seg))

    @export
    async def card(self, seg: Card, bot: Bot) -> "MessageSegment":
        ms = self.segment_class

        if seg.flag != "xml":
            raise SerializeFailed(lang.require("nbp-uniseg", "invalid_segment").format(type="card", seg=seg))

        return ms.xml(seg.raw)

    async def send_to(self, target: Target, bot: Bot, message: Message):
        from nonebot.adapters.ntchat.bot import send
        from nonebot.adapters.ntchat.bot import Bot as NTChatBot

        assert isinstance(bot, NTChatBot)

        class FakeEvent:
            from_wxid = target.id
            room_wxid = target.id

        return await send(bot, FakeEvent, message)  # type: ignore
