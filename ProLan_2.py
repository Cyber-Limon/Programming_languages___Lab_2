import math
import matplotlib.pyplot as plt
import numpy as np

a = str(input("Введите выражение: "))
print("-" * 150)
n = k = p = t = 0
string = str_der = ""
signs = "+-*/^()"
operations = ["sin", "cos", "tg", "ctg", "ln"]
der_signs = ["+", "-", "*", "/", "^", "sin", "cos", "tg", "ctg", "ln"]
d = e = ""
x_left = x_right = 0
fig, ax = plt.subplots()


def onpick(event):
    string_graph = ""
    x0 = event.xdata

    if x_left <= x0 <= x_right:
        derive = calc(d, x0)
        equation = calc(e, x0)

        if derive == "error" or equation == "error":
            print("-" * 150)
            return "Невозможно построить касательную"

        if x0 < 0:
            x0 = "(0" + str(x0) + ")"
        if derive < 0:
            derive = "(0" + str(derive) + ")"
        if equation < 0:
            equation = "(0" + str(equation) + ")"
        string_graph += str(derive) + "*(x-" + str(x0) + ")+" + str(equation)

        tangent_x = [x_left, x_right]
        tangent_y = [calc(OPN(string_graph)[0], tangent_x[0]), calc(OPN(string_graph)[0], tangent_x[1])]

        ax.plot(tangent_x, tangent_y)
        plt.draw()


