import os


from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id)


def combine_transcripts(transcript, timecodes):
    combined_transcripts = {}
    j = 0
    for i, timecode in enumerate(timecodes):
        # TODO: convert mm:ss to numbers or the other way
        while timecodes[i] <= int(transcript[j]["start"]) < timecodes[i + 1]:
            combined_transcripts[timecodes[i]].append(transcript[j]["text"])
            j += 1


if __name__ == "__main__":
    print(get_transcript('p69qUVs45tc'))
