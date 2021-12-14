import re

if __name__ == '__main__':  # chodziło o napisanie _funkcji_

    filename = "potop.txt"
    f = open(filename, "r", encoding='utf-8')   # a kto zamknie plik?
    f = f.read()    # cały plik do pamięci
    f = f.lower() 
    patterns = r'[0-9]'
    non_alphabetical = r'[^\w]'
    f = re.sub(patterns, " ", f)
    f = re.sub(non_alphabetical, " ", f)
    f = re.split(r'\s+', f)

    freq = {}
    for w in f:
        if w not in freq:   # polecam Counter albo chociaż defaultdict
            freq[w] = 0
        freq[w] += 1

    s = sorted(freq.values(), reverse= True)
    s = list(dict.fromkeys(s))  # co ma na celu ta linijka?

    n = 2
    list1 = []
    count = 1
    for i in s:
        if count <= n:
            list1.append(i)
        count = count + 1
    print(list1)
    for value in list1:
        for key in freq.keys():
            if freq[key] == value:
                print("Słowo \"{}\" wystąpiło {} razy".format(key, value))  # źle traktuje remisy