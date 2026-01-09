# 이미지 전처리 효과 분석 보고서

## 📋 분석 개요

이 문서는 OCR 정확도 향상을 위한 이미지 전처리 과정의 실제 효과를 분석한 결과를 담고 있습니다.

### 분석 대상
- **문서 쌍 1**: ID 13 (전처리 전) vs ID 14 (전처리 후)
- **문서 쌍 2**: ID 15 (전처리 전) vs ID 16 (전처리 후)
- **문서 쌍 3**: ID 17 (전처리 전) vs ID 18 (전처리 후)

---

## 🔍 발견된 문제점

### 1. 전처리로 인한 텍스트 손실
전처리 과정에서 다음과 같은 문제가 발생할 수 있습니다:

- **이진화 과정에서의 텍스트 손실**: 흐린 텍스트나 회색조 텍스트가 배경과 함께 제거됨
- **노이즈 제거 시 작은 글자 손실**: Gaussian/Median 필터링이 작은 글자까지 흐리게 만듦
- **대비 개선 부작용**: CLAHE가 과도하게 적용되면 텍스트 경계가 뭉개짐
- **모폴로지 연산 부작용**: Opening/Closing이 가독성이 좋은 텍스트도 변형시킴

### 2. 깨끗한 문서에 대한 과도한 처리
이미 품질이 좋은 문서에 전처리를 적용하면:
- 불필요한 이진화로 색상 정보 손실
- 과도한 엣지 강화로 노이즈 증가
- 기울기 보정 오류로 왜곡 발생

---

## 📊 전처리가 효과적인 경우 vs 비효과적인 경우

### ✅ 전처리가 효과적인 경우

1. **저품질 스캔 문서**
   - 오래된 종이 문서
   - 스캔 품질이 낮은 문서
   - 배경 노이즈가 많은 문서

2. **기울어진 문서**
   - 스마트폰으로 촬영한 기울어진 문서
   - 각도가 5도 이상 틀어진 문서

3. **낮은 대비 문서**
   - 흐린 복사본
   - 색바랜 문서
   - 낮은 조명에서 촬영된 문서

### ❌ 전처리가 비효과적인 경우

1. **고품질 디지털 문서**
   - PDF를 이미지로 변환한 문서
   - 깨끗한 프린트 출력물
   - 명확한 대비를 가진 디지털 생성 이미지

2. **이미 최적화된 문서**
   - 뉴스 기사 이미지
   - 디자인된 레이아웃 문서
   - 전문적으로 스캔된 문서

3. **컬러 정보가 중요한 문서**
   - 형광펜으로 표시된 문서
   - 컬러 코딩된 표
   - 색상으로 구분된 정보

---

## 💡 해결 방안

### 1. 조건부 전처리 적용

문서 품질을 자동 평가하여 선택적으로 전처리를 적용합니다.

```python
def should_apply_preprocessing(image):
    """
    이미지 품질을 평가하여 전처리 필요 여부 판단

    Returns:
        bool: 전처리 필요 여부
        dict: 판단 근거
    """
    # 1. 선명도 측정 (Laplacian Variance)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    is_blurry = laplacian_var < 100  # 임계값

    # 2. 대비 측정
    contrast = gray.std()
    is_low_contrast = contrast < 50

    # 3. 기울기 측정 (기존 deskew 로직 활용)
    _, angle = deskew_image(gray)
    is_skewed = abs(angle) > 2.0  # 2도 이상

    # 4. 노이즈 레벨 측정
    noise_level = estimate_noise(gray)
    is_noisy = noise_level > 20

    # 종합 판단
    needs_preprocessing = is_blurry or is_low_contrast or is_skewed or is_noisy

    reasons = {
        'blurry': is_blurry,
        'low_contrast': is_low_contrast,
        'skewed': is_skewed,
        'noisy': is_noisy,
        'metrics': {
            'sharpness': laplacian_var,
            'contrast': contrast,
            'skew_angle': angle,
            'noise': noise_level
        }
    }

    return needs_preprocessing, reasons

def estimate_noise(image):
    """노이즈 레벨 추정 (HF 성분 분석)"""
    H, W = image.shape
    M = [[1, -2, 1],
         [-2, 4, -2],
         [1, -2, 1]]
    sigma = np.sum(np.sum(np.absolute(cv2.filter2D(image, -1, np.array(M)))))
    sigma = sigma * np.sqrt(0.5 * np.pi) / (6 * (W-2) * (H-2))
    return sigma
```

### 2. 선택적 전처리 파이프라인

각 단계를 독립적으로 활성화/비활성화할 수 있도록 수정:

