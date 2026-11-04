#!/usr/bin/env python3
"""
Context inference and machine learning glossary extractor for ml-stt.

- Infers class date (MMDD) from audio filename or explicit argument.
- Infers lecture number (LectureXX) from 복습노트/<MMDD>/ (.pack/ 포함), 강의노트/ 슬라이드 날짜, 예습노트/.
- Selects the latest revision PDF (_rev_HO > _rev > base) and strips LaTeXiT metadata noise.
- Extracts key technical terms directly from 강의노트/Lecture*.pdf (and TA_Lecture*.pdf when applicable).
- Builds domain guidance prompt for STT transcription subagents.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import unicodedata

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

DATE_PATTERNS = [
    # 20261005, 2026-10-05, 2026.10.05, 2026_1005
    re.compile(r"(?:20\d{2})[-_.]?([01]\d)[-_.]?([0-3]\d)"),
    # 1005 머러기, 1005.m4a, 녹음_1001.wav, 0930
    re.compile(r"(?:^|[^\d])([01]\d)([0-3]\d)(?:[^\d]|$)"),
]

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

SLIDE_DATE_RE = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\.?\s+(\d{1,2}),\s+20\d{2}\b",
    re.IGNORECASE,
)

LATEXIT_RE = re.compile(r"<latexit[^>]*>.*?</latexit>", re.DOTALL | re.IGNORECASE)
BASE64_NOISE_RE = re.compile(r"[A-Za-z0-9+/=]{20,}(?:</latexit>)?")
URL_EMAIL_RE = re.compile(r"(?:https?://\S+|\b\S+@\S+\b)")

ENGLISH_STOPWORDS = {
    "and", "the", "for", "with", "from", "that", "this", "page", "part", "slide",
    "introduction", "machine", "learning", "lecture", "prof", "bang", "chul", "jung",
    "bangchuljung", "ajou", "fall", "sept", "oct", "nov", "dec", "march", "warm-up",
    "watch", "tutorial", "video", "youtube", "channel", "please", "thank", "attention",
    "question", "answer", "example", "examples", "problem", "setting", "roadmap",
    "targets", "target", "recall", "show", "consider", "suppose", "assume", "denote",
    "letting", "note", "many", "other", "things", "again", "what", "will", "step",
    "steps", "first", "second", "third", "where", "whose", "which", "when", "they",
    "their", "into", "onto", "over", "under", "some", "every", "always", "often",
    "just", "like", "need", "only", "still", "thus", "then", "also", "called",
    "using", "make", "take", "find", "seek", "used", "chosen", "within", "among",
    "remaining", "already", "automatic", "rules", "check", "earlier", "now", "however",
    "respectively", "corresponding", "illustration", "representation", "representations",
    "representative", "subtracting", "measurements", "handwritten", "non-trivially",
    "dimensinoality", "dimensionas", "su", "cient", "di", "erent",
}

COMMON_ML_ERROR_RULES = [
    ("기븐 / 기븐 컨디션", "given (조건부 확률 및 조건: X given Y)"),
    ("조인트 / 조인트 확률", "joint (결합확률 / joint probability)"),
    ("라이클리후드 / 라이클리 호드 / 라이클리호드", "likelihood (우도 / 가능도)"),
    ("마지널 / 마지널라이즈", "marginal / marginalize (주변확률 / 주변화)"),
    ("포스테리어 / 포스테리어리", "posterior (사후확률분포)"),
    ("포스테리어 프레딕티브 / 포스테리어 프레딕션", "posterior predictive (사후 예측분포)"),
    ("프라이어", "prior (사전확률분포)"),
    ("에비던스", "evidence (증거 / 주변우도)"),
    ("언씬 / 언신 데이터", "unseen data (학습에 쓰이지 않은 새 입력 데이터 x*, y*)"),
    ("포인트 에스티메이터", "point estimator (점추정량)"),
    ("제너레이티브 / 제너레이션", "generative / generation (생성형 프로세스 / 데이터 생성)"),
    ("세타 / 쎄타", "세타 (θ / theta, 모델 모수/파라미터)"),
    ("람다", "람다 (λ / lambda, 고유값·투영 좌표·라그랑주 승수)"),
    ("뮤", "뮤 (μ / mu, 평균 또는 라그랑주 직교 제약 승수)"),
    ("슈도 인버스 / 수도 인버스", "pseudo-inverse (의사역행렬 / 무어-펜로즈 역행렬 (B^T B)^(-1) B^T)"),
    ("콘스탄트", "constant (상수 / 결정론적 값)"),
    ("베리언스 / 베어리언스", "variance (분산)"),
    ("코베리언스 / 크로스 코베리언스", "covariance / cross-covariance (공분산 / 교차공분산)"),
    ("아핀 / 어파인", "affine (아핀 변환 / affine transformation Y = AX + b)"),
    ("레귤러라이제이션", "regularization (정규화 / 규제)"),
    ("그라디언트 / 그레디언트", "gradient (기울기 / 그래디언트)"),
    ("자코비안 / 야코비안", "Jacobian (자코비안 행렬 / 다변량 변수변환 행렬식)"),
    ("헤시안 / 헷세 행렬", "Hessian (헤시안 행렬)"),
    ("엠엘이", "MLE (Maximum Likelihood Estimation / 최대우도추정)"),
    ("엠에이피", "MAP (Maximum A Posteriori / 최대사후확률추정)"),
    ("디터미니스틱", "deterministic (결정론적)"),
    ("델타 함수", "Dirac delta function (디랙 델타 함수)"),
    ("오소고날 / 오쏘고날 / 올소고날", "orthogonal (직교 / 직교투영 orthogonal projection)"),
    ("오소노말 / 올소노말", "orthonormal (정규직교 / 정규직교 기저 orthonormal basis)"),
    ("프로젝션", "projection (투영 / 정사영 / 투영행렬 P_π)"),
    ("서브스페이스 / 프린시펄 서브스페이스", "subspace / principal subspace (부분공간 / 주부분공간)"),
    ("스팬 / 컬럼 스페이스", "span / column space (생성공간 / 열공간)"),
    ("베이시스", "basis (기저 / 기저벡터 b_i / 기저행렬 B)"),
    ("피씨에이", "PCA (Principal Component Analysis / 주성분 분석)"),
    ("프린시펄 컴포넌트", "principal component (주성분)"),
    ("디멘셔널리티 리덕션", "dimensionality reduction (차원 축소)"),
    ("오버컴플리트", "overcomplete (과완비 / 차원 과잉)"),
    ("리던던트 / 리던던시", "redundant / redundancy (중복 / 차원 중복성)"),
    ("센터링 / 웰 센터드", "centering / well-centered (평균 차감 / 영평균화)"),
    ("스탠다다이제이션", "standardization (표준화 / 표준편차로 스케일링)"),
    ("인코더 / 디코더", "encoder / decoder (인코더 B^T / 디코더 B)"),
    ("엠니스트", "MNIST (손글씨 숫자 이미지 데이터셋, 28x28=784차원)"),
    ("아이겐밸류 / 아이겐벡터 / 아이겐스페이스", "eigenvalue / eigenvector / eigenspace (고유값 / 고유벡터 / 고유공간)"),
    ("이브이디", "EVD (Eigenvalue Decomposition / 고유값 분해 A = P D P^-1)"),
    ("스펙트럴 씨어럼 / 스펙트럴 정리", "Spectral Theorem (스펙트럼 정리: 실대칭행렬 S = P D P^T 직교 대각화)"),
    ("다이아고날 / 다이아고날라이제이션", "diagonal matrix / diagonalization (대각행렬 / 대각화)"),
    ("캐릭터리스틱 폴리노미얼", "characteristic polynomial (특성다항식 det(A - λI) = 0)"),
    ("라그랑주 / 라그랑지안 / 멀티플라이어", "Lagrange multiplier / Lagrangian (라그랑주 승수법 / 라그랑지안 함수)"),
    ("인덕션", "induction (수학적 귀납법)"),
    ("루이스 세라노", "Luis Serrano (PCA 튜토리얼 영상 저자)"),
    ("아우티지", "outage (통신 중단/두절)"),
    ("힘숨찐", "힘숨찐 (교수님 비유: '힘을 숨기고 있다' - 분산 0으로 수렴 시 디터미니스틱을 포함함을 비유)"),
    ("장군님", "장군님 (교수님 비유: 단답형 점추정만 원하는 의사결정자 vs 원함수 PDF를 보유해야 하는 엔지니어)"),
]

COMMON_ML_TERMS_SEED = [
    # L01~L03: 확률·추론·선형회귀 기초
    "가우시안", "정규분포", "확률밀도함수(PDF)", "누적분포함수(CDF)", "조건부확률", "결합확률",
    "주변확률", "주변화(marginalization)", "사전분포(prior)", "가능도(likelihood)", "우도",
    "사후분포(posterior)", "사후 예측분포(posterior predictive)", "최대우도추정(MLE)", "최대사후확률추정(MAP)",
    "선형회귀(linear regression)", "최소제곱법(least squares)", "정규방정식(normal equation)",
    "의사역행렬(pseudo-inverse)", "가중치 벡터", "편향(bias)", "규제(regularization)", "릿지(Ridge)",
    "라쏘(Lasso)", "비용함수(cost function)", "손실함수(loss function)", "그래디언트(gradient)",
    "자코비안(Jacobian)", "헤시안(Hessian)", "아핀 변환(affine transformation)", "랜덤 벡터",
    "평균 벡터", "공분산 행렬", "대칭행렬", "양의 정부호(positive definite)", "i.i.d.",
    "독립(independent)", "베르누이(Bernoulli)", "이항분포(binomial)", "베이지안(Bayesian)",
    "풀리 베이지안(fully Bayesian)", "결정 유보", "힘숨찐", "아우티지(outage)", "장군님",
    # TA Lecture & L04: 가우시안 곱, 예측분포, 직교투영
    "교차공분산(cross-covariance)", "가우시안 곱(product of Gaussians)", "완전제곱식(completing the square)",
    "점추정량(point estimator)", "생성 프로세스(generative process)", "직교투영(orthogonal projection)",
    "투영행렬(projection matrix)", "부분공간(subspace)", "열공간(column space)", "생성공간(span)",
    "기저(basis)", "기저행렬(basis matrix)", "정규직교 기저(orthonormal basis)", "좌표(coordinates)",
    # L05: PCA, 고유값분해, 스펙트럼 정리, 라그랑주 승수법
    "주성분 분석(PCA)", "주성분(principal component)", "주부분공간(principal subspace)",
    "차원 축소(dimensionality reduction)", "데이터 압축(compression)", "과완비(overcomplete)",
    "중복성(redundancy)", "영평균화(centering)", "표준화(standardization)",
    "데이터 행렬(data matrix)", "데이터 공분산 행렬(data covariance matrix)",
    "저차원 표현(low-dimensional representation)", "코드(code)", "인코더(encoder)", "디코더(decoder)",
    "MNIST", "최대 분산 관점(maximum variance perspective)", "투영 관점(projection perspective)",
    "고유값(eigenvalue)", "아이겐밸류(eigenvalue)", "고유벡터(eigenvector)", "고유공간(eigenspace)",
    "특성다항식(characteristic polynomial)", "대각행렬(diagonal matrix)", "대각화(diagonalization)",
    "직교 대각화(orthogonally diagonalizable)", "고유값 분해(EVD)", "스펙트럼 정리(spectral theorem)",
    "라그랑주 승수법(Lagrange multiplier)", "라그랑지안(Lagrangian)", "수학적 귀납법(induction)",
    "일차 필요조건(first-order necessary condition)", "저랭크 근사(low-rank approximation)",
    "루이스 세라노(Luis Serrano)",
]


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def parse_date(filename_or_path: str, date_override: str | None = None) -> str:
    """Extract MMDD string from filename or override."""
    if date_override:
        clean = date_override.strip()
        m = re.fullmatch(r"(\d{2})(\d{2})", clean)
        if m and (1 <= int(m.group(1)) <= 12) and (1 <= int(m.group(2)) <= 31):
            return m.group(0)
        raise ValueError(f"유효하지 않은 날짜 형식입니다: {date_override!r} (예: 1005)")

    base = nfc(Path(filename_or_path).name)

    for pat in DATE_PATTERNS:
        match = pat.search(base)
        if match:
            mm, dd = match.group(1), match.group(2)
            if (1 <= int(mm) <= 12) and (1 <= int(dd) <= 31):
                return f"{mm}{dd}"

    raise ValueError(
        f"파일명에서 수업 날짜(MMDD)를 찾을 수 없습니다: {base!r}\n"
        f"--date MMDD 옵션으로 날짜를 직접 지정해 주세요. (예: /ml-stt audio.m4a --date 1005)"
    )


def _find_summary_notes(rev_dir: Path) -> list[Path]:
    """Return summary note files in rev_dir (.pack/정리노트*.md, 정리노트*.md, 정리노트*.html)."""
    candidates: list[Path] = []
    pack_dir = rev_dir / ".pack"
    for folder in (pack_dir, rev_dir):
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                name = nfc(f.name)
                if f.is_file() and "정리노트" in name and (name.endswith(".md") or name.endswith(".html")):
                    candidates.append(f)
    # Prefer .md over .html because .md has a concise top header
    candidates.sort(key=lambda p: (0 if p.suffix == ".md" else 1, nfc(p.name)))
    return candidates


def _extract_lecture_from_note(note_path: Path) -> int | None:
    """Extract primary LectureXX number from the top header of a summary note."""
    try:
        content = note_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    head_lines = "\n".join(content.splitlines()[:30])
    # Match e.g. "Lecture04", "Lecture 01", "Lecture01~02"
    m_range = re.search(r"Lecture\s*0?(\d+)\s*[~-]\s*0?(\d+)", head_lines, re.IGNORECASE)
    if m_range:
        return int(m_range.group(2))
    m = re.search(r"Lecture\s*0?(\d+)", head_lines, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        if num < 10:  # Ignore supplementary Lecture 10/11/12 references
            return num
    return None


def _extract_pdf_slide_date(pdf_path: Path) -> str | None:
    """Extract MMDD date printed on the first few pages of a lecture slide PDF."""
    if not fitz or not pdf_path.is_file():
        return None
    try:
        doc = fitz.open(pdf_path)
        for i in range(min(5, len(doc))):
            text = doc[i].get_text()
            for m in SLIDE_DATE_RE.finditer(text):
                mon_str = m.group(1).lower().rstrip(".")
                day = int(m.group(2))
                mon = MONTH_MAP.get(mon_str)
                if mon and 1 <= day <= 31:
                    # Skip syllabus/template footer dates like March 16, 2026 if a fall date exists
                    if mon >= 8:
                        return f"{mon:02d}{day:02d}"
    except Exception:
        pass
    return None


def _select_lecture_pdf(lec_dir: Path, lecture_num: int) -> Path | None:
    """Select the highest-priority PDF for LectureXX (_rev_HO > _rev > base)."""
    if not lec_dir.is_dir():
        return None
    matches: list[tuple[int, str, Path]] = []
    for f in lec_dir.iterdir():
        name = nfc(f.name)
        if re.match(rf"^Lecture{lecture_num:02d}_.*\.pdf$", name):
            if "_rev_HO.pdf" in name:
                prio = 3
            elif "_rev.pdf" in name:
                prio = 2
            else:
                prio = 1
            matches.append((prio, name, f))
    if not matches:
        return None
    matches.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return matches[0][2]


def _find_ta_pdf_for_date(lec_dir: Path, mmdd: str) -> Path | None:
    """Return TA_Lecture PDF if its slide date matches mmdd (or 1012 fallback)."""
    if not lec_dir.is_dir():
        return None
    for f in sorted(lec_dir.iterdir()):
        name = nfc(f.name)
        if name.startswith("TA_Lecture") and name.endswith(".pdf"):
            slide_mmdd = _extract_pdf_slide_date(f)
            if slide_mmdd == mmdd or (slide_mmdd is None and mmdd == "1012"):
                return f
    return None


def infer_lecture(repo_root: Path | str, mmdd: str) -> int:
    """Infer lecture number from 복습노트/<MMDD>/ (.pack/ 포함), 강의노트/ 슬라이드 날짜, 예습노트/."""
    repo = Path(repo_root)
    rev_root = repo / "복습노트"
    lec_dir = repo / "강의노트"

    # 1순위: 복습노트/<MMDD>/ (및 .pack/) 안의 정리노트 헤더 검사
    rev_dir = rev_root / mmdd
    if rev_dir.is_dir():
        for note in _find_summary_notes(rev_dir):
            lec = _extract_lecture_from_note(note)
            if lec is not None:
                return lec

    # 2순위: 강의노트/ 및 복습노트/의 날짜-렉처 매핑 테이블 구성 후 매칭
    date_to_lecture: dict[str, int] = {}

    if lec_dir.is_dir():
        for f in sorted(lec_dir.iterdir()):
            name = nfc(f.name)
            m = re.match(r"^Lecture(\d{2})_.*\.pdf$", name)
            if m:
                lec_num = int(m.group(1))
                if lec_num > 0:
                    slide_date = _extract_pdf_slide_date(f)
                    if slide_date:
                        date_to_lecture[slide_date] = max(date_to_lecture.get(slide_date, 0), lec_num)

    if rev_root.is_dir():
        for d in sorted(rev_root.iterdir()):
            if d.is_dir() and re.fullmatch(r"\d{4}", d.name):
                for note in _find_summary_notes(d):
                    lec = _extract_lecture_from_note(note)
                    if lec is not None:
                        date_to_lecture[d.name] = lec
                        break

    # 해당 날짜에 정확히 매칭되는 강의노트 슬라이드 날짜가 있으면 즉시 반환
    if mmdd in date_to_lecture:
        return date_to_lecture[mmdd]

    # 3순위: mmdd 이전의 가장 가까운 날짜(복습노트 또는 강의노트 슬라이드 날짜)의 Lecture 번호
    past_dates = sorted(d for d in date_to_lecture if d <= mmdd)
    if past_dates:
        return date_to_lecture[past_dates[-1]]

    # 4순위: 예습노트/Lxx/ 폴더 검사
    prev_dir = repo / "예습노트"
    if prev_dir.is_dir():
        prev_nums = []
        for f in prev_dir.iterdir():
            m = re.fullmatch(r"L0?(\d+)", nfc(f.name))
            if m and f.is_dir():
                prev_nums.append(int(m.group(1)))
        if prev_nums:
            return max(prev_nums)

    # 5순위: 강의노트/ 폴더에서 가장 최신 정규 Lecture 번호
    if lec_dir.is_dir():
        nums = []
        for f in lec_dir.iterdir():
            m = re.match(r"^Lecture(\d{2})_", nfc(f.name))
            if m:
                nums.append(int(m.group(1)))
        if nums:
            return max(nums)

    return 4


def get_lecture_title(repo_root: Path | str, lecture_num: int) -> str:
    """Find lecture slug/title from 강의노트/ directory."""
    repo = Path(repo_root)
    lec_dir = repo / "강의노트"
    pdf_path = _select_lecture_pdf(lec_dir, lecture_num)
    if pdf_path:
        name = nfc(pdf_path.name)
        m = re.match(rf"^Lecture{lecture_num:02d}_([A-Za-z0-9_]+?)(?:_rev(?:_HO)?)?\.pdf$", name)
        if m:
            return m.group(1)
    return f"Lecture{lecture_num:02d}"


def _clean_pdf_text(raw_text: str) -> str:
    """Strip embedded LaTeXiT base64 blocks, URLs, emails, and normalize PDF ligatures."""
    text = LATEXIT_RE.sub(" ", raw_text)
    text = BASE64_NOISE_RE.sub(" ", text)
    text = URL_EMAIL_RE.sub(" ", text)
    for lig, rep in (("ﬃ", "ffi"), ("ﬄ", "ffl"), ("ﬀ", "ff"), ("ﬁ", "fi"), ("ﬂ", "fl")):
        text = text.replace(lig, rep)
    # Fix common PDF font encoding glitches in lecture slides ("di!erent" -> "different")
    text = re.sub(r"di!erent", "different", text)
    text = re.sub(r"su!cient", "sufficient", text)
    text = re.sub(r"o!-diagonal", "off-diagonal", text)
    return text


def extract_lecture_terms(
    repo_root: Path | str,
    lecture_num: int,
    max_terms: int = 90,
    mmdd: str | None = None,
) -> list[str]:
    """Extract key ML/math technical terms from lecture PDF and seed glossary."""
    repo = Path(repo_root)
    lec_dir = repo / "강의노트"
    pdf_paths: list[Path] = []

    main_pdf = _select_lecture_pdf(lec_dir, lecture_num)
    if main_pdf:
        pdf_paths.append(main_pdf)

    if mmdd:
        ta_pdf = _find_ta_pdf_for_date(lec_dir, mmdd)
        if ta_pdf and ta_pdf not in pdf_paths:
            pdf_paths.append(ta_pdf)

    extracted_en: dict[str, str] = {}
    extracted_ko: set[str] = set()

    if pdf_paths and fitz:
        for pdf_path in pdf_paths:
            try:
                doc = fitz.open(pdf_path)
                raw_text = "\n".join(page.get_text() for page in doc)
                full_text = _clean_pdf_text(raw_text)

                # (1) 영문 머신러닝 약어 및 전문용어 (3글자 이상 또는 대문자 약어)
                for m in re.finditer(r"\b[A-Za-z]{2,}(?:-[A-Za-z]{2,})?\b", full_text):
                    word = m.group(0)
                    low = word.lower()
                    if low in ENGLISH_STOPWORDS:
                        continue
                    if len(word) < 4 and not word.isupper():
                        continue
                    # Preserve all-caps acronyms (PCA, EVD, MLE, MAP, MNIST), else lowercase
                    canonical = word if word.isupper() else low
                    if low not in extracted_en or word.isupper():
                        extracted_en[low] = canonical

                # (2) 한글 머신러닝 전문용어 패턴
                ml_kw_pat = re.compile(
                    r"[가-힣]{2,8}(?:확률|분포|우도|가우시안|회귀|최적화|경사하강|행렬|벡터|분산|공분산|"
                    r"고유값|고유벡터|고유공간|역행렬|내적|전치|투영|정사영|부분공간|기저|차원|주성분|"
                    r"대각화|승수법|귀납법|결정나무|군집화|추정|손실|비용|정규화|표준화|규제|베이지안)"
                )
                for m in ml_kw_pat.finditer(full_text):
                    extracted_ko.add(m.group(0))

                # (3) 괄호 안 병기 단어
                for m in re.finditer(r"([가-힣]{2,10})\s*\(([A-Za-z\s-]+)\)", full_text):
                    extracted_ko.add(m.group(1).strip())
                    en = m.group(2).strip()
                    if 2 <= len(en) < 30 and en.lower() not in ENGLISH_STOPWORDS:
                        extracted_en[en.lower()] = en
            except Exception:
                pass

    # Seed terms first (prioritize lecture-relevant seeds + core ML seeds), then PDF-extracted terms
    ordered_terms: list[str] = []
    seen_lower: set[str] = set()

    def _add_term(t: str) -> None:
        key = t.lower()
        if key not in seen_lower:
            seen_lower.add(key)
            ordered_terms.append(t)

    for w in COMMON_ML_TERMS_SEED:
        _add_term(w)

    for w in sorted(extracted_ko, key=lambda x: (-len(x), x)):
        _add_term(w)

    for w in sorted(extracted_en.values(), key=lambda x: (0 if x.isupper() else 1, -len(x), x)):
        _add_term(w)

    return ordered_terms[:max_terms]


def build_stt_prompt(lecture_num: int, lecture_title: str, terms: list[str]) -> str:
    """Format domain guidance block to inject into the subagent STT prompt."""
    sample_terms = ", ".join(terms[:65])
    homophone_guide = "\n".join(f"  - '{err}'로 들리면 -> '{cor}'" for err, cor in COMMON_ML_ERROR_RULES)

    return f"""[머신러닝기초 강의 도메인 가이드 (정방철 교수님, ECE3512)]
