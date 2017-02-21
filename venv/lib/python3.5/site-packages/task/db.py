# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Vishvananda Ishaya
# Copyright 2011 Openstack, LLC
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
SQLAlchemy code for storing tasks.

Some portions borrowed Openstack Compute.
"""

import datetime

from sqlalchemy import exc, orm, create_engine
from sqlalchemy import Boolean, Column, DateTime, Integer, PickleType, String
from sqlalchemy.ext import declarative


_now = datetime.datetime.utcnow


def inject_now_method(method):
    global _now
    _now = method


_ENGINE = None
_MAKER = None
_SQL_CONNECTION = None


def connect(sql_connection):
    """Register Models and create metadata."""
    global _SQL_CONNECTION
    global _ENGINE
    global _MAKER
    _ENGINE = None
    _MAKER = None
    _SQL_CONNECTION = sql_connection
    get_session()
    Task.metadata.create_all(_ENGINE)


def get_session(autocommit=True, expire_on_commit=False):
    """Helper method to grab session"""
    global _SQL_CONNECTION
    global _ENGINE
    global _MAKER
    if not _MAKER:
        if not _ENGINE:
            kwargs = {'pool_recycle': 3600,
                      'echo': False}

            _ENGINE = create_engine(_SQL_CONNECTION,
                                    **kwargs)
        _MAKER = (orm.sessionmaker(bind=_ENGINE,
                                   autocommit=autocommit,
                                   expire_on_commit=expire_on_commit))
    session = _MAKER()
    return session


class Duplicate(Exception):
    pass


class TaskNotFound(Exception):
    pass


def _runtime_now():
    return _now()


class Task(declarative.declarative_base()):
    """Represents a running service on a host."""
    __tablename__ = 'tasks'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    created_at = Column(DateTime, default=_runtime_now)
    updated_at = Column(DateTime, onupdate=_runtime_now)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    id = Column(String(255), primary_key=True)
    task_name = Column(String(255))
    is_member = Column(Boolean)
    is_active = Column(Boolean, default=True)
    completed_at = Column(DateTime)
    attempts = Column(Integer, default=0)
    method = Column(PickleType)
    progress = Column(PickleType)
    args = Column(PickleType)
    kwargs = Column(PickleType)

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        try:
            session.flush()
        except exc.IntegrityError, e:
            if str(e).endswith('is not unique'):
                raise Duplicate(str(e))
            else:
                raise

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = _now()
        self.save(session=session)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(orm.object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        columns = orm.object_mapper(self).columns
        for key, value in values.iteritems():
            if key in columns:
                setattr(self, key, value)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()


def task_destroy(task_id):
    session = get_session()
    with session.begin():
        task_ref = task_get(task_id, session=session)
        task_ref.delete(session=session)


def task_get(task_id, session=None):
    if not session:
        session = get_session()

    result = session.query(Task).\
                     filter_by(id=task_id).\
                     filter_by(deleted=False).\
                     first()

    if not result:
        raise TaskNotFound()

    return result


def task_timeout(time, task_name=None):
    session = get_session()
    query = session.query(Task).\
                    filter(Task.updated_at < time).\
                    filter_by(is_active=True).\
                    filter_by(deleted=False).\
                    filter_by(completed_at=None)
    if task_name:
        query = query.filter_by(task_name=task_name)
    result = query.update({Task.is_active: False,
                           Task.updated_at: _now()},
                           synchronize_session='fetch')
    return result


def task_pop(task_name=None):
    session = get_session()
    with session.begin():
        query = session.query(Task).\
                        filter_by(is_active=False).\
                        filter_by(deleted=False).\
                        filter_by(completed_at=None)
        if task_name:
            query = query.filter_by(task_name=task_name)
        task_ref = query.with_lockmode('update').first()
        # NOTE(vish): if with_lockmode isn't supported, as in sqlite,
        #             then this has concurrency issues
        if not task_ref:
            raise IndexError
        task_ref.is_active = True
        session.add(task_ref)
    return task_ref


def task_create(values):
    task_ref = Task()
    task_ref.update(values)
    task_ref.save()
    return task_ref


def task_start(task_id):
    session = get_session()
    with session.begin():
        session.query(Task).\
                filter_by(id=task_id).\
                update({Task.attempts: Task.attempts + 1,
                        Task.updated_at: _now(),
                        Task.is_active: True})


def task_update(task_id, values):
    session = get_session()
    with session.begin():
        task_ref = task_get(task_id, session=session)
        task_ref.update(values)
        task_ref.save(session=session)
