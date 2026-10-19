function calc(t){return {theta:t,x:80+35*t,y:240-35*t,squaredError:(1-t)**2+(3-t)**2};}
console.log(JSON.stringify([0,2,4].map(calc)));
