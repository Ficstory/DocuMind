import cv2
import numpy as np
from PIL import Image


def convert_to_grayscale(image):
    """
    이미지를 그레이스케일로 변환

    Args:
        image: numpy array (BGR) or PIL Image

    Returns:
        numpy array: 그레이스케일 이미지
    """
    if isinstance(image, Image.Image):
        image = np.array(image)

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    return gray


def remove_noise(image, method='gaussian'):
    """
    이미지의 노이즈 제거

    Args:
        image: numpy array (grayscale)
        method: 'gaussian', 'median', 'bilateral' 중 선택

    Returns:
        numpy array: 노이즈가 제거된 이미지
    """
    if method == 'gaussian':
        # 가우시안 블러로 노이즈 제거
        denoised = cv2.GaussianBlur(image, (5, 5), 0)
    elif method == 'median':
        # 중간값 필터로 노이즈 제거 (소금-후추 노이즈에 효과적)
        denoised = cv2.medianBlur(image, 5)
    elif method == 'bilateral':
        # 양방향 필터 (엣지는 보존하면서 노이즈 제거)
        denoised = cv2.bilateralFilter(image, 9, 75, 75)
    else:
        denoised = image

    return denoised


def enhance_contrast(image, method='clahe'):
    """
    이미지 대비 개선

    Args:
        image: numpy array (grayscale)
        method: 'clahe', 'hist_eq', 'gamma' 중 선택

    Returns:
        numpy array: 대비가 개선된 이미지
    """
    if method == 'clahe':
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # 지역적 히스토그램 평활화로 과도한 증폭 방지
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
    elif method == 'hist_eq':
        # 히스토그램 평활화
        enhanced = cv2.equalizeHist(image)
    elif method == 'gamma':
        # 감마 보정
        gamma = 1.2
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                         for i in np.arange(0, 256)]).astype("uint8")
        enhanced = cv2.LUT(image, table)
    else:
        enhanced = image

    return enhanced


def binarize(image, method='adaptive'):
    """
    이미지 이진화 (텍스트와 배경 분리)

    Args:
        image: numpy array (grayscale)
        method: 'otsu', 'adaptive', 'simple' 중 선택

    Returns:
        numpy array: 이진화된 이미지
    """
    if method == 'otsu':
        # Otsu's 이진화 (자동으로 최적 임계값 찾기)
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == 'adaptive':
        # 적응형 이진화 (지역별로 다른 임계값 적용)
        binary = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    elif method == 'simple':
        # 단순 이진화
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    else:
        binary = image

    return binary


def enhance_text_regions(image, kernel_size=(2, 2)):
    """
    모폴로지 연산으로 텍스트 영역 강조

    Args:
        image: numpy array (binary)
        kernel_size: 커널 크기 (tuple)

    Returns:
        numpy array: 텍스트가 강조된 이미지
    """
    # 모폴로지 연산용 커널 생성
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Opening: 작은 노이즈 제거 (침식 후 팽창)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)

    # Closing: 텍스트 내부의 작은 구멍 메우기 (팽창 후 침식)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    return closing


def deskew_image(image):
    """
    기울어진 문서 자동 보정

    Args:
        image: numpy array (grayscale or binary)

    Returns:
        numpy array: 기울기가 보정된 이미지
        float: 보정된 각도
    """
    # 이진화 (아직 안 되어있다면)
    if len(np.unique(image)) > 2:
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        binary = image

    # 좌표 추출
    coords = np.column_stack(np.where(binary > 0))

    # 최소 영역 사각형 찾기
    angle = cv2.minAreaRect(coords)[-1]

    # 각도 보정 (-45도 ~ 45도 범위로 조정)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # 회전 변환 적용
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated, angle


def preprocess_image_for_ocr(image, enable_deskew=True):
    """
    OCR 정확도 향상을 위한 통합 전처리 파이프라인

    Args:
        image: numpy array (BGR) or PIL Image
        enable_deskew: 기울기 보정 활성화 여부

    Returns:
        dict: 전처리 단계별 결과 이미지들
            - 'original': 원본 이미지
            - 'grayscale': 그레이스케일 이미지
            - 'denoised': 노이즈 제거된 이미지
            - 'enhanced': 대비 개선된 이미지
            - 'binary': 이진화된 이미지
            - 'final': 최종 전처리된 이미지
            - 'deskew_angle': 보정된 각도 (enable_deskew=True일 때만)
    """
    results = {}

    # PIL Image를 numpy array로 변환
    if isinstance(image, Image.Image):
        image = np.array(image)
        # RGB to BGR (OpenCV 형식)
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results['original'] = image.copy()

    # 1. 그레이스케일 변환
    gray = convert_to_grayscale(image)
    results['grayscale'] = gray

    # 2. 노이즈 제거
    denoised = remove_noise(gray, method='bilateral')
    results['denoised'] = denoised

    # 3. 대비 개선
    enhanced = enhance_contrast(denoised, method='clahe')
    results['enhanced'] = enhanced

    # 4. 이진화
    binary = binarize(enhanced, method='adaptive')
    results['binary'] = binary

    # 5. 텍스트 영역 강조
    morphed = enhance_text_regions(binary, kernel_size=(2, 2))

    # 6. 기울기 보정 (선택적)
    if enable_deskew:
        final, angle = deskew_image(morphed)
        results['deskew_angle'] = angle
    else:
        final = morphed
        results['deskew_angle'] = 0.0

    results['final'] = final

    return results


def preprocess_for_display(image):
    """
    Streamlit 표시용 이미지 전처리 (PIL Image로 변환)

    Args:
        image: numpy array

    Returns:
        PIL Image: 표시용 이미지
    """
    if len(image.shape) == 2:
        # Grayscale
        return Image.fromarray(image)
    else:
        # BGR to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)
