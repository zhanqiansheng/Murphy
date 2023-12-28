# import os, requests, time
# from xml.etree import ElementTree
#
# # This code is required for Python 2.7
# try:
#     input = raw_input
# except NameError:
#     pass
#
# if 'SPEECH_SERVICE_KEY' in os.environ:
#     subscription_key = os.environ['SPEECH_SERVICE_KEY']
# else:
#     subscription_key = "854b68902a2d42f39acb0b8fb789342d"
#
# class TextToSpeech(object):
#     def __init__(self, subscription_key):
#         self.subscription_key = subscription_key
#         self.tts = None
#         self.timestr = time.strftime("%Y%m%d-%H%M")
#         self.access_token = None
#         self.get_token()
#
#     def get_token(self):
#         # japaneast 换成自己的区域节点
#         fetch_token_url = "https://japaneast.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
#         headers = {
#             'Ocp-Apim-Subscription-Key': self.subscription_key
#         }
#         response = requests.post(fetch_token_url, headers=headers)
#         self.access_token = str(response.text)
#
#     def save_audio(self):
#         # japaneast 换成自己的区域节点
#         base_url = 'https://japaneast.tts.speech.microsoft.com/'
#         path = 'cognitiveservices/v1'
#         constructed_url = base_url + path
#         headers = {
#             'Authorization': 'Bearer ' + self.access_token,
#             'Content-Type': 'application/ssml+xml',
#             'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
#             'User-Agent': 'YOUR_RESOURCE_NAME'
#         }
#         xml_body = ElementTree.Element('speak', version='1.0')
#         xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
#         voice = ElementTree.SubElement(xml_body, 'voice')
#         voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
#         # zh-CN-YunyeNeural、zh-CN-YunxiNeural 是使用什么声音输出，可以看代码最后一行app.get_voices_list()获取节点支持的语音输出类型，填ShortName
#         # voice.set('name', 'zh-CN-YunyeNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
#         voice.set('name',
#                   'zh-CN-XiaoxiaoNeural')  # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
#         voice.text = self.tts
#         body = ElementTree.tostring(xml_body)
#
#         response = requests.post(constructed_url, headers=headers, data=body, stream=True)
#
#         if response.status_code == 200:
#             with open('sample-' + self.timestr + '.wav', 'wb') as audio:
#                 # audio.write(response.content)
#                 for chunk in response.iter_content(chunk_size=128):
#                     audio.write(chunk)
#                 print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
#         else:
#             print("\nStatus code: " + str(
#                 response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
#             print("Reason: " + str(response.reason) + "\n")
#
#     def get_voices_list(self):
#         # japaneast 换成自己的区域节点
#         base_url = 'https://japaneast.tts.speech.microsoft.com/'
#         path = 'cognitiveservices/voices/list'
#         constructed_url = base_url + path
#         headers = {
#             'Authorization': 'Bearer ' + self.access_token,
#         }
#         response = requests.get(constructed_url, headers=headers)
#         if response.status_code == 200:
#             print("\nAvailable voices: \n" + response.text)
#         else:
#             print("\nStatus code: " + str(
#                 response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
#
# async def listen_for_text(app):
#     uri = "'ws://region-31.seetacloud.com:20727/ws/v1/chat/completions"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             response = await websocket.recv()
#             print(f"Received from server: {response}")
#             app.tts = response
#             app.save_audio()
#
# if __name__ == "__main__":
#     subscription_key = os.getenv('SPEECH_SERVICE_KEY', '854b68902a2d42f39acb0b8fb789342d')
#     app = TextToSpeech(subscription_key)
#     asyncio.get_event_loop().run_until_complete(listen_for_text(app))
#








