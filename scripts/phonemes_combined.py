import os
from os.path import join


def create_phonemes():
    phonemes = __load_phonemes_in_at_dialect_in_sampa_format()
    sampa_to_ipa = __create_sampa_to_ipa_mapping()
    phonemes_ipa = __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa)
    ipa_list_phonemes = __read_ipa_list_phonemes()
    combined_phonemes = __create_combined_phonemes(ipa_list_phonemes, phonemes_ipa)
    __write_phonemes_in_ipa_format(combined_phonemes)


def __create_combined_phonemes(ipa_list_phonemes, phonemes_ipa):
    combined_phonemes = phonemes_ipa
    [combined_phonemes.append(phonem) for phonem in ipa_list_phonemes if phonem not in combined_phonemes]
    return combined_phonemes


def __read_ipa_list_phonemes():
    with open(join(".", "ipa_list.txt"), mode='r', encoding='utf8') as input_file:
        ipa_list_phonemes = input_file.read().split("\n")[2:]
    return ipa_list_phonemes


def __write_phonemes_in_ipa_format(phonemes_ipa):
    with open(join("D:\\workspaces\\tugraz\\speech_synth\\ue1\\src", "ipa_phonemes"), mode='w+', encoding='utf8') as output_file:
        output_file.write('|'.join(phonemes_ipa))


def __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa):
    phonemes_ipa = []
    [phonemes_ipa.append(sampa_to_ipa[phonem]) for phonem in phonemes]
    return phonemes_ipa


def __create_sampa_to_ipa_mapping():
    sampa_to_ipa = {}
    with open(join("D:\\workspaces\\tugraz\\speech_synth\\ue1\\src", "sampa_to_ipa.txt"), mode='r', encoding='utf8') as f:
        lines = f.read().split("\n")
        entries = [entry.split(' ') for entry in lines if entry]
        for entry in entries:
            sampa_to_ipa[entry[0]] = entry[1]
    return sampa_to_ipa


def __load_phonemes_in_at_dialect_in_sampa_format():
    phonemes = []
    for (root, _, file_names) in os.walk("D:\\workspaces\\tugraz\\speech_synth\\ue1\\aridialect_spo\\aridialect_labels"):
        for file_name in file_names:
            with open(join(root, file_name), mode='r', encoding='utf8') as label_file:
                lines = label_file.readlines()
                [phonemes.append(line[line.find("-") + 1:line.find("+")]) for line in lines if line[line.find("-") + 1:line.find("+")] not in phonemes]
    return phonemes


def read_phonemes():
    with open(join(".", "ipa_phonemes"), mode='r', encoding='utf8') as input_file:
        phoneme_list = input_file.readline().split("|")


if __name__ == '__main__':
    # create_phonemes()
    read_phonemes()
