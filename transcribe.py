import os
import sys
import time
import pyaudio
import logging
import threading
import numpy as np
from pydub import AudioSegment
from faster_whisper import WhisperModel

import warnings
import __main__

from config import (
    AUDIO_FRAMES_PER_BUFFER, AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_CHUNK_SIZE,
    AUDIO_RATE, AUDIO_THRESHOLD, WHISPER_MODEL_SIZE, 
    WHISPER_DEVICE_TYPE, WHISPER_COMPUTE_TYPE, WHISPER_BEAM_SIZE
)

warnings.filterwarnings("ignore", category=FutureWarning, module='whisper')
warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


__main__.is_recording = True
model_size = WHISPER_MODEL_SIZE
model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE_TYPE, compute_type=WHISPER_COMPUTE_TYPE)


def save_chunk(p, chunk_ctr, frames):
    audio = AudioSegment(
        data=b"".join(frames),
        sample_width=p.get_sample_size(AUDIO_FORMAT),
        frame_rate=AUDIO_RATE,
        channels=AUDIO_CHANNELS
    )
    output_file = f"audio/output_{chunk_ctr}.mp3"
    audio.export(output_file, format="mp3")
    return output_file

def transcribe_chunk(model, file_path):
    segments, _ = model.transcribe(file_path, beam_size=WHISPER_BEAM_SIZE)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription.strip()

def steps(model, p, chunk_ctr, frames):
    file_path = save_chunk(p, chunk_ctr, frames)
    text = transcribe_chunk(model, file_path)
    logger.info(f"[transcribed]{chunk_ctr}] {text}")

def record():

    p = pyaudio.PyAudio()
    stream = p.open(
        format=AUDIO_FORMAT,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_RATE, input=True,
        frames_per_buffer=AUDIO_FRAMES_PER_BUFFER
    )
    frames = []
    try:
        chunk_ctr = 0
        logger.info("start recording..")
        while __main__.is_recording:
            try:
                data = stream.read(AUDIO_FRAMES_PER_BUFFER, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                if np.max(audio_data) > AUDIO_THRESHOLD:
                    frames.append(data)
                    if len(frames) > AUDIO_CHUNK_SIZE:
                        steps(model, p, chunk_ctr, frames)
                        chunk_ctr += 1 
                        frames = []
            except OSError as e:
                logger.warning(f"{e}. pausing briefly to recover.")
                time.sleep(0.01)
    except KeyboardInterrupt:
        steps(p, chunk_ctr, frames)
        time.sleep(2)
        logger.info("done")
    
    stream.stop_stream()
    stream.close()
    p.terminate()


def run():
    recording_thread = threading.Thread(target=record)
    recording_thread.start()
    input("Press enter to stop recording. \n\n")
    __main__.is_recording = False
    logger.info('stopping transcriber..')
    recording_thread.join()

if __name__ == "__main__":
    run()
