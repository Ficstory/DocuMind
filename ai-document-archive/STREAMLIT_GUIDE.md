# Streamlit 실행 가이드

> DocuMind AI Document Archive System의 Streamlit 앱 실행 및 구조 설명

---

## 🚀 실행 방법

### 1. 기본 실행

```bash
# ai-document-archive 폴더로 이동
cd ai-document-archive

# Streamlit 앱 실행
streamlit run app.py
```

**실행 결과:**
- 로컬 서버 시작: `http://localhost:8501`
- 브라우저 자동 실행
- 파일 변경 시 자동 새로고침

### 2. 고급 실행 옵션

```bash
# 포트 변경
streamlit run app.py --server.port 8080

# 브라우저 자동 열기 비활성화
streamlit run app.py --server.headless true

# 파일 감시 비활성화
streamlit run app.py --server.fileWatcherType none

# 모든 옵션 조합
streamlit run app.py --server.port 8080 --server.headless true
```

### 3. 종료 방법

- **터미널에서:** `Ctrl + C`
- **브라우저:** 그냥 닫으면 됨 (서버는 계속 실행)

---

## 📂 app.py 파일 구조

### 전체 구조 개요

```
app.py (670줄)
├── 1. 임포트 (1-19줄)
├── 2. 데이터베이스 모델 (21-37줄)
├── 3. AI 모델 로딩 (39-66줄)
├── 4. 유틸리티 함수들 (68-554줄)
└── 5. Streamlit UI (556-670줄)
```

### 1️⃣ 임포트 섹션 (1-19줄)

```python
import streamlit as st                    # Streamlit 프레임워크
import torch                              # PyTorch
from sentence_transformers import ...    # 문장 임베딩
from transformers import ...              # Hugging Face 모델
from paddleocr import PaddleOCR          # OCR
from sqlmodel import ...                  # 데이터베이스 ORM
from PIL import Image                     # 이미지 처리
import numpy as np                        # 수치 연산
```

**역할:** 필요한 모든 라이브러리 임포트

---

### 2️⃣ 데이터베이스 모델 (21-37줄)

```python
class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str                # 파일명
    doc_type: str                # 문서 유형
    content: str                 # OCR 텍스트
    summary: str                 # 요약
    keywords: str                # 키워드
    structured_data: str         # 구조화 데이터 (JSON)
    upload_date: datetime        # 업로드 날짜
    image_data: bytes            # 이미지 바이너리
    embedding: Optional[str]     # 벡터 임베딩 (JSON)

# SQLite DB 초기화
engine = create_engine("sqlite:///archive.db")
SQLModel.metadata.create_all(engine)
```

**역할:** 문서 정보를 저장할 DB 스키마 정의

---

### 3️⃣ AI 모델 로딩 (39-66줄)

```python
@st.cache_resource  # 모델을 캐싱하여 재사용
def load_models():
    # 1. DiT - 문서 분류 모델
    dit_processor = AutoProcessor.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
    dit_model = AutoModelForImageClassification.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")

    # 2. PaddleOCR - 한국어 OCR
    ocr = PaddleOCR(lang='korean')

    # 3. Donut - 영수증 전용 OCR
    donut_processor = AutoProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    donut_model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

    # 4. LayoutLMv3 - 문서 레이아웃 분석
    layout_processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
    layout_model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")

    # 5. KoBART - 한국어 텍스트 요약
    summarizer_tokenizer = AutoTokenizer.from_pretrained("gangyeolkim/kobart-korean-summarizer-v2")
    summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("gangyeolkim/kobart-korean-summarizer-v2")

    # 6. Ko-SRoBERTa - 벡터 임베딩
    embedding_model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    return (dit_processor, dit_model, ocr, donut_processor, donut_model,
            layout_processor, layout_model, summarizer_tokenizer, summarizer_model,
            embedding_model)
```

**역할:**
- 앱 실행 시 모든 AI 모델을 한 번만 로드
- `@st.cache_resource`로 캐싱하여 재실행 시 빠름
- **첫 실행 시 모델 다운로드로 시간 소요 (수 GB)**

---

### 4️⃣ 유틸리티 함수들 (68-554줄)

#### 4-1. 문서 분류 (68-78줄)
```python
def classify_document(image, dit_processor, dit_model):
    """DiT 모델로 문서 유형 분류"""
    inputs = dit_processor(images=image, return_tensors="pt")
    outputs = dit_model(**inputs)
    predicted_class_idx = outputs.logits.argmax(-1).item()
    predicted_class = dit_model.config.id2label[predicted_class_idx]

    if 'invoice' in predicted_class.lower():
        return "영수증"
    return predicted_class
```

#### 4-2. OCR 텍스트 추출 (96-106줄)
```python
def extract_text_with_layout(image, ocr):
    """PaddleOCR로 텍스트 및 위치 추출"""
    result = PaddleOCR(lang='korean').ocr(np.array(image))
    text = ""
    boxes = []

    if result[0]:
        for line in result[0]:
            text += line[1][0] + " "
            boxes.append(line[0])

    return text.strip(), boxes
```

