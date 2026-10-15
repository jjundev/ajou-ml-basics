# Problem Explanation Synchronization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Update DS, ML and EC2 explanation skills and validate temporary stages without republishing existing explanations.

**Architecture:** Keep course adapters and local output layouts. Port the pinned bio template with DS code styling retained; use equivalent local helpers for review policy and validated choices. Review reuse is conservative and source-specific.

**Tech Stack:** Python 3.10+, standard library, pytest, Playwright Chromium for browser verification.

**Spec:** docs/superpowers/specs/2026-10-15-problem-explain-sync.md

## Global Constraints

- Do not publish, republish, commit or push.
- Use Python 3.10+ and standard-library production dependencies.
- Synthetic stage fixtures and temporary runs only.
- Preserve local .pack/.assets paths and reading-state identities.
- Copy no forecast adapter or biology chapter references.
- Missing evidence, stale hashes, content changes, unknown policy invalidate reused reviews.
- Always repeat source_visual/browser.
- Existing explanation files must retain baseline SHA-256.

## Review Focus

- An old approval with no policy revision cannot authorize a newly rebuilt stage: regression in review policy tests.
- A changed EC2 image/MD must invalidate reuse even when problems.txt is unchanged: composite-input rerender regression.
- ML homework remains outside review-only all selection and retains original/label normalization: source/render regressions.
- A stored closed TOC remains closed after reload at 1024px: Playwright acceptance.
- Missing/malformed answer models never produce guessed feedback: choice rendering regressions.

## File Structure

