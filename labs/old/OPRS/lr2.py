import math as m
from statistics import stdev
from scipy.stats import norm, kstest, ttest_ind, chisquare, f
import matplotlib.pyplot as plt


# calculating sample mean value
def sample_mean(X):
    summ = 0
    for item in X:
        summ += item
    summ = summ / len(X)

    return summ


# calculating Kolmagorov-Smirnov
def k_s(X):
    exp_value, disp = norm.fit(X)
    d, p = kstest(X, norm(exp_value, disp).cdf)

    return d, p


# function for single histogram building
def histogram(X):
    L = m.ceil(m.sqrt(len(X)))

    # fitting into normal distribution
    # expected value and dispersion:
    exp_value, disp = norm.fit(X)
    X = sorted(X)
    normal = norm.pdf(X, exp_value, disp)

    # configure X axis label
    delta = (max(X) - min(X)) / L
    histXAxis = [round(min(X) + delta * i, 2) for i in range(L)]
    histXAxis.append(max(X))

    # probs = []
    # for i in range(L):
    #     probs.append(norm(exp_value, disp).cdf(histXAxis[i+1]) - norm(exp_value, disp).cdf(histXAxis[i]))
    # print(probs)
    # print(sum(probs))

    # configure both plots and histogram with title and X ticks
    plt.plot(X, normal, 'r', linewidth=2)
    plt.hist(X, bins=L, density=True, color='b', edgecolor='black')
    plt.title(f"Expected value = {round(exp_value, 2)}, dispersion = {round(disp, 2)}")
    plt.xticks(histXAxis)
    plt.show()


# chi-square test
def chi2(X):
    exp = norm.cdf(X)
    d, p = chisquare(X, f_exp=exp)
    return d, p


# ttest and some other calculations to output (for sample means)
def ttest_combo(X, Y):
    d, p = ttest_ind(X, Y)
    print(f'd = {d}, p = {p}, df = {len(X) + len(Y) - 2}')
    print(f'N1 = {len(X)}, N2 = {len(Y)}')
    print(f'Sample mean 1 = {sample_mean(X)}, Sample mean 2 = {sample_mean(Y)}')
    print(f'Std. Deviation 1 = {stdev(X)}, Std. Deviation 2 = {stdev(Y)}\n')


# Fisher's statistics (for std. dev's)
def fisher(X, Y, alpha=0.05):
    F = []
    for i in range(len(X)):
        F.append(X[i]/Y[i])
    df1 = len(X) - 1
    df2 = len(Y) - 1
    p = f.cdf(F, df1, df2)
    f_stat = stdev(X) ** 2/stdev(Y) ** 2
    for item in p:
        if item > alpha:
            return f'Std. Deviations are statistically unequal. f = {f_stat}'
    return f'Std.Deviations are statistically equal. f = {f_stat}'


def main():
    uab4 = [0.75, 0.68, 0.7, 0.74, 0.68, 0.67, 0.72,
            0.69, 0.67, 0.73, 0.76, 0.73, 0.71, 0.72,
            0.72, 0.71, 0.69, 0.75, 0.77, 0.7, 0.79,
            0.78, 0.69, 0.67, 0.64, 0.66, 0.69, 0.79,
            0.66, 0.71, 0.7, 0.71, 0.72, 0.72, 0.67,
            0.7, 0.79, 0.76, 0.73, 0.66, 0.71, 0.69,
            0.69, 0.66, 0.67, 0.82, 0.68, 0.7, 0.68, 0.66]
    uab6 = [0.81, 0.8, 0.78, 0.8, 0.79, 0.8, 0.8, 0.82,
            0.78, 0.81, 0.79, 0.81, 0.8, 0.78, 0.79, 0.8,
            0.8, 0.79, 0.8, 0.81, 0.78, 0.81, 0.79, 0.82,
            0.8, 0.81, 0.82, 0.81, 0.81, 0.81, 0.8, 0.8,
            0.82, 0.8, 0.79, 0.79, 0.8, 0.79, 0.77, 0.79,
            0.79, 0.81, 0.77, 0.79, 0.82, 0.8, 0.81, 0.78, 0.79, 0.8]
    uab8 = [0.54, 0.53, 0.51, 0.56, 0.49, 0.48, 0.48, 0.55,
            0.47, 0.5, 0.51, 0.52, 0.57, 0.49, 0.41, 0.54,
            0.5, 0.49, 0.51, 0.47, 0.52, 0.47, 0.49, 0.49,
            0.53, 0.51, 0.54, 0.5, 0.39, 0.55, 0.47, 0.47,
            0.51, 0.57, 0.52, 0.46, 0.48, 0.5, 0.5, 0.41,
            0.5, 0.5, 0.48, 0.47, 0.42, 0.42, 0.46, 0.5, 0.53, 0.45]

    # KS tests and histograms for all samples
    d, p = k_s(uab4)
    print(f'UAB 4: d = {d}, p = {p}, min = {min(uab4)}, max = {max(uab4)}')
    histogram(uab4)
    d, p = k_s(uab6)
    print(f'UAB 6: d = {d}, p = {p}, min = {min(uab6)}, max = {max(uab6)}')
    histogram(uab6)
    d, p = k_s(uab8)
    print(f'UAB 8: d = {d}, p = {p}, min = {min(uab8)}, max = {max(uab8)}')
    histogram(uab8)

    print('UAB 4 vs UAB 6:')
    ttest_combo(uab4, uab6)
    result = fisher(uab4, uab6)
    print(f'Fishers result: {result}')

    print('UAB 6 vs UAB 8:')
    ttest_combo(uab6, uab8)
    result = fisher(uab6, uab8)
    print(f'Fishers result: {result}')

    # print(chi2(uab4))
    # print(chi2(uab6))
    # print(chi2(uab8))


if __name__ == "__main__":
    main()
