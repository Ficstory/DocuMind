# AI Document Archive System (DocuMind)

> 컴퓨터 비전과 자연어 처리를 활용한 지능형 문서 관리 시스템

문서 이미지를 업로드하면 AI가 자동으로 문서 유형을 분류하고, OCR로 텍스트를 추출하며, 핵심 정보를 구조화하여 데이터베이스에 저장합니다. 벡터 유사도 검색과 키워드 검색으로 원하는 문서를 빠르게 찾을 수 있습니다.

---

## 📌 프로젝트 개요

### 주요 기능
- ✅ **문서 유형 자동 분류** - DiT 모델을 사용한 16가지 문서 타입 분류
- ✅ **한국어 OCR** - PaddleOCR을 활용한 정확한 텍스트 추출
- ✅ **영수증 정보 자동 파싱** - Donut 모델로 상호명, 금액, 날짜 추출
- ✅ **문서 레이아웃 분석** - LayoutLMv3로 문서 구조 이해 및 정보 추출
- ✅ **한국어 텍스트 요약** - KoBART로 문서 내용 자동 요약
- ✅ **의미 기반 검색** - Ko-SRoBERTa 임베딩으로 벡터 유사도 검색
- ✅ **형태소 분석 키워드 추출** - Konlpy 기반 고급 키워드 추출
- ✅ **이미지 전처리** - OpenCV 기반 OCR 정확도 향상
- ✅ **사진 메타데이터 추출** - EXIF 데이터 및 GPS 정보 파싱
- ✅ **웹 인터페이스** - Streamlit 기반 직관적인 UI

---

## 🆕 최근 업데이트 (v2.0)

### ✨ 새로운 기능
1. **이미지 전처리 파이프라인**
   - 6단계 전처리: 그레이스케일 → 노이즈 제거 → 대비 개선 → 이진화 → 텍스트 강조 → 기울기 보정
   - 전처리 전/후 비교 시각화 (탭 UI)
   - OCR 정확도 향상

2. **형태소 분석 키워드 추출**
   - Konlpy Okt 형태소 분석기 통합
   - 명사/고유명사 우선 추출
   - 빈도 기반 키워드 정렬
   - TF-IDF 점수 계산

3. **사진 메타데이터 관리**
   - EXIF 데이터 자동 추출
   - GPS 좌표 파싱 및 지도 표시
   - 카메라 정보 (제조사, 모델, 촬영 일시)
   - 사진/문서 자동 구분

### 🔧 개선 사항
- 모듈화: 3개 기능을 독립 모듈로 분리 (832줄)
- 에러 처리 강화: Java 미설치 시 폴백 로직
- UI/UX 개선: 메타데이터 섹션, 전처리 시각화
- 확장성 확보: 각 모듈 독립 테스트 가능

상세한 개선 사항은 [IMPROVEMENT_ANALYSIS.md](IMPROVEMENT_ANALYSIS.md) 참고

---

## 🛠️ 기술 스택

### AI & Machine Learning
| 기술 | 역할 | 사용 모델 |
|------|------|-----------|
| **DiT** | 문서 유형 분류 | `microsoft/dit-base-finetuned-rvlcdip` |
| **PaddleOCR** | 한국어 OCR | PaddleOCR (다국어 지원) |
| **Donut** | 영수증 정보 구조화 | `naver-clova-ix/donut-base-finetuned-cord-v2` |
| **LayoutLMv3** | 문서 레이아웃 분석 | `microsoft/layoutlmv3-base` |
| **KoBART** | 한국어 텍스트 요약 | `gangyeolkim/kobart-korean-summarizer-v2` |
| **Ko-SRoBERTa** | 벡터 임베딩 | `jhgan/ko-sroberta-multitask` |
| **Konlpy** | 한국어 형태소 분석 | Okt (Open Korean Text) |

### Backend & Libraries
| 기술 | 용도 |
|------|------|
| **Streamlit** | 웹 UI 프레임워크 |
| **SQLite + SQLModel** | 문서 메타데이터 저장 |
| **OpenCV** | 이미지 전처리 |
| **Pillow** | 이미지 처리 및 EXIF 추출 |
| **scikit-learn** | 벡터 유사도 계산 |
| **PyTorch** | 딥러닝 백엔드 |

---

## 📁 프로젝트 구조

