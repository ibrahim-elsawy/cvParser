import abc
from abc import ABC, abstractproperty,  abstractmethod


class Paragraph():

	def __init__(self, text) -> None:
		self.text = text



class ProcessBase(ABC): 
	
	@abstractmethod
	def process(self, data):
		pass