# import os
# import requests
# import time
# from xml.etree import ElementTree
# import asyncio
# import websockets
# from queue import Queue
# import pygame
# import threading
# from queue import PriorityQueue
#
# try:
#     input = raw_input
# except NameError:
#     pass
#
# if 'SPEECH_SERVICE_KEY' in os.environ:
#     subscription_key = os.environ['SPEECH_SERVICE_KEY']
# else:
#     subscription_key = "854b68902a2d42f39acb0b8fb789342d"
#
# class TextToSpeech(object):
#     def __init__(self, subscription_key):
#         self.subscription_key = subscription_key
#         self.tts = None
#         self.audio_counter = 1
#         self.timestr = time.strftime("%Y%m%d-%H%M")
#         self.access_token = None
#         self.get_token()
#         self.accumulated_text = ""
#         self.audio_queue = Queue()
#         self.is_playing = False
#         self.init_audio_playback()
#         self.audio_queue = PriorityQueue()
#         default_audio_file = os.path.join('MP3', '0.wav')
#         self.audio_queue.put((0, default_audio_file))  # 优先级为0
#
#
#     async def maybe_convert_text(self):
#         global text_to_convert
#         punctuation_marks = ["。", "！", "？", "!", ".", "?"]
#
#         # 检查累积文本中是否包含任何标点符号
#         if any(mark in self.accumulated_text for mark in punctuation_marks) or self.accumulated_text.endswith("[DONE]"):
#             # 分割累积文本，直到第一个标点符号
#             for mark in punctuation_marks:
#                 if mark in self.accumulated_text:
#                     split_text = self.accumulated_text.split(mark, 1)
#                     text_to_convert = split_text[0] + mark
#                     self.accumulated_text = split_text[1] if len(split_text) > 1 else ""
#                     break
#
#             # 如果累积文本以 "[DONE]" 结束
#             if self.accumulated_text.endswith("[DONE]"):
#                 self.accumulated_text = self.accumulated_text.replace("[DONE]", "").strip()
#
#             if text_to_convert:
#                 self.tts = text_to_convert.strip()
#                 await self.save_audio()
#
#     def get_token(self):
#         # japaneast 换成自己的区域节点
#         fetch_token_url = "https://japaneast.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
#         headers = {
#             'Ocp-Apim-Subscription-Key': self.subscription_key
#         }
#         response = requests.post(fetch_token_url, headers=headers)
#         self.access_token = str(response.text)
#
#     def init_audio_playback(self):
#         def playback_thread():
#             pygame.mixer.init()
#             while True:
#                 # audio_file_path = self.audio_queue.get()
#                 _, audio_file_path = self.audio_queue.get()
#                 if audio_file_path:
#                     self.is_playing = True
#                     pygame.mixer.music.load(audio_file_path)
#                     pygame.mixer.music.play()
#                     while pygame.mixer.music.get_busy():
#                         time.sleep(0.1)
#                     self.is_playing = False
#
#         thread = threading.Thread(target=playback_thread, daemon=True)
#         thread.start()
#
#     def play_audio(self, audio_file_path):
#         pygame.mixer.init()
#         pygame.mixer.music.load(audio_file_path)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             time.sleep(0.1)
#     async def save_audio(self):
#         # 确保 MP3 目录存在
#         os.makedirs('MP3', exist_ok=True)
#         # 构建音频文件的完整路径
#         audio_file_path = os.path.join('MP3', str(self.audio_counter) + '.wav')
#         self.audio_counter += 1
#         # japaneast 换成自己的区域节点
#         base_url = 'https://japaneast.tts.speech.microsoft.com/'
#         path = 'cognitiveservices/v1'
#         constructed_url = base_url + path
#         headers = {
#             'Authorization': 'Bearer ' + self.access_token,
#             'Content-Type': 'application/ssml+xml',
#             'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
#             'User-Agent': 'YOUR_RESOURCE_NAME'
#         }
#         xml_body = ElementTree.Element('speak', version='1.0')
#         xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
#         voice = ElementTree.SubElement(xml_body, 'voice')
#         voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
#         # zh-CN-YunyeNeural、zh-CN-YunxiNeural 是使用什么声音输出，可以看代码最后一行app.get_voices_list()获取节点支持的语音输出类型，填ShortName
#         # voice.set('name', 'zh-CN-YunyeNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
#         voice.set('name',
#                   'zh-CN-XiaoxiaoNeural')  # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
#         voice.text = self.tts
#         body = ElementTree.tostring(xml_body)
#
#         response = requests.post(constructed_url, headers=headers, data=body, stream=True)
#         priority = self.audio_counter
#         if response.status_code == 200:
#             with open(audio_file_path, 'wb') as audio:
#                 for chunk in response.iter_content(chunk_size=128):
#                     audio.write(chunk)
#             self.audio_queue.put((priority, audio_file_path))
#             # # 确保同一个音频文件不会被重复添加
#             # if not self.is_playing or audio_file_path not in self.audio_queue.queue:
#             #     self.audio_queue.put(audio_file_path)
#         else:
#             print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong.\n")
#
#     def get_voices_list(self):
#         # japaneast 换成自己的区域节点
#         base_url = 'https://japaneast.tts.speech.microsoft.com/'
#         path = 'cognitiveservices/voices/list'
#         constructed_url = base_url + path
#         headers = {
#             'Authorization': 'Bearer ' + self.access_token,
#         }
#         response = requests.get(constructed_url, headers=headers)
#         if response.status_code == 200:
#             print("\nAvailable voices: \n" + response.text)
#         else:
#             print("\nStatus code: " + str(
#                 response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
#
# async def listen_for_text(app):
#     uri = "ws://region-31.seetacloud.com:22234/ws/v1/chat/completions"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             response = await websocket.recv()
#             print(f"Received from server: {response}")
#             app.accumulated_text += response
#             # await app.maybe_convert_text()
#             asyncio.create_task(app.maybe_convert_text())
#
# if __name__ == "__main__":
#     subscription_key = os.getenv('SPEECH_SERVICE_KEY', '854b68902a2d42f39acb0b8fb789342d')
#     app = TextToSpeech(subscription_key)
#     app.init_audio_playback()  # 启动音频播放线程
#     asyncio.get_event_loop().run_until_complete(listen_for_text(app))



