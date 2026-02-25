from flask import Flask, jsonify
import pyodbc
import os
import socket

app = Flask(__name__)

def get_db_connection():
    """Conecta ao SQL Server"""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_HOST', 'localhost')};"
        f"DATABASE=TestDB;"
        f"UID=sa;"
        f"PWD={os.getenv('DB_PASSWORD', 'YourPassword123!')}"
    )
    return pyodbc.connect(conn_str, timeout=5)

@app.route('/health')
def health():
    """Endpoint de health check com teste de database"""
    hostname = socket.gethostname()
    response = {
        'backend': '✅ OK',
        'hostname': hostname,
        'database': '❌ Not Connected'
    }
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT message, created_at FROM test_table ORDER BY id DESC")
        row = cursor.fetchone()
        
        if row:
            response['database'] = f'✅ Connected'
            response['db_message'] = row[0]
            response['db_timestamp'] = str(row[1])
        else:
            response['database'] = '✅ Connected (no data)'
        
        conn.close()
    except Exception as e:
        response['database'] = f'❌ Error: {str(e)}'
    
    # Formatar resposta HTML
    html = f"""
    <strong>Backend:</strong> {response['backend']}<br>
    <strong>Hostname:</strong> {response['hostname']}<br>
    <strong>Database:</strong> {response['database']}<br>
    """
    
    if 'db_message' in response:
        html += f"<strong>DB Message:</strong> {response['db_message']}<br>"
        html += f"<strong>DB Timestamp:</strong> {response['db_timestamp']}<br>"
    
    return html

@app.route('/api/info')
def info():
    """Informações do sistema"""
    return jsonify({
        'service': 'backend',
        'hostname': socket.gethostname(),
        'status': 'running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
