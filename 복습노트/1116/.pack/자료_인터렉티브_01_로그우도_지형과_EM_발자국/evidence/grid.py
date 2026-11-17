import math, json
X=[1,2,3,4,10]
def L(a,b,v): return sum(math.log(.5*math.exp(-(x-a)**2/(2*v))/math.sqrt(2*math.pi*v)+.5*math.exp(-(x-b)**2/(2*v))/math.sqrt(2*math.pi*v)) for x in X)
out={}
for v in (4,16):
    best=max(((L(i/20,j/20,v),i/20,j/20) for i in range(-20,241) for j in range(-20,241)))
    out[v]={'gridmax_L':best[0],'at':best[1:]}
print(json.dumps(out))