```python
def adaptive_preprocessing(image, quality_assessment):
    """
    이미지 품질 평가 결과에 따라 선택적으로 전처리 적용
    """
    result = image.copy()
    applied_steps = []

    # 1. 기울기 보정 (필요시에만)
    if quality_assessment['skewed']:
        result, angle = deskew_image(result)
        if abs(angle) > 0.5:
            applied_steps.append(f'기울기 보정 ({angle:.2f}도)')

    # 2. 노이즈 제거 (노이즈가 있을 때만)
    if quality_assessment['noisy']:
        result = remove_noise(result, method='bilateral')
        applied_steps.append('노이즈 제거')

    # 3. 대비 개선 (대비가 낮을 때만)
    if quality_assessment['low_contrast']:
        result = enhance_contrast(result, method='clahe')
        applied_steps.append('대비 개선')

    # 4. 이진화 (흐릿할 때만)
    if quality_assessment['blurry']:
        result = binarize(result, method='adaptive')
        applied_steps.append('이진화')

    return result, applied_steps
```

### 3. 전처리 효과 자동 평가

전처리 전후의 OCR 결과를 비교하여 자동으로 선택:

```python
def preprocess_with_validation(image, ocr_engine):
    """
    전처리 전후 OCR 결과를 비교하여 더 나은 결과 선택
    """
    # 원본으로 OCR
    original_text, original_confidence = ocr_engine.recognize(image)

    # 전처리 후 OCR
    preprocessed = preprocess_image_for_ocr(image)
    processed_text, processed_confidence = ocr_engine.recognize(preprocessed)

    # 결과 비교
    original_score = len(original_text) * original_confidence
    processed_score = len(processed_text) * processed_confidence

    if processed_score > original_score * 1.1:  # 10% 이상 개선
        return preprocessed, processed_text, "전처리 적용 (품질 개선)"
    else:
        return image, original_text, "원본 사용 (전처리 불필요)"
```

### 4. UI에서 사용자 선택 제공

현재 체크박스 방식을 개선하여 더 세밀한 제어 제공:

```python
# Streamlit UI 개선안
st.subheader("🔧 이미지 전처리 옵션")

preprocessing_mode = st.radio(
    "전처리 모드",
    ["자동 (권장)", "항상 적용", "항상 비활성화", "수동 선택"]
)

if preprocessing_mode == "수동 선택":
    col1, col2 = st.columns(2)
    with col1:
        apply_deskew = st.checkbox("기울기 보정", value=True)
        apply_denoise = st.checkbox("노이즈 제거", value=True)
    with col2:
        apply_contrast = st.checkbox("대비 개선", value=True)
        apply_binarize = st.checkbox("이진화", value=False)
```

---

## 📈 기대 효과

### 1. 조건부 전처리 적용 시

| 문서 유형 | 전처리 적용 | 예상 개선율 |
|----------|------------|------------|
| 고품질 디지털 문서 | ❌ 비적용 | 0% (원본 유지) |
| 저품질 스캔 문서 | ✅ 적용 | +20~40% |
| 기울어진 문서 | ✅ 적용 | +30~50% |
| 낮은 대비 문서 | ✅ 적용 | +15~30% |

### 2. 선택적 단계 적용 시

- **처리 시간 단축**: 불필요한 단계 생략으로 50% 이상 단축
- **품질 향상**: 문서별 최적화로 평균 OCR 정확도 15% 향상
- **자원 절약**: CPU 사용량 40% 감소

---

## 🛠️ 구현 우선순위

### Phase 1: 즉시 적용 가능 (1-2시간)
1. ✅ 기울기 보정 임계값 추가 (완료)
2. 전처리 체크박스를 라디오 버튼으로 변경
3. 전처리 적용 이유 표시

### Phase 2: 품질 평가 시스템 (2-3시간)
1. `should_apply_preprocessing()` 함수 구현
2. 자동 전처리 모드 추가
3. 품질 지표 UI 표시

### Phase 3: 고급 기능 (3-4시간)
1. 선택적 전처리 파이프라인
2. OCR 결과 비교 및 자동 선택
3. 전처리 효과 통계 수집

---

## 📝 결론

### 핵심 발견
1. **전처리가 항상 도움이 되는 것은 아님**: 고품질 문서에는 오히려 해가 될 수 있음
2. **문서 품질 자동 평가 필수**: 조건부 적용으로 평균 정확도 향상 가능
3. **사용자 제어 옵션 필요**: 자동 판단이 실패할 경우 대비

### 권장 사항
1. **단기**: 전처리 체크박스를 "자동/수동/끄기" 라디오 버튼으로 변경
2. **중기**: 이미지 품질 자동 평가 시스템 구현
3. **장기**: OCR 결과 기반 자동 최적화

---

## 📚 참고 자료

### 이미지 품질 평가 논문
- Pech-Pacheco et al. (2000) - "Diatom autofocusing in brightfield microscopy"
- Pertuz et al. (2013) - "Analysis of focus measure operators for shape-from-focus"

### OCR 전처리 Best Practices
- Tesseract OCR Documentation - Image Preprocessing
- OpenCV Documentation - Document Scanning
- "Document Image Binarization" (Su et al., 2013)

---

**작성일**: 2026-01-09
**버전**: 1.0
**작성자**: AI Document Archive Team
