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

"""Implementation of a standard async process.

Essentially the ``create_object()`` function with a few related functions
and classes.
"""
__docformat__ = 'restructuredtext'

import os
import sys
import signal
import io
import time
import ansar.encode as ar
from .root import start_up, tear_down
from .coding import breakpath
from .space import set_queue, get_queue_address, Completion
from .point import pt
from .lifecycle import Ready, ExitCode, Completed, Stop, Aborted, Faulted, Ack
from .binding import bind_any
from .log import log_to_nowhere, select_logs
from .rolling import RollingLog, LINES_IN_FILE
from .home import Homebase, TOOL_SERVICE
from .locking import lock_and_hold
from .retry import Retry
from .args import command_args, extract_args, arg_values, environment_variables
from .object import LOG_NUMBER, object_settings

__all__ = [
	'ComponentFailed',
	'hb',
	'create_object',
	'command_executable',
	'command_words',
	'command_input',
	'command_settings'
	'store_settings',
	'resource_folder'
	'tmp_folder'
	'model_folder'
	'resource_path'
	'tmp_path'
	'model_path'
]

#
#
class SilentExit(Exception):
	pass

class ObjectError(Exception):
	def __init__(self, condition, explanation=None):
		if explanation is None:
			message = condition
		else:
			message = '{condition} ({explanation})'.format(condition=condition, explanation=explanation)
		Exception.__init__(self, message)

class OperatorError(ObjectError):
	def __init__(self, condition, explanation=None):
		ObjectError.__init__(self, condition, explanation=explanation)

class ParentError(ObjectError):
	def __init__(self, condition, explanation=None):
		ObjectError.__init__(self, condition, explanation=explanation)

#
#
class ComponentFailed(Exception):
	def __init__(self, condition, explanation):
		Exception.__init__(self)
		self.condition = condition
		self.explanation = explanation

	def __str__(self):
		if self.explanation is None:
			s = '%s' % (self.condition,)
		else:
			s = '%s (%s)' % (self.condition, self.explanation)
		return s

# Fragments of supporting code that work between the
# platform and the object.
A0 = breakpath(sys.argv[0])[1]

def print_out(f, **kw):
	if kw:
		f = f.format(**kw)
	sys.stderr.write(f)

def silent_exit(code=0):
	sys.exit(code)

def error_exit(e, code=None, **kw):
	if kw:
		e = e.format(**kw)
	sys.stderr.write('{a0}: '.format(a0=A0))
	sys.stderr.write(e)
	sys.stderr.write('\n')
	if code is None:
		return
	sys.exit(code)

def file_decoding(name, t):
	f = ar.File(name, t, decorate_names=False)
	d = f.recover()
	return d

def input_decoding(t):
	utf8 = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='strict')
	input = utf8.read()

	codec = ar.CodecJson()
	d = codec.decode(input, t)
	return d

def file_encoding(name, value, t):
	f = ar.File(name, t, decorate_names=False)
	f.store(value)

def settings_recover(f, compiled):
	try:
		settings, v = f.recover()
		return settings, v
	except ar.FileNotFound:
		pass

	try:
		f.store(compiled)
	except ar.FileFailure:
		return None, None
	return compiled, None

def output_encoding(output, e):
	encoding = ar.CodecJson(pretty_format=True)
	e = encoding.encode(output, e)
	sys.stdout.write(e)
	sys.stdout.write('\n')

def output_exit(output, code=None):
	output_encoding(output, ar.Any())
	if code is None:
		return
	sys.exit(code)

