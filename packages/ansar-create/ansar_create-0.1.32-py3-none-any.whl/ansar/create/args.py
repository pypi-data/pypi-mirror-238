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

import os
import sys
import ansar.encode as ar

__all__ = [
	'command_flags',
	'command_args',
	'extract_args',
	'word_else',
	'QUOTED_TYPE',
	'SHIPMENT_WITH_QUOTES',
	'SHIPMENT_WITHOUT_QUOTES',
	'arg_values',
	'environment_variables',
	'component_args',
	'sub_args',
]

#
#
def command_flags(argv):
	'''Scan argv and return word and flag details.'''
	word = []
	lf = {}
	sf = {}
	for a in argv:
		if a.startswith('--ansar-'):	# Ignore.
			continue
		elif a.startswith('--'):		# Long - full name reference.
			try:
				i = a.index('=')
				k = a[2:i]
				v = a[i + 1:]
			except ValueError:
				k = a[2:]
				v = 'true'
			lf[k] = v
		elif a.startswith('-'):			# Short - match initial letter.
			try:
				i = a.index('=')
				k = a[1:i]
				v = a[i + 1:]
			except ValueError:
				k = a[1:]
				v = 'true'
			if len(k) > 1:
				e = 'short flag is not short, use long form --{name}[=<value>]'.format(name=k)
				raise ValueError(e)
			sf[k] = v
		else:
			word.append(a)				# A non-flag.

	return word, (lf, sf)

def command_args():
	'''Read sys.argv and return executable, words and flags.'''
	executable = os.path.abspath(sys.argv[0])
	word, ls = command_flags(sys.argv[1:])
	return executable, word, ls

def extract_args(settings, ls, other):
	lf, sf = ls
	rt = settings.__art__

	# Compile lists of names by first character.
	first_char = {}
	for k, _ in rt.value.items():
		c = k[0]
		try:
			f = first_char[c]
		except KeyError:
			f = []
			first_char[c] = f
		f.append(k)
	if other is not None:
		for k, _ in other.__art__.value.items():
			c = k[0]
			try:
				f = first_char[c]
			except KeyError:
				f = []
				first_char[c] = f
			f.append(k)

	# Promote short name to the matching long form.
	def short_to_long(a):
		for k, _ in rt.value.items():
			if k[0] != a:
				continue
			try:
				f = first_char[k[0]]
				if len(f) > 1:
					e1 = 'ambiguous short settings ({clashes})'.format(clashes=', '.join(f))
					e2 = '{e1}, use long form --{name}[=<value>]'.format(e1=e1, name=k)
					raise ValueError(e2)
			except KeyError:
				e = 'short to long form processing failed'
				raise ValueError(e)
			return k
		return None

	lx, sx = {}, {}
	lr, sr = {}, {}
	for k, v in lf.items():
		r = k.replace('-', '_')
		if r in rt.value:
			lx[k] = v
		else:
			lr[k] = v

	for k, v in sf.items():
		t = short_to_long(k)
		if t is None:
			sr[k] = v
			continue
		r = t.replace('-', '_')
		if r in rt.value:
			sx[k] = v
		else:
			sr[k] = v
	return (lx, sx), (lr, sr)

def word_else(i, word, d):
	if i < len(word):
		return word[i]
	return d

# Machinery to assign a value to a member of the
# current settings. Text must be decoded according
# to expected type.
QUOTED_TYPE = (ar.Character, ar.Rune,
	ar.Block, ar.String, ar.Unicode,
	ar.WorldTime, ar.TimeDelta, ar.ClockTime, ar.TimeSpan,
	ar.UUID,
	ar.Enumeration)

# A collection of items supporting the "run(main)" function. Lots of
# transformation of stdin and stdout and wiring to a Homebase.
SHIPMENT_WITH_QUOTES = """{
	"value": "%s"
}"""

SHIPMENT_WITHOUT_QUOTES = """{
	"value": %s
}"""

