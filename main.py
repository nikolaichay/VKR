from tkinter import *
import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import tasks as MyTs
from functools import partial
from PIL import Image, ImageTk
ss = MyTs.ss
ss1 = MyTs.ss1

s1 = "3914.2 15.2 0.252 1.29 0.555 140"
s2 = "5405.3 15.2 0.252 1.314 0.555 140"
s3 ="23500 50 4250 0.351 1.82 1.0 90"
date = [3914.2, 15.2, 0.252, 1.29, 0.555, 140]

class TextInputWindow:
    def __init__(self, master,MyFunc,i):
        self.master = master
        self.window = Toplevel(master)  
        self.window.title("Задание " + str(i))
        self.window.geometry("800x800")
        self.func = MyFunc
        self.string = ss[i-1]
        self.string_Start = ss1[i-1]
        self.fileName ="task"+str(i)+".txt"
        self.path = "image/task"+str(i)+".png"
        self.data_options = [s1,s2,s3]
        self.path_formula = "formula"+str(i)+".txt"
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)



    def create_widgets(self):
        self.scrollable_frame = tk.Frame(self.window)
        self.scrollable_frame.pack(fill='both', expand=True)

        # Создаем канвас и ассоциируем его с контейнером
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Добавляем полосу прокрутки к канвасу
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        # Конфигурируем канвас
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Создаем другой фрейм внутри канваса для размещения других виджетов
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)

        image_path = self.path
        try:
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.LANCZOS)  # Изменяем размер картинки, если необходимо
            photo = ImageTk.PhotoImage(image)
            tk.Label(self.inner_frame, image=photo).pack()
            self.image_label = tk.Label(self.inner_frame, image=photo)
            self.image_label.image = photo
        except FileNotFoundError:
            print(f"Файл {image_path} не найден.")
        tk.Label(self.inner_frame, text="Условие задачи").pack()
        self.text_display_con = Text(self.inner_frame, height=5, width=50, wrap=WORD)
        self.text_display_con.insert(tk.END, self.string)
        self.text_display_con.config(state=tk.DISABLED)
        self.text_display_con.pack()

        tk.Label(self.inner_frame, text="Начальные данные").pack()
        self.text_display_start = Text(self.inner_frame, height=7, width=20, wrap=WORD)
        self.text_display_start.insert(tk.END, self.string_Start)
        self.text_display_start.pack()


        tk.Label(self.inner_frame, text="Введите начальные данные").pack()
        self.text_entry = tk.Entry(self.inner_frame,width=50)
        self.text_entry.pack()
        
        tk.Label(self.inner_frame, text="Выберите вариант начальных данных:").pack()
        self.data_listbox = tk.Listbox(self.inner_frame, selectmode=tk.SINGLE, height=len(self.data_options), width=50)
        for option in self.data_options:
            self.data_listbox.insert(tk.END, option)
        self.data_listbox.pack()

        formula_button = tk.Button(self.inner_frame, text="Показать формулу", command=lambda: self.show_formula(self.get_formula()))
        formula_button.pack()


        graph_button = tk.Button(self.inner_frame, text="Показать график", command=self.show_graph)
        graph_button.pack()

        save_button = tk.Button(self.inner_frame, text="Сохранить данные", command=lambda:self.write_to_file())
        save_button.pack()
        tk.Label(self.inner_frame, text="Введите ответ:").pack()
        self.text_entry_answer = tk.Entry(self.inner_frame)
        self.text_entry_answer.pack()
        submit_button = tk.Button(self.inner_frame, text="Отправить", command=self.submit_text)
        submit_button.pack()

    def on_mousewheel(self, event):
        # В Windows и MacOS дельта прокрутки работает по-разному
        # В Windows значение event.delta обычно 120 или -120
        # В MacOS значение event.delta обычно 1 или -1
        # Вы можете настроить множитель для изменения скорости прокрутки
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def write_to_file(self):
        strMy = self.text_entry.get()
        selected_data = self.data_listbox.get(self.data_listbox.curselection())
        if strMy: # Проверяем, что строка не пуста
            with open(self.fileName, 'w') as file:
                file.write(strMy)
        elif selected_data:
            with open(self.fileName, 'w') as file:
                file.write(selected_data)
        else:
            messagebox.showwarning("Предупреждение", "Текстовое поле пусто. Введите данные.")

    def show_formula(self, formula):
        # Отображаем переданную формулу
        messagebox.showinfo("Формула", formula)
    def get_formula(self):
        with open(self.path_formula, 'r') as file:
            str_f = file.read()
        return str_f
    
    def show_graph(self):
    # Создаем новое окно для графика
        graph_window = Toplevel(self.master)
        graph_window.title("График")

        num_arrays = 10
        # Массив массивов
        arrays = []

        # Создаем массивы, изменяя i-й элемент
        for i in range(num_arrays):
            new_array = np.copy(date)
            # Изменяем элемент с индексом i
            new_array[0] += i*10
            arrays.append(new_array)

        fig = Figure(figsize=(5, 4), dpi=100)
        arr = arrays[0]
        res = []
        first_values = [array[0] for array in arrays]
        for i in range(num_arrays):
            res.append(MyTs.task1(*arrays[i]))

        ax = fig.add_subplot(111)
        # ax.plot(first_values, res)
        ax.bar(first_values, res)
        ax.set_xlabel('Внешние силы')  # Подпись для оси X
        ax.set_ylabel('Долговечность в часах')  # Подпись для оси Y
        ax.set_title('Связь между долговечностью и внешними силами')  # Заголовок графика

        canvas = FigureCanvasTkAgg(fig, master=graph_window)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def submit_text(self):
        user_answer = float(self.text_entry_answer.get())
        correct_answer= (self.func())
        if (abs(user_answer - correct_answer)<=0.01):
            messagebox.showinfo("Правильный ответ", "Ответ верный!")
            self.window.destroy()
            self.master.deiconify()
        else:
            messagebox.showerror("Неправильный ответ", "Ответ неверный. Попробуйте еще раз.")
        
    

    def on_close(self):
        self.master.deiconify()
        self.window.destroy()

i_r= [1,2,3]
Func = [MyTs.task1To,MyTs.task2To,MyTs.task3To]
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Расчет долговечности подшибников ступиц колес АТС")
        self.master.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        self.text_display = Text(self.master, height=15, width=30,wrap=WORD)
        self.text_display.pack()
        str1 = "Представлены 3 задания. \nЗадание 1 о расчете долговечности конических роликовых подшипников ступицы колеса.\nЗадание 2 о расчете долговечности двухрядного шарикового радиально-упорного подшипника ступицы колеса.\nЗадание 3 о расчете максимального значения нагрузок на подшипники ступицы  колеса.\n "
        self.text_display.insert(tk.END, str1)  # Здесь вы можете вставить начальный текст
        self.text_display.config(state=tk.DISABLED)
        for i in i_r:
            j = len(i_r) - i + 1
            textMy = "Задание " + str(j)
            text_input_button = tk.Button(self.master, text=textMy, command=partial(self.open_text_input_window,j))
            text_input_button.pack(side=BOTTOM, anchor=W, padx=5, pady=5)
        

    def open_text_input_window(self,i):
        mf = Func[i-1]
        TextInputWindow(self.master, mf, i)
        self.master.withdraw()



def Main():
    print(Func[0]())
    print(Func[1]())
    print(Func[2]())
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    Main()