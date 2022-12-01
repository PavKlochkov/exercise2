import matplotlib.pyplot as plt
import numpy as np
import requests as rq
import csv
import scipy as sc
import urllib.request
import re


if __name__ == '__main__':
    url = 'https://jenyay.net/uploads/Student/Modelling/task_02.txt'
    urllib.request.urlretrieve(url, 'variants.txt')
    with open('variants.txt', 'r') as file:
        data = file.readlines()
    var = 6-1
    print(data[var])
    print(re.findall('\d+[.]*\d*e*[-]*\d*', data[var]))
    znachenia = re.findall('\d+[.]*\d*e*[-]*\d*', data[var])

    d = float(znachenia[1])
    f_min = float(znachenia[2])
    f_max = float(znachenia[3])

    r = d/2
    c = 3*10**8
    j = complex(0,1)

    def h(n,kr):
        return sc.special.spherical_jn(n, kr)+1j*sc.special.spherical_yn(n,kr)

    def a(n,kr):
        return sc.special.spherical_jn(n,kr)/h(n,kr)

    def b(n,kr):
        return (k*r*sc.special.spherical_jn(n-1,kr)-n*sc.special.spherical_jn(n,kr))/(k*r*h(n-1,kr)-n*h(n,kr))

    delt_f = np.linspace(f_min,f_max,2500) # диапазон частот
    lambd = c/delt_f #длинны волн
    k = 2*np.pi/lambd # волновое число

    i = 79
    summa = 0
    n = 1

    while n!=i:
        summa += (-1)**n*(n+0.5)*(b(n,k*r)-a(n,k*r))
        n=n+1

    sigma = ((lambd**2)/np.pi*(abs(summa))**2) # значения ЭПР

    lines = ""
    with open("result.csv",mode = "w", encoding='utf-8') as w_file:
        filednames = ['#','Длина волны,м','Частота,Гц','ЭПР,м^2']
        writer = csv.DictWriter(w_file,fieldnames = filednames)
        writer.writeheader()
        writer.writerows([{'#':i+1, 'Длина волны,м':lambd[i], 'Частота,Гц':delt_f[i], 'ЭПР,м^2':sigma[i]} for i in range(len(sigma))])

    with open("result.csv", mode="r", encoding='utf-8') as w_file:
        for line in w_file:
            lines+= " ".join(line.split('\n'))
            lines = lines.replace("  ",'\n')

    with open("result.csv", mode="w", encoding='utf-8') as w_file:
            for line in lines:
                    w_file.write(line)

    plt.title("Зависимость ЭПР от частоты")
    plt.xlabel("$f$,Гц")
    plt.ylabel("$σ$,м^2")
    plt.plot(delt_f,sigma)
    plt.show()