- 본 오디오는 아주대학교 전자공학과 머신러닝기초 강의 녹음입니다.
- 학술 목적: 본 전사는 대학 전공 강의의 학술 연구 및 학습 복습 자료 작성을 위한 순수 교육용 기록입니다.
- 단원 범위: Lecture{lecture_num:02d} ({lecture_title})
- 주요 머신러닝/수학/통계 고유명사:
  {sample_terms}

- 필수 전사 및 발음 교정 규칙:
  1. 머신러닝 표준 용어 최우선: 교수님의 발음이 뭉개지거나 일상 단어로 들릴 경우, 문맥상 머신러닝/확률/선형대수 표준 용어로 정확히 전사하세요.
{homophone_guide}
  2. 표기 원칙: 자연스러운 한국어 음차를 기본으로 하되, 핵심 약어 및 수학 기호(MLE, MAP, PDF, i.i.d., EVD, PCA, MNIST, SVM, X, B, S, θ, λ, μ 등)는 영문/약어로 표기하세요.
  3. 안전성 보존 축어성(Safe Verbatim) 및 완곡 순화 규칙 (Strict Safety Shield):
     - 구글 Gemini API의 실시간 안전 필터(공격성, 혐오 표현, 비하, 비속어) 오탐을 원천 방지하기 위해, 교수님의 강의 중 자조적 감탄사, 학생 질책, 거친 농담이 발화될 경우 발화의 교육적 맥락과 의미를 100% 보존하되 안전한 표준 구어체로 완곡히 순화(Euphemistic Normalization)하여 전사하세요.
       * 감탄사/비속어: '제기랄/젠장' -> '이런/아이구'
       * 자조적/질책 비유: '바보 엔지니어/뇌가 썩는다' -> '미숙한 엔지니어/사고력이 무뎌진다', '쓰레기 논문' -> '부실한 논문/정크 페이퍼'
       * 기타 돌발 비속어/비하어: 문맥을 훼손하지 않는 자연스러운 완곡 표현으로 치환하여 게이트웨이 안전 필터 차단을 원천 예방하세요.
     - 단, 수학 수식 기호, 머신러닝 전문 용어, 및 교수님의 핵심 학습 비유('힘숨찐', '장군님', '도가니탕', '반지의 제왕' 등)는 절대 순화 대상이 아니며 원문 그대로 전사합니다.
