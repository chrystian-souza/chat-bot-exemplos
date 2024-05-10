import speech_recognition as sr
import pyttsx3
from chatterbot import ChatBot

# Criação do chatbot
chatbot = ChatBot("MeuBot")

def recognize_speech():
    """Captura a entrada de áudio do microfone, converte em texto e retorna."""
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

def get_user_feedback(text):
    """Solicita feedback do usuário e imprime uma mensagem de agradecimento."""
    engine = pyttsx3.init()
    engine.say("Esta resposta foi útil?")
    engine.runAndWait()
    feedback = input("Esta resposta foi útil? (Sim/Não): ")
    if feedback.lower() == 'não':
        engine.say("Por favor, digite qual seria a resposta correta.")
        engine.runAndWait()
        correct_response = input("Qual seria a resposta correta?: ")
        # Aqui, você poderia adicionar o processo para ajustar o treinamento do bot.
        print("Obrigado pelo seu feedback! Vou aprender com isso.")

def chatbot_response(text):
    """Processa o texto do usuário e gera uma resposta com o ChatterBot."""
    if text:  # Certifique-se de que o texto não é None ou vazio
        response = chatbot.get_response(text)
        return response.text
    else:
        return "Desculpe, não entendi. Pode repetir, por favor?"

def synthesize_speech(text):
    """Converte o texto em fala e reproduz pelos alto-falantes."""
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

while True:
    user_text = recognize_speech()
    if user_text and user_text.lower() == 'finalizar':
        synthesize_speech('Tchau! Até logo.')
        break

    chatbot_response_text = chatbot_response(user_text)
    spoken_text = synthesize_speech(chatbot_response_text)
    if spoken_text:
        get_user_feedback(spoken_text)


