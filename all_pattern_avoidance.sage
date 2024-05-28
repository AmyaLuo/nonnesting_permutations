from itertools import permutations
from itertools import combinations
from collections import Counter
import time

start_time = time.time()
n=6
# Generate the list of nonnesting permutations
multiset = list(range(1,n+1))
per = list(set(permutations(multiset)))

# Generate the list of SYT
ST=StandardTableaux([n,n])
lst=ST.list()

tab_list = []

# Iterate through the sublists
for sublist in lst:
    # Transpose the sublist to get elements at the same index
    transposed_sublist = list(map(list, zip(*sublist)))
    
    tab_list.append(transposed_sublist)

# lst1=[[[1,2],[2,1]]]
# lst2=[[[1,3],[2,4]],[[1,4],[2,3]]]
#Get nonnesting
nonnesting_list = [ [v for _,v in sorted((p,v) for v,pv in zip(v1,v2) for p in pv)]
           for v1 in per
           for v2 in tab_list]

nonnesting=[tuple(sublist) for sublist in nonnesting_list]


#Remove patterns
list_2n = list(range(1, 2*n+1))
com = list(combinations(list_2n, 4))
cnt_pat = Counter(nonnesting)
for i, tuples in enumerate(com):
    in1 = com[i][0] - 1
    in2 = com[i][1] - 1
    in3 = com[i][2] - 1
    in4 = com[i][3] - 1
    for j in nonnesting:
        # # identify undesired patterns
        if j[in1]==j[in2] and j[in1]<j[in3] and j[in3]<j[in4]:
            cnt_pat[j]+=1
        # elif j[in3]==j[in4] and j[in1]<j[in3] and j[in3]<j[in2]:
        #     cnt_pat[j]+=1
        if j[in3]==j[in4] and j[in3]<j[in1] and j[in1]<j[in2]:
            cnt_pat[j]+=1
        if j[in3]==j[in2] and j[in3]<j[in1] and j[in1]<j[in4]:
            cnt_pat[j]+=1
        # elif j[in3]==j[in2] and j[in1]<j[in2] and j[in2]<j[in4]:
        #     cnt_pat[j]+=1
        # elif j[in2]==j[in3] and j[in1]<j[in4] and j[in4]<j[in2]:
        #     cnt_pat[j]+=1
            
nonnesting_pat = []
for i in cnt_pat.elements():
    if cnt_pat[i] == 1:
        nonnesting_pat.append(i)


# print(nonnesting_pat)
print(len(nonnesting_pat))
print("--- %s seconds ---" % (time.time() - start_time))