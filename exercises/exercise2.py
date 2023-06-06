import pandas
import os

# Read the csv
dtypes = {'EVA_NR': int, 'DS100': str, 'IFOPT': str, 'NAME': str, 'Verkehr': str, 'Laenge': float, 'Breite': float, 'Betreiber_Name': str, 'Betreiber_Nr': float, 'Status': str }
complete_dataset = pandas.read_csv('https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV', sep=';', decimal=',', dtype=dtypes)

# Fill values in Betreiber_Nr and convert to int
complete_dataset = complete_dataset.fillna(value={'Betreiber_Nr': 0})
complete_dataset['Betreiber_Nr'] = complete_dataset['Betreiber_Nr'].astype(int)

# Drop the status column
reduced_dataset = complete_dataset.drop('Status', axis=1)

# Remove columns with invalid values
valid_verkehr_values = ['FV', 'RV', 'nur DPN']
reduced_dataset = reduced_dataset[reduced_dataset['Verkehr'].str.contains('|'.join(valid_verkehr_values), na=False)]

reduced_dataset = reduced_dataset[(reduced_dataset['Laenge'] >= -90) & (reduced_dataset['Laenge'] <= 90)]
reduced_dataset = reduced_dataset[(reduced_dataset['Breite'] >= -90) & (reduced_dataset['Breite'] <= 90)]

ifopt_pattern = r'^\w{2}\:\d+\:\d+(?:\:\d+)?$'
reduced_dataset = reduced_dataset[reduced_dataset['IFOPT'].str.contains(ifopt_pattern, na=False)]

# Write to local sqlite-table
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
reduced_dataset.to_sql('trainstops',  f'sqlite:///{CURRENT_DIR}/trainstops.sqlite', if_exists='replace', index=False)