import copy
import ctypes

import torch


# credit
# https://github.com/pyro-ppl/pyro/blob/beddc1f1a193d7f03bd588c9d6afe389bbd2d10c/pyro/distributions/util.py
class _DeepToMemo(dict):
    def __init__(self, to_args, to_kwargs):
        super().__init__()
        self._to_args = to_args
        self._to_kwargs = to_kwargs

    def get(self, key, default=None):
        result = super().get(key, default)
        if result is default:
            # Assume key is the id of another object, and look up that object.
            old = ctypes.cast(key, ctypes.py_object).value
            if isinstance(
                old, (torch.Tensor, torch.nn.Module)
            ):  # or maybe duck type here?
                self[key] = result = old.to(*self._to_args, **self._to_kwargs)
        return result


def deep_to(obj, *args, **kwargs):
    r"""
    Create a deep copy of an arbitrary Python object, calling ``.to(*args,
    **kwargs)`` on all :class:`torch.Tensor` s and :class:`torch.nn.Module` s
    in that object.

    Like :meth:`torch.Tensor.to` but unlike :meth:`torch.nn.Module.to`, this
    creates new objects. For compatibility with existing PyTorch module
    behavior, this first calls :meth:`torch.nn.Module.to` in-place, then
    creates a deep copy of the module.

    :param obj: Any python object.
    :param \*args:
    :param \*\*kwargs: See :meth:`torch.Tensor.to`.
    :returns: A deep copy of ``obj`` with all :class:`torch.Tensor` s and
        :class:`torch.nn.Module` s mapped.
    """
    memo = _DeepToMemo(args, kwargs)
    return copy.deepcopy(obj, memo)
