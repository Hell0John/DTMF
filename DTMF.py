import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.io import wavfile
from scipy.fftpack import fft


def analiz(ses: list, n: int, freq: int):
    # x'i zaman düzlemi olarak ayarlama
    k = np.linspace(0, len(ses) / freq, num=len(ses))

    fig = plt.figure('Girilen Ses dosyası')
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(k, ses)
    ax1.set_title('Plot Graph')
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.stem(k, ses)  # stem graf yapma
    ax2.set_title('Stem Graph')
    plt.show()

    a = math.floor(len(ses) / n)
    tus = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]
    x = np.arange(0, a)
    sekme_2 = plt.figure('Frekans Spektrumu')
    print('Girilen dosyanın şifresi:',end=' ')
    for i in range(n):
        ftel = abs(fft(ses[(a * i):((i + 1) * a)], freq))
        y=np.max(ftel[650:1000])
        frekans_1=y.index(y)
        z = np.max(ftel[1200:1500])
        frekans_2 = z.index(z)

        #max 30 fazlasından küçükse o satırda
        if frekans_1 < 727:
            j = 0
        elif frekans_1 < 800:
            j = 1
        elif frekans_1 < 882:
            j = 2
        else:
            j = 3


        # max 30 fazlasından küçükse o sütunda
        if frekans_2 < 1239:
            k = 0
        elif frekans_2 < 1366:
            k = 1
        else:
            k = 2

        bx = sekme_2.add_subplot(n, 1, i + 1)
        bx.plot(x, ftel[0:a])
        bx.set_title(tus[j][k])
        print(f'{tus[j][k]}',end=' ')
    plt.show()


if __name__ == "__main__":
    freq, dizi = wavfile.read('Ornek.wav')  # Verilen wav okuma

    n = 11 #verilen Ornek.wav 'da tuşa tıklanma sayısı.
    max_value = np.max(dizi)
    analiz(dizi - (max_value / 2), n, freq)

    # kendi numaramı oluşturma burdan sonra
    Fs = 8000
    string = input("\nNumaranızı giriniz (Örneğin: 5388121936) : ")  # Numarayı kullanıcıdan al tek bir string şeklinde
    dtmf = {
        '1': (697, 1209),
        '2': (697, 1336),
        '3': (697, 1477),
        '4': (770, 1209),
        '5': (770, 1336),
        '6': (770, 1477),
        '7': (852, 1209),
        '8': (852, 1336),
        '9': (852, 1477),
        '*': (941, 1209),
        '0': (941, 1336),
        '#': (941, 1477)
    }
    t = .1  # bir tuşa basmanın süresi
    s = .1  # aralık uzunluğu
    space = np.zeros(int(s * Fs))
    x = []
    num_samples = int(t * Fs)
    time = np.linspace(0, t, num_samples)
    for i in range(len(string)):
        p = 5*(np.sin(2 * np.pi * dtmf[string[i]][0] * time) + np.sin(2 * np.pi * dtmf[string[i]][1] * time))#5 amplitude
        x = np.concatenate((x, p, space))
    wavfile.write("5388121936.wav", Fs, x.astype(np.float32))
    Fs, dizi_2 = wavfile.read('5388121936.wav')
    analiz(dizi_2, len(string), Fs)