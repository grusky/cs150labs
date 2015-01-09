
def findStrings(letters, sofar = [], current = '') :
    if current in words:
        print("found", current)
    if len(letters) == 0 :
        if current in words :
            print(' '.join(sofar),current)
    else :
        if current in words :
            findStrings(letters, sofar + [current])
        for c in letters[0] :
            findStrings(letters[1:], sofar, current+c)
            


def main() :
    global words
    nums = ['o','i','abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']
    f = open('dict3.txt','r')
    text = f.read()
    wordlist = text.split("\n")
    words = set(wordlist)
    ph = input("  Enter your phone number: ")
    letters = []
    for c in ph :
        if 48 <= ord(c) and ord(c) < 58 :
            letters.append(nums[ord(c)-48])
    print(letters)
    findStrings(letters)
    

    
main()