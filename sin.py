import math
import turtle
a_list = []
x = 0
y = 0

t = turtle.Turtle()
t.shape("circle")
for i in range(60,300,10):
    a_list.append(i)

print(a_list)

for j in a_list:
    x += math.cos(math.radians(j))
    y += math.sin(math.radians(j))

    x1 = x*40
    y1 = y*40

    print(f'x:{x1} y:{y1}')

    t.goto(x1, y1)
    t.stamp()

turtle.mainloop()