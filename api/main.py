# uvicorn api.main:app --reload
from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd

app = FastAPI(title="Kepler Exoplanet API")

#upload
df = pd.read_csv("data/cumulative.csv")
df = df.dropna(subset=['koi_period', 'koi_prad', 'koi_srad', 'koi_teq'])

df['planet_volume_earth'] = df['koi_prad']**3  
df['habitable_zone'] = (df['koi_teq']>=200) & (df['koi_teq']<=320)  

columns_to_keep = ['kepoi_name', 'koi_disposition', 'koi_period', 'koi_prad', 'koi_srad', 'koi_teq', 'planet_volume_earth', 'habitable_zone']
global clean_df
clean_df = df[columns_to_keep]

#data structure
class PlanetCreate(BaseModel):
    kepoi_name: str
    koi_disposition: str
    koi_period: float
    koi_prad: float
    koi_srad: float
    koi_teq: float

#endpoints
@app.get("/")
def read_root():
    return {"status": "success", "message": "NASA Kepler API is online."}

@app.get("/planets")
def get_planets(
    status: str = Query(None, description="Фильтр по статусу"),
    limit: int = Query(50, description="Количество записей")
):
    result_df = clean_df.copy()
    if status:
        result_df = result_df[result_df['koi_disposition'] == status]
    result_df = result_df.head(limit)
    return result_df.to_dict(orient="records")

#new
@app.post("/planets")
def create_planet(planet: PlanetCreate):
    global clean_df

    planet_volume = planet.koi_prad ** 3
    is_habitable = 200 <= planet.koi_teq <= 320
  
    new_row = {
        'kepoi_name': planet.kepoi_name,
        'koi_disposition': planet.koi_disposition,
        'koi_period': planet.koi_period,
        'koi_prad': planet.koi_prad,
        'koi_srad': planet.koi_srad,
        'koi_teq': planet.koi_teq,
        'planet_volume_earth': planet_volume,
        'habitable_zone': is_habitable
    }
    
    clean_df = pd.concat([clean_df, pd.DataFrame([new_row])], ignore_index=True)
    
    return {"status": "success", "message": f"Planet {planet.kepoi_name} added!", "data": new_row}