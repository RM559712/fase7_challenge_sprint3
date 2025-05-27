import os
import glob
import pandas as pd

ROOT_DIR = '/workspace/fase7_challenge_sprint3/dados/download_manual/inmet_bak/'

# Pega somente arquivos SP
arquivos = [
    f for f in glob.glob(os.path.join(ROOT_DIR, '**', '*.CSV'), recursive=True)
    if 'INMET' in os.path.basename(f) and '_SP_' in os.path.basename(f)
]

registros = []

for arquivo in arquivos:
    try:
        with open(arquivo, 'r', encoding='latin1') as f:
            linhas = [next(f) for _ in range(8)]

        estacao = None
        codigo = None
        latitude = None
        longitude = None

        for linha in linhas:
            partes = linha.strip().split(';')
            if len(partes) < 2:
                continue

            chave = partes[0].strip().upper().replace(':', '')
            valor = partes[1].strip()

            if chave == 'ESTACAO':
                estacao = valor.upper()
            elif 'WMO' in chave or 'CODIGO' in chave:
                codigo = valor
            elif chave == 'LATITUDE':
                latitude = float(valor.replace(',', '.'))
            elif chave == 'LONGITUDE':
                longitude = float(valor.replace(',', '.'))

        if all([estacao, codigo, latitude, longitude]):
            registros.append({
                'CD_ESTACAO': codigo,
                'DC_NOME': estacao,
                'VL_LATITUDE': latitude,
                'VL_LONGITUDE': longitude
            })
        else:
            print(f"⚠️ Dados incompletos em: {arquivo}")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

# Salva resultado
df_estacoes = pd.DataFrame(registros).drop_duplicates()
df_estacoes.to_csv('estacoes_meteorologicas.csv', index=False)
print(f"\n✅ Arquivo gerado: estacoes_meteorologicas.csv com {len(df_estacoes)} estações.")
