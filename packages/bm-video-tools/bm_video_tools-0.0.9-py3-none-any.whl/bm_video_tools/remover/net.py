import os
import torch
import torch.nn.functional
import numpy as np
from typing import List

from . import u2net

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_model(model_name: str, model_path: str = None):
    if model_name == 'u2netp':
        net = u2net.U2NETP(3, 1)
        path = model_path or os.environ.get(
            "U2NETP_PATH",
            os.path.expanduser(os.path.join("~", ".bm-video-tools", model_name + ".pth")),
        )
    elif model_name == 'u2net':
        net = u2net.U2NET(3, 1)
        path = model_path or os.environ.get(
            "U2NET_PATH",
            os.path.expanduser(os.path.join("~", ".bm-video-tools", model_name + ".pth")),
        )
    elif model_name == 'u2net_human_seg':
        net = u2net.U2NET(3, 1)
        path = model_path or os.environ.get(
            "U2NETH_PATH",
            os.path.expanduser(os.path.join("~", ".bm-video-tools", model_name + ".pth")),
        )
    else:
        raise ValueError('model name must be one of u2netp, u2net, u2net_human_seg')

    if not os.path.exists(path):
        raise ValueError(f'{path} does not exist')

    print(f"current device: {DEVICE}")
    net.load_state_dict(torch.load(path, map_location=torch.device(DEVICE)))
    net.to(device=DEVICE, dtype=torch.float32, non_blocking=True)
    net.eval()
    return net


class Net(torch.nn.Module):
    def __init__(self, model_name, model_path=None):
        super(Net, self).__init__()
        net = load_model(model_name, model_path)
        self.net = net

    def forward(self, block_input: torch.Tensor):
        image_data = block_input.permute(0, 3, 1, 2)
        original_shape = image_data.shape[2:]
        image_data = torch.nn.functional.interpolate(image_data, (320, 320), mode='bilinear')
        image_data = (image_data / 255 - 0.485) / 0.229
        out = self.net(image_data)[0][:, 0:1]
        ma = torch.max(out)
        mi = torch.min(out)
        out = (out - mi) / (ma - mi) * 255
        out = torch.nn.functional.interpolate(out, original_shape, mode='bilinear')
        out = out[:, 0]
        out = out.to(dtype=torch.uint8, device=torch.device('cpu'), non_blocking=True).detach()
        return out


@torch.no_grad()
def remove_many(image_data: List[np.array], net: Net):
    image_data = np.stack(image_data)
    image_data = torch.as_tensor(image_data, dtype=torch.float32, device=DEVICE)
    return net(image_data).numpy()
