import whisper

# 加载 Whisper 模型
model = whisper.load_model("small")

while True:
    # 获取用户输入的音频文件路径
    audio_file_path = input("请输入音频文件路径，或输入 'exit' 退出: ")

    # 检查是否退出
    if audio_file_path.lower() == 'exit':
        break

    try:
        prompt = '以下是普通话的句子'

        # 使用 Whisper 模型进行音频转录
        result = model.transcribe(audio_file_path, language='zh', verbose=True)

        print(result["text"])
    except Exception as e:
        print("处理音频文件时发生错误:", e)