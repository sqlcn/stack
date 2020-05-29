
class Stack:
    #初始化对象，生产一个空栈
    def __init__(self):
        super().__init__()
        self.stack = []
    # 进栈操作
    def push(self, obj):
        self.stack.append(obj)
    # 出栈操作
    def pop(self):
        obj = self.stack[len(self.stack) - 1]
        self.stack.pop()
        return obj
    # 返回栈里还有多少个个数据
    def length(self):
        return len(self.stack)


with open('file.txt', 'r') as f:
    for line in f.readlines():
        # 去除line首尾的空格或换行符 这里主要是去除'\n'
        line = line.strip()
        print('*'*20)
        print(line)
        # 构造一个'栈'
        stack = Stack()
        # 从头到尾遍历line的每一个字符存到变量c中
        for c in line:
            # 如果字符c是个数
            if c.isnumeric():
                # 将c的内容push到栈中
                stack.push(c)
            # 如果c为算数符号
            elif c == '+' or c == '-' or c == '*' or c == '/':
                # 将栈顶（最后入栈）的内容弹出到变量a1中
                a1 = stack.pop()
                # 同样的操作得到第二个数
                a2 = stack.pop()
                # 将a2,c,a1拼接成字符串表达式，并用eval方法计算这个表达式，结果存入result
                result = eval(a2+c+a1)
                print(a2, c, a1, '=', result)
                stack.push(str(result))
        print(stack.pop())
        # 如果栈不为空（栈里还有内容）则报错
        if stack.length():
            print('Error!')
