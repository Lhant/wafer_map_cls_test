import pandas as pd
from sqlalchemy import create_engine, text

def db_exception_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            # logging.error(f"DB Error in {func.__name__}: {e}")
            print(f"DB Error in {func.__name__}: {e}")
            raise
    return wrapper

class SQLAlchemyUtils:
    # 方便使用
    db_path = 'test_wal_demo.db'
    db_url = f'sqlite:///{db_path}'

    def __init__(self, db_url):
        """
        初始化数据库连接，并设置WAL模式（仅适用于SQLite）
        :param db_url: 形如'sqlite:///test.db'
        """
        self.engine = create_engine(db_url)
        try:
            with self.engine.begin() as conn:
                conn.execute(text("PRAGMA journal_mode=WAL;"))
        except Exception as e:
            print(f"WAL模式设置失败(可能不是SQLite): {e}")

    @db_exception_handler
    def create_table(self, sql: str):
        """
        执行建表语句
        :param sql: 建表SQL语句
        """
        with self.engine.begin() as conn:
            conn.execute(text(sql))

    @db_exception_handler
    def execute(self, sql: str, params: dict = None):
        """
        执行任意 SQL（insert、update、delete等）
        :param sql: SQL语句，参数用冒号占位，例如: 'DELETE FROM users WHERE name=:name'
        :param params: 参数字典
        :return: 返回执行结果对象
        """
        with self.engine.begin() as conn:
            result = conn.execute(text(sql), params or {})
        return result

    @db_exception_handler
    def executemany(self, sql: str, params_list: list):
        """
        批量执行SQL（如批量插入、批量更新等）
        :param sql: SQL语句，参数用冒号占位，例如: 'INSERT INTO users (name, age) VALUES (:name, :age)'
        :param params_list: 参数字典组成的列表，例如: [{'name': 'Tom', 'age': 9}, {'name': 'Jerry', 'age': 10}]
        :return: 返回执行结果对象
        """
        if not params_list:
            print("⚠️ 批量操作参数为空，未执行SQL")
            return None
        with self.engine.begin() as conn:
            result = conn.execute(text(sql), params_list)
        print(f"✅ 批量执行完成，共影响 {result.rowcount} 行")
        return result

    @db_exception_handler
    def query(self, sql: str, params: dict = None):
        """
        参数化查询，返回pandas的DataFrame
        :param sql: 查询SQL语句，如 'SELECT * FROM users WHERE age=:age'
        :param params: 参数字典，如 {'age': 9}
        :return: pandas.DataFrame
        """
        df = pd.read_sql(sql, self.engine, params=params)
        return df

    @db_exception_handler
    def vacuum(self):
        with self.engine.begin() as conn:
            conn.execute(text("VACUUM"))

    @db_exception_handler
    def table_exists(self, table_name: str) -> bool:
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=:name"
        df = self.query(sql, {"name": table_name})
        return not df.empty


# ---------------------------------------------------------
# 测试用例
if __name__ == "__main__":
    # 1. 初始化数据库工具类（确保路径在你能看到的文件夹）

    db = SQLAlchemyUtils(SQLAlchemyUtils.db_url)

    # 2. 创建表
    db.create_table("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
    """)

    # 3. 批量插入数据
    users = [
        {'name': 'Tom', 'age': 9},
        {'name': 'Jerry', 'age': 10},
        {'name': 'Spike', 'age': 12}
    ]
    db.executemany("INSERT INTO users (name, age) VALUES (:name, :age)", users)

    # 4. 查询数据并打印
    df = db.query("SELECT * FROM users WHERE age >= :min_age", {'min_age': 10})
    print(df)

    # 5. 手动暂停，观察WAL文件（可选，便于你观察文件）
    print("\n请在此时查看当前文件夹，应该能看到 test_wal_demo.db-wal 和 test_wal_demo.db-shm 文件。")
    input("按回车键继续...")

    # 6. 额外演示更新和删除
    db.execute("UPDATE users SET age=11 WHERE name=:name", {'name': 'Jerry'})
    db.execute("DELETE FROM users WHERE name=:name", {'name': 'Tom'})

    df2 = db.query("SELECT * FROM users")
    print("\n更新和删除后的数据：")
    print(df2)

    print(db.table_exists('users'))