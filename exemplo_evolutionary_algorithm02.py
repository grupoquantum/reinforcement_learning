from Neuraline.ArtificialIntelligence.MachineLearning.ReinforcementLearning.evolutionary_algorithm import EvolutionaryAlgorithm
evolutionary_algorithm = EvolutionaryAlgorithm()
import turtle as interface
from random import randrange
screen = interface.Screen() 
screen.title('Pong Game - Multiplayer') 
screen.bgcolor('black') 
screen.setup(width=1000, height=600) 
canvas = screen.getcanvas()
geometry = '{}x{}+{}+{}'.format(1000, 600, 20, 20)
screen.cv._rootwindow.resizable(False, False)
canvas.master.geometry(geometry)
left_bar, right_bar = interface.Turtle(), interface.Turtle()
left_bar.speed(0), right_bar.speed(0)
left_bar.shape('square'), right_bar.shape('square')
left_bar.color('white'), right_bar.color('white')
left_bar.shapesize(stretch_wid=6, stretch_len=2), right_bar.shapesize(stretch_wid=6, stretch_len=2)
left_bar.penup(), right_bar.penup()
left_bar.goto(-400, 0), right_bar.goto(400, 0) 
hit_ball = interface.Turtle()
hit_ball.speed(40) 
hit_ball.shape('circle') 
hit_ball.color('black')
hit_ball.fillcolor('white')
hit_ball.penup() 
hit_ball.goto(0, 0) 
hit_ball.dx, hit_ball.dy = 5, -5
left_player, right_player, inputs, inputs_length = 0, 0, [], 0
panel = interface.Turtle() 
panel.speed(0) 
panel.color('white') 
panel.penup() 
panel.hideturtle() 
panel.goto(0, 260) 
panel.write('Human_PLAYER: 0    Robot_PLAYER: 0', align='center', font=('Courier', 24, 'normal')) 
def left_bar_up(): left_bar.sety(left_bar.ycor()+20) 
def right_bar_up(): left_bar.sety(left_bar.ycor()-20)
def set_punctuation(left_score=0, right_score=0):
    panel.clear()
    panel.write(f'Human_PLAYER: {left_score}    Robot_PLAYER: {right_score}', align='center', font=('Courier', 24, 'normal'))
screen.listen() 
screen.onkeypress(left_bar_up, 'Up'), screen.onkeypress(right_bar_up, 'Down')
while True:
    try:
        screen.update() 
        hit_ball.setx(hit_ball.xcor()+hit_ball.dx), hit_ball.sety(hit_ball.ycor()+hit_ball.dy)
        action, random = hit_ball.ycor(), randrange(-280, 281)
        # before the robot touches
        if (hit_ball.xcor() >= 360 and hit_ball.xcor() <= 370):
            if len(inputs) > 0:
                if len(inputs) > inputs_length:
                    # train with the latest actions
                    evolutionary_algorithm.fit(inputs=inputs)
                    inputs_length = len(inputs)
                # prediction for new action
                try: action = evolutionary_algorithm.predict(individuals=1)[0][0]
                except: pass
            else: action = random
        if hit_ball.ycor() > 280: 
            hit_ball.sety(280) 
            hit_ball.dy *= -1      
        if hit_ball.ycor() < -280: 
            hit_ball.sety(-280) 
            hit_ball.dy *= -1
        # robot error     
        if hit_ball.xcor() > 500: 
            hit_ball.goto(0, 0) 
            hit_ball.dy *= -1
            left_player += 1
            right_player = max(0, right_player-1)
            set_punctuation(left_player, right_player)
            # punish the wrong action
            evolutionary_algorithm.punishment()
        # human error      
        if hit_ball.xcor() < -500: 
            hit_ball.goto(0, 0) 
            hit_ball.dy *= -1
            right_player += 1
            left_player = max(0, left_player-1)
            set_punctuation(left_player, right_player)
        # robot touch
        if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (hit_ball.ycor() < right_bar.ycor()+80 and hit_ball.ycor() > right_bar.ycor()-80): 
            hit_ball.setx(360) 
            hit_ball.dx*=-1
            right_player += 1
            set_punctuation(left_player, right_player)
            # reward right action
            evolutionary_algorithm.reward()
            if [hit_ball.ycor()] not in inputs: inputs.append([hit_ball.ycor()])
        # human touch
        if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and (hit_ball.ycor() < left_bar.ycor()+80 and hit_ball.ycor() > left_bar.ycor()-80): 
            hit_ball.setx(-360) 
            hit_ball.dx*=-1
            left_player += 1
            set_punctuation(left_player, right_player)
            if [hit_ball.ycor()] not in inputs: inputs.append([hit_ball.ycor()])
        if hit_ball.xcor() >= 200:
            if hit_ball.xcor() >= 359 and hit_ball.xcor() <= 369: right_bar.sety(action)
            else: right_bar.sety(hit_ball.ycor())
    except: exit()