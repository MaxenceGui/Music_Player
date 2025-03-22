import os
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget
from PyQt6.QtCore import Qt

class Observer:
    def update(self):
        pass

class MusiqueDisplay(QVBoxLayout, Observer):
    def __init__(self):
        super().__init__()

        upper_layout = QHBoxLayout()
        lower_layout = QHBoxLayout()

        self.previous = None
        self.next = None
        self.play = None

        # Creating the upper layout
        self.btn_shuffle = QPushButton("Shuffle")

        self.song_title = QLabel("Song Title")
        self.song_title.alignment = Qt.AlignmentFlag.AlignCenter

        self.btn_repeat = QPushButton("Repeat")

        upper_layout.addWidget(self.btn_shuffle)
        upper_layout.addWidget(self.song_title)
        upper_layout.addWidget(self.btn_repeat)

        # Creating the lower layout
        self.btn_left = QPushButton("Previous")
        self.btn_play = QPushButton("Play")
        self.btn_right = QPushButton("Next")

        lower_layout.addWidget(self.btn_left)
        lower_layout.addWidget(self.btn_play)
        lower_layout.addWidget(self.btn_right)

        self.addLayout(upper_layout)
        self.addLayout(lower_layout)

    def update(self, info=None):
        self.btn_play.setText(info.get("State", "Play"))
        self.song_title.setText(info.get("Title", "Song Title"))

    def set_shuffle(self, func):
        self.btn_shuffle.clicked.connect(func)

    def set_repeat(self, func):
        self.btn_repeat.clicked.connect(func)

    def set_previous_function(self, func):
        self.btn_left.clicked.connect(func)

    def set_next_function(self, func):
        self.btn_right.clicked.connect(func)

    def set_play_function(self, func):
        self.btn_play.clicked.connect(func)


class SongDisplay(QVBoxLayout, Observer):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("Select a folder to play music")
        layout.addWidget(self.label)

        self.song_list = QListWidget()
        layout.addWidget(self.song_list)

        self.btn_select = QPushButton("Select Music Folder")
        layout.addWidget(self.btn_select)

        self.addLayout(layout)

    def update(self, info):
        self.label.setText(f"Loaded {info} files")

    def connect_select_folder_method(self, func):
        self.btn_select.clicked.connect(func)

    def set_play_selected_method(self, func):
        self.song_list.itemClicked.connect(func)
