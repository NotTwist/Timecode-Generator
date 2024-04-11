import os.path

from pytube import YouTube


def download_video(url, save_path='./'):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        print("Downloading: \"" + video.title + "\" with quality " + video.resolution)
        video_path = video.download(output_path=save_path)
        print("Downloading finished successfully")
        return video_path, video.fps, video.title, yt.video_id
    except Exception as e:
        print("An error occurred during downloading: ", str(e))
