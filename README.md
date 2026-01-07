# AI Document Archive System (DocuMind)

> 컴퓨터 비전, 자연어 처리를 통한 문서 아카이브 어플리케이션

사용자가 문서 이미지를 업로드하면 AI가 문서의 유형을 분류하고, 문서의 요약 내용, 키워드, 구조화 된 정보들을 추출하여 저장합니다. 그리고 사용자는 저장된 문서를 벡터 유사도로 검색하거나 키워드로 검색할 수 있습니다.

---

## 📌 프로젝트 개요

이 프로젝트는 AI 기술을 활용하여 문서 관리를 자동화하는 시스템입니다. 문서 이미지를 업로드하면 자동으로 문서 유형을 분류하고, OCR로 텍스트를 추출하며, 구조화된 정보를 파싱하여 데이터베이스에 저장합니다.

### 주요 기능
- ✅ **문서 유형 자동 분류** - DiT 모델을 사용한 16가지 문서 타입 분류
- ✅ **한국어 OCR** - PaddleOCR을 활용한 정확한 한국어 텍스트 추출
- ✅ **영수증 정보 자동 파싱** - Donut 모델로 영수증 구조화 데이터 추출
- ✅ **문서 레이아웃 분석** - LayoutLMv3로 문서 구조 이해 및 정보 추출
- ✅ **자동 요약** - KoBART로 한국어 문서 요약 생성
- ✅ **벡터 유사도 검색** - Ko-SRoBERTa 임베딩 기반 의미 검색
- ✅ **키워드 추출** - 불용어 제거 기반 키워드 자동 생성
- ✅ **웹 인터페이스** - Streamlit 기반 직관적인 UI

---

## 🛠️ 기술 스택

### AI & Machine Learning
| 기술 | 역할 | 사용 모델 |
|------|------|-----------|
| **DiT** (Document Image Transformer) | 문서 유형 자동 분류 | `microsoft/dit-base-finetuned-rvlcdip` |
| **PaddleOCR** | 한국어 OCR 및 텍스트 추출 | PaddleOCR + Donut (영수증 특화) |
| **Donut** | 영수증 정보 구조화 | `naver-clova-ix/donut-base-finetuned-cord-v2` |
| **LayoutLMv3** | 문서 레이아웃 분석 | `microsoft/layoutlmv3-base` |
| **KoBART** | 한국어 텍스트 자동 요약 | `gangyeolkim/kobart-korean-summarizer-v2` |
| **Ko-SRoBERTa** | 벡터 임베딩 및 유사도 검색 | `jhgan/ko-sroberta-multitask` |

### Backend & Database
| 기술 | 용도 |
|------|------|
| **SQLite + SQLModel** | 문서 정보 저장 및 검색 |
| **Streamlit** | 사용자 인터페이스 |

### Libraries
- **PyTorch** - 딥러닝 프레임워크
- **Transformers** - Hugging Face 모델 로딩
- **OpenCV** - 이미지 전처리
- **scikit-learn** - 벡터 유사도 계산
- **Pillow** - 이미지 처리

---

## 🎯 AI 모델 상세

### 1️⃣ DiT (Document Image Transformer)
- **목적**: 문서 유형 분류
- **지원 카테고리** (16가지):
  - letter, form, email, handwritten, advertisement
  - scientific report, scientific publication, file folder
  - news article, budget, invoice, presentation
  - questionnaire, resume, memo 등
