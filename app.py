from pandas import read_csv, read_excel
from matplotlib import pyplot as plt
from fpdf import FPDF
from matplotlib.backends.backend_pdf import PdfPages
import glob
import numpy as np
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
import io
from kivymd.uix.filemanager import MDFileManager

plt.rcParams.update({"figure.figsize": (12.0, 8.0)})
plt.rcParams.update({"font.size": 14})
Window.size = (1000, 700)
buf = io.StringIO()


class Data:
    def __init__(self):
        self.columns = []
        self.data = []
        self.value_counts_columns = dict()
        self.draw = []

    def read_file(self, path):
        file = path
        if "xlsx" in file[-3:]:
            self.data = read_excel(file)
            # self.table_pdf()
            return 0
        if "csv" in file[-3:]:
            self.data = read_csv(file)
            # self.table_pdf()
            return 0

    def select(self, X_columns=None, Y_columns=None, Z_columns=None):
        self.select_columns = []
        self.X = []
        self.Y = []
        self.Z = []
        if len(self.data) != 0:
            try:
                self.X = self.data[X_columns]
                try:
                    self.Y = self.data[Y_columns]
                except:
                    pass
            except:
                try:
                    self.Y = self.data[Y_columns]
                except:
                    return 0
            self.select_columns.append(X_columns)
            self.select_columns.append(Y_columns)
            if len(Z_columns) != 0:
                self.Z = self.data[Z_columns]
                self.select_columns.append(Z_columns)

    def get_info(self):
        self.columns = self.data.columns.tolist()
        for i in self.data:
            self.value_counts_columns[i] = self.data[i].value_counts()
        return f"{self.data.info(buf=buf)}"

    def plot_data(self):
        fig = plt.figure(figsize=plt.figaspect(0.5))
        if type(self.Z) != list and type(self.X) != list and type(self.Y) != list:
            plt.style.use("seaborn-notebook")
            ax = fig.add_subplot(1, 2, 1, projection="3d")
            ax.plot3D(self.X.values, self.Y.values, self.Z.values)
            ax.set_xlabel(f"x-{self.select_columns[0]}")
            ax.set_ylabel(f"y-{self.select_columns[1]}")
            ax.set_zlabel(f"z-{self.select_columns[2]}")
            ax.view_init(25, 11)
            ax = fig.add_subplot(1, 2, 2, projection="3d")
            fig = ax.scatter3D(
                self.X.values,
                self.Y.values,
                self.Z.values,
                c=self.Z.values,
                cmap="viridis",
                linewidth=0.5,
            )
            ax.set_xlabel(f"x-{self.select_columns[0]}")
            ax.set_ylabel(f"y-{self.select_columns[1]}")
            ax.set_zlabel(f"z-{self.select_columns[2]}")
            ax.view_init(25, 11)
            plt.savefig("image/3D.png")
            plt.show()
            return None

        if type(self.X) != list and type(self.Y) != list:
            plt.style.use("seaborn")
            ax = fig.add_subplot(1, 2, 1)
            ax.plot(self.X.values, self.Y.values)
            ax.set_xlabel(f"x-{self.select_columns[0]}")
            ax.set_ylabel(f"y-{self.select_columns[1]}")
            ax = fig.add_subplot(1, 2, 2)
            ax.scatter(self.X.values, self.Y.values)
            ax.set_xlabel(f"x-{self.select_columns[0]}")
            ax.set_ylabel(f"y-{self.select_columns[1]}")
            plt.savefig("image/1.png")
            plt.show()
            return None
        if type(self.X) != list:
            plt.style.use("seaborn")
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(self.X.values)
            ax.set_xlabel(f"NO-{self.select_columns[0]}")
            ax.set_ylabel(f"{self.select_columns[0]}")
            plt.savefig("image/2.png")
            plt.show()
            return None
        if type(self.Y) != list:
            plt.style.use("seaborn")
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(self.Y.values)
            ax.set_xlabel(f"NO-{self.select_columns[1]}")
            ax.set_ylabel(f"{self.select_columns[1]}")
            plt.savefig("image/3.png")
            plt.show()
            return None
        return 0

    def table_pdf(self):
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis("tight")
        ax.axis("off")
        the_table = ax.table(
            cellText=self.data.values[:50], colLabels=self.data.columns, loc="center"
        )
        pp = PdfPages("table.pdf")
        pp.savefig(fig, bbox_inches="tight")
        pp.close()


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # self.image('image/report.png', 10, 8, 33)
        self.set_font("Arial", "B", 11)
        self.ln(30)

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

    def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30)

    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)

    def read_images_in_folder(self):
        self.image_list = []
        for filename in glob.glob("image/*.png"):  # assuming gif
            self.image_list.append(filename)
        print(self.image_list)

    def add_image_to_page(self):
        my_list2 = [
            self.image_list[i : i + 3] for i in range(0, len(self.image_list), 3)
        ]
        for elem in my_list2:
            self.print_page(elem)


run = Data()


