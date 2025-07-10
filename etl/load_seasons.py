from espn_api.football import League
from etl.utils import get_db_connection

def load_season_data(year: int):
    league = League(
        league_id=1206951,
        year=year,
        swid="{BE77C299-A100-456A-9A58-03DFD0A2086B}",
        espn_s2="AEClUZxdsurZkvb4NnIlAnuGdxGLjf8TC9+i2ECduMMwjPO2E7mTaR2pHl0Y6X0DR/Y5VBTufKQkXRF3Z4pjI4WVZYqfLYF3YBCwJpovNFuTfTp6QyJKy6cy+JfaNi50t+DChHx0Ij7/rzw+Vmej7mUzNSiTxJc3waYs/s+OHl2DTiqqghscaUQhCqM6+MUNJPck4RnvJj+ahVSBiBaQ/M8W2JQphDmeU8xbrdjWbMnJa6Yznw1nXnpymwh4sgRonwmfFvFtCiOXg0/JBpGclwtD"
    )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO seasons (season_year)
        VALUES (?)
    """, (year,))
    print(f"✅ Season {year} inserted into 'seasons' table.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    for year in range(2012, 2025):
        load_season_data(year)