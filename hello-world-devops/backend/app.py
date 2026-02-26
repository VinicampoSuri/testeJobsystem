from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import pyodbc

app = Flask(__name__)
CORS(app)

# Configurações do banco de dados
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'sa')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'master')

def get_db_connection():
    """Tenta conectar ao SQL Server"""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={DB_HOST};'
            f'DATABASE={DB_NAME};'
            f'UID={DB_USER};'
            f'PWD={DB_PASSWORD};'
            f'TrustServerCertificate=yes;'
        )
        conn = pyodbc.connect(conn_str, timeout=5)
        return conn
    except Exception as e:
        return None

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'backend-api',
        'timestamp': datetime.now().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'production'),
        'version': '1.0.0'
    })

@app.route('/hello', methods=['GET'])
def hello():
    """Endpoint de teste básico"""
    return jsonify({
        'message': 'Hello from Backend! 🚀',
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'server': 'Flask + Gunicorn'
    })

@app.route('/db-test', methods=['GET'])
def db_test():
    """Testa conexão com o banco de dados"""
    conn = get_db_connection()
    
    if conn is None:
        return jsonify({
            'status': 'error',
            'message': 'Não foi possível conectar ao banco de dados',
            'db_host': DB_HOST,
            'timestamp': datetime.now().isoformat()
        }), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION as version")
        row = cursor.fetchone()
        version = row.version if row else 'Unknown'
        
        cursor.execute("SELECT DB_NAME() as current_db")
        row = cursor.fetchone()
        current_db = row.current_db if row else 'Unknown'
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Conexão com banco de dados OK! ✅',
            'database': {
                'host': DB_HOST,
                'current_database': current_db,
                'version': version[:100]  # Primeiros 100 chars
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao consultar banco: {str(e)}',
            'db_host': DB_HOST,
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
