from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import requests
import sys

class ContactBook(QWidget):
    def __init__(self):
        super().__init__()
        self.api_url = 'http://127.0.0.1:5000/contacts'# 后端 API 地址
        self.initUI()# 初始化界面
        self.loadContacts()# 加载联系人

    def initUI(self):
        self.setWindowTitle('通讯录') # 设置窗口标题
        self.setGeometry(100, 100, 400, 400)# 设置窗口位置和大小
        self.setStyleSheet("background-color: #f7f7f7;")# 设置背景颜色
        layout = QVBoxLayout()# 创建垂直布局

        # 联系人列表
        self.contact_list = QListWidget() # 创建联系人列表控件
        self.contact_list.setStyleSheet("font-size: 17px; background-color: #ffffff;")# 设置列表样式
        layout.addWidget(self.contact_list)# 将列表添加到布局中

        # 查找联系人界面
        search_layout = QHBoxLayout() # 创建水平布局
        self.search_input = QLineEdit() # 创建输入框
        self.search_input.setPlaceholderText("输入姓名查找...") # 设置占位符
        search_button = QPushButton('查找') # 创建查找按钮
        search_button.setStyleSheet("background-color: #FCF8FD;") # 设置按钮样式
        search_button.clicked.connect(self.search_contact) # 连接点击事件到查找方法
        search_layout.addWidget(QLabel('查找姓名:')) # 添加标签
        search_layout.addWidget(self.search_input) # 添加输入框
        search_layout.addWidget(search_button) # 添加按钮
        layout.addLayout(search_layout) # 将查找布局添加到主布局中

        # 添加联系人界面
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("姓名")
        self.phone_input = QLineEdit() # 创建电话输入框
        self.phone_input.setPlaceholderText("电话")
        add_button = QPushButton('添加')
        add_button.setStyleSheet("background-color: #FCF8FD;")
        add_button.clicked.connect(self.add_contact)  # 连接点击事件到添加方法
        add_layout.addWidget(QLabel('姓名:'))
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(QLabel('电话:'))
        add_layout.addWidget(self.phone_input)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)

        # 修改联系人界面
        modify_layout = QHBoxLayout()
        self.modify_name_input = QLineEdit()
        self.modify_name_input.setPlaceholderText("姓名")
        self.modify_phone_input = QLineEdit()
        self.modify_phone_input.setPlaceholderText("电话")
        modify_button = QPushButton('修改')
        modify_button.setStyleSheet("background-color: #FCF8FD;")
        modify_button.clicked.connect(self.modify_contact) # 连接点击事件到修改方法
        modify_layout.addWidget(QLabel('姓名:'))
        modify_layout.addWidget(self.modify_name_input)
        modify_layout.addWidget(QLabel('电话:'))
        modify_layout.addWidget(self.modify_phone_input)
        modify_layout.addWidget(modify_button)
        layout.addLayout(modify_layout)

        # 删除联系人界面
        delete_layout = QHBoxLayout()
        delete_button = QPushButton('删除')
        delete_button.setStyleSheet("background-color: #FCF8FD;")
        delete_button.clicked.connect(self.delete_contact) # 连接点击事件到删除方法
        delete_layout.addWidget(delete_button)
        layout.addLayout(delete_layout)

        self.contact_list.selectionModel().selectionChanged.connect(self.onSelectionChanged) # 连接选择变化信号
        self.setLayout(layout)# 设置主布局

        # 设置字体
        font = QFont("仿宋", 10) # 创建字体对象
        self.setFont(font) # 设置字体

    def loadContacts(self):
        response = requests.get(self.api_url)# 从后端获取联系人
        if response.status_code == 200:
            self.contact_list.clear() # 清空列表
            for contact in response.json(): # 遍历获取的联系人
                item = QListWidgetItem(f'{contact["name"]} - {contact["phone"]}')# 创建列表项
                item.setData(1, contact["id"])  # 存储联系人 ID
                self.contact_list.addItem(item) # 添加到列表

    def search_contact(self):
        name = self.search_input.text() # 获取输入的姓名
        if name:
            response = requests.get(f'{self.api_url}/search', params={'name': name}) # 查询联系人
            if response.status_code == 200:
                self.contact_list.clear() # 清空列表
                for contact in response.json(): # 遍历查询结果
                    item = QListWidgetItem(f'{contact["name"]} - {contact["phone"]}')# 创建列表项
                    item.setData(1, contact["id"])  # 存储联系人 ID
                    self.contact_list.addItem(item)  # 添加到列表

    def add_contact(self):
        name = self.name_input.text() # 获取姓名输入
        phone = self.phone_input.text() # 获取电话输入
        if name and phone:
            response = requests.post(self.api_url, json={'name': name, 'phone': phone})# 添加联系人
            if response.status_code == 200:
                self.loadContacts()# 重新加载联系人
                self.name_input.clear()# 清空输入框
                self.phone_input.clear()# 清空输入框

    def onSelectionChanged(self, selected, deselected):
        if selected.indexes():# 如果有选中项
            index = selected.indexes()[0]  # 获取选中项的索引
            item_text = self.contact_list.item(index.row()).text() # 获取选中项文本
            parts = item_text.split(' - ') # 分割姓名和电话
            if len(parts) > 1:
                self.modify_name_input.setText(parts[0]) # 设置修改姓名输入框
                self.modify_phone_input.setText(parts[1]) # 设置修改电话输入框

    def modify_contact(self):
        selected_item = self.contact_list.currentItem() # 获取当前选中项
        if selected_item:
            contact_id = selected_item.data(1) # 获取联系人 ID
            name = self.modify_name_input.text()# 获取修改后的姓名
            phone = self.modify_phone_input.text()# 获取修改后的电话
            if name and phone:
                response = requests.put(f'{self.api_url}/{contact_id}', json={'name': name, 'phone': phone})# 修改联系人
                if response.status_code == 200:
                    self.loadContacts() # 重新加载联系人

    def delete_contact(self):
        selected_item = self.contact_list.currentItem()# 获取当前选中项
        if selected_item:
            contact_id = selected_item.data(1) # 获取联系人 ID
            response = requests.delete(f'{self.api_url}/{contact_id}')# 删除联系人
            if response.status_code == 200:
                self.loadContacts()# 重新加载联系人

if __name__ == '__main__':
    app = QApplication(sys.argv)# 创建应用程序实例
    ex = ContactBook()# 创建通讯录窗口实例
    ex.show()# 显示窗口
    sys.exit(app.exec_())# 进入应用程序主循环