def OPN(a):
    num = func = ""
    string_numbers = []
    string_symbol = []

    for i in range(0, len(a)):

        if a[i] in signs:
            if len(num) != 0:
                string_numbers.append(num)
                num = ""

            if len(func) != 0:
                string_symbol.append(func)
                string_numbers.append("(")
                func = ""

            if len(string_symbol) == 0 and len(string_numbers) == 0:
                string_symbol.append(a[i])

            elif len(string_symbol) == 0:
                string_numbers.append("(")
                string_symbol.append(a[i])

            elif a[i] == "(":
                string_symbol.append(a[i])

            elif a[i] == ")":
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(":
                        string_symbol.pop(k)
                        break
                    x = string_symbol.pop()
                    if x in der_signs:
                        string_numbers.append(")")
                    string_numbers.append(x)

            elif a[i] == "^":
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(*/+-":
                        string_symbol.append(a[i])
                        string_numbers.append("(")
                        break
                    else:
                        x = string_symbol.pop()
                        if x in der_signs:
                            string_numbers.append(")")
                        string_numbers.append(x)
                        if len(string_symbol) == 0:
                            string_symbol.append(a[i])

                    if k == 0:
                        string_numbers.append("(")

            elif a[i] == "*":
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(+-":
                        string_symbol.append(a[i])
                        string_numbers.append("(")
                        break
                    else:
                        x = string_symbol.pop()
                        if x in der_signs:
                            string_numbers.append(")")
                        string_numbers.append(x)
                        if len(string_symbol) == 0:
                            string_symbol.append(a[i])

                    if k == 0:
                        string_numbers.append("(")

            elif a[i] == "/":
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(+-":
                        string_symbol.append(a[i])
                        string_numbers.append("(")
                        break
                    else:
                        x = string_symbol.pop()
                        if x in der_signs:
                            string_numbers.append(")")
                        string_numbers.append(x)
                        if len(string_symbol) == 0:
                            string_symbol.append(a[i])

                    if k == 0:
                        string_numbers.append("(")

            elif a[i] == "+":
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(":
                        string_symbol.append(a[i])
                        string_numbers.append("(")
                        break
                    else:
                        x = string_symbol.pop()
                        if x in der_signs:
                            string_numbers.append(")")
                        string_numbers.append(x)
                        if len(string_symbol) == 0:
                            string_symbol.append(a[i])

                    if k == 0:
                        string_numbers.append("(")

            else:
                for k in range(len(string_symbol) - 1, -1, -1):
                    if string_symbol[k] in "(":
                        string_symbol.append(a[i])
                        string_numbers.append("(")
                        break
                    else:
                        x = string_symbol.pop()
                        if x in der_signs:
                            string_numbers.append(")")
                        string_numbers.append(x)
                        if len(string_symbol) == 0:
                            string_symbol.append(a[i])

                    if k == 0:
                        string_numbers.append("(")

        elif a[i] in [str(k) for k in range(0, 10)] or a[i] == "." or a[i] == "x":
            num += a[i]

        else:
            func += a[i]

    if len(num) != 0:
        string_numbers.append(num)

    for i in range(len(string_symbol) - 1, -1, -1):
        x = string_symbol.pop()
        if x in der_signs:
            string_numbers.append(")")
        string_numbers.append(x)

    for i in string_numbers:
        if i not in "()":
            string_symbol.append(i)

    return [string_symbol, string_numbers]


def back_OPN(a):
    str = []

    for i in range(0, len(a)):

        if a[i] in "+-*/^":
            y = str.pop()
            x = str.pop()
            str.append("(" + x + a[i] + y + ")")

        elif a[i] in "()":
            continue

        elif a[i] == "sin":
            str.append("sin(" + str.pop() + ")")

        elif a[i] == "cos":
            str.append("cos(" + str.pop() + ")")

        elif a[i] == "tg":
            str.append("tg(" + str.pop() + ")")

        elif a[i] == "ctg":
            str.append("ctg(" + str.pop() + ")")

        elif a[i] == "ln":
            str.append("ln(" + str.pop() + ")")

        else:
            str.append(a[i])

    return str[0]


def calc(term, m):
    string_symbol = []
    string_numbers = term[:]

    for i in range(0, len(string_numbers)):
        if string_numbers[i] == "x":
            string_numbers[i] = str(m)
        elif string_numbers[i] == "e":
            string_numbers[i] = str(2.718281828459045)

    for i in range(0, len(string_numbers)):

        if string_numbers[i] in signs:
            y = string_symbol.pop()
            x = string_symbol.pop()

            if string_numbers[i] == "^":
                string_symbol.append(x ** y)

            elif string_numbers[i] == "*":
                string_symbol.append(x * y)

            elif string_numbers[i] == "/":
                if y == 0:
                    print("ОШИБКА: Деление на ноль")
                    return "error"
                string_symbol.append(x / y)

            elif string_numbers[i] == "+":
                string_symbol.append(x + y)

            else:
                string_symbol.append(x - y)

        elif string_numbers[i] == "sin":
            string_symbol.append(math.sin(string_symbol.pop()))

        elif string_numbers[i] == "cos":
            string_symbol.append(math.cos(string_symbol.pop()))

        elif string_numbers[i] == "tg":
            x = string_symbol.pop()
            if math.cos(x) == 0:
                print("ОШИБКА: Тангенс не определён, так как косинус равен нулю")
                return "error"
            string_symbol.append(math.tan(x))

        elif string_numbers[i] == "ctg":
            x = string_symbol.pop()
            if math.sin(x) == 0:
                print("ОШИБКА: Котангенс не определён, так как синус равен нулю")
                return "error"
            string_symbol.append(math.cos(x) / math.sin(x))

        elif string_numbers[i] == "ln":
            x = string_symbol.pop()
            if x <= 0:
                print("ОШИБКА: Логарифм не определён, так как аргумент неположительный")
                return "error"
            string_symbol.append(math.log(x))

        else:
            string_symbol.append(float(string_numbers[i]))

    if key == 1:
        print("Ответ: ", string_symbol[0])
    return string_symbol[0]


def graph(a):
    global d, e, x_left, x_right

    left, right = map(float, input("Введите диапазон для x: ").split())
    print("-" * 150)

    derivative = der(a[1], str_der)

    print("Производная: ", derivative)
    print("-" * 150)

    points = np.linspace(left, right, 10000)

    x = []
    y = []
    for i in range(0, len(points)):
        n = calc(a[0], points[i])
        if isinstance(n, float):
            y.append(n)
            x.append(points[i])
    ax.plot(x, y)

    d = OPN(derivative)[0]
    e = a[0]
    x_left = x[0]
    x_right = x[len(x) - 1]

    h = max(y) - min(y)
    l = h / 100 * 20

    plt.ylim(min(y) - l, max(y) + l)

    plt.draw()


def der(s, str_der):
    num_left = num_right = ""
    array_left = []
    array_right = []

    if s[len(s) - 1] == ")" and s[0] == "(":
        s.pop()
        s.pop(0)

    for i in range(len(s) - 1, -1, -1):

        b = 0

        if s[i] in der_signs:
            flag = 0

            for k in range(i - 1, -1, -1):

                if s[k] == ")":
                    b += 1

                if (((s[k].isdigit() or s[k] == "x" or (s[k] in der_signs and s[k + 1] in der_signs))
                     and k != 0) or b > 0) and flag == 0:
                    array_right.append(s[k])
                else:
                    flag = 1
                    array_left.append(s[k])

                if s[k] == "(":
                    b -= 1

            array_left.reverse()
            array_right.reverse()

            if array_left:
                num_left = back_OPN(array_left)
            if array_right:
                num_right = back_OPN(array_right)

            if s[i] in "+-":
                str_der += "((" + der(array_left, str_der) + ")" + s[i] + "(" + der(array_right, str_der) + "))"

            elif s[i] == "*":
                str_der += ("((" + der(array_left, str_der) + ")*" + num_right + "+"
                            + num_left + "*(" + der(array_right, str_der) + "))")

            elif s[i] == "/":
                str_der += ("(((" + der(array_left, str_der) + ")*" + num_right + "-"
                            + num_left + "*(" + der(array_right, str_der) + "))/(" + num_right + "^2))")

            elif s[i] == "^":
                if num_right.isdigit():
                    str_der += "(" + num_right + "*" + num_left + "^(" + num_right + "-1)" + "*" + der(array_left, str_der) + ")"
                else:
                    str_der += ("((" + num_right + "*" + num_left + "^(" + num_right + "-1)" + "*" + der(array_left, str_der)
                            + ")+(" + num_left + "^" + num_right + "*ln(" + num_left + ")*" + der(array_right,
                                                                                                  str_der) + "))")

            elif s[i] == "sin":
                str_der += "(cos(" + num_right + ")*(" + der(array_right, str_der) + "))"

            elif s[i] == "cos":
                str_der += "((0-sin(" + num_right + "))*(" + der(array_right, str_der) + "))"

            elif s[i] == "tg":
                str_der += "((" + der(array_right, str_der) + ")/(cos(" + num_right + "))^2)"

            elif s[i] == "ctg":
                str_der += "(0-1)*((" + der(array_right, str_der) + ")/(sin(" + num_right + "))^2)"

            else:
                str_der += "((" + der(array_right, str_der) + ")/(" + num_right + "))"

            break

        elif s[i].isdigit():
            return "0"

        elif s[i] == "x":
            return "1"

    return str_der


for i in range(0, len(a)):
    if a[i] != " ":
        string += a[i]

if string[0] == "-":
    a = "0-"
    n = 1
else:
    a = ""

for i in range(n, len(string)):

    if i > 0 and string[i] == "x" and string[i - 1] in [str(k) for k in range(0, 10)]:
        a += "*"

    if string[i] == "(" and string[i + 1] == "-":
        a += "(0-"

    elif string[i - 1] == "(" and string[i] == "-":
        continue

    else:
        a += string[i]

string = a
a = ""

for i in range(0, len(string)):

    if string[i] == "^" and string[i + 1] == "(":
        p += 1

    if p > 0 and string[i] == "(":
        t += 1

    elif p > 0 and string[i] == ")":
        t -= 1
        if t == 0:
            p = 0

    if string[i] == "^":
        k += 1
        a += "^("

    elif string[i] in "*/+-" and string[i - 1] != str(0) and p == 0:
        a += ")" * k + string[i]
        k = 0

    else:
        a += string[i]

if k != 0:
    a += ")" * k

print("Обработанное выражение: ", a)
print("-" * 150)

opn = OPN(a)
print("Обратная польская нотация: ", opn[1])
print("-" * 150)

key = int(input("Введите 1 - вычислить выражение\n"
                "Введите 2 - вычислить производную\n"
                "------> "))
print("-" * 150)

if key == 1:
    m = float(input("Введите значение x: "))
    print("-" * 150)
    calc(opn[0], m)
else:
    graph(opn)

fig.canvas.mpl_connect('button_press_event', onpick)
plt.show()