#### 4-3. 구조화된 정보 추출 (109-385줄)
```python
def extract_structured_with_layoutlm(image, text, boxes, layout_processor, layout_model, doc_type):
    """LayoutLMv3로 문서 구조 분석"""
    # 영수증: 상호명, 날짜, 시간, 금액, 합계 등 추출
    # 일반 문서: 제목, 부제목, 날짜, 핵심내용 등 추출
```

#### 4-4. 텍스트 요약 (413-421줄)
```python
def summarize_text(text, tokenizer, model):
    """KoBART로 텍스트 요약"""
    inputs = tokenizer(text[:1024], return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=128, min_length=20, num_beams=4)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
```

#### 4-5. 키워드 추출 (432-445줄)
```python
def extract_keywords(text, structured_data=None):
    """불용어 제거 기반 키워드 추출"""
    stopwords = ['은', '는', '이', '가', '을', '를', ...]
    words = text.split()
    keywords = [w for w in words if len(w) > 1 and w not in stopwords]
    return ", ".join(list(set(keywords)))
```

#### 4-6. 벡터 임베딩 생성 (423-430줄)
```python
def create_embedding(text, model):
    """Ko-SRoBERTa로 문장 임베딩 생성"""
    embedding = model.encode(text)
    return embedding.tolist()
```

#### 4-7. 문서 처리 파이프라인 (447-509줄)
```python
def process_document(uploaded_file, models):
    """전체 문서 처리 워크플로우"""
    # 1. 문서 분류
    doc_type = classify_document(image, dit_processor, dit_model)

    # 2. OCR 텍스트 추출
    content, boxes = extract_text_with_layout(image, ocr)

    # 3. 구조화된 정보 추출
    structured_data = extract_structured_with_layoutlm(...)

    # 4. 요약 생성
    summary = summarize_text(content, sum_tokenizer, sum_model)

    # 5. 키워드 추출
    keywords = extract_keywords(content, structured_data)

    # 6. 임베딩 생성
    embedding = create_embedding(content + " " + summary, embedding_model)

    return doc_type, content, summary, keywords, structured_data, img_data, embedding
```

#### 4-8. 벡터 유사도 검색 (511-528줄)
```python
def search_by_similarity(query, embedding_model, session):
    """코사인 유사도 기반 의미 검색"""
    query_embedding = create_embedding(query, embedding_model)

    all_docs = session.exec(select(Document)).all()
    similarities = []

    for doc in all_docs:
        if doc.embedding:
            doc_embedding = json.loads(doc.embedding)
            similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            similarities.append((doc, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, sim in similarities[:10] if sim > 0.5]
```

---

### 5️⃣ Streamlit UI (556-670줄)

```python
# 타이틀
st.title("AI 아카이브 시스템")

# 모델 로드
with st.spinner("AI 모델 로딩 중..."):
    models = load_models()

# 탭 생성
tab1, tab2, tab3 = st.tabs(["문서 업로드", "문서 검색", "문서 목록"])

# 세션 상태 초기화
if 'processed_file' not in st.session_state:
    st.session_state.processed_file = None

# ========================================
# 탭 1: 문서 업로드 (572-635줄)
# ========================================
with tab1:
    uploaded_file = st.file_uploader("문서를 업로드하세요", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None and not st.session_state.processing_complete:
        with st.spinner("문서 처리 중..."):
            # 문서 처리
            doc_type, content, summary, keywords, structured_data, img_data, embedding = process_document(uploaded_file, models)

            # 결과 표시
            st.image(uploaded_file, caption="업로드된 문서")
            st.write(f"**문서 유형:** {doc_type}")
            st.write(f"**요약:** {summary}")
            st.write(f"**키워드:** {keywords}")

            # 저장 버튼
            if st.button("저장"):
                with Session(engine) as session:
                    doc = Document(
                        filename=uploaded_file.name,
                        doc_type=doc_type,
                        content=content,
                        summary=summary,
                        keywords=keywords,
                        structured_data=json.dumps(structured_data, ensure_ascii=False),
                        image_data=img_data,
                        embedding=json.dumps(embedding)
                    )
                    session.add(doc)
                    session.commit()
                st.success("문서가 저장되었습니다!")

# ========================================
# 탭 2: 문서 검색 (637-661줄)
# ========================================
with tab2:
    search_query = st.text_input("검색어를 입력하세요")
    search_method = st.radio("검색 방법", ["벡터 유사도 검색", "키워드 검색"])

    if st.button("검색"):
        with Session(engine) as session:
            if search_method == "벡터 유사도 검색":
                results = search_by_similarity(search_query, models[9], session)
            else:
                # 키워드 검색
                statement = select(Document).where(
                    Document.keywords.contains(search_query) |
                    Document.summary.contains(search_query)
                )
                results = session.exec(statement).all()

            if results:
                print_result_list(results)
            else:
                st.info("검색 결과가 없습니다.")

# ========================================
# 탭 3: 문서 목록 (663-670줄)
# ========================================
with tab3:
    with Session(engine) as session:
        results = session.exec(select(Document)).all()
        if results:
            print_result_list(results)
```

