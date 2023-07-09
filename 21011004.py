import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

def convolution(x1: list, n: int, x2: list, m: int):
    N = n + m - 1
    y = [0] * N
    for i in range(N):
        for j in range(m):
            if (i-j)<n and i >= j:
                y[i] = y[i] + x1[i - j] * x2[j]
    return y

def graph( x1: list , n: int, sifir1 : int):
    a=np.arange(0-sifir1,n-sifir1,1)
    plt.stem(a, x1,linefmt='--')
    plt.xlabel("Indis")
    plt.ylabel("Değer")

if __name__ == "__main__":
    n = int(input("X1 dizisinin boyutunu giriniz: "))
    m = int(input("X2 dizisinin boyutunu giriniz: "))
    N = n + m - 1
    x2 = [0] * m
    x1 = [0] * n
    for x in range(n):
        x1[x] = int(input(f'X1[ {x} ]: '))
    sifir1 = int(input("X1 Dizisinin kaçıncı indisinin 0 noktası olduğunu giriniz: "))
    for x in range(m):
        x2[x] = int(input(f'X2[ {x} ]: '))
    sifir2 = int(input("X2 Dizisinin kaçıncı indisinin 0 noktası olduğunu giriniz: "))
    print("X1 Dizisi: [", end=' ')
    for x in range(n):
        if x != sifir1:
            print(f' {x1[x]} ', end=' ')
        else:
            print(f'\033[2;30;43m  {x1[x]}  \033[0;0m', end=' ')
    print("]")
    print("X2 Dizisi: [", end=' ')
    for x in range(m):
        if x != sifir2:
            print(f' {x2[x]} ', end=' ')
        else:
            print(f'\033[2;30;43m  {x2[x]}  \033[0;0m', end=' ')
    print("]")
    y=(convolution(x1, n, x2, m))
    sifiravg = (sifir1 + sifir2)
    print("(X1*X2) Dizisi Kendi Fonksiyonum: ", end=' ')
    for i in range(N):
        if sifiravg == i:
            print(f'\033[2;30;43m  {y[i]}  \033[0;0m', end=' ')
        else:
            print(y[i], end=' ')
    print("\n")
    print("(X1*X2) Dizisi Hazır Fonksiyonlu: ", end=' ')
    yHazir = np.convolve(x1, x2)
    for i in range(N):
        if sifiravg == i:
            print(f'\033[2;30;43m  {yHazir[i]}  \033[0;0m', end=' ')
        else:
            print(yHazir[i], end=' ')
    plt.subplot(4,1,1)
    graph(x1,n,sifir1)
    plt.title('X1')
    plt.subplot(4, 1, 2)
    graph(x2,m,sifir2)
    plt.title('X2')
    plt.subplot(4, 1, 3)
    graph(y,N,sifiravg)
    plt.title('Kendi yazdığım convolution fonksiyonu')
    plt.subplot(4, 1, 4)
    graph(yHazir,N,sifiravg)
    plt.title('Hazır convolution fonksiyonu')
    plt.show()
    #2. soru sonu
    duration1 = 5
    duration2 = 10
    freq = 44100
    print("\n5 Saniye Konuşunuz")
    recording1 = sd.rec(int(duration1 * freq), samplerate=freq, channels=1)
    sd.wait()
    print("\n10 Saniye Konuşunuz")
    recording2 = sd.rec(int(duration2 * freq), samplerate=freq, channels=1)
    sd.wait()
    retry=0
    while retry==0:
        M = int(input("M değerini giriniz: "))
        impuls = [0] * ((M * 400) + 1)
        impuls[0] = 1
        for i in range(1, M + 1):
            impuls[i * 400] = 0.8 * M
        my_y1 = convolution(recording1[:, 0], duration1 * freq, impuls, ((M * 400) + 1)) #sounddevice arrayleri sütunda sakladığından direk olarak sütunu tek array olarak yollama yaptım fonksiyonlara
        my_y2 = convolution(recording2[:, 0], duration2 * freq, impuls, ((M * 400) + 1))
        Y2 = np.convolve(recording2[:, 0], impuls)
        Y1 = np.convolve(recording1[:, 0], impuls)
        M = int(input("Ses Kayıtlarını dinlemek icin herhangi bir sayi giriniz:"))
        print("\nX1[n] Ses Kaydı Oynatılıyor.")
        sd.play(recording1, freq)
        sd.wait()
        print("\nY1[n] Ses Kaydı Oynatılıyor.")
        sd.play(Y1, freq)
        sd.wait()
        print("\nmyY1[n] Ses Kaydı Oynatılıyor.")
        sd.play(my_y1, freq)
        sd.wait()
        print("\nX2[n] Ses Kaydı Oynatılıyor.")
        sd.play(recording2, freq)
        sd.wait()
        print("\nY2[n] Ses Kaydı Oynatılıyor.")
        sd.play(Y2, freq)
        sd.wait()
        print("\nmyY2[n] Ses Kaydı Oynatılıyor.")
        sd.play(my_y2, freq)
        sd.wait()
        retry = int(input("Başka M değeri denemek için 0, Programdan çıkmak için 1 giriniz: "))