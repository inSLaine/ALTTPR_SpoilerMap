import kivy
import tkinter
import time
import sys
import os
import configparser
import re
from kivy.config import Config
from kivy.core.window import Window

# kivy.config.Config.set('graphics','resizable', 1)
# kivy.config.Config.set('graphics','borderless', 0)
# Window.size = (700, 700)
# Config.write()

from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image

if getattr(sys, 'frozen', False):
# we are running in a |PyInstaller| bundle
	base_path = sys._MEIPASS


from kivy.lang import Builder
from tkinter import Tk
from tkinter.filedialog import askopenfilename


mapWidth = 4000
mapHeight = 4000


countRepeatItems = {
	'bottleCount': 1,
	'progSword': 1,
	'progGlove': 1
}


lightWorldLocations = {
	}
	
darkWorldLocations = {
	}

allWorldItems = {
}
miscItems = ['','']

requiredItems = ['MoonPearl','Bottle1','Bottle2','Bottle3','Bottle4','ProgressiveSword1','ProgressiveSword2',
'ProgressiveSword3','ProgressiveSword4','Cape','FireRod','Shovel',
'Hammer','Flippers','ProgressiveGlove1','ProgressiveGlove2','Lamp',
'BookOfMudora','IceRod','Bow','Ether','Bombos','Quake','OcarinaInactive',
'MagicMirror','Hookshot','CaneOfSomaria','PegasusBoots','Mushroom','SilverArrowUpgrade']

bottleItems = ['BottleWithGreenPotion','BottleWithFairy','BottleWithRedPotion','BottleWithBluePotion','Bottle','BottleWithGoldenBee']

#Main Window / Canvas
class screenMan(ScreenManager):

	Window.size = (600,600)
	
	def on_touch_up(self, touch):
		if touch.is_mouse_scrolling:
			if touch.button == 'scrolldown':
				if(self.ids.lightScatter.scale < 4):
					self.ids.lightScatter.scale = self.ids.lightScatter.scale * 1.2
					self.ids.darkScatter.scale = self.ids.darkScatter.scale * 1.2
				pass
			elif touch.button == 'scrollup':
				if(self.ids.lightScatter.scale > 1):
					self.ids.lightScatter.scale = self.ids.lightScatter.scale * 0.8
					self.ids.darkScatter.scale = self.ids.darkScatter.scale * 0.8
				pass
				
	def zoomMap(self):
		pass
		# if touch.is_mouse_scrolling:
			# if touch.button == 'scrolldown':
				# print('down')
				# ## zoom in
				# if self.scale < 10:
					# self.scale = self.scale * 1.1

		# elif touch.button == 'scrollup':
			# ## zoom out
			# print('up')
			# if self.scale > 1:
				# self.scale = self.scale * 0.8

	def resource_path(self, relative_path):
		""" Get absolute path to resource, works for dev and for PyInstaller """
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")

		return os.path.join(base_path, relative_path)

	def setBottles(self, y):
		if(y in bottleItems):
			y = 'Bottle{}'.format(countRepeatItems['bottleCount'])
			countRepeatItems['bottleCount'] += 1
			return y
		else:
			return y
			
	def setSwords(self, y):
		if(y == "ProgressiveSword"):
			y = 'ProgressiveSword{}'.format(countRepeatItems['progSword'])
			countRepeatItems['progSword'] += 1
			return y
		else:
			return y
			
	def setGloves(self, y):
		if(y == "ProgressiveGlove"):
			y = 'ProgressiveGlove{}'.format(countRepeatItems['progGlove'])
			countRepeatItems['progGlove'] += 1
			return y
		else:
			return y
	
	def on_size(self, *args):
		w = Window.width
		h = Window.height
		Window.size = (w, h)
		
	def lightWorldLocations(self):
		f = open((self.resource_path('itemLocations/lightWorldLocations.txt')), 'r')
		for line in f:
			x = line.split(':')
			lightWorldLocations[x[0]] = (int(x[1])/mapWidth, 1 - int(x[2])/mapHeight)
			
	def darkWorldLocations(self):
		f = open((self.resource_path('itemLocations/darkWorldLocations.txt')), 'r')
		for line in f:
			x = line.split(':')
			darkWorldLocations[x[0]] = (int(x[1])/mapWidth, 1 - int(x[2])/(mapHeight))
		
	def placeWorldItems(self):
		for each in requiredItems:
			x = Image(source=self.resource_path('artAssets/{}.png'.format(each)))
			x.allow_stretch = True
			x.keep_ratio = True
			x.size_hint = (.03,.03)
			if(allWorldItems[each] in lightWorldLocations):
				x.pos_hint = {'center_x':lightWorldLocations[allWorldItems[each]][0],'center_y':lightWorldLocations[allWorldItems[each]][1]}
				x.text = '{}:{}'.format(each, allWorldItems[each])
				x.reload()
				self.ids.lightScatter.add_widget(x,0)
			elif(allWorldItems[each] in darkWorldLocations):
				x.pos_hint = {'center_x':darkWorldLocations[allWorldItems[each]][0],'center_y':darkWorldLocations[allWorldItems[each]][1]}
				x.reload()
				self.ids.darkScatter.add_widget(x,0)
			else:
				pass

	def chooseFile(self):
		Tk().withdraw()
		filename = askopenfilename()
		f = open(filename, 'r')
		for line in f:
			cleanLine = line.strip()
			noSpace = re.sub('', '', cleanLine)
			noQuote = re.sub('"', '', noSpace)
			noOBrack = re.sub('{', '', noQuote)
			noCBrack = re.sub('}', '', noOBrack)
			noParens = re.sub('\(([^)]+)\)', '', noCBrack)
			purgedLine = re.sub(',', '', noParens)
			if ":" in purgedLine:
				x = purgedLine.split(':')
				y = re.sub('\s+', '', x[1])
				y = self.setBottles(y)
				y = self.setSwords(y)
				y = self.setGloves(y)	
				allWorldItems[y] = x[0]
		self.lightWorldLocations()
		self.darkWorldLocations()
		self.placeWorldItems()
				
	pass
	

class spoilerMap(App):
	def build(self):
	


		
		return screenMan()
		
if __name__ == '__main__':
	spoilerMap().run()