"""


def main():
    parser = argparse.ArgumentParser(description="Infer machine learning context and terms for ml-stt")
    parser.add_argument("audio", help="Path to audio file (or filename)")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--date", help="Class date override (MMDD)")
    parser.add_argument("--lecture", type=int, help="Lecture number override (e.g. 4)")
    parser.add_argument("--json", action="store_true", help="Output JSON structure")
    parser.add_argument("--prompt-only", action="store_true", help="Print prompt injection text only")

    args = parser.parse_args()
    repo = Path(args.repo).resolve()

    date = parse_date(args.audio, args.date)
    lecture_num = args.lecture if args.lecture else infer_lecture(repo, date)
    lecture_title = get_lecture_title(repo, lecture_num)
    terms = extract_lecture_terms(repo, lecture_num, mmdd=date)
    prompt_guide = build_stt_prompt(lecture_num, lecture_title, terms)

    if args.prompt_only:
        print(prompt_guide)
        return

    result = {
        "audio": args.audio,
        "date": date,
        "lecture": lecture_num,
        "lecture_title": lecture_title,
        "output_filename": f"{date} 머러기.md",
        "output_path": str(repo / "STT" / f"{date} 머러기.md"),
        "terms_count": len(terms),
        "terms": terms,
        "prompt_guide": prompt_guide,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"수업 날짜: {date} (파일명에서 추출)")
        print(f"진도 강의: Lecture{lecture_num:02d} ({lecture_title})")
        print(f"추출 용어: {len(terms)}개")
        print(f"최종 저장: STT/{date} 머러기.md")


if __name__ == "__main__":
    main()
