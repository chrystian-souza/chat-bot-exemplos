import speech_recognition as sr
import pyttsx3
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Criação do chatbotsisim
chatbot = ChatBot("MeuBot")
trainer = ListTrainer(chatbot)

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

def get_user_feedback(text, response):
    """Solicita feedback do usuário e armazena a resposta correta para treinamento."""
    engine = pyttsx3.init()
    engine.say("Esta resposta foi útil?")
    engine.runAndWait()
    feedback = input("Esta resposta foi útil? (Sim/Não): ")
    if feedback.lower() == 'não':
        engine.say("Por favor, digite qual seria a resposta correta.")
        engine.runAndWait()
        correct_response = input("Qual seria a resposta correta?: ")
        store_feedback(text, correct_response)
        print("Obrigado pelo seu feedback! Vou aprender com isso.")

def store_feedback(question, correct_response):
    """Armazena o par pergunta e resposta correta para treinamento posterior."""
    with open("feedback_data.txt", "a") as file:
        file.write(f"{question} | {correct_response}\n")
    trainer.train([question, correct_response])  # Treina o bot imediatamente com o novo par

def chatbot_response(text):
    """Processa o texto do usuário e gera uma resposta com o ChatterBot."""
    if text:
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

    response = chatbot_response(user_text)
    synthesize_speech(response)
    if response:
        get_user_feedback(user_text, response)
