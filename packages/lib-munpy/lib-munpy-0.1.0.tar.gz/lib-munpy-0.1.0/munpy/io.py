import os
import numpy as np
import pandas as pd


def readBinary(filename: str, N_streets: int, dtype=np.float32, mode='array'):
    """
    Los outputs/inputs del modelo tienen la distribución (Nt, N_st)
    es decir pasos temporales X número de calles. Los binarios se cargan
    en un array de numpy justo con este formato. Si se desea se devuelven
    como dataframe.

    :param filename: archivo binario para decodificar.
    :param N_streets: número de calles de la simulación.
    :param dtype: tipo de dato guardado.
    :param mode: devolver como np.ndarray o como pd.DataFrame.
    :return: numpy.ndarray | pd.DataFrame
    """
    byte_size = np.dtype(dtype).itemsize
    Nt = int(
        os.stat(filename)[6] / byte_size / N_streets
    )
    length = Nt * N_streets
    data = np.fromfile(filename, dtype, length)
    data.shape = (Nt, N_streets)

    if mode == 'df':
        data = pd.DataFrame(data)

    return data


def dumpBinary(array: np.ndarray, filename: str):
    array.tofile(filename)


if __name__ == "__main__":

    att = '/home/ngomariz/data-munich/cartagena/results/NO.bin'
    dat = readBinary(att, 39)
    print(dat)

    # # # # METEOROLOGY
    # N_street, N_itner = 577, 433
    # meteo_dir = '/home/ngomariz/data-munich/data-case1/meteo'

    # street_meteo = [
    #     'WindDirection.bin', 'WindSpeed.bin', 'PBLH.bin',
    #     'UST.bin', 'LMO.bin', 'SurfaceTemperature.bin',
    #     'SurfacePressure.bin', 'SpecificHumidity.bin',
    #     'Rain.bin', 'Attenuation.bin', 'LiquidWaterContent.bin',
    #     'SolarRadiation.bin'
    # ]
    # intersection_meteo = [
    #     'WindDirectionInter.bin', 'WindSpeedInter.bin',
    #     'PBLHInter.bin', 'USTInter.bin', 'LMOInter.bin'
    # ]
    #
    # for stfile in street_meteo:
    #     stdata = readBinary(os.path.join(meteo_dir, stfile), N_streets=N_street)
    #     stdata_ctg = stdata[:30, :39]
    #     dumpBinary(stdata_ctg, f'/home/ngomariz/data-munich/cartagena/meteo/{stfile}')
    #
    # for interfile in intersection_meteo:
    #     interdata = readBinary(os.path.join(meteo_dir, interfile), N_streets=N_itner)
    #     interdata_ctg = interdata[:30, :25]
    #     dumpBinary(interdata_ctg, f'/home/ngomariz/data-munich/cartagena/meteo/{interfile}')
    #
    # # # # BACKGROUND CONCENTRATION
    # background_dir = '/home/ngomariz/data-munich/data-case1/background'
    # background_files = ['NO.bin', 'NO2.bin', 'O3.bin', 'PBC_3.bin']
    #
    # for bgfile in background_files:
    #     bgdata = readBinary(os.path.join(background_dir, bgfile), N_streets=N_street)
    #     bgdata_ctg = bgdata[:30, :39]
    #
    #     dumpBinary(bgdata_ctg, f'/home/ngomariz/data-munich/cartagena/background/{bgfile}')
    #
    # # # # Emission data
    # emission_dir = '/home/ngomariz/data-munich/data-case1/emission'
    # emission_files = ['NO.bin', 'NO2.bin', 'CO.bin', 'CH4.bin', 'FORM.bin']
    #
    # for emifile in emission_files:
    #     emidata = readBinary(os.path.join(emission_dir, emifile), N_streets=N_street)
    #     emidata_ctg = emidata[:30, :39]
    #
    #     dumpBinary(emidata_ctg, f'/home/ngomariz/data-munich/cartagena/emission/{emifile}')
