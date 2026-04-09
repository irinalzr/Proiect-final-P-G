import pandas as pd
import matplotlib.pyplot as plt
from db_conn import engine  
# df = pd.read_sql("SELECT * FROM ConsumerUnits", engine)

# Numarul de consumatori pe tara
# df.plot(x='country_name', y='number_of_consumers', kind='bar')
# plt.show()

# Distributia numarului de consumatori
# df['number_of_consumers'].hist()
# plt.xlabel("Nr consumatori")
# plt.ylabel("Frecventa")
# plt.show()

# print("Caracteristici numerice:")
df_char = pd.read_sql("SELECT * FROM Characteristics", engine)
df_num = df_char[df_char['data_type'] == 'Decimal']
# print(df_num[['Nume', 'Target', 'Limita inferioara', 'Limita superioara']])

print("Verificarea daca valorile tinta sunt in limitele specificate:")
df_num['within_limits'] = (
    (df_num['target'] >= df_num['lower_limit']) &
    (df_num['target'] <= df_num['upper_limit'])
)
print(df_num[['name', 'within_limits']])