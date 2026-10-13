"""Source-specific authoring for the nine frozen review packs; no approvals here."""
from pathlib import Path
import json,re,sys,html,os
REPO=Path(os.environ.get('ML_EXPLAIN_REPO',Path(__file__).resolve().parents[3]))
sys.path.insert(0,str(REPO/'.claude/skills/ml-problem-explain/scripts'))
from mpe_cli import load_run
ROOT=Path(os.environ.get('ML_EXPLAIN_WORKSPACE',Path(__file__).parent))
# Each record supplies learner-facing concept selection, actual first line,
# pitfalls and independently derived per-subpart checks. Full worked steps
# are source-grounded and then reviewed; original cards remain untouched.
DATA={}
def add(date,rows):DATA[date]=rows
add('0909',[
(r'기울기(slope)는 입력 1 증가당 출력 변화예요. $f(x)=\theta x$에서 $x$는 입력, $\theta$는 고정 기울기예요. 주어진 입력에 곱하고, 가파르기는 $|\theta|$로 비교해요.',r'$f(10)=\theta\cdot10$을 먼저 적어요.',r'음의 기울기는 내려가는 방향을 뜻해요. 가파르기는 부호가 아니라 절댓값으로 비교해요.',[r'입력 10으로 나누면 출력 -10, 5, 20에서 각각 -1, 1/2, 2가 복원돼요.',r'$|-1|=1$, $|1/2|=1/2$, $|2|=2$로 마지막이 가장 가파라요. 원 참고 답의 “클수록”은 양의 기울기끼리만 맞아요.']),
(r'행렬 곱(matrix multiplication)은 앞 행과 뒤 열의 내적이에요. $A\in\mathbb R^{m\times n}$, $B\in\mathbb R^{n\times r}$이면 $(AB)_{ij}=\sum_{k=1}^n A_{ik}B_{kj}$예요. 합칠 길이가 같아야 해요.',r'$A:3\times2$, $B:3\times3$을 적어요.',r'행 수끼리 비교하지 않아요. 앞의 열 수와 뒤의 행 수를 비교해요.',[r'첫 칸부터 길이 2인 행과 길이 3인 열을 내적해야 하므로 정의되지 않아요. 결과를 0행렬로 쓰면 안 돼요.']),
(r'같은 두 행렬도 순서에 따라 행과 열의 짝이 달라져요. $(AB)_{ij}=\sum_k A_{ik}B_{kj}$에서 $i,j$는 결과의 행·열이에요. 두 3×3 행렬은 양쪽 순서 모두 곱할 수 있지만 교환법칙은 없어요.',r'(b)는 $C_{11}=1\cdot1+2\cdot0+3\cdot1=4$로 시작해요. (c)는 순서를 바꿔 $D_{11}=1+4=5$예요.',r'두 결과가 모두 3×3이어도 값이 같다는 뜻은 아니에요.',[r'각 열은 앞 행렬의 두 열을 합한 것이에요. 첫 열은 1열+3열이라 [4,10,16]이 나와요. 독립 계산한 전체 행은 [4,3,5], [10,9,11], [16,15,17]이에요.',r'각 행은 뒤 행렬의 두 행을 합해요. 1행=1행+2행=[5,7,9], 2행=2행+3행=[11,13,15], 3행=1행+3행=[8,10,12]예요.']),
(r'직사각형 행렬 곱도 같은 내적 규칙을 써요. $(m\times n)(n\times r)$의 결과는 $m\times r$예요. 공통 길이 $n$은 곱해 더하는 횟수예요.',r'$(2\times4)(4\times2)=2\times2$, 첫 칸 $0+2+2+10=14$예요.',r'각 성분끼리만 곱하는 원소별 곱과 혼동하지 않아요.',[r'별도 내적으로 4칸을 구하면 행이 [14,6], [-21,2]예요. 둘째 행 둘째 열은 $12-1-1-8=2$로 부호를 확인해요.']),
(r'순서를 바꾸면 합칠 길이도 결과 크기도 달라져요. $(4\times2)(2\times4)$는 길이 2 내적 16개로 4×4 결과를 만들어요.',r'첫 행 $[0,3]$과 첫 열 $[1,4]^\top$의 내적 $0+12=12$예요.',r'이전 문제의 2×2 답을 전치하는 것이 아니에요. 곱 순서 교환과 전치는 다른 연산이에요.',[r'독립적으로 각 행을 선형결합하면 [12,3,-3,-12], [-3,1,2,6], [6,5,1,0], [13,12,3,2]예요. 4행 4열은 $5\cdot2+2(-4)=2$예요.'])])

def paragraphs(text):
 # Source steps can contain lists/tables; retain math/semantic markup while
 # dropping leading subpart labels beneath an explicit matching heading.
 return '<p>'+text.strip()+'</p>\n'
def section(k,title,body,cls='formal'):
 return f'<div class="layer {cls}" data-explanation="{k}"><h4>{title}</h4>{body}</div>'
