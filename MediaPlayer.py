import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from widget import MusiqueDisplay, SongDisplay
from PyQt6.QtCore import QUrl

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
        self.actual_song_name = ""
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

    def toggle_play(self):
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
            self.song_index = (self.song_index - 1) % len(self.song_files)
            self.play_song(self.song_files[self.song_index])

    def play_next(self):
        if self.song_files:
            self.song_index = (self.song_index + 1) % len(self.song_files)
            self.play_song(self.song_files[self.song_index])

    def shuffle(self):
        pass

    def repeat(self):
        pass

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
        music_layout.set_previous_function(self.player.play_previous)
        music_layout.set_next_function(self.player.play_next)
        music_layout.set_play_function(self.player.toggle_play)
        music_layout.set_shuffle(self.player.shuffle)
        music_layout.set_repeat(self.player.repeat)

        self.setLayout(main_layout)

        self.resize(400, 400)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
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
