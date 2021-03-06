from rnd import *
from plabel import PLable
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton

class Login(QWidget):

    rgsSignal = pyqtSignal()    # 跳转至注册界面的信号
    statSignal = pyqtSignal(str)    # 更新面板状态栏的信号
    sendSignal = pyqtSignal(dict)   # 向服务器发送数据的信号
    cfSignal = pyqtSignal(str) # 跳转至主界面的信号

    def __init__(self):
        super().__init__()

        self.initUI()
        #t2 = Thread(target=self.startservice, args=(q, ))
        #t2.start()

    # 绘制图形界面
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        # 用户名输入
        lbu = QLabel('用户名：', self)
        self.ur = QLineEdit(self)
        grid.addWidget(lbu, 1, 0, 1, 2)
        grid.addWidget(self.ur, 1, 1, 1, 2)

        # 密码输入
        lbp = QLabel('密码：', self)
        self.pw = QLineEdit(self)
        self.pw.setEchoMode(QLineEdit.Password)
        grid.addWidget(lbp, 2, 0, 1, 1)
        grid.addWidget(self.pw, 2, 1, 1, 2)

        # 验证码输入
        lbrn = QLabel('请输入验证码：', self)
        self.irn = QLineEdit(self)
        self.lbrnp = PLable()
        self.rnd = get_rnd(30, 60)  # 获取验证码
        pic = QPixmap('code.png')
        self.lbrnp.setPixmap(pic)
        grid.addWidget(lbrn, 3, 0, 1, 1)
        grid.addWidget(self.irn, 3, 1, 1, 1)
        grid.addWidget(self.lbrnp, 3, 2, 1, 1)
        self.lbrnp.clicked.connect(self.change_rnd)

        # 登录按钮
        bt1 = QPushButton('登录')
        grid.addWidget(bt1, 4, 2)
        bt1.clicked.connect(self.send)

        # 注册账号
        bt2 = QPushButton('注册账号')
        grid.addWidget(bt2, 4, 1)
        bt2.clicked.connect(self.go_rgs)

        # 设置布局
        self.setLayout(grid)
        # self.resize(400, 300)
        # self.setWindowTitle('登录')
        # self.show()

    # 当用户点击或登录报错时更换验证码
    def change_rnd(self):
        self.irn.clear()
        self.rnd = get_rnd(30, 60)
        pic = QPixmap('code.png')
        self.lbrnp.setPixmap(pic)

    # 将用户名与密码发送至服务器端
    def send(self):
        # 将用户输入的验证码转为小写
        urn = self.irn.text().lower()
        if self.rnd == urn:
            ur = self.ur.text()
            pw = self.pw.text()
            data = {'type': 'lg', 'cnt': {'ur': ur, 'pw': pw}}  # 定义传输数据结构
            self.sendSignal.emit(data)
        else:
            self.statSignal.emit('验证码错误！')
            self.irn.clear()

    # 跳转至注册页面
    def go_rgs(self):
        self.close()
        self.rgsSignal.emit()

    # 根据从服务器返回的结果执行相应操作
    def result(self, rs):
        if rs:  # 如果登录成功
            ur = self.ur.text()
            self.cfSignal.emit(ur)    # 发送跳转至主界面的信号
        else:
            self.ur.clear()
            self.pw.clear()
            self.change_rnd()