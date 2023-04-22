from PyQt5.QtCore import Qt#імпортуємо потрібні бібліотеки
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5 import QtGui
from PIL import Image, ImageFilter
import os


app = QApplication([])# створюємо додаток
window = QWidget()#створюємо вікно додатку
window.resize(1420, 820)#задаємо розмір вікна
window.setWindowTitle("Easy editor")#задаємо назву(заголовок) вікна
window.setWindowIcon(QtGui.QIcon('original.jpg'))

"""ІНТЕРФЕЙС ПРОГРАМИ"""
btn_folder = QPushButton("Папка")#створюємо кнопку з назвою
list_files = QListWidget()# створюємо місце, де будуть відображатися вибрані файли

main_label = QLabel("Зображення")#створюємо напис 

btn_left = QPushButton("Вліво")#створюємо кнопку "вліво"
btn_right = QPushButton("Вправо")# створюємо кнопку "Вправо"
btn_mirror = QPushButton("Дзеркало")#створюємо кнопку "Дзеркало"
btn_sharp = QPushButton("Різкість")# стаорюємо кнопку "Різкість"
btn_bw = QPushButton("Ч/Б")# створюємо кнопку "Ч.Б"

col1 = QVBoxLayout()#створюємо вертикальну лінію
col1.addWidget(btn_folder)#додаємо на лініюкнопку "Папка"
col1.addWidget(list_files)#додаємо на лінію місце відображення вибраних папок

col2 = QVBoxLayout()#стоврюємо вертикальну лінію
col2.addWidget(main_label)#додаємо на лінію напис "Зображення"

row1 = QHBoxLayout()#створюємо горизонтальну лінію
row1.addWidget(btn_left)#додаємо на лінію кнопки :"вліво"
row1.addWidget(btn_right)#"вправо"
row1.addWidget(btn_mirror)#"дзеркало"
row1.addWidget(btn_sharp)#"різкість"
row1.addWidget(btn_bw)#"Ч\б"

col2.addLayout(row1)#додаємо горизонтальну лінію на вертикальну

main_layout = QHBoxLayout()#створємо горизонтальну лінію

main_layout.addLayout(col1, 20)#додаємо всі лінії до головної та задаємо співвідношення
main_layout.addLayout(col2, 80)

window.setLayout(main_layout)
window.show()#показуємо вікно

"""ФУНКЦІОНАЛ ПРОГРАМИ"""
workdir = ''#створюємо нашу робочу директорію


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()#повертає шлях до нашої робочої папки


def filter(files, extensions):#функція для відбору лише зображень 
    result = []#пустий список
    for filename in files:#проходимося по списку з фалами
        for ext in extensions:#проходимося по списку з закінченнями папок
            if filename.endswith(ext):#перевіряємо чи файл містить один з даних форматів
                result.append(filename)#додаємо папку в робочу директорію
    return result#повертаємо список


def showFileNameslist():#створюємо функцію зі правильними закінченнями
    extensions = ['.jpg', '.png', '.jpeg', '.bmp', '.gif']# список з закінченнями папок
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)#зберігаємо назви файлів картинок
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

class ImageProcesor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def load_image(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def show_image(self,path):
        main_label.hide()
        pixmapimage = QtGui.QPixmap(path)
        w,h = main_label.width(), main_label.height() 
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        main_label.setPixmap(pixmapimage)
        main_label.show()

    def saveImage(self):  # збереження картинки в папку
        path = os.path.join(workdir, self.save_dir)#шлях до папки Modified
        if not (os.path.exists(path) or os.path.isdir(path)):#якщо папка не створена з  такм імям
            os.mkdir(path)#створює папку за поданим шляхом
        fullname = os.path.join(path, self.filename)#збираємо повний шлях до картинки у новій папці
        self.image.save(fullname)#зберігаємо картинку в папку за повним імям

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)


workimage = ImageProcesor()


def show_choosen_image():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.load_image(workdir,filename)
        image_path = os.path.join(workdir,filename)
        workimage.show_image(image_path)


btn_folder.clicked.connect(showFileNameslist) 
list_files.currentRowChanged.connect(show_choosen_image)

btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_bw.clicked.connect(workimage.do_bw)





app.exec_()
