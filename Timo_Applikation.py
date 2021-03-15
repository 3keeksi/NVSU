# speech to text nimmt audio file --> translated es in eine bestimmte sprache --> analysed es noch
import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3
from ibm_watson import ToneAnalyzerV3

authenticator = IAMAuthenticator(
    '8UCAgypR-tazqwu-qbsRCFPR1LXZaARjozXmWfTLrljp')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(
    'https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/2d0e63eb-af1f-40da-b460-2d79f0512e0b')

with open(join(dirname(__file__), './.', 'audio-file2.flac'),
          'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/flac',
    ).get_result()
textFromAudio = speech_recognition_results.__str__().split('{')[3].split('}')[0].split('\',')[0].split(':')[1].replace('\'', '').strip()
print(textFromAudio)

print("Geben Sie die Sprache ein in die Sie übersetzen wollen (von-zu): ")
languageToTranslateTo = input()

authenticator = IAMAuthenticator(
    'YqreNfgTltnFZc7hPkpy24VjZwXmq_xx9Jme73R_6dpa')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(
    'https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/b1f37d3c-7774-421e-844f-9a3f1c189369')

translation = language_translator.translate(
    text=textFromAudio,
    model_id=languageToTranslateTo).get_result()
textTranslated = translation.__str__().split('{')[2].split('}')[0].split(':')[1].replace('\'', '').strip()
print(textTranslated)

authenticator = IAMAuthenticator(
    'fAzrt6CXh8aZN2KA8zEMmj8wanU-J73ATmvE9jO-y7hp')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url(
    'https://api.eu-de.tone-analyzer.watson.cloud.ibm.com/instances/2588bf17-6b9a-4034-b2da-5b2a0345f65c')

tone_analysis = tone_analyzer.tone(
    {'text': textTranslated},
    content_type='application/json'
).get_result()
print(json.dumps(tone_analysis, indent=2))