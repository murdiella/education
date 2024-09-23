import numpy as np
import matplotlib.pyplot as plt
from data import values
from INS_and_SNS import INS, SNS


def simulate_flight_plan():
    ins = INS()
    initial_latitude = values['latitude']['value']
    initial_longitude = values['longitude']['value']
    ins.preparation()
    time = np.arange(0, 100, 0.1)
    latitude = initial_latitude + 10 * np.cos(0.1 * time)
    longitude = initial_longitude + 15 * np.cos(0.15 * time)
    ins.preparation()
    return latitude, longitude


def simulate_flight_ins():
    ins = INS()
    initial_latitude_ins = values['latitude']['value']
    initial_longitude_ins = values['longitude']['value']
    ins.preparation()

    time = np.arange(0, 100, 0.1)
    sq_error = 0.0001*time^2 - 0.0005*time


    latitude_ins = initial_latitude_ins + 10 * np.cos(0.1 * time) + sq_error
    longitude_ins = initial_longitude_ins + 15 * np.cos(0.15 * time) + sq_error

    return latitude_ins, longitude_ins


def simulate_flight_sns():
    sns = SNS()
    initial_latitude_sns = values['latitude']['value']
    initial_longitude_sns = values['longitude']['value']
    sns.preparation()

    time = np.arange(0, 100, 0.1)

    # Погрешность боротовой аппаратуры
    app_error = np.random.normal(0, 0.0004, len(time))
    # Погрешность, вызванная ионосферной задержкой
    ion_error = np.random.normal(0, 0.0005, len(time))
    # Погрешность вызванная тропосферной задержкой
    trop_error = np.random.normal(0, 0.0005, len(time))
    # Погрешность, вызванная внутренними шумами приёмника
    vn_error = np.random.normal(0, 0.0002, len(time))


    latitude_sns = initial_latitude_sns + 10 * np.cos(0.1 * time) + app_error + ion_error + trop_error + vn_error
    longitude_sns = initial_longitude_sns + 15 * np.cos(0.15 * time) + app_error + ion_error + trop_error + vn_error




    return latitude_sns, longitude_sns

def plot_flight_coordinates_plan(latitude, longitude):
    plt.figure(figsize=(12, 8))
    plt.plot(longitude, latitude, label='Latitude', color='b')
    plt.title('Plan')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.legend()
    plt.grid()
    plt.show()


def plot_flight_coordinates(latitude_ins, longitude_ins, sns_or_ins):
    plt.figure(figsize=(12, 8))
    plt.plot(longitude_ins, latitude_ins, label='Latitude', color='b')
    plt.title(f'Simulated Flight Coordinates With Error({sns_or_ins})')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.legend()
    plt.grid()
    plt.show()

latitude, longitude = simulate_flight_plan()
plot_flight_coordinates_plan(latitude, longitude)

latitude_ins, longitude_ins = simulate_flight_ins()
plot_flight_coordinates(latitude_ins, longitude_ins, "ins")

latitude_sns, longitude_sns = simulate_flight_sns()
plot_flight_coordinates(latitude_sns, longitude_sns, 'sns')

