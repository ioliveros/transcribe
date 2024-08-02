import os
import sys
import time
import pyaudio
import wave
import whisper
import logging
import numpy as np
import io
from pydub import AudioSegment

import numpy as np
import io
from scipy.io import wavfile

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')
warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

import os
import sys
import time
import pyaudio
import wave
import whisper
import logging
import numpy as np
import io
from pydub import AudioSegment

import numpy as np
import io
from scipy.io import wavfile

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')
warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

# FRAMES_PER_BUFFER = 3200
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

model = whisper.load_model("base")

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# def save_chunk(chunk_ctr, frames):
#     output_file = f"audio/output_{chunk_ctr}.wav"
#     with wave.open(output_file, "wb") as obj:
#         obj.setnchannels(CHANNELS)
#         obj.setsampwidth(p.get_sample_size(FORMAT))
#         obj.setframerate(RATE)
#         obj.writeframes(b"".join(frames))
#     return output_file

def save_chunk(chunk_ctr, frames):
    audio = AudioSegment(
        data=b"".join(frames),
        sample_width=p.get_sample_size(FORMAT),
        frame_rate=RATE,
        channels=CHANNELS
    )
    # raw_audio_data = frames.astype(np.int16).tobytes()
    # raw_audio_data = frames.astype(np.int16).tobytes()
    # raw_audio_data = frames[0].astype(np.int16).tobytes()
    # audio = AudioSegment(
    #     data=b"".join(frames),
    #     sample_width=p.get_sample_size(FORMAT),
    #     frame_rate=RATE,
    #     channels=CHANNELS
    # ) 
    output_file = f"audio/output_{chunk_ctr}.mp3"
    audio.export(output_file, format="mp3")
    #byte_stream = io.BytesIO()
    #audio.export(byte_stream, format="mp3")
    #byte_stream.seek(0)

    return output_file
    #return byte_stream

def steps(chunk_ctr, frames):
    file_path = save_chunk(chunk_ctr, frames)
    result = model.transcribe(file_path)
    # sys.stdout.write(result['text'] + ' ')
    # result = transcribe_audio(frames)
    sys.stdout.write(result['text'] + ' ')
    sys.stdout.flush()

# logger.info("start recording")
frames = []
try:
    chunk_size = 50
    chunk_ctr = 0
    while True:
        try:
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
            frames.append(data)
            if len(frames) > chunk_size:
                steps(chunk_ctr, frames)
                chunk_ctr += 1
                frames = []
        except OSError as e:
            logger.warning(f"{e}. Pausing briefly to recover.")
            time.sleep(0.01)
except KeyboardInterrupt:
    logger.info("Recording stopped by user.")
    time.sleep(1)
    logger.info("Saving last chunked frames")
    save_chunk(chunk_ctr, frames)
    time.sleep(2)
    logger.info("Done")

stream.stop_stream()
stream.close()
p.terminate()
