import streamlit as strmlt
from db import (
    create_conversation,
    get_conversations,
    get_conversation,
    get_session,
    get_messages,
    create_message,
    delete_conversation,
    RoleEnum,
)
from ai import get_chain_w_history , summerize_chat_content
from langchain.memory import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import random

strmlt.set_page_config(layout="wide")
strmlt.title(
    "Welcome to Langchain Chat App :rainbow[Smarter Version]! 🦜🔗🧠",
    help="It will remeber your past conversastions!",
)


session = get_session()

conversations = get_conversations(session=session)

conversations_titles = [conv.title for conv in conversations]
conversations_id = [conv.id for conv in conversations]

strmlt.session_state.require_reset = False
strmlt.session_state.active_conv_id = None
previous_conv_id = strmlt.session_state.active_conv_id


with strmlt.sidebar:
    selected_conv = strmlt.radio(
        "Select a Conversation",
        options=["New Conversation"] + conversations_titles,
    )
    if selected_conv in conversations_titles:
        idx = conversations_titles.index(selected_conv)
        strmlt.session_state.active_conv_id = conversations_id[idx]
        strmlt.button(
            "Delete Selected Conversation",
            key=f"conv_del-{strmlt.session_state.active_conv_id}",
            on_click=delete_conversation,
            kwargs={
                "session": session,
                "conversation_id": strmlt.session_state.active_conv_id,
            },
        )


if strmlt.session_state.active_conv_id is not None:
    active_conv_id = strmlt.session_state.active_conv_id
    conv_messages = get_messages(session, active_conv_id)
    conv_title = f"Conversation-{random.randint(0,999)}"

msgs = StreamlitChatMessageHistory(key="history")

if previous_conv_id != strmlt.session_state.active_conv_id:
    msgs.clear()
    
    for msg in conv_messages:
        if msg.role.value == RoleEnum.HUMAN.value:
            msgs.add_user_message(msg.body)
        elif msg.role.value == RoleEnum.AI.value:
            msgs.add_ai_message(msg.body)    




chain_w_history = get_chain_w_history(msgs)

conversation = None
messages = None

if strmlt.session_state.active_conv_id is not None:
    conversation = get_conversation(session, strmlt.session_state.active_conv_id)
    messages = get_messages(session, conversation.id)

current_container_key = f"conv-{conversation.id}" if conversation is not None else None

with strmlt.container(key=current_container_key):
    if messages is not None:
        for message in messages:
            strmlt.chat_message(message.role.value).write(message.body)

if prompt_text := strmlt.chat_input("Type your message here..."):
    strmlt.chat_message("human").write(prompt_text)
    if conversation == None:
        new_conv_title = summerize_chat_content(prompt_text)
        conversation = create_conversation(session, new_conv_title.content)
        
        strmlt.session_state.active_conv_id = conversation.id
        strmlt.session_state.require_reset = True
        
    
    create_message(session, prompt_text, conversation.id, RoleEnum("human"))
    response_placeholder = strmlt.chat_message("ai").empty()
    full_response = ""
    with strmlt.spinner("Thinking..."):
        for chunk in chain_w_history.stream(
            {"input": prompt_text}, config={"configurable": {"session_id": f"conv-{conversation.id}"}}
        ):
            full_response += chunk.content
            response_placeholder.markdown(full_response)

    response_placeholder.markdown(full_response)
    create_message(session, full_response, conversation.id, RoleEnum("ai"))
    if strmlt.session_state.require_reset:
        strmlt.rerun()


