import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token
import requests
import json
import os
import random
from denoiser.SSFilter import SSFilter

REQUEST_STATUS_CODE = 200
mp3 = "denoiser/audio/{}.mp3"

class DenoiserBotError(Exception):
    def __init__(self, message=None):
        self.message = message

class DenoiserBot(object):
    def __init__(self, token, denoiser):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)
        self.denoiser = denoiser

    def send_text_message(self, user_id, message):
        """ Send text message.
        :param user_id: user id
        :param message: message
        :return message id
        """
        return self.vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': random.randint(0, 10000)})

    def send_audio_message(self, user_id, owner_id, audio_id):
        """ Send message with audio attachment.
        :param user_id: user id
        :param owner_id: audio owner id
        :param audio_id: audio id
        :return message id
        """
        attach = 'doc{}_{}'.format(owner_id, audio_id)
        return self.vk.method('messages.send',
                              {'user_id': user_id,
                               'attachment': attach,
                               'random_id': random.randint(0, 10000)})

    def get_upload_url(self, peer_id, type='audio_message'):
        """ Get upload server url to load attachments for messages.
        :param peer_id: peer id
        :param type: type of attachment
        :return url to upload files
        """
        return self.vk.method('docs.getMessagesUploadServer',
                                 {'type': type,
                                  'peer_id': peer_id})['upload_url']

    def save_doc(self, file, title):
        """ Save document on server.
        :param file: result of uploading file
        :param title: title of document
        :return: array of information about uploaded documents
        """
        return self.vk.method('docs.save',
                              {'file': file,
                               'title': title})

    def get_message(self, message_id):
        """ Get message by id.
        :param message_id: message id
        :return: message
        """
        return self.vk.method('messages.getById',
                              {'message_ids': message_id})

    def download_audio(self, audio_id, audio_url):
        """ Download audio from given url.
        :param audio_id: audio id
        :param audio_url: url to download audio from
        """
        r = requests.get(audio_url)
        if r.status_code == REQUEST_STATUS_CODE:
            mp3_file = mp3.format(audio_id)
            with open(mp3_file, 'wb') as file:
                file.write(r.content)
        else:
            raise DenoiserBotError("Error in download_audio get request {}. "
                                   "{} status code.".format(audio_url, r.status_code))

    def upload_audio(self, audio_id, peer_id):
        """ Upload audio to server.
        :param audio_id: audio id
        :param peer_id: peer id
        :return: document with information about saved audio
        """
        mp3_file = mp3.format('d' + audio_id)
        audio = {'file': (mp3_file, open(mp3_file, 'rb'))}
        upload_url = self.get_upload_url(peer_id)
        r = requests.post(upload_url, files=audio)
        if r.status_code == REQUEST_STATUS_CODE:
            result = json.loads(r.text)['file']
            saved = self.save_doc(result, mp3_file)
            return saved
        else:
            raise DenoiserBotError("Error in upload_audio post request {}. "
                                   "{} status code.".format(upload_url + "?files='{}'".format(audio), r.status_code))

    def denoise_audio(self, audio_id):
        """ Denoise audio with given id.
        :param audio_id: audio id
        """
        mp3_file = mp3.format(audio_id)
        denoised_mp3_file = mp3.format('d'  + audio_id)
        try:
            self.denoiser.run(mp3_file, denoised_mp3_file, 'mp3')
        except FileNotFoundError as e:
            raise DenoiserBotError("FileNotFoundError {} while denoising audio".format(e.filename))

    def clear(self, audio_id):
        """ Clear directory from unused files.
        :param audio_id: audio id
        """
        mp3_file = mp3.format(audio_id)
        d_mp3_file = mp3.format('d'  + audio_id)
        os.system("rm -R {}".format(mp3_file))
        os.system("rm -R {}".format(d_mp3_file))

    def run(self):
        """ Listen to message and reply to them."""
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    user_id = event.user_id
                    if request == "hi":
                        self.send_text_message(user_id, "hi!!!")
                    elif request == "help":
                        self.send_text_message(user_id, "Attach audio message to denoise it.\n"
                                          "In the beginning of the audio message leave 2-3 second clear to record noise.")
                    else:
                        try:
                            msg = self.get_message(event.message_id)
                            for item in msg['items']:
                                if 'attachments' in item:
                                    for attach in item['attachments']:
                                        if 'audio_message' in attach:
                                            audio_id = str(attach['audio_message']['id'])
                                            audio_url = attach['audio_message']['link_mp3']
                                            self.download_audio(audio_id, audio_url)
                                            self.denoise_audio(audio_id)
                                            doc = self.upload_audio(audio_id, user_id)
                                            self.send_audio_message(user_id, doc['audio_message']['owner_id'], doc['audio_message']['id'])
                                            self.clear(audio_id)
                        except DenoiserBotError as e:
                            self.send_text_message(user_id, "Sorry, an error occurred!!!")

if __name__ == '__main__':
    denoiser = SSFilter()
    bot = DenoiserBot(token, denoiser)
    bot.run()

