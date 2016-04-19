import math

import sys

import distributions
import random


class stats:
    # aux method
    @staticmethod
    def x_media(num_random_list):

        x_media_value = 0

        for i in range(len(num_random_list)):
            x_media_value += num_random_list[i]

        return x_media_value / float(len(num_random_list))

    @staticmethod
    def sum_variance(self, num_random_list):
        x_media_value = self.x_media(num_random_list)
        sum = 0

        for i in range(len(num_random_list)):
            sum += math.pow(num_random_list[i] - x_media_value, 2)

        return sum

    @staticmethod
    def random_num_congr(seed, a, c, m, num_quantity, is_seed_included):
        num_rand_list = []
        if (a > 0 and c > 0 and m > 0) and (a < m and c < m):
            i = 0
            if is_seed_included:
                num_rand_list.append(seed)
                i = 1
            else:
                n = float((a * seed + c) % float(m))
                num_rand_list.append(n)
                i += 1
            while i < num_quantity:
                n = ((a * num_rand_list[i - 1] + c) % float(m))
                num_rand_list.append(n)
                i += 1
            for j in range(len(num_rand_list)):
                num_rand_list[j] /= float(m)

            return num_rand_list
        else:
            raise Exception("Some parameters got errors.")

    def random_num_congr2(self, seed, num_quantity, is_seed_included):  # without a,c,m
        num_rand_list = []
        a = 1103515245
        c = 12345
        m = 32768

        i = 0

        if is_seed_included:
            num_rand_list.append(seed)
            i = 1
        else:
            n = float(a * seed + c) % m
            num_rand_list.append(n)
            i += 1

        while i < num_quantity:
            n = float(a * num_rand_list[i - 1] + c) % m
            num_rand_list.append(n)
            i += 1
        for j in range(len(num_rand_list)):
            num_rand_list[j] /= float(m)

    def random_num_congr3(self, seed, a, c, m, num_quantity, fromNum, toNum, is_seed_included):  # between two numbers
        num_rand_list = []

        if (a > 0 and c > 0 and m > 0) and (a < m and c < m):
            i = 0
            if is_seed_included:
                num_rand_list.append(seed)
                i = 1
            else:
                n = float(a * seed + c) % m
                if fromNum <= n <= toNum:
                    num_rand_list.append(n)
                    i += 1

            cont = 0
            while cont < 2147483647:
                n = float(a * num_rand_list[i - 1] + c) % m

                if fromNum <= n <= toNum:
                    num_rand_list.append(n)
                    i += 1

                if i >= num_quantity:
                    break
                cont += 1

            for j in range(len(num_rand_list)):
                num_rand_list[j] /= float(toNum)

            return num_rand_list
        else:
            raise Exception("Some parameters got errors.")

    # Test
    def midTest(self, num_random_list, a, alpha):
        inter_conf = []

        desv_tipic = float(1 / 12)
        x_media_value = self.x_media(num_random_list)
        z = distributions.normal_distribution(1 - (alpha / 2))
        inter_conf.append(x_media_value - desv_tipic / math.sqrt(len(num_random_list)) * z)
        inter_conf.append(x_media_value + desv_tipic / math.sqrt(len(num_random_list)) * z)

        return inter_conf[0] < x_media_value < inter_conf[1]

    def varianceTest(self, num_random_list, alpha, n):
        S_square = (1 / (float)(n - 1)) * self.sum_variance(self, num_random_list)
        list = [distributions.ji_squared_distribution(alpha / 2, n - 1) / (12 * (n - 1)),
                distributions.ji_squared_distribution(1 - (alpha / 2), n - 1) / (12 * (n - 1))]

        return list[1] < S_square < list[0]

    def independenceTest(self, num_random_list, alpha):

        sign = []
        Xn = num_random_list[0]

        for i in range(1, len(num_random_list)):

            if num_random_list[i] < Xn:
                sign.append("-")
            else:
                if num_random_list[i] > Xn:
                    sign.append("+")
                else:
                    sign.append(sign[i - 1])
            Xn = num_random_list[i]

        h = 0

        for i in range(1, len(sign)):
            if sign[i] != sign[i - 1]:
                h += 1

        e = (2 * len(num_random_list) - 1) / float(3)
        v = (16 * len(num_random_list) - 29) / float(90)
        Zc = (h - e) / math.sqrt(v)

        return Zc > distributions.normal_distribution(alpha / 2)
        
    def shapeTest(self, num_random_list, alpha):
        num_random_list.sort()
        list = []
        interval = len(num_random_list) / 5
        interval_rest = len(num_random_list) % 5
        cont = 0
    
        for i in range(0, int(interval) - 1):
            aux = []
            for j in range(0, 5):
                aux.append(num_random_list[cont])
                cont += 1
            list.append(aux)
    
        if interval_rest != 0:
            lenght = 5 + interval_rest
        else:
            lenght = 5
    
        aux = []
    
        for i in range(lenght):
            aux.append(num_random_list[cont])
            cont += 1
    
        list.append(aux)
    
        # calculate Ei
    
        ei = []
    
        ei.append(len(num_random_list) * (list[0][len(list[0]) - 1]) - list[0][0])  # whos is this?
    
        for i in range(1 ,len(list)):
            ei.append(len(num_random_list) * (list[i][len(list[i]) - 1] - list[i - 1][len(list[i - 1]) - 1]))
    
        chi = []
    
        for i in range(len(list)):
            chi.append(math.pow(len(list[i]) - ei[i], 2) / ei[i])
    
        sumChi = 0
    
        for item in chi:
            sumChi += item
    
        return sumChi > distributions.ji_squared_distribution(alpha, len(list) - 1 - 2)


