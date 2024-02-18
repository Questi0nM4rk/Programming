import assemblyai as aai
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_KEY = getenv('API_KEY')

aai.settings.api_key = API_KEY
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("D:\\vscode_stuff\Programming\Python\speechToText\sound.mp3")

print(transcript.text)
