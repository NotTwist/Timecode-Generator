import os.path

from src.scene_changes import scene_change_detector
from src.video_reader import read_video
from src.video_downloader import download_video
from src.write_chapters import convert_frames, save_timecodes

if __name__ == "__main__":
    url = input("Input youtube url: ")
    save_path = "../temp/"
    out_path = "../output/"
    video_path, fps, name = download_video(url, save_path)
    frames = read_video(video_path)
    print("Analyzing for scene changes")
    scene_changes, _, _, _ = scene_change_detector(frames)
    timecodes = convert_frames(scene_changes, fps)
    print("Timecodes for scene changes:")
    print(*timecodes, sep='\n')
    save_timecodes(timecodes, os.path.join(out_path, name+ "_timecode"+".txt"))
    print("Timecodes saved in output directory")
    os.remove(video_path)

