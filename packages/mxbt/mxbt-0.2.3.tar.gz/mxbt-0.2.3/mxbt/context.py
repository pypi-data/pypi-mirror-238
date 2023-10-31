from nio import MatrixRoom, Event, RoomMessageText
from dataclasses import dataclass, field
from typing import List

from .types.file import File
from .api import Api

@dataclass
class Context:
    """
    Event context class
    """
    api: Api
    room: MatrixRoom
    room_id: str
    event: Event
    sender: str
    event_id: str
    body: str=str()
    command: str=str()
    args: List[str]=field(
        default_factory=lambda: list()
    )
    substring: str=str()

    async def send(self, body: str | File, use_html: bool=False) -> None:
        """
        Send text or file to context room

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.api.send(self.room_id, body, use_html)
        #await self.__send(body, use_html, False, False)

    async def reply(self, body: str | File, use_html: bool=False) -> None:
        """
        Reply context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.api.reply(self.room_id, body, self.event_id, use_html)
        #await self.__send(body, use_html, True, False)

    async def edit(self, body: str | File, use_html: bool=False) -> None:
        """
        Edit context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.api.edit(self.room_id, body, self.event_id, use_html)
        #await self.__send(body, use_html, False, True)
 
    async def delete(self, reason: str | None=None) -> None:
        """
        Delete context event

        Parameters:
        -------------
        reason: str | None - optional
            Reason, why message is deleted
        """
        await self.api.delete(
            self.room.room_id,
            self.event.event_id,
            reason
        )
    
    async def react(self, body: str) -> None:
        """
        Send reaction to context message.

        Parameters:
        --------------
        body : str
            Reaction emoji.
        """
        await self.api.send_reaction(
            self.room.room_id,
            self.event.event_id,
            body
        )

    @staticmethod
    def __parse_command(message: RoomMessageText) -> tuple:
        args = message.body.split(" ")
        command = args[0]
        if len(args) > 1:
            args = args[1:]
        return command, args

    @staticmethod
    def from_command(api: Api, room: MatrixRoom, message: RoomMessageText):
        command, args = Context.__parse_command(message)
        return Context(
            api=api,
            room=room, 
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body,
            command=command,
            args=args,
            substring=' '.join(args)
        )

    @staticmethod
    def from_text(api: Api, room: MatrixRoom, message: RoomMessageText):
        return Context(
            api=api,
            room=room,
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body
        )

