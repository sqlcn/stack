
with open('file.txt', 'r') as f:
    for line in f.readlines():
        # 去除line首尾的空格或换行符 这里主要是去除'\n'
        line = line.strip()
        print('*'*20)
        print(line)
        # 定义一个空栈
        stack = []
        # 从头到尾遍历line的每一个字符存到变量c中
        for c in line:
            # 如果字符c是个数
            if c.isnumeric():
                # 将c的内容push到栈中
                stack.append(c)
            # 如果c为算数符号
            elif c == '+' or c == '-' or c == '*' or c == '/':
                # 将栈顶（最后入栈）的内容存入变量a1中
                a1 = stack[len(stack) - 1]
                # 将栈顶的内容弹出（删除最后一个入栈的内容）
                stack.pop()
                # 同样的操作得到第二个数
                a2 = stack[len(stack)-1]
                stack.pop()
                # 将a2,c,a1拼接成字符串表达式，并用eval方法计算这个表达式，结果存入result
                result = eval(a2+c+a1)
                print(a2, c, a1, '=', result)
                stack.append(str(result))
        print(stack[len(stack) - 1])
        stack.pop()
        if len(stack):
            print('Error!')
