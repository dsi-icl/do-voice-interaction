import os
import sys
import io
import torch
from collections import OrderedDict

from TTS.models.tacotron import Tacotron
from TTS.layers import *
from TTS.utils.data import *
from TTS.utils.audio import AudioProcessor
from TTS.utils.generic_utils import load_config
from TTS.utils.text import text_to_sequence
from TTS.utils.synthesis import synthesis
from TTS.utils.text.symbols import symbols, phonemes
from TTS.utils.visual import visualize
import contextlib
import sys, os

@contextlib.contextmanager
def ignore_stdout():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stdout = os.dup(1)
    sys.stdout.flush()
    os.dup2(devnull, 1)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stdout, 1)
        os.close(old_stdout)

# Set constants
MODEL_PATH = './tts_model/best_model.pth.tar'
CONFIG_PATH = './tts_model/config.json'
OUT_FILE = './tts_audios/tts_out.wav'
CONFIG = load_config(CONFIG_PATH)
use_cuda = False

def tts(model, ap, text, config=CONFIG, use_cuda=use_cuda, out_path=OUT_FILE):
    waveform, alignment, spectrogram, mel_spectrogram, stop_tokens = synthesis(model, text, CONFIG, use_cuda, ap)
    ap.save_wav(waveform, OUT_FILE)
    return alignment, spectrogram, stop_tokens



def load_model(sentence,model_path=MODEL_PATH, config=CONFIG, use_cuda=use_cuda, out_path=OUT_FILE):
    # load the model
    num_chars = len(phonemes) if CONFIG.use_phonemes else len(symbols)

    with ignore_stdout():
        model = Tacotron(num_chars, CONFIG.embedding_size, CONFIG.audio['num_freq'], CONFIG.audio['num_mels'], CONFIG.r, attn_windowing=False)

	# load the audio processor
	# CONFIG.audio["power"] = 1.3
    CONFIG.audio["preemphasis"] = 0.97
    with ignore_stdout():
        ap = AudioProcessor(**CONFIG.audio)

    # load model state
    if use_cuda:
        cp = torch.load(model_path)
    else:
        cp = torch.load(model_path, map_location=lambda storage, loc: storage)

	# load the model
    model.load_state_dict(cp['model'])
    if use_cuda:
        model.cuda()
    model.eval()

    model.decoder.max_decoder_steps = 1000
    align, spec, stop_tokens = tts(model, ap, sentence, config, use_cuda, out_path)

if __name__ == '__main__':
	sentence =  "Welcome to the Data Observatory. I am your voice assistant. Can I help you ?"
	load_model(sentence)
