from tkinter import Menu, Tk, Canvas
from tkinter import IntVar, StringVar, DISABLED, END, NORMAL
from tkinter import Checkbutton, Radiobutton, Entry, Button, Listbox, Text, OptionMenu

from download import Download as d
from musicTag import MusicTag as tg
import os, pyperclip

LABELFONT = ("Serif", 10, "bold")
NORMALFONT = ("Serif", 10, "normal")

# ---------------------------- UI SETUP ------------------------------- #
class UI():
    def __init__(self) -> None:
        self.title = None
        self.results = None

        self.window = Tk()
        self.window.title('Music Download/Tagger')
        self.window.minsize(width=600, height=620)
        self.window.maxsize(width=600, height=620)
        
        self.menu_option = Menu(self.window, tearoff=False)
        self.menu_option.add_command(label="Paste", command=self.paste_link)

    
        self.canvas = Canvas(width=600, height=620)
        self.canvas.grid(column=0,row=0, columnspan=2)

        self.music_list_label = self.canvas.create_text(20, 60, text="Downloaded Music:", anchor="nw", font=NORMALFONT)
        self.similar_list_label = self.canvas.create_text(393, 60, text="Return results:", anchor="ne", font=NORMALFONT)
        # All the tags label
        self.tag_label =  self.canvas.create_text(20, 380, text="Tags:", anchor="nw", font=LABELFONT)
        self.title_label = self.canvas.create_text(20, 410, text="Title:", anchor="nw", font=NORMALFONT)
        self.artist_label = self.canvas.create_text(210, 410, text="Artist:", anchor="nw", font=NORMALFONT)
        self.contribute_label = self.canvas.create_text(400, 410, text="Contributing-Artists:", anchor="nw", font=NORMALFONT)
        self.album_label = self.canvas.create_text(20, 460, text="Album:", anchor="nw", font=NORMALFONT)
        self.year_label = self.canvas.create_text(210, 460, text="Year:", anchor="nw", font=NORMALFONT)
        self.Genre_label = self.canvas.create_text(400, 460, text="Genre:", anchor="nw", font=NORMALFONT)

        self.vid_checked = IntVar(value=1)
        self.delete_vid = Checkbutton(text="Delete mp4 ('Check to delete')", variable=self.vid_checked)
        self.canvas_delete = self.canvas.create_window(20, 5, anchor="nw", window=self.delete_vid)

        self.options = [
            '360p',
            '720p' 
        ]

        self.variable = StringVar(self.window)
        self.variable.set(self.options[0])
        self.resolution_menu = OptionMenu(self.window, self.variable, *self.options)
        self.canvas_res = self.canvas.create_window(250,3, anchor="nw", window=self.resolution_menu)

        self.radio_state = IntVar()
        self.link_radiobtn = Radiobutton(text="Link", value=0, variable=self.radio_state)
        self.canvas_link = self.canvas.create_window(20,33, anchor="nw", window=self.link_radiobtn)

        self.playlist_radiobtn = Radiobutton(text="Playlist", value=1, variable=self.radio_state)
        self.canvas_playlist = self.canvas.create_window(100,33, anchor="nw", window=self.playlist_radiobtn)

        self.link_entry = Entry(width=35)
        self.canvas_link_entry = self.canvas.create_window(200, 35, anchor="nw", window=self.link_entry)
        self.link_entry.bind("<Button-3>", self.pop_menu)


        self.tag_title_entry = Entry(width=30)
        self.canvas_title_entry = self.canvas.create_window(20, 430, anchor="nw", window=self.tag_title_entry)

        self.tag_artist_entry = Entry(width=30)
        self.canvas_artist_entry = self.canvas.create_window(210, 430, anchor="nw", window=self.tag_artist_entry)

        self.tag_contribute_entry = Entry(width=30)
        self.canvas_contribute_entry = self.canvas.create_window(400, 430, anchor="nw", window=self.tag_contribute_entry)

        self.tag_album_entry = Entry(width=30)
        self.canvas_album_entry = self.canvas.create_window(20, 480, anchor="nw", window=self.tag_album_entry)

        self.tag_year_entry = Entry(width=30)
        self.canvas_year_entry = self.canvas.create_window(210, 480, anchor="nw", window=self.tag_year_entry)

        self.tag_genre_entry = Entry(width=30)
        self.canvas_genre_entry = self.canvas.create_window(400, 480, anchor="nw", window=self.tag_genre_entry)

        self.save_button = Button(text="Save Change/s", width=79, command=self.save)
        self.canvas_save_button = self.canvas.create_window(20, 520, anchor="nw", window=self.save_button)

        self.download_button = Button(text="Download", width=20, command=self.download)
        self.canvas_download_button = self.canvas.create_window(590, 32, anchor="ne", window=self.download_button)

        self.current_download_list = Listbox(height=18, width=45, exportselection=0)
        self.songs = [f for f in os.listdir("Downloads/") if f.endswith(".mp3")]
        for song in self.songs:
            self.current_download_list.insert(self.songs.index(song), song)

        self.current_download_list.bind("<<ListboxSelect>>", self.song_selection)
        self.canvas_download_list = self.canvas.create_window(20, 80, anchor="nw", window=self.current_download_list)

        self.similar_song_list = Listbox(height=18, width=45, exportselection=0)
        self.similar_song_list.insert(0, "No Information")
        self.similar_song_list.bind("<<ListboxSelect>>", self.song_detail_selection)
        self.canvas_songs_list = self.canvas.create_window(580,80, anchor="ne", window=self.similar_song_list)

        self.update_box = Text(height=3, width=70)
        self.update_box.config(state=DISABLED)
        self.canvas_update = self.canvas.create_window(20, 550, anchor="nw", window=self.update_box)
        self.window.mainloop()

    def pop_menu(self, e):
        self.menu_option.tk_popup(e.x_root, e.y_root)

    def paste_link(self):
        self.link_entry.insert(0, pyperclip.paste())

    def updates(self, message):
        self.update_box.config(state=NORMAL)
        self.update_box.insert(END, "\n{}".format(message))
        self.update_box.config(state=DISABLED)
        self.update_box.see(END)

    def download(self):
        # Grab url from entry
        url = self.link_entry.get()
        if not url == "":
            # Check if user click link or playlist
            if not self.radio_state.get() and (not "list" in url):
                dload = d(URL=url)
                self.link_entry.delete(0, END)
                status = dload.download_link(self.vid_checked.get(), self.variable.get())
                if not status == 0:
                    self.updates("Download completed and converted")
                    self.update_download()
                else:
                    self.updates("This video/audio is unavailable for access!")
            # If user click playlist
            elif self.radio_state.get() and ("list" in url):
                dload = d(playlist=url)
                self.link_entry.delete(0, END)
                dload.download_playlist(self.vid_checked.get(), self.variable.get())
                self.updates("Download completed and converted")
                self.update_download()
                if dload.fail_count > 0:
                    self.updates("{} of the videos/audios were not accessible or was not able to be converted!".format(dload.fail_count))
                    print(dload.failed_songs)
            else:
                self.updates("Check the link and make sure you have selected the right one (Link or Playlist)")
        else:
            self.updates("Please enter a link!")
            
    def update_download(self):
        # Update downloaded list after downloading
        new_list = [f for f in os.listdir("Downloads/") if f.endswith(".mp3")]
        for song in new_list:
            if song not in self.songs:
                self.current_download_list.insert(new_list.index(song), song)
                self.songs.append(song)


    def save(self):
        selected = self.current_download_list.curselection()

        title = self.tag_title_entry.get()
        year = self.tag_year_entry.get()
        album = self.tag_album_entry.get()

        contribute = []
        artists = self.tag_contribute_entry.get()
        if "," in artists:
            new_artists = artists.split(", ")
            contribute = new_artists
        else:
            contribute.append(artists)

        artist = self.tag_artist_entry.get()
        genre = self.tag_genre_entry.get()

        if selected and not title == "":
            if self.similar_song_list.curselection():
                selected_info = self.results[self.similar_song_list.curselection()[0]]
            else:
                selected_info = None
            new_info = {
                'Title': title,
                'Year': year,
                'Release-Date': year,
                'Album': album,
                'Contributing': contribute,
                'Artist': artist,
                'Genre': genre
            }
            self.updates("{}'s tags are updated!".format(new_info['Title']))

            if selected_info == new_info:
                tg(self.title).tagInfo(selected_info)
            else:
                tg(self.title).tagInfo(new_info)

    def song_detail_selection(self, event):
        if not self.similar_song_list.get(self.similar_song_list.curselection()) == "No Information":
            information = self.results[self.similar_song_list.curselection()[0]]
            self.delete_info()
            self.add_info(information)

        
    def add_info(self, details):
        self.tag_title_entry.insert(0,details['Title'])
        self.tag_artist_entry.insert(0,details['Artist'])
        self.tag_contribute_entry.insert(0,", ".join(details['Contributing']))
        self.tag_album_entry.insert(0,details['Album'])
        self.tag_year_entry.insert(0,details['Year'])
        self.tag_genre_entry.insert(0,details['Genre'])
    
    def delete_info(self):
        self.tag_title_entry.delete(0,END)
        self.tag_artist_entry.delete(0,END)
        self.tag_contribute_entry.delete(0,END)
        self.tag_album_entry.delete(0,END)
        self.tag_year_entry.delete(0,END)
        self.tag_genre_entry.delete(0,END)

    def song_selection(self, event):
        self.similar_song_list.delete(0,END)
        self.title = self.current_download_list.get(self.current_download_list.curselection())
        tagger = tg(str(self.title).replace(".mp3",""))
        self.results = tagger.search()
        self.delete_info()
        # update detail list
        
        for song in self.results:
            self.similar_song_list.insert(self.results.index(song), "{} by {}".format(song["Title"], song["Artist"]))