class First_screen(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


Builder.load_string(
    """

<First_screen>:
    name: 'screen1'
    BoxLayout:
        orientation: 'vertical'
        MDBottomAppBar:
            MDToolbar:
                title: "Data Analysis"
                icon: "keyboard-backspace"
                type: "bottom"
                mode: "end"
                
    BoxLayout:
        padding: dp(20)
        MDTextFieldRound:
            size_hint: (5, 0.06)
            id:inputPath
            hint_text: "path to file"
            pos_hint: {'center_x': .9, 'center_y': .95}
        MDFillRoundFlatButton:
            pos_hint: {'center_x': 10, 'center_y':10}
        MDFillRoundFlatButton:
            text: "Browse"
            pos_hint: {'center_x':0.9, 'center_y': .95}
            on_release: app.file_manager_open()

    BoxLayout:
        padding: dp(20)
        MDTextField:
            size_hint: (0.15,0)
            id:X
            hint_text: "X"
            pos_hint: {'center_x': .9, 'center_y': .85}
        MDTextField:
            size_hint: (0.15,0)
            id:Y
            hint_text: "Y"
            pos_hint: {'center_x': .9, 'center_y': .85}
        MDTextField:
            size_hint: (0.15,0)
            id:Z
            hint_text: "Z"
            pos_hint: {'center_x': .9, 'center_y': .85}
        MDTextField:
            size_hint: (0.04,0)
        MDCard:
            orientation: "vertical"
            padding: "8dp"
            size_hint: (0.5,0)
            size: "280dp", "280dp"
            pos_hint: {'center_x': .9, 'center_y': .63}
            
            MDLabel:
                text: "Informaition"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: self.texture_size[1]
                
            MDSeparator:
                height: "1dp"
            
            MDLabel:
                id:label_text
                
            
    BoxLayout:
        padding: dp(20)
        ScrollView:
            size_hint: (0.15, 0.45)
            pos_hint: {'center_x': .9, 'center_y': .606}
            MDList:
                id:box1
        ScrollView:
            size_hint: (0.15, 0.45)
            pos_hint: {'center_x': .9, 'center_y': .606}
            MDList:
                id:box2
        ScrollView:
            size_hint: (0.15, 0.45)
            pos_hint: {'center_x': .9, 'center_y': .606}
            MDList:
                id:box3
        MDTextField:
            size_hint: (0.04,0)
        ScrollView:
            size_hint: (0.5, 0.4)
            pos_hint: {'center_x': .9, 'center_y': .63}
            MDList:
                id:box
    BoxLayout:      
        MDRoundFlatIconButton:
            text: "Read File"
            pos_hint: {'center_x':0.3, 'center_y': .3}
            on_release: app.read_file_path()
            
        MDRoundFlatIconButton:
            text: "select columns"
            pos_hint: {'center_x': .6, 'center_y': .3}
            on_release: app.set_columns()
        
        MDRoundFlatIconButton:
            text: "Draw"
            pos_hint: {'center_x': .5, 'center_y': .3}
            on_release: app.draw_data()
            
        MDRoundFlatIconButton:
            text: "Save Pdf"
            pos_hint: {'center_x': .5, 'center_y': .3}
            on_release: app.save_pdf()
        
    MDNavigationDrawer:
        id: nav_drawer
           
"""
)


class Main_app(MDApp):
    sm = ScreenManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.X_in = ""
        self.Y_in = ""
        self.Z_in = ""
        Window.bind(on_keyboard=self.events)
        self.manager_open = False

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # previous=True,
        )
        self.file_manager.use_access = True
        self.file_manager.ext = [".csv", ".xlsx"]

    def build(self):
        self.sm.add_widget(First_screen(name="screen1"))
        return self.sm

    def file_manager_open(self):
        self.file_manager.show(r"./")  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        c = self.sm.get_screen("screen1").ids.inputPath
        c.text = path
        run.read_file(path)
        self.read_file_button()

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device.."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def read_file_button(self):
        box1 = self.sm.get_screen("screen1").ids.box1
        box2 = self.sm.get_screen("screen1").ids.box2
        box3 = self.sm.get_screen("screen1").ids.box3
        label = self.sm.get_screen("screen1").ids.label_text
        run.get_info()
        s = buf.getvalue()
        columns = run.columns
        for box in zip([box1, box2, box3], ["x", "y", "z"]):
            for column in columns:
                box[0].add_widget(
                    OneLineListItem(
                        text=f"{column} {box[1]}",
                        on_release=self.set_columns_selcet_from_gui,
                    )
                )
        label.text = f"""The columns in file {run.columns} number columns is {len(run.columns)} , Row in Data {run.data.shape[0]}"""

    def set_columns_selcet_from_gui(self, onelinelistitem):
        text = onelinelistitem.text
        if "x" in text[-1]:
            X = self.sm.get_screen("screen1").ids.X
            X.text = text[:-2]
            self.X_in = text[:-2]
        elif "y" in text[-1]:
            Y = self.sm.get_screen("screen1").ids.Y
            Y.text = text[:-2]
            self.Y_in = text[:-2]
        elif "z" in text[-1]:
            Z = self.sm.get_screen("screen1").ids.Z
            Z.text = text[:-2]
            self.Z_in = text[:-2]

    def set_columns(self):
        print(self.X_in, self.Y_in, self.Z_in)
        run.select(self.X_in, self.Y_in, self.Z_in)

    def draw_data(self):
        self.X_in = ""
        self.Y_in = ""
        self.Z_in = ""
        X = self.sm.get_screen("screen1").ids.X
        X.text = ""
        Y = self.sm.get_screen("screen1").ids.Y
        Y.text = ""
        Z = self.sm.get_screen("screen1").ids.Z
        Z.text = ""
        run.plot_data()

    def save_pdf(self):
        pdf = PDF()
        pdf.read_images_in_folder()
        pdf.add_image_to_page()
        pdf.output("Repot.pdf", "F")

    def read_file_path(self):
        c = self.sm.get_screen("screen1").ids.inputPath
        path = c.text
        try:
            run.read_file(path)
            self.read_file_button()
        except:
            pass


def Main():
    Main_app().run()


Main()
