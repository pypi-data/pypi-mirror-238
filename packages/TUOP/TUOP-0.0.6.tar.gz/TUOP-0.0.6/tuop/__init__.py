import tkinter as tk
from random import choice
from time import sleep
from itertools import permutations


class triangle (): #рисует треугольник серпинского
    def __init__(self, iterations = 3000, firstDots = [(50, 550), (550, 550), (250, 50)], geometry="600x600"):
        self.draw(iterations, geometry, firstDots)

    def create_circle(self, x, y, my_canvas, r=1):
        x0 = x-r
        y0 = y-r
        y1 = y+r
        x1 = x+r
        return my_canvas.create_oval(x0, y0, x1, y1, fill="red", outline="black")

    def draw(self, iterations, geometry, firstDots):
        self.window = tk.Tk()
        self.window.title("треугольник Серпинского")
        self.window.geometry(geometry)

        text = tk.StringVar()
        label = tk.Label(textvariable=text)
        label.pack()
        self.canvas = tk.Canvas(bg="white", width=1000, height=1000)
        self.canvas.pack(expand=1, anchor=tk.CENTER)
        canvas = self.canvas

        for i in firstDots:
            self.create_circle(i[0], i[1], canvas)

        nextDot = [(firstDots[0][0]+firstDots[2][0])//2, (firstDots[0][1]+firstDots[2][1])//2]
        self.create_circle(nextDot[0], nextDot[1], canvas)

        for i in range(iterations):
            lastDot = nextDot
            dot = choice(firstDots)
            nextDot = [(lastDot[0]+dot[0])//2, (lastDot[1]+dot[1])//2]
            self.create_circle(nextDot[0], nextDot[1], canvas)
            self.window.update()
            sleep(0.001)
        self.window.title("треугольник Серпинского (Готово!)")
        text.set("Готово")

        self.window.mainloop()


def ege1(graph, matrix): #первое задание егэ
    res=[]
    for p in permutations(graph):
        mymatrix = ""
        for x in p:
            for y in p:
                if y in graph[x]:
                    mymatrix+="w"
                else:
                    mymatrix+="."
        if matrix == mymatrix:
            res.append(p)
    return res


if __name__ == "__main__":
    pass
