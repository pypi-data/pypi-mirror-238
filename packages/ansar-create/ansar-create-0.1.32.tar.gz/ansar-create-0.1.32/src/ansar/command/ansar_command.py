# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2022 Scott Woods
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

"""Utility to maintain the operational folders and files of standard components.

Starts with the process-as-an-async-object abstraction and takes it to
the next level. There is a new abstraction that manages a collection
of one or more processes. A complete runtime environment is provided for
each process, i.e. a place for temporary files and persisted files, and
a per-process configuration. Once configured to satisfy requirements a
process can be started and stopped repeatedly using single commands.
"""
__docformat__ = 'restructuredtext'

__all__ = [
    'main',
]

import sys
import os
import stat
import signal
import errno
import datetime
import calendar
import tempfile
import shutil
import uuid
import re
import ansar.create as ar
from ansar.create.root import rt
from ansar.create.args import sub_args
from ansar.create.object import object_settings, LOG_NUMBER
from ansar.create.framework import hb
from ansar.create.rolling import read_log

# For termination of sub-commands without having
# to detect and propagate through the call stack.
class SubCompletion(Exception):
    def __init__(self, code):
        Exception.__init__(self)
        self.code = code

class SubFailed(Exception):
    def __init__(self, condition, explanation=None):
        Exception.__init__(self)
        self.condition = condition
        self.explanation = explanation

    def __str__(self):
        if self.explanation is None:
            s = self.condition
        else:
            s = '%s (%s)' % (self.condition, self.explanation)
        return s

class SubCannot(SubFailed):
    def __init__(self, condition, explanation=None):
        SubFailed.__init__(self, condition, explanation)

# Per-command arguments as required.
# e.g. command-line parameters specific to create.
class CreateSettings(object):
    def __init__(self,
            home_path=None,
            redirect_bin=None,
            redirect_settings=None,
            redirect_logs=None,
            redirect_resource=None,
            redirect_tmp=None,
            redirect_model=None
            ):
        self.home_path = home_path
        self.redirect_bin = redirect_bin
        self.redirect_settings = redirect_settings
        self.redirect_logs = redirect_logs
        self.redirect_resource = redirect_resource
        self.redirect_tmp = redirect_tmp
        self.redirect_model = redirect_model

CREATE_SETTINGS_SCHEMA = {
    'home_path': ar.Unicode(),
    'redirect_bin': ar.Unicode(),
    'redirect_settings': ar.Unicode(),
    'redirect_logs': ar.Unicode(),
    'redirect_resource': ar.Unicode(),
    'redirect_tmp': ar.Unicode(),
    'redirect_model': ar.Unicode(),
}

ar.bind(CreateSettings, object_schema=CREATE_SETTINGS_SCHEMA)

create_settings = CreateSettings()

#
#
class AddSettings(object):
    def __init__(self, executable=None, role_name=None, home_path=None, start=0, step=1, count=1,
        settings_file=None,
        input_file=None,
        retry=None, storage=None):
        self.executable = executable
        self.role_name = role_name
        self.home_path = home_path
        self.start = start
        self.step = step
        self.count = count
        self.settings_file = settings_file
        self.input_file = input_file
        self.retry = retry
        self.storage = storage

ADD_SETTINGS_SCHEMA = {
    'executable': ar.Unicode(),
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'start': ar.Integer8(),
    'step': ar.Integer8(),
    'count': ar.Integer8(),
    'settings_file': ar.Unicode(),
    'input_file': ar.Unicode(),
    'retry': ar.UserDefined(ar.RetryIntervals),
    'storage': ar.Integer8(),
}

ar.bind(AddSettings, object_schema=ADD_SETTINGS_SCHEMA)

add_settings = AddSettings()

#
#
class UpdateSettings(object):
    def __init__(self, role_name=None, home_path=None, executable=None, invert_search=False):
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.invert_search = invert_search

UPDATE_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'executable': ar.Unicode(),
    'invert_search': ar.Boolean(),
}

ar.bind(UpdateSettings, object_schema=UPDATE_SETTINGS_SCHEMA)

update_settings = UpdateSettings()

#
#
class ListSettings(object):
    def __init__(self, role_name=None, home_path=None, executable=None, invert_search=False, long_listing=False):
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.invert_search = invert_search
        self.long_listing = long_listing

LIST_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'executable': ar.Unicode(),
    'invert_search': ar.Boolean(),
    'long_listing': ar.Boolean(),
}

ar.bind(ListSettings, object_schema=LIST_SETTINGS_SCHEMA)

list_settings = ListSettings()

#
#
class StartSettings(object):
    def __init__(self, role_name=None, home_path=None, executable=None, invert_search=False):
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.invert_search = invert_search

START_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'executable': ar.Unicode(),
    'invert_search': ar.Boolean(),
}

ar.bind(StartSettings, object_schema=START_SETTINGS_SCHEMA)

start_settings = StartSettings()

#
#
class RunSettings(object):
    def __init__(self, forwarding=None, executable=None, role_name=None, home_path=None, invert_search=False, code_path=None, test_run=False, test_analyzer=None, debug_level=LOG_NUMBER.NONE):
        self.forwarding = forwarding
        self.executable = executable
        self.role_name = role_name
        self.home_path = home_path
        self.invert_search = invert_search
        self.code_path = code_path
        self.test_run = test_run
        self.test_analyzer = test_analyzer
        self.debug_level = debug_level

RUN_SETTINGS_SCHEMA = {
    'forwarding': ar.Unicode(),
    'executable': ar.Unicode(),
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'invert_search': ar.Boolean(),
    'code_path': ar.Unicode(),
    'test_run': ar.Boolean(),
    'test_analyzer': ar.Unicode(),
    'debug_level': LOG_NUMBER,
}

ar.bind(RunSettings, object_schema=RUN_SETTINGS_SCHEMA)

run_settings = RunSettings()

#
#
class StopSettings(object):
    def __init__(self, role_name=None, home_path=None, executable=None, invert_search=False):
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.invert_search = invert_search

STOP_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    'executable': ar.Unicode(),
    'invert_search': ar.Boolean(),
}

ar.bind(StopSettings, object_schema=STOP_SETTINGS_SCHEMA)

stop_settings = StopSettings()

# Extraction of logs for a role.
#
START_OF = ar.Enumeration(MONTH=0, WEEK=1, DAY=2, HOUR=3, MINUTE=4, HALF=5, QUARTER=6, TEN=7, FIVE=8)

class LogSettings(object):
    def __init__(self, role_name=None, home_path=None,
            clock=False, from_=None, last=None, start=None, back=None,
            to=None, span=None, count=None):
        # One of these for a <begin>
        self.role_name = role_name
        self.home_path = home_path
        self.clock = clock
        self.from_ = from_
        self.last = last
        self.start = start
        self.back = back

        # One of these (optional), for an <end>
        self.to = to
        self.span = span
        self.count = count

LOG_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    "clock": ar.Boolean,
    "from_": ar.Unicode,
    "last": START_OF,
    "start": int,
    "back": ar.TimeSpan,

    "to": ar.Unicode,
    "span": ar.TimeSpan,
    "count": int,
}

ar.bind(LogSettings, object_schema=LOG_SETTINGS_SCHEMA)

log_settings = LogSettings()

#
#
class InputSettings(object):
    def __init__(self, role_name=None, home_path=None, set_file=None, executable=None):
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.set_file = set_file

INPUT_SETTINGS_SCHEMA = {
    "role_name": ar.Unicode(),
    "home_path": ar.Unicode(),
    "executable": ar.Unicode(),
    "set_file": ar.Unicode(),
}

ar.bind(InputSettings, object_schema=INPUT_SETTINGS_SCHEMA)

input_settings = InputSettings()

#
#
class SetSettings(object):
    def __init__(self, property=None, role_name=None, home_path=None, executable=None, invert_search=False,
        encoding_file=None, retry_intervals=None, not_set=False):
        self.property = property
        self.role_name = role_name
        self.home_path = home_path
        self.executable = executable
        self.invert_search = invert_search
        self.encoding_file = encoding_file
        self.retry_intervals = retry_intervals
        self.not_set = not_set

SET_SETTINGS_SCHEMA = {
    "property": ar.Unicode,
    "role_name": ar.Unicode,
    "home_path": ar.Unicode,
    "executable": ar.Unicode,
    'invert_search': ar.Boolean(),
    "encoding_file": ar.Unicode(),
    "retry_intervals": ar.RetryIntervals,
    "not_set": ar.Boolean,
}

ar.bind(SetSettings, object_schema=SET_SETTINGS_SCHEMA)

set_settings = SetSettings()


#
#
class EditSettings(object):
    def __init__(self, property=None, role_name=None, home_path=None):
        self.property = property
        self.role_name = role_name
        self.home_path = home_path

EDIT_SETTINGS_SCHEMA = {
    "property": ar.Unicode,
    "role_name": ar.Unicode,
    "home_path": ar.Unicode,
}

ar.bind(EditSettings, object_schema=EDIT_SETTINGS_SCHEMA)

edit_settings = EditSettings()

#
#
class DeploySettings(object):
    def __init__(self, build_path=None, snapshot_path=None, home_path=None):
        self.build_path = build_path
        self.snapshot_path = snapshot_path
        self.home_path = home_path

DEPLOY_SETTINGS_SCHEMA = {
    "build_path": ar.Unicode,
    "snapshot_path": ar.Unicode,
    "home_path": ar.Unicode,
}

ar.bind(DeploySettings, object_schema=DEPLOY_SETTINGS_SCHEMA)

deploy_settings = DeploySettings()

#
#
class ReturnedSettings(object):
    def __init__(self, role_name=None, home_path=None, timeout=None, start=None):
        # One of these for a <begin>
        self.role_name = role_name
        self.home_path = home_path
        self.timeout = timeout
        self.start = start

RETURNED_SETTINGS_SCHEMA = {
    'role_name': ar.Unicode(),
    'home_path': ar.Unicode(),
    "timeout": ar.Float8,
    "start": ar.Integer8,
}

ar.bind(ReturnedSettings, object_schema=RETURNED_SETTINGS_SCHEMA)

returned_settings = ReturnedSettings()

# Support for sub-command machinery.
def get_host():
    """Retrieve the name of this executable. Return a string."""
    a0 = sys.argv[0]
    bp = ar.breakpath(a0)
    bp1 = bp[1]
    return bp1

def console(line, newline=True, **kv):
    """Place a string on the stdout, i.e. the results of the command."""
    if kv:
        line = line.format(**kv)
    sys.stdout.write(line)
    if newline:
        sys.stdout.write('\n')

