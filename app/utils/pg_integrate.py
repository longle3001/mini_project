import psycopg

# Cấu hình kết nối
DATABASE_URL = "postgresql://postgres:mysecretpassword@db:5432/postgres_data"


# SQL để kiểm tra sự tồn tại của bảng
check_table_query = """
SELECT EXISTS (
    SELECT FROM pg_tables
    WHERE schemaname = 'public' AND tablename  = 'embedding'
);
"""

# SQL để tạo bảng nếu nó không tồn tại
create_table_query = """
CREATE TABLE IF NOT EXISTS embedding (
    filename VARCHAR(255),
    content TEXT,
    type VARCHAR(50),
    project VARCHAR(255),
    organisation_id VARCHAR(255),
    embedding_id VARCHAR(255)
);
"""


# Hàm kết nối và kiểm tra hoặc tạo bảng
def setup_database():
    # Kết nối tới PostgreSQL
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Kiểm tra sự tồn tại của bảng
            cur.execute(check_table_query)
            exists = cur.fetchone()[0]

            # Nếu bảng không tồn tại, tạo bảng
            if not exists:
                cur.execute(create_table_query)
                print("Table 'embedding' was created.")
            else:
                print("Table 'embedding' already exists.")


def add_record(
    filename: str,
    content: str,
    type: str,
    project: str,
    organisation_id: str,
    embedding_id: str,
):
    # Kết nối tới PostgreSQL
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            value = f"('{filename}','{content}', '{type}','{project}','{organisation_id}','{embedding_id}')"
            insert = """
            INSERT INTO EMBEDDING 
            (filename, content, type, project, organisation_id, embedding_id) 
            VALUES
            """
            insert = insert + value
            cur.execute(insert)


def search_organisation_id(organisation_id: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # avoid sql injection
            if " or " in organisation_id:
                return None
            sql = f"select * from EMBEDDING where organisation_id='{organisation_id}'"
            res = cur.execute(sql)
            res = res.fetchall()
        return res
