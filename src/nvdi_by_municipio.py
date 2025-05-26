import ee
import datetime

# === 1. Autenticação ===
ee.Authenticate()        # Só precisa rodar uma vez, depois pode remover
ee.Initialize()

# === 2. Configurações ===
asset_id = "users/marcofranzoi/municipios_top_cana"
data_inicio = "2022-04-01"
data_fim    = "2023-03-31"

# Coleção NDVI MODIS
colecao = ee.ImageCollection("MODIS/006/MOD13Q1") \
    .filterDate(data_inicio, data_fim) \
    .select("NDVI") \
    .map(lambda img: img.multiply(0.0001).copyProperties(img, ["system:time_start"]))

# Média do período
ndvi_medio = colecao.mean()

# Carrega municípios
municipios = ee.FeatureCollection(asset_id)

# Reduz por região (média de NDVI por município)
ndvi_por_municipio = ndvi_medio.reduceRegions(
    collection=municipios,
    reducer=ee.Reducer.mean(),
    scale=250  # resolução do MOD13Q1
)

# === 3. Exportação ===
task = ee.batch.Export.table.toDrive(
    collection=ndvi_por_municipio,
    description="ndvi_media_municipios_cana",
    folder="GEE_Export",  # pasta no seu Google Drive
    fileNamePrefix="ndvi_municipios_2022_2023",
    fileFormat="CSV"
)

task.start()
print("🚀 Exportação iniciada. Verifique o status com:")
print("   earthengine task list")
