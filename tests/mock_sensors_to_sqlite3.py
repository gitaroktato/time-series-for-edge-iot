import sqlite3
import time
import random


def create_tables(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS sensors(
       name TEXT,
       x REAL,
       y REAL,
       z REAL,
       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur = conn.cursor()
    cur.execute(sql)
    index_sql = """
    CREATE INDEX idx_sensors_timestamp ON sensors (timestamp);
    """
    cur.execute(index_sql)
    conn.commit()


def add_sensor(conn, sensor):
    sql = '''INSERT INTO sensors(name, x, y, z)
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, sensor)
    conn.commit()
    return cur.lastrowid


def main():
    try:
        with sqlite3.connect('sensors_storage.sqlite') as conn:
            # Turn on WAL mode
            conn.execute('PRAGMA journal_mode=WAL;')
            create_tables(conn)
            for i in range(1, 86400):

                # sensors write
                sensors = [
                    ('accel', random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)),
                    ('gyro', random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5))
                ]
                for sensor in sensors:
                    sensor_id = add_sensor(conn, sensor)
                    print(f'Added sensor {sensor}')
                time.sleep(1)
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    main()