# Generate some help for command-line users,
# extracted from the settings class.
STANDARD_SYNOPSIS = '''
	$ %s [--<name>=<value> ...] \\
		[-<character>=<value> ...] \\
		[word ...]

There are zero or more settings passed to the command, and zero or
more words (e.g. file names). The <name> in the long-form setting is
matched to a member in the command settings and the <value> is assumed
to be a JSON encoding appropriate to that member. Refer to the SETTINGS
section for details on each member.

The short-form option uses a <character> to match an initial character
of a member in the command settings. Any ambiguity arising from multiple
matches results in a diagnostic and exit. Adopting the long-form avoids
this issue. The <value> is processed in the same manner for both long-
and short-form settings.

If the command expects an input object this is passed as one or
more words (e.g. file names) or on stdin. Reading of stdin is triggered
by the lack of any words.
'''

STANDARD_SAMPLE = '''A full encoding of the settings is presented below. This includes examples
of the JSON encodings that can be used as the <value> when passing a
setting on the command-line.

Presenting correct JSON encodings on a command line can become difficult
where complex data types are involved, and JSON syntax overlaps with
command-line syntax. For this reason quotes around encodings for types
such as Python str are automatically provided, e.g. --who=John will
set the "who" member to the str value "John". This automation does not
apply to a str that appears as part of a more complex encoding. Multi-line
encodings for values such as lists and sets can generally be collapsed
into a single-line. Consult a JSON reference for full details on the
handling of whitespace.
'''

# A console request for info about a component.
def settings_help(s):
	def not_available(reason):
		error_exit('no help available ({reason})', reason=reason, code=1)

	# Extract some reasonable documentation.
	if s is None:
		not_available('no defined settings')
	tos = type(s)

	not_documented = 'settings not documented'
	try:
		settings_doc = tos.__doc__
		init_doc = tos.__init__.__doc__
	except AttributeError:
		not_available(not_documented)

	if not settings_doc or not init_doc:
		not_available(not_documented)

	# Clean up the source comments.
	synopsis = settings_doc.split('\n')
	synopsis = [s.strip() for s in synopsis]
	if len(synopsis) > 2 and synopsis[0] and not synopsis[1]:
		tagline = synopsis[0]
		description = synopsis[2:]
	else:
		tagline = None
		description = synopsis
	while description and not description[-1]:
		description.pop()

	arguments = init_doc.split('\n')
	arguments = [a.strip() for a in arguments]

	arg = {}
	notes = []
	for a in arguments:
		if a.startswith('* '):
			notes = []
			arg[a[2:]] = notes
			continue
		if a:
			notes.append(a)

	# Presentation
	print_out('NAME\n')
	if tagline:
		print_out('{name} - {tagline}\n', name=A0, tagline=tagline)
	else:
		print_out('{name}\n', name=A0)
	print_out('\n')
	print_out('SYNOPSIS\n')
	print_out(STANDARD_SYNOPSIS % (A0,))
	print_out('\n')
	print_out('DESCRIPTION\n')
	for d in description:
		print_out('{line}\n', line=d)
	print_out('\n')
	print_out('SETTINGS\n')
	schema = tos.__art__.value
	for k, v in schema.items():
		print_out('--{member}=<{proto}>\n', member=k, character=k[0], proto=ar.type_to_text(v))
		try:
			notes = arg[k]
		except KeyError:
			continue
		for n in notes:
			print_out(n)
			print_out('\n')
		print_out('\n')
	print_out('SAMPLE\n')
	print_out(STANDARD_SAMPLE)
	eos = ar.UserDefined(tos)
	fake = ar.fake(eos)

	encoding = ar.CodecJson(pretty_format=True)
	sample = encoding.encode(fake, eos)
	print_out('\n')
	print_out(sample)
	print_out('\n')

# A console request for a copy of the current configuration.
# Generate the JSON encoding and place on stdout.
def dump_settings(settings):
	output_encoding(settings, ar.UserDefined(type(settings)))

def dump_input(input, toi):
	output_encoding(input, toi)

signal_received = None

def catch_interrupt(number, frame):
	global signal_received
	signal_received = number

def interrupt_alias(number, frame):
	global signal_received
	root = start_up(None)
	# Skip the filtering.
	accepting = 'Accepting signal {number} as SIGINT alias'
	root.log(ar.TAG_TRACE, accepting.format(number=number))
	signal_received = signal.SIGINT

