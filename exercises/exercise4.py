import zipfile
import pandas
import os
import urllib.request as ur

# usecols = [ 'Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv' ]
# dtypes = { 'Geraet': int, 'Hersteller': str, 'Model': str, 'Monat': str, 'Temperatur in °C (DWD)': float, 'Batterietemperatur in °C': float, 'Geraet aktiv': str}
usecols = [ 0, 1, 2, 3, 4, 9, 10]
names = [ 'Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv' ]

def read_zipfile(url: str):
    localFileName, _ = ur.urlretrieve(url)
    with zipfile.ZipFile(localFileName) as zip:
        dataset = pandas.read_csv(
            zip.open('data.csv'),
            usecols=usecols,
            skipinitialspace=True,
            sep=';',
            decimal=',',
            names=names,
            header=0,
            true_values=['Ja'],
            false_values=['Nein']
        )

    return dataset

def rename_columns(dataset: pandas.DataFrame):
    renamed_dataset = dataset.copy()
    renamed_dataset.rename(columns={'Temperatur in °C (DWD)':'Temperatur', 'Batterietemperatur in °C':'Batterietemperatur'}, inplace=True)

    return renamed_dataset

def convert_temperature(dataset: pandas.DataFrame):
    converted_dataset = dataset.copy()
    converted_dataset['Temperatur'] = converted_dataset['Temperatur'] * 1.8 + 32
    converted_dataset['Batterietemperatur'] = converted_dataset['Batterietemperatur'] * 1.8 + 32

    return converted_dataset

def convert_active(dataset: pandas.DataFrame):
    converted_dataset = dataset.copy()
    converted_dataset['Geraet aktiv'] = converted_dataset['Geraet aktiv'] == 'Ja'

    return converted_dataset

def validate_entries(dataset: pandas.DataFrame):
    validated_dataset = dataset.copy()
    validated_dataset = validated_dataset[validated_dataset['Geraet'] > 0]

    return validated_dataset

def write_to_db(dataset: pandas.DataFrame):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset.to_sql('temperatures',  f'sqlite:///{CURRENT_DIR}/temperatures.sqlite', if_exists='replace', index=False)

dataset = read_zipfile('https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip')

dataset = rename_columns(dataset)

dataset = convert_temperature(dataset)

dataset = convert_active(dataset)

dataset = validate_entries(dataset)

write_to_db(dataset)