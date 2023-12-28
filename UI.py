import tkinter as tk
import ttkbootstrap as ttk
from tktooltip import ToolTip
import os
import downloader
import json
from databases import Database as databases
from eyed3 import load
from eyed3.id3 import Tag
from azlyrics.azlyrics import lyrics


def check_for_songs(logger):
    try:
        logger.info("Checking for songs")
        songs = [f for f in os.listdir("Downloads/") if f.endswith(".mp3")]
        # songs = [str(f).join('.mp3') for f in range(100)]
        logger.info(f"Found {len(songs)} songs")
    except Exception as e:
        logger.error("Error checking for songs")
        songs = []
    return songs


def check_for_lyrics(logger, song, artist):
    logger.info("Checking for lyrics")
    results = lyrics(artist, song)
    logger.info(results)
    if "Error" in results:
        # remove non-english characters
        song = song.encode("ascii", "ignore").decode()
        logger.info(song)
        # remove brackets in song title
        song = song.replace("(", "").replace(")", "")
        # remove whitespace with a dash
        results = lyrics(artist, song)
        if "Error" in results:
            # remove whitespace with a dash
            artist = artist.replace(" ", "-")
            logger.info(artist)
            results = lyrics(artist, song)

    if "Error" not in results:
        logger.info("Lyrics found")
        # remove and newlines from the start of the lyrics
    else:
        logger.info("Lyrics not found")
        results = [""]
    return results[0]


