import re

if __name__ == '__main__':

    filename = "potop.txt"
    f = open(filename, "r", encoding='utf-8')
    f = f.read() #sprobuj zamienic miejscami
    f = f.lower() 
    patterns = r'[0-9]'
    non_alphabetical = r'[^\w]'
    f = re.sub(patterns, " ", f)
    f = re.sub(non_alphabetical, " ", f)
    f = re.split(r'\s+', f)

    freq = {}
    for w in f:
        if w not in freq:
            freq[w] = 0
        freq[w] += 1

    max_freq = max(freq.values())
    

    for w in freq:
        if freq[w] == max_freq:
            print("Słowo \"%s\" wystąpiło najwięszką ilość razy, czyli %s razy" % (w, max_freq))