import math as m
import statistics
from scipy.stats import norm, probplot, kstest, shapiro, chi2_contingency, skew, kurtosis, sem
import matplotlib.pyplot as plt


# calculating sample mean value
def sample_mean(X):
    summ = 0
    for item in X:
        summ += item
    summ = summ / len(X)

    return summ


# calculating sample unshifted dispersion value
def sample_disp(X):
    mean = sample_mean(X)

    summ = 0
    for item in X:
        summ += (item - mean) ** 2
    summ = summ / (len(X) - 1)

    return m.sqrt(summ)


# calculating Kolmagorov-Smirnov
def k_s(X):
    exp_value, disp = norm.fit(X)
    d, p = kstest(X, norm(exp_value, disp).cdf)

    return d, p


# calculating Shapiro-Wilk
def shap(X):
    d, p = shapiro(X)
    return d, p


# calculating Chi-Squared
def c_s(X):
    exp_value, disp = norm.fit(X)
    d, p, f, _ = chi2_contingency([X, norm(exp_value, disp).cdf])

    return d, p, f


# function for histogram building
def histogram(X):
    L = m.ceil(m.sqrt(len(X)))

    # fitting into normal distribution
    # expected value and dispersion:
    exp_value, disp = norm.fit(X)
    normal = norm.pdf(X, exp_value, disp)

    # configure X axis label
    delta = (max(X) - min(X)) / L
    histXAxis = [round(min(X) + delta * i, 2) for i in range(L + 1)]

    # configure both plots and histogram with title and X ticks
    plt.plot(X, normal, 'r', linewidth=2)
    plt.hist(X, bins=L, density=True, color='b', edgecolor='black')
    plt.title(f"Expected value = {round(exp_value, 2)}, dispersion = {round(disp, 2)}")
    plt.xticks(histXAxis)
    plt.show()


# function for bar plot of function distribution
def sample_distribution(X):
    L = m.ceil(m.sqrt(len(X)))

    # fitting into normal distribution
    # expected value and dispersion:
    exp_value, disp = norm.fit(X)
    normal = norm.cdf(X, exp_value, disp)
    plt.hist(X, L, density=True, cumulative=True, color='b', edgecolor='black')
    plt.plot(X, normal, 'r', linewidth=2)
    plt.show()


# comparing actual value to expected one
def lin_graph(X):
    probplot(X, plot=plt)
    plt.show()


# main execution script
def main():
    # my variant is 5
    input_data = [6.4, 7.0, 7.4, 7.6, 8.0, 8.0,
                  8.2, 8.6, 8.7, 9.3, 10.0, 10.0,
                  10.0, 10.4, 11.0, 12.0, 12.0, 12.0,
                  12.5, 14.5, 15.0, 15.0, 15.4, 15.4,
                  17.0, 17.0, 17.0, 17.3, 17.4, 17.5,
                  17.6, 17.7, 18.0, 18.0, 18.0, 18.0,
                  18.0, 18.2, 18.5, 18.6, 19.7, 20.0,
                  20.0, 20.0, 20.3, 20.8, 21.8, 22.4,
                  22.6, 22.7, 23.0, 23.0, 23.4, 23.8,
                  24.0, 24.5, 24.6, 24.8, 25.4, 25.8,
                  26.0, 26.2, 26.3, 28.3, 28.8, 30.1,
                  30.2, 32.0, 32.0, 32.5, 38.0, 42.4,
                  45.0, 46.0]

    # getting sample statistics
    print(f'Sample mean = {sample_mean(input_data)}')
    print(f'Sample Unshifted dispersion = {sample_disp(input_data)}')
    print(f'N = {len(input_data)}')
    print(f'Min = {min(input_data)}')
    print(f'Max = {max(input_data)}')
    print(f'Median = {statistics.median(input_data)}')
    print(f'Mode = {statistics.mode(input_data)}')
    print(f'Variance = {statistics.stdev(input_data)}')
    print(f'Standard error = {sem(input_data)}')
    print(f'Skewness = {skew(input_data)}')
    print(f'Kurtosis = {kurtosis(input_data)}')

    # calculating Kolmagorov-Smirnov
    print('Kolmagorov-Smirnov:')
    d, p = k_s(input_data)
    print(f"D = {d}, p = {p}")  # Kolmagorov-Smirnov

    # calculating Chi-Squared
    # print('Chi-Squared:')
    # print(c_s(input_data))  # X^2  # Chi-squared

    # calculating Shapiro-Wilk
    # d, p = shap(input_data)
    # print('Shapiro-Wilk:')
    # print(f'D = {d}, p = {p}')

    # histogram plot with normal distribution on top of it
    histogram(input_data)

    # sample distribution as bar plot
    sample_distribution(input_data)

    # plot with expected and real values referring to normal distribution
    lin_graph(input_data)


# preventing unwanted script runs
if __name__ == "__main__":
    main()
