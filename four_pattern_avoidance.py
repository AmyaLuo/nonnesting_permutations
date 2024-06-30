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
#                               Revision History                               #
################################################################################
#   2024/06/30: Ryan Maguire                                                   #
#       Avoiding multiple if-then statements.                                  #
################################################################################
"""

# 20240507. An attempt to improve user friendliness.
# input n and Lambda, return nonnesting_pat
# Note: takes time, can only do repeated patterns of length 4
import time
import itertools
import collections
from sage.all_cmdline import *

def gen_nonnesting(n):

    # Generate the list of nonnesting permutations
    multiset = list(range(1, n + 1))
    per = list(set(itertools.permutations(multiset)))
    tab_list = []

    # Iterate through the sublists of the standard Young tableaux.
    for sublist in StandardTableaux([n, n]).list():

        # Transpose the sublist to get elements at the same index
        transposed_sublist = list(map(list, zip(*sublist)))
        tab_list.append(transposed_sublist)

    # Get nonnesting.
    nonnesting_list = [
        [v for _, v in sorted((p, v) for v, pv in zip(v1, v2) for p in pv)]
        for v1 in per
        for v2 in tab_list
    ]

    return [tuple(sublist) for sublist in nonnesting_list]

def get_word(pattern):
    d = pattern & 0x03
    c = (pattern >> 2) & 0x03
    b = (pattern >> 4) & 0x03
    a = (pattern >> 6) & 0x03

    return [a, b, c, d]

def diff_sign(x, y):
    diff = y - x

    if diff > 0:
        return 1

    if diff < 0:
        return -1

    return 0

def get_word_diffs(pattern):
    word = get_word(pattern)
    word_diff = [
        diff_sign(word[0], word[1]),
        diff_sign(word[0], word[2]),
        diff_sign(word[0], word[3]),
        diff_sign(word[1], word[2]),
        diff_sign(word[1], word[3]),
        diff_sign(word[2], word[3])
    ]

    return word_diff

def nonnesting_avoid(n, avoid):
    nonnesting = gen_nonnesting(n)

    # Remove patterns.
    list_2n = list(range(1, 2*n + 1))
    com = list(itertools.combinations(list_2n, 4))
    cnt_pat = collections.Counter(nonnesting)
    word_diffs = [get_word_diffs(pattern) for pattern in avoid]

    for j in nonnesting:
        for i in range(len(com)):
            in_list = [com[i][k] - 1 for k in range(4)]

            in_diff = [
                diff_sign(j[in_list[0]], j[in_list[1]]),
                diff_sign(j[in_list[0]], j[in_list[2]]),
                diff_sign(j[in_list[0]], j[in_list[3]]),
                diff_sign(j[in_list[1]], j[in_list[2]]),
                diff_sign(j[in_list[1]], j[in_list[3]]),
                diff_sign(j[in_list[2]], j[in_list[3]])
            ]

            for word_diff in word_diffs:
                if word_diff == in_diff:
                    cnt_pat[j] += 1

            if cnt_pat[j] > 1:
                break

    nonnesting_pat = []
    for i in cnt_pat.elements():
        if cnt_pat[i] == 1:
            nonnesting_pat.append(i)

    return nonnesting_pat

# 1123, 2311, 2113
for n in range(7):
    start_time = time.time()
    print(len(nonnesting_avoid(n, [0b01011011, 0b10110101, 0b10010111])))
    print("--- %s seconds ---" % (time.time() - start_time))
