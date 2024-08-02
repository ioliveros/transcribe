# transcribe

A naive approach to transcribe real-time audio using pyaudio and huggingface [whisper model](https://huggingface.co/openai/whisper-base.en)


#### dependencies (only tested in MacOS)

When you encounter build issues with `PyAudio`
```
note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed building wheel for PyAudio
```
Make sure you install dependencies below first
```
brew install portaudio
```

#### install requirements
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```


#### Run script
```bash
python3 transcriber.py
```
