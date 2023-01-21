import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


Base = declarative_base()


PostLike = sa.Table(
    'post_likes',
    Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('post_id', UUID(as_uuid=True), sa.ForeignKey('posts.id'), nullable=False),
    sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
    sa.Column('date', sa.Date(), default=datetime.date.today)
)


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = sa.Column(sa.String(150), unique=True)
    first_name = sa.Column(sa.String(100), nullable=False)
    last_name = sa.Column(sa.String(100), nullable=False)
    hashed_password = sa.Column(sa.Text())
    is_active = sa.Column(sa.Boolean(), default=True)
    last_login = sa.Column(sa.DateTime(), nullable=False)
    last_request = sa.Column(sa.DateTime(), nullable=False)

    posts = relationship('Post', backref='creator')
    liked_posts = relationship('Post', secondary=PostLike, backref='liked_by', lazy='subquery')

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sa.Column(sa.String())
    owner_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.title}'


