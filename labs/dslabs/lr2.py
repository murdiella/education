import numpy as np
import pandas as pd
import pickle   # сохранение модели
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_squared_error as mse, r2_score as r2
from IPython.display import Image

def main():
    df = pd.read_csv('newds.csv')
    # df.head()

    feature_names = ['Rooms', 'Square', 'LifeSquare', 'KitchenSquare', 'Floor', 'HouseFloor', 'HouseYear', 'Ecology_1',
                     'Social_1', 'Social_3', 'Healthcare_1', 'Helthcare_2', 'Shops_1']
    target_name = 'Price'
    df = df[feature_names + [target_name]]
    # df.head()

    feature_names_for_stand = df[feature_names].select_dtypes(include=['float32', 'float16', 'int64']).columns.tolist()
    scaler = StandardScaler()
    stand_features = scaler.fit_transform(df[feature_names_for_stand])


if __name__ == "__main__":
    main()
