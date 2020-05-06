l1 = [1,2,3]
l2 = [4,5,6]
r = l1+l2

gset = [1,2,3,4,5,6,7,8,9,10]

a = sorted(list(set(gset).difference(set(r))))
print (a)
