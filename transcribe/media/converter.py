import magic
import moviepy.editor as mp
import time

class SimpleConverter:
    def __init__(self):
        self.codec = 'flac'
        self.fps = 24000

    def setCodec(self, codec):
        self.code = codec
        return self

    def setFps(self, fps):
        self.fps = fps
        return self

    def convert(self, source, destination):
        file_mime = magic.Magic(mime=True).from_file(source)
        if file_mime.find('video') != -1:
            clip = mp.VideoFileClip(source).audio
        elif file_mime.find('audio') != -1:
            clip = mp.AudioFileClip(source)
        else:
            raise Exception("Please, select audio or video file")
        clip.write_audiofile(destination, codec=self.codec, fps=self.fps, ffmpeg_params=["-ac", "1"], verbose=False, logger=None)
