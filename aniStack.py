from tkinter import *
import time
import math

TubeX0 = 50
TubeY0 = 150
TubeDeep = 5
BallRaius = 50

QueueX0 = 200
QueueY0 = 100

MoveStep = 100
Speed = 2

TubeX1 = TubeX0+BallRaius
TubeY1 = TubeY0+BallRaius*TubeDeep
TubeTopX = TubeX0+BallRaius/2
TubeTopY = TubeY0 - BallRaius/2-BallRaius/4

EvalX1 = TubeX1 + (BallRaius+2)*2
EvalY = TubeY1-BallRaius/2
EvalX2 = EvalX1 + (BallRaius+2)*2
EvalXe = (EvalX1+EvalX2)/2


class Ball:
    def __init__(self, canvas, txt, pos):
        self.canvas = canvas
        self.txt = txt
        # self.index = index

        self.ballId = self.canvas.create_oval(
            pos[0]-BallRaius/2, pos[1]-BallRaius /
            2, pos[0]+BallRaius/2, pos[1]+BallRaius/2,
            fill='green', outline='green')
        self.numId = self.canvas.create_text(pos[0], pos[1],
                                             text=self.txt, fill='yellow',
                                             font=('', BallRaius-25))

    def getTxt(self):
        return self.txt

    def getIndex(self):
        return self.index

    def getPos(self):
        pos = self.canvas.coords(self.ballId)
        return [(pos[0]+pos[2])/2, (pos[1]+pos[3])/2]

    def animate(self, poly):
        for pos in poly:
            startPos = self.getPos()
            distance = self.distance(startPos, pos)
            # dx = (pos[0]-startPos[0])/MoveStep
            # dy = (pos[1]-startPos[1])/MoveStep
            while not self.match(self.getPos(), pos):         # 测试是否到达终点
                global window
                self.canvas.move(self.ballId, distance[0], distance[1])
                self.canvas.move(self.numId, distance[0], distance[1])
                window.update()
                time.sleep(0.01)

    def distance(self, pos1, pos2):
        dx = pos2[0]-pos1[0]
        dy = pos2[1]-pos1[1]
        dist = math.sqrt(dx*dx+dy*dy)      # 两点的距离
        dtime = dist/Speed                 # 走完动画花的时间
        return [dx/dtime, dy/dtime]

    def match(self, pos1, pos2, mat=1):
        if abs(pos2[0]-pos1[0]) < mat and abs(pos2[1]-pos1[1]) < mat:
            return True
        return False

    def destory(self):
        self.canvas.delete(self.ballId)
        self.canvas.delete(self.numId)


class Stack:
    def __init__(self, canvas):
        self.stack = []
        self.canvas = canvas
        self.canvas.create_line(TubeX0-2, TubeY0-2,
                                TubeX0-2, TubeY1+2,
                                TubeX1+2, TubeY1+2,
                                TubeX1+2, TubeY0-2,
                                width=4, fill='blue', joinstyle=BEVEL)

    def push(self, ball):
        index = len(self.stack)
        # ball = Ball(self.canvas, number, [
        #             TubeX0+BallRaius/2, TubeY1-(index*BallRaius)-BallRaius/2])
        ball.animate(
            [[TubeTopX, TubeTopY], [TubeTopX, TubeY1-(index*BallRaius)-BallRaius/2]])
        self.stack.append(ball)

    def pop(self):
        index = len(self.stack)-1
        ball = self.stack.pop()
        ball.animate([[TubeTopX, TubeTopY]])
        return ball


def main():
    global window

    strBuf = '65+1-5*'  # 需解析的字符串
    queue = []          # 等待处理的球的队列

    window = Tk()
    window.title('Stack animate')
    # window.geometry('640x480+50+50')

    canvas = Canvas(window, width=640, height=480,)
    canvas.pack()

    stk = Stack(canvas)

    # 生成球的队列
    index = 0
    for char in strBuf:
        ball = Ball(canvas, char, [QueueX0+BallRaius*index, QueueY0])
        queue.append(ball)
        # print(ball.getPos())
        index += 1

    for ball in queue:
        c = ball.getTxt()
        if c.isnumeric():               # 判断球内的字符是否数字
            stk.push(ball)              # 是数字，球就进栈
        elif c == '+' or c == '-' or c == '*' or c == '/':
            ball.animate([[EvalXe, EvalY]])

            ball1 = stk.pop()
            ball1.animate([[TubeTopX+BallRaius, TubeTopY], [EvalX1, EvalY]])

            ball2 = stk.pop()
            ball2.animate([[TubeTopX+BallRaius, TubeTopY], [EvalX2, EvalY]])

            a1 = ball1.getTxt()
            a2 = ball2.getTxt()
            ball1.animate([[EvalXe, EvalY]])
            ball2.animate([[EvalXe, EvalY]])
            
            result = eval(a1+c+a2)
            newBall = Ball(canvas, str(result), ball.getPos())

            ball1.destory()
            ball2.destory()
            ball.destory()
            # ball.setTxt(str(result))
            stk.push(newBall)
            # 删除ball1,ball2

    ball = stk.pop()
    ball.animate([[EvalXe, EvalY]])
    # time.sleep(1)

    window.mainloop()


if __name__ == "__main__":
    main()
