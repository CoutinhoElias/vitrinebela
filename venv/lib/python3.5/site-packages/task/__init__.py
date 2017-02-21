# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Vishvananda Ishaya
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Stores tasks and allows them to be run again later.
"""


import datetime
import functools
import inspect
import logging
import types
import uuid


import db


class Failure(Exception):
    def __init__(self, progress):
        self.progress = progress


_now = datetime.datetime.utcnow


def inject_now_method(method):
    global _now
    _now = method
    db.inject_now_method(method)


def _create(task_name, method, is_member, *args, **kwargs):
    now = _now()
    task_id = str(uuid.uuid4())
    logging.debug('Creating task %s at %s', task_id, now)
    task = {'id': task_id,
            'task_name': task_name,
            'method': method,
            'is_member': is_member,
            'args': args,
            'kwargs': kwargs,
            'created_at': now,
            'updated_at': now,
            'is_active': False,
            'progress': None}
    db.task_create(task)
    return task_id


def _is_member(func, args):
    """Checks args to determine if func is a bound method."""
    if not args:
        return False
    ismethod = False
    for item in inspect.getmro(type(args[0])):
        for x in inspect.getmembers(item):
            if 'im_func' in dir(x[1]):
                ismethod = x[1].im_func == func
                if ismethod:
                    break
        else:
            continue
        break
    return ismethod


def ify(name=None, auto_update=True):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if 'task_id' in kwargs:
                task_id = kwargs.pop('task_id')
                progress = kwargs.pop('progress')
                if not auto_update:
                    return func(task_id=task_id, progress=progress, *args, **kwargs)

                try:
                    rv = func(task_id=task_id, progress=progress, *args, **kwargs)
                except Failure as ex:
                    fail(task_id, ex.progress)
                    return ex.progress
                except Exception as ex:
                    fail(task_id, None)
                    raise
                if not isinstance(rv, types.GeneratorType):
                    update(task_id, rv)
                    finish(task_id)
                    return rv

                def gen():
                    try:
                        for orig_rv in rv:
                            update(task_id, orig_rv)
                            yield orig_rv
                    except Failure as ex:
                        fail(task_id, ex.progress)
                        yield ex.progress
                    except Exception as ex:
                        fail(task_id, None)
                        raise StopIteration
                    finish(task_id)

                return gen()

            else:
                task_name = name or func.__name__
                if _is_member(wrapped, args):
                    method = func.__name__
                    is_member = True
                else:
                    method = wrapped
                    is_member = False
                task_id = _create(task_name, method, is_member,
                                  *args, **kwargs)
                return task_id
        return wrapped
    return wrapper


def get(task_id):
    """Get task from id."""
    return db.task_get(task_id)


def claim(task_name=None):
    """Get a free task_id if available optionally by task_name."""
    try:
        return db.task_pop(task_name)['id']
    except IndexError:
        return None


def timeout(time, task_name=None):
    """Free tasks by time and optional task_name.

    :returns: number of tasks freed"""
    return db.task_timeout(time, task_name)


def run(task_id):
    """Runs the task with task id.

    Underlying method will receive two kwargs:
        task_id = id of the current task for updating
        progress = last progress passed to task_update"""
    task = db.task_get(task_id)
    if task['is_member']:
        method = getattr(task['args'][0], task['method'])
    else:
        method = task['method']
    db.task_start(task_id)
    return method(task_id=task['id'], progress=task['progress'],
                  *task['args'], **task['kwargs'])


def fail(task_id, progress=None):
    """Fail the current task with optional progress."""
    now = _now()
    values = {}
    values['updated_at'] = now
    values['is_active'] = False
    if progress:
        values['progress'] = progress
    db.task_update(task_id, values)
    logging.debug('Failed task %s at %s', task_id, now)


def update(task_id, progress):
    """Update the current task progress."""
    now = _now()
    values = {}
    values['updated_at'] = now
    values['progress'] = progress
    db.task_update(task_id, values)
    logging.debug('Updated task %s at %s', task_id, now)


def finish(task_id):
    """Mark the task completed."""
    values = {}
    values['updated_at'] = _now()
    values['completed_at'] = _now()
    values['is_active'] = False
    db.task_update(task_id, values)
    logging.debug('Finished task %s', task_id)


def is_active(task_id):
    """True if the task is active."""
    try:
        return db.task_get(task_id)['is_active']
    except db.TaskNotFound:
        return False


def is_complete(task_id):
    """Completed if the task is done."""
    try:
        return db.task_get(task_id)['completed_at'] is not None
    except db.TaskNotFound:
        return False


def exists(task_id):
    """True if the task exists."""
    try:
        db.task_get(task_id)
        return True
    except db.TaskNotFound:
        return False


def setup_db(sql_connection='sqlite:///task.sqlite'):
    """True if the task exists."""
    db.connect(sql_connection)
