import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from config import token
import requests
import json
import os
import random
from denoiser.spectral_subtraction import SSFilter

REQUEST_STATUS_CODE = 200

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)
denoiser = SSFilter()
mp3 = "denoiser/audio/{}.mp3"


def send_msg(user_id, message):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': random.randint(0, 10000)})


def send_audio(user_id, msg):
    attach = 'doc%s_%s' % (msg['audio_message']['owner_id'], msg['audio_message']['id'])
    vk.method('messages.send',
              {'user_id': user_id,
               'attachment': attach,
               'random_id': random.randint(0, 10000)})


def download_audio(audio_id, audio_url):
    r = requests.get(audio_url)
    if r.status_code == REQUEST_STATUS_CODE:
        mp3_file = mp3.format(audio_id)
        with open(mp3_file, 'wb') as file:
            file.write(r.content)


def upload_audio(audio_id, peer_id):
    mp3_file = mp3.format('d' + audio_id)
    audio = {'file': (mp3_file, open(mp3_file, 'rb'))}
    upload_url = vk.method('docs.getMessagesUploadServer', {'type': 'audio_message', 'peer_id': peer_id})['upload_url']
    upload = requests.post(upload_url, files=audio)
    result = json.loads(upload.text)['file']
    saved = vk.method('docs.save', {'file': result, 'title': mp3_file})
    return saved


def denoise_audio(audio_id):
    mp3_file = mp3.format(audio_id)
    denosed_mp3_file = mp3.format('d'  + audio_id)
    denoiser.run(mp3_file, denosed_mp3_file, 'mp3')


def clear_file(audio_id):
    mp3_file = mp3.format(audio_id)
    d_mp3_file = mp3.format('d'  + audio_id)
    os.system("rm -R {}".format(mp3_file))
    os.system("rm -R {}".format(d_mp3_file))


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            user_id = event.user_id
            if request == "hi":
                send_msg(user_id, "hi!!!")
            elif request == "help":
                send_msg(user_id, "Attach audio message to denoise it.\n"
                                  "In the beginning of the audio message leave 2-3 second clear to record noise.")
            else:
                msg_id = event.message_id
                msg = vk.method('messages.getById', {'message_ids': msg_id})

                for item in msg['items']:
                    if 'attachments' in item:
                        for attach in item['attachments']:
                            if 'audio_message' in attach:
                                audio_id = str(attach['audio_message']['id'])
                                audio_url = attach['audio_message']['link_mp3']
                                download_audio(audio_id, audio_url)
                                denoise_audio(audio_id)
                                audio_doc = upload_audio(audio_id, user_id)
                                send_audio(user_id, audio_doc)
                                clear_file(audio_id)
