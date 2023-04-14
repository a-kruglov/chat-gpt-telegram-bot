import os
import uuid
import openai
import telebot
import pydub
from config import AUDIOS_DIR


class VoiceRecogniser:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    @staticmethod
    def generate_unique_filename():
        uuid_value = uuid.uuid4()
        return f"{str(uuid_value)}"

    @staticmethod
    def convert_speech_to_text(audio_filepath):
        with open(audio_filepath, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)
            return transcript["text"]

    def download_voice_as_ogg(self, voice):
        voice_file = self.bot.get_file(voice.file_id)
        downloaded_file = self.bot.download_file(voice_file.file_path)
        filename = self.generate_unique_filename()
        ogg_filepath = os.path.join(AUDIOS_DIR, f"{filename}.ogg")
        with open(ogg_filepath, 'wb') as new_file:
            new_file.write(downloaded_file)
        return ogg_filepath

    def convert_ogg_to_mp3(self, ogg_filepath):
        filename = self.generate_unique_filename()
        mp3_filepath = os.path.join(AUDIOS_DIR, f"{filename}.mp3")
        audio = pydub.AudioSegment.from_file(ogg_filepath, format="ogg")
        audio.export(mp3_filepath, format="mp3")
        return mp3_filepath

    def covert_voice_to_text(self, message: telebot.types.Message):
        ogg_filepath = self.download_voice_as_ogg(message.voice)
        mp3_filepath = self.convert_ogg_to_mp3(ogg_filepath)
        text = self.convert_speech_to_text(mp3_filepath)
        os.remove(ogg_filepath)
        os.remove(mp3_filepath)
        return text
