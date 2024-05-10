import speech_recognition as sr
import pyttsx3
from chatterbot import ChatBot



# Criação e configuração do chatbot
chatbot = ChatBot("MeuBot")

# Função para reconhecer fala
def recognize_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", text)
        return text
    except sr.UnknownValueError:
        print("Não consegui entender.")
        return None
    except sr.RequestError as e:
        print("Houve um erro:", e)
        return None

# Função para processar a resposta do chatbot
def chatbot_response(text):
    if text:  # Certifique-se de que o texto não é None ou vazio
        response = chatbot.get_response(text)
        return response.text
    else:
        return "Desculpe, não entendi. Pode repetir, por favor?"

# Função para sintetizar texto em fala
def synthesize_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'portuguese' in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say("Bot: " + text)
    engine.runAndWait()
    return text

# Texto informativo inicial para o usuário
def initial_prompt():
    engine = pyttsx3.init()
    engine.say("Olá, por favor comece a falar para interagir comigo.")
    engine.runAndWait()
    print("Olá, por favor comece a falar para interagir comigo.")

# Loop principal do chatbot
initial_prompt()  # Chama o prompt inicial antes de entrar no loop
while True:
    user_text = recognize_speech()
    if user_text and user_text.lower() == 'finalizar':
        synthesize_speech('Tchau! Até logo.')
        break
    chatbot_response_text = chatbot_response(user_text)
    synthesize_speech(chatbot_response_text)


