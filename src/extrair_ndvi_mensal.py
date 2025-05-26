import ee
import datetime
import uuid

# Inicializa Earth Engine
ee.Initialize()

# Configurações
bucket_name = "earthengine_fiap"
asset_municipios = "projects/fabled-gist-435119-r7/assets/municipios_top_cana"
timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
test_filename = f"temp_{timestamp}.txt"

# 1. Teste de permissão de escrita no bucket
print(f"⏳ Testando permissão de escrita no bucket: gs://{bucket_name}/{test_filename}")
teste_fc = ee.FeatureCollection([
    ee.Feature(None, {"teste": f"verificacao_{uuid.uuid4()}"})
])

test_task = ee.batch.Export.table.toCloudStorage(
    collection=teste_fc,
    description="Teste_Bucket_Permissao",
    bucket=bucket_name,
    fileNamePrefix=test_filename,
    fileFormat="CSV"
)

try:
    test_task.start()
    print("📤 Teste de escrita iniciado com sucesso.")
except Exception as e:
    raise RuntimeError(f"❌ Falha ao tentar escrever no bucket: {e}")

# 2. Carrega os municípios
municipios = ee.FeatureCollection(asset_municipios)

# 3. Coleção MODIS com NDVI
colecao = ee.ImageCollection("MODIS/006/MOD13Q1").select("NDVI")

# 4. Função segura para NDVI médio mensal
def extrair_ndvi_mensal(ano, mes):
    ini = ee.Date.fromYMD(ano, mes, 1)
    fim = ini.advance(1, "month")
    
    colecao_mensal = colecao.filterDate(ini, fim)

    ndvi_condicional = ee.Algorithms.If(
        colecao_mensal.size().gt(0),
        colecao_mensal.mean().multiply(0.0001),
        ee.Image().select()
    )

    imagem_valida = ee.Image(ndvi_condicional)

    return imagem_valida.reduceRegions(
        collection=municipios,
        reducer=ee.Reducer.mean(),
        scale=250
    ).map(lambda f: f.set("ano", ano).set("mes", mes))

# 5. Loop por ano e mês
anos = list(range(2020, 2024))
meses = list(range(1, 13))
resultado_geral = ee.FeatureCollection([])

for ano in anos:
    for mes in meses:
        print(f"📆 Processando NDVI - {ano}/{mes:02}")
        resultado_geral = resultado_geral.merge(extrair_ndvi_mensal(ano, mes))

# 6. Exportação final para Cloud Storage
export_task = ee.batch.Export.table.toCloudStorage(
    collection=resultado_geral,
    description="Exporta_NDVI_Mensal_Cana",
    bucket=bucket_name,
    fileNamePrefix="ndvi_mensal_cana_2020_2023",
    fileFormat="CSV"
)

export_task.start()
print("✅ Exportação do NDVI mensal iniciada com sucesso.")
print("🔍 Use 'earthengine task list' para acompanhar.")
