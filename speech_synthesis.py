import pyttsx3

def speak_text(text):
    """
    テキストを音声で再生します。
    :param text: 読み上げる文字列
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text = "こんにちは。これが音声応答のテストです。"
    speak_text(text)
