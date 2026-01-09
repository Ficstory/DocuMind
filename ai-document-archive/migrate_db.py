"""
데이터베이스 마이그레이션 스크립트
기존 데이터를 유지하면서 새 컬럼 추가
"""
import sqlite3

def migrate_database():
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()

    # 새로운 컬럼들 추가
    new_columns = [
        ('is_photo', 'INTEGER'),
        ('has_exif', 'INTEGER'),
        ('has_gps', 'INTEGER'),
        ('camera_make', 'TEXT'),
        ('camera_model', 'TEXT'),
        ('photo_datetime', 'TIMESTAMP'),
        ('gps_latitude', 'REAL'),
        ('gps_longitude', 'REAL'),
        ('gps_altitude', 'REAL'),
        ('image_width', 'INTEGER'),
        ('image_height', 'INTEGER'),
        ('orientation', 'INTEGER')
    ]

    for column_name, column_type in new_columns:
        try:
            cursor.execute(f'ALTER TABLE document ADD COLUMN {column_name} {column_type}')
            print(f'✅ 컬럼 추가 성공: {column_name}')
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e):
                print(f'⚠️  이미 존재하는 컬럼: {column_name}')
            else:
                print(f'❌ 에러 발생 ({column_name}): {e}')

    conn.commit()
    conn.close()
    print('\n✅ 마이그레이션 완료!')

if __name__ == '__main__':
    migrate_database()