def cannot(line, newline=True, **kv):
    """Place an error diagnostic on stderr, including the executable name."""
    if kv:
        t = line.format(**kv)
    else:
        t = line

    h = get_host()
    sys.stderr.write(h)
    sys.stderr.write(': ')
    sys.stderr.write(t)
    if newline:
        sys.stderr.write('\n')

def abort(self, completed=None):
    """Clear an object of all its workers."""
    self.abort()
    while self.working():
        c = self.select(ar.Completed)
        k = self.debrief()
        if completed is not None:
            completed[k] = c.value

def process_status(self, selected):
    """Try to lock everything. Return dicts of inactive vs running."""
    started = {}
    inactive = set()
    running = {}
    selected_roles = ', '.join(selected)
    self.console('Detect status of associated roles ({roles})'.format(roles=selected_roles))
    try:
        for role in selected:
            hb.role_exists(role)
            hb.open_role(None, None)
            a = self.create(ar.lock_and_hold, hb.role_entry.path, 'lockup')
            self.assign(a, role)
            if hb.role_start_stop is not None and hb.role_start_stop[2]:
                started[role] = hb.role_start_stop[2][-1].start
            else:
                started[role] = None

        # Expect a response for each entry;
        expected = self.working()
        for _ in range(expected):
            m = self.select(ar.Stop, ar.Ready, ar.Completed)
            if isinstance(m, ar.Stop):
                raise SubCompletion(1)
            if isinstance(m, ar.Ready):     # This one is inactive.
                role = self.progress()
                inactive.add(role)
                continue
            # Locker has completed.
            role = self.debrief()
            value = m.value
            if isinstance(value, ar.LockedOut):     # Active.
                running[role] = (value, started[role])
                continue
            s = 'unexpected locking (%r)' % (value,)
            raise SubFailed('cannot determine status', s)
    finally:
        abort(self)
    return inactive, running

def stop_process(self, processes, confirmation=False):
    """Try to terminate the set of running entries with an optional confirmation."""
    if not processes:
        return True
    r = ', '.join(processes.keys())
    self.console('Stop roles ({roles})'.format(roles=r))
    # Inter-process send of termination.
    for k, v in processes.items():
        os.kill(v[0].pid, signal.SIGINT)

    if not confirmation:
        return

    self.console('Poll for termination'.format(roles=r))
    for _ in range(5):
        self.start(ar.T1, 1.0)
        m = self.select(ar.Stop, ar.T1)
        if isinstance(m, ar.Stop):
            raise SubCompletion(1)
        _, running = process_status(self, processes.keys())
        if len(running) == 0:
            return
    sticky = running.keys()
    failed = 'cannot stop current process(es) - {roles}'.format(roles=', '.join(sticky))
    raise SubFailed(failed)

def start_process(self, selected):
    """Initiate the processes configured in the specified roles."""
    for role in selected:
        # TBC !!!!!!
        hb.role_exists(role)
        hb.open_role(None, None)
        a = self.create(ar.Process, hb.executable_name(), origin=ar.ORIGIN_START, home_path=hb.home_path, role_name=role)
        self.assign(a, role)
        m = self.select(ar.Completed, ar.Stop)

        if isinstance(m, ar.Stop):
            abort(self)
            return None
        # Object completed. Switch on return value.
        value = m.value
        if isinstance(value, ar.Ack):
            continue
        if isinstance(value, ar.Faulted):
            f = str(value)
            failed = 'cannot start {role}, {error}'.format(role=role, error=f)
            raise SubFailed(failed)
        s = 'unexpected locking "%r"' % (value,)
        failed = 'cannot start {role}, {error}'.format(role=role, error=s)
        raise SubFailed(failed)

def executable_file(executable):
    try:
        s = os.stat(executable)
    except OSError as e:
        reason = str(e)
        failed = 'cannot use executable {executable}, {reason}'.format(executable=executable, reason=reason)
        raise SubFailed(failed)

    mode = s.st_mode
    rwx = stat.filemode(mode)
    if len(rwx) != 10 or rwx[3] != 'x' or rwx[6] != 'x':
        reason = 'unexpected permissions {rwx}'.format(rwx=rwx)
        failed = 'cannot use executable {executable}, {reason}'.format(executable=executable, reason=reason)
        raise SubFailed(failed)

# Actual implementation of sub-commands starts here.
# Create, add, update... These are the global functions
# called by the internal handler functions inside the
# main object.
DEFAULT_HOME = '.ansar-home'
DEFAULT_ROLE = '{executable}-{number}'

def create_home(self, path):
    hb.basic_plan(path)

    redirect = {}
    sub = create_settings
    if sub.redirect_bin: redirect['bin'] = sub.redirect_bin
    if sub.redirect_settings: redirect['settings'] = sub.redirect_settings
    if sub.redirect_logs: redirect['logs'] = sub.redirect_logs
    if sub.redirect_resource: redirect['resource'] = sub.redirect_resource
    if sub.redirect_tmp: redirect['tmp'] = sub.redirect_tmp
    if sub.redirect_model: redirect['model'] = sub.redirect_model
    redirect = {k: os.path.abspath(v) for k, v in redirect.items()}

    r = ', '.join(redirect.keys()) or '- none'

    # Cant create whats already there.
    if hb.plan_exists():
        exists = 'home at "{path}" already exists'
        raise SubCannot(exists.format(path=path))

    creating = 'Creating "{path}" (with redirects {redirect})'
    self.console(creating.format(path=path, redirect=r))
    hb.create_plan(redirect, None)
    return 0

#
#
def no_home(path):
    text = 'home at "{path}" does not exist or is incomplete'
    raise SubCannot(text.format(path=path))

def already_exists(role):
    text = '"{role}" already exists'
    raise SubCannot(text.format(role=role))

def doesnt_exist(role, home):
    text = 'role "{role}" ({home}) does not exist or has unexpected contents'
    raise SubCannot(text.format(role=role, home=home))

def no_matches(search):
    text = 'no matches for "{search}"'
    raise SubCannot(text.format(search=search))

def open_home(home):
    hb.basic_plan(home)
    if not hb.plan_exists():
        no_home(home)
    hb.open_plan()

#
#
def add_role(self, executable, role, home, ls):
    open_home(home)

    # Suitability.
    e = os.path.join(hb.bin.path, executable)
    executable_file(e)

    # Shorthands
    start = add_settings.start
    step = add_settings.step
    count = add_settings.count
    stop = start + count

    rv = {}     # Expanded roles and their settings.
    kv = {}     # Key-values for expansion of names and args.
    kv['executable'] = ar.breakpath(executable)[1]
    for i in range(start, stop, step):
        kv['number'] = i
        kv['uuid'] = uuid.uuid4()
        s = role.format(**kv)
        ls0 = {}
        ls1 = {}

        for k, v in ls[0].items():
            ls0[k] = v.format(**kv)
        for k, v in ls[1].items():
            ls1[k] = v.format(**kv)

        if add_settings.settings_file:
            ls0['settings-file'] = add_settings.settings_file
        if add_settings.input_file:
            ls0['input-file'] = add_settings.input_file

        # Always. Or zombie will never finish creation.
        ls0['store-settings'] = 'true'
        ls0['store-input'] = 'true'

        rv[s] = ls_args([ls0, ls1])

    a = [e for e in hb.entry_list()]
    b = rv.keys()
    c = a & b
    if len(c) > 0:
        j = ', '.join(c)
        raise ValueError('collision(s) in new names - {collisions}'.format(collisions=j))

    adding = 'Adding "{executable}" as "{role}", "{home}" ({count})'
    self.console(adding.format(executable=executable, role=role, home=home, count=len(rv)))

    for k, ls in rv.items():
        hb.role_exists(k)
        # Let sub-process do all the creation as its in possession
        # of settings and input details.
        # hb.create_role(executable, None, None, retry=add_settings.retry, storage=add_settings.storage)
        # executable_name=hb.executable_name()
        a = self.create(ar.Process, executable, origin=ar.ORIGIN_RUN, debug=object_settings.debug_level,
            home_path=hb.home_path, role_name=k,
            settings=ls)
        self.assign(a, k)
        m = self.select(ar.Completed, ar.Stop)
        if isinstance(m, ar.Stop):
            abort(self)
            raise SubCompletion(1)

        # Process completed.
        value = m.value
        if isinstance(value, ar.Ack):   # All done.
            pass
        elif isinstance(value, ar.Faulted):
            reason = str(value)
            not_stored = 'cannot store settings for "{role}" ({home}) - {reason}'
            raise SubFailed(not_stored.format(role=k, home=home, reason=reason))
        else:
            reason = 'unexpected response from component (%r)' % (value,)
            not_stored = 'cannot store settings for "{role}" ({home}) - {reason}'
            raise SubFailed(not_stored.format(role=k, home=home, reason=reason))

    return 0

def find_matches(role, flip, executable=None):
    search = role or '(all)'

    def has_executable(e):
        hb.role_exists(e)
        hb.open_role(None, None)
        if hb.role_executable and hb.role_executable[2] == executable:
            return True
        return False

    if executable is None:
        existing = [e for e in hb.entry_list()]
    else:
        existing = [e for e in hb.entry_list() if has_executable(e)]

    if role is None:
        matched = existing
    else:
        machine = re.compile(role)
        def match_flip(e):
            if machine.match(e):
                return not flip
            return flip
        matched = [e for e in existing if match_flip(e)]
        if len(matched) < 1:
            no_matches(search)
    return search, matched

def find_files(role, folder):
    role_search = role if role is not None else 'all'
    if role is None:
        search = ar.Folder(path=folder.path)
    else:
        search = ar.Folder(path=folder.path, re=role)

    matched = [f for f in search.matching()]
    if len(matched) < 1:
        no_matches(role_search)
    return matched

def matched_status(self, matched, search, force):
    not_running, running = process_status(self, matched)
    if running:
        if not force:
            pids = ['%d' % (v[0].pid,) for k, v in running.items()]
            pids = ', '.join(pids)
            currently_running = '"{search}" currently running as - {pids}'
            raise SubCannot(currently_running.format(search=search, pids=pids))
        stop_process(self, running, confirmation=True)
    return not_running, running

def update_role(self, settings, role, home, ls):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, update_settings.invert_search, executable=update_settings.executable)
    _, running = matched_status(self, matched, search, settings.force)

    updating = 'Updating "{search}" ({home})'
    self.console(updating.format(search=search, home=home))

    ls.append('--store-settings=true')
    try:
        for m in matched:
            hb.role_exists(m)
            hb.open_role(None, None, retry=update_settings.retry, storage=update_settings.storage)
            executable_name = hb.executable_name()
            storing = 'Running "{executable}" ({role}) to store settings'
            self.console(storing.format(role=m, executable=executable_name))
            a = self.create(ar.Process, executable_name, origin=ar.ORIGIN_RUN, debug=ar.USER_LOG_NONE,
                home_path=hb.home_path, role_name=m,
                settings=ls)
            self.assign(a, hb.role)
            r = self.select(ar.Completed, ar.Stop)
            if isinstance(r, ar.Stop):
                raise SubCompletion(1)
            # Process completed. Remove record.
            m = self.debrief()
            value = r.value
            if isinstance(value, ar.Ack):
                pass
            elif isinstance(value, ar.Faulted):
                reason = str(value)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
            else:
                reason = 'unexpected response from component (%r)' % (value,)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
    finally:
        self.console('Clear locks and complete bounces')
        abort(self)
        start_process(self, running)

    return 0

