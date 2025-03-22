import os
import random
import sys

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel, QHBoxLayout, QPushButton, QListWidget
from PyQt6.QtCore import QUrl, QSettings, Qt


#  _       ___     __           __     ________
# | |     / (_)___/ /___ ____  / /_   / ____/ /___ ___________
# | | /| / / / __  / __ `/ _ \/ __/  / /   / / __ `/ ___/ ___/
# | |/ |/ / / /_/ / /_/ /  __/ /_   / /___/ / /_/ (__  |__  )
# |__/|__/_/\__,_/\__, /\___/\__/   \____/_/\__,_/____/____/
#                /____/

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


#    __  ___         ___       ____  __                         ________
#   /  |/  /__  ____/ (_)___ _/ __ \/ /___ ___  _____  _____   / ____/ /___ ___________
#  / /|_/ / _ \/ __  / / __ `/ /_/ / / __ `/ / / / _ \/ ___/  / /   / / __ `/ ___/ ___/
# / /  / /  __/ /_/ / / /_/ / ____/ / /_/ / /_/ /  __/ /     / /___/ / /_/ (__  |__  )
#/_/  /_/\___/\__,_/_/\__,_/_/   /_/\__,_/\__, /\___/_/      \____/_/\__,_/____/____/
#                                        /____/


class Subject:

    def __init__(self):
        self.listeners = []

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, info=None):
        for listener in self.listeners:
            listener.update(info)

class MediaPlayer(QWidget, Subject):
    def __init__(self):
        super().__init__()
        self.song_files = []
        self.song_index = -1
        self.song_prev_index = -1
        self.actual_song_name = ""
        self.loop = False
        self.random = False
        self.repeat_song = False
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.mediaStatusChanged.connect(self.handle_media_status)

    def toggle_play(self):
        if self.song_index == -1:
            self.play_next()

        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.notify({"State" : "Play", "Title" : self.actual_song_name})
        else:
            self.player.play()
            self.notify({"State" : "Pause", "Title" : self.actual_song_name})

    def play_song(self, song_path):
        self.actual_song_name = os.path.basename(song_path)
        self.player.setSource(QUrl.fromLocalFile(song_path))
        self.player.play()
        self.notify({"State" : "Pause", "Title" : self.actual_song_name})

    def play_previous(self):
        if self.song_files:
            self.song_index = (self.song_index - 1) % len(self.song_files) if not self.random else self.song_prev_index
            self.play_song(self.song_files[self.song_index])

    def play_next(self):
        if self.song_files:
            increment = 1 if not self.random else random.randint(0, len(self.song_files) - 1)
            self.song_prev_index = self.song_index
            if not self.repeat_song:
                self.song_index = (self.song_index + increment) % len(self.song_files)
            self.play_song(self.song_files[self.song_index])

    def shuffle(self):
        self.random = not self.random

    def repeat(self):
        self.repeat_song = True if self.random else False
        self.loop = not self.loop

    def handle_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self.loop:
            self.play_next()

class MusiquePlayer(QWidget, Subject):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.player = MediaPlayer()

        main_layout = QVBoxLayout()
        music_layout = MusiqueDisplay()
        file_layout = SongDisplay()
        main_layout.addLayout(music_layout)
        main_layout.addLayout(file_layout)

        # Attach observer
        self.player.attach(music_layout)
        self.attach(file_layout)

        # Get song list
        self.song_list = file_layout.song_list
        self.info_label = file_layout.label

        # Set button connection
        file_layout.connect_select_folder_method(self.select_folder)
        file_layout.set_play_selected_method(self.play_selected_song)
        music_layout.set_btn_methods({
            "repeat": self.player.repeat,
            "shuffle": self.player.shuffle,
            "previous": self.player.play_previous,
            "play": self.player.toggle_play,
            "next": self.player.play_next
        })

        self.setLayout(main_layout)

        self.resize(400, 250)

        folder = self.load_folder_path()
        if folder:
            self.load_songs(folder)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self.save_folder_path(folder)
            self.load_songs(folder)

    def load_songs(self, folder):
        self.player.song_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.mp3', '.wav', '.ogg'))]
        self.song_list.clear()
        for file in self.player.song_files:
            self.song_list.addItem(os.path.basename(file))
        self.notify(info = len(self.song_list))

    def play_selected_song(self):
        index = self.song_list.currentRow()
        if 0 <= index < len(self.player.song_files):
            self.player.song_index = index
            self.player.play_song(self.player.song_files[index])

    def save_folder_path(self, folder_path):
        setting = QSettings("MediaPlayer", "MusicPlayer")
        setting.setValue("folder_path", folder_path)

    def load_folder_path(self):
        setting = QSettings("MediaPlayer", "MusicPlayer")
        return setting.value("folder_path", "")


#    __  ___      _
#   /  |/  /___ _(_)___
#  / /|_/ / __ `/ / __ \
# / /  / / /_/ / / / / /
#/_/  /_/\__,_/_/_/ /_/


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusiquePlayer()
    window.show()
    sys.exit(app.exec())
