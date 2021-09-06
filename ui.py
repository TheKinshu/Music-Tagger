from pprint import pprint
from tkinter import *
import os
from typing import NoReturn
from download import Download as d
from musicTag import MusicTag as tg

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

        self.canvas = Canvas(width=600, height=620)
        self.canvas.grid(column=0,row=0, columnspan=2)

        self.music_list_label = self.canvas.create_text(20, 60, text="Downloaded Music:", anchor="nw", font=NORMALFONT)
        self.similar_list_label = self.canvas.create_text(483, 60, text="Return results:", anchor="ne", font=NORMALFONT)
        # All the tags label
        self.tag_label =  self.canvas.create_text(20, 380, text="Tags:", anchor="nw", font=LABELFONT)
        self.title_label = self.canvas.create_text(20, 410, text="Title:", anchor="nw", font=NORMALFONT)
        self.artist_label = self.canvas.create_text(210, 410, text="Artist:", anchor="nw", font=NORMALFONT)
        self.contribute_label = self.canvas.create_text(400, 410, text="Contributing-Artists:", anchor="nw", font=NORMALFONT)
        self.album_label = self.canvas.create_text(20, 460, text="Album:", anchor="nw", font=NORMALFONT)
        self.year_label = self.canvas.create_text(210, 460, text="Year:", anchor="nw", font=NORMALFONT)
        self.Genre_label = self.canvas.create_text(400, 460, text="Genre:", anchor="nw", font=NORMALFONT)

        self.radio_state = IntVar()
        self.link_radiobtn = Radiobutton(text="Link", value=0, variable=self.radio_state, command=self.purpose_selection)
        self.canvas_link = self.canvas.create_window(20,5, anchor="nw", window=self.link_radiobtn)

        self.playlist_radiobtn = Radiobutton(text="Playlist", value=1, variable=self.radio_state, command=self.purpose_selection)
        self.canvas_playlist = self.canvas.create_window(100,5, anchor="nw", window=self.playlist_radiobtn)


        self.link_entry = Entry(width=35)
        self.canvas_link_entry = self.canvas.create_window(200, 7, anchor="nw", window=self.link_entry)

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
        self.canvas_download_button = self.canvas.create_window(590, 4, anchor="ne", window=self.download_button)

        self.current_download_list = Listbox(height=18, width=30, exportselection=0)
        self.songs = (os.listdir("Downloads/"))
        for song in self.songs:
            self.current_download_list.insert(self.songs.index(song), song)

        self.current_download_list.bind("<<ListboxSelect>>", self.song_selection)
        self.canvas_download_list = self.canvas.create_window(20, 80, anchor="nw", window=self.current_download_list)

        self.similar_song_list = Listbox(height=18, width=30, exportselection=0)
        self.similar_song_list.insert(0, "No Information")
        self.similar_song_list.bind("<<ListboxSelect>>", self.song_detail_selection)
        self.canvas_songs_list = self.canvas.create_window(580,80, anchor="ne", window=self.similar_song_list)

        self.update_box = Text(height=3, width=70)
        self.update_box.config(state=DISABLED)
        self.canvas_update = self.canvas.create_window(20, 550, anchor="nw", window=self.update_box)
        self.window.mainloop()

    def purpose_selection(self):
        print(self.radio_state.get())

    def updates(self, message):
        self.update_box.config(state=NORMAL)
        self.update_box.insert(END, "\n{}".format(message))
        self.update_box.config(state=DISABLED)
        self.update_box.see(END)

    def download(self):
        url = self.link_entry.get()
        if not url == "":
            dload = d(url)
            status = dload.download_link()
            if not status == 0:
                self.updates("Download completed and converted")
                # Update downloaded list after downloading
                new_list = (os.listdir("Downloads/"))
                for song in new_list:
                    if song not in self.songs:
                        self.current_download_list.insert(new_list.index(song), song)
                        self.songs = new_list
                self.link_entry.delete(0, END)
            else:
                self.updates("This video/audio is unavailable for access!")
        else:
            self.updates("Please enter a link!")
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
            selected_info = self.results[self.current_download_list.curselection()[0]]
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
        #print(self.results[self.similar_song_list.curselection()[0]])
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