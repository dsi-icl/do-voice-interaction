import pyaudio
from deepspeech import Model
import scipy.io.wavfile as wav
import wave, os, sys, contextlib

@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

WAVE_OUTPUT_FILENAME = "audio/test_audio.wav"

def record_audio(output=WAVE_OUTPUT_FILENAME):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    with ignore_stderr():
        p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = [stream.read(CHUNK) for i in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def deepspeech_predict(output=WAVE_OUTPUT_FILENAME,model_path='deepspeech-0.7.4-models.pbmm',scorer_path='deepspeech-0.7.4-models.scorer'):

    N_FEATURES = 25
    N_CONTEXT = 9
    BEAM_WIDTH = 500
    LM_ALPHA = 0.75
    LM_BETA = 1.85

    with ignore_stderr():
        ds = Model(model_path)
    ds.setBeamWidth(BEAM_WIDTH)
    ds.setScorerAlphaBeta(0.75,1.85)
    ds.enableExternalScorer(scorer_path)

    fs, audio = wav.read(output)
    return ds.stt(audio)

if __name__ == '__main__':
	record_audio(WAVE_OUTPUT_FILENAME)
	predicted_text = deepspeech_predict(WAVE_OUTPUT_FILENAME)
	print(predicted_text)
