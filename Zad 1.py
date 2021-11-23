class Aho_corasick:  
    def __init__(self):  
        self.goto = {}
        self.out = []
        self.breaks = None
        
    def __repr__(self):
        p = self.out
        print(p)

def make_trie(words):  #tworzenie drzewa
    root = Aho_corasick()  #obiekt klasy Aho

    for word in words:  #każdego słowa we wzorcach wykorzystujemy do stworzenia drzewa
        point = root
        for letter in word: 
            point = point.goto.setdefault(letter, Aho_corasick()) #tworzenie dicta
        point.out.append(word)
    return root

def bfs(words): 
    root = make_trie(words) 
    q = [] #tworzymy kolejkę
    for point in iter(root.goto.values()): #iterując po elementach dicta tworzymy kolejkę do szukania wszerz
        q.append(point)
        point.breaks = root # stworzenie failedlinków

    while q:
        rightpoint = q.pop(0) #szukamy wszerz po węzłach

        for node, unique_point in rightpoint.goto.items():
            q.append(unique_point)
            firstpoint = rightpoint.breaks
            while firstpoint is not None and node not in firstpoint.goto:
                firstpoint = firstpoint.breaks
            unique_point.breaks = firstpoint.goto[node] if firstpoint else root
            unique_point.out = unique_point.out + unique_point.breaks.out
    point = root

def search_pattern(text, call): #szukamy wzorca
    root = make_trie(words) 
    point = root
    for i in range(len(text)): 
        while point is not None and text[i] not in point.goto:
            point = point.breaks
        if point == None:
            point = root
        if text[i] in point.goto:
            point = point.goto[text[i]]
        for word in point.out:
            call(word,i - len(word) + 1)


def found( words, loc):  # wypisywanie rezultatu
    print("Wzorzec {} znaleziono na pozycji {}".format(words, loc))

words = ['abb', 'ab','cał']
text = "abbcał"
search_pattern(text, found)