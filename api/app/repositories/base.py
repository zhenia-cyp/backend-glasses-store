from sqlalchemy.orm import Session



class BaseRepository(object):
    def __init__(self, session: Session):
        self.session = session
