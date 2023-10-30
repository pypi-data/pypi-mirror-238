from types import TracebackType
from typing import Type
from heaobject.activity import DesktopObjectAction, Status
from heaobject.user import NONE_USER
from heaobject.root import Share, ShareImpl, Permission, DesktopObject
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.aiohttp import absolute_url_minus_base
from aiohttp.web import Request, Application

from typing import Any
from abc import ABC, abstractmethod
from collections.abc import Iterable, Callable, Awaitable
from contextlib import AbstractAsyncContextManager
import logging


def default_shares(request: Request) -> tuple[ShareImpl]:
    """
    Default shares are NONE_USER and VIEWER permission.
    """
    share = ShareImpl()
    share.user = request.headers.get(SUB, NONE_USER)
    share.permissions = [Permission.VIEWER]
    return (share,)


class DesktopObjectActionLifecycle(AbstractAsyncContextManager[DesktopObjectAction | None]):
    """
    Asynchronous context manager that generates desktop object actions and puts them on the message queue.
    """

    def __init__(self, request: Request,
                 code: str,
                 description: str, *,
                 user_id: str | None = None,
                 shares: Iterable[Share] | None = None,
                 activity_cb: Callable[[Application, DesktopObjectAction], Awaitable[None]] | None = None) -> None:
        """
        Creates the context manager. A HTTP request, code, and description are required. Code may be any value that is
        meaningful to a microservice or web client, but HEA provides a set of standard codes that this context manager
        will populate automatically. They are:
            hea-get: Accessing a desktop object was attempted.
            hea-create: Creating a desktop object was attempted.
            hea-update: Updating a desktop object was attempted.
            hea-duplicate: Duplicating a desktop object was attempted.
            hea-move: Moving a desktop object was attempted.
            hea-archive: Archiving a desktop object was attempted.
            hea-unarchive: Unarchiving a desktop object was attempted.
        HEA reserves the hea- prefix for future extension. For custom codes, you must populate the action in the body
        of the context manager block.

        :param request: HTTP request (required).
        :param code: one of the codes above (required).
        :param description: A brief description of the action for display in a user interface (required).
        :param user_id: the id of the user who attempted the action.
        :param shares: the users with whom this action may be shared.
        :param activity_cb: a callable that publishes the action on the message queue.
        :raises TypeError: if an argument of the wrong type was provided.
        :raises ValueError: if an otherwise invalid value was passed as an argument.
        """
        if code is None:
            raise ValueError('code cannot be None')
        if description is None:
            raise ValueError('description cannot be None')
        if not isinstance(request, Request):
            raise TypeError(f'request must be a Request but was a {type(request)}')
        self.__request = request
        self.__code = str(code)
        self.__description = str(description)
        self.__activity: DesktopObjectAction | None = None
        self.__user_id = str(user_id) if user_id is not None else request.headers.get(SUB, NONE_USER)
        self.__shares = list(shares) if shares is not None else list(default_shares(request))
        if any(not isinstance(share, Share) for share in self.__shares):
            raise ValueError(f'shares must all be Share objects but were {", ".join(set(str(type(share)) for share in self.__shares))}')
        self.__activity_cb: Callable[[Application, DesktopObjectAction], Awaitable[None]] | None = activity_cb


    async def __aenter__(self) -> DesktopObjectAction:
        self.__activity = DesktopObjectAction()
        self.__activity.generate_application_id()
        self.__activity.code = self.__code
        self.__activity.owner = NONE_USER
        self.__activity.shares = self.__shares
        self.__activity.user_id = self.__user_id
        self.__activity.description = self.__description
        if self.__activity_cb:
            await self.__activity_cb(self.request.app, self.__activity)

        self.__activity.status = Status.IN_PROGRESS
        if self.__activity_cb:
            await self.__activity_cb(self.request.app, self.__activity)

        return self.__activity

    async def __aexit__(self, exc_type: Type[BaseException] | None,
                        exc_value: BaseException | None,
                        traceback: TracebackType | None) -> Any:
        if exc_type is not None:
            self.__activity.status = Status.FAILED
        elif self.__activity.status not in (Status.SUCCEEDED, Status.FAILED):
            if exc_type is None:
                self.__activity.status = Status.SUCCEEDED
            else:
                self.__activity.status = Status.FAILED
        if self.__activity_cb:
            await self.__activity_cb(self.request.app, self.__activity)

    @property
    def request(self) -> Request:
        """The request."""
        return self.__request

    @property
    def code(self) -> str:
        """The code."""
        return self.__code

    @property
    def desktop_object_action(self) -> DesktopObjectAction | None:
        """The created desktop action."""
        return self.__activity
