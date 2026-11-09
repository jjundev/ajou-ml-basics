# Independent solve (separate agent; saw only tmp/ml-problem-explain/midterm1021-a1/problems-only.md, sympy inline)
p1:a (-2,16)^T | p1:b [[-2,2],[2,-5],[3,-1]], 3x2
p2:a [[2,1],[1,2]], det 3, (1/3)[[2,-1],[-1,2]] | p2:b p=(2,1,1), r=(1,-1,-1), A^T r=0
p3:a 1/(2*sqrt2*pi) exp(-1/4[(x1-2)^2-2(x1-2)(x2+2)+3(x2+2)^2]) | p3:b c=3e^2/sqrt(2pi), mean -1, var 1/9
p4:a (2/5,3/5), (3/10,3/10,2/5) | p4:b 3/4, not independent
p5:a P(D)=2/9, posterior (1/3,2/3) | p5:b MAP 2/3, P(X3=1|D)=5/9 vs plug-in 2/3
p6:a (4/3,3/2) | p6:b (1,1)
p7:a mu_x=(2,-1), Sx=[[3,1],[1,2]], mu_y=(2,3) | p7:b Sy=[[9,9],[9,18]], Cxy=[[4,5],[3,0]]
p8:a N(1,1/2) | p8:b Z=e^-1/(2 sqrt pi), not normalized
p9:a Phi^T Phi=2I, S_N=I/3 | p9:b Phi^T y=(4,2), m_N=(4/3,2/3), N(m_N, I/3)
p10:a N(8/3,5/3) | p10:b N(8/3,8/3)
Comparison with answer-checks.json and card answers: 20/20 agree.