def delete_role(self, settings, role, home):
    home = home or update_settings.home_path or DEFAULT_HOME
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, update_settings.invert_search, executable=update_settings.executable)
    _, running = matched_status(self, matched, search, settings.force)

    deleting = 'Deleting "{search}" ({home})'
    self.console(deleting.format(search=search, home=home))

    for r in matched:
        hb.role_exists(r)
        hb.open_role(None, None)
        hb.delete_role(r)

    return 0

def list_home(self, role, home):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, list_settings.invert_search, executable=list_settings.executable)
    matched.sort()

    listing = 'StorageListing "{search}" ({home})'
    self.console(listing.format(search=search, home=home))

    if not list_settings.long_listing:
        for m in matched:
            console('%s' % (m,))
        return 0

    folders, files, bytes = 0, 0, 0
    for m in matched:
        hb.role_exists(m)
        hb.open_role(None, None)
        fo, fi, by = ar.shape_of_folder(hb.role_logs.path)
        console('%-24s %s (%d/%d/%d)' % (m, hb.role_executable[2], 1 + fo, fi, by))
        folders += 1 + fo
        files += fi
        bytes += by
    console('%-24s (%d/%d/%d)' % ('totals', folders, files, bytes))

    return 0

def destroy_home(self, settings, home):
    open_home(home)

    existing = [e for e in hb.entry_list()]
    _, running = matched_status(self, existing, '(all)', settings.force)

    destroying = 'Destroying "{home}"'
    self.console(destroying.format(home=home))

    # Can now remove without side-effects from
    # operational processes.
    hb.destroy_plan()
    return 0

# Other raison d'etre. Maintain the processes implied
# by all the home info.
def start_role(self, settings, role, home, ls):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, start_settings.invert_search, executable=start_settings.executable)
    _, running = matched_status(self, matched, search, settings.force)

    starting = 'Starting "{search}" ({home})'
    self.console(starting.format(search=search, home=home))

    for m in matched:
        hb.role_exists(m)
        hb.open_role(None, None)
        # Create a new instance of the executable. It may collide with
        # an earlier start.
        a = self.create(ar.Process, hb.executable_name(), origin=ar.ORIGIN_START,
            home_path=hb.home_path, role_name=m, settings=ls)
        self.assign(a, m)
        r = self.select(ar.Completed, ar.Stop)

        if isinstance(r, ar.Stop):
            abort(self)
            raise SubCompletion(1)
        # Process completed. Remove record.
        m = self.debrief()
        value = r.value
        if isinstance(value, ar.Ack):       # New instance established itself.
            pass
        elif isinstance(value, ar.LockedOut):
            fault = 'unexpected lockout on "{role}", still running as <{pid}>'
            raise SubCannot(fault.format(role=m, pid=value.pid))
        elif isinstance(value, ar.Faulted):
            fault = str(value)
            raise SubCannot(fault)
        elif isinstance(value, ar.Incognito):
            fault = 'unexpected Incognito response for "%s" (%s)' % (m, value.type_name)
            raise SubCannot(fault)
        else:
            fault = 'unexpected locking response for "%s" (%r)' % (m, value)
            raise SubFailed(fault)
    return 0

#
#
class Run(object):
    def __init__(self, role=None, home=None, executable=None, completed=None):
        self.role = role
        self.home = home
        self.executable = executable
        self.completed = completed or ar.default_map()

RUN_OUTPUT_SCHEMA = {
    "role": ar.Unicode(),
    "home": ar.Unicode(),
    "executable": ar.Unicode(),
    "completed": ar.MapOf(ar.Unicode(), ar.Any()),
}

ar.bind(Run, object_schema=RUN_OUTPUT_SCHEMA)

def long_form(path):
    d = {}
    path = os.path.abspath(path)
    m, _ = ar.storage_manifest(path)
    for f, t in ar.storage_walk(m):
        if isinstance(t, ar.StorageListing):
            d[t.name] = f
    return d

def run_role(self, settings, role, home, ls):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, run_settings.invert_search, executable=run_settings.executable)

    forwarding = run_settings.forwarding
    if forwarding is not None and forwarding not in matched:
        fault = 'roles matching "{search}" do not include "{forwarding}"'
        raise SubCannot(fault.format(search=search, forwarding=forwarding))

    _, running = matched_status(self, matched, search, settings.force)

    running_sub = 'Running "{search}" ({home})'
    self.console(running_sub.format(search=search, home=home))

    completed = {}
    try:
        for m in matched:
            hb.role_exists(m)
            hb.open_role(None, None)
            # Create a new instance of the executable. It should not collide with
            # an earlier start.
            fwd = m == forwarding

            a = self.create(ar.Process, hb.executable_name(), forwarding=fwd,
                origin=ar.ORIGIN_RUN, debug=run_settings.debug_level,
                home_path=hb.home_path, role_name=m,
                settings=ls)
            self.assign(a, hb.role)

        while self.working():
            r = self.select(ar.Completed, ar.Stop)

            if isinstance(r, ar.Stop):
                break
            # Process completed. Remove record.
            m = self.debrief()
            value = r.value
            completed[m] = value
            if not ar.is_message(value):
                c = 'unexpected completion of "%s", %r' % (m, value)
                value = ar.Faulted(condition=c)
            self.console('Completion for "%s" (%r)' % (m, value))
    finally:
        abort(self, completed)
        start_process(self, running)

    # Look for roles that generated test reports and collate
    # that into a full test suite.
    suite = ar.TestSuite()
    failed = []

    # If provided, improve the quality of test information by
    # augmenting module names with their full path.
    lf = {}
    if run_settings.code_path:
        lf = long_form(run_settings.code_path)

    # Compile a list of failed tests. Take the opportunity
    # to add any path information to each test.
    for role, value in completed.items():
        if isinstance(value, ar.TestReport):
            suite.report[role] = value
            for t in value.tested:
                t.source = lf.get(t.source, t.source)
                if not t.condition:
                    failed.append(t)

    if run_settings.test_analyzer:
        a = self.create(ar.Process, run_settings.test_analyzer, input=suite, debug=run_settings.debug_level)
        self.assign(a, suite)
        r = self.select(ar.Completed, ar.Stop)

        if isinstance(r, ar.Stop):
            abort(self)
            value = ar.Aborted()
        else:
            s = self.debrief()
            value = r.value
            if not ar.is_message(value):
                c = 'unexpected completion of "%s", %r' % (m, value)
                value = ar.Faulted(condition=c)

        s = store(value, ar.Any(), pretty=True)
        sys.stdout.write(s)
        return 0

    # A default reporting of test results.
    if run_settings.test_run:
        for role, report in suite.report.items():
            print(f'role "{role}" (pass/fail): {report.passed}/{report.failed}')

        for f in failed:
            print(f'{f.source}:{f.line} - {f.text}')

        if len(failed) > 0:
            return 1
        return 0

    r = Run(home=home, role=role, executable=run_settings.executable, completed=completed)
    s = store(r, ar.Any(), pretty=True)
    sys.stdout.write(s)
    return 0

def stop_role(self, settings, role, home):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, stop_settings.invert_search, executable=stop_settings.executable)

    inactive, running = process_status(self, matched)
    if inactive:
        if not settings.force:
            not_running = ', '.join(inactive)
            fault = '"{search}" not currently running - {names}'
            raise SubCannot(fault.format(search=search, names=not_running))

    stopping = 'Stopping "{search}" ({home})'
    self.console(stopping.format(search=search, home=home))

    stop_process(self, running, confirmation=True)
    return 0

def short_delta(d):
    t = ar.span_to_text(d.total_seconds())
    i = t.find('d')
    if i != -1:
        j = t.find('h')
        if j != -1:
            return t[:j + 1]
        return t[:i + 1]
    i = t.find('h')
    if i != -1:
        j = t.find('m')
        if j != -1:
            return t[:j + 1]
        return t[:i + 1]
    # Minutes or seconds only.
    i = t.find('.')
    if i != -1:
        i += 1
        j = t.find('s')
        if j != -1:
            e = j - i
            e = min(1, e)
            return t[:i + e] + 's'
        return t[:i] + 's'

def home_status(self, role, home):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, list_settings.invert_search, executable=list_settings.executable)
    matched.sort()

    _, running = process_status(self, matched)

    now = datetime.datetime.now(ar.UTC)
    def long_status():
        for m in matched:
            try:
                v, s0 = running[m]
            except KeyError:
                continue

            if s0 is not None:
                d = now - s0
                s = '%s' % (short_delta(d),)
            else:
                s = '(never started)'
            console('%-24s <%d> %s' % (m, v.pid, s))

    def short_status():
        for m in matched:
            try:
                v, s0 = running[m]
            except KeyError:
                continue

            console(m)

    stating = 'Status "{search}" ({home})'
    self.console(stating.format(search=search, home=home))

    if list_settings.long_listing:
        long_status()
    else:
        short_status()
    return 0

#
#
def open_role(role, home):
    open_home(home)

    if not hb.role_exists(role):
        doesnt_exist(role, home)
    hb.open_role(None, None)

#
#
def role_history(self, role, home):
    open_role(role, home)

    def long_history():
        now = datetime.datetime.now(ar.UTC)
        for s in hb.role_start_stop[2]:
            start = ar.world_to_text(s.start)
            if s.stop is None:
                console('%s ... ?' % (start,))
                continue
            stop = ar.world_to_text(s.stop)
            d = s.stop - s.start
            span = '%s' % (short_delta(d),)
            if isinstance(s.returned, ar.Incognito):
                console('%s ... %s (%s) %s' % (start, stop, span, s.returned.type_name))
            else:
                console('%s ... %s (%s) %s' % (start, stop, span, s.returned.__class__.__name__))

    def short_history():
        for i, s in enumerate(hb.role_start_stop[2]):
            now = datetime.datetime.now(ar.UTC)
            d = now - s.start
            start = '%s ago' % (short_delta(d),)
            if s.stop is None:
                console('[%d] %s ... ?' % (i, start))
                continue
            d = s.stop - s.start
            stop = short_delta(d)
            if isinstance(s.returned, ar.Incognito):
                console('[%d] %s ... %s (%s)' % (i, start, stop, s.returned.type_name))
            else:
                console('[%d] %s ... %s (%s)' % (i, start, stop, s.returned.__class__.__name__))

    revising = 'Accessing history "{role}", "{home}"'
    self.console(revising.format(role=role, home=home))

    if list_settings.long_listing:
        long_history()
    else:
        short_history()
    return 0

