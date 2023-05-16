import pandas
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
Logic for the first block of data-sets regarding brand-specific information.
It combines the information from the single months into one big sql-table.

Every entry from the original sets is extended to include the month and year it describes.
The names of the columns are in german to make it easier to find the corresponding entries in the originals. 
"""
columnNames = ['Marke', 'Modellreihe', 'Insgesamt', 'mit Dieselantrieb', 'Hybridantrieb (gesamt)', 'Hybridantrieb (Benzin)', 'Hybridantrieb (Diesel)', 'Plugin-Hybridantrieb (gesamt)', 'Plugin-Hybridantrieb (Benzin)', 'Plugin-Hybridantrieb (Diesel)', 'Elektroantrieb', 'Allradantrieb', 'Cabriolets']

def read_brand_datafile_xls(url: str, sheet_index: int) -> pandas.DataFrame:
    dataset = pandas.read_excel(url,sheet_name=sheet_index, engine='xlrd', usecols='B,C,D,G,J,M,P,S', skiprows=8, skipfooter=7)
    return dataset

def read_brand_datafile_xlsx_until_end_2020(url: str, sheet_index: str) -> pandas.DataFrame:
    dataset = pandas.read_excel(url,sheet_name=sheet_index, engine='openpyxl', usecols='B,C,D,G,J,M,P,S', skiprows=8, skipfooter=2)
    return dataset

def read_brand_datafile_xlsx_after_2020(url: str, sheet_name: str) -> pandas.DataFrame:
    dataset = pandas.read_excel(url,sheet_name=sheet_name, engine='openpyxl', usecols='B,C,D,G,S,V,Y,AB,AE,AH,AK,AN,AQ', skiprows=8, skipfooter=2)
    return dataset

def modify_brand_dataset_until_end_2020(dataset: pandas.DataFrame, year: int, month: int): 
    dataset.columns.values[0] = columnNames[0]
    dataset.columns.values[1] = columnNames[1]
    dataset.columns.values[2] = columnNames[2]
    dataset.columns.values[3] = columnNames[3]
    dataset.columns.values[4] = columnNames[4]
    dataset.columns.values[5] = columnNames[10]
    dataset.columns.values[6] = columnNames[11]
    dataset.columns.values[7] = columnNames[12]
    dataset.insert(5, columnNames[5], '-')
    dataset.insert(6, columnNames[6], '-')
    dataset.insert(7, columnNames[7], '-')
    dataset.insert(8, columnNames[8], '-')
    dataset.insert(9, columnNames[9], '-')
    
    
    dataset.insert(2, 'Jahr', year)
    dataset.insert(3, 'Monat', month)

    dataset['Marke'].ffill(inplace=True)  

    dataset.replace('-', 0, inplace=True)

def modify_brand_dataset_after_2020(dataset: pandas.DataFrame, year: int, month: int): 
    dataset.columns.values[0] = columnNames[0]
    dataset.columns.values[1] = columnNames[1]
    dataset.columns.values[2] = columnNames[2]
    dataset.columns.values[3] = columnNames[3]
    dataset.columns.values[4] = columnNames[4]
    dataset.columns.values[5] = columnNames[5]
    dataset.columns.values[6] = columnNames[6]
    dataset.columns.values[7] = columnNames[7]
    dataset.columns.values[8] = columnNames[8]
    dataset.columns.values[9] = columnNames[9]
    dataset.columns.values[10] = columnNames[10]
    dataset.columns.values[11] = columnNames[11]
    dataset.columns.values[12] = columnNames[12]
    
    dataset.insert(2, 'Jahr', year)
    dataset.insert(3, 'Monat', month)

    dataset['Marke'].ffill(inplace=True)    

    dataset.replace('-', 0, inplace=True)

def prepare_brand_dataset_xls(url: str, sheet_name: str, year: int, month: int) -> pandas.DataFrame:
    dataset = read_brand_datafile_xls(url, sheet_name)

    modify_brand_dataset_until_end_2020(dataset, year, month)

    return dataset

def prepare_brand_dataset_until_end_2020(url: str, sheet_index: str, year: int, month: int) -> pandas.DataFrame:
    dataset = read_brand_datafile_xlsx_until_end_2020(url, sheet_index)
    
    modify_brand_dataset_until_end_2020(dataset, year, month)

    return dataset

def prepare_brand_dataset_after_2020(url: str, sheet_name: str, year: int, month: int) -> pandas.DataFrame:
    dataset = read_brand_datafile_xlsx_after_2020(url, sheet_name)
    modify_brand_dataset_after_2020(dataset, year, month)

    return dataset

def combine_brand_datasets(datasets) -> pandas.DataFrame:
    dataset = pandas.concat(datasets)
    dataset.sort_values(by=['Marke', 'Modellreihe', 'Jahr', 'Monat'], inplace=True)

    return dataset

def get_brand_dataset_for_2023() -> pandas.DataFrame:
    dataset2023_01 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_01.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2023, 1)
    dataset2023_02 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_02.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2023, 2)
    dataset2023_03 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_03.xlsx?__blob=publicationFile&v=2', 'FZ 10.1', 2023, 3)

    dataset2023 = combine_brand_datasets([dataset2023_01, dataset2023_02, dataset2023_03])

    return dataset2023

def get_brand_dataset_for_2022() -> pandas.DataFrame:
    dataset2022_01 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_01.xlsx?__blob=publicationFile&v=8', 'FZ10.1', 2022, 1)
    dataset2022_02 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_02.xlsx?__blob=publicationFile&v=6', 'FZ10.1', 2022, 2)
    dataset2022_03 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_03.xlsx?__blob=publicationFile&v=4', 'FZ10.1', 2022, 3)
    dataset2022_04 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_04.xlsx?__blob=publicationFile&v=7', 'FZ10.1', 2022, 4)
    dataset2022_05 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_05.xlsx?__blob=publicationFile&v=5', 'FZ10.1', 2022, 5)
    dataset2022_06 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_06.xlsx?__blob=publicationFile&v=4', 'FZ10.1', 2022, 6)
    dataset2022_07 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_07.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2022, 7)
    dataset2022_08 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_08.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2022, 8)
    dataset2022_09 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_09.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2022, 9)
    dataset2022_10 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_10.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2022, 10)
    dataset2022_11 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_11.xlsx?__blob=publicationFile&v=5', 'FZ10.1', 2022, 11)
    dataset2022_12 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_12.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2022, 12)

    dataset2022 = combine_brand_datasets([
        dataset2022_01, 
        dataset2022_02, 
        dataset2022_03, 
        dataset2022_04, 
        dataset2022_05, 
        dataset2022_06, 
        dataset2022_07, 
        dataset2022_08, 
        dataset2022_09, 
        dataset2022_10,
        dataset2022_11,
        dataset2022_12
    ])

    return dataset2022

def get_brand_dataset_for_2021() -> pandas.DataFrame:
    dataset2021_01 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_01.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2021, 1)
    dataset2021_02 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_02.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2021, 2)
    dataset2021_03 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_03.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2021, 3)
    dataset2021_04 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_04.xlsx?__blob=publicationFile&v=6', 'FZ10.1', 2021, 4)
    dataset2021_05 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_05.xlsx?__blob=publicationFile&v=5', 'FZ10.1', 2021, 5)
    dataset2021_06 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_06.xlsx?__blob=publicationFile&v=4', 'FZ10.1', 2021, 6)
    dataset2021_07 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_07.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2021, 7)
    dataset2021_08 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_08.xlsx?__blob=publicationFile&v=8', 'FZ10.1', 2021, 8)
    dataset2021_09 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_09.xlsx?__blob=publicationFile&v=5', 'FZ10.1', 2021, 9)
    dataset2021_10 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_10.xlsx?__blob=publicationFile&v=2', 'FZ10.1', 2021, 10)
    dataset2021_11 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_11.xlsx?__blob=publicationFile&v=3', 'FZ10.1', 2021, 11)
    dataset2021_12 = prepare_brand_dataset_after_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_12.xlsx?__blob=publicationFile&v=7', 'FZ10.1', 2021, 12)

    dataset2021 = combine_brand_datasets([
        dataset2021_01, 
        dataset2021_02, 
        dataset2021_03, 
        dataset2021_04, 
        dataset2021_05, 
        dataset2021_06, 
        dataset2021_07, 
        dataset2021_08, 
        dataset2021_09, 
        dataset2021_10,
        dataset2021_11,
        dataset2021_12
    ])
    
    return dataset2021

def get_brand_dataset_for_2020() -> pandas.DataFrame:
    dataset2020_01 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_01_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 1)
    dataset2020_02 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_02_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 2)
    dataset2020_03 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_03_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 3)
    dataset2020_04 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_04_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 4)
    dataset2020_05 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_05_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 5)
    dataset2020_06 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_06_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 6)
    dataset2020_07 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_07_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 7)
    dataset2020_08 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_08_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 8)
    dataset2020_09 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_09_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 9)
    dataset2020_10 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_10_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 10)
    dataset2020_11 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_11_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 11)
    dataset2020_12 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_12_xlsx.xlsx?__blob=publicationFile&v=2', 3, 2020, 12)

    dataset2020 = combine_brand_datasets([
        dataset2020_01, 
        dataset2020_02, 
        dataset2020_03, 
        dataset2020_04, 
        dataset2020_05, 
        dataset2020_06, 
        dataset2020_07, 
        dataset2020_08, 
        dataset2020_09, 
        dataset2020_10,
        dataset2020_11,
        dataset2020_12
    ])
    
    return dataset2020

def get_brand_dataset_for_2019() -> pandas.DataFrame:
    # Improvement: Checkout why the name of the worksheet does not work.
    dataset2019_01 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_01_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 1)
    dataset2019_02 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_02_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 2)
    dataset2019_03 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_03_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 3)
    dataset2019_04 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_04_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 4)
    dataset2019_05 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_05_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 5)
    dataset2019_06 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_06_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 6)
    dataset2019_07 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_07_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 7)
    dataset2019_08 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_08_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 8)
    dataset2019_09 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_09_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 9)
    dataset2019_10 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_10_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 10)
    dataset2019_11 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_11_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 11)
    dataset2019_12 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_12_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2019, 12)

    dataset2019 = combine_brand_datasets([
        dataset2019_01, 
        dataset2019_02, 
        dataset2019_03, 
        dataset2019_04, 
        dataset2019_05, 
        dataset2019_06, 
        dataset2019_07, 
        dataset2019_08, 
        dataset2019_09, 
        dataset2019_10,
        dataset2019_11,
        dataset2019_12
    ])
    
    return dataset2019

def get_brand_dataset_for_2018() -> pandas.DataFrame:
    dataset2018_01 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_01_xls.xls?__blob=publicationFile&v=2', 1, 2018, 1)
    dataset2018_02 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_02_xls.xls?__blob=publicationFile&v=2', 1, 2018, 2)
    dataset2018_03 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_03_xls.xls?__blob=publicationFile&v=2', 1, 2018, 3)
    dataset2018_04 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_04_xls.xls?__blob=publicationFile&v=2', 1, 2018, 4)
    dataset2018_05 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_05_xls.xls?__blob=publicationFile&v=2', 1, 2018, 5)
    dataset2018_06 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_06_xls.xls?__blob=publicationFile&v=2', 1, 2018, 6)
    dataset2018_07 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_07_xls.xls?__blob=publicationFile&v=2', 1, 2018, 7)
    dataset2018_08 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_08_xls.xls?__blob=publicationFile&v=2', 1, 2018, 8)
    dataset2018_09 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_09_xls.xls?__blob=publicationFile&v=2', 1, 2018, 9)
    dataset2018_10 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_10_xls.xls?__blob=publicationFile&v=3', 1, 2018, 10)
    dataset2018_11 = prepare_brand_dataset_xls('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_11_xls.xls?__blob=publicationFile&v=2', 1, 2018, 11)
    dataset2018_12 = prepare_brand_dataset_until_end_2020('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_12_xlsx.xlsx?__blob=publicationFile&v=2', 1, 2018, 12)

    dataset2018 = combine_brand_datasets([
        dataset2018_01, 
        dataset2018_02, 
        dataset2018_03, 
        dataset2018_04, 
        dataset2018_05, 
        dataset2018_06, 
        dataset2018_07, 
        dataset2018_08, 
        dataset2018_09, 
        dataset2018_10,
        dataset2018_11,
        dataset2018_12
    ])
    
    return dataset2018

def update_brand_dataset():
    branddataset2018 = get_brand_dataset_for_2018()
    branddataset2019 = get_brand_dataset_for_2019()
    branddataset2020 = get_brand_dataset_for_2020()
    branddataset2021 = get_brand_dataset_for_2021()
    branddataset2022 = get_brand_dataset_for_2022()
    branddataset2023 = get_brand_dataset_for_2023()

    branddataset = combine_brand_datasets([
        branddataset2018,
        branddataset2019,
        branddataset2020,
        branddataset2021,
        branddataset2022,
        branddataset2023
    ])

    branddataset.to_sql('brand-statistics', f'sqlite:///{CURRENT_DIR}/data.sqlite', if_exists='replace', index=False)

"""
Logic for the second block of data-sets regarding information regarding the federal states.
It combines the information from the single months into one big sql-table.

