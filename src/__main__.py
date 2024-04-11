import os.path

import numpy as np

from src.description_generator import get_description
from src.scene_changes import scene_change_detector
from src.video_reader import read_video
from src.video_downloader import download_video
from src.write_chapters import convert_frames, save_timecodes
from tqdm.auto import tqdm
if __name__ == "__main__":
    url = input("Input youtube url: ")
    save_path = "../temp/"
    out_path = "../output/"
    video_path, fps, name, video_id = download_video(url, save_path)
    frames = read_video(video_path)
    print("Analyzing for scene changes")
    scene_changes, scene_changes_frames = scene_change_detector(frames)
    descriptions = []
    for frame in tqdm(scene_changes_frames):
        description = get_description(frame)
        # print(description)
        descriptions.append(description)
    timecodes = np.column_stack((np.array(scene_changes), np.array(descriptions)))
    # print(timecodes)
    timecodes = convert_frames(timecodes, fps)
    print("Timecodes for scene changes:")
    print(*timecodes, sep='\n')
    save_timecodes(timecodes, os.path.join(out_path, name + "_timecode" + ".txt"))
    print("Timecodes saved in output directory")
    os.remove(video_path)
