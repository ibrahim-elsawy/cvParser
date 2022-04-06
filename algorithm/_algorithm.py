import abc
from abc import  ABC, abstractmethod


class AlgorithmBase(ABC):

	@abstractmethod
	def apply(self, data):
		pass