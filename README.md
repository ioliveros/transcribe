# transcribe

A naive approach to transcribe real-time audio using pyaudio and huggingface [whisper model](https://huggingface.co/openai/whisper-base.en)

We are using [faster-whisper](https://github.com/SYSTRAN/faster-whisper) a fast inference engine for transformer models, a re-implementation of openai's whisper.


By default it's using `cpu` as device_type, for faster results use `cuda` if available in your machine.

```python
WHISPER_DEVICE_TYPE="cuda"
WHISPER_COMPUTE_TYPE="int8_float16"
```

----
When you encounter build issues with `PyAudio`
```
note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed building wheel for PyAudio
```

Install dependencies


### MacOS
```
brew install portaudio
```

### Ubuntu (linux)
```
sudo apt update
sudo apt install portaudio19-dev
pkg-config --modversion portaudio-2.0
```

##### install requirements (make sure to have python >= 3.8 version)
```bash
python3 -m venv env
source env/bin/activate
env/bin/python3 -m pip install --upgrade pip
pip install -r requirements.txt
```


##### Run script
```bash
python3 transcribe.py
```

![Screen Shot 2024-08-03 at 3 41 21 AM](https://github.com/user-attachments/assets/d4b9c818-6798-45fa-8d60-f7c7f63adfbe)


-----


#### faster-whisper issues(?) might be similar [issue](https://github.com/SYSTRAN/faster-whisper/issues/935)

```bash
source env/bin/activate
pip install --force-reinstall "faster-whisper @ https://github.com/SYSTRAN/faster-whisper/archive/refs/heads/master.tar.gz"
```
