# -----------------------------------------------
# SCRIPT: Localiza o município IBGE (CD_MUN) de cada estação meteorológica
# AUTOR: Marco Franzoi
# DATA: 2025-05-26
# OBJETIVO: Atribuir o código do município IBGE (CD_MUN) a cada estação meteorológica do INMET,
#           com base em suas coordenadas geográficas, usando um shapefile do IBGE.
# -----------------------------------------------

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# -----------------------------------------------
# 1. CONFIGURAÇÃO DOS CAMINHOS DOS ARQUIVOS
# -----------------------------------------------

# Caminho para o shapefile dos municípios de SP (baixado do IBGE)
CAMINHO_SHAPEFILE = '/workspace/fase7_challenge_sprint3/dados/download_manual/ibge_shapefiles/SP_Municipios_2022.shp'

# Caminho para o arquivo CSV com as estações meteorológicas (com lat/lon já extraídos)
CAMINHO_ESTACOES = '/workspace/fase7_challenge_sprint3/dados/estacoes_meteorologicas.csv'

# -----------------------------------------------
# 2. CARREGAMENTO DOS DADOS
# -----------------------------------------------

# Carrega os polígonos dos municípios do shapefile do IBGE
gdf_municipios = gpd.read_file(CAMINHO_SHAPEFILE)

# Carrega as estações meteorológicas em formato tabular
df_estacoes = pd.read_csv(CAMINHO_ESTACOES)

# -----------------------------------------------
# 3. CONVERSÃO DAS ESTAÇÕES PARA OBJETOS GEOGRÁFICOS (PONTOS)
# -----------------------------------------------

# Cria pontos (longitude, latitude) e converte para GeoDataFrame com CRS EPSG:4326
gdf_estacoes = gpd.GeoDataFrame(
    df_estacoes,
    geometry=[Point(lon, lat) for lon, lat in zip(df_estacoes['VL_LONGITUDE'], df_estacoes['VL_LATITUDE'])],
    crs='EPSG:4326'  # Sistema de referência geográfica (WGS 84)
)

# -----------------------------------------------
# 4. REPROJEÇÃO PARA ALINHAR OS SISTEMAS DE COORDENADAS
# -----------------------------------------------

# Reprojeta os municípios para o mesmo sistema de coordenadas das estações
gdf_municipios = gdf_municipios.to_crs(gdf_estacoes.crs)

# -----------------------------------------------
# 5. JUNÇÃO ESPACIAL: IDENTIFICAR O MUNICÍPIO DE CADA ESTAÇÃO
# -----------------------------------------------

# Faz a sobreposição espacial: em qual polígono de município cada ponto está contido
estacoes_com_mun = gpd.sjoin(
    gdf_estacoes,
    gdf_municipios,
    how='left',
    predicate='within'
)

# -----------------------------------------------
# 6. AJUSTE DOS NOMES DAS COLUNAS DO IBGE (caso variem)
# -----------------------------------------------

# Mostra colunas disponíveis para conferência
print("\n🔍 Colunas disponíveis no shapefile:")
print(gdf_municipios.columns)

# Verifica os nomes reais das colunas do shapefile
col_codigo = 'CD_MUN' if 'CD_MUN' in gdf_municipios.columns else 'CD_GEOCMU'
col_nome = 'NM_MUN' if 'NM_MUN' in gdf_municipios.columns else 'NM_MUNICIP'

# Renomeia as colunas para padronizar no resultado final
estacoes_com_mun.rename(columns={
    col_codigo: 'CD_MUN',
    col_nome: 'NOME_MUNICIPIO'
}, inplace=True)

# -----------------------------------------------
# 7. EXPORTAÇÃO DO RESULTADO FINAL PARA CSV
# -----------------------------------------------

# Salva CSV com as estações e o município onde estão localizadas
caminho_saida = '/workspace/fase7_challenge_sprint3/dados/estacoes_com_municipio.csv'
estacoes_com_mun[['CD_ESTACAO', 'DC_NOME', 'VL_LATITUDE', 'VL_LONGITUDE', 'CD_MUN', 'NOME_MUNICIPIO']].to_csv(
    caminho_saida,
    index=False
)

print(f"\n✅ Arquivo gerado: {caminho_saida}")