def from_last(last):
    d = datetime.datetime.now(ar.UTC)

    if last == START_OF.MONTH:
        f = datetime.datetime(d.year, d.month, 1, tzinfo=d.tzinfo)
    elif last == START_OF.WEEK:
        dow = d.weekday()
        dom = d.day - 1
        if dom >= dow:
            f = datetime.datetime(d.year, d.month, d.day - dow, tzinfo=d.tzinfo)
        elif d.month > 1:
            t = dow - dom
            r = calendar.monthrange(d.year, d.month - 1)
            f = datetime.datetime(d.year, d.month - 1, r[1] - t, tzinfo=d.tzinfo)
        else:
            t = dow - dom
            r = calendar.monthrange(d.year - 1, 12)
            f = datetime.datetime(d.year - 1, 12, r[1] - t, tzinfo=d.tzinfo)
    elif last == START_OF.DAY:
        f = datetime.datetime(d.year, d.month, d.day, tzinfo=d.tzinfo)
    elif last == START_OF.HOUR:
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, tzinfo=d.tzinfo)
    elif last == START_OF.MINUTE:
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, minute=d.minute, tzinfo=d.tzinfo)
    elif last == START_OF.HALF:
        t = d.minute % 30
        m = d.minute - t
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, minute=m, tzinfo=d.tzinfo)
    elif last == START_OF.QUARTER:
        t = d.minute % 15
        m = d.minute - t
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, minute=m, tzinfo=d.tzinfo)
    elif last == START_OF.TEN:
        t = d.minute % 10
        m = d.minute - t
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, minute=m, tzinfo=d.tzinfo)
    elif last == START_OF.FIVE:
        t = d.minute % 5
        m = d.minute - t
        f = datetime.datetime(d.year, d.month, d.day, hour=d.hour, minute=m, tzinfo=d.tzinfo)
    else:
        return None
    return f

#
#
def clocker(self, begin, end, count):
    try:
        for d, t in read_log(hb.role_logs, begin, end, count):
            if self.halted:
                return ar.Aborted()
            c = d.astimezone(tz=None)           # To localtime.
            s = c.strftime('%Y-%m-%dt%H:%M:%S') # Normal part.
            f = c.strftime('%f')[:3]            # Up to milliseconds.
            h = '%s.%s' % (s, f)
            i = t.index(' ')
            sys.stdout.write(h)
            console(t[i:], newline=False)
    except Exception as e:
        condition = str(e)
        fault = ar.Faulted(condition)
        return fault
    return None

ar.bind(clocker)

#
#
def printer(self, begin, end, count):
    try:
        for _, t in read_log(hb.role_logs, begin, end, count):
            if self.halted:
                return ar.Aborted()
            console(t, newline=False)
    except Exception as e:
        condition = str(e)
        fault = ar.Faulted(condition)
        return fault
    return None

ar.bind(printer)

#
#
def world_or_clock(s, clock):
    if clock:
        t = ar.text_to_clock(s)
        d = datetime.datetime.fromtimestamp(t, tz=ar.UTC)
        return d
    return ar.text_to_world(s)

def role_log(self, role, home):
    open_role(role, home)

    begin, end = None, None
    if log_settings.from_ is not None:
        begin = world_or_clock(log_settings.from_, log_settings.clock)
        self.console('Beginning at from')
    elif log_settings.last is not None:
        begin = from_last(log_settings.last)
        if begin is None:
            raise SubCannot('cannot resolve <last>')
        self.console('Beginning at LAST')
    elif log_settings.start is not None:
        if role.count('.') > 0:
            raise SubCannot('log from <start> requires an entry <role>')
        start_stop = hb.role_start_stop[2]
        if log_settings.start < 0:
            y = len(start_stop) + log_settings.start
        else:
            y = log_settings.start
        try:
            s = start_stop[y]
        except IndexError:
            fault = '<start>[%d] does not exist (%d entries)' % (log_settings.start, len(start_stop))
            raise SubCannot(fault)
        begin = s.start
        p1 = y + 1
        if p1 < len(start_stop):
            end = start_stop[p1].start
        else:
            end = None
        self.console('Beginning at START')
    elif log_settings.back is not None:
        d = datetime.datetime.now(ar.UTC)
        t = datetime.timedelta(seconds=log_settings.back)
        begin =  d - t
        self.console('Beginning at BACK')

    count = None
    if log_settings.to is not None:
        end = world_or_clock(log_settings.to, log_settings.clock)
        self.console('Ending at TO')
    elif log_settings.span is not None:
        t = datetime.timedelta(seconds=log_settings.span)
        end = begin + t
        self.console('Ending at SPAN')
    elif log_settings.count is not None:
        count = log_settings.count
        # Override an assignment associated with "start".
        end = None
        self.console('Ending on COUNT')
    # Else
    #   end remains as the default None or
    #   the stop part of a start-stop.

    # Now that <begin> and <end> have been established, a
    # few more sanity checks.
    if begin is None:
        fault = 'cannot log "{role}" - no <begin>'.format(role=role)
        raise SubCannot(fault)

    if end is not None and end < begin:
        fault = 'cannot log "{role}" - <end> is before <begin>'.format(role=role)
        raise SubCannot(fault)

    extracting = 'Extracting logs "{role}", "{home}"'
    self.console(extracting.format(role=role, home=home))

    if log_settings.clock:
        a = self.create(clocker, begin, end, count)
    else:
        a = self.create(printer, begin, end, count)
    m = self.select(ar.Stop, ar.Completed)
    if isinstance(m, ar.Stop):
        ar.halt(a)
        m = self.select(ar.Completed)
        raise SubCompletion(1)
    value = m.value
    if value is None:   # Reached the end.
        pass
    elif isinstance(value, ar.Faulted):     # Failed to complete stream.
        fault = str(value)
        raise SubFailed(fault)
    elif isinstance(value, ar.Aborted):     # Interrupted.
        raise SubCompletion(1)
    else:
        raise SubFailed('unexpected log printer response <%r>' % (value,))

    return 0

def home_folder(self, selected, role, home):
    open_home(home)

    def folder(role):
        hb.open_role(None, None)
        d = {
            'bin': hb.bin,
            'settings': hb.settings,
            'logs': hb.role_logs,
            'tmp': hb.role_tmp,
            'model': hb.role_model,
            'resource': hb.role_resource,
        }
        try:
            s = d[selected]
        except KeyError:
            fault = 'unknown {folder} ({role}, {path})'.format(role=role, path=hb.home_path, folder=selected)
            raise SubCannot(fault)
        if s is None:
            fault = 'role "{role}" ({path}) has no {folder}'.format(role=role, path=hb.home_path, folder=selected)
            raise SubCannot(fault)
        console('%s' % (s.path,))

    if not hb.role_exists(role):
        doesnt_exist(role, home)

    folding = 'Resolving folders "{selected}" ("{role}", "{home}")'
    self.console(folding.format(selected=selected, role=role, home=home))

    folder(role)

    return 0

def input_by_role(self, role, home):
    open_home(home)

    # Find matches or all.
    matched = find_files(role, hb.input)
    #_, running = matched_status(self, matched, search, settings.force)

    updating = 'Updating input "{search}" ({home}), {count} matches'
    self.console(updating.format(search=role, home=home, count=len(matched)))

    if input_settings.set_file:
        settings = [
            '--input-file={input}'.format(input=input_settings.set_file),
            '--store-input=true',
        ]
    else:   # Get file.
        if len(matched) != 1:
            raise SubCannot('multiple inputs ({n} matches)'.format(n=len(matched)))
        # Cant use sub-process as encoding is placed on stdout.
        m = matched[0]
        hb.role_exists(m)
        #hb.open_role(None, None)
        #if hb.input_by_role is None or hb.input_by_role[1] is None:
        #    raise SubCannot('role "{role}" has no default input'.format(role=m))
        input_change = os.path.join(hb.input.path, m + '.json')
        try:
            with open(input_change, 'r') as f:
                s = f.read()
        except OSError as e:
            raise SubCannot('no file for "{role}" ({name})'.format(role=m, name=input_change))
        sys.stdout.write(s)
        sys.stdout.write('\n')
        return 0

    try:
        for m in matched:
            hb.role_exists(m)
            hb.open_role(None, None)
            if input_settings.executable and hb.role_executable[2] != input_settings.executable:
                continue
            executable_name = hb.executable_name()
            updating = 'Running "{executable}" ({role}) to update input'
            self.console(updating.format(role=m, executable=executable_name))
            a = self.create(ar.Process, executable_name, origin=ar.ORIGIN_RUN,
                home_path=hb.home_path, role_name=m,
                settings=settings)
            self.assign(a, hb.role)
            r = self.select(ar.Completed, ar.Stop)
            if isinstance(r, ar.Stop):
                raise SubCompletion(1)
            # Process completed. Remove record.
            m = self.debrief()
            value = r.value
            if isinstance(value, ar.Ack):
                pass
            elif isinstance(value, ar.Faulted):
                reason = str(value)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
            else:
                reason = 'unexpected response from component (%r)' % (value,)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
    finally:
        abort(self)
        #start_process(self, running)

    return 0

