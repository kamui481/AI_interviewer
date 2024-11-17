import whisper

def transcribe_audio(file_path):
    """
    音声ファイルを文字起こしします。
    :param file_path: 音声ファイルのパス
    :return: 文字起こし結果
    """
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    audio_file = "audio_file.wav"  # サンプル音声ファイル
    transcription = transcribe_audio(audio_file)
    print(f"文字起こし結果: {transcription}")
