from sqlalchemy.ext.asyncio import AsyncSession



class BaseRepository(object):
    def __init__(self, session: AsyncSession):
        self.session = session