def settings_by_role(self, role, home):
    open_home(home)

    # Find matches or all.
    matched = find_files(role, hb.settings)
    #_, running = matched_status(self, matched, search, settings.force)

    updating = 'Updating settings "{search}" ({home}), {count} matches'
    self.console(updating.format(search=role, home=home, count=len(matched)))

    if input_settings.set_file:
        settings = [
            '--settings-file={input}'.format(input=input_settings.set_file),
            '--store-settings=true',
        ]
    else:   # Get file.
        if len(matched) != 1:
            raise SubCannot('multiple inputs ({n} matches)'.format(n=len(matched)))
        # Cant use sub-process as encoding is placed on stdout.
        m = matched[0]
        hb.role_exists(m)
        #hb.open_role(None, None)
        #if hb.settings_by_role is None or hb.settings_by_role[1] is None:
        #    raise SubCannot('role "{role}" has no settings'.format(role=m))
        settings_change = os.path.join(hb.settings.path, m + '.json')
        try:
            with open(settings_change, 'r') as f:
                s = f.read()
        except OSError as e:
            raise SubCannot('no file for "{role}" ({name})'.format(role=m, name=settings_change))
        sys.stdout.write(s)
        sys.stdout.write('\n')
        return 0

    try:
        for m in matched:
            hb.role_exists(m)
            hb.open_role(None, None)
            if input_settings.executable and hb.role_executable[2] != input_settings.executable:
                continue
            executable_name = hb.executable_name()
            updating = 'Running "{executable}" ({role}) to update settings'
            self.console(updating.format(role=m, executable=executable_name))
            a = self.create(ar.Process, executable_name, origin=ar.ORIGIN_RUN,
                home_path=hb.home_path, role_name=m,
                settings=settings)
            self.assign(a, hb.role)
            r = self.select(ar.Completed, ar.Stop)
            if isinstance(r, ar.Stop):
                raise SubCompletion(1)
            # Process completed. Remove record.
            m = self.debrief()
            value = r.value
            if isinstance(value, ar.Ack):
                pass
            elif isinstance(value, ar.Faulted):
                reason = str(value)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
            else:
                reason = 'unexpected response from component (%r)' % (value,)
                fault = 'cannot store settings for "{role}" ({home}) - {reason}'
                raise SubFailed(fault.format(role=m, home=home, reason=reason))
    finally:
        abort(self)
        #start_process(self, running)

    return 0

def store(v, t=None, pretty=False):
    codec = ar.CodecJson(pretty_format=pretty)
    t = t or ar.UserDefined(type(v))
    s = codec.encode(v, t)
    if pretty:
        s += '\n'
    return s

def recover(s, c, t=None):
    codec = ar.CodecJson()
    t = t or ar.UserDefined(type(c))
    v = codec.decode(s, t)
    return v

def get_property(self, selected, role, home):
    open_role(role, home)

    getting = 'Getting property "{selected}" ("{role}", "{home}")'
    self.console(getting.format(selected=selected, role=role, home=home))

    property = {
        'retry': hb.role_retry,
        'storage': hb.role_storage,
        'connect-above': hb.role_connect_above,
        'accept-below': hb.role_accept_below,
        'directory-scope': hb.role_directory_scope,
    }
    try:
        p = property[selected]
    except KeyError:
        fault = '"{property}" ({role}) does not exist'
        raise SubFailed(fault.format(property=selected, role=role))

    if p is None or p[2] is None:
        fault = '"{property}" ({role}) is not set'
        raise SubFailed(fault.format(property=selected, role=role))

    try:
        s = store(p[2], t=p[0], pretty=True)
    except ar.CodecFailed as e:
        reason = str(e)
        fault = '"{property}" ({role}) {reason})'
        raise SubFailed(fault.format(property=selected, role=role, reason=reason))

    sys.stdout.write(s)
    return 0

def set_property(self, settings, selected, role, home, j):
    open_home(home)

    # Find matches or all.
    search, matched = find_matches(role, set_settings.invert_search, executable=set_settings.executable)
    _, running = matched_status(self, matched, search, settings.force)

    # Decode the new value.
    if j is not None:
        try:
            content = {
                "retry": ar.UserDefined(ar.RetryIntervals),
                "storage": ar.Integer8(),
				'connect-above': ar.Any(),
				'accept-below': ar.UserDefined(ar.HostPort),
        		'directory-scope': ar.Integer8(),
            }
            t = content[selected]
            p, v = recover(j, None, t)
        except KeyError:
            start_process(self, running)
            fault = 'unknown property "{property}"'
            raise SubCannot(fault.format(property=selected))
        except ar.CodecFailed as e:
            start_process(self, running)
            reason = str(e)
            fault = '"{property}" ({role}), {reason})'
            raise SubCannot(fault.format(property=selected, role=role, reason=reason))

    setting = 'Setting property "{search}" ({home})'
    self.console(setting.format(search=search, home=home))

    try:
        for m in matched:
            hb.role_exists(m)
            hb.open_role(None, None)
            property = {
                'retry': hb.role_retry,
                'storage': hb.role_storage,
				'connect-above': hb.role_connect_above,
				'accept-below': hb.role_accept_below,
        		'directory-scope': hb.role_directory_scope,
            }
            tfv = property[selected]
            if j is not None:
                tfv[1].store(p)
            else:
                os.remove(tfv[1].name + '.json')    # TBF - This needs a proper method.
    except KeyError:
        fault = 'unknown property "{property}" (during store/remove)'
        raise SubCannot(fault.format(property=selected))
    except ar.FileFailure as e:
        reason = str(e)
        fault = '"{property}" ({role}), {reason})'
        raise SubFailed(fault.format(property=selected, role=role, reason=reason))
    finally:
        self.console('Clear locks and complete bounces')
        start_process(self, running)

    return 0

def edit_property(self, settings, selected, role, home):
    search, matched = role, [role]
    open_role(role, home)

    property = {
        'retry': hb.role_retry,
        'storage': hb.role_storage,
		'connect-above': hb.role_connect_above,
		'accept-below': hb.role_accept_below,
        'directory-scope': hb.role_directory_scope,
    }
    try:
        t, f, v = property[selected]
    except KeyError:
        fault = '"{property}" ({role}) does not exist'
        raise SubCannot(fault.format(property=selected, role=role))

    _, running = matched_status(self, matched, search, settings.force)

    editing = 'Editing property "{selected}" ("{role}", "{home}")'
    self.console(editing.format(selected=selected, role=role, home=home))

    try:
        self.console('Prepare materials for editor session')
        fd, name = tempfile.mkstemp()
        os.close(fd)

        # Prepare materials for editor.
        temporary = ar.File(name, t, decorate_names=False)
        if v is not None:
            temporary.store(v)
        else:
            temporary.store(ar.make(t))

        # Setup detection of change.
        modified = os.stat(name).st_mtime

        # Run the editor.
        self.console('Run the editor')
        editor = os.getenv('ANSAR_EDITOR') or 'vi'
        a = self.create(ar.Utility, editor, name)
        self.assign(a, editor)
        m = self.select(ar.Completed)
        e = self.debrief()
        value = m.value
        if isinstance(value, ar.Faulted):
            s = str(value)
            condition = 'unexpected editor behaviour "{error}"'.format(error=s)
            raise SubFailed(condition)
        elif isinstance(value, ar.Aborted):
            raise SubCompletion(1)

        # Was the file modified?
        if os.stat(name).st_mtime == modified:
            cannot('property not modified')
            raise SubCompletion(0)

        # Validate contents and update the runtime.
        self.console('Parse the materials before setting')
        a, _ = temporary.recover()
        f.store(a)
    except ar.CodecFailed as e:
        condition = str(e)
        raise SubFailed(condition)
    except ar.FileFailure as e:
        condition = str(e)
        raise SubFailed(condition)
    finally:
        # Clean out the file used as a temporary
        # edit space.
        self.console('Clear out edit artefacts and complete bounces')
        os.remove(name)

        # Restart the processes if it was running
        # previously.
        start_process(self, running)

    return 0

# DEPLOY
# Transfer machinery
def folder_transfer(self, delta, target):
    """An async routine to copy folders-and-files to target folder."""

    # Interruption happens at the lowest level of transfer activity, i.e before
    # each IO operation (i.e. read or write of blocks). Parent object calls
    # a halt() on this object and the halted flag is checked by every delta
    # opcode (e.g. storage.AddFile) before every IO. If halted it raises the special
    # TransferHalted exception to jump back to this code.
    machine = ar.DeltaMachine(self, target)
    try:
        self.console('File transfer ({deltas} deltas) to {target}'.format(deltas=len(delta), target=target))
        for d in delta:
            d(machine)
        self.console('Move {aliases} aliases to targets'.format(aliases=machine.aliases()))
        machine.rename()
    except ar.TransferHalted:
        return ar.Aborted()
    except OSError as e:
        condition = str(e)
        fault = ar.Faulted(condition)
        return fault
    finally:
        self.console('Clear {aliases} aliases'.format(aliases=machine.aliases()))
        machine.clear()
    return ar.Ack()

ar.bind(folder_transfer)

class INITIAL: pass
class RUNNING: pass
class HALTED: pass

class FolderTransfer(ar.Point, ar.StateMachine):
    def __init__(self, delta, target):
        ar.Point.__init__(self)
        ar.StateMachine.__init__(self, INITIAL)
        self.delta = delta
        self.target = target
        self.transfer = None

def FolderTransfer_INITIAL_Start(self, message):
    self.transfer = self.create(folder_transfer, self.delta, self.target)
    return RUNNING

def FolderTransfer_RUNNING_Completed(self, message):
    value = message.value
    self.complete(value)

def FolderTransfer_RUNNING_Stop(self, message):
    ar.halt(self.transfer)
    return HALTED

def FolderTransfer_HALTED_Completed(self, message):
    self.complete(ar.Aborted())

FOLDER_TRANSFER_DISPATCH = {
    INITIAL: (
        (ar.Start,), ()
    ),
    RUNNING: (
        (ar.Completed, ar.Stop), ()
    ),
    HALTED: (
        (ar.Completed,), ()
    ),
}

ar.bind(FolderTransfer, FOLDER_TRANSFER_DISPATCH)

#
#
class STOPPED: pass

class SettingsTransfer(ar.Point, ar.StateMachine):
    def __init__(self, role, executable, settings_change, setting_values):
        ar.Point.__init__(self)
        ar.StateMachine.__init__(self, INITIAL)
        self.role = role
        self.executable = executable
        self.settings_change = settings_change
        self.setting_values = setting_values
        self.transfer = None

def SettingsTransfer_INITIAL_Start(self, message):
    role = self.role
    executable = self.executable
    settings_change = self.settings_change
    setting_values = self.setting_values

    settings = []
    if settings_change:
        self.console('Settings file "{file}" to {role} ({executable})'.format(file=settings_change, role=role, executable=executable))
        settings.append('--settings-file={input}'.format(input=settings_change))

    if setting_values:
        values = ', '.join(setting_values.keys())
        self.console('Values files "{values}" to {role} ({executable})'.format(values=values, role=role, executable=executable))
        for s, v in setting_values.items():
            with open(v, "r") as f:
                value = f.read()
            settings.append('--{setting}={value}'.format(setting=s, value=value))

    settings.append('--store-settings=true')

    self.transfer = self.create(ar.Process, executable, origin=ar.ORIGIN_RUN, debug=object_settings.debug_level,
        home_path=hb.home_path, role_name=role,
        settings=settings)
    return RUNNING

def SettingsTransfer_RUNNING_Completed(self, message):
    value = message.value
    self.complete(value)

def SettingsTransfer_RUNNING_Stop(self, message):
    self.send(message, self.transfer)
    return STOPPED

def SettingsTransfer_STOPPED_Completed(self, message):
    self.complete(ar.Aborted())

