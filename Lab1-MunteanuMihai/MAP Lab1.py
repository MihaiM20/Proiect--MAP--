def suma_primelor_100():
    return sum(range(1, 101))

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def cmmdc(a, b):
    while b:
        a, b = b, a % b
    return a

def an_bisect(an):
    return an % 4 == 0 and (an % 100 != 0 or an % 400 == 0)

def suma_si_media(lista):
    suma = sum(lista)
    media = suma / len(lista)
    return suma, media

def min_max_lista(lista):
    return min(lista), max(lista)

def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def rezolvare_ecuatie_gradul_2(a, b, c):
    delta = b**2 - 4*a*c
    if delta < 0:
        return "Ecuatia nu are solutii reale"
    elif delta == 0:
        x = -b / (2*a)
        return f"Ecuatia are o singura solutie: {x}"
    else:
        x1 = (-b + delta**0.5) / (2*a)
        x2 = (-b - delta**0.5) / (2*a)
        return f"Ecuatia are doua solutii: {x1} si {x2}"

def verificare_triunghi(a, b, c):
    return a + b > c and a + c > b and b + c > a

def main():
    print("Selectati exercitiul dorit:")
    print("1. Suma primelor 100 de numere naturale")
    print("2. Factorialul unui numar introdus")
    print("3. CMMDC al doua numere introduse")
    print("4. Verificare an bisect")
    print("5. Suma si media unei liste")
    print("6. Cel mai mic si cel mai mare numar dintr-o lista")
    print("7. Sortare lista prin metoda bubble sort")
    print("8. Rezolvare ecuatie de gradul al doilea")
    print("9. Verificare daca trei numere pot forma un triunghi")

    optiune = int(input("Introduceti optiunea: "))

    if optiune == 1:
        print("Suma primelor 100 de numere naturale este:", suma_primelor_100())
    elif optiune == 2:
        n = int(input("Introduceti un numar: "))
        print(f"Factorialul lui {n} este:", factorial(n))
    elif optiune == 3:
        a = int(input("Introduceti primul numar: "))
        b = int(input("Introduceti al doilea numar: "))
        print(f"CMMDC al lui {a} si {b} este:", cmmdc(a, b))
    elif optiune == 4:
        an = int(input("Introduceti anul: "))
        print(f"Anul {an} este bisect:", an_bisect(an))
    elif optiune == 5:
        lista = list(map(int, input("Introduceti elementele listei separate prin spatiu: ").split()))
        suma, media = suma_si_media(lista)
        print(f"Suma elementelor listei este: {suma}, iar media este: {media}")
    elif optiune == 6:
        lista = list(map(int, input("Introduceti elementele listei separate prin spatiu: ").split()))
        minim, maxim = min_max_lista(lista)
        print(f"Cel mai mic numar din lista este: {minim}, iar cel mai mare este: {maxim}")
    elif optiune == 7:
        lista = list(map(int, input("Introduceti elementele listei separate prin spatiu: ").split()))
        print("Lista sortata este:", bubble_sort(lista))
    elif optiune == 8:
        a = float(input("Introduceti coeficientul a: "))
        b = float(input("Introduceti coeficientul b: "))
        c = float(input("Introduceti coeficientul c: "))
        print(rezolvare_ecuatie_gradul_2(a, b, c))
    elif optiune == 9:
        a = float(input("Introduceti primul numar: "))
        b = float(input("Introduceti al doilea numar: "))
        c = float(input("Introduceti al treilea numar: "))
        print("Numerele pot forma un triunghi:", verificare_triunghi(a, b, c))
    else:
        print("Optiune invalida!")

if __name__ == "__main__":
    main()
