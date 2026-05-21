from conversation.dialog_manager import dialog_manager

def handle_chat(user_input, user_context):
    return dialog_manager.process_message(user_input, user_context)
