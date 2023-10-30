# MIT License
#
# Copyright (c) 2017 Scott Woods
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

"""Standard Ansar messages.

These are either generated from within Ansar - and then expected by the
application in related scenarios. Or they are used internally by Ansar
and may be used in the wider application. Ansar async objects will
exhibit common patterns of behaviour.
"""
__docformat__ = 'restructuredtext'

import re
from ansar.encode import String, Unicode, bind_message, Any, Enumeration

__all__ = [
	'Start',
	'Completed',
	'Faulted',
	'Stop',
	'Aborted',
	'TimedOut',
	'Nothing',
	'Ready',
	'ExitCode',
	'Enquiry',
	'Maybe',
	'Cannot',
	'Interrupted',
	'Exhausted',
	'Ack',
	'Nak',
	'HostPort',
]

class Start(object):
	"""First message received by every async machine, from creator to child."""
	pass

class Completed(object):
	"""Last message sent, from child to creator.

	:param value: return value for an async object
	:type value: any
	"""
	def __init__(self, value=None):
		self.value = value

class ConditionExplanation(object):
	"""Base for notification messages."""
	def __init__(self, condition=None, explanation=None):
		self.condition = condition
		self.explanation = explanation

	def __str__(self):
		s = '(no information)'
		if self.condition:
			if self.explanation:
				s = '%s, %s' % (self.condition, self.explanation)
			else:
				s = self.condition
		return s

CONDITION_EXPLANATION_SCHEMA = {
	'condition': Unicode,
	'explanation': Unicode
}

class Faulted(ConditionExplanation):
	"""Abnormal termination. Often passed within the Completed message."""
	def __init__(self, condition=None, explanation=None):
		ConditionExplanation.__init__(self, condition, explanation)

class TimedOut():
	"""Termination due to internal timer. Often passed within the Completed message."""
	pass

class Stop(object):
	"""Initiate teardown in the receiving object."""
	pass

class Aborted(object):
	"""Completion of teardown. Often passed within the Completed message."""
	pass

class Nothing(object):
	"""A positive null."""
	pass

class Ready(object):
	"""Report a positive state."""
	pass

class ExitCode():
	"""Auto-message for async objects returning an integer to the console."""
	def __int__(self, code=0):
		self.code = code

class Maybe(ConditionExplanation):
	"""A failed attempt but worth another go.

	Returned by an object under the control of a retry machine. This
	advises the machine that the latest attempt did not work but
	another attempt might do so.

	:param condition: something detected that produced this result
	:type condition: str
	:param explanation: possible resolution to the detected problem
	:type explanation: str
	"""
	def __init__(self, condition=None, explanation=None):
		ConditionExplanation.__init__(self, condition, explanation)

class Cannot(ConditionExplanation):
	"""A failed attempt and it doesnt look good.

	Returned by an object under the control of a retry machine. This
	advises the machine that the latest attempt did not work and
	encountered a condition suggesting that further retries are
	wasted effort or inappropriate.

	:param condition: something detected that produced this result
	:type condition: str
	:param explanation: possible resolution to the detected problem
	:type explanation: str
	"""
	def __init__(self, condition=None, explanation=None):
		ConditionExplanation.__init__(self, condition, explanation)

class Interrupted(object):
	"""Had work underway. Need to get back and resume."""
	def __init__(self, work=None):
		self.work = work

class Exhausted(object):
	"""The retry strategy is exhausted. There are no more attempts to be made."""
	pass

INTERRUPTED_SCHEMA = {
	'work': Any,
}

bind_message(Maybe, object_schema=CONDITION_EXPLANATION_SCHEMA, copy_before_sending=False)
bind_message(Cannot, object_schema=CONDITION_EXPLANATION_SCHEMA, copy_before_sending=False)
bind_message(Interrupted, object_schema=INTERRUPTED_SCHEMA, copy_before_sending=False)
bind_message(Exhausted, copy_before_sending=False)

# Most basic sync and/or status check.
#
class Enquiry(object):
	"""Prompt an action from receiver."""
	pass

class Ack(object):
	"""Report in the positive."""
	pass

class Nak(object):
	"""Report in the negative."""
	pass

bind_message(Start, copy_before_sending=False)
bind_message(Completed, object_schema={'value': Any()}, copy_before_sending=False)
bind_message(Faulted, object_schema=CONDITION_EXPLANATION_SCHEMA, copy_before_sending=False)
bind_message(TimedOut, copy_before_sending=False)
bind_message(Stop, copy_before_sending=False)
bind_message(Aborted, copy_before_sending=False)
bind_message(Nothing, copy_before_sending=False)
bind_message(Ready, copy_before_sending=False)
bind_message(ExitCode, copy_before_sending=False)
bind_message(Enquiry, copy_before_sending=False)
bind_message(Ack, copy_before_sending=False)
bind_message(Nak, copy_before_sending=False)

#
#
class HostPort(object):
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port

	def inet(self):
		return (self.host, self.port)

HOST_PORT_SCHEMA = {
	'host': str,
	'port': int,
}

bind_message(HostPort, object_schema=HOST_PORT_SCHEMA)
