from __future__ import annotations

import json

from pathlib import Path

from b22ao.aosystem import AOSystem
from b22ao.message import Message, State

from typing import Optional


class BaseOperation:

    """
    Base class for any adaptive optics routine.
    Children implement #start and #stop, and can #deform the mirrors and #capture data from the camera at their leisure!
    """

    def __init__(self):

        self.ao = AOSystem()
        self.config = None
        self.listener = None

    def attach_listener(self, listener):
        self.listener = listener

    def load_config(self, config: Optional[str | Path]):
        if config:
            with open(config, 'r') as doc:
                self.config = json.load(doc)

    def select_dm(self, dm: int):
        """
        If your entire operation involves a single mirror, you can specify it here

        e.g. passed in as config:

        self.select_dm(self.config['mirror'])  # where "mirror": 2 in config file
        # later:
        self.deform(mask)  # no need to specify mirror in subsequent calls
        """
        self.ao.select_dm(dm)

    def deform(self, mask, mirror: Optional[int] =None):
        """
        Send a mask to specified mirror (1 or 2).

        If a mirror was previously selected with #select_dm
        and no mirror is specified here, the mask is applied
        to the mirror selected earlier.

        Bear in mind that the deformable mirrors in B22 *do not* support readback,
        so there is no guarantee that the mask is fully applied by the time this
        function returns; it may be necessary to wait for an empirically-determined
        time before characterising the system.
        """
        self.ao.deform(mask, mirror)

    def capture(self):
        """
        Returns a single detector frame
        """
        return self.ao.capture()

    def run(self):
        """
        Do not override. Implement #start instead
        """
        self.notify(Message(self, State.Running))
        self.start()
        self.notify(Message(self, State.Idle))

    def abort(self):
        """
        Do not override. Implement #stop instead
        """
        self.stop()
        self.notify(Message(self, State.Idle, "Aborted"))

    def start(self):
        """
        Starts the operation

        If a JSON configuration file was specified,
        implementations can now access the dictionary self.config
        """
        raise NotImplementedError

    def stop(self):
        """
        Stops the operation
        """
        raise NotImplementedError

    def report_progress(self, iteration, value, **other_stuff):
        """
        Inform a listening component (e.g. a live plot) of the latest result.
        """
        msg = dict({"iteration": iteration, "value": value}, **other_stuff)
        self.notify(Message(self, State.Running, msg))

    def report_error(self, error_msg: str):
        msg = {"error": error_msg}
        self.notify(Message(self, State.Error, msg))

    def notify(self, message: Message):
        try:
            self.listener.notify(message)
        except AttributeError:
            print(message)