class UI:
    def __init__(self, logger, settings=None) -> None:

        self.themeSettings = None
        self.logger = logger
        self.settings = settings
        self.currentSelectedSong = None
        self.downloadFolder = "Downloads"
        self.currentDownload = "None"

        self.test = None
        self.musicDownloader = downloader

        # Check if settings exist
        # If settings do not exist, create settings
        if settings is None:
            self.logger.info("Settings not found")
            self.logger.info("Creating settings")
            json_object = {
                "theme": "darkly",
                "default-quality": "360p",
                "delete-afterward": False
            }
            with open("settings.json", "w") as outfile:
                json.dump(json_object, outfile)
            self.settings = json_object

        self.currentTheme = self.settings["theme"]
        self.currentQuality = self.settings["default-quality"]
        self.currentDelete = self.settings["delete-afterward"]

        self.window = ttk.Window(themename=self.currentTheme)
        self.window.iconbitmap("doro.ico")
        self.SIZE = "600x620"

        self.window.minsize(600, 620)

        self.window.title("Welcome to Music Download/Tagger 2.0")
        self.window.geometry(self.SIZE)

        self.logger = logger
        self.logger.info("Creating UI")

        self.logger.info("Creating Notebook")
        self.notebook = ttk.Notebook(self.window, bootstyle="light")

        # Page 1
        self.logger.info("Creating Page 2")
        self.create_page2()

        # Page 2
        self.logger.info("Creating Page 1")
        self.create_page1()

        # Page 3
        self.logger.info("Creating Page 3")
        self.create_page3()

        self.notebook.pack(expand=True, fill='both')
        self.window.mainloop()

    def create_page1(self):
        self.page1 = ttk.Frame(self.notebook)

        self.directory_frame = ttk.Frame(self.page1)

        self.directory_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.55)

        self.notebook.add(self.page1, text="Music Library")

        self.songs = check_for_songs(self.logger)

        self.panel1 = ttk.Treeview(self.directory_frame)
        self.panel1.heading("#0", text="Music Library")

        self.logger.info("Adding songs to UI")

        for song in self.songs:
            self.panel1.insert("", "end", text=song.replace(".mp3", ""))
        self.panel1.bind("<<TreeviewSelect>>", self.get_songs)

        # Add double click to edit song details
        self.panel1.bind("<Double-1>", self.detail_edit)
        self.panel1.pack(expand=True, fill='both')

        # Scrollbars
        self.libraryScrollBar = ttk.Scrollbar(self.panel1, orient="vertical", command=self.panel1.yview)
        self.panel1.configure(yscrollcommand=self.libraryScrollBar.set)
        self.libraryScrollBar.pack(side='right', fill='y')

        self.musicSettings = ttk.Labelframe(self.page1, text="Quick Edits")
        self.musicSettings.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3)
        self.musicSettings.columnconfigure(0, weight=1)
        self.musicSettings.columnconfigure(1, weight=1)
        self.musicSettings.columnconfigure(2, weight=1)

        self.musicSettings.rowconfigure(0, weight=1)
        self.musicSettings.rowconfigure(1, weight=1)
        self.musicSettings.rowconfigure(2, weight=3)
        self.musicSettings.rowconfigure(3, weight=3)

        self.songName = tk.StringVar()
        self.artistName = tk.StringVar()
        self.conArtist = tk.StringVar()
        self.albumName = tk.StringVar()
        self.year = tk.StringVar()
        self.genre = tk.StringVar()

        self.songNameEntry = ttk.Entry(self.musicSettings, foreground="grey", textvariable=self.songName)
        self.songPlaceHolder = "Song Name"
        self.songNameEntry.insert(0, self.songPlaceHolder)
        self.songNameEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.songNameEntry))
        self.songNameEntry.bind("<FocusOut>",
                                lambda event: self.on_focus_out(event, self.songNameEntry, self.songPlaceHolder))
        self.songNameEntry.grid(row=0, column=0, sticky='we', padx=(2, 5))

        self.artistNameEntry = ttk.Entry(self.musicSettings, foreground="grey", textvariable=self.artistName)
        self.artistPlaceHolder = "Artist Name"
        self.artistNameEntry.insert(0, self.artistPlaceHolder)
        self.artistNameEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.artistNameEntry))
        self.artistNameEntry.bind("<FocusOut>",
                                  lambda event: self.on_focus_out(event, self.artistNameEntry, self.artistPlaceHolder))
        self.artistNameEntry.grid(row=0, column=1, sticky='we', padx=(2, 5))

        self.conArtistEntry = ttk.Entry(self.musicSettings, foreground="grey", textvariable=self.conArtist)
        self.conArtistPlaceHolder = "Contribute Artists Name"
        self.conArtistEntry.insert(0, self.conArtistPlaceHolder)
        self.conArtistEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.conArtistEntry))
        self.conArtistEntry.bind("<FocusOut>",
                                 lambda event: self.on_focus_out(event, self.conArtistEntry, self.conArtistPlaceHolder))
        self.conArtistEntry.grid(row=0, column=2, sticky='we', padx=(2, 5))

        self.albumNameEntry = ttk.Entry(self.musicSettings, foreground="grey", textvariable=self.albumName)
        self.albumPlaceHolder = "Album Name"
        self.albumNameEntry.insert(0, self.albumPlaceHolder)
        self.albumNameEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.albumNameEntry))
        self.albumNameEntry.bind("<FocusOut>",
                                 lambda event: self.on_focus_out(event, self.albumNameEntry, self.albumPlaceHolder))
        self.albumNameEntry.grid(row=1, column=0, sticky='we', padx=(2, 5))

        self.yearEntry = ttk.Entry(self.musicSettings, foreground="grey", textvariable=self.year)
        self.yearPlaceHolder = "Year"
        self.yearEntry.insert(0, self.yearPlaceHolder)
        self.yearEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.yearEntry))
        self.yearEntry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.yearEntry, self.yearPlaceHolder))
        self.yearEntry.grid(row=1, column=1, sticky='we', padx=(2, 5))

        self.genreCB = ttk.Combobox(self.musicSettings,
                                    values=self.all_genre(), foreground="grey", textvariable=self.genre)
        self.genrePlaceHolder = "Genre"
        self.genreCB.insert(0, self.genrePlaceHolder)
        self.genreCB.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.genreCB))
        self.genreCB.bind("<FocusOut>",
                          lambda event: self.on_focus_out(event, self.genreCB, self.genrePlaceHolder))
        self.genreCB.grid(row=1, column=2, sticky='we', padx=(2, 5))

        self.saveSettingsButton = ttk.Button(self.musicSettings, text="Save Settings", bootstyle="secondary")
        self.saveSettingsButton.bind("<Button-1>", self.quick_edit_saves)
        self.saveSettingsButton.grid(row=2, column=0, columnspan=3, sticky='nesw')

        # force update button
        self.forceUpdateButton = ttk.Button(self.musicSettings, text="Force Update", bootstyle="success")
        self.forceUpdateButton.bind("<Button-1>", self.force_update)
        self.forceUpdateButton.grid(row=3, column=0, columnspan=3, sticky='nesw')

    def force_update(self, event):
        # refresh the music library
        self.panel1.delete(*self.panel1.get_children())
        self.songs = check_for_songs(self.logger)
        for song in self.songs:
            self.panel1.insert("", "end", text=song.replace(".mp3", ""))

    def detail_edit(self, event):
        if self.currentSelectedSong is not None:
            # Create a popup window
            self.popup = tk.Toplevel()
            self.popup.iconbitmap("doro.ico")
            self.popup.title("Edit Song Details")
            self.popup.geometry("600x620")
            self.popup.minsize(600, 620)

            # Add Online Database and lyrics
            self.infoFrame = ttk.Frame(self.popup)

            self.databasePanel = ttk.Treeview(self.infoFrame)
            self.databasePanel.heading("#0", text="Online Database")
            self.find_song()
            self.databasePanel.place(relx=0.01, rely=0.03, relwidth=0.47, relheight=0.59)
            self.databasePanel.bind("<<TreeviewSelect>>", self.get_song_tags)

            # Add lyrics panel with label frame saying its Lyrics and add a text box that fills the label frame with
            # 1 x 1 grid
            self.lyricsLabel = ttk.Labelframe(self.infoFrame, text="Lyrics")
            self.lyricsLabel.columnconfigure(0, weight=1)
            self.lyricsLabel.rowconfigure(0, weight=1)

            # Add a text box that fills the label frame with 1 x 1 grid
            self.lyricsText = tk.Text(self.lyricsLabel)
            self.lyricsText.grid(row=0, column=0, sticky='nesw')
            self.lyricsText.insert(tk.END, "Lyrics")
            self.lyricsLabel.place(relx=0.53, rely=0.03, relwidth=0.47, relheight=0.59)

            self.infoFrame.pack(expand=True, fill='both', pady=(20, 0), padx=30)

            self.editorLF = ttk.Labelframe(self.popup, text="Edit Song Details")
            self.editorLF.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3)
            self.editorLF.columnconfigure(0, weight=1)
            self.editorLF.columnconfigure(1, weight=1)
            self.editorLF.columnconfigure(2, weight=1)

            self.editorLF.rowconfigure(0, weight=1)
            self.editorLF.rowconfigure(1, weight=1)
            self.editorLF.rowconfigure(2, weight=1)

            self.songDetailName = tk.StringVar()
            self.artistDetailName = tk.StringVar()
            self.conDetailArtist = tk.StringVar()
            self.albumDetailName = tk.StringVar()
            self.yearDetail = tk.StringVar()
            self.genreDetail = tk.StringVar()

            self.songDetailNameEntry = ttk.Entry(self.editorLF, foreground="grey", textvariable=self.songDetailName)
            self.songDetailNameEntry.insert(0, self.songPlaceHolder)
            self.songDetailNameEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.songDetailNameEntry))
            self.songDetailNameEntry.bind("<FocusOut>",
                                          lambda event: self.on_focus_out(event, self.songDetailNameEntry,
                                                                          self.songPlaceHolder))
            self.songDetailNameEntry.grid(row=0, column=0, sticky='we', padx=(2, 5))

            self.artistDetailNameEntry = ttk.Entry(self.editorLF, foreground="grey", textvariable=self.artistDetailName)
            self.artistDetailNameEntry.insert(0, self.artistPlaceHolder)
            self.artistDetailNameEntry.bind("<FocusIn>",
                                            lambda event: self.on_focus_in(event, self.artistDetailNameEntry))
            self.artistDetailNameEntry.bind("<FocusOut>",
                                            lambda event: self.on_focus_out(event, self.artistDetailNameEntry,
                                                                            self.artistPlaceHolder))
            self.artistDetailNameEntry.grid(row=0, column=1, sticky='we', padx=(2, 5))

            self.conDetailArtistEntry = ttk.Entry(self.editorLF, foreground="grey", textvariable=self.conDetailArtist)
            self.conDetailArtistEntry.insert(0, self.conArtistPlaceHolder)
            self.conDetailArtistEntry.bind("<FocusIn>",
                                           lambda event: self.on_focus_in(event, self.conDetailArtistEntry))
            self.conDetailArtistEntry.bind("<FocusOut>",
                                           lambda event: self.on_focus_out(event, self.conDetailArtistEntry,
                                                                           self.conArtistPlaceHolder))
            self.conDetailArtistEntry.grid(row=0, column=2, sticky='we', padx=(2, 5))

            self.albumDetailNameEntry = ttk.Entry(self.editorLF, foreground="grey", textvariable=self.albumDetailName)
            self.albumDetailNameEntry.insert(0, self.albumPlaceHolder)
            self.albumDetailNameEntry.bind("<FocusIn>",
                                           lambda event: self.on_focus_in(event, self.albumDetailNameEntry))
            self.albumDetailNameEntry.bind("<FocusOut>",
                                           lambda event: self.on_focus_out(event, self.albumDetailNameEntry,
                                                                           self.albumPlaceHolder))
            self.albumDetailNameEntry.grid(row=1, column=0, sticky='we', padx=(2, 5))

            self.yearDetailEntry = ttk.Entry(self.editorLF, foreground="grey", textvariable=self.yearDetail)
            self.yearDetailEntry.insert(0, self.yearPlaceHolder)
            self.yearDetailEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.yearDetailEntry))
            self.yearDetailEntry.bind("<FocusOut>",
                                      lambda event: self.on_focus_out(event, self.yearDetailEntry,
                                                                      self.yearPlaceHolder))
            self.yearDetailEntry.grid(row=1, column=1, sticky='we', padx=(2, 5))

            self.genreDetailCB = ttk.Combobox(self.editorLF,
                                              values=self.all_genre(), foreground="grey", textvariable=self.genreDetail)
            self.genreDetailCB.insert(0, self.genrePlaceHolder)
            self.genreDetailCB.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.genreDetailCB))
            self.genreDetailCB.bind("<FocusOut>",
                                    lambda event: self.on_focus_out(event, self.genreDetailCB,
                                                                    self.genrePlaceHolder))
            self.genreDetailCB.grid(row=1, column=2, sticky='we', padx=(2, 5))

            self.saveDetailSettingsButton = ttk.Button(self.editorLF, text="Save Settings", bootstyle="secondary")
            self.saveDetailSettingsButton.bind("<Button-1>", self.detailEditingSaving)
            self.saveDetailSettingsButton.grid(row=2, column=0, columnspan=3, sticky='nesw')

    def find_song(self):
        results = databases(self.logger, self.currentSelectedSong, method='search').get_artist_with_song_name()
        if results is not None:
            for result in results:
                self.databasePanel.insert("", "end", text=f"{result['name']} - {result['artist']}")
        print(results)

    def detailEditingSaving(self, event):

        try:
            audioFile = load(f"Downloads/{self.currentSelectedSong}.mp3")
            audioFile.tag.album_artist = self.artistDetailName.get()
            audioFile.tag.album = self.albumDetailName.get()
            audioFile.tag.title = self.songDetailName.get()
            audioFile.tag.artist = self.conDetailArtist.get()
            audioFile.tag.recording_date = self.yearDetail.get()
            audioFile.tag.genre = self.genreDetail.get()
            # save lyrics
            audioFile.tag.lyrics.set(self.lyricsText.get(1.0, tk.END))
            # save the changes
            audioFile.tag.save()
        except Exception as e:
            self.logger.error("Error saving details")
        finally:
            # Close the popup
            self.popup.destroy()

    def create_page2(self):
        # Page 2
        self.page2 = ttk.Frame(self.notebook)
        self.notebook.add(self.page2, text="Download Music")

        self.downloadSettings = ttk.Labelframe(self.page2, text="Download Settings")
        self.downloadSettings.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

        self.downloadSettings.columnconfigure(0, weight=1)
        self.downloadSettings.columnconfigure(1, weight=1)
        self.downloadSettings.columnconfigure(2, weight=1)

        self.downloadSettings.rowconfigure(0, weight=1)
        self.downloadSettings.rowconfigure(1, weight=1)
        self.downloadSettings.rowconfigure(2, weight=1)

        self.downloadState = tk.IntVar(None, 1)

        self.playlistRadio = ttk.Radiobutton(self.downloadSettings, text="Playlist", value=2,
                                             variable=self.downloadState)
        ToolTip(self.playlistRadio, "Download a playlist")
        self.playlistRadio.grid(row=0, column=1, sticky='e')

        self.songRadio = ttk.Radiobutton(self.downloadSettings, text="Song", value=1, variable=self.downloadState)
        ToolTip(self.songRadio, "Download a single song")
        self.songRadio.grid(row=0, column=0, sticky='e')

        self.urlLink = tk.StringVar()
        self.downloadEntry = ttk.Entry(self.downloadSettings, foreground="grey", textvariable=self.urlLink)
        self.downloadEntryPlaceholder = "Enter URL"
        self.downloadEntry.insert(0, "Enter URL")
        self.downloadEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.downloadEntry))
        self.downloadEntry.bind("<FocusOut>",
                                lambda event: self.on_focus_out(event, self.downloadEntry, "Enter URL"))
        self.downloadEntry.grid(row=1, column=0, columnspan=3, sticky='we', padx=3)

        self.downloadButton = ttk.Button(self.downloadSettings, text="Download", bootstyle="secondary")
        self.downloadButton.bind("<Button-1>", self.downloadMusic)
        self.downloadButton.grid(row=2, column=0, columnspan=3, sticky='nesw')

        self.downloadArea = ttk.Labelframe(self.page2, text="Download Area")
        self.downloadArea.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)

        self.processingLabel = ttk.Label(self.downloadArea, text="Currently Downloading:\t\t\tNone")
        self.processingLabel.place(relx=0.05, rely=0.1)

        self.progress = ttk.Meter(self.downloadArea, subtext="Download Progress", textright="%", stripethickness=10, )
        self.progress.place(relx=0.32, rely=0.2)

    def create_page3(self):
        self.page3 = ttk.Frame(self.notebook)
        self.notebook.add(self.page3, text="Settings")

        self.downloadSettingsFrame = ttk.Labelframe(self.page3, text="Download Configurations")
        self.downloadSettingsFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

        self.downloadSettingsFrame.columnconfigure(0, weight=1)
        self.downloadSettingsFrame.columnconfigure(1, weight=1)

        self.downloadSettingsFrame.rowconfigure(0, weight=1)
        self.downloadSettingsFrame.rowconfigure(1, weight=1)
        self.downloadSettingsFrame.rowconfigure(2, weight=1)
        self.downloadSettingsFrame.rowconfigure(3, weight=1)

        # Set to see if the user wants to delete the song after downloading
        self.deleteSong = tk.BooleanVar()
        self.deleteSong.set(self.currentDelete)
        self.deleteSongCB = ttk.Checkbutton(self.downloadSettingsFrame, text="Delete Song After Download",
                                            variable=self.deleteSong)
        self.deleteSongCB.grid(row=0, column=0, sticky='e')

        # Set to see if the user wants to download the song in the highest quality
        self.qualityCheckLabel = ttk.Label(self.downloadSettingsFrame, text="Highest Quality")
        self.qualityCheckLabel.grid(row=1, column=0, sticky='')
        self.qualityCheck = tk.StringVar()
        self.qualityCheck.set(self.currentQuality)
        self.qualityCheckCB = ttk.Combobox(self.downloadSettingsFrame, values=["360p", '480p'], state="readonly",
                                           textvariable=self.qualityCheck, bootstyle="light")
        self.qualityCheckCB.grid(row=1, column=1, )

        self.themeSettingsLabel = ttk.Label(self.downloadSettingsFrame, text="Theme")
        self.themeSettingsLabel.grid(row=2, column=0, sticky='')
        self.themeSettings = tk.StringVar()
        self.themeSettings.set(self.currentTheme)
        self.themeSettingsCB = ttk.Combobox(self.downloadSettingsFrame, values=["darkly", 'solar', 'superhero',
                                                                                'cyborg', 'vapor'], state="readonly",
                                            textvariable=self.themeSettings, bootstyle="darkly")
        self.themeSettingsCB.grid(row=2, column=1, )

        self.saveUISettingsButton = ttk.Button(self.downloadSettingsFrame, text="Save Settings", bootstyle="secondary")
        self.saveUISettingsButton.bind("<Button-1>", self.saveUISettings)
        self.saveUISettingsButton.grid(row=3, column=0, columnspan=3, sticky='nesw')

    def saveUISettings(self, event):
        self.logger.info("Saving UI Settings")
        self.logger.info(f"Delete Song: {self.deleteSong.get()}")
        self.logger.info(f"Quality: {self.qualityCheck.get()}")
        self.logger.info(f"Theme: {self.themeSettings.get()}")

        json_object = {
            "theme": self.themeSettings.get(),
            "default-quality": self.qualityCheck.get(),
            "delete-afterward": self.deleteSong.get()
        }
        with open("settings.json", "w") as outfile:
            json.dump(json_object, outfile)

        # change theme
        self.window.style.theme_use(self.themeSettings.get())

    def setProgress(self, title, progress):
        self.processingLabel.config(text=f"Currently Downloading:\t\t\t{title}")
        self.progress["amountused"] = round(progress * 100, 2)

    def downloadMusic(self, event):
        if self.downloadState.get() == 1:
            self.logger.info("Downloading song")

            downloader = self.musicDownloader.downloader(str(self.urlLink.get()), "Video", self.qualityCheck.get(),
                                                         self.logger, self.setProgress, self.window)

            downloader.single_download()

        elif self.downloadState.get() == 2:
            self.logger.info("Downloading playlist")
            self.musicDownloader.downloader(str(self.urlLink.get()), "Video", self.qualityCheck.get(), self.logger,
                                            self.setProgress, self.window).playlist_download()

    def get_songs(self, event):
        # reset the entry boxes with placeholders
        self.songName.set(self.songPlaceHolder)
        self.artistName.set(self.artistPlaceHolder)
        self.conArtist.set(self.conArtistPlaceHolder)
        self.albumName.set(self.albumPlaceHolder)
        self.year.set(self.yearPlaceHolder)
        self.genre.set(self.genrePlaceHolder)

        for item in self.panel1.selection():
            item_text = self.panel1.item(item, "text")
            self.logger.info("Current selected song: " + item_text)
            self.currentSelectedSong = item_text

            # Load the song details
            audioFile = load(f"Downloads/{self.currentSelectedSong}.mp3")

            # Set tags if they exist
            set_if_not_none = lambda attr, var: var.set(getattr(audioFile.tag, attr)) if getattr(audioFile.tag,
                                                                                                 attr) is not None else None

            set_if_not_none('title', self.songName)
            set_if_not_none('artist', self.artistName)
            set_if_not_none('album_artist', self.conArtist)
            set_if_not_none('album', self.albumName)
            set_if_not_none('recording_date', self.year)
            set_if_not_none('genre', self.genre)


    def get_song_tags(self, event):
        try:
            selectionText = None
            for selection in self.databasePanel.selection():
                selectionText = self.databasePanel.item(selection, "text")
                self.logger.info("Current selected option " + selectionText)
            song, artist = selectionText.split(" - ")
            lyrics = check_for_lyrics(self.logger, song, artist)
            self.lyricsText.delete(1.0, tk.END)
            self.lyricsText.insert(tk.END, lyrics)
            picks = databases(self.logger, song, artist, "getinfo")
            trackName, artistName = picks.get_music_tag()
            album, artists, year = picks.find_album(trackName, artistName)
            self.songDetailName.set(trackName)
            self.artistDetailName.set(artistName)
            self.conDetailArtist.set(", ".join(artists))
            self.albumDetailName.set(album)
            self.yearDetail.set(year)
        except Exception as e:
            self.logger.error("Error getting song tags")
            self.logger.error(e)

    def on_focus_in(self, event, entry):
        placeholders = [self.songPlaceHolder, self.artistPlaceHolder, self.conArtistPlaceHolder, self.albumPlaceHolder,
                        self.yearPlaceHolder, self.genrePlaceHolder, self.downloadEntryPlaceholder]
        if entry.get() in placeholders:
            entry.delete(0, "end")
            entry.insert(0, "")
            entry.config(foreground="white")

    @staticmethod
    def on_focus_out(event, entry, placeholders=None):
        if not entry.get():
            entry.insert(0, placeholders)
            entry.config(foreground="grey")

    @staticmethod
    def all_genre():
        return ["Rock", "Pop", 'K-Pop', 'J-Pop', "Hip-Hop", "Rap", "Country", "Jazz", "Blues", "R&B", "Soul", "Funk",
                "Reggae",
                "Electronic", "Dance", "Classical", "Latin", "Metal", "Alternative", "Indie", "Punk", "Gospel",
                "Christian", "Instrumental", "New Age", "Folk", "World", "Other"]

    def quick_edit_saves(self, event):
        self.logger.info("Saving settings")
        if len(self.songName.get()) > 0 and self.songName.get() != self.songPlaceHolder:
            self.logger.info(f"Song Name: {self.songName.get()}")
            self.logger.info(f"Artist Name: {self.artistName.get()}")
            self.logger.info(f"Contribute Artist Name: {self.conArtist.get()}")
            self.logger.info(f"Album Name: {self.albumName.get()}")
            self.logger.info(f"Year: {self.year.get()}")
            self.logger.info(f"Genre: {self.genre.get()}")

            # rename the file to song name with artist name
            os.rename(f"{self.downloadFolder}/{self.currentSelectedSong}.mp3",
                      f"{self.downloadFolder}/{self.songName.get()} - {self.artistName.get()}.mp3")

            # Load the song details
            audioFile = load(f"./Downloads/{self.songName.get()} - {self.artistName.get()}.mp3")

            # Set tags if the entry is not empty
            set_tag_if_not_empty = lambda tag, value, placeholder: setattr(audioFile.tag, tag,
                                                                           value) if value != placeholder else None

            set_tag_if_not_empty('title', self.songName.get(), self.songPlaceHolder)
            set_tag_if_not_empty('artist', self.artistName.get(), self.artistPlaceHolder)
            set_tag_if_not_empty('album_artist', self.conArtist.get(), self.conArtistPlaceHolder)
            set_tag_if_not_empty('album', self.albumName.get(), self.albumPlaceHolder)
            set_tag_if_not_empty('recording_date', self.year.get(), self.yearPlaceHolder)
            set_tag_if_not_empty('genre', self.genre.get(), self.genrePlaceHolder)

            # Only add the specific tags if the entry is not empty
            # if self.songName.get() != self.songPlaceHolder:
            #     audioFile.tag.title = self.songName.get()
            # if self.artistName.get() != self.artistPlaceHolder:
            #     audioFile.tag.artist = self.artistName.get()
            # if self.conArtist.get() != self.conArtistPlaceHolder:
            #     audioFile.tag.album_artist = self.conArtist.get()
            # if self.albumName.get() != self.albumPlaceHolder:
            #     audioFile.tag.album = self.albumName.get()
            # if self.year.get() != self.yearPlaceHolder:
            #     audioFile.tag.recording_date = self.year.get()
            # if self.genre.get() != self.genrePlaceHolder:
            #     audioFile.tag.genre = self.genre.get()
            audioFile.tag.save()

            # reset panel and get new songs
            self.panel1.delete(*self.panel1.get_children())
            self.songs = check_for_songs(self.logger)
            for song in self.songs:
                self.panel1.insert("", "end", text=song.replace(".mp3", ""))

            self.currentSelectedSong = None

        else:
            self.logger.error("Song Name is empty. Please enter a song name")
