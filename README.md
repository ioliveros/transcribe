# transcribe

A naive approach to transcribe real-time audio using pyaudio and huggingface [whisper model](https://huggingface.co/openai/whisper-base.en)


#### dependencies (only tested in MacOS)
```
note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for PyAudio
```
brew install portaudio


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
