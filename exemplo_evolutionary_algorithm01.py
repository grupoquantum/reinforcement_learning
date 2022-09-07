from Neuraline.ArtificialIntelligence.MachineLearning.ReinforcementLearning.evolutionary_algorithm import EvolutionaryAlgorithm
evolutionary_algorithm = EvolutionaryAlgorithm()
import tkinter as tk
window = tk.Tk()
width, height, punctuation, record, action, inputs = 900, 500, 0, 0, 0, []
canvas = tk.Canvas(window, bg='black', width=width, height=height)
geometry = '{}x{}+{}+{}'.format(width, height, 30, 30)
canvas.master.geometry(geometry)
window.resizable(False, False)
window.title('Pong Game - Single Player')
canvas.pack()
ball = canvas.create_oval(430, 10, 470, 50, fill='white')
platform_y = height - 20
platform = canvas.create_rectangle(width//2-50, platform_y, width//2+50, platform_y+10, fill='white')
speed_x = speed_y = 2
text_punctuation = canvas.create_text(100, 20, text=f'Punctuation: {punctuation} - record: {record}', font=('Arial Bold', 12), fill='white')
def set_punctuation(game_over=False):
    global punctuation, record, action, inputs
    if game_over:
        punctuation = 0
        if len(inputs) > 0:
            # punish the wrong action
            evolutionary_algorithm.punishment()
            # train with the latest actions
            evolutionary_algorithm.fit(inputs=inputs)
            # prediction for new action
            action = evolutionary_algorithm.predict(individuals=1)[0][0]
        elif [action] not in inputs: inputs.append([action])
    else:
        punctuation = punctuation + 1
        if punctuation > record: record = punctuation
        # reward right action
        evolutionary_algorithm.reward()
        if [action] not in inputs: inputs.append([action])
    canvas.itemconfig(text_punctuation, text=f'Punctuation: {punctuation} - record: {record}')
def to_right():
    def right_position(event):
        x1, y1, x2, y2 = canvas.coords(platform)
        if x2 < width:
            limit = min(width-x2, 10)
            canvas.move(platform, limit, 0)
    right_position('<Right>')
def to_left():
    def left_position(event):
        x1, y1, x2, y2 = canvas.coords(platform)
        if x1 > 0:
            limit = min(x1, 10)
            canvas.move(platform, -limit, 0)
    left_position('<Left>')
def move_ball():
    global speed_x, speed_y, action
    ball_x1, ball_y1, ball_x2, ball_y2 = canvas.coords(ball)
    if ball_x1 <= 0 or ball_x2 >= width: speed_x = -speed_x
    if ball_y1 <= 0: speed_y = (2+punctuation)
    elif ball_y2 >= platform_y:
        ball_position = (ball_x1 + ball_x2) // 2
        platform_x1, _, platform_x2, _ = canvas.coords(platform)
        speed_y = -(2+punctuation)
        action = speed_x
        if platform_x1 <= ball_position <= platform_x2: set_punctuation(game_over=False) 
        else: set_punctuation(game_over=True)
    canvas.move(ball, speed_x, speed_y), canvas.after(20, move_ball), canvas.move(platform, action, 0)
    platform_x1, _, platform_x2, _ = canvas.coords(platform)
    if platform_x1 <= 0: to_right()
    if platform_x2 >= width: to_left()
move_ball()
window.mainloop()