def clean(s) :
    news = ''
    for c in s :
        if c in "!,'-.?:;\n" :
            news = news + ""
        else :
            news = news + c.lower()
    #print(news)
    return news

def main() :
    cap = 10
    words = {}
    f = open('hamlet.txt','r')
    text = f.read()
    tlist = text.split(' ')
    for word in tlist :
        print (word, clean(word), "", sep='*')
        w = clean(word)
        if w in words :
            words[w] = words[w] + 1
        elif w != '' :
            words[w] = 1
    sortwords = []
    for w in words:
        i = 0
        while i < len(sortwords) and sortwords[i][1] > words[w]:
            i = i + 1
        sortwords.insert(i, (w, words[w]))
    
    print(sortwords)
    sortwords = sortwords[:cap]
    #print(sortwords)
    for i in range(cap) :
        sortwords[i] = sortwords[i][0]
    #print(sortwords)
    f = open('hamlet.txt','r')
    text = f.read()
    tlist = text.split(' ')
    for word in tlist :
        w = clean(word)
        if w not in sortwords :
            print(word, end=' ')
    print()
main()