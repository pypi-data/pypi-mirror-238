"""
"""
from __future__ import annotations

import warnings

from gradio.context import LocalContext
from gradio.helpers import TrackedIterable
from gradio.queueing import Queue
from typing_extensions import assert_type

from ..utils import SimpleQueue
from .types import GeneratorResQueueResult
from .types import GradioQueueEvent
from .types import RegularResQueueResult


QUEUE_RPC_METHODS = [
    "set_progress",
    "log_message",
]


def get_queue_instance():
    blocks = LocalContext.blocks.get()
    if blocks is None: # pragma: no cover
        return None
    return blocks._queue


def try_process_queue_event(method_name: str, *args, **kwargs):
    queue = get_queue_instance()
    if queue is None: # pragma: no cover
        warnings.warn("ZeroGPU: Cannot get Gradio app Queue instance")
        return
    method = getattr(queue, method_name, None)
    assert callable(method)
    method(*args, **kwargs)


def patch_gradio_queue(
    res_queue: SimpleQueue[RegularResQueueResult] | SimpleQueue[GeneratorResQueueResult],
):

    def rpc_method(method_name: str):
        def method(*args, **kwargs):
            if args and isinstance(args[0], Queue):
                args = args[1:] # drop `self`
            res_queue.put(GradioQueueEvent(method_name, args, kwargs))
        return method

    for method_name in QUEUE_RPC_METHODS:
        if (method := getattr(Queue, method_name, None)) is None: # pragma: no cover
            warnings.warn(f"ZeroGPU: Gradio Queue has no {method_name} attribute")
            continue
        if not callable(method): # pragma: no cover
            warnings.warn(f"ZeroGPU: Gradio Queue {method_name} is not callable")
            continue
        setattr(Queue, method_name, rpc_method(method_name))

    TrackedIterable.__reduce__ = tracked_iterable__reduce__


def tracked_iterable__reduce__(self):
    res: tuple = super(TrackedIterable, self).__reduce__() # type: ignore
    cls, base, state, *_ = res
    return cls, base,{**state, **{
        'iterable': None,
        '_tqdm': None,
    }}
