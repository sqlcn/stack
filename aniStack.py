from tkinter import *
import time
import math

# 以下为全局变量
TubeX0 = 50         # 栈的左上角坐标位置
TubeY0 = 150
TubeDeep = 5        # 栈的深度（能容纳5个球）
BallRaius = 50      # 每个球的半径
# 预先计算栈的其他坐标点
TubeX1 = TubeX0+BallRaius                       # 栈底部小球的中心坐标
TubeY1 = TubeY0+BallRaius*TubeDeep
TubeTopX = TubeX0+BallRaius/2                   # 栈顶部出入口外的中心坐标
TubeTopY = TubeY0 - BallRaius/2-BallRaius/4

QueueX0 = 200       # 待进栈小球的坐标位置
QueueY0 = 100

# 运算动画时的相关坐标
EvalX1 = TubeX1 + (BallRaius+2)*2
EvalY = TubeY1-BallRaius/2
EvalX2 = EvalX1 + (BallRaius+2)*2
EvalXe = (EvalX1+EvalX2)/2

Speed = 2  # 小球移动的速度

class Ball:     # window:TK窗口对象，canvas:画布对象，txt:小球的内容，txt:小球的坐标
    def __init__(self, window, canvas, txt, pos):
        self.window = window
        self.canvas = canvas
        self.txt = txt

        self.ballId = self.canvas.create_oval(
            pos[0]-BallRaius/2, pos[1]-BallRaius /
            2, pos[0]+BallRaius/2, pos[1]+BallRaius/2,
            fill='green', outline='green')
        self.numId = self.canvas.create_text(pos[0], pos[1],
                                             text=self.txt, fill='yellow',
                                             font=('', BallRaius-25))

    def getTxt(self):
        return self.txt

    # def getIndex(self):
    #     return self.index

    def getPos(self):
        pos = self.canvas.coords(self.ballId)
        return [(pos[0]+pos[2])/2, (pos[1]+pos[3])/2]

    def animate(self, poly):
        for pos in poly:                                        # 遍历路径的每一个途经点
            startPos = self.getPos()                            # 获得开始位置坐标
            distance = self.distance(startPos, pos)             # 获得每一步需移动的x和y的步长（可能为负数）
            while not self.match(self.getPos(), pos):  # 测试是否到途经点
                # 根据x和y的步长，分别移动小球和小球里的数字（符号）
                self.canvas.move(self.ballId, distance[0], distance[1])
                self.canvas.move(self.numId, distance[0], distance[1])
                self.window.update()
                time.sleep(0.01)

    def distance(self, pos1, pos2):
        dx = pos2[0]-pos1[0]                # 分别计算x坐标和y坐标的距离
        dy = pos2[1]-pos1[1]
        dist = math.sqrt(dx*dx+dy*dy)       # 利用勾股定理计算两点的距离
        dtime = dist/Speed                  # 走完行程所用的时间
        return [dx/dtime, dy/dtime]         # 返回每次移动的步长

    def match(self, pos1, pos2, mat=1):     # 判断两个坐标点pos1和pos2是否重合，mat为精度，即mat=1时，误差+-0.5都算重合
        if abs(pos2[0]-pos1[0]) < mat and abs(pos2[1]-pos1[1]) < mat: #简单计算而不用勾股定理计算距离
            return True
        return False

    def destory(self):
        self.canvas.delete(self.ballId)
        self.canvas.delete(self.numId)


class Stack:    # canvas:画布对象
    def __init__(self, canvas):
        self.stack = []
        self.canvas = canvas
        # 画出栈的外形
        self.canvas.create_line(TubeX0-2, TubeY0-2,
                                TubeX0-2, TubeY1+2,
                                TubeX1+2, TubeY1+2,
                                TubeX1+2, TubeY0-2,
                                width=4, fill='blue', joinstyle=BEVEL)

    def push(self, ball):
        index = len(self.stack)
        # 小球移动的动画，参数是两个坐标点，先到栈口上部，然后落到栈里
        ball.animate([[TubeTopX, TubeTopY], [TubeTopX, TubeY1-(index*BallRaius)-BallRaius/2]])
        self.stack.append(ball)

    def pop(self):
        index = len(self.stack)-1
        ball = self.stack.pop()
        # 出栈动画，小球移动到栈口上方
        ball.animate([[TubeTopX, TubeTopY]])
        return ball


def main():

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
        ball = Ball(window, canvas, char, [QueueX0+BallRaius*index, QueueY0])
        queue.append(ball)
        # print(ball.getPos())
        index += 1

    for ball in queue:
        c = ball.getTxt()
        if c.isnumeric():               # 判断球内的字符是否数字
            stk.push(ball)              # 是数字，球就进栈
        elif c == '+' or c == '-' or c == '*' or c == '/':
            #下面几个animate方法演示计算过程的动画
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
            newBall = Ball(window, canvas, str(result), ball.getPos())

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
