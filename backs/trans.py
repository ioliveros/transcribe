import whisper

model = whisper.load_model("base")
result = model.transcribe("audio/output_0.wav")

print(result)
