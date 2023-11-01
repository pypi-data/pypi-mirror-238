from unittest import IsolatedAsyncioTestCase

from brickworks.cli import _get_settings
from brickworks.db import db, set_sessionmaker


class RollbackTestcase(IsolatedAsyncioTestCase):
    """
    Testcase that will cause new objects to be marked as "testdata"
    and will delete that data after every test
    Will also start a session for each test, so no need to use @standalone_session
    make sure to super the asyncTearDown and asyncSetup methods!
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = _get_settings()

    async def asyncSetUp(self) -> None:
        set_sessionmaker(self.settings)
        self._db = db(self.settings)  # pylint: disable=attribute-defined-outside-init
        await self._db.__aenter__()  # pylint: disable=unnecessary-dunder-call

        return await super().asyncSetUp()

    async def asyncTearDown(self) -> None:
        await db.session.rollback()
        await db.session.close()
        await self._db.__aexit__(None, None, None)  # pylint: disable=unnecessary-dunder-call
        return await super().asyncTearDown()
