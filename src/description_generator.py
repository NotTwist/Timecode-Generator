from src.clip_gpt_captioning.src.predict import predict_description


def get_description(image):
    return predict_description(image)
