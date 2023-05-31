import pandas
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
Logic for the first block of data-sets regarding brand-specific information.
It combines the information from the single months into one big sql-table.

Every entry from the original sets is extended to include the month and year it describes.
The names of the columns are in german to make it easier to find the corresponding entries in the originals. 
"""

class BrandDataSetInformation:
    def __init__(self, url:str, year:int, month:int, sheet_index: int, skiprows: int, skipfooter: int):
        self.url = url
        self.year = year
        self.month = month
        self.sheet_index = sheet_index
        self.skiprows = skiprows
        self.skipfooter = skipfooter

brand_datasets = [
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_01_xls.xls?__blob=publicationFile&v=2', 2018, 1, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_02_xls.xls?__blob=publicationFile&v=2', 2018, 2, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_03_xls.xls?__blob=publicationFile&v=2', 2018, 3, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_04_xls.xls?__blob=publicationFile&v=2', 2018, 4, 1, 9, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_05_xls.xls?__blob=publicationFile&v=2', 2018, 5, 1, 9, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_06_xls.xls?__blob=publicationFile&v=2', 2018, 6, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_07_xls.xls?__blob=publicationFile&v=2', 2018, 7, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_08_xls.xls?__blob=publicationFile&v=2', 2018, 8, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_09_xls.xls?__blob=publicationFile&v=2', 2018, 9, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_10_xls.xls?__blob=publicationFile&v=3', 2018, 10, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_11_xls.xls?__blob=publicationFile&v=2', 2018, 11, 1, 8, 7),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2018_12_xlsx.xlsx?__blob=publicationFile&v=2', 2018, 12, 1, 8, 2),

    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_01_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 1, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_02_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 2, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_03_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 3, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_04_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 4, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_05_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 5, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_06_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 6, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_07_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 7, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_08_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 8, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_09_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 9, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_10_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 10, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_11_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 11, 1, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2019_12_xlsx.xlsx?__blob=publicationFile&v=2', 2019, 12, 1, 8, 2),

    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_01_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 1, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_02_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 2, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_03_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 3, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_04_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 4, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_05_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 5, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_06_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 6, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_07_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 7, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_08_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 8, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_09_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 9, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_10_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 10, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_11_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 11, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2020_12_xlsx.xlsx?__blob=publicationFile&v=2', 2020, 12, 3, 8, 2),

    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_01.xlsx?__blob=publicationFile&v=2', 2021, 1, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_02.xlsx?__blob=publicationFile&v=2', 2021, 2, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_03.xlsx?__blob=publicationFile&v=2', 2021, 3, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_04.xlsx?__blob=publicationFile&v=6', 2021, 4, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_05.xlsx?__blob=publicationFile&v=5', 2021, 5, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_06.xlsx?__blob=publicationFile&v=4', 2021, 6, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_07.xlsx?__blob=publicationFile&v=3', 2021, 7, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_08.xlsx?__blob=publicationFile&v=8', 2021, 8, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_09.xlsx?__blob=publicationFile&v=5', 2021, 9, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_10.xlsx?__blob=publicationFile&v=2', 2021, 10, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_11.xlsx?__blob=publicationFile&v=3', 2021, 11, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2021_12.xlsx?__blob=publicationFile&v=7', 2021, 12, 3, 8, 2),
    
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_01.xlsx?__blob=publicationFile&v=8', 2022, 1, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_02.xlsx?__blob=publicationFile&v=6', 2022, 2, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_03.xlsx?__blob=publicationFile&v=4', 2022, 3, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_04.xlsx?__blob=publicationFile&v=7', 2022, 4, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_05.xlsx?__blob=publicationFile&v=5', 2022, 5, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_06.xlsx?__blob=publicationFile&v=4', 2022, 6, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_07.xlsx?__blob=publicationFile&v=3', 2022, 7, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_08.xlsx?__blob=publicationFile&v=2', 2022, 8, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_09.xlsx?__blob=publicationFile&v=3', 2022, 9, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_10.xlsx?__blob=publicationFile&v=2', 2022, 10, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_11.xlsx?__blob=publicationFile&v=5', 2022, 11, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2022_12.xlsx?__blob=publicationFile&v=3', 2022, 12, 3, 8, 2),

    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_01.xlsx?__blob=publicationFile&v=2', 2023, 1, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_02.xlsx?__blob=publicationFile&v=3', 2023, 2, 3, 8, 2),
    BrandDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/fz10_2023_03.xlsx?__blob=publicationFile&v=2', 2023, 3, 3, 8, 2),
]

columnNames = [
    'Marke',
    'Modellreihe',
    'Insgesamt',
    'mit Dieselantrieb',
    'Hybridantrieb (gesamt)',
    'Hybridantrieb (Benzin)',
    'Hybridantrieb (Diesel)',
    'Plugin-Hybridantrieb (gesamt)',
    'Plugin-Hybridantrieb (Benzin)',
    'Plugin-Hybridantrieb (Diesel)',
    'Elektroantrieb',
    'Allradantrieb',
    'Cabriolets'
]

def read_brand_datafile(url: str, year: int, month: int, sheet_index: int, skiprows: int, skipfooter: int):
    if year <= 2018 and month <= 11:
        dataset = pandas.read_excel(url,sheet_name=sheet_index, engine='xlrd', usecols='B,C,D,G,J,M,P,S', skiprows=skiprows, skipfooter=skipfooter)
    elif year <= 2020 and month <= 12:
        dataset = pandas.read_excel(url,sheet_name=sheet_index, engine='openpyxl', usecols='B,C,D,G,J,M,P,S', skiprows=skiprows, skipfooter=skipfooter)
    else:
        dataset = pandas.read_excel(url,sheet_name=sheet_index, engine='openpyxl', usecols='B,C,D,G,S,V,Y,AB,AE,AH,AK,AN,AQ', skiprows=skiprows, skipfooter=skipfooter)
    
    return dataset

def modify_brand_dataset(dataset: pandas.DataFrame, year: int, month: int):
    if year <= 2020 and month <= 12:
        dataset.columns.values[0] = columnNames[0]
        dataset.columns.values[1] = columnNames[1]
        dataset.columns.values[2] = columnNames[2]
        dataset.columns.values[3] = columnNames[3]
        dataset.columns.values[4] = columnNames[4]
        dataset.columns.values[5] = columnNames[10]
        dataset.columns.values[6] = columnNames[11]
        dataset.columns.values[7] = columnNames[12]
        dataset.insert(5, columnNames[5], 0)
        dataset.insert(6, columnNames[6], 0)
        dataset.insert(7, columnNames[7], 0)
        dataset.insert(8, columnNames[8], 0)
        dataset.insert(9, columnNames[9], 0)
    else:
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
    dataset.replace('/', 0, inplace=True)

    dataset.fillna(0, inplace=True)
    dataset[columnNames[1]].replace(0, '', inplace=True)

    dataset[columnNames[0]] = dataset[columnNames[0]].astype(str)
    dataset[columnNames[1]] = dataset[columnNames[1]].astype(str)
    dataset[columnNames[2]] = dataset[columnNames[2]].astype(int)
    dataset[columnNames[3]] = dataset[columnNames[3]].astype(int)
    dataset[columnNames[4]] = dataset[columnNames[4]].astype(int)
    dataset[columnNames[5]] = dataset[columnNames[5]].astype(int)
    dataset[columnNames[6]] = dataset[columnNames[6]].astype(int)
    dataset[columnNames[7]] = dataset[columnNames[7]].astype(int)
    dataset[columnNames[8]] = dataset[columnNames[8]].astype(int)
    dataset[columnNames[9]] = dataset[columnNames[9]].astype(int)
    dataset[columnNames[10]] = dataset[columnNames[10]].astype(int)
    dataset[columnNames[11]] = dataset[columnNames[11]].astype(int)
    dataset[columnNames[12]] = dataset[columnNames[12]].astype(int)

def get_polished_brand_dataset(url: str, sheet_index: int, year: int, month: int, skiprows: int, skipfooter: int) -> pandas.DataFrame:
    dataset = read_brand_datafile(url, year, month, sheet_index, skiprows, skipfooter)

    modify_brand_dataset(dataset, year, month)

    return dataset

def get_brand_datasets():
    datasets = []
    for info in brand_datasets:
        current_branddataset = get_polished_brand_dataset(info.url, info.sheet_index, info.year, info.month, info.skiprows, info.skipfooter)

        datasets.append(current_branddataset)
    
    branddataset = pandas.concat(datasets)
    branddataset.sort_values(by=['Marke', 'Modellreihe', 'Jahr', 'Monat'], inplace=True)

    branddataset.to_sql('brand-statistics', f'sqlite:///{CURRENT_DIR}/data.sqlite', if_exists='replace', index=False)

"""
Logic for the second block of data-sets regarding information regarding the federal states.
It combines the information from the single months into one big sql-table.