Every entry from the original sets is extended to include the month and year it describes.
The names of the columns are in german to make it easier to find the corresponding entries in the originals. 
"""

federal_state_columnNames = [
    'Bundesland',
    'Anzahl (gesamt)',
    'Anzahl (alternativer Antrieb)',
    'Anzahl (Elektro-Antrieb)',
    'Anzahl (BEV)',
    'Anzahl (Brennstoffzelle)',
    'Anzahl (Plug-in-Hybrid)',
    'Anzahl (Hybrid)',
    'Anzahl (Voll-Hybrid)',
    'Anzahl (Benzin-Hybrid)',
    'Anzahl (Benzin-Voll-Hybrid)',
    'Anzahl (Diesel-Hybrid)',
    'Anzahl (Diesel-Voll-Hybrid)',
    'Anzahl (Gas)',
    'Anzahl (Wasserstoff)'
]

def read_federal_state_datafile_2021(url: str, sheet_name: str) -> pandas.DataFrame:
    dataset = pandas.read_excel(url,sheet_name=sheet_name, engine='openpyxl', usecols='B,C,D,F,H:O', skiprows=11, nrows=18)
    return dataset

def read_federal_state_datafile(url: str, sheet_name: str) -> pandas.DataFrame:
    dataset = pandas.read_excel(url,sheet_name=sheet_name, engine='openpyxl', usecols='B,C,D,F,H:R', skiprows=11, nrows=18)
    return dataset

def modify_federal_state_dataset_2021(dataset: pandas.DataFrame, year: int, month: int):
    dataset.columns.values[0] = federal_state_columnNames[0]
    dataset.columns.values[1] = federal_state_columnNames[1]
    dataset.columns.values[2] = federal_state_columnNames[2]
    dataset.columns.values[3] = federal_state_columnNames[3]
    dataset.columns.values[4] = federal_state_columnNames[4]
    dataset.columns.values[5] = federal_state_columnNames[5]
    dataset.columns.values[6] = federal_state_columnNames[6]
    dataset.columns.values[7] = federal_state_columnNames[7]
    dataset.columns.values[8] = federal_state_columnNames[9]
    dataset.columns.values[9] = federal_state_columnNames[11]
    dataset.columns.values[10] = federal_state_columnNames[13]
    dataset.columns.values[11] = federal_state_columnNames[14]
    
    dataset.insert(8, federal_state_columnNames[8], 0)
    dataset.insert(10, federal_state_columnNames[10], 0)
    dataset.insert(12, federal_state_columnNames[12], 0)

    dataset.insert(1, 'Jahr', year)
    dataset.insert(2, 'Monat', month)

    dataset.replace('-', 0, inplace=True)

def modify_federal_state_dataset(dataset: pandas.DataFrame, year: int, month: int):
    dataset.columns.values[0] = federal_state_columnNames[0]
    dataset.columns.values[1] = federal_state_columnNames[1]
    dataset.columns.values[2] = federal_state_columnNames[2]
    dataset.columns.values[3] = federal_state_columnNames[3]
    dataset.columns.values[4] = federal_state_columnNames[4]
    dataset.columns.values[5] = federal_state_columnNames[5]
    dataset.columns.values[6] = federal_state_columnNames[6]
    dataset.columns.values[7] = federal_state_columnNames[7]
    dataset.columns.values[8] = federal_state_columnNames[8]
    dataset.columns.values[9] = federal_state_columnNames[9]
    dataset.columns.values[10] = federal_state_columnNames[10]
    dataset.columns.values[11] = federal_state_columnNames[11]
    dataset.columns.values[12] = federal_state_columnNames[12]
    dataset.columns.values[13] = federal_state_columnNames[13]
    dataset.columns.values[14] = federal_state_columnNames[14]

    dataset.insert(1, 'Jahr', year)
    dataset.insert(2, 'Monat', month)

    dataset.replace('-', 0, inplace=True)

def prepare_federal_state_dataset_2021(url: str, year: int, month: int):
    dataset = read_federal_state_datafile_2021(url, 'FZ 28.9')

    modify_federal_state_dataset_2021(dataset, year, month)

    return dataset

def prepare_federal_state_dataset(url: str, year: int, month: int):
    dataset = read_federal_state_datafile(url, 'FZ 28.9')

    modify_federal_state_dataset(dataset, year, month)

    return dataset

def combine_federal_state_datasets(datasets) -> pandas.DataFrame:
    dataset = pandas.concat(datasets)

    return dataset

def get_federal_state_dataset_2023():
    federal_state_2023_01 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_01.xlsx?__blob=publicationFile&v=3', 2023, 1)
    federal_state_2023_02 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_02.xlsx?__blob=publicationFile&v=6', 2023, 2)
    federal_state_2023_03 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_03.xlsx?__blob=publicationFile&v=6', 2023, 3)

    return combine_federal_state_datasets([federal_state_2023_01, federal_state_2023_02, federal_state_2023_03])

def get_federal_state_dataset_2022():
    federal_state_2022_01 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_01.xlsx?__blob=publicationFile&v=7', 2022, 1)
    federal_state_2022_02 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_02.xlsx?__blob=publicationFile&v=9', 2022, 2)
    federal_state_2022_03 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_03.xlsx?__blob=publicationFile&v=5', 2022, 3)
    federal_state_2022_04 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_04.xlsx?__blob=publicationFile&v=5', 2022, 4)
    federal_state_2022_05 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_05.xlsx?__blob=publicationFile&v=6', 2022, 5)
    federal_state_2022_06 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_06.xlsx?__blob=publicationFile&v=8', 2022, 6)
    federal_state_2022_07 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_07.xlsx?__blob=publicationFile&v=6', 2022, 7)
    federal_state_2022_08 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_08.xlsx?__blob=publicationFile&v=5', 2022, 8)
    federal_state_2022_09 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_09.xlsx?__blob=publicationFile&v=4', 2022, 9)
    federal_state_2022_10 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_10.xlsx?__blob=publicationFile&v=4', 2022, 10)
    federal_state_2022_11 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_11.xlsx?__blob=publicationFile&v=7', 2022, 11)
    federal_state_2022_12 = prepare_federal_state_dataset('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_12.xlsx?__blob=publicationFile&v=6', 2022, 12)

    return combine_federal_state_datasets([
        federal_state_2022_01,
        federal_state_2022_02,
        federal_state_2022_03,
        federal_state_2022_04,
        federal_state_2022_05,
        federal_state_2022_06,
        federal_state_2022_07,
        federal_state_2022_08,
        federal_state_2022_09,
        federal_state_2022_10,
        federal_state_2022_11,
        federal_state_2022_12
    ])

def get_federal_state_dataset_2021():
    federal_state_2021_01 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_01.xlsx?__blob=publicationFile&v=4', 2021, 1)
    federal_state_2021_02 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_02.xlsx?__blob=publicationFile&v=4', 2021, 2)
    federal_state_2021_03 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_03.xlsx?__blob=publicationFile&v=4', 2021, 3)
    federal_state_2021_04 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_04.xlsx?__blob=publicationFile&v=5', 2021, 4)
    federal_state_2021_05 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_05.xlsx?__blob=publicationFile&v=6', 2021, 5)
    federal_state_2021_06 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_06.xlsx?__blob=publicationFile&v=4', 2021, 6)
    federal_state_2021_07 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_07.xlsx?__blob=publicationFile&v=3', 2021, 7)
    federal_state_2021_08 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_08.xlsx?__blob=publicationFile&v=4', 2021, 8)
    federal_state_2021_09 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_09.xlsx?__blob=publicationFile&v=2', 2021, 9)
    federal_state_2021_10 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_10.xlsx?__blob=publicationFile&v=7', 2021, 10)
    federal_state_2021_11 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_11.xlsx?__blob=publicationFile&v=6', 2021, 11)
    federal_state_2021_12 = prepare_federal_state_dataset_2021('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_12.xlsx?__blob=publicationFile&v=3', 2021, 12)

    return combine_federal_state_datasets([
        federal_state_2021_01,
        federal_state_2021_02,
        federal_state_2021_03,
        federal_state_2021_04,
        federal_state_2021_05,
        federal_state_2021_06,
        federal_state_2021_07,
        federal_state_2021_08,
        federal_state_2021_09,
        federal_state_2021_10,
        federal_state_2021_11,
        federal_state_2021_12
    ])

def update_federal_state_dataset():
    federal_state_dataset_2021 = get_federal_state_dataset_2021()
    federal_state_dataset_2022 = get_federal_state_dataset_2022()
    federal_state_dataset_2023 = get_federal_state_dataset_2023()

    federal_state_dataset = combine_federal_state_datasets([
        federal_state_dataset_2021, 
        federal_state_dataset_2022, 
        federal_state_dataset_2023
    ])

    federal_state_dataset.to_sql('federal-state-statistics',  f'sqlite:///{CURRENT_DIR}/data.sqlite', if_exists='replace', index=False)

update_brand_dataset()
update_federal_state_dataset()