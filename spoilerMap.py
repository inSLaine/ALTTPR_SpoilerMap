from kivy.config import Config
from kivy.core.window import Window
import kivy

kivy.config.Config.set('graphics','resizable', 1)
kivy.config.Config.set('graphics','borderless', 0)
Window.size = (700, 700)
Config.write()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from  kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
import time
import os
from kivy.lang import Builder
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import configparser
import re



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

	def setBottles(self, x):
		if(x[1] in bottleItems):
			x[1] = 'Bottle{}'.format(countRepeatItems['bottleCount'])
			countRepeatItems['bottleCount'] += 1
			return x
		else:
			return x
			
	def setSwords(self, x):
		if(x[1] == "ProgressiveSword"):
			x[1] = 'ProgressiveSword{}'.format(countRepeatItems['progSword'])
			countRepeatItems['progSword'] += 1
			return x
		else:
			return x
			
	def setGloves(self, x):
		if(x[1] == "ProgressiveGlove"):
			x[1] = 'ProgressiveGlove{}'.format(countRepeatItems['progGlove'])
			countRepeatItems['progGlove'] += 1
			return x
		else:
			return x
	
	def on_size(self, *args):
		Window.size = (Window.height, Window.height)
		Window.size = (Window.width, Window.width)
		
	def lightWorldLocations(self):
		f = open('itemLocations/lightWorldLocations.txt', 'r')
		for line in f:
			x = line.split(':')
			lightWorldLocations[x[0]] = (int(x[1])/mapWidth, 1 - int(x[2])/mapHeight)
			
	def darkWorldLocations(self):
		f = open('itemLocations/darkWorldLocations.txt', 'r')
		for line in f:
			x = line.split(':')
			darkWorldLocations[x[0]] = (int(x[1])/mapWidth, 1 - int(x[2])/(mapHeight))
		
	def placeWorldItems(self):
		for each in requiredItems:
			x = Image(source='artAssets/{}.png'.format(each))
			x.allow_stretch = True
			x.keep_ratio = True
			x.size_hint = (.03,.03)
			if(allWorldItems[each] in lightWorldLocations):
				x.pos_hint = {'center_x':lightWorldLocations[allWorldItems[each]][0],'center_y':lightWorldLocations[allWorldItems[each]][1]}
				x.reload()
				self.ids.lightWorldPage.add_widget(x,1)
			elif(allWorldItems[each] in darkWorldLocations):
				x.pos_hint = {'center_x':darkWorldLocations[allWorldItems[each]][0],'center_y':darkWorldLocations[allWorldItems[each]][1]}
				x.reload()
				self.ids.darkWorldPage.add_widget(x,1)
			else:
				pass

	def chooseFile(self):
		Tk().withdraw()
		filename = askopenfilename()
		f = open(filename, 'r')
		for line in f:
			cleanLine = line.strip()
			noSpace = re.sub('\s+', '', cleanLine)
			noQuote = re.sub('"', '', noSpace)
			noOBrack = re.sub('{', '', noQuote)
			noCBrack = re.sub('}', '', noOBrack)
			noParens = re.sub('\(([^)]+)\)', '', noCBrack)
			purgedLine = re.sub(',', '', noParens)
			if ":" in purgedLine:
				x = purgedLine.split(':')
				x = self.setBottles(x)
				x = self.setSwords(x)
				x = self.setGloves(x)
				allWorldItems[x[1]] = x[0]
		self.lightWorldLocations()
		self.darkWorldLocations()
		self.placeWorldItems()
				
	pass
	

class spoilerMap(App):
	def build(self):
		
		return screenMan()
		
if __name__ == '__main__':
    spoilerMap().run()