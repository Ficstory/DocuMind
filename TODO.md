# DocuMind - TODO List

## 🚀 현재 상태
- [x] 프로젝트 초기 세팅 완료
- [x] 가상환경(venv) 구성
- [x] .gitignore 설정
- [x] Git 원격 저장소 연결 (GitLab + GitHub)
- [x] 첫 커밋 완료
- [ ] 의존성 설치 진행 중 (`pip install -r requirements.txt`)

---

## 📋 실습 과제 (우선 작업)

### 실습 과제 1: 이미지 전처리
**요구사항:**
- [ ] 인식률을 높일 텍스트와 배경 분리
- [ ] 노이즈 제거 및 선명도 향상
- [ ] 기울어진 문서 자동 보정
- [ ] 전처리 전후 비교 옵션을 제공하고 비교 결과 시각화

**Pseudo Code 참고:**
```python
def preprocess_image_for_ocr(image):
    # 1. 그레이스케일 변환
    # 2. 노이즈 제거
    # 3. 대비 개선
    # 4. 이진화 (텍스트와 배경 분리)
    # 5. 텍스트 영역 강조
```

**구현 항목:**
- [ ] OpenCV를 활용한 전처리 함수 구현
- [ ] 노이즈 제거, 대비 개선, 이진화, 모폴로지 연산 적용
- [ ] Streamlit UI에 전처리 비교 결과 시각화 추가
- [ ] 전처리 전/후 OCR 정확도 비교 테스트

---

### 실습 과제 2: 형태소 분석
**요구사항:**
- [ ] 단순히 불용어 제거를 통해 키워드를 추출하는 방식을 한국어 형태소 분석 키워드 추출 방식으로 바꿔 키워드 추출의 정능을 개선

**Pseudo Code 참고:**
```python
def extract_keywords_with_morpheme_analysis(text, top_k=15):
    # 1. 형태소 분석 및 품사 태깅
    pos_tagged = morpheme_analyze(text)

    # 2. 명사만 추출 (일반명사, 고유명사)
    nouns = extract_nouns_from_pos(pos_tagged)

    # 3. 복합 명사 생성
    compound_nouns = create_compound_nouns(pos_tagged)

    # 4. TF-IDF 점수 계산
    word_scores = calculate_tfidf_scores(nouns)

    # 5. 점수 기준 상위 키워드 선택
    top_keywords = select_top_keywords(word_scores, top_k)

    return top_keywords
```

**구현 항목:**
- [ ] 한국어 형태소 분석기(Konlpy) 통합
- [ ] 명사, 고유명사 위주의 키워드 추출
- [ ] 복합 명사 및 신조어 처리
- [ ] TF-IDF 기반 키워드 중요도 계산
- [ ] 기존 불용어 제거 방식과 비교 테스트

---

### 실습 과제 3: 사진 구분 및 메타데이터 검색
**요구사항:**
- [ ] EXIF 데이터로 사진 구분 및 메타데이터 추출
- [ ] 사진 내용 인식을 위한 객체 탐지
- [ ] 사진 레벨 데이터 기반 검색 기능
- [ ] 사진에 위치 정보가 존재하는 경우 지도에 마커 표시

**Pseudo Code 참고:**
```python
def extract_photo_metadata(image):
    # 1. EXIF 데이터 읽기
    exif_info = read_exif_data(image)

    # 2. 주요 정보 추출 (날짜, 카메라, GPS)
    metadata = extract_key_info(exif_info)

    # 3. GPS 좌표를 위도/경도로 변환
    if metadata.get('gps_info'):
        metadata['location'] = convert_gps_to_coordinates(metadata['gps_info'])

    return metadata

def detect_photo_objects(image):
    # 사진에서 객체 탐지
    # 객체 목록 반환
```

**구현 항목:**
- [ ] EXIF 데이터 추출 기능 구현
- [ ] 사진/문서 자동 구분 로직
- [ ] GPS 정보 파싱 및 지도 표시 기능
- [ ] 객체 탐지 모델 통합 (선택)
- [ ] 메타데이터 기반 검색 필터 추가

---

## 📋 추가 작업 항목

### 1. 환경 설정 & 테스트
- [ ] 의존성 설치 완료 확인
- [ ] Streamlit 앱 실행 테스트 (`streamlit run ai-document-archive/app.py`)
- [ ] 샘플 이미지로 기본 기능 테스트
- [ ] 데이터베이스(archive.db) 생성 확인

### 2. 문서화
- [ ] README.md 개선
  - [ ] 프로젝트 소개 및 주요 기능 상세 설명
  - [ ] 시스템 요구사항 명시
  - [ ] 설치 가이드 개선 (가상환경 포함)
  - [ ] 사용 예시 스크린샷 추가
  - [ ] 기술 스택 상세 설명
  - [ ] 실습 과제 구현 내용 정리
- [ ] 코드 주석 개선
- [ ] 실습 과제별 구현 문서 작성

### 3. 코드 개선
- [ ] 에러 핸들링 강화
  - [ ] 파일 업로드 실패 시 처리
  - [ ] OCR 실패 시 fallback 로직
  - [ ] 모델 로딩 실패 처리
- [ ] 코드 리팩토링
  - [ ] 긴 함수 분리 (특히 `process_document`)
  - [ ] 상수 분리 (magic number/string 제거)
  - [ ] 설정 파일 분리 (config.py)
- [ ] 성능 최적화
  - [ ] 모델 캐싱 최적화
  - [ ] 대용량 이미지 처리 개선

### 4. 기능 추가
- [ ] 다중 파일 업로드 지원
- [ ] PDF 파일 지원 추가
- [ ] 문서 편집/삭제 기능
- [ ] 검색 필터 개선 (날짜, 문서 유형별, 메타데이터)
- [ ] 문서 내보내기 (CSV, JSON)
- [ ] 통계 대시보드 추가

### 5. 테스트
- [ ] 단위 테스트 작성 (pytest)
- [ ] 통합 테스트 작성
- [ ] 다양한 문서 유형으로 테스트
- [ ] 실습 과제 구현 내용 검증

### 6. Git 관리
- [ ] 브랜치 전략 수립 (feature/fix 브랜치)
- [ ] 실습 과제별 브랜치 생성 권장
- [ ] 커밋 컨벤션 정립

---

## 🔥 우선순위 (High Priority)

1. **의존성 설치 완료 후 앱 실행 테스트**
2. **실습 과제 1: 이미지 전처리 구현**
3. **실습 과제 2: 형태소 분석 키워드 추출**
4. **실습 과제 3: 사진 메타데이터 검색**
5. **README.md 개선** (실습 과제 내용 포함)

---

## 💡 개선 아이디어

- 실시간 OCR 결과 표시
- 문서 비교 기능
- 태그 시스템
- 자동 분류 규칙 학습
- 모바일 반응형 UI

---

## 📝 메모

- 현재 모델 다운로드 시간이 오래 걸림 → 초기 설치 가이드에 명시 필요
- PaddleOCR, Transformers 모델이 자동으로 다운로드됨 (~수 GB)
- GPU 사용 시 성능 향상 가능
- 실습 과제는 각각 별도 브랜치로 작업 권장 (feature/preprocess, feature/morpheme, feature/metadata)