- **출처**: [Microsoft DiT](https://github.com/microsoft/unilm/tree/master/dit)

### 2️⃣ PaddleOCR
- **목적**: 한국어 텍스트 추출 및 바운딩 박스 검출
- **특징**:
  - 한국어 포함 80개 이상 언어 지원
  - 텍스트 검출, 방향 분류, 텍스트 인식의 3단계 파이프라인
- **출처**: [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

### 3️⃣ Donut (Document Understanding Transformer)
- **목적**: 영수증 정보 구조화 (OCR-free)
- **추출 정보**: 상호명, 날짜, 시간, 품목, 금액 등
- **특징**: 이미지에서 직접 구조화된 정보를 수출하는 종단간 모델
- **출처**: [Naver Clova IX Donut](https://github.com/clovaai/donut)

### 4️⃣ LayoutLMv3
- **목적**: 문서 레이아웃 분석 및 정보 추출
- **특징**:
  - OCR 정보(텍스트, 위치, 이미지)를 통합하여 처리
  - 제목, 본문, 날짜, 금액 등 구조화된 정보 추출
- **출처**: [Microsoft LayoutLMv3](https://github.com/microsoft/unilm/tree/master/layoutlmv3)

### 5️⃣ KoBART
- **목적**: 한국어 텍스트 자동 요약
- **특징**:
  - SKT에서 공개한 한국어 BART 모델
  - 문서 내용을 2-3 문장으로 요약
- **출처**: [KoBART Summarizer](https://huggingface.co/gangyeolkim/kobart-korean-summarizer-v2)

### 6️⃣ Ko-SRoBERTa
- **목적**: 벡터 임베딩 생성 및 의미 기반 검색
- **특징**:
  - 문장을 768차원 벡터로 인코딩
  - 코사인 유사도를 통한 의미적 문서 검색
- **출처**: [jhgan/ko-sroberta-multitask](https://huggingface.co/jhgan/ko-sroberta-multitask)

---

## 📁 프로젝트 구조

```
14th-ai1/
├── ai-document-archive/        # 메인 프로젝트 폴더
│   ├── app.py                  # Streamlit 애플리케이션
│   ├── requirements.txt        # Python 패키지 의존성
│   ├── README.md               # 프로젝트 상세 가이드
│   └── test-image.png          # 테스트용 샘플 이미지
├── venv/                       # Python 가상환경
├── .gitignore                  # Git 제외 파일 목록
├── TODO.md                     # 작업 목록
└── README.md                   # 프로젝트 개요 (현재 파일)
```

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

### 2. 의존성 설치

```bash
# PyTorch CPU 버전 (권장 - 빠른 설치)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 나머지 패키지 설치
pip install streamlit transformers sentence-transformers paddlepaddle paddleocr sqlmodel pillow opencv-python numpy scikit-learn sentencepiece

# 또는 requirements.txt 사용 (CUDA 버전 - GPU 있는 경우)
pip install -r ai-document-archive/requirements.txt
```

### 3. 애플리케이션 실행

```bash
cd ai-document-archive
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 💡 사용 방법

### 1️⃣ 문서 업로드 탭
1. PNG/JPG/JPEG 형식의 문서 이미지 업로드
2. AI가 자동으로 문서 유형 분류 및 정보 추출
3. 요약, 키워드, 구조화된 정보 확인
4. "저장" 버튼 클릭하여 DB에 보관

### 2️⃣ 문서 검색 탭
- **벡터 유사도 검색**: 의미 기반 검색 (예: "커피 영수증")
- **키워드 검색**: 정확한 키워드 매칭

### 3️⃣ 문서 목록 탭
- 저장된 모든 문서 조회
- 이미지 미리보기 및 다운로드

---

## 📋 실습 과제

이 프로젝트는 다음 실습 과제를 포함합니다:

### 과제 1: 이미지 전처리
- OCR 정확도 향상을 위한 이미지 전처리
- 노이즈 제거, 대비 개선, 이진화, 문서 보정

### 과제 2: 형태소 분석
- 한국어 형태소 분석기(Konlpy) 통합
- TF-IDF 기반 키워드 추출 개선

### 과제 3: 사진 메타데이터 검색
- EXIF 데이터 추출 및 GPS 정보 파싱
- 사진/문서 자동 구분
- 지도 기반 위치 표시

자세한 내용은 [TODO.md](TODO.md) 참고

---

## 🔧 주요 함수 및 모듈

### 문서 처리 파이프라인
```python
def process_document(uploaded_file, models):
    # 1. 문서 유형 분류 (DiT)
    doc_type = classify_document(image, dit_processor, dit_model)

    # 2. OCR 텍스트 추출 (PaddleOCR)
    content, boxes = extract_text_with_layout(image, ocr)

    # 3. 구조화된 정보 추출 (LayoutLMv3 + Donut)
    structured_data = extract_structured_with_layoutlm(...)

    # 4. 텍스트 요약 (KoBART)
    summary = summarize_text(content, sum_tokenizer, sum_model)

    # 5. 키워드 추출
    keywords = extract_keywords(content, structured_data)

    # 6. 벡터 임베딩 생성 (Ko-SRoBERTa)
    embedding = create_embedding(content + " " + summary, embedding_model)

    return doc_type, content, summary, keywords, structured_data, embedding
```

---

## 📊 시스템 요구사항

- **Python**: 3.11+
- **메모리**: 최소 8GB RAM (모델 로딩 시)
- **저장공간**: 약 5GB (모델 캐시 포함)
- **GPU**: 선택사항 (CPU만으로도 작동)

---

## 📝 라이선스

이 프로젝트는 교육 및 학습 목적으로 제작되었습니다.

---

## 🙏 참고 자료

- [Microsoft DiT](https://github.com/microsoft/unilm/tree/master/dit)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Donut](https://github.com/clovaai/donut)
- [LayoutLMv3](https://github.com/microsoft/unilm/tree/master/layoutlmv3)
- [KoBART](https://github.com/SKT-AI/KoBART)
- [Ko-SRoBERTa](https://huggingface.co/jhgan/ko-sroberta-multitask)

---

## 📫 Contact

프로젝트 문의: [GitHub Issues](https://github.com/Ficstory/DocuMind/issues)
