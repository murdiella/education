import math as m

S = 0
p = 0
f = 1/6
def an(i):
    return (2*m.sin(m.pi*i/3)+m.sin(2*m.pi*i/3)-m.sin(m.pi*i))/(m.pi*i)
def bn(i):
    return (-2*m.cos(m.pi*i/3)-m.cos(2*m.pi*i/3)+3*m.cos(m.pi*i))/(m.pi*i)

for i0 in range(20):
    i = i0 + 1
    print(-m.atan(bn(i)/an(i)))
    for x0 in range(600):
        x = (x0+1)/100-3
        if 0 >= x:
            g = 0
        elif 1 > x and x > -3:
            g = 1
        elif x >= 1 and x < 2:
            g = -1
        elif x >= 2 and x < 3:
            g = -2
        f = f + an(i)*m.cos(i*m.pi*x/3) + bn(i)*m.sin(i*m.pi*x/3)
        S = S + (g-f)*(g-f)
        p += 1
S = m.sqrt(S/p)/100
print(S)
