import urllib.request #для работы с URL файлами
import scipy as sc #для функции Бесселя и Неймана
import numpy as np #для работы с массивами
import re #для работы со строками
import matplotlib.pyplot as plt #графики
import os #для работы с директорией
#задаем функции нашей программы, а также коэффициенты а и b
def h(n,x):
    return sc.special.spherical_jn(n, x) + 1j * sc.special.spherical_yn(n, x) #ханкеля первого рода через сумму бесселя и неймана первого рода
#вычисляем коэффициенты а и b для расчета поперечного сечения рассеяния
#отношение бесселя к ханкелю первого рода
def a(n,x):
    return sc.special.spherical_jn(n, x)/h(n, k*r) 
#считаем производную функции бесселя как разность для порядка n и n-1 и делим на производную функцию ханкеля, тоже посчитанную как разность для порядка n и n-1
def b(n,x):
    return (x * sc.special.spherical_jn(n-1, x) - n * sc.special.spherical_jn(n, x)) / (x * h(n - 1, x) - n * h(n, x)) 

def sigma(povtor,x):
    sigm = 0
    for n in range(1,povtor):
        sigm = sigm + np.power(-1,n)*(n+0.5)*(b(n,x)-a(n,x)) #power берет два массива и умножает значения одного, возведенные в степень другого 
        print('n= ',n)
    return sigm #конечная функция основной программы, в которую пользователь задает количество повторов для корректировки точности (ЭПР 

if __name__=='__main__':
    url = 'https://jenyay.net/uploads/Student/Modelling/task_02.csv' #скачиваем файл с диаметром сферы и диапазоном частот моего варианта 
    urllib.request.urlretrieve(url, 'znachenia.xml')
    with open('znachenia.xml', 'r') as file:
        data = file.readlines() #открываем файл и считываем его значения в переменную data
    #вводим наш вариант и желаемое число шагов приближения (используется дальше в массиве linespace)   
    var = int(input('Введите ваш вариант: '))
    priblizhenie = int(input('Введите приближение(число шагов): ')) 
    print(data[var])
    #функция findall выполняет поиск по заданному шаблону в строке (8 вариант) и возвращает нам список совпадений, который мы выводим далее
    print(re.findall(r'\d+[.]*\d*e*[-]*\d*', data[var])) 
    variant = re.findall(r'\d+[.]*\d*e*[-]*\d*', data[var])
    D = float(variant[1])
    print('D= ',D)
    fmin = float(variant[2])
    print('fmin= ',fmin)
    fmax = float(variant[3])
    print('fmax= ',fmax)
    #вычисляем радиус сферы как половину диаметра и выводим пользователю
    r = D/2      
    print('r= ',r)
    #генерируем массив частот f с использованием функции linspace в заданном диапазоне
    f = np.linspace(fmin,fmax,priblizhenie) #используется для генерации последовательных чисел в линейном пространтсве с одинаковым шагом
    print('f= ',f)
    lamda = 3*10**8/f #вычисляем длину волны для каждой частоты на нашем шаге 
    print('lamda= ',lamda)
    k = 2*np.pi/lamda #вычисляем волновое число 
    print('k= ',k)
    result = lamda**2/np.pi*abs(sigma(70,k*r))**2 #вычисляем абсолютное значение функции sigma, где 70 это количество повторов в вызове функции sigma 
    print('sigma = ',result)
    plt.xlabel('f, Гц') #подписываем оси х и y наших графиков
    plt.ylabel('sigma, м^2')
    plt.plot(f,result) #строим графки с осями f и result (ранее мы записали в result значение полученного sigma)
    plt.show()

    # creating json file
    if 'results' not in os.listdir(): #проверка на наличие папки results
        os.makedirs(os.path.join(os.getcwd(), 'results')) #создает каталог results в случае отсутствия 
    #открывает файл results и записывает туда структуру JSON файла в режими кодировки UTF-8
    with open('results/result.json', 'w', encoding='utf8') as file:
        file.write('{\n    "data": [\n')
        for i in range(priblizhenie): #повторение в диапазоне priblizhenie 
            slova = {"freq": f[i], "lambda": lamda[i], "rcs": result[i]} #создание словаря с ключами в ковычках
            if i + 1 != priblizhenie: #если иттерация не последняя, то продолжает
                file.write('        {},\n'.format(slova))
            if i + 1 == priblizhenie:
                file.write('        {}\n'.format(slova))
        file.write('    ]\n}') #закрывает квадратную и фигурную скобку в конце