def groups(p,steps):
 if len(p.subparts)==1:return {p.subparts[0]:steps},[]
 out={s:[] for s in p.subparts};common=[];current=None
 for step in steps:
  m=re.match(r'\s*\(([a-z])\)',re.sub('<[^>]+>','',step))
  if m and m[1] in out:current=m[1];step=re.sub(r'^\s*\('+current+r'\)\s*','',step)
  if current:out[current].append(step)
  else:common.append(step)
 return out,common

def author(date):
 item=load_run(ROOT/date)[0];pck=item['pack']
 assert len(DATA[date])==len(pck.problems)
 for p,row in zip(pck.problems,DATA[date]):
  recall,start,pitfall,checks=row
  assert len(checks)==len(p.subparts),(date,p.id)
  steps=list(p.reference_steps)
  if date=='1007' and p.id=='p8':
   steps[0]=r'두 이차형식을 따로 이름 붙여요. $$Q_A=(\mathbf{x}-\mathbf{a})^\top\mathbf{A}^{-1}(\mathbf{x}-\mathbf{a})$$ $$Q_B=(\mathbf{x}-\mathbf{b})^\top\mathbf{B}^{-1}(\mathbf{x}-\mathbf{b})$$ 두 밀도의 곱을 $P(\mathbf{x})$라고 하면, 입력과 무관한 정규화 상수를 제외하고 $$P(\mathbf{x})\propto\exp\left(-\frac12(Q_A+Q_B)\right)$$예요. 곱의 지수를 더한다는 뜻이에요.'
  if date=='0921' and p.id=='p1':
   steps=[s.replace('그래서 $a$는 $b$에도 $c$에도 의존하지 않아요.','그래서 그래프에서 $a$의 부모는 없어요. 이는 $a$가 $b,c$와 통계적으로 독립이라는 뜻은 아니에요.') for s in steps]
  if date=='0928' and p.id=='p3':
   steps=[s for s in steps if not ('차수가 높을수록 최대우도 해는' in s or '계수가 큰 8차에서' in s)]
  grouped,common=groups(p,steps)
  solve=''.join(paragraphs(s) for s in common)
  for sub,check in zip(p.subparts,checks):
   body=''.join(paragraphs(s) for s in grouped[sub])
   if not body:body=paragraphs(check)
   solve+=f'<div data-subpart="{sub}"><h4>{"풀이" if sub=="main" else "("+sub+")"}</h4>{body}</div>'
  verify=''
  for sub,check in zip(p.subparts,checks):verify+=f'<div data-subpart="{sub}"><h4>{"검산" if sub=="main" else "("+sub+") 검산"}</h4>{paragraphs(check)}</div>'
  # Complete original answer shown once, with source interpretation caveats
  # in the learner-facing checks rather than silently editing frozen sources.
  verify+=paragraphs(p.reference_answer)
  if date=='0928' and p.id=='p3':verify+=paragraphs('원 참고 답의8차 선택은 해당 예제의 경향으로 읽어요. 모든 데이터에서 계수가 반드시 더 크다는 주장은 성립하지 않아요.')
  if date=='0921' and p.id=='p1':verify+=paragraphs('원 참고 답에서 “의존하지 않음”은 부모가 없다는 뜻으로 한정해 읽어요. 결합분포의 통계적 독립과 구별해요.')
  body=section('understand','무엇을 구하는 문제인가요?',paragraphs(html.escape(p.title.split('. ',1)[-1])+'를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.'),'eli5')
  body+=section('recall','이 문제를 봤을 때 떠올릴 개념과 공식',paragraphs(recall))
  body+=section('start','종이에 적을 첫 줄',paragraphs(start))
  body+=section('solve','왜 이렇게 푸는지 함께 따라가요',solve)
  body+=section('verify','완성 답과 검산',verify)
  body+=section('pitfall','여기서 주의해요',paragraphs(pitfall),'warn')
  body+=section('retry','설명을 닫고 다시 해요',f'<ol><li>{start}</li><li>각 소문항의 계산과 이유를 직접 적어요.</li><li>{pitfall}</li></ol>')
  summary_recall=recall.split('예요.')[0]+'예요.' if '예요.' in recall else recall.split('요.')[0]+'요.'
  formulas=re.findall(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)',recall)
  if formulas and formulas[0] not in summary_recall:summary_recall+=' $'+formulas[0]+'$'
  body+='<div class="sum" hidden>'+''.join(f'<div class="summary-group"><h4>{title}</h4>{paragraphs(text)}</div>' for title,text in [('떠올릴 개념·공식',summary_recall),('첫 줄',start),('검산', ' '.join(checks))])+'</div>'
  (item['folder']/'explanations'/f'{p.id}.html').write_text(body+'\n',encoding='utf-8')
 if __name__=='__main__':print(date,len(pck.problems))

exec((ROOT/'content-data.py').read_text())

if __name__=='__main__':
 for date in sys.argv[1:] or sorted(DATA):author(date)
