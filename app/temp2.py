import random
import time
import turtle


numbers = list(range(100))
random.shuffle(numbers)
print(numbers)

numbers = range(2, 8, 2)
print("Банан" * len(numbers))
print(list(numbers))


start, step, counter = 6,3,10
print([*range(start, counter * step + start, step)])

l1=[1,2,3]
l2=[3,2,1]
l3=[1,3,2]
if l1==l3:
    print("true")
else:
    print("false")

        
for i in range(2):
    for j in range(1, 6):
        if j % 2 == 1:
            continue
        if j == 3:
            break
        print(i, j)
        
        
def func():
    yield from range(1, 4)

for n in func():
    print(n, end=')')
    
import turtle
import math


def draw_house():
    # --- настройка окна ---
    screen = turtle.Screen()
    screen.title("Домик")
    screen.bgcolor("skyblue")
    screen.setup(width=700, height=600)

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pensize(3)

    # вспомогательная функция: прямоугольник с заливкой
    def rect(x, y, w, h, fill):
        t.penup()
        t.goto(x, y)
        t.setheading(0)
        t.pendown()
        t.color("black", fill)
        t.begin_fill()
        for _ in range(2):
            t.forward(w); t.left(90)
            t.forward(h); t.left(90)
        t.end_fill()

    # --- земля ---
    rect(-350, -200, 700, 100, "lightgreen")

    # --- корпус дома ---
    rect(-100, -100, 200, 150, "lightyellow")

    # --- крыша (треугольник) ---
    t.penup()
    t.goto(-120, 50)
    t.setheading(0)
    t.pendown()
    t.color("black", "tomato")
    t.begin_fill()
    t.goto(0, 160)
    t.goto(120, 50)
    t.goto(-120, 50)
    t.end_fill()

    # --- дверь ---
    rect(-30, -100, 60, 80, "saddlebrown")
    # ручка
    t.penup()
    t.goto(15, -60)
    t.pendown()
    t.color("gold")
    t.dot(9)

    # --- окна с рамами ---
    for wx in (-85, 45):
        rect(wx, -30, 40, 40, "lightskyblue")
        # крестовина
        t.color("black")
        t.penup(); t.goto(wx + 20, -30)
        t.setheading(90); t.pendown(); t.forward(40)
        t.penup(); t.goto(wx, -10)
        t.setheading(0); t.pendown(); t.forward(40)

    # --- солнце ---
    sun_x, sun_y, sun_r = 180, 165, 35
    t.penup()
    t.goto(sun_x, sun_y - sun_r)
    t.setheading(0)
    t.pendown()
    t.color("black", "gold")
    t.begin_fill()
    t.circle(sun_r)
    t.end_fill()

    # лучи
    for i in range(12):
        rad = math.radians(i * 30)
        x1 = sun_x + (sun_r + 5) * math.cos(rad)
        y1 = sun_y + (sun_r + 5) * math.sin(rad)
        x2 = sun_x + (sun_r + 20) * math.cos(rad)
        y2 = sun_y + (sun_r + 20) * math.sin(rad)
        t.penup(); t.goto(x1, y1)
        t.pendown(); t.goto(x2, y2)

    # --- облако из трёх кругов ---
    t.color("white", "white")
    for cx, cy, r in [(-180, 120, 25), (-210, 130, 30), (-240, 120, 25)]:
        t.penup()
        t.goto(cx, cy - r)      # центр круга окажется в (cx, cy)
        t.setheading(0)
        t.pendown()
        t.begin_fill()
        t.circle(r)
        t.end_fill()

    turtle.done()


draw_house()