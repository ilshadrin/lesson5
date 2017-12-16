from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///blog.sqlite') # выбираем с какой БД мы будем работать, в данном случае это "sqlite"

db_session = scoped_session(sessionmaker(bind=engine)) #создаем сессию для раоты с БД, соединение с БД  bind=engine - связываем сессию с базой

Base = declarative_base()   # деклоративная БД, будем работать с БД как с питон кодом            
Base.query = db_session.query_property() #привязываем к declarative_base возможность делать запросы к БД


class User(Base):  #объявляем нашу таблицу как класс юзер, передаем Base. Это означает, что класс Юзер наследуется от класса Ваse
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # для таблице юзерс создает колонки/столбцы   primary_key=True - id будет первичным ключем
    first_name = Column(String(50)) #  строка
    last_name = Column(String(50)) # строка
    email = Column(String(120), unique=True) # unique=True - проверка на уникальность email
    posts = relationship('Post', backref='author') #связь между таблицами, говорим что будем связываться с классом Post /// backref='author' - создает связь

    def __init__(self, first_name=None, last_name=None, email=None): #__init__ - конструктор класса, используется (вызывается автоматически) при создании нового юзера
        self.first_name=first_name  #self - обращение к самому себе
        self.last_name=last_name
        self.email=email

    def __repr__(self):  #вывод информации 
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.email)



class Post(Base): #начинается работа с таблицей, создаем таблицу Posts
    __tablename__='posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    image = Column(String(500))
    published = Column(DateTime)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title=None, image=None, published=None, content=None, user_id=None): 
        self.title=title  
        self.image=image
        self.published=published
        self.content=content
        self.user_id=user_id

    def __repr__(self):
        return '<Post {}>'.format(self.title)



if __name__ == "__main__": #если этот файл вызвали напрямую 
    Base.metadata.create_all(bind=engine)