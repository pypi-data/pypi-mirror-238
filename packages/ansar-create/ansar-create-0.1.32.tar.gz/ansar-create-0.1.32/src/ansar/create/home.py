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

"""An operational environment for a collection of processes.

"""
__docformat__ = 'restructuredtext'

import os
import sys
import uuid
import ansar.encode as ar
from .coding import breakpath
from .retry import RetryIntervals
from .lifecycle import HostPort

__all__ = [
	'FULL_SERVICE',
	'TOOL_SERVICE',
	'Homebase',
]

# Name of the redirect file, i.e. if it exists then it contains the
# absolute path of where expected materials can be found, rather than
# in the folder containing the redirect.
REDIRECT = '.redirect'

class StartStop(object):
	def __init__(self, start=None, stop=None, returned=None):
		self.start = start
		self.stop = stop
		self.returned = returned

START_STOP_SCHEMA = {
	"start": ar.WorldTime,
	"stop": ar.WorldTime,
	"returned": ar.Any,
}

ar.bind(StartStop, object_schema=START_STOP_SCHEMA)

STARTING_AND_STOPPING = 8

# Services provided;
# bin ....... executable files
# entry ..... name for a process
# settings .. persistent configuration
# input ..... default arguments
# logs ...... records of activity
# resource .. read-only per-executable materials
# tmp ....... cleared on start
# model ..... persistent, compiled materials

FULL_SERVICE = ['bin', 'entry', 'settings', 'input', 'logs', 'resource', 'tmp', 'model', 'properties']
TOOL_SERVICE = ['settings', 'resource', 'properties']

# TFV
COMPONENT_PROPERTIES = {
	"executable": ar.Unicode,
	"retry": ar.UserDefined(RetryIntervals),
}

def get_decoration(p, s, t):
	if p is None:
		f = None
		v = None
	else:
		f = p.file(s, t)
		try:
			v, _ = f.recover()
		except ar.FileNotFound:
			v = None
	return [t, f, v]

def set_decoration(p, s, t, v):
	if p is None:
		f = None
	else:
		f = p.file(s, t)
		if v is not None:
			f.store(v)
	return [t, f, v]

