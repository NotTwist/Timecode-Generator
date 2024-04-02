def frame_to_time(frame, fps):
    seconds = frame / fps
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return shorten_timecode('{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds)))


def shorten_timecode(timecode):
    components = timecode.split(":")
    hour, minute, second = map(int, components)
    if hour == 0:
        return '{:02d}:{:02d}'.format(minute, second)
    return '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)


def convert_frames(frames, fps):
    return sorted(list(set([frame_to_time(frame, fps) for frame in frames])))


def save_timecodes(timecodes, out_path):
    with open(out_path, 'w') as file:
        for timecode in timecodes:
            file.write(timecode + '\n')
#
# if __name__=="__main__":
#     print(shorten_timecode("00:00:01"))
