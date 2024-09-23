from math import sqrt
from scipy.stats import norm


# calculating sample mean value
def sample_mean(X):
    summ = 0
    for item in X:
        summ += item

    return summ / len(X)


# Mann-Whitney characteristics function
def MW(X, Y):
    N1 = len(X)
    N2 = len(Y)
    # lengths of samples
    print(f'Valid N1 = {N1}')
    print(f'Valid N2 = {N2}')

    # avgs of samples basically
    print(f'Mean 1 = {sample_mean(X)}')
    print(f'Mean 2 = {sample_mean(Y)}')

    # making sorted => ranked list of variables
    ranked = []
    for item in X:
        tup = [item, 0, 1]
        ranked.append(tup)
    for item in Y:
        tup = [item, 0, 2]
        ranked.append(tup)
    ranked = sorted(ranked, key=lambda tupp: tupp[0])
    for i in range(len(ranked)):
        ranked[i][1] = i + 1

    # making avg indexes for equals
    # print(ranked)  # debug print (1)
    same_ids = [1]
    for i in range(len(ranked)):
        if ranked[i][0] == ranked[same_ids[0]][0] and i != same_ids[0] - 1 and i != len(ranked) - 1:
            same_ids.append(i + 1)
        elif i == len(ranked) - 1:  # case of last item in list
            # print(f'for i = {i}: {same_ids}')  # debug print (2)
            if ranked[i][0] == ranked[same_ids[0]][0]:
                same_ids.append(i + 1)
            avg = sample_mean(same_ids)
            for idd in same_ids:
                ranked[idd - 1][1] = avg
        elif i != same_ids[0] - 1:  # case of inequality
            # print(f'for i = {i}: {same_ids}')  # same debug (2)
            avg = sample_mean(same_ids)
            for idd in same_ids:
                ranked[idd - 1][1] = avg
            same_ids = [i + 1]
    # print(ranked)  # same debug print (1) showing that code above works

    # calculating summ of ranks by each of two groups
    R1 = 0
    R2 = 0
    for i in range(len(ranked)):
        if ranked[i][2] == 1:
            R1 += ranked[i][1]
        else:
            R2 += ranked[i][1]
    print(f'Summ of ranks R1 = {R1}')
    print(f'Summ of ranks R2 = {R2}')

    # FINALLY calculating U statistic
    U1 = N1 * N2 + N1 * (N1 + 1) / 2 - R1
    U2 = N1 * N2 + N2 * (N2 + 1) / 2 - R2
    if U1 > U2:
        U = U2
        print(f'U = {U}')
    else:
        U = U1
        print(f'U = {U}')

    # the Z statistic
    mu = N1 * N2 / 2
    sigma = sqrt(N1 * N2 * (N1 + N2 + 1) / 12)
    Z = (U - mu) / sigma
    print(f'Z = {Z}')
    # probability to get the same Z statistic if H0 is approved true
    p = 2 * norm.cdf(Z)
    print(f'p = {p}')

    return p


# our main function
def main():
    uab4 = [7, 3, 7, 5, 6, 5, 9, 7, 8, 9,
            6, 8, 8, 6, 7, 5, 5, 4, 8, 3,
            7, 5, 8, 6, 8, 7, 6, 4, 7, 8,
            7, 6, 3, 8, 9, 6, 8, 4, 3, 7,
            4, 8, 6, 5, 3, 6, 10, 4, 8, 7]
    uab6 = [4, 4, 9, 2, 3, 5, 7, 4, 5, 4,
            7, 6, 9, 4, 8, 6, 2, 5, 5, 4,
            4, 9, 5, 7, 8, 3, 6, 3, 5, 6,
            8, 7, 4, 4, 5, 2, 5, 4, 6, 5,
            4, 5, 6, 3, 8, 4, 8, 5, 5, 4]
    uab8 = [6, 2, 6, 4, 5, 4, 8, 6, 7, 8,
            5, 7, 7, 5, 6, 3, 4, 3, 7, 2,
            6, 4, 7, 5, 7, 6, 5, 3, 6, 7,
            6, 5, 2, 7, 8, 5, 7, 3, 2, 6,
            3, 7, 5, 4, 2, 5, 9, 3, 7, 2]

    print('UAB 4 vs UAB 6')
    MW(uab4, uab6)
    print('\nUAB 6 vs UAB 8')
    MW(uab6, uab8)


if __name__ == "__main__":
    main()
