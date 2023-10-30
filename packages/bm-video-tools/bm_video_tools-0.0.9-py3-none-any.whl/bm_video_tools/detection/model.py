import os


def load_model(model_name) -> str:
    model_path = os.path.expanduser(os.path.join("~", ".bm-video-tools", model_name + ".xml"))
    if not os.path.exists(model_path):
        raise ValueError(f'{model_path} does not exist')
    return model_path