SETTINGS_TRANSFER_DISPATCH = {
    INITIAL: (
        (ar.Start,), ()
    ),
    RUNNING: (
        (ar.Completed, ar.Stop), ()
    ),
    STOPPED: (
        (ar.Completed,), ()
    ),
}

ar.bind(SettingsTransfer, SETTINGS_TRANSFER_DISPATCH)

#
#
class InputTransfer(ar.Point, ar.StateMachine):
    def __init__(self, role, executable, input_change):
        ar.Point.__init__(self)
        ar.StateMachine.__init__(self, INITIAL)
        self.role = role
        self.executable = executable
        self.input_change = input_change
        self.transfer = None

def InputTransfer_INITIAL_Start(self, message):
    role = self.role
    executable = self.executable
    input_change = self.input_change

    settings = []
    self.console('Input file "{file}" to {role} ({executable})'.format(file=input_change, role=role, executable=executable))
    settings.append('--input-file={input}'.format(input=input_change))

    settings.append('--store-input=true')

    self.transfer = self.create(ar.Process, executable, origin=ar.ORIGIN_RUN, debug=object_settings.debug_level,
            home_path=hb.home_path, role_name=role,
            settings=settings)
    return RUNNING

def InputTransfer_RUNNING_Completed(self, message):
    value = message.value
    self.complete(value)

def InputTransfer_RUNNING_Stop(self, message):
    self.send(message, self.transfer)
    return STOPPED

def InputTransfer_STOPPED_Completed(self, message):
    self.complete(ar.Aborted())

INPUT_TRANSFER_DISPATCH = {
    INITIAL: (
        (ar.Start,), ()
    ),
    RUNNING: (
        (ar.Completed, ar.Stop), ()
    ),
    STOPPED: (
        (ar.Completed,), ()
    ),
}

ar.bind(InputTransfer, INPUT_TRANSFER_DISPATCH)

#
#
def deploy_storage(self, settings, build, storage, home):
    open_home(home)

    # Extract the map of role-executable, i.e. many-to-1.
    def executable(r):
        hb.role_exists(r)
        hb.open_role(None, None)
        return hb.role_executable[2]
    role_executable = {r: executable(r) for r in hb.entry_list()}

    # And the inverse map, i.e. 1-to-many.
    executable_roles = {}
    for r, e in role_executable.items():
        try:
            roles = executable_roles[e]
        except KeyError:
            roles = set()
            executable_roles[e] = roles
        roles.add(r)

    roles = set(role_executable.keys())
    executables = set(executable_roles.keys())

    # Results of scans for change.
    file_change = []
    settings_change = []
    input_change = []
    setting_value_change = []

    # Unique set of names of the roles affected
    # by the detected changes.
    touching_roles = set()

    def cannot_deploy(bs, fs, bt, ft):
        if not bs:
            return 'unexpected source "{f}"'.format(f=fs)
        if not bt:
            return 'target not found'
        return 'no error'

    if build:
        build = os.path.abspath(build)
        # Special case of file transfer method.
        SHARED_BIN = ar.DELTA_FILE_ADD | ar.DELTA_FILE_UPDATE    # Cant do ar.DELTA_FILE_UGM, no source.
        s, ugm = ar.storage_manifest(build)
        t, _ = ar.storage_manifest(hb.bin.path)
        delta = [d for d in ar.storage_delta(s, t, flags=SHARED_BIN)]
        changing = set(d.source.name for d in delta)

        if len(changing) > 0:               # There is significant change.
            touched = len(touching_roles)
            for c in changing:                  # Executable
                r = executable_roles.get(c)     # Roles configured with.
                if r:
                    touching_roles |= r               # Remember.

            todo = (build, hb.bin.path, delta, ugm)        # Record of todo.
            file_change.append(todo)
            detected = 'Detected {executables} changing executables (added {roles} associated roles)'
            self.console(detected.format(executables=len(changing), roles=len(touching_roles) - touched))

    # Results of scan without regard to whether something
    # has changed, i.e. this is what is available.
    resource_by_executable = {}
    model_by_role = {}
    settings_by_role = {}
    input_by_role = {}
    setting_value_by_role = {}

    if storage:
        storage = os.path.abspath(storage)
        # Load all the deployment methods defined in this
        # storage area.
        method = set(f for f in os.listdir(storage))

        # For each method scan for changes and record in the
        # relevant results list.
        if 'resource-by-executable' in method:
            p = os.path.join(storage, 'resource-by-executable')

            # It might be possible to treat the entire resource
            # folder as one manifest but determining which
            # executables/roles are changing becomes much harder.
            for executable in os.listdir(p):
                source = os.path.join(p, executable)
                target = os.path.join(hb.resource.path, executable)
                bs, bt = os.path.isdir(source), os.path.isdir(target)
                if not bs or not bt:
                    cd = cannot_deploy(bs, 'folder', bt, 'folder')
                    self.warning('Cannot deploy "resource-by-executable/{executable}" ({error})'.format(executable=executable, error=cd))
                    continue
                s, ugm = ar.storage_manifest(source)
                t, _ = ar.storage_manifest(target)
                delta = [d for d in ar.storage_delta(s, t)]
                resource_by_executable[executable] = source
                if len(delta) > 0:
                    touched = len(touching_roles)
                    r = executable_roles.get(executable)
                    if r:
                        touching_roles |= r
                    todo = (source, target, delta, ugm)
                    file_change.append(todo)
                    detected = 'Detected {changes} resource changes for "{executable}" (added {roles} associated roles)'
                    self.console(detected.format(changes=len(delta), executable=executable, roles=len(touching_roles) - touched))

        if 'model-by-executable' in method:
            # To be considered. See settings-by-executable.
            pass

        if 'model-by-role' in method:
            p = os.path.join(storage, 'model-by-role')
            for role in os.listdir(p):
                source = os.path.join(p, role)
                target = os.path.join(hb.model.path, role)
                bs, bt = os.path.isdir(source), os.path.isdir(target)
                if not bs or not bt:
                    cd = cannot_deploy(bs, 'folder', bt, 'folder')
                    self.warning('Cannot deploy "model-by-role/{role}" ({error})'.format(role=role, error=cd))
                    continue
                s, ugm = ar.storage_manifest(source)
                t, _ = ar.storage_manifest(target)
                delta = [d for d in ar.storage_delta(s, t)]
                model_by_role[role] = source
                if len(delta) > 0:
                    touching_roles.add(role)
                    todo = (source, target, delta, ugm)
                    file_change.append(todo)
                    detected = 'Detected {changes} model changes for "{role}"'
                    self.console(detected.format(changes=len(delta), role=role))

        # Settings and input.
        if 'settings-by-executable' in method:
            # To be considered. Creates complex relationship between
            # settings for all roles using an executable, specific roles
            # and setting values. And then figure out what should be done
            # when one of these files changes or one of the related
            # setting value files changes.
            pass

        if 'settings-by-role' in method:
            p = os.path.join(storage, 'settings-by-role')
            for r in os.listdir(p):
                role, _ = os.path.splitext(r)
                source = os.path.join(p, r)
                target = os.path.join(hb.settings.path, r)
                bs, bt = os.path.isfile(source), os.path.isfile(target)
                if not bs or not bt:
                    cd = cannot_deploy(bs, 'file', bt, 'file')
                    self.warning('Cannot deploy "settings-by-role/{role}" ({error})'.format(role=r, error=cd))
                    continue
                s = os.stat(source)
                t = os.stat(target)
                settings_by_role[role] = source
                if s.st_mtime > t.st_mtime:
                    touching_roles.add(role)
                    todo = (source, role, None, None)
                    settings_change.append(todo)
                    detected = 'Detected settings change for "{role}"'
                    self.console(detected.format(role=role))

        if 'setting-value-by-executable' in method:
            # To be considered. See settings-by-executable.
            pass

        if 'setting-value-by-role' in method:
            p = os.path.join(storage, 'setting-value-by-role')
            # Each role.
            for role in os.listdir(p):
                role_path = os.path.join(p, role)
                if not os.path.isdir(role_path):
                    self.warning('Cannot deploy "setting-value-by-role/{role}" (unexpected source)'.format(role=role))
                    continue
                target = os.path.join(hb.settings.path, role + '.json')
                if not os.path.isfile(target):
                    self.warning('Cannot deploy "setting-value-by-role/{role}" (target not found)'.format(role=role))
                    continue
                t = os.stat(target)
                setting_value = {}
                sv = []
                # Each setting.
                for s in os.listdir(role_path):
                    setting, _ = os.path.splitext(s)
                    source = os.path.join(role_path, s)
                    if not os.path.isfile(source):
                        self.warning('Cannot deploy "setting-value-by-role/{role}/{setting}" (unexpected source)'.format(role=role, setting=s))
                        continue
                    # Value for setting for role.
                    v = os.stat(source)
                    setting_value[setting] = source
                    if v.st_mtime > t.st_mtime:
                        todo = (setting, source)
                        sv.append(todo)
                setting_value_by_role[role] = setting_value
                if len(sv) > 0:
                    touching_roles.add(role)
                    todo = (None, role, sv, None)
                    setting_value_change.append(todo)
                    detected = 'Detected {changes} setting-value changes for "{role}"'
                    self.console(detected.format(changes=len(sv), role=role))

        if 'input-by-role' in method:
            p = os.path.join(storage, 'input-by-role')
            for r in os.listdir(p):
                role, _ = os.path.splitext(r)
                source = os.path.join(p, r)
                target = os.path.join(hb.input.path, r)
                bs, bt = os.path.isfile(source), os.path.isfile(target)
                if not bs or not bt:
                    cd = cannot_deploy(bs, 'file', bt, 'file')
                    self.warning('Cannot deploy "input-by-role/{role}" ({error})'.format(role=r, error=cd))
                    continue
                s = os.stat(source)
                t = os.stat(target)
                input_by_role[role] = source
                if s.st_mtime > t.st_mtime:
                    touching_roles.add(role)
                    todo = (source, role, None, None)
                    input_change.append(todo)
                    detected = 'Detected input changes for "{role}"'
                    self.console(detected.format(role=role))

    if len(file_change) < 1 and len(settings_change) < 1 and len(setting_value_change) < 1 and len(input_change) < 1:
        self.console('Nothing to deploy')
        return 0

    search = ', '.join(touching_roles)
    _, running = matched_status(self, touching_roles, search, settings.force)
    n = len(running)

    try:
        self.console('Starting transfer of materials')

        for t in file_change:
            target = t[1]
            delta = t[2]
            a = self.create(FolderTransfer, delta, target)
            self.assign(a, t)

        full_settings = set()
        for s in settings_change:
            source = s[0]
            role = s[1]
            full_settings.add(role)
            # Overlay any defined setting-value content.
            v = setting_value_by_role.get(role)
            a = self.create(SettingsTransfer, role, role_executable[role], source, v)
            self.assign(a, s)

        for rsv in setting_value_change:
            role = rsv[1]
            sv = rsv[2]
            if role in full_settings:
                continue
            v = {s: v for s, v in sv}
            a = self.create(SettingsTransfer, role, role_executable[role], None, v)
            self.assign(a, rsv)

        while self.working():
            m = self.select(ar.Completed, ar.Stop)
            if isinstance(m, ar.Stop):
                raise SubCompletion(1)
            # Completed.
            t = self.debrief()
            self.console('Completed transfer to "{target}"'.format(target=t[1]))
            value = m.value
            if isinstance(value, ar.Ack):   # Reached the end.
                pass
            elif isinstance(value, ar.Faulted):     # Failed to complete transfer.
                fault = str(value)
                self.console('Fault in transfer to "{target}" ({fault})'.format(target=t[1], fault=fault))
                raise SubFailed(fault)
            else:
                raise SubFailed('unexpected transfer response <%r>' % (value,))

        for i in input_change:
            source = i[0]
            role = i[1]
            a = self.create(InputTransfer, role, role_executable[role], source)
            self.assign(a, i)

        while self.working():
            m = self.select(ar.Completed, ar.Stop)
            if isinstance(m, ar.Stop):
                raise SubCompletion(1)
            # Completed.
            t = self.debrief()
            self.console('Completed transfer to "{target}"'.format(target=t[1]))
            value = m.value
            if isinstance(value, ar.Ack):   # Reached the end.
                pass
            elif isinstance(value, ar.Faulted):     # Failed to complete transfer.
                fault = str(value)
                self.console('Fault in transfer to "{target}" ({fault})'.format(target=t[1], fault=fault))
                raise SubFailed(fault)
            else:
                raise SubFailed('unexpected transfer response <%r>' % (value,))
    finally:
        self.abort()
        while self.working():
            c = self.select(ar.Completed)
            d = self.debrief()

        n = len(running)
        if n > 0:
            self.console('Restoring {n} stopped roles'.format(n=n, roles=running))
            start_process(self, running)
    return 0

