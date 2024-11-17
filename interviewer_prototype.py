import os
import openai
from scoring_logic import calculate_scores
from speech_synthesis import speak_text  # 音声応答関数をインポート
from voice_recognition import transcribe_audio  # 音声認識関数（別ファイルに実装済み）
import speech_recognition as sr
from gtts import gTTS

# 環境変数からAPIキーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を確認してください。")

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("音声入力中です... 話してください。")
        try:
            audio = recognizer.listen(source, timeout=10)
            print("音声を処理中...")
            text = recognizer.recognize_google(audio, language="ja-JP")
            print(f"音声入力結果: {text}")
            return text
        except sr.WaitTimeoutError:
            print("音声入力がタイムアウトしました。")
            return None
        except sr.UnknownValueError:
            print("音声を認識できませんでした。")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition サービスへの接続でエラーが発生しました: {e}")
            return None

def get_ai_question(previous_answer=None, is_first_question=False):
    """
    AIが自動で次の質問を生成します。
    :param previous_answer: 前回の回答（次の質問に反映可能）
    :param is_first_question: 最初の質問かどうか
    :return: AIが生成した質問
    """
    try:
        # 最初の質問を生成
        if is_first_question:
            messages = [
                {"role": "system", "content": "あなたは日本語を話すAI面接官です。"},
                {"role": "user", "content": "最初の質問をお願いします。"}
            ]
        else:
            # 以降の質問は回答に基づく
            messages = [
                {"role": "system", "content": "あなたは日本語を話すAI面接官です。1回の応答で1つの質問だけを生成してください。"},
                {"role": "user", "content": f"前回の回答: {previous_answer}"}
            ]

        # ChatCompletion API の呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または "gpt-4"
            messages=messages
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"AIとの通信中にエラーが発生しました: {str(e)}"

def speak_text_jp(text):
    """
    日本語のテキストを音声で再生します。
    """
    try:
        tts = gTTS(text=text, lang='ja')
        tts.save("output.mp3")
        os.system("start output.mp3")
    except Exception as e:
        print(f"音声合成に失敗しました: {e}")

def main():
    print("AI面接官: 質問と回答を日本語で行います。終了するには '終了' と言ってください。\n")

    # 最初の質問を取得
    question = get_ai_question(is_first_question=True)
    print(f"AIの質問: {question}")
    speak_text_jp(question)

    previous_answer = None

    while True:
        user_answer = transcribe_audio()

        if user_answer is None:
            print("音声が認識されませんでした。もう一度試してください。")
            continue

        if user_answer.lower() in ["終了", "終わり", "quit", "exit"]:
            print("面接を終了します。お疲れさまでした！")
            speak_text_jp("面接を終了します。お疲れさまでした。")
            break

        # 次の質問を生成
        question = get_ai_question(previous_answer=user_answer)
        print(f"AIの質問: {question}")
        speak_text_jp(question)
        previous_answer = user_answer

if __name__ == "__main__":
    main()