import os
import requests
import time
from xml.etree import ElementTree
import asyncio
import websockets
from queue import Queue
import pygame
import threading
from queue import PriorityQueue

try:
    input = raw_input
except NameError:
    pass

if 'SPEECH_SERVICE_KEY' in os.environ:
    subscription_key = os.environ['SPEECH_SERVICE_KEY']
else:
    subscription_key = "854b68902a2d42f39acb0b8fb789342d"

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = None
        self.audio_counter = 1
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.get_token()
        self.accumulated_text = ""
        self.audio_queue = Queue()
        self.is_playing = False
        self.init_audio_playback()
        self.audio_queue = PriorityQueue()
        default_audio_file = os.path.join('MP3', '0.wav')
        self.audio_queue.put((0, default_audio_file))  # 优先级为0


    async def maybe_convert_text(self):
        global text_to_convert
        punctuation_marks = ["。", "！", "？", "!", ".", "?"]

        # 检查累积文本中是否包含任何标点符号
        if any(mark in self.accumulated_text for mark in punctuation_marks) or self.accumulated_text.endswith("[DONE]"):
            # 分割累积文本，直到第一个标点符号
            for mark in punctuation_marks:
                if mark in self.accumulated_text:
                    split_text = self.accumulated_text.split(mark, 1)
                    text_to_convert = split_text[0] + mark
                    self.accumulated_text = split_text[1] if len(split_text) > 1 else ""
                    break

            # 如果累积文本以 "[DONE]" 结束
            if self.accumulated_text.endswith("[DONE]"):
                self.accumulated_text = self.accumulated_text.replace("[DONE]", "").strip()

            if text_to_convert:
                self.tts = text_to_convert.strip()
                await self.save_audio()

    def get_token(self):
        # japaneast 换成自己的区域节点
        fetch_token_url = "https://japaneast.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def init_audio_playback(self):
        def playback_thread():
            pygame.mixer.init()
            while True:
                # audio_file_path = self.audio_queue.get()
                _, audio_file_path = self.audio_queue.get()
                if audio_file_path:
                    self.is_playing = True
                    pygame.mixer.music.load(audio_file_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    self.is_playing = False

        thread = threading.Thread(target=playback_thread, daemon=True)
        thread.start()

    def play_audio(self, audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    async def save_audio(self):
        # 确保 MP3 目录存在
        os.makedirs('MP3', exist_ok=True)
        # 构建音频文件的完整路径
        audio_file_path = os.path.join('MP3', str(self.audio_counter) + '.wav')
        self.audio_counter += 1
        # japaneast 换成自己的区域节点
        base_url = 'https://japaneast.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        # zh-CN-YunyeNeural、zh-CN-YunxiNeural 是使用什么声音输出，可以看代码最后一行app.get_voices_list()获取节点支持的语音输出类型，填ShortName
        # voice.set('name', 'zh-CN-YunyeNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.set('name',
                  'zh-CN-XiaoxiaoNeural')  # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body, stream=True)
        priority = self.audio_counter
        if response.status_code == 200:
            with open(audio_file_path, 'wb') as audio:
                for chunk in response.iter_content(chunk_size=128):
                    audio.write(chunk)
            self.audio_queue.put((priority, audio_file_path))
            # # 确保同一个音频文件不会被重复添加
            # if not self.is_playing or audio_file_path not in self.audio_queue.queue:
            #     self.audio_queue.put(audio_file_path)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong.\n")

    def get_voices_list(self):
        # japaneast 换成自己的区域节点
        base_url = 'https://japaneast.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(
                response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

async def listen_for_text(app):
    uri = "ws://region-3.seetacloud.com:19897/ws/v1/chat/completions"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(f"Received from server: {response}")
            app.accumulated_text += response
            # await app.maybe_convert_text()
            asyncio.create_task(app.maybe_convert_text())

if __name__ == "__main__":
    subscription_key = os.getenv('SPEECH_SERVICE_KEY', '854b68902a2d42f39acb0b8fb789342d')
    app = TextToSpeech(subscription_key)
    app.init_audio_playback()  # 启动音频播放线程
    asyncio.get_event_loop().run_until_complete(listen_for_text(app))