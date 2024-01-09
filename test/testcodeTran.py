def find_primeroot(p):
    nroot=[]
    root=[]
    for i in range(2,p):
        for j in range(2,p-1):
            if i**j%p==1:
                nroot.append(i)
                break
            elif j+1==p-1:
                root.append(i)
                break
    print("primary root:",root,len(root))
    print(nroot,len(nroot))
find_primeroot(11)