---

## 🎨 Streamlit 주요 컴포넌트

### UI 요소

| 컴포넌트 | 코드 | 설명 |
|---------|------|------|
| **타이틀** | `st.title("제목")` | 페이지 제목 |
| **탭** | `st.tabs(["탭1", "탭2"])` | 탭 UI |
| **파일 업로드** | `st.file_uploader()` | 파일 선택 |
| **버튼** | `st.button("클릭")` | 클릭 가능한 버튼 |
| **텍스트 입력** | `st.text_input("입력")` | 사용자 입력 필드 |
| **라디오** | `st.radio("선택", ["A", "B"])` | 단일 선택 |
| **스피너** | `with st.spinner("로딩...")` | 로딩 표시 |
| **이미지** | `st.image(image)` | 이미지 표시 |
| **텍스트** | `st.write("텍스트")` | 일반 텍스트 출력 |
| **컬럼** | `col1, col2 = st.columns(2)` | 2열 레이아웃 |
| **확장** | `st.expander("제목")` | 접을 수 있는 영역 |

### 세션 상태 관리

```python
# 세션 상태 초기화
if 'key' not in st.session_state:
    st.session_state.key = None

# 값 저장
st.session_state.key = "value"

# 값 읽기
value = st.session_state.key
```

**역할:** 페이지 새로고침 시 상태 유지

---

## 🔧 주요 데코레이터

### @st.cache_resource

```python
@st.cache_resource
def load_models():
    # 무거운 객체 로드 (모델, DB 연결 등)
    return model
```

**용도:**
- 모델, DB 연결 등 **무거운 객체를 캐싱**
- 앱 재실행 시 다시 로드하지 않음
- **메모리 효율적**

### @st.cache_data

```python
@st.cache_data
def load_data():
    # 데이터 로드 (CSV, JSON 등)
    return data
```

**용도:**
- DataFrame, 리스트 등 **데이터를 캐싱**
- 함수 인자가 같으면 캐시된 결과 반환

---

## 📊 실행 흐름

```
1. streamlit run app.py 실행
   ↓
2. 임포트 및 전역 변수 초기화
   - DB 엔진 생성
   - 테이블 생성
   ↓
3. Streamlit UI 렌더링
   - st.title() 표시
   - load_models() 호출 (캐시됨)
   ↓
4. 사용자 인터랙션 대기
   - 파일 업로드
   - 버튼 클릭
   ↓
5. 이벤트 발생 시 해당 코드 블록 재실행
   - 파일 업로드 → process_document() 실행
   - 검색 버튼 → search_by_similarity() 실행
   ↓
6. UI 업데이트
   - st.write(), st.image() 등으로 결과 표시
```

---

## 💡 개발 팁

### 1. 디버깅

```python
# 변수 출력
st.write("debug:", variable)

# JSON 출력
st.json(data)

# 에러 표시
st.error("에러 메시지")

# 경고 표시
st.warning("경고 메시지")

# 성공 메시지
st.success("성공!")
```

### 2. 레이아웃

```python
# 2열 레이아웃
col1, col2 = st.columns(2)
with col1:
    st.write("왼쪽")
with col2:
    st.write("오른쪽")

# 사이드바
with st.sidebar:
    st.write("사이드바 내용")
```

### 3. 성능 최적화

```python
# 무거운 연산은 캐싱
@st.cache_data
def expensive_computation(param):
    # 오래 걸리는 연산
    return result

# 조건부 실행
if st.button("실행"):
    # 버튼 클릭 시에만 실행
    result = expensive_computation()
```

---

## 🐛 문제 해결

### Q: 모델 로딩이 너무 오래 걸려요
**A:** 첫 실행 시 Hugging Face에서 모델 다운로드 (수 GB). 이후엔 캐시 사용으로 빠름.

### Q: 파일 업로드 후 결과가 안 나와요
**A:** `st.session_state`로 상태 관리 확인. 브라우저 새로고침 시 초기화됨.

### Q: DB에 저장이 안 돼요
**A:** `archive.db` 파일 권한 확인. SQLite는 파일 기반이라 쓰기 권한 필요.

### Q: 페이지가 계속 재실행돼요
**A:** Streamlit은 위젯 상호작용 시 전체 스크립트 재실행. `@st.cache_resource` 사용.

---

## 📚 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Streamlit Gallery](https://streamlit.io/gallery) - 예제 앱 모음

---

## 🎯 다음 단계

1. ✅ 앱 실행 테스트
2. ✅ 샘플 문서로 기능 확인
3. 📝 실습 과제 1: 이미지 전처리 구현
4. 📝 실습 과제 2: 형태소 분석 개선
5. 📝 실습 과제 3: 사진 메타데이터 추출
