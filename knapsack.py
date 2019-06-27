import time
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MyPaintWidget(Widget):

    def add_item(self, x, y, txt='', color=[1, 1, 1, 1]):
        if x > 200 or y > 100:
            with self.canvas:
                Color(*color, mode='hsv')
                Button(pos=(x, y), size=(100, 50),
                       text=txt, background_color=color)


class MyKnapSackApp(App):
    x, y = 0, 450
    W = []
    V = []

    def build(self):
        self.parent = Widget()

        self.painter = MyPaintWidget()

        # Buttons
        runbtn = Button(text='run', pos=(0, 0), size=(200, 100))
        runbtn.bind(on_release=self.run_knapsack)
        inputbtn = Button(text='input', pos=(0, 500), size=(200, 50))
        inputbtn.bind(on_release=self.add_item)

        # Text Input
        self.txtI = TextInput(text='value', multiline=False, pos=(0, 550),
                              font_size=30, size=(100, 50))
        self.txtW = TextInput(text='weight', multiline=False, pos=(100, 550),
                              font_size=30, size=(100, 50))
        self.txtCapacity = TextInput(text='capacity', multiline=False,
                                     pos=(0, 100), font_size=30,
                                     size=(200, 50))

        # Add widgets
        self.parent.add_widget(runbtn)
        self.parent.add_widget(inputbtn)
        self.parent.add_widget(self.painter)
        self.parent.add_widget(self.txtI)
        self.parent.add_widget(self.txtW)
        self.parent.add_widget(self.txtCapacity)

        return self.parent

    def add_item(self, btn):
        if self.x <= 100:
            self.V.append(int(self.txtI.text))
            self.W.append(int(self.txtW.text))
            color = (random(), 1, 1)
            self.painter.add_item(self.x, self.y, (self.txtI.text)
                                  + ' : ' + (self.txtW.text), color)

            self.txtI.text = ''
            self.txtW.text = ''

            self.y -= 50
            if self.y < 150:
                self.x += 100
                self.y = 450

    def knapsack(self, W, wt, val, n):
        K = [[0 for x in range(W+1)] for x in range(n+1)]
        # Build table K[][] in bottom up manner
        x, y = 200, 550
        for i in range(n+1):
            for w in range(W+1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif wt[i-1] <= w:
                    K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
                else:
                    K[i][w] = K[i-1][w]
                self.parent.add_widget(Button(pos=(x, y), size=(50, 50),
                                       text=str(K[i][w]),
                                       background_color=[random(), random(),
                                       random(), 1]))
                x += 50
            y -= 50
            x = 200

        return K[n][W]

    def run_knapsack(self, obj):
        w = int(self.txtCapacity.text)
        self.txtCapacity.text = ''
        self.knapsack(w, self.W, self.V, len(self.V))


if __name__ == '__main__':
    MyKnapSackApp().run()
