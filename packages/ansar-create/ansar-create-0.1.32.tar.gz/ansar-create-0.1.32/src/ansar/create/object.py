# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".

.
"""
__docformat__ = 'restructuredtext'

import ansar.encode as ar

__all__ = [
	'LOG_NUMBER',
	'object_settings',
]

#
#
LOG_NUMBER = ar.Enumeration(FAULT=ar.USER_LOG_FAULT, WARNING=ar.USER_LOG_WARNING,
	CONSOLE=ar.USER_LOG_CONSOLE, OBJECT=ar.USER_LOG_OBJECT,
	TRACE=ar.USER_LOG_TRACE, DEBUG=ar.USER_LOG_DEBUG, NONE=ar.USER_LOG_NONE)

# Values that capture the details of a "call-sequence"
# passed to the running child, by a calling parent. In
# general the absence of these values implies a hand-rolled
# "call" from a command-line shell.
class ObjectSettings(object):
	"""Values that capture the details of a "call" between parent and child process.

	These are the values used to implement integration between parent and child
	processes. There are also values that are useful at the command-line, i.e.
	debug_level, help, dump_settings, dump_input, store_settings, store_input,
	settings_file, input_file and output_file are all available as command-line
	setttings (i.e. to dump the current input use --dump-input).

	:param call_signature: I/O expectations of the caller
	:type call_signature: "io", "i", "o" or None
	:param debug_level: NONE, DEBUG, TRACE, OBJECT, CONSOLE, WARNING, FAULT
	:type debug_level: str
	:param home_path: location of a process group
	:type home_path: str
	:param role_name: role within a process group
	:type role_name: str
	:param point_of_origin: context of execution - start, run or call (sub-process)
	:type point_of_origin: 0, 1, or 2
	:param help: enable output of help page
	:type help: bool
	:param dump_settings: enable output of current settings
	:type dump_settings: JSON representation
	:param dump_input: enable output of the stored input
	:type dump_input: JSON representation
	:param store_settings: enable saving of the current settings
	:type store_settings: bool
	:param store_input: enable saving of the current input
	:type store_input: bool
	:param settings_file: use the settings in the specified file
	:type settings_file: str
	:param input_file: use the input in the specified file
	:type input_file: str
	:param output_file: place any output in the specified file
	:type output_file: str
	"""
	def __init__(self,
			call_signature=None,				# All scenarios.
			debug_level=None,
			home_path=None, role_name=None,		# Fully-homed only.
			point_of_origin=2,					# Variants on home execution.
			help=False,							# Administrative features.
			dump_settings=False,
			dump_input=False,
			store_settings=False, store_input=False, reset_to_factory_settings=False,
			settings_file=None, input_file=None,
			output_file=None):
		self.call_signature = call_signature
		self.debug_level = debug_level
		self.home_path = home_path
		self.role_name = role_name
		self.point_of_origin = point_of_origin
		self.help = help
		self.dump_settings = dump_settings
		self.dump_input = dump_input
		self.store_settings = store_settings
		self.store_input = store_input
		self.reset_to_factory_settings = reset_to_factory_settings
		self.settings_file = settings_file
		self.input_file = input_file
		self.output_file = output_file

	def homed(self):
		if self.home_path and self.role_name:
			return True
		return False

OBJECT_SETTINGS_SCHEMA = {
	'call_signature': ar.Unicode(),
	'debug_level': LOG_NUMBER,
	'home_path': ar.Unicode(),
	'role_name': ar.Unicode(),
	'point_of_origin': ar.Integer8(),
	'help': ar.Boolean(),
	'dump_settings': ar.Boolean(),
	'dump_input': ar.Boolean(),
	'store_settings': ar.Boolean(),
	'store_input': ar.Boolean(),
	'reset_to_factory_settings': ar.Boolean(),
	'settings_file': ar.Unicode(),
	'input_file': ar.Unicode(),
	'output_file': ar.Unicode(),
}

ar.bind(ObjectSettings, object_schema=OBJECT_SETTINGS_SCHEMA)

object_settings = ObjectSettings()
