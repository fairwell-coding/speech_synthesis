import os
from os.path import join


def create_phonemes():
    phonemes_ipa = read_phonemes()
    __write_phonemes_in_ipa_format(phonemes_ipa)


def __write_phonemes_in_ipa_format(phonemes_ipa):
    with open(join("/IMS-Toucan/Preprocessing", "ipa_phonemes_complete.txt"), mode='w+', encoding='utf8') as output_file:
        output_file.write('\n'.join(phonemes_ipa))


def read_phonemes():
    with open(join(".", "ipa_phonemes_merged"), mode='r', encoding='utf8') as input_file2:
        phoneme_list_merged = input_file2.readline().split("|")

    with open(join(".", "ipa_phonemes"), mode='r', encoding='utf8') as input_file:
        phoneme_list = input_file.readline().split("|")

    # Add missing phonemes (without training resulted in error)
    phoneme_list.append("u")
    phoneme_list.append(phoneme_list_merged[106])

    return phoneme_list


if __name__ == '__main__':
    create_phonemes()
    #read_phonemes()
