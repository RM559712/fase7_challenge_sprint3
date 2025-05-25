import geopandas as gpd
import pandas as pd
from pathlib import Path
import zipfile

# Diretórios
base_dir = Path("/workspace/data")
csv_path = Path("/workspace/fase7_challenge_sprint3/dados/canadeacucar_long_final.csv")
saida_shp = Path("/workspace/fase7_challenge_sprint3/dados/municipios_top_cana.shp")
saida_zip = Path("/workspace/fase7_challenge_sprint3/dados/municipios_top_cana.zip")

# Carrega CSV da cana-de-açúcar
df_csv = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
codigos_ibge = df_csv["Cod Municipio"].astype(str).unique()

# Lê os shapefiles por estado e filtra
shapefiles = list(base_dir.rglob("*.shp"))
gdfs = []

for shp_path in shapefiles:
    print(f"📄 Lendo: {shp_path}")
    try:
        gdf = gpd.read_file(shp_path)
        col_ibge = next(col for col in gdf.columns if col.startswith("CD_") and "MUN" in col.upper())
        gdf[col_ibge] = gdf[col_ibge].astype(str)
        gdf_filtrado = gdf[gdf[col_ibge].isin(codigos_ibge)]
        gdfs.append(gdf_filtrado)
    except Exception as e:
        print(f"⚠️ Erro ao processar {shp_path.name}: {e}")

# Junta e exporta como Shapefile
gdf_final = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)
gdf_final.to_file(saida_shp, driver="ESRI Shapefile")
print(f"✅ Shapefile exportado: {saida_shp}")

# Compacta os arquivos .shp, .shx, .dbf, .prj
print("📦 Compactando arquivos...")
with zipfile.ZipFile(saida_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    for ext in [".shp", ".shx", ".dbf", ".prj"]:
        part = saida_shp.with_suffix(ext)
        if part.exists():
            zipf.write(part, arcname=part.name)

print(f"✅ Arquivo ZIP gerado: {saida_zip}")

# gsutil cp /workspace/fase7_challenge_sprint3/dados/municipios_top_cana.zip gs://earthengine_fiap/
# earthengine --project fabled-gist-435119-r7 upload table gs://earthengine_fiap/municipios_top_cana.zip   --asset_id=projects/fabled-gist-435119-r7/assets/municipios_top_cana
# earthengine --project fabled-gist-435119-r7 task list 