def ignore_signal(number, frame):
	pass

def log_signal(number, frame):
	root = start_up(None)
	# Skip the filtering.
	root.log(ar.TAG_WARNING, 'Unexpected signal {number}'.format(number=number))

# Default handling of mismatch between loaded settings and
# what the application expects.
def no_upgrade(s, v):
	rt = s.__art__
	c = 'decoded version "%s" of "%s"' % (v, rt.path)
	raise ObjectError(c, explanation='not supported')

# Standard parameter processing. Check for name collision.
#
def standard_passing(special_settings):
	if special_settings is not None:
		a = object_settings.__art__.value.keys()
		b = special_settings.__art__.value.keys()
		c = set(a) & set(b)
		if len(c) > 0:
			j = ', '.join(c)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))
	executable, word, ls = command_args()
	x, r = extract_args(object_settings, ls, special_settings)
	arg_values(object_settings, x)
	return executable, word, r

# The global home for this instance of
# the framework.
hb = Homebase()

#
#
def start_vector(self, object_type, settings, input):
	name_counts = ['"%s" (%d)' % (k, len(v)) for k, v in pt.thread_classes.items()]

	executable = os.path.abspath(sys.argv[0])
	self.trace('Executable "%s" as process (%d)' % (executable, os.getpid()))
	self.trace('Working folder "%s"' % (os.getcwd()))
	self.trace('Running object "%s"' % (object_type.__art__.path,))
	self.trace('Class threads (%d) %s' % (len(pt.thread_classes), ','.join(name_counts)))

	def create(self):
		if input is not None:
			return self.create(object_type, settings, input)
		if settings is not None:
			return self.create(object_type, settings)
		return self.create(object_type)

	if hb.role_retry and hb.role_retry[2]:
		def attempt(self, work):
			b = create(self)
			return b
		a = self.create(Retry, attempt, hb.role_retry[2])
	else:
		a = create(self)
	m = self.select(Completed, Stop)

	if isinstance(m, Completed):
		# Do a "fake" signaling. Sidestep all the platform machinery
		# and just set a global. It does avoid any complexities
		# arising from overlapping events. Spent far too much time
		# trying to untangle signals, exceptions and interrupted i/o.
		global signal_received
		signal_received = signal.SIGUSR1
		return m.value

	# Received a Stop.
	self.send(m, a)
	m = self.select(Completed)
	return m.value

bind_any(start_vector, lifecycle=True, message_trail=True, execution_trace=True)

