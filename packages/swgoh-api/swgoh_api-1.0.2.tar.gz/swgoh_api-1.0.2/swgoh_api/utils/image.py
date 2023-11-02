import os


def save_image(img, path, name):
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{name}", "wb") as f:
        f.write(img)
