from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__)

# Render'ın otomatik tanımladığı veritabanı bağlantı bilgisi (DATABASE_URL ortam değişkeni)
DATABASE_URL = os.getenv

#HTML ŞABLONU (tek sayfada from + liste)
HTML = """
<!doctype html>
<html>
<head>
    <title>Buluttan Selam!</title>
    <style>
        body { font-family: Arial: text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        from { margin: 220px auto; }
        input { padding: 10px; font-size. 16px; }
        button { padding: 10px 15px; background: #4CAF50; color:white; border: nane; border-radius: 6px; cursor: pointer, }
        ul { list-style: nane; paddding: 0; }
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
     <h1> Buluttan Selam!</h1>
     <p>AAdını yaz, selamını bırak</p>
     <form method="POST">
         <input type="text" name="isim" placeholder="Adını yaz" required>
         <button> type="submit">Gönder</button>
     </form>
     <h3>Ziyaretçiler:</h3>
     <ul>
          {% for ad in isimler %}
              <li>{{ ad }}</li>
          {% endfor %}
     </ul>
 </body>
 </html>
 """

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = connect_db()
    cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

if request.method == "POST":
    isim = request.from.get("isim")
  if isim:
      cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
      conn.commit()
      
cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
isimler = [row[0] for row in cur.fetchall()]

      cur.close()
      conn.close()
      return render_template_string(HTML, isimler=isimler)

if__name__== "__main__":
   app.run(host=="0.0.0.0", port=5000)

         
         

       

