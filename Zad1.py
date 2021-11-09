class Aho:  
    def __init__(self):  
        self.goto = {}
        self.out = []
        self.breaks = None

def make_trie(words):  #tworzenie drzewa
    root = Aho()  

    for word in words:
        point = root
        for letter in word:
            point = point.goto.setdefault(letter, Aho())
        point.out.append(word)
    return root

def find(y, words):  #szukamy w słowie wzorca
    root = make_trie(words)  
    q = []
    for point in iter(root.goto.values()):
        q.append(point)
        point.breaks = root

    while len(q) > 0:
        rightpoint = q.pop(0)

        for clue, uniquepoint in iter(rightpoint.goto.items()):
            q.append(uniquepoint)
            firstpoint = rightpoint.breaks
            while firstpoint != None and not clue in firstpoint.goto:
                firstpoint = firstpoint.breaks
            uniquepoint.breaks = firstpoint.goto[clue] if firstpoint else root
            uniquepoint.out += uniquepoint.breaks.out
    point = root

    for i in range(len(y)):
        while point != None and y[i] not in point.goto:
            point = point.breaks
        if point == None:
            point = root
            continue
        point = point.goto[y[i]]
        for design in point.out:
            print("The Design found at position %s to %s, found pattern: %s" % (i - len(design) + 1, i, design))

words = ['a', 'ab', 'aa', 'abc', 'bc', 'bca', 'cc', 'c', 'cba', 'cab']
y = "abcbaacab"
find(y, words)