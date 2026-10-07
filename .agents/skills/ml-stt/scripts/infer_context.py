#!/usr/bin/env python3
"""
Context inference and machine learning glossary extractor for ml-stt.

- Infers class date (MMDD) from audio filename or explicit argument.
- Infers lecture number (LectureXX) from 복습노트/<MMDD>/, 예습노트/, or 강의노트/.
- Extracts key technical terms directly from 강의노트/Lecture*.pdf and MML textbook.
- Builds domain guidance prompt for STT transcription subagents.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
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

COMMON_ML_ERROR_RULES = [
    ("기븐 / 기븐 컨디션", "given (조건부 확률 및 조건: X given Y)"),
    ("조인트 / 조인트 확률", "joint (결합확률 / joint probability)"),
    ("라이클리후드 / 라이클리 호드 / 라이클리호드", "likelihood (우도 / 가능도)"),
    ("마지널 / 마지널라이즈", "marginal / marginalize (주변확률 / 주변화)"),
    ("포스테리어 / 포스테리어리", "posterior (사후확률분포)"),
    ("프라이어", "prior (사전확률분포)"),
    ("에비던스", "evidence (증거 / 주변우도)"),
    ("세타 / 쎄타", "세타 (θ / theta, 모델 모수/파라미터)"),
    ("슈도 인버스 / 수도 인버스", "pseudo-inverse (의사역행렬 / 무어-펜로즈 역행렬)"),
    ("콘스탄트", "constant (상수 / 결정론적 값)"),
    ("베리언스 / 베어리언스", "variance (분산)"),
    ("코베리언스", "covariance (공분산)"),
    ("아핀 / 어파인", "affine (아핀 변환 / affine transformation)"),
    ("레귤러라이제이션", "regularization (정규화 / 규제)"),
    ("그라디언트 / 그레디언트", "gradient (기울기 / 그래디언트)"),
    ("자코비안 / 야코비안", "Jacobian (자코비안 행렬)"),
    ("헤시안 / 헷세 행렬", "Hessian (헤시안 행렬)"),
    ("엠엘이", "MLE (Maximum Likelihood Estimation / 최대우도추정)"),
    ("엠에이피", "MAP (Maximum A Posteriori / 최대사후확률추정)"),
    ("디터미니스틱", "deterministic (결정론적)"),
    ("델타 함수", "Dirac delta function (디랙 델타 함수)"),
    ("아우티지", "outage (통신 중단/두절)"),
    ("힘숨찐", "힘숨찐 (교수님 비유: '힘을 숨기고 있다' - 분산 0으로 수렴 시 디터미니스틱을 포함함을 비유)"),
]

COMMON_ML_TERMS_SEED = [
    "가우시안", "정규분포", "확률밀도함수(PDF)", "누적분포함수(CDF)", "조건부확률", "결합확률",
    "주변확률", "주변화(marginalization)", "사전분포(prior)", "가능도(likelihood)", "우도",
    "사후분포(posterior)", "사후 예측분포(posterior predictive)", "최대우도추정(MLE)", "최대사후확률추정(MAP)",
    "선형회귀(linear regression)", "최소제곱법(least squares)", "정규방정식(normal equation)",
    "의사역행렬(pseudo-inverse)", "가중치 벡터", "편향(bias)", "규제(regularization)", "릿지(Ridge)",
    "라쏘(Lasso)", "비용함수(cost function)", "손실함수(loss function)", "그래디언트(gradient)",
    "자코비안(Jacobian)", "헤시안(Hessian)", "아핀 변환(affine transformation)", "랜덤 벡터",
    "평균 벡터", "공분산 행렬", "대칭행렬", "양의 정부호(positive definite)", "아이겐밸류(eigenvalue)",
    "고유값", "고유벡터(eigenvector)", "i.i.d.", "독립(independent)", "베르누이(Bernoulli)",
    "이항분포(binomial)", "베이지안(Bayesian)", "풀리 베이지안(fully Bayesian)", "결정 유보",
    "힘숨찐", "아우티지(outage)", "로지스틱 회귀", "SVM", "결정 트리", "앙상블", "클러스터링", "PCA"
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


def infer_lecture(repo_root: Path | str, mmdd: str) -> int:
    """Infer lecture number from 복습노트/<MMDD>/, 예습노트/, or latest notes."""
    repo = Path(repo_root)

    # 1순위: 복습노트/<MMDD>/ 안의 정리노트 헤더 검사
    rev_dir = repo / "복습노트" / mmdd
    if rev_dir.is_dir():
        for f in rev_dir.iterdir():
            name = nfc(f.name)
            if name.endswith(".md") and "정리노트" in name:
                try:
                    content = f.read_text(encoding="utf-8")
                    m = re.search(r"Lecture\s*0?(\d+)", content)
                    if m:
                        return int(m.group(1))
                except Exception:
                    pass

    # 2순위: 예습노트/Lxx/ 폴더 검사
    prev_dir = repo / "예습노트"
    if prev_dir.is_dir():
        for f in prev_dir.iterdir():
            m = re.fullmatch(r"L0?(\d+)", nfc(f.name))
            if m and f.is_dir():
                # 예습노트가 특정 Lecture를 명시하고 있는 경우
                pass

    # 3순위: 복습노트/ 에서 mmdd 이전의 가장 최근 폴더 검사
    rev_root = repo / "복습노트"
    if rev_root.is_dir():
        folders = sorted([d.name for d in rev_root.iterdir() if d.is_dir() and re.fullmatch(r"\d{4}", d.name)])
        past_folders = [d for d in folders if d <= mmdd]
        target_folder = past_folders[-1] if past_folders else (folders[-1] if folders else None)

        if target_folder:
            f_dir = rev_root / target_folder
            for f in f_dir.iterdir():
                name = nfc(f.name)
                if name.endswith(".md") and "정리노트" in name:
                    try:
                        content = f.read_text(encoding="utf-8")
                        m = re.search(r"Lecture\s*0?(\d+)", content)
                        if m:
                            base_lec = int(m.group(1))
                            if target_folder == mmdd:
                                return base_lec
                            # 이전 수업 날짜라면 그 다음 혹은 같은 렉처
                            return base_lec
                    except Exception:
                        pass

    # 4순위: 강의노트/ 폴더에서 가장 최신 Lecture 번호
    lec_dir = repo / "강의노트"
    if lec_dir.is_dir():
        nums = []
        for f in lec_dir.iterdir():
            m = re.match(r"^Lecture(\d{2})_", nfc(f.name))
            if m:
                nums.append(int(m.group(1)))
        if nums:
            return max(nums)

    # 기본 fallback: 4 (학기 중반 4강)
    return 4


def get_lecture_title(repo_root: Path | str, lecture_num: int) -> str:
    """Find lecture slug/title from 강의노트/ directory."""
    repo = Path(repo_root)
    lec_dir = repo / "강의노트"
    if lec_dir.is_dir():
        for f in lec_dir.iterdir():
            name = nfc(f.name)
            m = re.match(rf"^Lecture{lecture_num:02d}_([A-Za-z0-9_]+?)(?:_rev)?\.pdf$", name)
            if m:
                return m.group(1)
    return f"Lecture{lecture_num:02d}"


def extract_lecture_terms(repo_root: Path | str, lecture_num: int, max_terms: int = 80) -> list[str]:
    """Extract key ML/math technical terms from lecture PDF and MML textbook."""
    repo = Path(repo_root)
    terms: set[str] = set()

    # 1. 강의노트 PDF 텍스트 추출
    lec_dir = repo / "강의노트"
    pdf_path = None
    if lec_dir.is_dir():
        for f in lec_dir.iterdir():
            if re.match(rf"^Lecture{lecture_num:02d}_.*\.pdf$", nfc(f.name)):
                pdf_path = f
                break

    if pdf_path and fitz:
        try:
            doc = fitz.open(pdf_path)
            full_text = "\n".join(page.get_text() for page in doc)

            # (1) 영문 머신러닝 약어 및 용어 (2글자 이상)
            for m in re.finditer(r"\b[A-Za-z]{2,}(?:-[A-Za-z0-9]+)?\b", full_text):
                word = m.group(0)
                if word.lower() not in {"and", "the", "for", "with", "from", "that", "this", "page", "part", "slide"}:
                    terms.add(word)

            # (2) 한글 머신러닝 전문용어 패턴
            ml_kw_pat = re.compile(
                r"[가-힣]{2,8}(?:확률|분포|우도|가우시안|회귀|최적화|경사하강|행렬|벡터|분산|공분산|고유값|고유벡터|역행렬|내적|전치|결정나무|군집화|추정|손실|비용|정규화|규제|베이지안)"
            )
            for m in ml_kw_pat.finditer(full_text):
                terms.add(m.group(0))

            # (3) 괄호 안 병기 단어
            for m in re.finditer(r"([가-힣]{2,10})\s*\(([A-Za-z\s]+)\)", full_text):
                terms.add(m.group(1).strip())
                en = m.group(2).strip()
                if len(en) < 30:
                    terms.add(en)
        except Exception:
            pass

    # 2. 핵심 필수 공통 어휘 보강
    for w in COMMON_ML_TERMS_SEED:
        terms.add(w)

    sorted_terms = sorted(terms, key=lambda x: (-len(x), x))
    return sorted_terms[:max_terms]


def build_stt_prompt(lecture_num: int, lecture_title: str, terms: list[str]) -> str:
    """Format domain guidance block to inject into the subagent STT prompt."""
    sample_terms = ", ".join(terms[:50])
    homophone_guide = "\n".join(f"  - '{err}'로 들리면 -> '{cor}'" for err, cor in COMMON_ML_ERROR_RULES)

    return f"""[머신러닝기초 강의 도메인 가이드 (정방철 교수님, ECE3512)]
- 본 오디오는 아주대학교 전자공학과 머신러닝기초 강의 녹음입니다.
- 단원 범위: Lecture{lecture_num:02d} ({lecture_title})
- 주요 머신러닝/수학/통계 고유명사:
  {sample_terms}

- 필수 전사 및 발음 교정 규칙:
  1. 머신러닝 표준 용어 최우선: 교수님의 발음이 뭉개지거나 일상 단어로 들릴 경우, 문맥상 머신러닝/확률/선형대수 표준 용어로 정확히 전사하세요.
{homophone_guide}
  2. 표기 원칙: 자연스러운 한국어 음차를 기본으로 하되, 핵심 약어 및 수학 기호(MLE, MAP, PDF, i.i.d., SVM, PCA, X, θ 등)는 영문/약어로 표기하세요.
  3. 철저한 축어성(Verbatim): 요약이나 어미 생략 없이 실제 발화된 내용을 있는 그대로 기록하세요. 교수님의 비유적 표현(예: '힘숨찐', '장군님')도 발화 그대로 기록합니다.
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
    terms = extract_lecture_terms(repo, lecture_num)
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
