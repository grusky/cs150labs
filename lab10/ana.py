
def contains(s, w) :
    for c in w :
        if c in s :
            s = s.replace(c,'',1)
            w = w.replace(c,'',1)
        else :
            return False, s
    return True, s

def grams(s, words, builtlist = []) :
    if s != '' :
        for w in words :
            b, remains = contains(s, w)
            if b and len(builtlist) < 3:
                grams(remains, words, builtlist + [w])
    else :
        print(' '.join(builtlist))
            


def main() :
    
    f = open('words3.txt','r')
    text = f.read()
    words = text.split("\n")
    #pruned = {}
    pruned = []
    s = "bellmanford"
    for w in words :
        b, r = contains(s, w)
        if b and len(w) >= 2:
            pruned.append(w)
            #print(w)
            #pruned[w] = None
    print(len(words))
    print(len(pruned))
    #print(' '.join(pruned))
    grams(s, pruned)
    

    
main()