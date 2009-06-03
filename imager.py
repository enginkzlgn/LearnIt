#!/usr/bin/python
#coding:utf-8

import gtk 
import gtk.glade as Glade
import os,sys
from image_util import ResizableImage



image_file_extansions=["png","jpg","peg","ico"]

class Viewer(object):

	def __init__(self):
		self.is_full=0
		self.images=[]
		self.count=0
		self.glade = Glade.XML('imager/imager.glade','window')
		self.pencere = self.glade.get_widget('window')
		self.glade.signal_autoconnect(self)

		self.open = self.glade.get_widget('open')
		self.prev = self.glade.get_widget('prev')
		self.play = self.glade.get_widget('play')
		self.next = self.glade.get_widget('next')
		self.image_buttons_query()
		alan=self.glade.get_widget('alan')
		self.image_area=ResizableImage()
		alan.add(self.image_area)
		
		self.pencere.connect('key_press_event',self.key_press)
		self.pencere.connect('destroy',gtk.main_quit)
		self.pencere.set_size_request(300,300)
		self.pencere.show_all()
	def key_press(self,wid,ev):
		space_id=32
		backspace_id=65288
		F11=65480
		result=ev.keyval
		ev.time=0
		print result," key..."
		if result == space_id:
			self.go_next(0)
		elif result == backspace_id:
			self.go_prev(0)
		elif result == F11:
			if self.is_full == 0:
				self.pencere.fullscreen()
				self.is_full=1
			else:
				self.pencere.unfullscreen()
				self.is_full=0

	def image_buttons_query(self):
		is_active=False
		if len(self.images)>1:
			is_active=True
		else:
			is_active=False
		self.play.set_sensitive(is_active)
		self.prev.set_sensitive(is_active)
		self.next.set_sensitive(is_active)

	def go_prev(self,ev):
		if self.count == 0:
			self.count=len(self.images)-1
		else:
			self.count-=1
		self.set_image(self.count)

	
	def go_next(self,ev):
		if self.count==len(self.images)-1:
			self.count=0
		else:
			self.count+=1
		self.set_image(self.count)

	def play(self,ev):
		print "change the next image"


	def set_image(self,count=0):
		if len(self.images)>1:
			self.image_area.set_from_file(self.images[count])



			

		
	def import_files(self,path):
		if os.path.isdir(path):
			while len(self.images) != 0:
				self.images.pop()
			self.count=0
		
			for i in os.listdir(path):
				if i[0] is '.': continue
				if i[-3:].lower() in image_file_extansions:
					file = os.path.join(path,i)
					self.images.append(file)


		
	def open_directory(self,ev):
		folder_dialog = gtk.FileChooserDialog("Klasör Seç",
		self.pencere, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		("İptal", gtk.RESPONSE_CANCEL, "Seç", gtk.RESPONSE_OK))
		response = folder_dialog.run()
		if response == gtk.RESPONSE_OK:
			self.import_files( folder_dialog.get_filename())
			self.image_buttons_query()
		folder_dialog.destroy()
		self.set_image()
		self.image_buttons_query()





if __name__=="__main__":
	Viewer()
	gtk.main()