def extract_storage(self, settings, storage, home):
    open_home(home)

    # Extract the map of role-executable, i.e. many-to-1.
    def executable(r):
        hb.role_exists(r)
        hb.open_role(None, None)
        return hb.role_executable[2]
    role_executable = {r: executable(r) for r in hb.entry_list()}

    # And the inverse map, i.e. 1-to-many.
    executable_roles = {}
    for r, e in role_executable.items():
        try:
            roles = executable_roles[e]
        except KeyError:
            roles = set()
            executable_roles[e] = roles
        roles.add(r)

    roles = set(role_executable.keys())
    #executables = set(executable_roles.keys())

    # Results of scans for change.
    # Source, target, delta, ugm
    file_change = []
    #setting_value_change = []

    touching_roles = set()

    storage = os.path.abspath(storage)
    try:
        os.makedirs(storage)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    method = set(f for f in os.listdir(storage))

    source = hb.resource.path
    target = os.path.join(storage, 'resource-by-executable')
    s, ugm = ar.storage_manifest(source)
    if 'resource-by-executable' in method or s.manifests > 0 or s.listings > 0:
        # As a read-only space its debatable whether this should
        # be part of an extraction.
        # Handled as a wholesale delta rather than per-executable.
        try:
            os.makedirs(target)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        t, _ = ar.storage_manifest(target)
        delta = [d for d in ar.storage_delta(s, t)]
        if len(delta) > 0:
            for k in s.content.keys():
                r = executable_roles.get(k)
                if r:
                    touching_roles |= r
            todo = (source, target, delta, ugm)
            file_change.append(todo)
            detected = 'Detected {resources} resource changes ({roles} associated roles)'
            self.console(detected.format(resources=len(delta), roles=len(touching_roles)))

    source = hb.model.path
    target = os.path.join(storage, 'model-by-role')
    s, ugm = ar.storage_manifest(source)
    if 'model-by-role' in method or s.manifests > 0 or s.listings > 0:
        try:
            os.makedirs(target)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        t, _ = ar.storage_manifest(target)
        delta = [d for d in ar.storage_delta(s, t)]
        if len(delta) > 0:
            r = set(s.content.keys())
            touching_roles |= r
            todo = (source, target, delta, ugm)
            file_change.append(todo)
            detected = 'Detected {changes} model changes ({roles} associated roles)'
            self.console(detected.format(changes=len(delta), roles=len(r)))

    source = hb.settings.path
    target = os.path.join(storage, 'settings-by-role')
    s, ugm = ar.storage_manifest(source)
    if 'settings-by-role' in method or s.manifests > 0 or s.listings > 0:
        try:
            os.makedirs(target)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        t, _ = ar.storage_manifest(target)
        delta = [d for d in ar.storage_delta(s, t)]
        if len(delta) > 0:
            r = set(os.path.splitext(k)[0] for k in s.content.keys())
            touching_roles |= r
            todo = (source, target, delta, ugm)
            file_change.append(todo)
            detected = 'Detected {changes} settings changes ({roles} associated roles)'
            self.console(detected.format(changes=len(delta), roles=len(r)))

    if 'setting-value-by-role' in method:
        pass

    source = hb.input.path
    target = os.path.join(storage, 'input-by-role')
    s, ugm = ar.storage_manifest(source)
    if 'input-by-role' in method or s.manifests > 0 or s.listings > 0:
        try:
            os.makedirs(target)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        t, _ = ar.storage_manifest(target)
        delta = [d for d in ar.storage_delta(s, t)]
        if len(delta) > 0:
            r = set(os.path.splitext(k)[0] for k in s.content.keys())
            touching_roles |= r
            todo = (source, target, delta, ugm)
            file_change.append(todo)
            detected = 'Detected {changes} input changes ({roles} associated roles)'
            self.console(detected.format(changes=len(delta), roles=len(r)))

    if len(file_change) < 1:
        self.console('Nothing to extract')
        return 0

    search = ', '.join(touching_roles)
    _, running = matched_status(self, touching_roles, search, settings.force)
    n = len(running)

    try:
        self.console('Starting extraction of materials')

        for t in file_change:
            target = t[1]
            delta = t[2]
            a = self.create(FolderTransfer, delta, target)
            self.assign(a, t)

        while self.working():
            m = self.select(ar.Completed, ar.Stop)
            if isinstance(m, ar.Stop):
                raise SubCompletion(1)
            # Completed.
            t = self.debrief()
            self.console('Completed extraction to "{target}"'.format(target=t[1]))
            value = m.value
            if isinstance(value, ar.Ack):   # Reached the end.
                pass
            elif isinstance(value, ar.Faulted):     # Failed to complete transfer.
                fault = str(value)
                self.console('Fault in extraction to "{target}" ({fault})'.format(target=t[1], fault=fault))
                raise SubFailed(fault)
            else:
                raise SubFailed('unexpected extraction response <%r>' % (value,))
    finally:
        self.abort()
        while self.working():
            c = self.select(ar.Completed)
            d = self.debrief()

        n = len(running)
        if n > 0:
            self.console('Restoring {n} stopped roles'.format(n=n, roles=running))
            start_process(self, running)
    return 0

def returned_value(self, role, home, timeout, start):
    open_role(role, home)

    start_stop = hb.role_start_stop[2]
    if len(start_stop) < 1:
        fault = 'role "{role}" has no start/stop records ({home})'
        raise SubCannot(fault.format(role=role, home=home))

    if start is None:
        start = len(start_stop) - 1
    elif start < 0:
        start = len(start_stop) + start
        if start < 0:
            fault = 'start out-of-range'
            raise SubCannot(fault)
    elif start < len(start_stop):
        pass
    else:
        fault = 'start out-of-range'
        raise SubCannot(fault)

    # Criteria met - valid row in the table.
    start_stop = hb.role_start_stop[2]
    selected = start_stop[start]
    anchor = selected.start

    def returned(r):
        try:
            s = store(r, t=ar.Any(), pretty=True)
        except ar.CodecFailed as e:
            fault = str(e)
            raise SubFailed(fault)
        sys.stdout.write(s)

    # This row has already returned.
    if selected.stop is not None:
        returned(selected.returned)
        return 0

    # Cannot poll for completion of anything other
    # than the last row.
    start_stop = hb.role_start_stop[2]
    if start != len(start_stop) - 1:
        fault = 'selected start did not complete'
        raise SubCannot(fault)

    if timeout is not None:
        self.start(ar.T1, timeout)

    self.start(ar.T2, 1.0)
    while True:
        m = self.select(ar.Stop, ar.T1, ar.T2)
        if isinstance(m, ar.Stop):
            break
        elif isinstance(m, ar.T1):
            returned(ar.TimedOut())
            return 1
        elif isinstance(m, ar.T2):
            r, v = hb.role_start_stop[1].recover()
            if len(r) < start:
                fault = 'lost original start position - index out-of-range'
                raise SubCannot(fault)
            if r[start].start != anchor:
                fault = 'lost original start position - datetime anchor'
                raise SubCannot(fault)

            if r[start].stop is not None:
                returned(r[start].returned)
                break
            self.start(ar.T2, 1.0)

    return 0

def ls_args(ls):
    args = ['--%s=%s' % (k, v) for k, v in ls[0].items()]
    args.extend(['-%s=%s' % (k, v) for k, v in ls[1].items()])
    return args

#
#
HOME = 'home'
ROLE = 'role'
EXECUTABLE = 'executable'

def word_argument(i, w, a, d, name):
    if i < len(w):
        p = w[i]
        if a:
            raise SubCannot(f'a value for "{name}" detected as a word and an argument')
        return p
    return a or d

def create(self, _, ls, word):
    home = word_argument(0, word, create_settings.home_path, DEFAULT_HOME, HOME)
    return create_home(self, home)

def add(self, _, ls, word):
    executable = word_argument(0, word, add_settings.executable, None, EXECUTABLE)
    role = word_argument(1, word, add_settings.role_name, DEFAULT_ROLE, ROLE)
    home = word_argument(2, word, add_settings.home_path, DEFAULT_HOME, HOME)
    if executable is None:
        raise SubCannot('an <executable> is required')
    b = ar.breakpath(executable)
    if b[0]:
        raise SubCannot('the <executable> must be the name of a loadable file to be found in <bin>')
    return add_role(self, executable, role, home, ls)

def update(self, settings, ls, word):
    role = word_argument(0, word, update_settings.role_name, None, ROLE)
    home = word_argument(1, word, update_settings.home_path, DEFAULT_HOME, HOME)
    return update_role(self, settings, role, home, ls_args(ls))

