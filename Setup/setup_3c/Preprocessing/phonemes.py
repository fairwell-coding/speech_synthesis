import os
from os.path import join


def create_phonemes(path_to_label_file):
    phonemes = __load_phonemes_in_at_dialect_in_sampa_format(path_to_label_file)
    sampa_to_ipa = __create_sampa_to_ipa_mapping()
    phonemes_ipa = __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa)
    #__write_phonemes_in_ipa_format(phonemes_ipa)
    return phonemes_ipa


def __write_phonemes_in_ipa_format(phonemes_ipa):
    with open(join("D:\\workspaces\\tugraz\\speech_synth\\ue1\\src", "ipa_phonemes"), mode='w+', encoding='utf8') as output_file:
        output_file.write('|'.join(phonemes_ipa))


def __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa):
    phonemes_ipa = ''
    for phonem in phonemes:
        phonemes_ipa = phonemes_ipa + ' '.join(sampa_to_ipa[phonem])
    return phonemes_ipa


def __create_sampa_to_ipa_mapping():
    sampa_to_ipa = {}
    with open(join("/IMS-Toucan/Preprocessing/", "sampa_to_ipa.txt"), mode='r', encoding='utf8') as f:
        lines = f.read().split("\n")
        # [entry for entry in ddd if entry]
        entries = [entry.split(' ') for entry in lines if entry]
        for entry in entries:
            sampa_to_ipa[entry[0]] = entry[1]
    return sampa_to_ipa


def __load_phonemes_in_at_dialect_in_sampa_format(path_to_label_file):
    phonemes = []
    #for (root, _, file_names) in os.walk("D:\\workspaces\\tugraz\\speech_synth\\ue1\\aridialect_spo\\aridialect_labels"):
    #    for file_name in file_names:
    with open(path_to_label_file, mode='r', encoding='utf8') as label_file:
        lines = label_file.readlines()
        [phonemes.append(line[line.find("-") + 1:line.find("+")]) for line in lines]

        #for elem in phonemes:
        #   print(elem)
        return phonemes


def read_phonemes():
    with open(join(".", "ipa_phonemes"), mode='r', encoding='utf8') as input_file:
        phoneme_list = input_file.readline().split("|")

    print(phoneme_list)

if __name__ == '__main__':
    create_phonemes(path_to_label_file)
    #read_phonemes()
