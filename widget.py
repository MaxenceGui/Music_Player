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
        self.btns = {}

        # Creating the upper layout
        btn_shuffle = QPushButton("Shuffle")
        btn_shuffle.clicked.connect(self.shuffle_clicked)
        self.btns["shuffle"] = btn_shuffle

        self.song_title = QLabel("Song Title")
        self.song_title.alignment = Qt.AlignmentFlag.AlignCenter

        btn_repeat = QPushButton("Repeat")
        btn_repeat.clicked.connect(self.repeat_clicked)
        self.btns["repeat"] = btn_repeat

        upper_layout.addWidget(btn_shuffle)
        upper_layout.addWidget(self.song_title)
        upper_layout.addWidget(btn_repeat)

        # Creating the lower layout
        btn_left = QPushButton("Previous")
        self.btns["previous"] = btn_left

        btn_play = QPushButton("Play")
        self.btns["play"] = btn_play

        btn_right = QPushButton("Next")
        self.btns["next"] = btn_right

        lower_layout.addWidget(btn_left)
        lower_layout.addWidget(btn_play)
        lower_layout.addWidget(btn_right)

        self.addLayout(upper_layout)
        self.addLayout(lower_layout)


    def update(self, info=None):
        self.btns.get("play").setText(info.get("State", "Play"))
        self.song_title.setText(info.get("Title", "Song Title"))

    def set_btn_methods(self, funcs: dict):
        for key, func in funcs.items():
            self.btns.get(key).clicked.connect(func)

    def repeat_clicked(self):
        btn = self.btns.get("repeat")
        btn.setText("Repeat" if btn.text() != "Repeat" else "Repeat: on")

    def shuffle_clicked(self):
        btn = self.btns.get("shuffle")
        btn.setText("Shuffle" if btn.text() != "Shuffle" else "Unshuffle")


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
