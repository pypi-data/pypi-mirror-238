# -*- coding: utf-8 -*-
"""
    pip_services4_rpc.commands.IEventListener
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for event_name listeners.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.exec import Parameters
from pip_services4_components.context import IContext

from ..commands import IEvent


class IEventListener(ABC):
    """
    An interface for listener objects that receive notifications on fired events.

    Example:

    .. code-block:: python
    
        class MyListener(IEventListener):
            def on_event(self, context, event_name, args):
                print("Fired event_name " + event_name.get_name())

        event = Event("myevent")
        event.addListener(MyListener())
        event.notify(Context.from_trace_id("123"), Parameters.from_tuples("param1", "ABC"))
    """

    def on_event(self, context: Optional[IContext], event: IEvent, value: Parameters):
        """
        A method called when events this listener is subscrubed to are fired.

        :param context: (optional) transaction id to trace execution through call chain.

        :param event: event_name reference

        :param value: event_name arguments
        """
        raise NotImplementedError('Method from interface definition')
