"""
    Utility functions for loading weights.
"""

import gdown

MODEL_WEIGHTS = {
    "L": "1Gh32arzhW06C1ZJyzcJSSfdJDi3RgWoG",
    "S": "1pSQruQyg8KJq6VmzhMLFbT_VaHJMdlWF",
}


def download_weights(checkpoint_fpath, model_size="L"):
    """
    Downloads weights from Google Drive.
    """

    download_id = MODEL_WEIGHTS[model_size.strip().upper()]

    gdown.download(
        f"https://drive.google.com/uc?id={download_id}", checkpoint_fpath, quiet=False
    )
