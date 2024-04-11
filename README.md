# Timecode Generator
## Automate Youtube descriptions
A python script designed to automate the process of creating chapters in YouTube videos by detecting scene changes and cuts. It works by downloading the video from a YouTube link, then using a heuristic scene change detector it finds all cuts in the video and saves timecodes in a /output directory.
## Generate chapter names
The script also has a simple chapter name generation based on the image after scene change. It uses [this](https://github.com/jmisilo/clip-gpt-captioning) small model based on OpenAI's CLIP and GPT-2 to generate a simple description for an image.
## Usage
* Have Python 3 installed
* Download model from [here](https://drive.google.com/file/d/1Gh32arzhW06C1ZJyzcJSSfdJDi3RgWoG/view?usp=sharing) and paste next to predict.py inside `src/clip_gpt_captioning/src/`
* Install requirements: `pip install -r requirements.txt`
* run \_\_main__.py
* Paste link to a video
* Timecodes and descriptions will be saved in output directory
## Example
Using this [example video](https://www.youtube.com/watch?v=kOBHegu6KoU):

1. `Timecode: 00:19 Man holding a baby in a field.`
![Example 1](example1.jpeg)

## Notes
1. Scene detection is not perfect, especially with motion graphics. It works best for traditional videos with camera.
2. YouTube requires chapters be at least 10 seconds long. If scene changes happen quickly, chapter length might be shorter than expected. So you have to delete unneeded timecodes (which you will probably do anyway, as scenes are not a perfect way to identify chapters)
3. This program doesn't account for audio and uses only the difference between frames to find cuts. It is best to be used as a first step to creating chapters, then cleaning them from unneeded timecodes add maybe adding additional. 
