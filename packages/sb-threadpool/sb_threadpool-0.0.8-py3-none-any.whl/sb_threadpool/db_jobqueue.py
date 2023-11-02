import typing
from threading import Lock
from typing import TypeVar, Generic

from sb_db_common import Session
from .jobqueue import JobQueue

T = TypeVar("T", bound="Job")


class Dbhelper(object):
    def __init__(
        self, provider_name: str, table_name: str = "job_queue", db_name: str = ""
    ):
        self.provider_name = provider_name
        self.table_name = table_name
        self.db_name = db_name

        self.reset_query = f"update {self.table_name} set in_progress = 0;"
        self.queue_get_next_item_query = (
            f"select id, item from {self.table_name} where in_progress = 0 and "
            "retries < 6 order by id limit 1;"
        )
        self.queue_count_query = f"select count(*) from {self.table_name} where in_progress = 0 and retries < 6;"
        self.clear_queue_query = f"delete from {self.table_name};"

        if provider_name == "sqlite":
            self.exists_query = f"SELECT count(*) FROM sqlite_schema WHERE type='table' and name = '{self.table_name}';"
            self.create_query = (
                f"create table {self.table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, item text, in_progress integer, "
                f"retries integer, errors text);"
            )
            self.queue_insert_query = (
                f"insert into {self.table_name}(item, in_progress, retries, errors) values "
                "(:item, 0, 0, '');"
            )
            self.queue_delete_query = f"delete from {self.table_name} where id = :id"
            self.queue_set_in_progress_query = f"update {self.table_name} set in_progress = :in_progress where id = :id"
            self.queue_retry_query = (
                f"update {self.table_name} set in_progress = 0, retries = retries + 1 where "
                "id = :id"
            )
            self.queue_fail_query = f"update {self.table_name} set in_progress = 0, retries = 6 where id = :id"
            self.already_in_queue_query = (
                f"select count(*) from {self.table_name} where item = :item;"
            )
        elif provider_name == "mysql":
            self.exists_query = (
                f"select count(*) from INFORMATION_SCHEMA.tables where TABLE_SCHEMA = '{db_name}' and "
                f"TABLE_TYPE = 'BASE TABLE' and TABLE_NAME = '{self.table_name}'"
            )
            self.create_query = (
                f"create table {self.table_name}(id int PRIMARY KEY AUTO_INCREMENT, item varchar(1000), "
                f"in_progress int, retries int, errors varchar(500));"
            )
            self.queue_insert_query = (
                f"insert into {self.table_name}(item, in_progress, retries, errors) values "
                "(%(item)s, 0, 0, '');"
            )
            self.queue_delete_query = f"delete from {self.table_name} where id = %(id)s"
            self.queue_set_in_progress_query = (
                f"update {self.table_name} set in_progress = %(in_progress)s where "
                "id = %(id)s"
            )
            self.queue_retry_query = (
                f"update {self.table_name} set in_progress = 0, retries = retries + 1 where "
                "id = %(id)s"
            )
            self.queue_fail_query = f"update {self.table_name} set in_progress = 0, retries = 6 where id = %(id)s"
            self.already_in_queue_query = (
                f"select count(*) from {self.table_name} where item = %(item)s;"
            )
        elif provider_name == "pgsql":
            self.exists_query = (
                f"select count(*) from INFORMATION_SCHEMA.tables where TABLE_CATALOG = '{db_name}' "
                f"and TABLE_TYPE = 'BASE TABLE' and TABLE_NAME = '{self.table_name}'"
            )
            self.create_query = (
                f"create table {self.table_name}(id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY, item varchar(1000), "
                f"in_progress int, retries int, errors varchar(500));"
            )
            self.queue_insert_query = (
                f"insert into {self.table_name}(item, in_progress, retries, errors) values "
                "(%(item)s, 0, 0, '') returning id;"
            )
            self.queue_delete_query = f"delete from {self.table_name} where id = %(id)s"
            self.queue_set_in_progress_query = (
                f"update {self.table_name} set in_progress = %(in_progress)s where "
                "id = %(id)s"
            )
            self.queue_retry_query = (
                f"update {self.table_name} set in_progress = 0, retries = retries + 1 where "
                "id = %(id)s"
            )
            self.queue_fail_query = f"update {self.table_name} set in_progress = 0, retries = 6 where id = %(id)s"
            self.already_in_queue_query = (
                f"select count(*) from {self.table_name} where item = %(item)s;"
            )
        else:
            raise Exception("Unknown provider name")


class DbJobQueue(JobQueue, Generic[T]):
    session: Session
    db_helper: Dbhelper

    def __init__(self, session: Session, table_name: str = "job_queue"):
        super().__init__()
        self.lock = Lock()
        self.session = session

        provider_name = session.connection.provider_name
        self.db_helper = Dbhelper(
            provider_name, table_name, session.connection.database
        )

        result = session.fetch_scalar(self.db_helper.exists_query)
        if result == 0:
            session.execute(self.db_helper.create_query)
            session.commit()

        session.execute(self.db_helper.reset_query)
        session.commit()

    def get_job(self) -> T | None:
        try:
            self.lock.acquire()
            row = self.session.fetch_one(self.db_helper.queue_get_next_item_query)
            if row is not None:
                cls = typing.get_args(self.__orig_class__)[0]
                job = cls(row[0])
                job.load(row)

                params = {"id": job.name, "in_progress": 1}
                self.session.execute(self.db_helper.queue_set_in_progress_query, params)
                self.session.commit()
                return job
            else:
                return None

        except Exception as ex:
            print(ex)
            return None
        finally:
            self.lock.release()

    def queue_job(self, job: T):
        result = self.session.fetch_scalar(
            self.db_helper.already_in_queue_query, {"item": job.item}
        )
        if result == 0:
            self.session.execute(self.db_helper.queue_insert_query, {"item": job.item})
            self.session.commit()

    def commit_job(self, job: T):
        self.session.execute(self.db_helper.queue_delete_query, {"id": job.name})
        self.session.commit()

    def rollback_job(self, job: T):
        self.session.execute(self.db_helper.queue_retry_query, {"id": job.name})
        self.session.commit()

    def fail_job(self, job: T):
        self.session.execute(self.db_helper.queue_fail_query, {"id": job.name})
        self.session.commit()

    def count(self) -> int:
        try:
            self.lock.acquire()
            count = self.session.fetch_scalar(self.db_helper.queue_count_query)
            return count
        finally:
            self.lock.release()

    def clear(self):
        try:
            self.lock.acquire()
            self.session.execute(self.db_helper.clear_queue_query)
            self.session.commit()
        finally:
            self.lock.release()

    def close(self):
        try:
            self.lock.acquire()
            self.session.close()
        finally:
            self.lock.release()
