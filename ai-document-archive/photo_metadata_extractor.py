from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import io


class PhotoMetadataExtractor:
    """
    사진 EXIF 메타데이터 추출기
    """

    def __init__(self):
        pass

    def extract_exif_data(self, image_file):
        """
        이미지 파일에서 EXIF 데이터 추출

        Args:
            image_file: PIL Image 객체 또는 파일 경로 또는 BytesIO

        Returns:
            dict: EXIF 데이터 딕셔너리
        """
        try:
            # 이미지 열기
            if isinstance(image_file, str):
                image = Image.open(image_file)
            elif isinstance(image_file, bytes):
                image = Image.open(io.BytesIO(image_file))
            elif isinstance(image_file, io.BytesIO):
                image = Image.open(image_file)
            else:
                image = image_file

            # EXIF 데이터 추출
            exif_data = {}
            exif = image.getexif()

            if exif is None:
                return exif_data

            # EXIF 태그 변환
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                exif_data[tag_name] = value

            return exif_data

        except Exception as e:
            print(f"EXIF 추출 실패: {e}")
            return {}

    def extract_gps_info(self, exif_data):
        """
        EXIF 데이터에서 GPS 정보 추출

        Args:
            exif_data: EXIF 데이터 딕셔너리

        Returns:
            dict: GPS 정보 (위도, 경도, 고도 등)
        """
        gps_info = {}

        if 'GPSInfo' not in exif_data:
            return gps_info

        gps_data = exif_data['GPSInfo']

        # GPS 태그 변환
        gps_decoded = {}
        for tag_id in gps_data:
            tag_name = GPSTAGS.get(tag_id, tag_id)
            gps_decoded[tag_name] = gps_data[tag_id]

        # 위도 추출
        if 'GPSLatitude' in gps_decoded and 'GPSLatitudeRef' in gps_decoded:
            lat = self._convert_to_degrees(gps_decoded['GPSLatitude'])
            if gps_decoded['GPSLatitudeRef'] == 'S':
                lat = -lat
            gps_info['latitude'] = lat

        # 경도 추출
        if 'GPSLongitude' in gps_decoded and 'GPSLongitudeRef' in gps_decoded:
            lon = self._convert_to_degrees(gps_decoded['GPSLongitude'])
            if gps_decoded['GPSLongitudeRef'] == 'W':
                lon = -lon
            gps_info['longitude'] = lon

        # 고도 추출
        if 'GPSAltitude' in gps_decoded:
            altitude = float(gps_decoded['GPSAltitude'])
            if 'GPSAltitudeRef' in gps_decoded and gps_decoded['GPSAltitudeRef'] == 1:
                altitude = -altitude
            gps_info['altitude'] = altitude

        return gps_info

    def _convert_to_degrees(self, value):
        """
        GPS 좌표를 도(degree) 단위로 변환

        Args:
            value: GPS 좌표 값 (degrees, minutes, seconds)

        Returns:
            float: 도 단위 좌표
        """
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    def extract_metadata(self, image_file):
        """
        이미지에서 주요 메타데이터 추출

        Args:
            image_file: PIL Image 객체 또는 파일 경로

        Returns:
            dict: 메타데이터 딕셔너리
        """
        metadata = {
            'is_photo': False,
            'has_exif': False,
            'has_gps': False,
            'camera_make': None,
            'camera_model': None,
            'datetime': None,
            'gps_info': {},
            'width': None,
            'height': None,
            'orientation': None
        }

        try:
            # 이미지 열기
            if isinstance(image_file, str):
                image = Image.open(image_file)
            elif isinstance(image_file, bytes):
                image = Image.open(io.BytesIO(image_file))
            elif isinstance(image_file, io.BytesIO):
                image = Image.open(image_file)
            else:
                image = image_file

            # 기본 정보
            metadata['width'] = image.width
            metadata['height'] = image.height
            metadata['format'] = image.format

            # EXIF 데이터 추출
            exif_data = self.extract_exif_data(image)

            if exif_data:
                metadata['has_exif'] = True
                metadata['is_photo'] = True

                # 카메라 정보
                if 'Make' in exif_data:
                    metadata['camera_make'] = exif_data['Make']
                if 'Model' in exif_data:
                    metadata['camera_model'] = exif_data['Model']

                # 촬영 날짜
                if 'DateTime' in exif_data:
                    try:
                        metadata['datetime'] = datetime.strptime(
                            exif_data['DateTime'], '%Y:%m:%d %H:%M:%S'
                        )
                    except:
                        metadata['datetime'] = exif_data['DateTime']
                elif 'DateTimeOriginal' in exif_data:
                    try:
                        metadata['datetime'] = datetime.strptime(
                            exif_data['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S'
                        )
                    except:
                        metadata['datetime'] = exif_data['DateTimeOriginal']

                # 방향 정보
                if 'Orientation' in exif_data:
                    metadata['orientation'] = exif_data['Orientation']

                # GPS 정보
                gps_info = self.extract_gps_info(exif_data)
                if gps_info:
                    metadata['has_gps'] = True
                    metadata['gps_info'] = gps_info

            return metadata

        except Exception as e:
            print(f"메타데이터 추출 실패: {e}")
            return metadata

    def is_photo(self, image_file):
        """
        이미지가 사진인지 문서인지 판별

        Args:
            image_file: PIL Image 객체 또는 파일 경로

        Returns:
            bool: 사진이면 True, 문서면 False
        """
        metadata = self.extract_metadata(image_file)
        return metadata['has_exif']

    def format_metadata_for_display(self, metadata):
        """
        메타데이터를 표시용으로 포맷팅

        Args:
            metadata: 메타데이터 딕셔너리

        Returns:
            dict: 포맷팅된 메타데이터
        """
        formatted = {}

        if metadata['camera_make']:
            formatted['카메라 제조사'] = metadata['camera_make']

        if metadata['camera_model']:
            formatted['카메라 모델'] = metadata['camera_model']

        if metadata['datetime']:
            if isinstance(metadata['datetime'], datetime):
                formatted['촬영 일시'] = metadata['datetime'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted['촬영 일시'] = str(metadata['datetime'])

        if metadata['width'] and metadata['height']:
            formatted['해상도'] = f"{metadata['width']} x {metadata['height']}"

        if metadata['has_gps']:
            gps = metadata['gps_info']
            if 'latitude' in gps and 'longitude' in gps:
                formatted['GPS 위도'] = f"{gps['latitude']:.6f}"
                formatted['GPS 경도'] = f"{gps['longitude']:.6f}"
            if 'altitude' in gps:
                formatted['GPS 고도'] = f"{gps['altitude']:.2f}m"

        formatted['사진 여부'] = '사진' if metadata['is_photo'] else '문서'

        return formatted


def extract_metadata_simple(image_file):
    """
    간단한 메타데이터 추출 (기존 방식 호환)

    Args:
        image_file: PIL Image 객체 또는 파일 경로

    Returns:
        dict: 메타데이터 딕셔너리
    """
    extractor = PhotoMetadataExtractor()
    return extractor.extract_metadata(image_file)
