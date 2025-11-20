from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Ortam değişkeninden DATABASE_URL'i al
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://zeynep:MeSjOGra7VoVAgE2iWDHb918JnjwXDCY@dpg-d4fkiq3e5dus7396lv1g-a.oregon-postgres.render.com/hellocloud2_db_yy11"
)

def connect_db():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return jsonify({"status": "online", "message": "API is running. Use /ziyaretciler endpoint."}), 200

@app.route('/ziyaretciler', methods=['GET', 'POST'])
def ziyaretciler():
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    cur = None
    try:
        cur = conn.cursor()

        # TABLO OLUŞTURMA
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ziyaretciler (
                id SERIAL PRIMARY KEY,
                isim TEXT
            );
        """)

        # POST
        if request.method == "POST":
            data = request.json
            isim = data.get("isim")

            if isim:
                cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
                conn.commit()

            return jsonify({"status": "eklendi", "isim": isim}), 201

        # GET
        elif request.method == "GET":
            cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
            isimler = [row[0] for row in cur.fetchall()]
            return jsonify({"ziyaretciler": isimler})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

