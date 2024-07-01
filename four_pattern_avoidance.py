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
#   2024/07/01: Ryan Maguire                                                   #
#       General clean up, got rid of pylint warnings.                          #
################################################################################
"""

# Pylint incorrectly thinks sage does not have the StandardTableaux class.
# Disable this warning.
# pylint: disable = no-member

# 20240507. An attempt to improve user friendliness.
# input n and Lambda, return nonnesting_pat
# Note: takes time, can only do repeated patterns of length 4
import time
import itertools
import collections
import sage.all

def gen_nonnesting(index):
    """
        Generates list of non-nesting permutations.
    """

    # Generate the list of nonnesting permutations
    multiset = list(range(1, index + 1))
    per = list(set(itertools.permutations(multiset)))
    tab_list = []

    # Iterate through the sublists of the standard Young tableaux.
    for sublist in sage.all.StandardTableaux([index, index]).list():

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
    """
        Given a four-element word pattern = abcd, with a, b, c, and d
        being 2-bit integers (0 <= a, b, c, d <= 3), splits the pattern into
        a, b, c, d and returns the list [a, b, c, d].
    """

    # Bit-wise and with 3 = 0x03 gives the bottom two bits.
    low = pattern & 0x03

    # Bit-shift down and use bit-wise and to get the remaining elements.
    mid_low = (pattern >> 2) & 0x03
    mid_high = (pattern >> 4) & 0x03
    high = (pattern >> 6) & 0x03

    return [high, mid_high, mid_low, low]

def diff_sign(left, right):
    """
        Computes the sign of the difference of two integers.
    """
    if left < right:
        return 1

    if left > right:
        return -1

    return 0

def get_word_diffs(pattern):
    """
        Given a pattern, such as "1123", computes the sign of
        the differences for each pair of elements. The order is increasing
        lexicographically, so (first slot, third slot) comes after
        (zeroth slot, second slot). For "1123" we would get

            word_diff = [
                0, # 1 - 1 = 0
                1, # 2 - 1 > 0
                1, # 3 - 1 > 0
                1, # 2 - 1 > 0
                1, # 3 - 1 > 0
                1, # 3 - 2 > 0
            ]

        This can probably be improved. For a pattern with word length n,
        this returns a list of length n * (n + 1) / 2. We can probably
        get away with a list of O(n) somehow, but this hasn't been explored.
    """
    word = get_word(pattern)

    # Loop through the elements lexicographically.
    return [
        diff_sign(word[left_index], word[right_index])
        for left_index in range(3)
        for right_index in range(left_index + 1, 4)
    ]

def nonnesting_avoid(index, avoid):
    """
        Counts how many times a pattern is avoided.
    """
    nonnesting = gen_nonnesting(index)

    # Remove patterns.
    list_2n = list(range(1, 2*index + 1))
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
for value in range(7):
    start_time = time.time()
    print(len(nonnesting_avoid(value, [0b01011011, 0b10110101, 0b10010111])))
    print(f"--- {time.time() - start_time} seconds ---")
