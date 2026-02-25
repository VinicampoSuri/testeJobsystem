from flask import Flask
import pyodbc
app = Flask(__name__)

@app.route('/api/health')
def health():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DB_IP;DATABASE=TestDB;UID=sa;PWD=YourPass')
        return "Backend + DB OK"
    except:
        return "Backend OK, DB Error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
