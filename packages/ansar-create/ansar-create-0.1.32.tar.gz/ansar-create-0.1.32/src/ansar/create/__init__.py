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

"""Tools and runtime for asynchronous programming.

Repo: git@github.com:mr-ansar/ansar-create.git
Branch: main
Commit: 8ebfca5bacb229828a9b2218bdb208ee814d867f
Version: 0.1.31 (2023-10-30@12:18:01+NZDT)
"""

from ansar.encode import *

from .coding import Gas, breakpath
from .space import NO_SUCH_ADDRESS
from .space import create_an_object, find_object, destroy_an_object
from .space import OpenAddress
from .space import abdicate_to_address, discard_address
from .space import send_a_message
from .space import set_queue, get_queue, get_queue_address
from .space import start_a_thread, running_in_thread

from .lifecycle import Start, Completed, Faulted
from .lifecycle import Stop, Aborted, TimedOut
from .lifecycle import Nothing, Ready, ExitCode, Enquiry
from .lifecycle import Maybe, Cannot, Interrupted, Exhausted
from .lifecycle import Ack, Nak
from .lifecycle import HostPort

from .pending import Queue, Buffering, Machine, InputTimeout

from .point import Point
from .point import completed_object
from .point import T1, T2, T3, T4
from .point import StartTimer, CancelTimer
from .point import PointLog
from .point import RedirectLog
from .point import OpenTap, CloseTap, TapLine
from .point import Threaded, Channel
from .point import object_dispatch
from .point import bind_point, bind_function
from .point import halt
from .point import AutoStop
from .point import PointTest

from .machine import Stateless, StateMachine, bind_stateless, bind_statemachine

from .retry import RetryIntervals, intervals_only, smart_intervals, Retry
from .locking import LockUp, lock_file, unlock_file, LockedOut, lock_and_hold

from .log import PEAK_BEFORE_BLOCKING, LogAgent
from .log import log_to_stderr, log_to_nowhere, select_logs, LogToMemory
from .rolling import read_log

from .test import TestReport, TestSuite, test_enquiry

from .root import start_up, tear_down
from .root import open_channel, drop_channel, OpenChannel, AddOn
from .object import LOG_NUMBER, ObjectSettings, object_settings
from .home import Homebase
from .framework import create_object
from .processing import Process, Punctuation, Utility, process_args
from .processing import ORIGIN_START, ORIGIN_RUN, ORIGIN_CALL
from .args import command_args, sub_args, extract_args, arg_values, component_args, word_else
from .args import environment_variables

from .framework import command_executable, command_words, command_variables
from .framework import command_settings, store_settings
from .framework import resource_folder, tmp_folder, model_folder
from .framework import resource_path, tmp_path, model_path

from .storage import DELTA_FILE_ADD, DELTA_FILE_UPDATE, DELTA_FILE_UGM, DELTA_FILE_REMOVE
from .storage import DELTA_FOLDER_ADD, DELTA_FOLDER_UPDATE, DELTA_FOLDER_UGM, DELTA_FOLDER_REMOVE
from .storage import DELTA_FILE_CRUD, DELTA_FOLDER_CRUD
from .storage import DELTA_CRUD

from .storage import TransferHalted, DeltaMachine
from .storage import StorageTables, StorageAttributes, StorageManifest, StorageListing
from .storage import storage_manifest, storage_delta, storage_walk
from .storage import AddFolder, RemoveFolder
from .storage import AddFile, UpdateFile, RemoveFile, UpdateUser, UpdateGroup, UpdateMode
from .storage import ReplaceWithFile, ReplaceWithFolder

from .binding import bind_any

bind = bind_any
create = create_object
