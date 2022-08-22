import numpy as np

xkcd_limit = 2340
K = 40

dict_elos = {}
for i in range(1, xkcd_limit):
    dict_elos[str(i)] = 1500


def new_rating(old_rating, expected, result, k_value):
    return old_rating + k_value * (result - expected)


def expected_result(rating, opp_rating):
    return 1 / (1 + 10 ** ((opp_rating - rating)/400))


with open('xkcd_h2h.csv', 'r') as f:
    for line in f:
        line.strip()
        comics = line.split()

        A = comics[0]
        B = comics[1]

        A_ELO = dict_elos[A]
        B_ELO = dict_elos[B]

        A_expect = expected_result(A_ELO, B_ELO)
        B_expect = expected_result(B_ELO, A_ELO)

        dict_elos[A] = new_rating(A_ELO, A_expect, 1, K)
        dict_elos[B] = new_rating(B_ELO, B_expect, 1, K)

np.save('xkcd_elo.npy', dict_elos)
