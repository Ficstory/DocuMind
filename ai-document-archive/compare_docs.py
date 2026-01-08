import sqlite3
import json

conn = sqlite3.connect('archive.db')
cursor = conn.cursor()

cursor.execute('SELECT id, filename, doc_type, keywords, summary, structured_data FROM document WHERE id IN (2, 4) ORDER BY id')
docs = cursor.fetchall()

output = []

for doc in docs:
    doc_id, filename, doc_type, keywords, summary, structured_data = doc
    title = "작업 전 - 기존 모델" if doc_id == 2 else "작업 후 - 개선된 모델"

    output.append(f'\n{"="*80}')
    output.append(f'문서 ID {doc_id} ({title})')
    output.append(f'{"="*80}')
    output.append(f'파일명: {filename}')
    output.append(f'문서 유형: {doc_type}')
    output.append(f'\n키워드:')
    output.append(keywords)
    output.append('')

    if structured_data:
        output.append('구조화된 데이터:')
        output.append(json.dumps(json.loads(structured_data), indent=2, ensure_ascii=False))

conn.close()

# 파일로 저장
with open('comparison.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

# 화면 출력
print('\n'.join(output))
