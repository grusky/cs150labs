
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
        count = 0
        for w in words :
            b, remains = contains(s, w)
            if b and len(builtlist) < 3:
                count = count + grams(remains, words, builtlist + [w])
        return count
    else :
        print(' '.join(builtlist))
        return 1
            


def main() :
    
    words = []
    f = open('words1.txt','r')
    text = f.read()
    words.append(set(text.split()))
    f = open('words2.txt','r')
    text = f.read()
    words.append(set(text.split()))
    f = open('words3.txt','r')
    text = f.read()
    words.append(set(text.split()))
    f = open('words4.txt','r')
    text = f.read()
    words.append(set(text.split()))
    words[2] = words[2]&words[3]
    f = open('scrabble.txt','r')
    text = f.read()
    words.append(set(text.split()))
    print(len(words[2]))
    print(len(words[3]))
    print(len(words[4]))
    print(len(words[2]&words[4]))
    words[2] = words[2]&words[4]
    s = "oberlinstudent"
    for i in range(1) :
        i = 2
        wordlist = words[i]
        pruned = []
        for w in wordlist :
            b, r = contains(s, w)
            if b and len(w) >= 4:
                pruned.append(w)
        
        print("Word list",i,"prodcued",grams(s, pruned),"anagrams.")
        print("It had",len(wordlist),"words,",len(pruned),"after pruning.")
    
    

main()