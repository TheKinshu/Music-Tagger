import tkinter as tk
import ttkbootstrap as ttk
from tktooltip import ToolTip
import os


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


class UI:
    def __init__(self, logger) -> None:
        self.window = ttk.Window(themename="darkly")
        self.SIZE = "600x620"

        self.window.minsize(600, 620)

        self.window.title("Welcome to Music Download/Tagger 2.0")
        self.window.geometry(self.SIZE)

        self.logger = logger
        self.logger.info("Creating UI")

        self.logger.info("Creating Notebook")
        self.notebook = ttk.Notebook(self.window, bootstyle="light")

        # Page 1
        self.logger.info("Creating Page 1")
        self.create_page1()

        # Page 2
        self.logger.info("Creating Page 2")
        self.create_page2()

        # Page 3
        self.logger.info("Creating Page 3")
        self.create_page3()


        self.notebook.pack(expand=True, fill='both')
        self.window.mainloop()

    def create_page1(self):
        self.page1 = ttk.Frame(self.notebook)

        self.directory_frame = ttk.Frame(self.page1)
        self.library_frame = ttk.Frame(self.page1)

        self.directory_frame.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.55)
        self.library_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.55)

        self.notebook.add(self.page1, text="Music Library")

        self.songs = check_for_songs(self.logger)

        self.panel1 = ttk.Treeview(self.directory_frame)
        self.panel1.heading("#0", text="Music Library")

        self.logger.info("Adding songs to UI")

        for song in self.songs:
            self.panel1.insert("", "end", text=song.replace(".mp3", ""))
        self.panel1.bind("<<TreeviewSelect>>", self.get_songs)
        self.panel1.pack(expand=True, fill='both')

        self.panel2 = ttk.Treeview(self.library_frame)
        self.panel2.heading("#0", text="Online Database")
        self.panel2.pack(expand=True, fill='both', pady=(0, 10))

        self.panel3 = ttk.Treeview(self.library_frame)
        self.panel3.heading("#0", text="Lyrics")
        self.panel3.pack(expand=True, fill='both')

        # Scrollbars
        self.libraryScrollBar = ttk.Scrollbar(self.panel1, orient="vertical", command=self.panel1.yview)
        self.panel1.configure(yscrollcommand=self.libraryScrollBar.set)
        self.libraryScrollBar.pack(side='right', fill='y')

        self.databaseScrollBar = ttk.Scrollbar(self.panel2, orient="vertical", command=self.panel2.yview)
        self.panel2.configure(yscrollcommand=self.databaseScrollBar.set)
        self.databaseScrollBar.pack(side='right', fill='y')

        self.lyricsScrollBar = ttk.Scrollbar(self.panel3, orient="vertical", command=self.panel3.yview)
        self.panel3.configure(yscrollcommand=self.lyricsScrollBar.set)
        self.lyricsScrollBar.pack(side='right', fill='y')

        self.musicSettings = ttk.Labelframe(self.page1, text="Music Settings")
        self.musicSettings.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3)
        self.musicSettings.columnconfigure(0, weight=1)
        self.musicSettings.columnconfigure(1, weight=1)
        self.musicSettings.columnconfigure(2, weight=1)

        self.musicSettings.rowconfigure(0, weight=1)
        self.musicSettings.rowconfigure(1, weight=1)
        self.musicSettings.rowconfigure(2, weight=3)

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
        self.saveSettingsButton.bind("<Button-1>", self.save_settings)
        self.saveSettingsButton.grid(row=2, column=0, columnspan=3, sticky='nesw')

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

        self.playlistRadio = ttk.Radiobutton(self.downloadSettings, text="Playlist", value=1)
        ToolTip(self.playlistRadio, "Download a playlist")
        self.playlistRadio.grid(row=0, column=0, sticky='e')

        self.songRadio = ttk.Radiobutton(self.downloadSettings, text="Song", value=2)
        ToolTip(self.songRadio, "Download a single song")
        self.songRadio.grid(row=0, column=1, sticky='e')

        self.urlLink = tk.StringVar()
        self.downloadEntry = ttk.Entry(self.downloadSettings, foreground="grey", textvariable=self.urlLink)
        self.downloadEntryPlaceholder = "Enter URL"
        self.downloadEntry.insert(0, "Enter URL")
        self.downloadEntry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.downloadEntry))
        self.downloadEntry.bind("<FocusOut>",
                                lambda event: self.on_focus_out(event, self.downloadEntry, "Enter URL"))
        self.downloadEntry.grid(row=1, column=0, columnspan=3, sticky='we', padx=3)

        self.downloadButton = ttk.Button(self.downloadSettings, text="Download", bootstyle="secondary")
        self.downloadButton.grid(row=2, column=0, columnspan=3, sticky='nesw')

        self.downloadArea = ttk.Labelframe(self.page2, text="Download Area")
        self.downloadArea.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)


    def create_page3(self):
        self.page3 = ttk.Frame(self.notebook)
        self.notebook.add(self.page3, text="Settings")

        self.downloadSettingsFrame = ttk.Labelframe(self.page3, text="Download Configurations")
        self.downloadSettingsFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

        self.downloadSettingsFrame.columnconfigure(0, weight=1)
        self.downloadSettingsFrame.columnconfigure(1, weight=1)

        self.downloadSettingsFrame.rowconfigure(0, weight=1)
        self.downloadSettingsFrame.rowconfigure(1, weight=1)

        # Set to see if the user wants to delete the song after downloading
        self.deleteSong = tk.BooleanVar()
        self.deleteSong.set(False)
        self.deleteSongCB = ttk.Checkbutton(self.downloadSettingsFrame, text="Delete Song After Download",
                                            variable=self.deleteSong)
        self.deleteSongCB.grid(row=0, column=0, sticky='e')

        # Set to see if the user wants to download the song in the highest quality
        self.highestQualityLabel = ttk.Label(self.downloadSettingsFrame, text="Highest Quality")
        self.highestQualityLabel.grid(row=1, column=0, sticky='')
        self.highestQuality = tk.StringVar()
        self.highestQuality.set("360")
        self.highestQualityCB = ttk.Combobox(self.downloadSettingsFrame, values=["360", '480'], state="readonly",
                                             textvariable=self.highestQuality, bootstyle="light")
        self.highestQualityCB.grid(row=1, column=1,)
    def get_songs(self, event):
        for item in self.panel1.selection():
            item_text = self.panel1.item(item, "text")
            self.logger.info("Current selected song: " + item_text)

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

    def save_settings(self, event):
        self.logger.info("Saving settings")
        if len(self.songName.get()) > 0 and self.songName.get() != self.songPlaceHolder:
            self.logger.info(f"Song Name: {self.songName.get()}")
            self.logger.info(f"Artist Name: {self.artistName.get()}")
            self.logger.info(f"Contribute Artist Name: {self.conArtist.get()}")
            self.logger.info(f"Album Name: {self.albumName.get()}")
            self.logger.info(f"Year: {self.year.get()}")
            self.logger.info(f"Genre: {self.genre.get()}")
        else:
            self.logger.error("Song Name is empty. Please enter a song name")
