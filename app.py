from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Ortam değişkeninden (Render'dan) DATABASE_URL'i al
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zeynep:MeSjOGra7VoVAgE2iWDHb918JnjwXDCY@dpg-d4fkiq3e5dus7396lv1g-a.oregon-postgres.render.com/hellocloud2_db_yy11")

def connect_db():
    try:
        # psycop2'nin bağlanırken URL'yi kullanması
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        # Bağlantı hatasını konsola yazdır
        print(f"Database connection error: {e}") 
        return None

# --- YENİ EKLENEN ROTA: Kök Yolu (404 Hatasını Giderir) ---
@app.route('/')
def index():
    # Uygulamanın çalıştığını belirten JSON yanıtı döndürür
    return jsonify({"status": "online", "message": "API is running. Use /ziyaretciler endpoint."}), 200
# ------------------------------------------------------------------

# --- Ziyaretçiler Rotası (GET ve POST) ---
@app.route('/ziyaretciler', methods=['GET', 'POST'])
def ziyaretciler():
    conn = connect_db()
    # Eğer veritabanına bağlanılamazsa hata döndür
    if not conn:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    # Bağlantıyı ve kürsörü yönetmek için try/except/finally bloğu kullanıldı
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
        
        # POST İŞLEMİ (Yeni Ziyaretçi Ekleme)
        if request.method == "POST":
            data = request.json
            isim = data.get("isim") 

            if isim:
                cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
                conn.commit()
            
            # POST işleminden sonra başarılı yanıt
            return jsonify({"status": "eklendi", "isim": isim}), 201

        # GET İŞLEMİ (Ziyaretçileri Listeleme)
        elif request.method == "GET":
            cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
            isimler = [row[0] for row in cur.fetchall()]
            # Başarılı GET yanıtı
            return jsonify({"ziyaretciler": isimler})

    except Exception as e:
        # Bir hata oluşursa yapılan işlemleri geri al
        conn.rollback() 
        return jsonify({"error": str(e)}), 500
    
    # --- YENİ EKLENEN BÖLÜM: Bağlantıları Her Durumda Kapat ---
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    # -------------------------------------------------------------

# Uygulama Başlatma
if __name__ == '__main__':
    # Render için gerekli host ve port ayarları
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
