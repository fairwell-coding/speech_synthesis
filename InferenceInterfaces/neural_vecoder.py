import os

import librosa.display as lbd
import matplotlib.pyplot as plt
import sounddevice
import soundfile
import torch
import torchaudio

from speechbrain.pretrained import EncoderClassifier
from InferenceInterfaces.InferenceArchitectures.InferenceHiFiGAN import HiFiGANGenerator
from InferenceInterfaces.InferenceArchitectures.InferenceTacotron2 import Tacotron2
from Preprocessing.TextFrontend import TextFrontend


class neural_vecoder(torch.nn.Module):

    def __init__(self, device="cpu", speaker_embedding=None):
        super().__init__()
        self.speaker_embedding = speaker_embedding
        self.device = device
        if isinstance(speaker_embedding, torch.Tensor):
            self.speaker_embedding = speaker_embedding
        else:
            #self.speaker_embedding = torch.load(os.path.join("Models", "SpeakerEmbedding", speaker_embedding), map_location='cpu').to(
            #    torch.device(device)).squeeze(0).squeeze(0)
            self.speaker_embedding = None
        self.mel2wav = HiFiGANGenerator(path_to_weights=os.path.join("Models", "HiFiGAN_aridialect", "best.pt")).to(torch.device(device))
        self.mel2wav.eval()
        self.to(torch.device(device))

    def forward(self, mel):
        with torch.no_grad():
            wave = self.mel2wav(mel)

        return wave

    def mel_to_file(self, mel_list, file_location, silent=False):
        """
        :param silent: Whether to be verbose about the process
        :param text_list: A list of strings to be read
        :param file_location: The path and name of the file it should be saved to
        """
        wav = None
        silence = torch.zeros([24000])
        i=0
        for melspec in mel_list:
            print("Synthesize Mel-Spectra")
            if wav is None:
                wav = self(melspec).cpu()
                wav = torch.cat((wav, silence), 0)
            else:
                wav = torch.cat((wav, self(melspec).cpu()), 0)
                wav = torch.cat((wav, silence), 0)
            i=i+1
        soundfile.write(file=file_location, data=wav.cpu().numpy(), samplerate=48000)

    def read_aloud(self, wavname, view=False, blocking=False):
        if wavname.strip() == "":
            return
        wav = self(False,wavname).cpu()
        #wav = self(text, view).cpu()
        wav = torch.cat((wav, torch.zeros([24000])), 0)
        if not blocking:
            sounddevice.play(wav.numpy(), samplerate=48000)
        else:
            sounddevice.play(torch.cat((wav, torch.zeros([12000])), 0).numpy(), samplerate=48000)
            sounddevice.wait()

    def plot_attention(self, wavname):
        sentence_tensor = self.text2phone.string_to_tensor("",False,path_to_wavfile=wavname).squeeze(0).long().to(torch.device(self.device))
        att = self.phone2mel(text=sentence_tensor, speaker_embedding=self.speaker_embedding, return_atts=True)
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.imshow(att.detach().numpy(), interpolation='nearest', aspect='auto', origin="lower")
        axes.set_title("{}".format(sentence))
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        plt.tight_layout()
        plt.show()

    def save_embedding_table(self):
        import json
        phone_to_embedding = dict()
        for phone in self.text2phone.ipa_to_vector:
            if phone in ['?', 'ɚ', 'p', 'u', 'ɹ', 'ɾ', 'ʔ', 'j', 'l', 'ɔ', 'v', 'm', '~', 'ᵻ', 'ɪ', 'ʒ', 'æ', 'n', 'z', 'ŋ', 'i', 'b', 'o', 'ɛ', 'e', 't', '!',
                         'ʊ', 'ð', 'd', 'θ',
                         'ɑ', 'ɡ', 's', 'ɐ', 'k', 'w', 'ə', 'ʌ', 'ʃ', '.', 'a', 'ɜ', 'h', 'f']:
                print(phone)
                phone_to_embedding[phone] = self.phone2mel.enc.embed(torch.LongTensor([self.text2phone.ipa_to_vector[phone]])).detach().numpy().tolist()
        with open("embedding_table_512dim.json", 'w', encoding="utf8") as fp:
            json.dump(phone_to_embedding, fp)
