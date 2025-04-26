from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    """Initialize MySQL with Flask app."""
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'pranali03'
    app.config['MYSQL_DB'] = 'podcast_db'
    
    mysql.init_app(app)

def insert_podcast(youtube_url, transcription, summary, detected_lang):
    """Insert podcast details into the database."""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO podcasts (youtube_url, transcription, summary, detected_language) 
            VALUES (%s, %s, %s, %s)
        """, (youtube_url, transcription, summary, detected_lang))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return False
    return True