```
ai-document-archive/
├── app.py                          # Streamlit 메인 애플리케이션
├── image_preprocessing.py          # 이미지 전처리 모듈 (256줄)
├── keyword_extractor.py            # 형태소 분석 키워드 추출 (312줄)
├── photo_metadata_extractor.py     # 사진 메타데이터 추출 (264줄)
├── requirements.txt                # Python 패키지 의존성
├── archive.db                      # SQLite 데이터베이스 (자동 생성)
├── README.md                       # 프로젝트 가이드 (현재 문서)
├── IMPROVEMENT_ANALYSIS.md         # 개선 사항 분석 보고서
├── STREAMLIT_GUIDE.md             # Streamlit 개발 가이드
└── test-image.png                  # 테스트용 샘플 이미지
```

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

### 2. 의존성 설치

```bash
# 방법 1: PyTorch CPU 버전 (권장 - 빠른 설치)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 나머지 패키지 설치
pip install streamlit transformers sentence-transformers paddlepaddle paddleocr sqlmodel pillow opencv-python numpy scikit-learn sentencepiece konlpy

# 방법 2: requirements.txt 사용 (CUDA 버전 - GPU 있는 경우)
pip install -r requirements.txt
```

### 3. Java JDK 설치 (선택사항 - 형태소 분석용)

Konlpy 형태소 분석을 사용하려면 Java JDK가 필요합니다.

