from app.database import engine

try:
    conn = engine.connect()
    print("CONNECTED")
    conn.close()
except Exception as e:
    print("ERROR:", e)