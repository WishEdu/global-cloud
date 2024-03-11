import psycopg2 as pg
import psycopg2.extras

from configs import DB_NAME, DB_USER, DB_PASSWORD


conn = pg.connect(f"host=localhost dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# on startup will create table if one not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS cdn(
    id BIGSERIAL PRIMARY KEY,
    owner_type VARCHAR(16),
    owner_id BIGINT,
    file_type VARCHAR(16),
    file_name VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
conn.commit()


def add_file(file_owner: str, file_owner_id: int, file_type: str, file_name: str) -> int:
    try:
        cur.execute("""
            INSERT INTO cdn(owner_type, owner_id, file_type, file_name)
            VALUES(%s, %s, %s, %s)
            RETURNING id
        """, (file_owner, file_owner_id, file_type, file_name))
    except:
        conn.rollback()
        return -1
    
    conn.commit()
    return cur.fetchone()

def get_by_file_id(file_id: int) -> psycopg2.extras.RealDictRow:
    try:
        cur.execute("""SELECT owner_type, owner_id, file_type, file_name
                       FROM cdn WHERE id = %s
                    """, (file_id,))
    except:
        conn.rollback()
        return -1
    
    return cur.fetchone()

def delete_by_file_id(file_id: int) -> int:
    try:
        cur.execute("DELETE FROM cdn WHERE id = %s RETURNING id", (file_id,))
    except:
        conn.rollback()
        return -1
    
    conn.commit()
    return cur.fetchone()

def get_user_avatar_or_group_logo(owner_type: int, owner_id: int) -> psycopg2.extras.RealDictRow:
    try:
        cur.execute("""SELECT file_type, file_name FROM cdn
                       WHERE owner_type = %s AND owner_id = %s AND
                       (file_type = 'avatar' OR file_type = 'logo')
                       ORDER BY created_at DESC LIMIT 1
                    """, (owner_type, owner_id))
    except:
        conn.rollback()
        return -1
    
    return cur.fetchone()