def delete(self, settings, ls, word):
    # Settings reuse.
    role = word_argument(0, word, update_settings.role_name, None, ROLE)
    home = word_argument(1, word, update_settings.home_path, DEFAULT_HOME, HOME)
    return delete_role(self, settings, role, home)

def list_(self, _, ls, word):
    role = word_argument(0, word, list_settings.role_name, None, ROLE)
    home = word_argument(1, word, list_settings.home_path, DEFAULT_HOME, HOME)
    return list_home(self, role, home)

def destroy(self, settings, ls, word):
    # Settings reuse.
    home = word_argument(0, word, create_settings.home_path, DEFAULT_HOME, HOME)
    return destroy_home(self, settings, home)

def start(self, settings, ls, word):
    role = word_argument(0, word, start_settings.role_name, None, ROLE)
    home = word_argument(1, word, start_settings.home_path, DEFAULT_HOME, HOME)
    return start_role(self, settings, role, home, ls_args(ls))

def run(self, settings, ls, word):
    role = word_argument(0, word, run_settings.role_name, None, ROLE)
    home = word_argument(1, word, run_settings.home_path, DEFAULT_HOME, HOME)
    return run_role(self, settings, role, home, ls_args(ls))

def stop(self, settings, ls, word):
    role = word_argument(0, word, stop_settings.role_name, None, ROLE)
    home = word_argument(1, word, stop_settings.home_path, DEFAULT_HOME, HOME)
    return stop_role(self, settings, role, home)

def status(self, _, ls, word):
    # Settings reuse.
    role = word_argument(0, word, list_settings.role_name, None, ROLE)
    home = word_argument(1, word, list_settings.home_path, DEFAULT_HOME, HOME)
    return home_status(self, role, home)

def history(self, _, ls, word):
    # Settings reuse.
    role = word_argument(0, word, list_settings.role_name, None, ROLE)
    home = word_argument(1, word, list_settings.home_path, DEFAULT_HOME, HOME)
    if not role or role.count('.') > 0:
        raise SubCannot('an entry <role> is required')
    return role_history(self, role, home)

def log(self, _, ls, word):
    role = word_argument(0, word, log_settings.role_name, None, ROLE)
    home = word_argument(1, word, log_settings.home_path, DEFAULT_HOME, HOME)
    if not role:
        raise SubCannot('a <role> is required')

    # Initial sanity checks and a default <begin>.
    f = [log_settings.from_, log_settings.last, log_settings.start, log_settings.back]
    c = len(f) - f.count(None)
    if c == 0:
        log_settings.back = ar.text_to_span('5m')   # Default query of last 5 mins.
    elif c != 1:
        raise SubCannot('one of <from>, <last>, <start> or <back> is required')

    t = [log_settings.to, log_settings.span, log_settings.count]
    c = len(t) - t.count(None)
    if c == 0:
        pass        # Default is query to end-of-log or end of start-stop.
    elif c != 1:
        raise SubCannot('one of <to>, <span> or <count> is required')

    return role_log(self, role, home)

def folder(self, _, ls, word):
    # Settings reuse.
    selected = word_else(0, word, None)
    role = word_argument(1, word, list_settings.role_name, None, ROLE)
    home = word_argument(2, word, list_settings.home_path, DEFAULT_HOME, HOME)
    if selected is None:
        raise SubCannot('one of the standard <space> names is required')
    if role is None:
        raise SubCannot('a <role> is required')
    return home_folder(self, selected, role, home)

def input_(self, _, ls, word):
    role = word_argument(0, word, input_settings.role_name, None, ROLE)
    home = word_argument(1, word, input_settings.home_path, DEFAULT_HOME, HOME)
    return input_by_role(self, role, home)

def settings(self, _, ls, word):
    # Settings reuse.
    role = word_argument(0, word, input_settings.role_name, None, ROLE)
    home = word_argument(1, word, input_settings.home_path, DEFAULT_HOME, HOME)
    return settings_by_role(self, role, home)

def get(self, _, ls, word):
    # Settings reuse.
    selected = word_argument(0, word, set_settings.property, None, ROLE)
    role = word_argument(1, word, set_settings.role_name, None, ROLE)
    home = word_argument(2, word, set_settings.home_path, DEFAULT_HOME, HOME)
    if selected is None:
        raise SubCannot('a <property> is required')
    if role is None:
        raise SubCannot('a <role> is required')
    return get_property(self, selected, role, home)

def set_(self, settings, ls, word):
    selected = word_argument(0, word, set_settings.property, None, ROLE)
    role = word_argument(1, word, set_settings.role_name, None, ROLE)
    home = word_argument(2, word, set_settings.home_path, DEFAULT_HOME, HOME)
    if selected is None:
        raise SubCannot('a <property> is required')

    if set_settings.not_set:
        j = None
    elif set_settings.encoding_file:
        with open(set_settings.encoding_file, 'r') as f:
            j = f.read()
    else:
        j = sys.stdin.read()

    return set_property(self, settings, selected, role, home, j)

def edit(self, settings, ls, word):
    # Settings reuse.
    selected = word_argument(0, word, edit_settings.property, None, ROLE)
    role = word_argument(1, word, edit_settings.role_name, None, ROLE)
    home = word_argument(2, word, edit_settings.home_path, DEFAULT_HOME, HOME)
    if selected is None:
        raise SubCannot('a <property> is required')
    if role is None:
        raise SubCannot('a <role> is required')

    return edit_property(self, settings, selected, role, home)

def deploy(self, settings, ls, word):
    build = word_argument(0, word, deploy_settings.build_path, None, ROLE)
    snapshot = word_argument(1, word, deploy_settings.snapshot_path, None, ROLE)
    home = word_argument(2, word, deploy_settings.home_path, DEFAULT_HOME, HOME)
    if build is None and snapshot is None:
        raise SubCannot('no <build> and no <snapshot> - nothing to do')
    return deploy_storage(self, settings, build, snapshot, home)

def extract(self, settings, ls, word):
    # Settings reuse.
    snapshot = word_argument(0, word, deploy_settings.snapshot_path, None, ROLE)
    home = word_argument(1, word, deploy_settings.home_path, DEFAULT_HOME, HOME)
    if snapshot is None:
        raise SubCannot('no <snapshot> - nothing to do')
    return extract_storage(self, settings, snapshot, home)

def returned(self, _, ls, word):
    role = word_argument(0, word, returned_settings.role_name, None, ROLE)
    home = word_argument(1, word, returned_settings.home_path, DEFAULT_HOME, HOME)
    if role is None:
        raise SubCannot('a <role> is required')
    timeout = returned_settings.timeout
    start = returned_settings.start

    return returned_value(self, role, home, timeout, start)

# Support functions for the
# sub-command and args machinery.
def jump_table(*args):
    t = {a[0].__name__.rstrip('_'): a for a in args}
    return t

# Bring all the functions together as a table that
# uses the function name, i.e. f.__name__ as a key.
table = jump_table(
    (create, create_settings),
    (add, add_settings),
    (update, update_settings),
    (delete, update_settings),
    (list_, list_settings),
    (destroy, create_settings),
    (start, start_settings),
    (run, run_settings),
    (stop, stop_settings),
    (status, list_settings),
    (history, list_settings),
    (log, log_settings),
    (folder, list_settings),
    (input_, input_settings),
    (settings, input_settings),
    (get, set_settings),
    (set_, set_settings),
    (edit, edit_settings),
    (deploy, deploy_settings),
    (extract, deploy_settings),
    (returned, returned_settings),
)

# The command-line tool that performs CRUD for a collection
# of process descriptions, and the associated CRUD of the
# process instances.
def ansar(self, settings):
    sub_function, r, word = ar.command_words()
    if sub_function is None:
        return 0

    # Everything lined up for execution of
    # the selected sub-command.
    code = 0
    name = sub_function.__name__.rstrip('_')
    try:
        self.trace('Call the sub-command function')
        code = sub_function(self, settings, r, word)

    except SubCompletion as c:
        code = c.code
    except SubCannot as e:
        cannot('cannot perform "{sub}", {error}', sub=name, error=str(e))
        code = 1
    except SubFailed as e:
        cannot('command "{sub}" failed, {error}', sub=name, error=str(e))
        code = 1
    except ValueError as e:
        cannot('cannot perform "{sub}" command, {error}', sub=name, error=str(e))
        code = 1
    except OSError as e:
        cannot('cannot perform "{sub}" command, {error}', sub=name, error=str(e))
        code = 1
    return code

ar.bind(ansar)

def word_else(i, w, d):
    if i < len(w):
        return w[i]
    return d

#
#
def sub_parameters(specific_settings):
    if specific_settings is not None:
        a = object_settings.__art__.value.keys()        # Framework values.
        b = specific_settings.__art__.value.keys()      # Application.
        c = set(a) & set(b)
        if len(c) > 0:
            j = ', '.join(c)
            raise ValueError('collision in settings names - {collisions}'.format(collisions=j))

    executable, ls1, sub, ls2, word = ar.sub_args()
    x1, r1 = ar.extract_args(object_settings, ls1, specific_settings)
    ar.arg_values(object_settings, x1)

    # Support for the concept of a noop pass, just for the
    # framework.
    def no_sub_required(s):
        return s.help or s.dump_settings or s.dump_input

    if sub is not None:
        try:
            sub_function, sub_settings = table[sub]
        except KeyError:
            raise ValueError('unknown sub-command "{sub}"'.format(sub=sub))

        if sub_settings:
            x2, r2 = ar.extract_args(sub_settings, ls2, None)
            ar.arg_values(sub_settings, x2)
        else:
            r2 = ls2
    elif no_sub_required(object_settings):
        # Give framework a chance to complete some
        # admin operation.
        sub_function = None
        r2 = ({}, {})
    else:
        raise ValueError('no-op command')

    bundle = (sub_function, # The sub-command function.
        r2,                 # Remainder from ls2, i.e. for passing to sub-component
        word)               # Non-flag arguments.

    return executable, bundle, r1

# Entry point for packaging. The
# $ ansar command starts here.
class AnsarSettings(object):
    def __init__(self, force=False, user_name=None, user_key=None):
        self.force = force
        self.user_name = user_name
        self.user_key = user_key

ANSAR_SETTINGS_SCHEMA = {
    'force': ar.Boolean(),
    'user_name': ar.Unicode(),
    'user_key': ar.Block(),
}

ar.bind(AnsarSettings, object_schema=ANSAR_SETTINGS_SCHEMA)

#
#
compiled_defaults=AnsarSettings()

def main():
    ar.create_object(ansar, factory_settings=compiled_defaults, parameter_passing=sub_parameters)

# The standard entry point. Needed for IDEs
# and debugger sessions.
if __name__ == '__main__':
    main()
