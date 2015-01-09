
def sort(n,X,H) :
    for i in range(n) :
        for j in range(n-1) :
            if X[j] > X[j+1] :
                X[j],X[j+1] = X[j+1],X[j]
                H[j],H[j+1] = H[j+1],H[j]

def solve(n,X,H) :
    sort(n,X,H)
    best = 0
    for i in range(n) :
        count = 1
        zoneEnd = X[i] + H[i]
        j = i+1
        while(j < n and zoneEnd > X[j]) :
            count = count+1
            zoneEnd = max(zoneEnd, X[j]+H[j])
            #print("right from tower",i,"hit tower",j,"zone ends at", zoneEnd, "count is",count)
            j = j + 1
        if count > best :
            best = count
    for i in range(n) :
        count = 1
        zoneEnd = X[i] - H[i]
        j = i-1
        while(j >= 0 and zoneEnd < X[j]) :
            count = count+1
            zoneEnd = min(zoneEnd, X[j]-H[j])
            #print("left from tower",i,"hit tower",j,"zone ends at", zoneEnd,"count is",count)
            j = j - 1
        if count > best :
            best = count        
    return best

def main() :
    
    f = open('input1.txt','r')
    n = eval(f.readline()[:-1])
    case = 1
    while n > 0 :
        L = f.readline()[:-1].split(' ')
        X = []
        H = []
        for i in range(n):
            X.append(eval(L[2*i]))
            H.append(eval(L[2*i+1]))
        #print(X)
        #print(H)
        print("Case",case,"can have",solve(n,X,H),"towers fall.")   
        case = case + 1
        n = eval(f.readline()[:-1])
        
        
main()