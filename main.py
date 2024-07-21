import random
import time
from turtle import *


class Paddle(Turtle):

    def __init__(self):
        super().__init__("square")
        self.color("white")
        self.penup()
        self.shapesize(1, 6)
        self.goto(0, -150)
        window.listen()
        window.onkey(lambda: self.backward(50), "Left")
        window.onkey(lambda: self.forward(50), "Right")


class AtariBrick(Turtle):

    def __init__(self):
        super().__init__("square")
        self.shapesize(1, 2)
        self.penup()
        self.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def destroy(self):
        self.hideturtle()


class Ball(Turtle):

    def __init__(self):
        super().__init__("circle")
        self.fillcolor("white")
        self.penup()
        self.goto(0, 0)
        self.speed("slow")
        self.x_move = 5
        self.y_move = 5

    def move(self):
        self.goto(self.xcor() + self.x_move, self.ycor() + self.y_move)

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1


class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.goto(100, -200)
        self.fillcolor("white")
        self.score = 0
        self.lives = 3
        self.hideturtle()
        self.writeScore()

    def writeScore(self):
        self.pencolor("white")
        self.write(f"Score: {self.score}", font=("Arial", 30, "bold"))
        self.sety(self.ycor()-50)
        self.write(f"Lives: {self.lives}", font=("Arial", 30, "bold"))
        self.sety(self.ycor()+50)

    def increaseScore(self):
        self.clear()
        self.score += 1
        self.writeScore()

    def loseLife(self):
        self.lives -= 1
        self.writeScore()

    def gameOver(self):
        self.pencolor("red")
        self.goto(-200, 0)
        self.write("Game Over!", font=("Helvica", 50, "bold"))

    def youWIN(self):
        self.pencolor("green")
        self.goto(-175, 0)
        self.write("You WIN!", font=("Helvica", 50, "bold"))


window = Screen()
window.colormode(255)
window.bgcolor("black")
window.window_width()
window.screensize(500, 500)

paddle = Paddle()
ball = Ball()
score = ScoreBoard()
atari = []
y_cors = [230, 205, 180, 155, 130, 105, 80, 55]
x_cors = [-280, -240, -200, -160, -120, -80, -40, 0, 40, 80, 120, 160, 200, 240, 280]
window.tracer(0)
for i in range(len(y_cors)):
    for n in range(len(x_cors)):
        brick = AtariBrick()
        brick.sety(y_cors[i])
        brick.setx(x_cors[n])
        atari.append(brick)
game = True

window.update()
time.sleep(3)
while game:
    window.update()
    ball.move()

    if abs(ball.xcor() - paddle.xcor()) < 90 and abs(ball.ycor() - paddle.ycor()) < 20:
        ball.bounce_y()

    if ball.xcor() >= 330 or ball.xcor() <= -330:
        ball.bounce_x()

    if ball.ycor() >= 290:
        ball.bounce_y()

    for i in atari:
        if abs(ball.xcor() - i.xcor()) < 40 and abs(ball.ycor() - i.ycor()) < 20:
            i.destroy()
            atari.remove(i)
            ball.bounce_y()
            score.increaseScore()

    if ball.ycor() <= -250:
        score.loseLife()
        ball.goto(0,0)
        paddle.setx(0)
        time.sleep(3)

    if score.score == 120:
        score.youWIN()
        game = False

    if score.lives == 0:
        score.gameOver()
        game = False

mainloop()