class Homebase(object):
	def __init__(self):
		self.plan = None

		# Always available
		self.home_path = None		# Full path to location of.
		self.home_name = None		# Shortened name.
		self.home = None			# Folder at path.
		self.home_id = None			# Unique identity.

		# Available services.
		self.bin = None
		self.entry = None
		self.settings = None
		self.input = None
		self.logs = None
		self.resource = None
		self.tmp = None
		self.model = None
		self.properties = None

		# Every role
		self.role_executable = None		# Decoration.
		self.role = None				# Full, dotted name.
		self.role_name = None			# Shortened name.
		self.role_settings = None		# Decoration.
		self.role_logs = None			# Folder access to records.
		self.role_resource = None		# Instance access to read-only executable materials.
		self.role_tmp = None			# ... to cleared space.
		self.role_model = None			# ... to saved space.
		self.role_properties = None		# Folder

		self.store = lambda : False

		# Single-level role.
		self.role_entry = None			# Folder for locks, etc
		self.role_retry = None
		self.role_start_stop = None		# Decoration.
		self.role_input = None

		self.role_storage = None
		self.role_connect_above = None
		self.role_accept_below = None
		self.role_directory_scope = None

		# Role executable,
		self.executable_resource = None

		# Hold some data from command line.
		self.environment_variables = None
		self.command_executable = None
		self.command_words = None
		self.command_input = None

		# Prepared materials for startup of
		# other executables, i.e. class Process.
		self.bin_path = None
		self.bin_env = None

	# Set of queries that provide for create/open of a complex,
	# persistent object. Each step creates new folders+files or
	# recovers existing materials, returning progress indicators
	# and building an image of what is present on disk.

	def basic_plan(self, path, plan=FULL_SERVICE):
		'''Build an in-memory, read-only sketch of the static elements.'''
		self.plan = plan

		path = os.path.abspath(path)
		b = breakpath(path)
		self.home_path = path
		self.home_name = b[1]
		self.home = ar.Folder(path, auto_create=False)

		def if_required(service):
			if service not in plan:
				return None
			return self.home.folder(service)

		# Create the base set of expected folder objects.
		self.bin = if_required('bin')
		self.resource = if_required('resource')
		self.entry = if_required('entry')
		self.settings = if_required('settings')
		self.input = if_required('input')
		self.logs = if_required('logs')
		self.tmp = if_required('tmp')
		self.model = if_required('model')
		self.properties = if_required('properties')

	def plan_exists(self):
		'''Compare the in-memory sketch against the disk reality.'''
		leaf = [
			self.bin, self.resource, self.entry, self.settings, self.input,
			self.logs, self.tmp, self.model, self.properties
		]
		for f in leaf:
			if f and not f.exists():
				return False
		return True

	def ready_for_subprocessing(self):
		'''Prepare materials for anyone wanting to start a sub-process.'''
		bin_env = dict(os.environ)
		old = bin_env.get('PATH', None)
		if old:
				bin_path = '%s:%s' % (self.bin.path, old)
		else:
				bin_path = self.bin.path
		bin_env['PATH'] = bin_path
		self.bin_path = bin_path
		self.bin_env = bin_env

	def create_plan(self, redirect, default_bin):
		'''Create links to external locations and switch to writable folders.'''
		self.home = ar.Folder(self.home.path)

		# Give this new environment a unique id and make it available
		# to every subsequent client.
		self.home_id = set_decoration(self.home, 'id', ar.UUID(), uuid.uuid4())

		# If codepath provides a default location for executables,
		# i.e. a manual command-line, and there is no explicit redirect
		# then adopt that default.
		if default_bin and 'bin' not in redirect:
			redirect['bin'] = default_bin

		# Function that honours redirects and creates the necessary
		# folders and support materials (e.g. a back-link).
		def follow(location, read_only=False):
			if location is None:
				return None
			location = ar.Folder(location.path)
			b = breakpath(location.path)
			try:
				over = redirect[b[1]]
			except KeyError:
				return location
			f = location.file(REDIRECT, str)
			# Distinct treatment for folders that can/cant be safely
			# shared by multiple components.
			if not read_only:
				s = str(self.home_id[2])
				s = 'ansar-%s-%s' % (b[1], s)
				over = os.path.join(over, s)	# A per-id folder at external location.
			f.store(over)
			location = ar.Folder(over)
			if read_only:
				return location
			#f = location.file('.ansar-origin', str)	 # Include a back-link.
			#file_decoration(f, self.home.path)
			set_decoration(location, '.ansar-origin', str, self.home.path)
			return location

		# Establish the essential elements of a home.
		self.bin = follow(self.bin, read_only=True)
		self.settings = follow(self.settings)
		self.input = follow(self.input)
		self.logs = follow(self.logs)
		self.resource = follow(self.resource, read_only=True)
		self.tmp = follow(self.tmp)
		self.model = follow(self.model)
		self.entry = follow(self.entry)
		self.properties = follow(self.properties)

		# Build support materials for lookup/verification of
		# entry executables.
		if self.bin:
			self.ready_for_subprocessing()

	def open_plan(self):
		'''Follow existing links to external locations and switch to writable folders.'''
		self.home_id = get_decoration(self.home, 'id', ar.UUID())

		def follow(location, read_only=False):
			if location is None:
				return None
			location = ar.Folder(location.path)
			f = location.file(REDIRECT, str)
			try:
				path, _ = f.recover()
			except ar.FileNotFound:
				return location
			location = ar.Folder(path)
			return location

		self.bin = follow(self.bin, read_only=True)
		self.settings = follow(self.settings)
		self.input = follow(self.input)
		self.logs = follow(self.logs)
		self.resource = follow(self.resource, read_only=True)
		self.tmp = follow(self.tmp)
		self.model = follow(self.model)
		self.entry = follow(self.entry)
		self.properties = follow(self.properties)

		if self.bin:
			self.ready_for_subprocessing()

	def destroy_plan(self):
		'''Explicit clearance of folders that may be redirected and not read-only.'''

		self.settings and ar.remove_folder(self.settings.path)
		self.input and ar.remove_folder(self.input.path)
		self.logs and ar.remove_folder(self.logs.path)

		self.tmp and ar.remove_folder(self.tmp.path)
		self.model and ar.remove_folder(self.model.path)
		self.properties and ar.remove_folder(self.properties.path)

		self.home and ar.remove_folder(self.home.path)

	def runs_from_bin(self, pfe):
		'''Verify that the presented executable is within the proper location.'''
		if pfe[0] != self.bin.path:
			fe = pfe[1] + pfe[2]
			raise ValueError('executable "%s" (%s) is outside "%s"' % (fe, pfe[0], self.bin.path))

	def role_exists(self, role):
		'''Create extensions based on the assigned role.'''
		if not role:
			raise ValueError('null/empty role')
		r = role.split('.')
		self.role = role
		self.role_name = r[0]

		def if_required(f):
			if f is None:
				return None
			return f.folder(role, auto_create=False)

		self.role_logs = if_required(self.logs)
		self.role_tmp = if_required(self.tmp)
		self.role_model = if_required(self.model)
		self.role_properties = if_required(self.properties)

		def if_exists(f):
			if f is None:
				return True
			return f.exists()

		return if_exists(self.role_logs) and if_exists(self.role_tmp) and if_exists(self.role_model) and if_exists(self.role_properties)

	def create_role(self, executable, settings, input, retry=None, storage=None):
		def if_required(f):
			if f is None:
				return None
			return ar.Folder(f.path)

		self.role_logs = if_required(self.role_logs)
		self.role_tmp = if_required(self.role_tmp)
		self.role_model = if_required(self.role_model)
		self.role_properties = if_required(self.role_properties)

		self.role_executable = set_decoration(self.role_properties, 'executable', ar.Unicode(), executable)

		if settings is not None and self.settings:
			self.role_settings = set_decoration(self.settings, self.role, ar.UserDefined(type(settings)), settings)

		if self.role_name == self.role and input is not None and self.input:
			toi = ar.fix_expression(type(input), {})
			self.role_input = set_decoration(self.input, self.role, toi, input)

		if self.role == self.role_name and self.entry:
			self.role_entry = self.entry.folder(self.role_name)
			self.role_retry = set_decoration(self.role_entry, 'retry', ar.UserDefined(RetryIntervals), retry)
			self.role_start_stop = set_decoration(self.role_entry, 'start-stop', ar.DequeOf(StartStop), ar.deque())

		if self.role_properties:
			if storage:
				self.role_storage = set_decoration(self.role_properties, 'storage', ar.Integer8(), storage)
			self.role_connect_above = set_decoration(self.role_properties, 'connect-above', ar.Any(), None)
			self.role_accept_below = set_decoration(self.role_properties, 'accept-below', ar.UserDefined(HostPort), None)
			self.role_directory_scope = set_decoration(self.role_properties, 'directory-scope', int, None)

		if self.resource:
			self.executable_resource = self.resource.folder(executable)

	def open_role(self, settings, input, retry=None, storage=None):
		def if_required(f):
			if f is None:
				return None
			return ar.Folder(f.path)

		self.role_logs = if_required(self.role_logs)
		self.role_tmp = if_required(self.role_tmp)
		self.role_model = if_required(self.role_model)
		self.role_properties = if_required(self.role_properties)

		self.role_executable = get_decoration(self.role_properties, 'executable', ar.Unicode())

		if settings and self.settings:
			self.role_settings = get_decoration(self.settings, self.role, ar.UserDefined(type(settings)))

		if input and self.input:
			toi = ar.fix_expression(type(input), {})
			self.role_input = get_decoration(self.input, self.role, toi)

		if self.role_tmp:
			ar.remove_contents(self.role_tmp.path)

		if self.role == self.role_name and self.entry:
			self.role_entry = self.entry.folder(self.role_name)
			if retry is None:
				self.role_retry = get_decoration(self.role_entry, 'retry', ar.UserDefined(RetryIntervals))
			else:
				self.role_retry = set_decoration(self.role_entry, 'retry', ar.UserDefined(RetryIntervals), retry)
			self.role_start_stop = get_decoration(self.role_entry, 'start-stop', ar.DequeOf(StartStop))

		if self.role_properties:
			if storage is None:
				self.role_storage = get_decoration(self.role_properties, 'storage', ar.Integer8())
			else:
				self.role_storage = set_decoration(self.role_properties, 'storage', ar.Integer8(), storage)
			self.role_connect_above = get_decoration(self.role_properties, 'connect-above', ar.Any())
			self.role_accept_below = get_decoration(self.role_properties, 'accept-below', ar.UserDefined(HostPort))
			self.role_directory_scope = get_decoration(self.role_properties, 'directory-scope', int)

		if self.resource:
			executable = self.role_executable[2] or breakpath(sys.argv[0])[1]
			self.executable_resource = self.resource.folder(executable)

	def executable_name(self):
		name = os.path.join(self.bin.path, self.role_executable[2])
		return name

	def delete_role(self, role):
		'''.'''

		self.role_logs and ar.remove_folder(self.role_logs.path)
		self.role_tmp and ar.remove_folder(self.role_tmp.path)
		self.role_model and ar.remove_folder(self.role_model.path)

		if self.role_entry:
			ar.remove_folder(self.role_entry.path)
		try:
			# TBF - hard-coded extent.
			s = os.path.join(self.settings.path, self.role + '.json')
			os.remove(s)
		except FileNotFoundError:
			pass
		if self.input:
			try:
				# TBF - hard-coded extent.
				s = os.path.join(self.input.path, self.role + '.json')
				os.remove(s)
			except FileNotFoundError:
				pass

	def self_storage(self, settings):
		self.role_settings[2] = settings
		def store():
			try:
				self.role_settings[1].store(settings)
			except ar.FileFailure as e:
				return False
			return True
		self.store = store

	def verify(self):
		folder = (
			self.bin,
			self.role_logs,
			self.executable_resource,
			self.role_tmp,
			self.role_model,
		)

		for f in folder:
			if f is not None and not f.exists():
				s = 'Location "%s" not found' % (f.path,)
				raise ValueError(s)

	def entry_list(self):
		for f in os.listdir(self.entry.path):
			p = os.path.join(self.entry.path, f)
			if os.path.isdir(p):
				yield f

	def entry_started(self):
		if self.role_start_stop is None:
			return
		start_stop = self.role_start_stop[2]
		s = StartStop(start=ar.world_now())
		start_stop.append(s)
		n = len(start_stop)
		if n > STARTING_AND_STOPPING:
			for i in range(STARTING_AND_STOPPING, n):
				start_stop.popleft()
		self.role_start_stop[1].store(start_stop)

	def entry_returned(self, returned):
		if self.role_start_stop is None:
			return
		start_stop = self.role_start_stop[2]
		if not start_stop:  # Not present or empty.
			return
		s = start_stop[-1]
		if s.stop is not None:  # Already stopped.
			return
		s.stop = ar.world_now()
		s.returned = returned
		self.role_start_stop[1].store(start_stop)

	def home_role(self, path, role, settings, input, plan=FULL_SERVICE,
			#create_home=False, create_role=False,
			redirect={}, default_bin=None, executable=None, retry=None):
		self.basic_plan(path, plan=plan)
		if not self.plan_exists():
			#if not create_home:
			#	fault = 'home at "{path}" does not exist or is incomplete'.format(path=path)
			#	raise RuntimeError(fault)
			self.create_plan(redirect, default_bin)
		else:
			self.open_plan()
		if role is None:
			return
		if not self.role_exists(role):
			#if not create_role:
			#	fault = '"{role}" ({path}) does not exist or has unexpected contents'.format(role=role, path=hb.home_path)
			#	raise RuntimeError(fault)
			self.create_role(executable, settings, input, retry=retry)
		else:
			self.open_role(settings, input, retry=retry)
