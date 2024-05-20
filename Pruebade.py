import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos del archivo CSV€€
df = pd.read_csv('fifa.csv', index_col='ID', encoding='windows-1252')
df['Sueldo'] = df['Sueldo'].str.replace(r'\D', '', regex=True).replace('', 0).astype(int)

#df['Sueldo'] = df['Sueldo'].astype(int)
#df['Sueldo'] = df['Sueldo'].astype(str).astype(float)
print(df.loc[212198, 'Sueldo'])
print(df.dtypes)
#print (df ['Sueldo']