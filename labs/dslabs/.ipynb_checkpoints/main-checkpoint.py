import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats


def main():
    """Основной выполняемый скрипт"""

    ds = pd.read_csv('train_buildings.csv')
    # print(ds.columns.tolist())

    # Функции текстового описания датасета
    # print(ds.describe())
    # print(ds.head())
    # print(ds['Rooms'])
    # print(ds.Rooms)  # Другой способ вызова
    # print(f"Mean no. of rooms  = {ds['Rooms'].mean()}")
    # print(f"Median no. of rooms = {ds['Rooms'].median()}")
    # print(f"Mode of rooms = {ds['Rooms'].mode()[0]}")

    # Функции графического описания датасета
    # Гистограммы
    # sns.displot(ds['Square'])
    # sns.displot(ds['Rooms'])
    # sns.displot(ds['Price'])

    # Плотности Распределения
    # sns.kdeplot(ds['Square'], shade=True, legend=False)
    # sns.kdeplot(ds['Rooms'], shade=True, legend=False)
    sns.kdeplot(ds['Price'], shade=True, legend=False)

    # Коробка с усами (чего???)
    # sns.boxplot(ds['Square'])
    # sns.boxplot(ds['Rooms'])
    # sns.boxplot(ds['Price'])

    # Парные плотности
    # my_cols = ['Square', 'Rooms', "Price"]
    # sns.plot = sns.pairplot(ds[my_cols])

    # Регрессия + плотности
    # grid = sns.jointplot(data=ds, x='Square', y='Price', kind='reg')

    # Парные корреляции
    # cols = ds.columns.tolist()
    # corr_matrix = ds[cols].corr()
    # corr_matrix = np.round(corr_matrix, 2)
    # corr_matrix[np.abs(corr_matrix) < 0.3] = 0
    # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

    plt.show()

    # Обработка пропусков
    # missing_num = ds.isnull().sum()
    # print(missing_num)

    # lifesquare_med = ds['LifeSquare'].median()
    # ds['LifeSquare'] = ds['LifeSquare'].fillna(lifesquare_med)
    # Healthcare_1_med = ds['Healthcare_1'].median()
    # ds['Healthcare_1'] = ds['Healthcare_1'].fillna(Healthcare_1_med)
    # missing_num = ds.isnull().sum()
    # print(missing_num)

    # Обработка выбросов
    # Второй датасет: накинуть пропусков и выбросов, обработать. прислать отчет на почту vl.arefin@gmail.com


if __name__ == '__main__':
    main()
