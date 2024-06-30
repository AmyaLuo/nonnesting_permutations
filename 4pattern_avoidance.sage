"""
################################################################################
#                                   LICENSE                                    #
################################################################################
#   This file is part of nonnesting_permtuation.                               #
#                                                                              #
#   nonnesting_permtuations is free software: you can redistribute it and/or   #
#   modify it under the terms of the GNU General Public License as published   #
#   by the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                        #
#                                                                              #
#   nonnesting_permtuations is distributed in the hope that it will be useful, #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License          #
#   along with nonnesting_permtuations.  If not, see                           #
#   <https://www.gnu.org/licenses/>.                                           #
################################################################################
#   Purpose:                                                                   #
#       Find the set of nonnesting permutations that avoid some patterns       #
################################################################################
#   Author:     Amya Luo                                                       #
#   Date:       May 28, 2024.                                                  #
################################################################################
"""
# 05072024. An attempt to improve user friendliness of test_sage.sage
# input n and Lambda, return nonnesting_pat
# Note: takes time, can only do repeated patterns of length 4
from itertools import permutations
from itertools import combinations
from collections import Counter
import time

start_time = time.time()

def gen_nonnesting(n):
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

    #Get nonnesting
    nonnesting_list = [ [v for _,v in sorted((p,v) for v,pv in zip(v1,v2) for p in pv)]
            for v1 in per
            for v2 in tab_list]

    nonnesting=[tuple(sublist) for sublist in nonnesting_list]
    return nonnesting

def nonnesting_avoid(n,avoid):
    nonnesting = gen_nonnesting(n)
    #Remove patterns
    list_2n = list(range(1, 2*n+1))
    com = list(combinations(list_2n, 4))
    cnt_pat = Counter(nonnesting)
    for j in nonnesting:
        for i, tuples in enumerate(com):
            in1 = com[i][0] - 1
            in2 = com[i][1] - 1
            in3 = com[i][2] - 1
            in4 = com[i][3] - 1
            # Check for each pattern
            if 1123 in avoid:
                if j[in1]==j[in2] and j[in1]<j[in3] and j[in3]<j[in4]:
                    cnt_pat[j]+=1
            if 1223 in avoid:
                if j[in3]==j[in2] and j[in1]<j[in3] and j[in3]<j[in4]:
                    cnt_pat[j]+=1
            if 1233 in avoid:
                if j[in3]==j[in4] and j[in1]<j[in2] and j[in2]<j[in4]:
                    cnt_pat[j]+=1
            if 1132 in avoid:
                if j[in1]==j[in2] and j[in1]<j[in4] and j[in4]<j[in3]:
                    cnt_pat[j]+=1
            if 1332 in avoid:
                if j[in3]==j[in2] and j[in1]<j[in4] and j[in4]<j[in3]:
                    cnt_pat[j]+=1
            if 1322 in avoid:
                if j[in3]==j[in4] and j[in1]<j[in4] and j[in4]<j[in2]:
                    cnt_pat[j]+=1
            if 2213 in avoid:
                if j[in1]==j[in2] and j[in3]<j[in1] and j[in1]<j[in4]:
                    cnt_pat[j]+=1
            if 2113 in avoid:
                if j[in3]==j[in2] and j[in2]<j[in1] and j[in1]<j[in4]:
                    cnt_pat[j]+=1
            if 2133 in avoid:
                if j[in3]==j[in4] and j[in2]<j[in1] and j[in1]<j[in4]:
                    cnt_pat[j]+=1
            if 2231 in avoid:
                if j[in1]==j[in2] and j[in4]<j[in1] and j[in1]<j[in3]:
                    cnt_pat[j]+=1
            if 2331 in avoid:
                if j[in3]==j[in2] and j[in4]<j[in1] and j[in1]<j[in3]:
                    cnt_pat[j]+=1
            if 2311 in avoid:
                if j[in3]==j[in4] and j[in4]<j[in1] and j[in1]<j[in2]:
                    cnt_pat[j]+=1
            if 3312 in avoid:
                if j[in1]==j[in2] and j[in3]<j[in4] and j[in4]<j[in1]:
                    cnt_pat[j]+=1
            if 3112 in avoid:
                if j[in3]==j[in2] and j[in3]<j[in4] and j[in4]<j[in1]:
                    cnt_pat[j]+=1
            if 3122 in avoid:
                if j[in3]==j[in4] and j[in2]<j[in4] and j[in4]<j[in1]:
                    cnt_pat[j]+=1
            if 3321 in avoid:
                if j[in1]==j[in2] and j[in4]<j[in3] and j[in3]<j[in1]:
                    cnt_pat[j]+=1
            if 3221 in avoid:
                if j[in3]==j[in2] and j[in4]<j[in3] and j[in3]<j[in1]:
                    cnt_pat[j]+=1
            if 3211 in avoid:
                if j[in3]==j[in4] and j[in4]<j[in2] and j[in2]<j[in1]:
                    cnt_pat[j]+=1
            if cnt_pat[j]>1:
                break
                
    nonnesting_pat = []
    for i in cnt_pat.elements():
        if cnt_pat[i] == 1:
            nonnesting_pat.append(i)
    return nonnesting_pat
    # return cnt_pat

print(len(nonnesting_avoid(6,[1123,2311,2113])))
print("--- %s seconds ---" % (time.time() - start_time))