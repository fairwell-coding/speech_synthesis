from os.path import join


def create_phonemes(path_to_label_file):
    phonemes = __load_phonemes_in_at_dialect_in_sampa_format(path_to_label_file)
    sampa_to_ipa = __create_sampa_to_ipa_mapping()
    phonemes_ipa = __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa)
    return phonemes_ipa


def __convert_phonemes_from_sampa_into_ipa_format(phonemes, sampa_to_ipa):
    phonemes_ipa = ''
    for phonem in phonemes:
        phonemes_ipa += ' '.join(sampa_to_ipa[phonem])
    return phonemes_ipa


def __create_sampa_to_ipa_mapping():
    sampa_to_ipa = {}
    with open(join("/IMS-Toucan/Preprocessing/", "sampa_to_ipa.txt"), mode='r', encoding='utf8') as f:
        lines = f.read().split("\n")
        entries = [entry.split(' ') for entry in lines if entry]
        for entry in entries:
            sampa_to_ipa[entry[0]] = entry[1]
    return sampa_to_ipa


def __load_phonemes_in_at_dialect_in_sampa_format(path_to_label_file):
    phonemes = []
    with open(path_to_label_file, mode='r', encoding='utf8') as label_file:
        lines = label_file.readlines()
        [phonemes.append(line[line.find("-") + 1:line.find("+")]) for line in lines]
        return phonemes

