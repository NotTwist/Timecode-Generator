import numpy as np


def frame_to_time(frame, fps):
    seconds = int(frame[0]) / fps
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return shorten_timecode('{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds)))+' '+frame[1]


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
if __name__ == "__main__":
    array = np.array([['246', 'Man with glasses and a beard is reading a book.'],
                      ['573', 'Man holding a baby in a field.'],
                      ['783', 'Man with glasses and a white shirt with a black stripe on it.'],
                      ['1001', 'Man in a black shirt is holding a beer bottle and smiling.'],
                      ['1205', 'Man in a blue shirt is holding a blue cup.'],
                      ['1414',
                       'Man in a black shirt with a white shirt and blue jeans is talking to a woman in a black shirt.'],
                      ['1648', 'Man in a blue shirt and black hat playing baseball.'],
                      ['2127',
                       'Man holding a baby in a pink shirt and a woman holding a baby in a blue shirt.'],
                      ['2370', 'Man in a blue shirt and sunglasses is looking at something.'],
                      ['2682',
                       'Man with sunglasses and a red shirt is standing in the middle of a field.'],
                      ['2979', 'Man with a white shirt and glasses is eating a snack.'],
                      ['3200',
                       'Man in a blue shirt with a white hat and sunglasses is holding a beer.'],
                      ['3282', 'Man in a blue shirt is sitting at a desk with a computer.'],
                      ['3561', 'Man with glasses and a red shirt is playing with a toy.']])
    print(convert_frames(array, 30))
