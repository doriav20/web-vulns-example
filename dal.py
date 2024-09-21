import sqlite3

DB_FILE_NAME: str = 'posts.db'


def with_db_cursor(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            cursor = conn.cursor()
            res = func(cursor, *args, **kwargs)
            conn.commit()
        return res

    return wrapper


@with_db_cursor
def create_table(cursor: sqlite3.Cursor) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''

    cursor.execute(query)


def init_db() -> None:
    create_table()


@with_db_cursor
def get_posts(cursor: sqlite3.Cursor) -> list:
    query = '''
    SELECT id, author, content, DATETIME(created_at, 'localtime') FROM posts
    '''
    cursor.execute(query)

    posts = cursor.fetchall()
    if posts is None:
        return []

    return posts


@with_db_cursor
def create_post(cursor: sqlite3.Cursor, author: str, content: str) -> None:
    query = f'''
    INSERT INTO posts (author, content) VALUES ('{author}', '{content}')
    '''

    try:
        cursor.executescript(query)
    except sqlite3.Error:
        pass