#
#
def create_object(object_type,
	factory_settings=None, factory_input=None, factory_variables=None, upgrade=None,
	parameter_passing=standard_passing, logs=log_to_nowhere):
	"""Creates an async process shim around a "main" async object. Returns nothing.

	:param object_type: the type of an async object to be instantiated
	:type object_type: a function or a Point-based class
	:param factory_settings: persistent values
	:type factory_settings: instance of a registered class
	:param factory_input: per-invocation values
	:type factory_input: instance of a registered class
	:param factory_variables: host environment values
	:type factory_variables: instance of a registered class
	:param upgrade: function that accepts old versions of settings/input and produces the current version
	:type upgrade: function
	:param parameter_passing: method for parsing sys.argv[]
	:type parameter_passing: a function
	:param logs: a callable object expecting to receive log objects
	:type logs: function or class with __call__ method
	:rtype: None
	"""
	global signal_received

	# Start with nothing. Dont know folders, what input has been passed, where stored
	# settings might be, how to behave with respect to parent-child piping, or how to behave
	# with logging. Nothing.
	try:
		# Parse out args vs words, split into framework settings
		# vs object.
		executable, word, r = parameter_passing(factory_settings)

		hb.command_executable = executable
		hb.command_words = word
	except ValueError as e:
		f = Faulted('cannot process command-line arguments', str(e))
		output_exit(f, code=0)

	# Try to match names members of an environment object with variables in
	# the environment. Decode matched values.
	try:
		if factory_variables is not None:
			hb.environment_variables = environment_variables(factory_variables)
	except ValueError as e:
		f = Faulted('cannot process environment variables', str(e))
		output_exit(f, code=0)

	# Determine the runtime support; homed, tool or plain object.
	try:
		bp = breakpath(executable)

		homed = object_settings.homed()		# Controlled by command-line args.
		if homed:
			hb.home_role(object_settings.home_path, object_settings.role_name,
				factory_settings, factory_input,
				executable=bp[1])
			if hb.role_executable and hb.role_executable[2] != bp[1]:
				raise RuntimeError('running executable does not match the <executable> in the assigned role')
		elif object_settings.home_path or object_settings.role_name:
			raise RuntimeError('missing home or role value')
		elif factory_settings:
			base = os.getenv('ANSAR_TOOL') or os.getenv('HOME') or os.getcwd()
			path = os.path.join(base, '.ansar-tool')
			role = bp[1]
			hb.home_role(path, role,
				factory_settings, factory_input,
				plan=TOOL_SERVICE,
				executable=bp[1])
		else:
			pass	# Plain old object.
	except (ValueError, RuntimeError, OSError) as e:
		f = Faulted('cannot establish runtime', str(e))
		output_exit(f, code=0)

	def daemonize():
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try:
			pid = os.fork()
			if pid > 0:
				# exit first parent
				sys.exit(0)
		except OSError as e:
			f = Faulted('cannot establish daemon [1] %d (%s)' % (e.errno, e.strerror))
			output_exit(f, code=0)

		# decouple from parent environment
		os.chdir("/")
		os.setsid()
		os.umask(0)

		try:
			pid = os.fork()
			if pid > 0:
				# exit second parent
				sys.exit(0)
		except OSError as e:
			f = Faulted('cannot establish daemon [2] %d (%s)' % (e.errno, e.strerror))
			output_exit(f, code=0)

		# redirect standard file descriptors
		#sys.stdout.flush()
		#sys.stderr.flush()
		#si = file(self.stdin, 'r')
		#so = file(self.stdout, 'a+')
		#se = file(self.stderr, 'a+', 0)
		#os.dup2(si.fileno(), sys.stdin.fileno())
		#os.dup2(so.fileno(), sys.stdout.fileno())
		#os.dup2(se.fileno(), sys.stderr.fileno())

		# write pidfile
		#atexit.register(self.delpid)
		#pid = str(os.getpid())
		#file(self.pidfile,'w+').write("%s\n" % pid)

	if homed and object_settings.point_of_origin == 0:
		daemonize()

	# Tunable, operational parameters and persisted. Load and perform any
	# related object_settings operations.
	cant_frame = None
	cant_code = 0
	settings = factory_settings
	if factory_settings is not None:
		if not ar.is_message(factory_settings):
			f = Faulted('cannot support settings', 'not a registered message')
			output_exit(f, code=0)

		tos = ar.UserDefined(type(factory_settings))

		if object_settings.reset_to_factory_settings:
			try:
				hb.role_settings[1].store(settings)
				cant_frame = Ack()
			except (ar.FileFailure, ar.CodecFailed) as e:
				cant_frame = Faulted('cannot store settings', str(e))
		else:
			try:
				# Allow persisted settings to be overridden by explicit
				# input file, then make assignments on top of the result.
				v = None
				if object_settings.settings_file:
					settings, v = file_decoding(object_settings.settings_file, tos)
				else:
					settings, v = settings_recover(hb.role_settings[1], factory_settings)

				if v is not None:
					mismatch = 'mismatched version (%s) of settings' % (v,)
					if not upgrade:
						f = Faulted(condition=mismatch, explanation='no upgrade feature available')
						output_exit(f, code=0)
					try:
						settings = upgrade(settings, v)
						if hb.role_settings and hb.role_settings[1]:
							hb.role_settings[1].store(settings)
							hb.role_settings[2] = settings
					except ValueError as e:
						f = Faulted(condition=mismatch, explanation=str(e))
						output_exit(f, code=0)

				arg_values(settings, r)
				hb.role_settings[2] = settings
			except ValueError as e:
				f = Faulted('cannot assign values to settings', str(e))
				output_exit(f, code=0)
			except (ar.FileFailure, ar.CodecFailed) as e:
				f = Faulted('cannot recover settings from file', str(e))
				output_exit(f, code=0)

			# Settings are resolved. Carry out any user-requested
			# actions. Assume this is at the console.
			if object_settings.help:
				settings_help(settings)
				silent_exit()

			# These are assumed to be programmatic and only command.
			if object_settings.dump_settings:
				try:
					dump_settings(settings)
				except ar.CodecFailed as e:
					c = 'cannot dump settings, {error}'.format(error=str(e))
					f = Faulted(condition=c)
					output_exit(f, code=0)
				silent_exit()

			if object_settings.store_settings:
				try:
					hb.role_settings[1].store(settings)
					cant_frame = Ack()
				except (ar.FileFailure, ar.CodecFailed) as e:
					cant_frame = Faulted('cannot store settings', str(e))
	elif object_settings.help:
		settings_help(settings)
		silent_exit()
	elif object_settings.dump_settings:
		cant_frame = Faulted(condition='cannot dump settings, no settings defined')
	elif object_settings.settings_file:
		cant_frame = Faulted(condition='cannot recover settings from file, no settings defined')
	elif len(r[0]) > 0 or len(r[1]) > 0:
		lf, sf = r
		lk, sk = lf.keys(), sf.keys()
		ld = [k for k in lk]
		sd = [k for k in sk]
		ld.extend(sd)
		detected = ', '.join(ld)
		cant_frame = Faulted(condition='settings detected in arguments ({detected}) and no settings defined'.format(detected=detected))
	elif object_settings.store_settings:
		cant_frame = Ack()

	# Primary input. Object expects to work on an instance of
	# input_type. Load from file or pipe.
	input = None
	if factory_input is not None:
		toi = ar.fix_expression(type(factory_input), {})
		try:
			# Explicit file has priority, then the presence/absence
			# of command-line words (e.g. files), then input
			# piped from the parent.
			v = None
			if object_settings.input_file:
				input, v = file_decoding(object_settings.input_file, toi)
			elif word:
				pass
			elif object_settings.dump_input:
				input, v = factory_input, None
			elif object_settings.call_signature is None or 'i' in object_settings.call_signature:
				input, v = input_decoding(toi)
			elif hb.role_input and hb.role_input[2]:
				input, v = hb.role_input[2], None
			else:
				f = Faulted('no input source', 'no input-file, no words, not piped and no stored image')
				output_exit(f, code=0)

			if v is not None:
				mismatch = 'mismatched version (%s) of input' % (v,)
				if not upgrade:
					f = Faulted(condition=mismatch, explanation='no upgrade feature available')
					output_exit(f, code=0)
				try:
					input = upgrade(input, v)
					if hb.role_input and hb.role_input[1]:
						hb.role_input[1].store(input)
						hb.role_input[2] = input
				except ValueError as e:
					f = Faulted(condition=mismatch, explanation=str(e))
					output_exit(f, code=0)

		except (ar.FileFailure, ar.CodecFailed) as e:
			f = Faulted('cannot decode input', str(e))
			output_exit(f, code=0)

		if object_settings.dump_input:
			try:
				dump_input(input, toi)
			except ar.CodecFailed as e:
				c = 'cannot dump input, {error}'.format(error=str(e))
				f = Faulted(condition=c)
				output_exit(f, code=0)
			silent_exit()

		if object_settings.store_input:
			try:
				hb.role_input[1].store(input)
				cant_frame = Ack()
			except (ar.FileFailure, ar.CodecFailed) as e:
				cant_frame = Faulted('cannot store input', str(e))

		hb.command_input = input
	elif object_settings.dump_input:
		cant_frame = Faulted('cannot dump input, no input defined')
	elif object_settings.input_file:
		cant_frame = Faulted('cannot recover input from file', 'no input defined')
	elif object_settings.call_signature is not None and 'i' in object_settings.call_signature:
		cant_frame = Faulted('call signature mismatch', 'no input defined')
	elif object_settings.store_input:
		cant_frame = Ack()

	if cant_frame is not None:
		output_exit(cant_frame, code=cant_code)

	# Resolve logging - where should it go?
	try:
		files_in_folder = None
		if homed:
			if hb.role_storage and hb.role_storage[2]:
				bytes_in_file = 120 * LINES_IN_FILE
				files_in_folder = hb.role_storage[2] / bytes_in_file

			if object_settings.point_of_origin == 0:		# Start
				logs = RollingLog(hb.role_logs.path, files_in_folder=files_in_folder)
			elif object_settings.point_of_origin == 1:		# Run
				if object_settings.debug_level in (None, LOG_NUMBER.NONE):
					logs = log_to_nowhere
				else:
					logs = select_logs(object_settings.debug_level)
			else:	# Call.
				if object_settings.debug_level is not None:
					logs = select_logs(object_settings.debug_level)
				else:
					logs = RollingLog(hb.role_logs.path, files_in_folder=files_in_folder)
		elif object_settings.debug_level is not None:
			logs = select_logs(object_settings.debug_level)
	except OSError as e:
		f = Faulted('cannot initiate logging', str(e))
		output_exit(f, code=0)

	error_condition = None
	exit_code = 0
	output_value = None
	early_return = False
	root = None
	try:
		# Primary goal is translation of SIGINT (control-c) into
		# a stop protocol. The SIGHUP signal also receives similar
		# attention on the basis its notification of a shutdown.
		# For debugging purposes other signals are logged as warnings.
		signal.signal(signal.SIGINT, catch_interrupt)
		signal.signal(signal.SIGQUIT, interrupt_alias)
		signal.signal(signal.SIGHUP, interrupt_alias)
		signal.signal(signal.SIGTERM, interrupt_alias)

		signal.signal(signal.SIGCHLD, ignore_signal)
		signal.signal(signal.SIGTRAP, log_signal)
		signal.signal(signal.SIGABRT, log_signal)
		#signal.signal(signal.SIGKILL, log_signal)	... cant be caught.
		signal.signal(signal.SIGPIPE, log_signal)
		signal.signal(signal.SIGUSR1, log_signal)
		signal.signal(signal.SIGUSR2, log_signal)
		signal.signal(signal.SIGALRM, log_signal)
		signal.signal(signal.SIGTTIN, log_signal)
		#signal.signal(signal.SIGSTOP, log_signal)	... ditto.
		signal.signal(signal.SIGTSTP, log_signal)
		signal.signal(signal.SIGPWR, log_signal)

		# Start up async world.
		root = start_up(logs)

		if homed and hb.role_entry:
			name = 'lockup'
			a = root.create(lock_and_hold, hb.role_entry.path, name)
			root.assign(a, name)
			m = root.select(Ready, Completed)
			if isinstance(m, Completed):	# Cannot lock.
				root.debrief()
				raise Completion(m.value)	# Jump forward for early shutdown.

		cs = object_settings.call_signature
		no_output = cs is not None and 'o' not in cs
		if object_settings.point_of_origin == 0 or no_output:
			early_return = True
			output_encoding(Ack(), ar.Any())
			sys.stdout.close()
			os.close(1)

		#
		#
		if homed:
			hb.entry_started()

		# Create the async object.
		a = root.create(start_vector, object_type, settings, input)

		# Termination of this function is
		# either by SIGINT (control-c) or assignment by start_vector.
		while signal_received is None:
			time.sleep(0.1)
			#signal.pause()

		# If it was keyboard then async object needs
		# to be bumped.
		if signal_received != signal.SIGUSR1:
			root.send(Stop(), a)
		m = root.select(Completed)
		value = m.value

		# Translate async completion to a standard exit code or
		# error diagnostic and code.
		if isinstance(value, int):
			# Infer that parent was automated, i.e. not
			# an interactive shell.
			if object_settings.call_signature:
				output_value = ExitCode(value)
			else:
				exit_code = value	# Respond to keyboard user.
		elif ar.is_message(value):
			output_value = value
		else:
			error_condition = 'unexpected object completion %r' % (value,)
	except Completion as c:
		output_value = c.value
	except KeyboardInterrupt:
		error_condition = 'unexpected keyboard interrupt'
	except SystemExit:
		error_condition = 'unexpected system exit'
	except Exception as e:
		s = str(e)
		error_condition = 'unhandled exception (%s)' % (s,)
	except:
		error_condition = 'unhandled opaque exception'
	finally:
		# Clear the lock.
		if root is not None:
			root.abort()
			while root.working():
				root.select(Completed)
				root.debrief()

		if error_condition is not None:
			output_value = Faulted('object failure', error_condition)

		# Close the active record.
		if homed:
			hb.entry_returned(output_value)

		#
		#
		if output_value is not None:
			try:
				if object_settings.output_file:
					file_encoding(object_settings.output_file, output_value, ar.Any())
				elif not early_return:
					output_encoding(output_value, ar.Any())
			except (ar.FileFailure, ar.CodecFailed) as e:
				if not early_return:
					f = Faulted('cannot encode output', str(e))
					output_exit(f)
			except Exception as e:
				if not early_return:
					f = Faulted('unexpected exception during output', str(e))
					output_exit(f)

		tear_down(code=exit_code)

