import torch
import numpy as np
from PIL import Image
from torchvision import transforms

from . import data_loader
from .net import load_model


def norm_pred(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)
    return dn


def preprocess(image):
    label_3 = np.zeros(image.shape)
    label = np.zeros(label_3.shape[0:2])

    if 3 == len(label_3.shape):
        label = label_3[:, :, 0]
    elif 2 == len(label_3.shape):
        label = label_3

    if 3 == len(image.shape) and 2 == len(label.shape):
        label = label[:, :, np.newaxis]
    elif 2 == len(image.shape) and 2 == len(label.shape):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]

    transform = transforms.Compose(
        [data_loader.RescaleT(320), data_loader.ToTensorLab(flag=0)]
    )
    sample = transform({"imidx": np.array([0]), "image": image, "label": label})

    return sample


def predict(net, item):
    sample = preprocess(item)

    with torch.no_grad():
        if torch.cuda.is_available():
            inputs_test = torch.cuda.FloatTensor(sample["image"].unsqueeze(0).cuda().float())
        else:
            inputs_test = torch.FloatTensor(sample["image"].unsqueeze(0).float())

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        pred = d1[:, 0, :, :]
        pred_norm = norm_pred(pred).squeeze()
        predict_np = pred_norm.cpu().detach().numpy()
        img = Image.fromarray(predict_np * 255).convert("RGB")

        del d1, d2, d3, d4, d5, d6, d7, pred, pred_norm, predict_np, inputs_test, sample

        return img


def naive_cutout(img, mask):
    empty = Image.new("RGBA", img.size, 0)
    cutout = Image.composite(img, empty, mask.resize(img.size, Image.LANCZOS))
    return cutout


def transparent(input_path, output_path, model_name):
    model = load_model(model_name)

    img = Image.open(input_path).convert("RGB")
    mask = predict(model, np.array(img)).convert("L")

    cutout = naive_cutout(img, mask)
    cutout.save(output_path, format="PNG")