def arg_values(settings, ls, skip=False):
	lf, sf = ls
	rt = settings.__art__

	# Compile lists of names by first character.
	first_char = {}
	for k, _ in rt.value.items():
		c = k[0]
		try:
			f = first_char[c]
		except KeyError:
			f = []
			first_char[c] = f
		f.append(k)

	# Promote short name to the matching long form.
	def short_to_long(a):
		for k, _ in rt.value.items():
			if k[0] != a:
				continue
			try:
				f = first_char[k[0]]
				if len(f) > 1:
					e1 = 'ambiguous short settings ({clashes})'.format(clashes=', '.join(f))
					e2 = '{e1}, use long form --{name}[=<value>]'.format(e1=e1, name=k)
					raise ValueError(e2)
			except KeyError:
				pass	# Strange. Should hit all.
			return k
		# Short name not detected in schema.
		if skip:
			return None
		e = 'unknown short setting "{name}", dump and verify'.format(name=a)
		raise ValueError(e)

	# Convert value text according to type of name and
	# assign to settings object.
	def k_equals_v(k, v):
		# Unknown name errors and
		# codec errors
		try:
			r = k.replace('-', '_')
			t = rt.value[r]
		except KeyError as e:
			if skip:
				return
			e = 'unknown name "{name}"'.format(name=k)
			raise ValueError(e)
		if isinstance(t, QUOTED_TYPE):
			v = SHIPMENT_WITH_QUOTES % (v,)
		else:
			v = SHIPMENT_WITHOUT_QUOTES % (v,)
		try:
			encoding = ar.CodecJson()
			v, _ = encoding.decode(v, t)
		except ar.CodecFailed as e:
			s = str(e)
			t = 'cannot decode value for "{name}", {failed}'.format(name=k, failed=s)
			raise ValueError(e)
		setattr(settings, r, v)

	for k, v in lf.items():
		k_equals_v(k, v)

	for k, v in sf.items():
		t = short_to_long(k)
		if t is None:
			continue
		k_equals_v(t, v)

def environment_variables(factory_variables):
	if not ar.is_message(factory_variables):
		raise ValueError('supplied variables are not a registered object')

	environment = {k[5:].replace('-', '_'): v for k, v in os.environ.items()
			if k.startswith('AR_V_')}

	rt = factory_variables.__art__
	schema = rt.value
	for k, t in schema.items():
		K = k.upper()
		try:
			r = environment[K]
		except KeyError:
			continue

		if isinstance(t, QUOTED_TYPE):
			r = SHIPMENT_WITH_QUOTES % (r,)
		else:
			r = SHIPMENT_WITHOUT_QUOTES % (r,)
		try:
			encoding = ar.CodecJson()
			v, _ = encoding.decode(r, t)
		except ar.CodecFailed as e:
			d = 'cannot decode value for "{name}", {failed}'.format(name=k, failed=str(e))
			raise ValueError(d)
		setattr(factory_variables, k, v)
	return factory_variables

#
#
REDIRECTED = [
	'bin', 'settings', 'logs',
	'resource', 'tmp', 'model',
]

def component_args(settings):
	'''Extract ansar-name arguments from argv and assign to settings. Return collection of redirects.'''
	redirect = {}
	lf = {}
	for a in sys.argv:
		if not a.startswith('--ansar-'):
			continue
		try:
			i = a.index('=')
			k = a[8:i]
			v = a[i+1:]
		except ValueError:
			k = a[8:]
			v = 'true'

		if k in REDIRECTED:
			redirect[k] = os.path.abspath(v)
			continue

		lf[k] = v

	arg_values(settings, (lf, {}))
	return redirect

#
#
def wording(argv):
	'''Find the words on a command-line. Yield index and word.'''
	for i, a in enumerate(argv):
		if not a.startswith('-'):
			yield i, a

def sub_args():
	'''Split argv into executable and sub-command parts. Assign first set of flags to settings.'''
	i = iter(wording(sys.argv))
	try:
		e, executable = next(i)
		s, sub = next(i)
	except StopIteration:
		# Assume that this is a lack of sub-word.
		executable = os.path.abspath(sys.argv[0])
		word, ls1 = command_flags(sys.argv[1:])
		return executable, ls1, None, ({}, {}), word

	if e != 0:
		s = 'internal (no executable at [0])'
		raise ValueError(s)

	executable = os.path.abspath(executable)
	word, ls1 = command_flags(sys.argv[e + 1: s])
	# Verify word is empty?
	word, ls2 = command_flags(sys.argv[s + 1:])

	return executable, ls1, sub, ls2, word