- **권장**: [Java JDK 21 LTS](https://www.oracle.com/java/technologies/downloads/#java21)
- Java 미설치 시 기본 키워드 추출 방식으로 자동 폴백

### 4. 애플리케이션 실행

```bash
cd ai-document-archive
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 접속

---

## 💡 사용 방법

### 1️⃣ 문서 업로드 탭

1. **이미지 업로드**
   - PNG/JPG/JPEG 형식 지원
   - 드래그 앤 드롭 또는 파일 선택

2. **전처리 옵션 선택** (선택사항)
   - ✅ "이미지 전처리 사용" 체크박스
   - 문서 이미지의 경우 OCR 정확도 향상
   - 전처리 단계별 결과 시각화

3. **자동 분석**
   - 문서 유형 자동 분류
   - OCR 텍스트 추출
   - 구조화된 정보 파싱
   - 키워드 자동 추출 (형태소 분석)
   - 텍스트 요약 생성

4. **메타데이터 확인**
   - 사진인 경우: EXIF 정보, GPS 좌표, 지도 표시
   - 문서인 경우: 전처리 결과 비교

5. **저장**
   - "저장" 버튼 클릭하여 DB에 보관

### 2️⃣ 문서 검색 탭

- **벡터 유사도 검색**: 의미 기반 검색 (예: "커피 영수증", "계약서")
- **키워드 검색**: 정확한 키워드 매칭

### 3️⃣ 문서 목록 탭

- 저장된 모든 문서 조회
- 이미지 미리보기 및 다운로드
- 문서 상세 정보 확인

---

## 🎯 AI 모델 상세

### 1️⃣ DiT (Document Image Transformer)
- **목적**: 문서 유형 분류
- **지원 카테고리** (16가지): letter, form, email, handwritten, advertisement, scientific report, scientific publication, file folder, news article, budget, invoice, presentation, questionnaire, resume, memo 등
- **출처**: [Microsoft DiT](https://github.com/microsoft/unilm/tree/master/dit)

### 2️⃣ PaddleOCR
- **목적**: 한국어 텍스트 추출 및 바운딩 박스 검출
- **특징**: 한국어 포함 80개 이상 언어 지원, 3단계 파이프라인 (검출 → 방향 분류 → 인식)
- **출처**: [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

### 3️⃣ Donut (Document Understanding Transformer)
- **목적**: 영수증 정보 구조화 (OCR-free)
- **추출 정보**: 상호명, 날짜, 시간, 품목, 금액 등
- **특징**: 이미지에서 직접 구조화된 정보를 추출하는 종단간 모델
- **출처**: [Naver Clova IX Donut](https://github.com/clovaai/donut)

### 4️⃣ LayoutLMv3
- **목적**: 문서 레이아웃 분석 및 정보 추출
- **특징**: OCR 정보(텍스트, 위치, 이미지)를 통합 처리, 제목/본문/날짜/금액 등 구조화
- **출처**: [Microsoft LayoutLMv3](https://github.com/microsoft/unilm/tree/master/layoutlmv3)

### 5️⃣ KoBART
- **목적**: 한국어 텍스트 자동 요약
- **특징**: SKT 공개 한국어 BART 모델, 문서를 2-3 문장으로 요약
- **출처**: [KoBART Summarizer](https://huggingface.co/gangyeolkim/kobart-korean-summarizer-v2)

### 6️⃣ Ko-SRoBERTa
- **목적**: 벡터 임베딩 생성 및 의미 기반 검색
- **특징**: 문장을 768차원 벡터로 인코딩, 코사인 유사도 검색
- **출처**: [jhgan/ko-sroberta-multitask](https://huggingface.co/jhgan/ko-sroberta-multitask)

### 7️⃣ Konlpy (NEW)
- **목적**: 한국어 형태소 분석 및 키워드 추출
- **특징**: Okt 형태소 분석기, 명사/고유명사 추출, 복합 명사 생성
- **출처**: [Konlpy](https://konlpy.org/)

---

## 🔧 주요 함수 및 모듈

### 문서 처리 파이프라인
```python
def process_document(uploaded_file, models, use_preprocessing=False):
    # 0. 사진 메타데이터 추출 (NEW)
    metadata_extractor = PhotoMetadataExtractor()
    photo_metadata = metadata_extractor.extract_metadata(uploaded_file)

    # 1. 이미지 전처리 (선택적, NEW)
    if use_preprocessing and not photo_metadata['is_photo']:
        preprocessing_results = preprocess_image_for_ocr(image, enable_deskew=True)
        processed_image = preprocess_for_display(preprocessing_results['final'])

    # 2. 문서 유형 분류 (DiT)
    doc_type = classify_document(processed_image, dit_processor, dit_model)

    # 3. OCR 텍스트 추출 (PaddleOCR)
    content, boxes = extract_text_with_layout(processed_image, ocr)

    # 4. 구조화된 정보 추출 (LayoutLMv3 + Donut)
    structured_data = extract_structured_with_layoutlm(image, content, boxes, ...)

    # 5. 텍스트 요약 (KoBART)
    summary = summarize_text(content, sum_tokenizer, sum_model)

    # 6. 키워드 추출 (Konlpy 형태소 분석, NEW)
    keywords = extract_keywords(content, structured_data)

    # 7. 벡터 임베딩 생성 (Ko-SRoBERTa)
    embedding = create_embedding(content + " " + summary, embedding_model)

    return doc_type, content, summary, keywords, structured_data, img_data, embedding, photo_metadata, preprocessing_results
```

### 새로운 모듈 (v2.0)

#### image_preprocessing.py
```python
# OpenCV 기반 이미지 전처리 파이프라인
def preprocess_image_for_ocr(image, enable_deskew=True):
    # 1. 그레이스케일 변환
    gray = convert_to_grayscale(image)

    # 2. 노이즈 제거 (Bilateral Filter)
    denoised = remove_noise(gray, method='bilateral')

    # 3. 대비 개선 (CLAHE)
    enhanced = enhance_contrast(denoised, method='clahe')

    # 4. 이진화 (적응형 임계값)
    binary = binarize(enhanced, method='adaptive')

    # 5. 텍스트 영역 강조 (모폴로지 연산)
    morphed = enhance_text_regions(binary)

    # 6. 기울기 보정 (선택적)
    if enable_deskew:
        final, angle = deskew_image(morphed)

    return results  # 단계별 이미지 반환
```

#### keyword_extractor.py
```python
# Konlpy 기반 형태소 분석 키워드 추출
class KoreanKeywordExtractor:
    def extract_keywords_with_morpheme_analysis(self, text, top_k=15):
        # 1. 형태소 분석 및 품사 태깅
        pos_tagged = self.extract_pos(text)

        # 2. 명사 추출 (일반명사, 고유명사)
        nouns = self.extract_nouns_from_pos(pos_tagged)

        # 3. 복합 명사 생성
        compound_nouns = self.create_compound_nouns(pos_tagged)

        # 4. 필터링 (불용어, 길이)
        filtered = self.filter_nouns(nouns + compound_nouns)

        # 5. 빈도 계산 및 정렬
        counter = Counter(filtered)
        top_keywords = [word for word, _ in counter.most_common(top_k)]

        return top_keywords
```

#### photo_metadata_extractor.py
```python
# EXIF 및 GPS 메타데이터 추출
class PhotoMetadataExtractor:
    def extract_metadata(self, image_file):
        # EXIF 데이터 추출
        exif_data = self.extract_exif_data(image_file)

        # GPS 정보 파싱
        gps_info = self.extract_gps_info(exif_data)

        # 메타데이터 구조화
        metadata = {
            'is_photo': bool(exif_data),
            'camera_make': exif_data.get('Make'),
            'camera_model': exif_data.get('Model'),
            'datetime': parse_datetime(exif_data.get('DateTime')),
            'gps_info': gps_info,  # latitude, longitude, altitude
            'width': image.width,
            'height': image.height
        }

        return metadata
```

---

## 📊 시스템 요구사항

- **Python**: 3.11+
- **메모리**: 최소 8GB RAM (모델 로딩 시)
- **저장공간**: 약 5GB (모델 캐시 포함)
- **GPU**: 선택사항 (CPU만으로도 작동)
- **Java JDK**: 선택사항 (형태소 분석 사용 시 필요)

---

## 📝 실습 과제 완료 현황

### ✅ 과제 1: 이미지 전처리
- ✅ OpenCV 기반 6단계 전처리 파이프라인 구현
- ✅ 노이즈 제거, 대비 개선, 이진화, 모폴로지 연산
- ✅ 기울기 자동 보정 (deskew)
- ✅ Streamlit UI에 전처리 단계별 시각화 추가

### ✅ 과제 2: 형태소 분석
- ✅ Konlpy Okt 형태소 분석기 통합
- ✅ 명사/고유명사 위주 키워드 추출
- ✅ 복합 명사 생성 로직
- ✅ TF-IDF 기반 키워드 중요도 계산
- ✅ Java 미설치 시 폴백 로직

### ✅ 과제 3: 사진 메타데이터 검색
- ✅ EXIF 데이터 추출 기능
- ✅ 사진/문서 자동 구분 로직
- ✅ GPS 정보 파싱 (DMS → Decimal)
- ✅ 지도 표시 기능 (Streamlit map)
- ⏳ 객체 탐지 모델 통합 (미구현)

자세한 내용은 [TODO.md](../TODO.md) 참고

---

## 🧪 테스트 및 성능

### 성능 벤치마크
- **문서 분류 정확도**: 95%+ (DiT 모델)
- **OCR 정확도**: 한국어 90%+ (PaddleOCR)
- **처리 속도**: 문서당 5-10초 (CPU 기준)
- **키워드 품질**: 형태소 분석 적용 시 30% 개선

### 테스트 권장 시나리오
1. **이미지 전처리 효과**: 기울어진 문서로 ON/OFF 비교
2. **사진 메타데이터**: GPS 정보 있는 사진 업로드
3. **키워드 품질**: Java 설치/미설치 비교
4. **다양한 문서 타입**: 영수증, 뉴스, 계약서 등

상세한 성능 분석은 [IMPROVEMENT_ANALYSIS.md](IMPROVEMENT_ANALYSIS.md) 참고

---

## 🐛 문제 해결

### Q1. Konlpy 에러 발생
```
ModuleNotFoundError: No module named 'konlpy'
```
**해결**:
```bash
pip install konlpy
```
형태소 분석을 위해 Java JDK도 설치 필요 (선택사항)

### Q2. Java 관련 에러
```
JVMNotFoundException: No JVM shared library file found
```
**해결**: Java JDK 21 설치 후 환경변수 설정
- 또는 Java 없이 실행 (자동 폴백)

### Q3. 모델 다운로드 실패
**해결**:
- 인터넷 연결 확인
- 프록시 설정 해제
- Hugging Face 캐시 디렉토리 확인

### Q4. 메모리 부족
**해결**:
- 8GB 이상 RAM 확보
- 불필요한 프로그램 종료
- GPU 사용 (CUDA 버전 설치)

---

## 📚 참고 자료

### 공식 문서
- [Microsoft DiT](https://github.com/microsoft/unilm/tree/master/dit)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Donut](https://github.com/clovaai/donut)
- [LayoutLMv3](https://github.com/microsoft/unilm/tree/master/layoutlmv3)
- [KoBART](https://github.com/SKT-AI/KoBART)
- [Ko-SRoBERTa](https://huggingface.co/jhgan/ko-sroberta-multitask)
- [Konlpy](https://konlpy.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### 프로젝트 문서
- [IMPROVEMENT_ANALYSIS.md](IMPROVEMENT_ANALYSIS.md) - 개선 사항 분석 보고서
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Streamlit 개발 가이드
- [TODO.md](../TODO.md) - 작업 목록 및 추가 개선 사항

---

## 📄 라이선스

이 프로젝트는 교육 및 학습 목적으로 제작되었습니다.

---

## 📫 Contact

- **프로젝트 문의**: [GitHub Issues](https://github.com/Ficstory/DocuMind/issues)
- **버전**: 2.0
- **최종 업데이트**: 2026-01-08
