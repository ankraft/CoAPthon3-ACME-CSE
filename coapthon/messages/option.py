#
#	option.py
#
#	This is a patched version of the CoAPthon serializer.py file.
#
#	Original auhtor: Giacomo Tanganelli
#	Patches by: Andreas Kraft
#
#	see https://github.com/Tanganelli/CoAPthon3
#
#
#	Overview about the patches:
#
#	- added __repl__ method
#

from coapthon import defines
from coapthon.utils import byte_len

__author__ = 'Giacomo Tanganelli'


class Option(object):
	"""
	Class to handle the CoAP Options.
	"""
	def __init__(self):
		"""
		Data structure to store options.
		"""
		self._number = None
		self._value = None

	@property
	def number(self):
		"""
		Return the number of the option.

		:return: the option number
		"""
		return self._number

	@number.setter
	def number(self, value):
		"""
		Set the option number.

		:type value: int
		:param value: the option number
		"""
		self._number = value

	@property
	def value(self):
		"""
		Return the option value.

		:return: the option value in the correct format depending on the option
		"""
		if type(self._value) is None:
			self._value = bytes()
		opt_type = defines.OptionRegistry.LIST[self._number].value_type
		if opt_type == defines.INTEGER:
			if byte_len(self._value) > 0:
				return int(self._value)
			else:
				return defines.OptionRegistry.LIST[self._number].default
		return self._value

	@value.setter
	def value(self, value):
		"""
		Set the value of the option.

		:param value: the option value
		"""
		opt_type = defines.OptionRegistry.LIST[self._number].value_type
		if opt_type == defines.INTEGER:
			if type(value) is not int:
				value = int(value)
			if byte_len(value) == 0:
				value = 0
		elif opt_type == defines.STRING:
			if type(value) is not str:
				value = str(value)
		elif opt_type == defines.OPAQUE:
			if type(value) is bytes:
				pass
			else:
				if value is not None:
					value = bytes(value, "utf-8")
		self._value = value

	@property
	def length(self):
		"""
		Return the value length

		:rtype : int
		"""
		if isinstance(self._value, int):
			return byte_len(self._value)
		if self._value is None:
			return 0
		return len(self._value)

	def is_safe(self):
		"""
		Check if the option is safe.

		:rtype : bool
		:return: True, if option is safe
		"""
		if self._number == defines.OptionRegistry.URI_HOST.number \
				or self._number == defines.OptionRegistry.URI_PORT.number \
				or self._number == defines.OptionRegistry.URI_PATH.number \
				or self._number == defines.OptionRegistry.MAX_AGE.number \
				or self._number == defines.OptionRegistry.URI_QUERY.number \
				or self._number == defines.OptionRegistry.PROXY_URI.number \
				or self._number == defines.OptionRegistry.PROXY_SCHEME.number:
			return False
		return True

	@property
	def name(self):
		"""
		Return option name.

		:rtype : String
		:return: the option name
		"""
		return defines.OptionRegistry.LIST[self._number].name

	def __str__(self):
		"""
		Return a string representing the option

		:rtype : String
		:return: a message with the option name and the value
		"""
		return self.name + ": " + str(self.value)


	def __repr__(self):
		"""
		Return a string representing the option

		:rtype : String
		:return: a message with the option name and the value
		"""
		return self.__str__()

  
	def __eq__(self, other):
		"""
		Return True if two option are equal

		:type other: Option
		:param other: the option to be compared against
		:rtype : Boolean
		:return: True, if option are equal
		"""
		return self.__dict__ == other.__dict__