Every entry from the original sets is extended to include the month and year it describes.
The names of the columns are in german to make it easier to find the corresponding entries in the originals. 
"""

class FederalStateDataSetInformation:
    def __init__(self, url: str, sheet_name: str, year: int, month: int):
        self.url = url
        self.sheet_name = sheet_name
        self.year = year
        self.month = month

federal_state_datasets = [
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_01.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2021, 1),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_02.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2021, 2),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_03.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2021, 3),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_04.xlsx?__blob=publicationFile&v=5', 'FZ 28.9', 2021, 4),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_05.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2021, 5),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_06.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2021, 6),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_07.xlsx?__blob=publicationFile&v=3', 'FZ 28.9', 2021, 7),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_08.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2021, 8),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_09.xlsx?__blob=publicationFile&v=2', 'FZ 28.9', 2021, 9),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_10.xlsx?__blob=publicationFile&v=7', 'FZ 28.9', 2021, 10),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_11.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2021, 11),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2021_12.xlsx?__blob=publicationFile&v=3', 'FZ 28.9', 2021, 12),

    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_01.xlsx?__blob=publicationFile&v=7', 'FZ 28.9', 2022, 1),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_02.xlsx?__blob=publicationFile&v=9', 'FZ 28.9', 2022, 2),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_03.xlsx?__blob=publicationFile&v=5', 'FZ 28.9', 2022, 3),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_04.xlsx?__blob=publicationFile&v=5', 'FZ 28.9', 2022, 4),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_05.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2022, 5),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_06.xlsx?__blob=publicationFile&v=8', 'FZ 28.9', 2022, 6),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_07.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2022, 7),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_08.xlsx?__blob=publicationFile&v=5', 'FZ 28.9', 2022, 8),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_09.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2022, 9),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_10.xlsx?__blob=publicationFile&v=4', 'FZ 28.9', 2022, 10),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_11.xlsx?__blob=publicationFile&v=7', 'FZ 28.9', 2022, 11),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2022_12.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2022, 12),

    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_01.xlsx?__blob=publicationFile&v=3', 'FZ 28.9', 2023, 1),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_02.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2023, 2),
    FederalStateDataSetInformation('https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_03.xlsx?__blob=publicationFile&v=6', 'FZ 28.9', 2023, 3),
]

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

def read_federal_state_datafile(url: str, sheet_name: str, year: int) -> pandas.DataFrame:
    if year <= 2021:
        dataset = pandas.read_excel(url,sheet_name=sheet_name, engine='openpyxl', usecols='B,C,D,F,H:O', skiprows=11, nrows=18)
    else:
        dataset = pandas.read_excel(url,sheet_name=sheet_name, engine='openpyxl', usecols='B,C,D,F,H:R', skiprows=11, nrows=18)

    return dataset

def modify_federal_state_dataset(dataset: pandas.DataFrame, year: int, month: int):
    if year <= 2021:
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
    else:
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
    dataset.replace('/', 0, inplace=True)

    columns_to_fill = [
        federal_state_columnNames[1],
        federal_state_columnNames[2],
        federal_state_columnNames[3],
        federal_state_columnNames[4],
        federal_state_columnNames[5],
        federal_state_columnNames[6],
        federal_state_columnNames[7],
        federal_state_columnNames[8],
        federal_state_columnNames[9],
        federal_state_columnNames[10],
        federal_state_columnNames[11],
        federal_state_columnNames[12],
        federal_state_columnNames[13],
        federal_state_columnNames[14],
    ]
    dataset[columns_to_fill].fillna(0, inplace=True)

    dataset[federal_state_columnNames[0]] = dataset[federal_state_columnNames[0]].astype(str)
    dataset[federal_state_columnNames[1]] = dataset[federal_state_columnNames[1]].astype(int)
    dataset[federal_state_columnNames[2]] = dataset[federal_state_columnNames[2]].astype(int)
    dataset[federal_state_columnNames[3]] = dataset[federal_state_columnNames[3]].astype(int)
    dataset[federal_state_columnNames[4]] = dataset[federal_state_columnNames[4]].astype(int)
    dataset[federal_state_columnNames[5]] = dataset[federal_state_columnNames[5]].astype(int)
    dataset[federal_state_columnNames[6]] = dataset[federal_state_columnNames[6]].astype(int)
    dataset[federal_state_columnNames[7]] = dataset[federal_state_columnNames[7]].astype(int)
    dataset[federal_state_columnNames[8]] = dataset[federal_state_columnNames[8]].astype(int)
    dataset[federal_state_columnNames[9]] = dataset[federal_state_columnNames[9]].astype(int)
    dataset[federal_state_columnNames[10]] = dataset[federal_state_columnNames[10]].astype(int)
    dataset[federal_state_columnNames[11]] = dataset[federal_state_columnNames[11]].astype(int)
    dataset[federal_state_columnNames[12]] = dataset[federal_state_columnNames[12]].astype(int)
    dataset[federal_state_columnNames[13]] = dataset[federal_state_columnNames[13]].astype(int)
    dataset[federal_state_columnNames[14]] = dataset[federal_state_columnNames[14]].astype(int)

def get_polished_federal_state_dataset(information: FederalStateDataSetInformation) -> pandas.DataFrame:
    dataset = read_federal_state_datafile(information.url, information.sheet_name, information.year)

    modify_federal_state_dataset(dataset, information.year, information.month)

    return dataset

def get_federal_state_datasets():
    datasets = []
    for information in federal_state_datasets:
        current_dataset = get_polished_federal_state_dataset(information)

        datasets.append(current_dataset)

    federal_state_dataset = pandas.concat(datasets)        

    federal_state_dataset.to_sql('federal-state-statistics',  f'sqlite:///{CURRENT_DIR}/data.sqlite', if_exists='replace', index=False)

get_brand_datasets()
get_federal_state_datasets()