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


class aridialect_text2mel(torch.nn.Module):

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
        self.text2phone = TextFrontend(language="at-lab", use_word_boundaries=False,
                                       use_explicit_eos=False, inference=True)
        #self.phone2mel = Tacotron2(path_to_weights=os.path.join("Models", "Tacotron2_aridialect", "best.pt"),
        #                           idim=166, odim=80, spk_embed_dim=960, reduction_factor=1).to(torch.device(device))

        #self.phone2mel = Tacotron2(path_to_weights=os.path.join("Models", "Tacotron2_aridialect", "best.pt"),
        #                          idim=166, odim=80, spk_embed_dim=None, reduction_factor=1).to(torch.device(device))

        self.phone2mel = Tacotron2(path_to_weights=os.path.join("Models", "Tacotron2_aridialect", "checkpoint_29492.pt"),
                                   idim=166, odim=80, spk_embed_dim=None, reduction_factor=1).to(torch.device(device))

        self.phone2mel.eval()
        self.to(torch.device(device))

    def forward(self, path_to_wavfile):
        with torch.no_grad():
            #get spk_id from wavefile and compute speaker embedding
            speaker_embedding_function_ecapa = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",run_opts={"device": str(self.device)},savedir="Models/speechbrain_speaker_embedding_ecapa")
            speaker_embedding_function_xvector = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb",run_opts={"device": str(self.device)},savedir="Models/speechbrain_speaker_embedding_xvector")

            wav2mel = torch.jit.load("Models/SpeakerEmbedding/wav2mel.pt")
            dvector = torch.jit.load("Models/SpeakerEmbedding/dvector-step250000.pt").to(self.device).eval()

            datapoint, sample_rate = torchaudio.load(path_to_wavfile)

            ecapa_spemb = speaker_embedding_function_ecapa.encode_batch(torch.Tensor(datapoint).to(self.device)).flatten().detach().cpu()
            xvector_spemb = speaker_embedding_function_xvector.encode_batch(torch.Tensor(datapoint).to(self.device)).flatten().detach().cpu()
            dvector_spemb = dvector.embed_utterance(wav2mel(torch.Tensor(datapoint), 16000).to(self.device)).flatten().detach().cpu()
            combined_spemb = torch.cat([ecapa_spemb, xvector_spemb, dvector_spemb], dim=0)

            #torch.save(cached_speaker_embedding, "Models/SpeakerEmbedding/aridialect_embedding.pt")
            #self.speaker_embedding = torch.load(os.path.join("Models", "SpeakerEmbedding", "aridialect_embedding.pt"), map_location='cpu').to(torch.device("cpu")).squeeze(0).squeeze(0)

            self.speaker_embedding = combined_spemb.to(self.device)

            phones = self.text2phone.string_to_tensor(text="",view=False,path_to_wavfile=path_to_wavfile).squeeze(0).long().to(torch.device(self.device))
            mel = self.phone2mel(phones, speaker_embedding=self.speaker_embedding).transpose(0, 1)

        return mel

    def read_to_mel(self, wav_list, file_location="", silent=False):
        """
        :param silent: Whether to be verbose about the process
        :param text_list: A list of strings to be read
        :param file_location: The path and name of the file it should be saved to
        """
        #mel_list = None
        mel_list = []
        i=0
        for wavname in wav_list:
            if wavname.strip() != "":
                if not silent:
                    print("Now generating Mel-Spectra of {}".format(wavname))
                mel_list.append(self(wavname).cpu())
                i=i+1
        return mel_list

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
