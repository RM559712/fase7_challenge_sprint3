import ee
import datetime
import os
from google.cloud import storage

# Inicializa Earth Engine
ee.Initialize(project='fabled-gist-435119-r7')

# Nome do bucket de destino
BUCKET_NAME = "earthengine_fiap"
CAMINHO_BUCKET = f"gs://{BUCKET_NAME}"

# Verificação de permissão: tenta criar um arquivo temporário no bucket
def testar_bucket():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    blob = bucket.blob(f"temp_{timestamp}.txt")
    try:
        blob.upload_from_string("teste de escrita no bucket")
        print(f"📤 Teste de escrita iniciado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Falha ao escrever no bucket: {e}")
        return False

if not testar_bucket():
    exit("🚫 Encerrando script devido à falha de permissão no bucket.")

# Define a coleção NDVI com a nova versão MODIS 6.1
colecao = ee.ImageCollection("MODIS/061/MOD13Q1").select("NDVI")

# Carrega os municípios do asset
municipios = ee.FeatureCollection("projects/fabled-gist-435119-r7/assets/municipios_top_cana")

# Define período
anos = [2020, 2021, 2022, 2023]
meses = list(range(1, 13))

# Lista de resultados por período
lista_ndvi = []

# Função para extrair NDVI médio por município
for ano in anos:
    for mes in meses:
        data_inicio = ee.Date(f"{ano}-{mes:02d}-01")
        data_fim = data_inicio.advance(1, "month")

        print(f"📆 Processando NDVI - {ano}/{mes:02d}")

        # Filtra a coleção no intervalo
        img = colecao.filterDate(data_inicio, data_fim).mean()

        # Verifica se a imagem contém bandas
        band_names = img.bandNames().getInfo()
        if not band_names:
            print(f"⚠️ Sem bandas para {ano}/{mes:02d}, pulando.")
            continue

        # Reduz por regiões (média por município)
        ndvi_por_mun = img.reduceRegions(
            collection=municipios,
            reducer=ee.Reducer.mean(),
            scale=250,
        ).map(lambda f: f.set("ano", ano).set("mes", mes))

        lista_ndvi.append(ndvi_por_mun)

# Junta todas as coleções em uma só
ndvi_final = ee.FeatureCollection(lista_ndvi).flatten()

# Nome do arquivo de saída
arquivo_saida = "Exporta_NDVI_Mensal_Cana"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

# Exporta para o bucket
tarefa = ee.batch.Export.table.toCloudStorage(
    collection=ndvi_final,
    description=arquivo_saida,
    bucket=BUCKET_NAME,
    fileNamePrefix=f"ndvi_mensal_cana_{timestamp}",
    fileFormat="CSV"
)

tarefa.start()

print("✅ Exportação do NDVI mensal iniciada com sucesso.")
print("🔍 Use 'earthengine task list' para acompanhar.")
