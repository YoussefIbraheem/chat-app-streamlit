from sqlalchemy import (
    String,
    Integer,
    create_engine,
    Column,
    ForeignKey,
    DateTime,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from enum import Enum as PyEnum
from datetime import datetime


class Base(DeclarativeBase):
    pass


class RoleEnum(PyEnum):
    AI = "ai"
    HUMAN = "human"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True , autoincrement=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True , autoincrement=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    role = Column(SQLEnum(RoleEnum,values_callable=lambda x: [e.value for e in x]), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    conversation = relationship("Conversation", back_populates="messages")


engine = create_engine("sqlite:///chat_history.db")

sessionLocal = sessionmaker(bind=engine)



Base.metadata.create_all(engine)


def get_session():
    return sessionLocal()


def create_conversation(session, title):
    conv = Conversation(title=title,created_at=datetime.now())
    session.add(conv)
    session.commit()
    return conv


def create_message(session, body, conversation_id, role: RoleEnum):
    message = Message(body=body,conversation_id=conversation_id,role=role,created_at = datetime.now())
    session.add(message)
    session.commit()
    return message


def get_conversations(session):
    return session.query(Conversation).order_by(Conversation.created_at.desc()).all()


def get_conversation(session, conversation_id):
    return session.query(Conversation).filter_by(id=conversation_id).first()


def delete_conversation(session,conversation_id):
    conversation = session.query(Conversation).filter_by(id=conversation_id).first()
    session.delete(conversation)
    session.commit()


def get_messages(session, conversation_id):
    return session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc()).all()
    


def get_message(session, conversation_id, message_id):
    return (
        session.query(Message)
        .filter_by(id=message_id, conversation_id=conversation_id)
        .first()
    )
