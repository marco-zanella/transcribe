from google.cloud import speech_v1
from google.cloud import storage

class GoogleCloud:
    def __init__(self, key_path, bucket):
        self.key_path = key_path
        self.bucket = bucket
        self.language = 'it-IT'
        self.storage_client = storage.Client.from_service_account_json(self.key_path)
        self.speech_client = speech_v1.SpeechClient.from_service_account_json(self.key_path)

    def getRemoteFilename(self):
        return '_transcribe_tmp.flac'

    def getRemoteUri(self):
        return 'gs://' + self.bucket + '/' + self.getRemoteFilename()

    def upload(self, audio_file):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(self.getRemoteFilename())
        blob.upload_from_filename(audio_file)

    def deleteRemote(self):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(self.getRemoteFilename())
        blob.delete()

    def convert(self, audio_file):
        self.upload(audio_file)
        config = {
            "language_code": self.language,
            "enable_automatic_punctuation": True
        }
        audio = {"uri": self.getRemoteUri()}
        operation = self.speech_client.long_running_recognize(config=config, audio=audio)
        response = operation.result()
        content = ' '.join(map(lambda result: result.alternatives[0].transcript, response.results))
        self.deleteRemote()
        return content
