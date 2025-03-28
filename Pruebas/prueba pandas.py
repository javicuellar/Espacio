import pandas as pd

# Datos de ejemplo
data = {
    'clave': ['A', 'AB', 'ABC', 'AC', 'BC', 'BCD'],
    'valor': [5, 2, 3, 1, 5, 6]
}

# Crear un DataFrame a partir de los datos
df = pd.DataFrame(data)

# Ordenar los datos por la columna clave
df = df.sort_values('clave')

# Crear columnas para almacenar el valor acumulado
df['valor_acumulado'] = 0

print(df)

def Total(df, fila, clave):
    print("clave", clave, "df.iloc[fila + 1, 0]", df.iloc[fila + 1, 0], "fila", fila, "len(df)", len(df))
    if fila == len(df) - 1:
        df.iloc[fila, 2] += df.iloc[fila, 1]
        return df.iloc[fila, 1]
    elif fila < len(df) - 1:
        if clave in df.iloc[fila + 1, 0]:
            print("   --> Hay mas filas: ", fila, " clave siguiente dentro: ", df.iloc[fila + 1, 0], " valor: ", df.iloc[fila, 2] +1)
            if fila == 4:
                pass
            df.iloc[fila, 2] += df.iloc[fila, 1] + Total(df, fila + 1, df.iloc[fila + 1, 0])
        else:
            df.iloc[fila + 1, 2] = Total(df, fila + 1, df.iloc[fila + 1, 0])
            return df.iloc[fila, 1]


df.iloc[0,2] = Total(df, 0, df.iloc[0,0])

df