import os
from media.converter import SimpleConverter as MediaConverter
from text.docx import Docx
from speech_to_text.google_cloud import GoogleCloud as SpeechToText
from view.window import Window

def transcribe(config):
    media_converter = MediaConverter()
    speech_to_text = SpeechToText(config['google_cloud']['key_path'], config['google_cloud']['bucket'])
    docx = Docx()

    window = Window(media_converter, speech_to_text, docx, config['paths']['output_directory'])
    window.show()