Each course owns scripts/*_source.py (input/paths), *_render.py (preserving HTML/MD assembly), *_cli.py (stage workflow), *_contract.py and *_publish.py (review gate), assets/note-template.html (UI), references/authoring.md and verification.md (agent contracts). New local *_review_policy.py handles policy-aware review carry; *_choices.py handles verified input models for DS/ML. Tests live alongside each skill. Plans, ledger, stage evidence and snapshots are separate from published coursework.

### Task 1: DS standalone synchronization

**Files:**
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/scripts/mpe_source.py`, `mpe_render.py`, `mpe_cli.py`, `mpe_contract.py`, `mpe_publish.py`
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/assets/note-template.html`, `assets/port-provenance.json`, `SKILL.md`, `references/authoring.md`, `references/verification.md`
- Create: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/scripts/mpe_review_policy.py`
- Test: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests/test_sync.py`, `tests/test_sync_browser.py`

**Interfaces:**
- Consumes: existing `load_source(path: Path, repo: Path) -> SourcePack`, `build_explanation(pack, fragments, stage: Path, repo: Path) -> Artifacts` and existing tests' fixture builders.
- Produces: `rerender(repo, target, run) -> int`; `POLICY_VERSION: str`; `carry_reviews(stored: dict, fresh: dict, references: list, reusable: bool) -> dict`; review records and manifests carry `review_policy_version`.

- [x] **Step 1: Add behavioral regressions before implementation.** Stage fixtures test problem-pane/original preservation, valid choice feedback versus static fallback, review-only newest-first all, subpart boundaries, policy-aware approval reuse, changed/missing references and source inputs. Use literal expected states:

```python
def test_legacy_policy_cannot_reuse_approval():
    from mpe_review_policy import carry_reviews
    old = {'content': {'status': 'pass'}, 'independent': {'status': 'pass'}}
    fresh = {'content': {'status': 'not_run'}, 'independent': {'status': 'not_run'}}
    result = carry_reviews(old, fresh, [], True)
    assert result['content']['status'] == 'not_run'
    assert result['independent']['status'] == 'not_run'
```

- [x] **Step 2: Run RED and baseline suites.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests/test_sync.py" -q`
Expected: failures for missing panel, all, review-policy module or model wiring, not fixture/import mistakes. Record baseline platform problems separately.

- [x] **Step 3: Implement local contracts and adapters.** Copy bio's latest template behavior; retain course code styles and keys. Add optional verified choice model only for HTML adapters. Keep raw source metadata/legacy payload hashes backward-compatible when no model exists. Exclude choices before matching subpart labels. Keep strict same-input reuse; verify relocated reference bytes and actual image/link targets, otherwise reset approval. EC2 retains its composite source digest; ML retains normalized fragment hashes and homework layout. Store policy on initial reviews and manifests, and reject stale policy on new publish.

```python
POLICY_VERSION = 'problem-explain-2026-10-15'

def carry_reviews(stored, fresh, references, reusable):
    result = dict(fresh)
    result['review_policy_version'] = POLICY_VERSION
    result['references'] = references
    if reusable and stored.get('review_policy_version') == POLICY_VERSION:
        for key in ('content', 'independent'):
            if stored.get(key, {}).get('status') == 'pass':
                result[key] = stored[key]
    return result
```

- [x] **Step 4: Run GREEN and existing skill tests.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-jagual/.agents/skills/ds-problem-explain/tests" -q`
Expected: new behavioral regressions pass; existing code/math, path, publication rollback and layout tests pass after intentional UI expectations are updated. New fixture approvals explicitly identify current policy; a dedicated legacy fixture stays versionless and is rejected. No test targets real coursework publish paths.

- [x] **Step 5: Update skill contracts and pinned provenance.** Document exact all/rerender commands and course paths, static choice fallback, independent checks and policy invalidation. Preserve existing parent review-pack integration text. Pin bio source commit and destination hashes without rewriting historical source hashes. Record the tested diff; commits remain uncreated per user scope.

### Task 2: ML standalone synchronization

**Files:**
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/scripts/mpe_source.py`, `mpe_render.py`, `mpe_cli.py`, `mpe_contract.py`, `mpe_publish.py`
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/assets/note-template.html`, `assets/port-provenance.json`, `SKILL.md`, `references/authoring.md`, `references/verification.md`
- Create: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/scripts/mpe_review_policy.py`
- Test: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests/test_sync.py`, `tests/test_sync_browser.py`

**Interfaces:**
- Consumes: existing `load_source(path: Path, repo: Path) -> SourcePack`, `build_explanation(pack, fragments, stage: Path, repo: Path) -> Artifacts` and existing tests' fixture builders.
- Produces: `rerender(repo, target, run) -> int`; `POLICY_VERSION: str`; `carry_reviews(stored: dict, fresh: dict, references: list, reusable: bool) -> dict`; review records and manifests carry `review_policy_version`.

- [x] **Step 1: Add behavioral regressions before implementation.** Stage fixtures test problem-pane/original preservation, valid choice feedback versus static fallback, review-only newest-first all, subpart boundaries, policy-aware approval reuse, changed/missing references and source inputs. Use literal expected states:

```python
def test_legacy_policy_cannot_reuse_approval():
    from mpe_review_policy import carry_reviews
    old = {'content': {'status': 'pass'}, 'independent': {'status': 'pass'}}
    fresh = {'content': {'status': 'not_run'}, 'independent': {'status': 'not_run'}}
    result = carry_reviews(old, fresh, [], True)
    assert result['content']['status'] == 'not_run'
    assert result['independent']['status'] == 'not_run'
```

- [x] **Step 2: Run RED and baseline suites.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests/test_sync.py" -q`
Expected: failures for missing panel, all, review-policy module or model wiring, not fixture/import mistakes. Record baseline platform problems separately.

- [x] **Step 3: Implement local contracts and adapters.** Copy bio's latest template behavior; retain course code styles and keys. Add optional verified choice model only for HTML adapters. Keep raw source metadata/legacy payload hashes backward-compatible when no model exists. Exclude choices before matching subpart labels. Keep strict same-input reuse; verify relocated reference bytes and actual image/link targets, otherwise reset approval. EC2 retains its composite source digest; ML retains normalized fragment hashes and homework layout. Store policy on initial reviews and manifests, and reject stale policy on new publish.

```python
POLICY_VERSION = 'problem-explain-2026-10-15'

def carry_reviews(stored, fresh, references, reusable):
    result = dict(fresh)
    result['review_policy_version'] = POLICY_VERSION
    result['references'] = references
    if reusable and stored.get('review_policy_version') == POLICY_VERSION:
        for key in ('content', 'independent'):
            if stored.get(key, {}).get('status') == 'pass':
                result[key] = stored[key]
    return result
```

- [x] **Step 4: Run GREEN and existing skill tests.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/.claude/skills/ml-problem-explain/tests" -q`
Expected: new behavioral regressions pass; existing code/math, path, publication rollback and layout tests pass after intentional UI expectations are updated. New fixture approvals explicitly identify current policy; a dedicated legacy fixture stays versionless and is rejected. No test targets real coursework publish paths.

- [x] **Step 5: Update skill contracts and pinned provenance.** Document exact all/rerender commands and course paths, static choice fallback, independent checks and policy invalidation. Preserve existing parent review-pack integration text. Pin bio source commit and destination hashes without rewriting historical source hashes. Record the tested diff; commits remain uncreated per user scope.

### Task 3: EC2 standalone synchronization

**Files:**
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/scripts/epe_source.py`, `epe_render.py`, `epe_cli.py`, `epe_contract.py`, `epe_publish.py`
- Modify: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/assets/note-template.html`, `assets/port-provenance.json`, `SKILL.md`, `references/authoring.md`, `references/verification.md`
- Create: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/scripts/epe_review_policy.py`
- Test: `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests/test_sync.py`, `tests/test_sync_browser.py`

**Interfaces:**
- Consumes: existing `load_source(path: Path, repo: Path) -> SourcePack`, `build_explanation(pack, fragments, stage: Path, repo: Path) -> Artifacts` and existing tests' fixture builders.
- Produces: `rerender(repo, target, run) -> int`; `POLICY_VERSION: str`; `carry_reviews(stored: dict, fresh: dict, references: list, reusable: bool) -> dict`; review records and manifests carry `review_policy_version`.

- [x] **Step 1: Add behavioral regressions before implementation.** Stage fixtures test problem-pane/original preservation, valid choice feedback versus static fallback, review-only newest-first all, subpart boundaries, policy-aware approval reuse, changed/missing references and source inputs. Use literal expected states:

```python
def test_legacy_policy_cannot_reuse_approval():
    from epe_review_policy import carry_reviews
    old = {'content': {'status': 'pass'}, 'independent': {'status': 'pass'}}
    fresh = {'content': {'status': 'not_run'}, 'independent': {'status': 'not_run'}}
    result = carry_reviews(old, fresh, [], True)
    assert result['content']['status'] == 'not_run'
    assert result['independent']['status'] == 'not_run'
```

- [x] **Step 2: Run RED and baseline suites.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests/test_sync.py" -q`
Expected: failures for missing panel, all, review-policy module or model wiring, not fixture/import mistakes. Record baseline platform problems separately.

- [x] **Step 3: Implement local contracts and adapters.** Copy bio's latest template behavior; retain course code styles and keys. Add optional verified choice model only for HTML adapters. Keep raw source metadata/legacy payload hashes backward-compatible when no model exists. Exclude choices before matching subpart labels. Keep strict same-input reuse; verify relocated reference bytes and actual image/link targets, otherwise reset approval. EC2 retains its composite source digest; ML retains normalized fragment hashes and homework layout. Store policy on initial reviews and manifests, and reject stale policy on new publish.

```python
POLICY_VERSION = 'problem-explain-2026-10-15'

def carry_reviews(stored, fresh, references, reusable):
    result = dict(fresh)
    result['review_policy_version'] = POLICY_VERSION
    result['references'] = references
    if reusable and stored.get('review_policy_version') == POLICY_VERSION:
        for key in ('content', 'independent'):
            if stored.get(key, {}).get('status') == 'pass':
                result[key] = stored[key]
    return result
```

- [x] **Step 4: Run GREEN and existing skill tests.**

Run: `python -m pytest --rootdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests" --confcutdir="C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests" "C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-electronic-circuits-2/.claude/skills/ec2-problem-explain/tests" -q`
Expected: new behavioral regressions pass; existing code/math, path, publication rollback and layout tests pass after intentional UI expectations are updated. New fixture approvals explicitly identify current policy; a dedicated legacy fixture stays versionless and is rejected. No test targets real coursework publish paths.

- [x] **Step 5: Update skill contracts and pinned provenance.** Document exact all/rerender commands and course paths, static choice fallback, independent checks and policy invalidation. Preserve existing parent review-pack integration text. Pin bio source commit and destination hashes without rewriting historical source hashes. Record the tested diff; commits remain uncreated per user scope.

### Task 4: Browser stage acceptance and protected-file audit

**Files:**
- Create: local skill `tests/test_sync_browser.py` behavioral acceptance tests and temporary stage under `.scratch/problem-explain-sync-20261015/`.
- Modify: `.scratch/problem-explain-sync-20261015/progress.md` and save browser results/screenshots there.

**Interfaces:**
- Consumes: each course `build_explanation`, `check_artifacts`, current policy and synthetic fixtures.
- Produces: persistent temporary HTML/MD stage previews, browser results, baseline comparison report.

- [x] **Step 1: Exercise UI state in Chromium.**

```python
for width in (1024, 1280):
    page.set_viewport_size({'width': width, 'height': 900})
    page.goto(url, wait_until='networkidle')
    assert page.locator('#panel-left').is_visible()
    assert page.locator('#panel-prob').is_visible()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
page.locator('#toggle-left').click()
page.reload(wait_until='networkidle')
assert page.locator('#panel-left').is_hidden()
```

- [x] **Step 2: Verify both themes, mobile fold, original tabs, dock/float/movement/resize, choices or static absence, image zoom and print remount.** Record console errors, failed requests, external requests, KaTeX errors and horizontal overflow; all must be zero. Browser tests use synthetic stages and never invoke publish.
- [x] **Step 3: Run all three scoped suites and repository-level checks where discoverable.** Capture complete output; disclose unrelated baseline collection/platform failures by name, rather than hiding them.
- [x] **Step 4: Compare protected explanation hashes and review the whole diff.**

```python
for name, digest in baseline.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
```

Expected: zero removed or changed protected explanations, no new published explanations, only intended skill files and plan/spec/evidence changes. Fresh reviewer checks policy carry, source preservation, model wiring and existing modifications. Record fixes and final results in the ledger; no commits/push/publication.

## Self-review

Spec coverage: UI and source preservation -> Tasks 1-3, browser -> Task 4; policy and composite hashes -> Tasks 1-3; docs/provenance -> each Step 5; no-publication -> Task 4 hash audit. All named interfaces are defined in their owning task. No unresolved implementation placeholders. Current user authorization is execution method: inline; run continuously without another permission round.

## Execution result (2026-10-16 KST)

Completed approved scope A. DS 124 passed; EC2 118 passed plus 31 subtests; ML 111 passed with 2 unchanged baseline 1014 delivery failures. See `../reports/2026-10-16-problem-explain-sync.md`. No existing explanation was republished; all 3092 protected files are byte-identical.
