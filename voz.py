import speech_recognition as sr

def ouvir_sintomas() -> str:
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        reconhecedor.adjust_for_ambient_noise(fonte, duration=1)
        print("🎙️ Fale seus sintomas... (aguardando até silêncio)")

        try:
            audio = reconhecedor.listen(fonte, timeout=5)  # ouça até a pessoa parar
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"📝 Texto reconhecido: {texto}")
            return texto.lower().strip()
        except sr.WaitTimeoutError:
            print("⏱️ Tempo de espera esgotado (ninguém falou).")
            return ""
        except sr.UnknownValueError:
            print("❌ Não foi possível entender o áudio.")
            return ""
        except sr.RequestError:
            print("⚠️ Erro ao acessar o serviço de reconhecimento.")
            return ""