#
#
def command_variables():
	"""Global access to the values decoded from the environment. Returns the variables object."""
	return hb.environment_variables

def command_executable():
	"""Global access to the host executable. Returns a str."""
	return hb.command_executable

def command_words():
	"""Global access to the words appearing on the command-line. Returns a list of words."""
	return hb.command_words

def set_debug(debug_level):
	"""Global mechansim for assigning the object debug_level. Returns nothing."""
	object_settings.debug_level = debug_level

def command_settings():
	"""Global access to the values decoded from persistent configuration. Returns the values or None."""
	if hb.role_settings is not None:
		return hb.role_settings[2]
	return None

def store_settings(settings):
	"""Global mechanism for updating the persistent configuration. Returns indication of success."""
	if hb.role_settings is not None:
		hb.role_settings[1].store(settings)
		hb.role_settings[2] = settings
		return True
	return False

def command_input():
	"""Global access to the values decoded from the input pipe or file. Returns the values or None."""
	return hb.command_input

def resource_folder():
	"""Part of the disk management context, i.e. resource. Returns the per-executable, read-only resource folder or None."""
	if object_settings.homed():
		return hb.executable_resource
	return None

def tmp_folder():
	"""Part of the disk management context, i.e tmp. Returns the empty-on-start, temporary folder or None."""
	if object_settings.homed():
			return hb.role_tmp
	return None

def model_folder():
	"""Part of the disk management context, i.e. model. Returns the folder of bulk, persistent storage or None."""
	if object_settings.homed():
			return hb.role_model
	return None

#
#
def resource_path():
	"""Partner to resource_folder(). Returns the folder path or None."""
	f = resource_folder()
	if f:
		return f.path
	return None

def tmp_path():
	"""Partner to tmp_folder(). Returns the folder path or None."""
	f = tmp_folder()
	if f:
		return f.path
	return None

def model_path():
	"""Partner to model_folder(). Returns the folder path or None."""
	f = model_folder()
	if f:
		return f.path
	return None
