from konlpy.tag import Okt, Mecab, Komoran
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re


class KoreanKeywordExtractor:
    """
    한국어 형태소 분석 기반 키워드 추출기
    """

    def __init__(self, analyzer='okt'):
        """
        초기화

        Args:
            analyzer: 'okt', 'mecab', 'komoran' 중 선택
        """
        self.analyzer_name = analyzer

        try:
            if analyzer == 'okt':
                self.analyzer = Okt()
            elif analyzer == 'mecab':
                self.analyzer = Mecab()
            elif analyzer == 'komoran':
                self.analyzer = Komoran()
            else:
                self.analyzer = Okt()
        except Exception as e:
            print(f"Warning: {analyzer} 초기화 실패, Okt로 대체합니다. Error: {e}")
            self.analyzer = Okt()
            self.analyzer_name = 'okt'

        # 한국어 불용어 리스트
        self.stopwords = set([
            '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다',
            '을', '를', '입니다', '합니다', '있습니다', '없습니다', '그', '저', '것', '수', '등', '년', '월', '일',
            '그리고', '또한', '및', '그러나', '하지만', '따라서', '때문에', '위해', '통해', '대한', '관한',
            '및', '등등', '즉', '예를', '들어', '또는', '혹은', '만약', '만', '더', '덜', '매우', '너무',
            '정도', '쯤', '것', '수', '등', '곳', '때', '분', '개', '명', '원', '점', '번', '차', '회'
        ])

    def extract_nouns(self, text):
        """
        텍스트에서 명사만 추출

        Args:
            text: 분석할 텍스트

        Returns:
            list: 추출된 명사 리스트
        """
        if self.analyzer_name == 'okt':
            return self.analyzer.nouns(text)
        elif self.analyzer_name == 'mecab':
            words = self.analyzer.nouns(text)
            return words
        elif self.analyzer_name == 'komoran':
            return self.analyzer.nouns(text)
        else:
            return self.analyzer.nouns(text)

    def extract_pos(self, text):
        """
        형태소 분석 및 품사 태깅

        Args:
            text: 분석할 텍스트

        Returns:
            list: (형태소, 품사) 튜플 리스트
        """
        return self.analyzer.pos(text)

    def extract_nouns_from_pos(self, pos_tagged):
        """
        품사 태깅된 결과에서 명사만 추출

        Args:
            pos_tagged: (형태소, 품사) 튜플 리스트

        Returns:
            list: 명사 리스트
        """
        nouns = []
        for word, pos in pos_tagged:
            # 일반명사(Noun), 고유명사(Proper Noun) 추출
            if pos in ['Noun', 'NNG', 'NNP']:
                nouns.append(word)
        return nouns

    def create_compound_nouns(self, pos_tagged, min_length=2):
        """
        연속된 명사를 복합 명사로 생성

        Args:
            pos_tagged: (형태소, 품사) 튜플 리스트
            min_length: 복합 명사 최소 길이

        Returns:
            list: 복합 명사 리스트
        """
        compound_nouns = []
        temp_noun = []

        for word, pos in pos_tagged:
            if pos in ['Noun', 'NNG', 'NNP']:
                temp_noun.append(word)
            else:
                if len(temp_noun) >= 2:
                    compound = ''.join(temp_noun)
                    if len(compound) >= min_length:
                        compound_nouns.append(compound)
                temp_noun = []

        # 마지막 명사 처리
        if len(temp_noun) >= 2:
            compound = ''.join(temp_noun)
            if len(compound) >= min_length:
                compound_nouns.append(compound)

        return compound_nouns

    def filter_nouns(self, nouns, min_length=2, max_length=15):
        """
        명사 필터링 (불용어 제거, 길이 제한)

        Args:
            nouns: 명사 리스트
            min_length: 최소 길이
            max_length: 최대 길이

        Returns:
            list: 필터링된 명사 리스트
        """
        filtered = []
        for noun in nouns:
            # 불용어 제거
            if noun in self.stopwords:
                continue

            # 길이 제한
            if len(noun) < min_length or len(noun) > max_length:
                continue

            # 숫자만 있는 경우 제거
            if noun.isdigit():
                continue

            # 특수문자만 있는 경우 제거
            if re.match(r'^[^\w\s]+$', noun):
                continue

            filtered.append(noun)

        return filtered

    def calculate_tfidf_scores(self, texts, top_k=15):
        """
        TF-IDF 점수 계산

        Args:
            texts: 텍스트 리스트 (문서 컬렉션)
            top_k: 상위 k개 키워드

        Returns:
            dict: {키워드: TF-IDF 점수}
        """
        # 텍스트가 하나만 있는 경우, 빈도 기반으로 처리
        if len(texts) == 1:
            nouns = self.extract_nouns(texts[0])
            filtered = self.filter_nouns(nouns)
            counter = Counter(filtered)
            top_keywords = dict(counter.most_common(top_k))
            return top_keywords

        # TF-IDF 벡터라이저
        vectorizer = TfidfVectorizer(
            tokenizer=lambda x: self.filter_nouns(self.extract_nouns(x)),
            max_features=top_k * 2
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()

            # 평균 TF-IDF 점수 계산
            scores = {}
            for idx, word in enumerate(feature_names):
                scores[word] = tfidf_matrix[:, idx].mean()

            # 상위 k개 선택
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_keywords = dict(sorted_scores[:top_k])

            return top_keywords
        except ValueError:
            # TF-IDF 계산 실패 시 빈도 기반으로 폴백
            all_nouns = []
            for text in texts:
                nouns = self.extract_nouns(text)
                all_nouns.extend(self.filter_nouns(nouns))

            counter = Counter(all_nouns)
            top_keywords = dict(counter.most_common(top_k))
            return top_keywords

    def extract_keywords_with_morpheme_analysis(self, text, top_k=15):
        """
        형태소 분석 기반 키워드 추출 (통합 함수)

        Args:
            text: 분석할 텍스트
            top_k: 추출할 키워드 개수

        Returns:
            list: 키워드 리스트 (점수 순)
        """
        # 1. 형태소 분석 및 품사 태깅
        pos_tagged = self.extract_pos(text)

        # 2. 명사 추출
        nouns = self.extract_nouns_from_pos(pos_tagged)

        # 3. 복합 명사 생성
        compound_nouns = self.create_compound_nouns(pos_tagged)

        # 4. 모든 명사 결합
        all_nouns = nouns + compound_nouns

        # 5. 필터링
        filtered_nouns = self.filter_nouns(all_nouns)

        # 6. 빈도 계산
        counter = Counter(filtered_nouns)

        # 7. 상위 키워드 선택
        top_keywords = [word for word, _ in counter.most_common(top_k)]

        return top_keywords

    def extract_keywords_with_tfidf(self, text, corpus=None, top_k=15):
        """
        TF-IDF 기반 키워드 추출

        Args:
            text: 분석할 텍스트
            corpus: 참조 문서 컬렉션 (선택사항)
            top_k: 추출할 키워드 개수

        Returns:
            list: 키워드 리스트 (TF-IDF 점수 순)
        """
        if corpus is None:
            # 문서 컬렉션이 없으면 현재 텍스트만 사용
            corpus = [text]
        else:
            # 현재 텍스트를 문서 컬렉션에 추가
            corpus = list(corpus) + [text]

        # TF-IDF 점수 계산
        scores = self.calculate_tfidf_scores(corpus, top_k)

        # 점수 순으로 정렬
        sorted_keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, score in sorted_keywords[:top_k]]

        return top_keywords

    def compare_methods(self, text, top_k=15):
        """
        여러 키워드 추출 방법 비교

        Args:
            text: 분석할 텍스트
            top_k: 추출할 키워드 개수

        Returns:
            dict: 각 방법별 키워드 리스트
        """
        results = {}

        # 1. 형태소 분석 기반
        results['morpheme'] = self.extract_keywords_with_morpheme_analysis(text, top_k)

        # 2. 단순 명사 추출 + 빈도
        nouns = self.extract_nouns(text)
        filtered = self.filter_nouns(nouns)
        counter = Counter(filtered)
        results['frequency'] = [word for word, _ in counter.most_common(top_k)]

        # 3. TF-IDF (단일 문서)
        results['tfidf'] = self.extract_keywords_with_tfidf(text, None, top_k)

        return results


def extract_keywords_simple(text, top_k=15):
    """
    간단한 키워드 추출 (기존 방식 호환)

    Args:
        text: 분석할 텍스트
        top_k: 추출할 키워드 개수

    Returns:
        list: 키워드 리스트
    """
    extractor = KoreanKeywordExtractor()
    return extractor.extract_keywords_with_morpheme_analysis(text, top_k)