def generate_random():
    a = random.randint(0, 2147483647)
    res = '0.' + str(a)
    return float(res)


if __name__ == '__main__':

    st = stats()

    print("Opciones: \n")
    print("1) Numeros Aleatorios que cumplan con todas las pruebas. ")
    print("2) Numeros Aleatorios que cumplan con la Prueba de la Media. ")
    print("3) Numeros Aleatorios que cumplan con la Prueba de la Varianza. ")
    print("4) Numeros Aleatorios que cumplan con la Prueba de Forma. ")
    print("5) Numeros Aleatorios que cumplan con la Prueba de la Independencia. ")
    option = int(input("Escoja: "))

    if option == 1:
        cant_num = int(input("Entre la cantidad de numeros: (>5) "))
        alpha = float(input("Entre el valor de alpha: "))

        media = False
        varianza = False
        forma = False
        independencia = False

        print("Realizando las Pruebas......")

        while not (media and varianza and independencia and forma):
            m = 2147483647
            c = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            a = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            seed = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            num_rand_list = st.random_num_congr(seed, a, c, m, cant_num, True)
            media = st.midTest(num_rand_list, a, alpha)
            varianza = st.varianceTest(num_rand_list, alpha, len(num_rand_list))
            independencia = st.independenceTest(num_rand_list, alpha)
            forma = st.shapeTest(num_rand_list, alpha)

            if media and varianza and independencia and forma:
                for item in num_rand_list:
                    print(item)
                break

    if option == 2:
        cant_num = int(input("Entre la cantidad de numeros: (>5) "))
        alpha = float(input("Entre el valor de alpha: "))

        media = False

        print("Realizando la prueba.......")

        while not media:
            m = 2147483647
            c = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            a = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            seed = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            num_rand_list = st.random_num_congr(seed, a, c, m, cant_num, True)
            media = st.midTest(num_rand_list, a, alpha)

            if media:
                for item in num_rand_list:
                    print(item)
                break

    if option == 3:
        cant_num = int(input("Entre la cantidad de numeros: (>5) "))
        alpha = float(input("Entre el valor de alpha: "))

        varianza = False

        print("Realizando la prueba.......")

        while not varianza:
            m = 2147483647
            c = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            a = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            seed = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            num_rand_list = st.random_num_congr(seed, a, c, m, cant_num, True)

            varianza = st.varianceTest(num_rand_list, alpha, len(num_rand_list))

            if varianza:
                for item in num_rand_list:
                    print(item)
                break

    if option == 4:
        cant_num = int(input("Entre la cantidad de numeros: (>5) "))
        alpha = float(input("Entre el valor de alpha: "))

        forma = False

        print("Realizando la prueba.......")

        while not forma:
            m = 2147483647
            c = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            a = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            seed = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            num_rand_list = st.random_num_congr(seed, a, c, m, cant_num, True)

            forma = st.shapeTest(num_rand_list, alpha)

            if forma:
                for item in num_rand_list:
                    print(item)
                break

    if option == 5:
        cant_num = int(input("Entre la cantidad de numeros: (>5) "))
        alpha = float(input("Entre el valor de alpha: "))

        independencia = False

        print("Realizando la prueba.......")

        while not independencia:
            m = 2147483647
            c = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            a = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            seed = int(math.floor(generate_random() * (m / 2 - 0) + 0))
            num_rand_list = st.random_num_congr(seed, a, c, m, cant_num, True)

            independencia = st.independenceTest(num_rand_list, alpha)

            if independencia:
                for item in num_rand_list:
                    print(item)
                break