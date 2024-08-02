import os
import sys
import time
import pyaudio
import whisper
import logging
import threading
import numpy as np
from pydub import AudioSegment
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')
warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 500

is_recording = True
model = whisper.load_model("base")


def save_chunk(p, chunk_ctr, frames):
    audio = AudioSegment(
        data=b"".join(frames),
        sample_width=p.get_sample_size(FORMAT),
        frame_rate=RATE,
        channels=CHANNELS
    )
    output_file = f"audio/output_{chunk_ctr}.mp3"
    audio.export(output_file, format="mp3")
    return output_file

def steps(p, chunk_ctr, frames):
    file_path = save_chunk(p, chunk_ctr, frames)
    result = model.transcribe(file_path)
    print(result['text'].strip())

def record():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )
    frames = []
    try:
        chunk_size = 50
        chunk_ctr = 0
        logger.debug("start recording..")
        while is_recording:
            try:
                data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                if np.max(audio_data) > THRESHOLD:
                    frames.append(data)
                    if len(frames) > chunk_size:
                        steps(p, chunk_ctr, frames)
                        chunk_ctr += 1 
                        frames = []
            except OSError as e:
                logger.warning(f"{e}. pausing briefly to recover.")
                time.sleep(0.01)
    except KeyboardInterrupt:
        steps(p, chunk_ctr, frames)
        time.sleep(2)
        logger.debug("done")
    
    stream.stop_stream()
    stream.close()
    p.terminate()


def run():
    
    recording_thread = threading.Thread(target=record)
    recording_thread.start()

    input("press enter to stop recording. \n\n")
    
    is_recording = False
    recording_thread.join()
