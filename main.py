from tkinter import Tk, PhotoImage, Canvas, Label
from random import randint
from time import perf_counter

window = Tk()


class Elements:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


class Fire(Elements):
    img = PhotoImage(file="fire.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Glina):
            return Pottery()
        elif isinstance(other, Water):
            return Aroma()
        elif isinstance(other, Wind):
            return Cold()
        elif isinstance(other, Dust):
            return Magma()


class Water(Elements):
    img = PhotoImage(file="water.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Fire):
            return Aroma()
        elif isinstance(other, Earth):
            return Glina()
        elif isinstance(other, Cold):
            return Ice()      
        elif isinstance(other, Cloud):
            return Rain()
        elif isinstance(other, HotWind):
            return Tornado()
        elif isinstance(other, Time):
            return Bacteria()


class Wind(Elements):
    img = PhotoImage(file="wind.png").subsample(4, 4)
    def __add__(self, other):
        if isinstance(other, Earth):
            return Dust()
        elif isinstance(other, Fire):
            return Cold()
        elif isinstance(other, Hot):
            return HotWind()


class Earth(Elements):
    img = PhotoImage(file="ground.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Wind):
            return Dust()
        elif isinstance(other, Water):
            return Glina()
        elif isinstance(other, Bacteria):
            return Plant()


class Pottery(Elements):
    img = PhotoImage(file="pottery.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Plant):
            return PottedPlant()

class Aroma(Elements):
    img = PhotoImage(file="aroma.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Cold):
            return Cloud()


class Plant(Elements):
    img = PhotoImage(file="plant.png")

    def __add__(self, other):
        if isinstance(other, Pottery):
            return PottedPlant()
        elif isinstance(other, Time):
            return Tree()


class Cold(Elements):
    img = PhotoImage(file="cold.png")

    def __add__(self, other):
        if isinstance(other, Water):
            return Ice()
        elif isinstance(other, Aroma):
            return Cloud()
        elif isinstance(other, Rain):
            return Snow()
        elif isinstance(other, Magma):
            return Hot()


class Cloud(Elements):
    img = PhotoImage(file="cloud.png")

    def __add__(self, other):
        if isinstance(other, Water):
            return Rain()


class Rain(Elements):
    img = PhotoImage(file="rain.png")

    def __add__(self, other):
        if isinstance(other, Cold):
            return Snow()

class Dust(Elements):
    img = PhotoImage(file="dust.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Fire):
            return Magma()


class Magma(Elements):
    img = PhotoImage(file="magma.png").subsample(3, 3)

    def __add__(self, other):
        if isinstance(other, Cold):
            return Hot()
        if isinstance(other, Wind):
            return HotWind()


class Hot(Elements):
    img = PhotoImage(file="hot.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Wind):
            return HotWind()


class HotWind(Elements):
    img = PhotoImage(file="hot_wind.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Water):
            return Tornado()


class Time(Elements):
    img = PhotoImage(file="time.png").subsample(10, 10)

    def __add__(self, other):
        if isinstance(other, Plant):
            return Tree()
        elif isinstance(other, Water):
            return Bacteria()


class Bacteria(Elements):
    img = PhotoImage(file="bacteria.png").subsample(4, 4)

    def __add__(self, other):
        if isinstance(other, Earth):
            return Plant()


class PottedPlant(Elements):
    img = PhotoImage(file="potted_plant.png")

class Snow(Elements):
    img = PhotoImage(file="snow.png")

class Ice(Elements):
    img = PhotoImage(file="ice.png")

class Tornado(Elements):
    img = PhotoImage(file="tornado.png").subsample(4, 4)

class Tree(Elements):
    img = PhotoImage(file="tree.png")

class Glina(Elements):
    img = PhotoImage(file="glina.png").subsample(2, 2)


class Main:
    WIDTH = 700
    HEIGHT = 550

    def __init__(self, window):

        window.title("The Alchemist")
        window.geometry("{}x{}+410+150".format(self.WIDTH, self.HEIGHT))
        window.resizable(False, False)
        window.wm_iconbitmap("icon.ico")

        self.start = perf_counter()
        self.canvas = Canvas(window, width=self.WIDTH, height=self.HEIGHT, bd=0)
        self.canvas.pack()

        self.elements = [Fire(), Earth(), Water(), Wind()]

        for el in self.elements:
            img = self.canvas.create_image(
                randint(50, self.WIDTH), 
                randint(50, self.HEIGHT), 
                image=el.img
            )

        window.bind("<B1-Motion>", self.move)

        self.label = Label(self.canvas, 
            text=f'{len(self.elements)}/22',
            bg='lime', font=('Arial', 20)
        );  self.label.place(x=0, y=0)


    def move(self, event):

        img_id = self.canvas.find_overlapping(
            event.x, event.y, 
            event.x + 10, event.y + 10
        )
        # print(img_id)
        if len(img_id) > 1:
            el_id1, el_id2 = img_id[0], img_id[1]
            el1 = self.elements[el_id1 - 1]
            el2 = self.elements[el_id2 - 1]

            new_el = el1 + el2

            if new_el:
                if new_el not in self.elements:
                    self.canvas.create_image(event.x, event.y, image=new_el.img)
                    self.elements.append(new_el)
                    self.label['text'] = f'{len(self.elements)}/22'

        self.canvas.coords(img_id, event.x, event.y)

        end = perf_counter() - self.start
        print(f'{end: 0.2f} сек.')
        if Time() not in self.elements and 120.0 <= end:
            self.time_event()

    def time_event(self):
        from tkinter.messagebox import showinfo
        self.canvas.create_image(620, 75, image=Time.img)
        self.elements.append(Time())
        showinfo(
            "Достижение!",
            "Поздравляю, вы пробыли в игре больше 2 минут.\nВы открыли элемент 'Время'!"
        )


if __name__ == "__main__":
    
    main = Main(window)

    window.mainloop()
