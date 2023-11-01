from .deep_to import *
from .device import *
from .to import *


def get_torch_info():
    torch_flag_list = [
        "torch.backends.cuda.is_built",
        "torch.backends.cuda.matmul.allow_tf32",
        "torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction",
        "torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction",
        "torch.backends.cudnn.allow_tf32",
        "torch.backends.cudnn.benchmark",
    ]
    torch_info = {}
    for flag in torch_flag_list:
        value = eval(flag)  # pylint: disable=eval-used
        if callable(value):
            torch_info[flag] = value()
        else:
            torch_info[flag] = value
    return torch_info
