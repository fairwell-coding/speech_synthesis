import os
from os.path import join


def create_phonemes():
    #phonemes = __load_phonemes_in_at_dialect_in_sampa_format()
    #sampa_to_ipa = __create_sampa_to_ipa_mapping()
    #phonemes_ipa = __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa)
    phonemes_ipa = read_phonemes()
    __write_phonemes_in_ipa_format(phonemes_ipa)


def __write_phonemes_in_ipa_format(phonemes_ipa):
    with open(join("/IMS-Toucan/Preprocessing", "ipa_phonemes_complete.txt"), mode='w+', encoding='utf8') as output_file:
        output_file.write('\n'.join(phonemes_ipa))
        #output_file.write(phonemes_ipa)

def __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa):
    phonemes_ipa = []
    phonemes_ipa_string = []
    [phonemes_ipa.append(sampa_to_ipa[phonem]) for phonem in phonemes]
    for elem in phonemes_ipa:
         phoneme_string = str(elem)
         phonemes_ipa_string.append(phoneme_string)
    #phonemes_ipa_string.append('u')
         #print(phoneme_string)
    print(phonemes_ipa)
    return phonemes_ipa_string


def __create_sampa_to_ipa_mapping():
    sampa_to_ipa = {}
    with open(join("/IMS-Toucan/Preprocessing/", "sampa_to_ipa.txt"), mode='r', encoding='utf8') as f:
        lines = f.read().split("\n")
        # [entry for entry in ddd if entry]
        entries = [entry.split(' ') for entry in lines if entry]
        for entry in entries:
            sampa_to_ipa[entry[0]] = entry[1]
    return sampa_to_ipa


def __load_phonemes_in_at_dialect_in_sampa_format():
    phonemes = []
    #for (root, _, file_names) in os.walk("/IMS-Toucan/aridialect/aridialect_labels"):
    #    for file_name in file_names:
    #        with open(join(root, file_name), mode='r', encoding='utf8') as label_file:
    #            lines = label_file.readlines()
    #            [phonemes.append(line[line.find("-") + 1:line.find("+")]) for line in lines if line[line.find("-") + 1:line.find("+")] not in phonemes]
    phonemes = read_phonemes()

    return phonemes


def read_phonemes():
    with open(join(".", "ipa_phonemes_merged"), mode='r', encoding='utf8') as input_file2:
        phoneme_list_merged = input_file2.readline().split("|")

    with open(join(".", "ipa_phonemes"), mode='r', encoding='utf8') as input_file:
        phoneme_list = input_file.readline().split("|")

    phoneme_list.append("u")
    phoneme_list.append(phoneme_list_merged[106])
    print(phoneme_list)
    return phoneme_list

if __name__ == '__main__':
    create_phonemes()
    #read_phonemes()
