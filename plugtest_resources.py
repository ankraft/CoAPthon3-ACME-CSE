# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional, Tuple, Callable

import logging
import threading
import time

from coapthon import defines
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from coapthon.messages.request import Request
__author__ = 'Giacomo Tanganelli'


logger = logging.getLogger(__name__)


class TestResource(Resource):
    def __init__(self, name:Optional[str]="TestResource", coap_server:Optional[CoAP]=None) -> None:
        super(TestResource, self).__init__(name, coap_server, visible=True, observable=False, allow_children=True)
        self.payload = "Test Resource"
        self.resource_type = "Type1"
        self.maximum_size_estimated = len(self.payload)

    def render_GET(self, request:Request) -> Resource:
        return self

    def render_PUT(self, request:Request) -> Resource:
        for option in request.options:
            if option.number == defines.OptionRegistry.CONTENT_TYPE.number:
                self.payload = (option.value, request.payload)
                return self
        self.payload = request.payload
        return self

    def render_POST(self, request:Request) -> Resource:
        res = TestResource()
        res.location_query = request.uri_query
        for option in request.options:
            if option.number == defines.OptionRegistry.CONTENT_TYPE.number:
                res.payload = {option.value: request.payload}
                return res

        res.payload = request.payload
        return res

    def render_DELETE(self, request:Request) -> bool:
        return True


class SeparateResource(Resource):

    def __init__(self, name:Optional[str]="Separate", coap_server:Optional[CoAP]=None) -> None:
        super(SeparateResource, self).__init__(name, coap_server, visible=True, observable=False, allow_children=False)
        self.payload = "Separate Resource"
        self.interface_type = "separate"
        self.add_content_type("text/plain")

    def render_GET(self, request:Request) -> Tuple[Resource, Callable]:
        return self, self.render_GET_separate

    def render_GET_separate(self, request:Request) -> Resource:
        time.sleep(5)
        return self


class ObservableResource(Resource):

    def __init__(self, name:Optional[str]="Obs", coap_server:Optional[CoAP]=None) -> None:
        super(ObservableResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        self.payload = "Observable Resource"
        self.period = 5
        self.update(True)

    def render_GET(self, request:Request) -> Resource:
        return self

    def render_POST(self, request:Request) -> Resource:
        self.payload = request.payload
        return self

    def update(self, first:Optional[bool]=False) -> None:
        self.payload = "Observable Resource"
        if not self._coap_server.stopped.isSet():

            timer = threading.Timer(self.period, self.update)
            timer.setDaemon(True)
            timer.start()

            if not first and self._coap_server is not None:
                logger.debug("Periodic Update")
                self._coap_server.notify(self)
                self.observe_count += 1


class LargeResource(Resource):

    def __init__(self, name:Optional[str]="Large", coap_server:Optional[CoAP]=None) -> None:
        super(LargeResource, self).__init__(name, coap_server, visible=True, observable=False, allow_children=False)
        # 2000 bytes
        self.payload = """\
"Me sabbee plenty"—grunted Queequeg, puffing away at his pipe and sitting up in bed.
"You gettee in," he added, motioning to me with his tomahawk, and throwing the clothes to one side. He really did this
in not only a civil but a really kind and charitable way. I stood looking at him a moment. For all his tattooings
he was on the whole a clean, comely looking cannibal. What's all this fuss I have been making about, thought I to
myself—the man's a human being just as I am: he has just as much reason to fear me, as I have to be afraid of him.
Better sleep with a sober cannibal than a drunken Christian.
"Landlord," said I, "tell him to stash his tomahawk there, or pipe, or whatever you call it; tell him to stop smoking,
in short, and I will turn in with him. But I don't fancy having a man smoking in bed with me. It's dangerous. Besides,
I ain't insured."
This being told to Queequeg, he at once complied, and again politely motioned me to get into bed—rolling over to one
side as much as to say—"I won't touch a leg of ye."
"Good night, landlord," said I, "you may go."
I turned in, and never slept better in my life.
Upon waking next morning about daylight, I found Queequeg's arm thrown over me in the most loving and affectionate
manner. You had almost thought I had been his wife. The counterpane was of patchwork, full of odd little
parti-coloured squares and triangles; and this arm of his tattooed all over with an interminable Cretan labyrinth
of a figure, no two parts of which were of one precise shade—owing I suppose to his keeping his arm at sea
unmethodically in sun and shade, his shirt sleeves irregularly rolled up at various times—this same arm of his,
I say, looked for all the world like a strip of that same patchwork quilt. Indeed, partly lying on it as the arm did
 when I first awoke, I could hardly tell it from the quilt, they so blended their hues together; and it was only by
 the sense of weight and pressure that I could tell that Queequeg was hugging"""

    def render_GET(self, request:Request) -> Resource:
        return self


class LargeUpdateResource(Resource):

    def __init__(self, name:Optional[str]="Large", coap_server:Optional[CoAP]=None) -> None:
        super(LargeUpdateResource, self).__init__(name, coap_server, visible=True, observable=False, allow_children=False)
        self.payload = ""

    def render_GET(self, request:Request) -> Resource:
        return self

    def render_PUT(self, request:Request) -> Resource:
        self.payload = request.payload
        return self


class LongResource(Resource):

    def __init__(self, name:Optional[str]="Large", coap_server:Optional[CoAP]=None) -> None:
        super(LongResource, self).__init__(name, coap_server, visible=True, observable=False,
                                                  allow_children=False)
        self.payload = ""

    def render_GET(self, request:Request) -> Resource:
        time.sleep(5)
        return self
