import librosa
import os
import soundfile as sf



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arr = os.listdir('/Users/DanielZirat/Desktop/aridialect/aridialect_wav22050')
    for file in arr:
        filename = '/Users/DanielZirat/Desktop/aridialect/aridialect_wav22050/' + file
        y, s = librosa.load(filename,sr=16000)
        filename = '/Users/DanielZirat/Desktop/aridialect/aridialect_wav16000/' + file
        sf.write(filename, y, s)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
