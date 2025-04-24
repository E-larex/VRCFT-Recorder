from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLineEdit, QFileDialog,
    QDoubleSpinBox, QLabel
)
import os, json

class AudioProcessorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.wp='./data'
        self.init_ui()
        self.setup_connections()
        self.load_all_data()
    
    def setup_connections(self):
        self.config_combo.currentTextChanged.connect(self.load_data)
        self.file_edit.textChanged.connect(self.save_data)
        self.pre_time.valueChanged.connect(self.save_data)
        self.post_time.valueChanged.connect(self.save_data)

    def load_all_data(self):
        self.jsons = []
        self.pkls = []
        for name in os.listdir(self.wp):
            if os.path.isfile(self.wp+'/'+name):
                if name.endswith('.json'):
                    self.jsons.append(name.split('.')[0])
                if name.endswith('.pkl'):
                    self.pkls.append(name.split('.')[0])
        self.config_combo.clear()
        self.config_combo.addItems(self.jsons)

    def load_data(self,config):
        if not os.path.isfile(f'{self.wp}/{config}.json'):
            return 0
        with open(f'{self.wp}/{config}.json')as file:
            setting = json.load(file)
        self.file_edit.setText(setting.get('path'))
        self.pre_time.setValue(setting.get('prefix'))
        self.post_time.setValue(setting.get('suffix'))
        if os.path.isfile(f'{self.wp}/{config}.pkl'):
            self.btn_rec.setDisabled(True)
            self.btn_paly.setDisabled(False)
            self.btn_delrec.setDisabled(False)
            self.btn_delconf.setDisabled(True)
        else:
            self.btn_rec.setDisabled(False)
            self.btn_paly.setDisabled(True)
            self.btn_delrec.setDisabled(True)
            self.btn_delconf.setDisabled(False)

    def save_data(self):
        path = self.file_edit.text()
        prefix = self.pre_time.value()
        suffix = self.post_time.value()
        config = self.config_combo.currentText()
        print(path,prefix,suffix)
        with open(f'{self.wp}/{config}.json', 'w')as file:
            json.dump({'path':path,'prefix':prefix,'suffix':suffix},file)


    def action(self):
        print('111')

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()

        # 第一行：配置选择
        self.config_combo = QComboBox()
        self.config_combo.setEditable(True)
        main_layout.addWidget(self.config_combo)

        # 第二行：文件选择
        file_layout = QHBoxLayout()
        self.file_edit = QLineEdit()
        self.file_btn = QPushButton("选择音频文件")
        self.file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(self.file_btn)
        main_layout.addLayout(file_layout)

        # 第三行：前后时间设置
        time_layout = QHBoxLayout()
        
        # 前空时间
        pre_layout = QVBoxLayout()
        pre_layout.addWidget(QLabel("音频前空出时间（秒）:"))
        self.pre_time = QDoubleSpinBox()
        # self.pre_time.setRange(0.0, 60.0)
        # self.pre_time.setSingleStep(0.1)
        pre_layout.addWidget(self.pre_time)
        
        # 后空时间
        post_layout = QVBoxLayout()
        post_layout.addWidget(QLabel("音频后空出时间（秒）:"))
        self.post_time = QDoubleSpinBox()
        # self.post_time.setRange(0.0, 60.0)
        # self.post_time.setSingleStep(0.1)
        post_layout.addWidget(self.post_time)
        
        time_layout.addLayout(pre_layout)
        time_layout.addLayout(post_layout)
        main_layout.addLayout(time_layout)

        # 第四行：操作按钮
        btn_layout = QHBoxLayout()
        self.btn_rec = QPushButton("录制")
        self.btn_paly = QPushButton("播放")
        self.btn_delrec = QPushButton("删除录制")
        self.btn_delconf = QPushButton("删除配置")
        btn_layout.addWidget(self.btn_rec)
        btn_layout.addWidget(self.btn_paly)
        btn_layout.addWidget(self.btn_delrec)
        btn_layout.addWidget(self.btn_delconf)
        main_layout.addLayout(btn_layout)

        # 关键修复：设置主布局到窗口
        self.setLayout(main_layout)  # 新增这行代码

        # 窗口设置
        self.setWindowTitle("音频处理工具")
        self.setMinimumSize(500, 200)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择音频文件",
            "",
            "音频文件 (*.mp3 *.wav *.ogg);;所有文件 (*)"
        )
        if file_path:
            self.file_edit.setText(file_path)


if __name__ == "__main__":
    app = QApplication([])
    window = AudioProcessorUI()
    window.show()
    app.exec()
