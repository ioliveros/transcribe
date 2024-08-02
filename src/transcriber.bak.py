import os
import sys
import time
import pyaudio
import whisper
import logging
from pydub import AudioSegment

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')
warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

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

def save_chunk(chunk_ctr, frames):
    audio = AudioSegment(
        data=b"".join(frames),
        sample_width=p.get_sample_size(FORMAT),
        frame_rate=RATE,
        channels=CHANNELS
    )
    output_file = f"audio/output_{chunk_ctr}.mp3"
    audio.export(output_file, format="mp3")
    return output_file

def steps(chunk_ctr, frames):
    file_path = save_chunk(chunk_ctr, frames)
    result = model.transcribe(file_path)
    sys.stdout.write(result['text'] + ' ')
    sys.stdout.flush()

frames = []
try:
    chunk_size = 50
    chunk_ctr = 0
    logger.info("Start recording..")
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