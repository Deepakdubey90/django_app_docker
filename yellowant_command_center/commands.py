"""Code which actually takes care of application API calls or other business logic"""
from yellowant.messageformat import MessageClass

from todo.sdk import TodoSDK
from yellowant_message_builder.messages import items_message, item_message


def create_item(args, user_integration, message=None):
    """YellowAnt command to create an item.

    Args:
        args (dict): Key-value pair of arguments passed from YellowAnt.
        user_integration (yellowant_api.models.UserIntegration): User integration data.
        message (MessageClass, optional): Message to add details to.

    Returns:
        MessageClass: Message containing details of a created item.
    """
    message = message or MessageClass()

    # verify arguments
    title = args.get("title")
    description = args.get("description")
    if title is None or not title:
        # inform the user that they have not provided valid arguments
        message.message_text = "You need to provide values for both `title` and `description` as arguments."
        return message

    new_item = TodoSDK(token=user_integration.user.id).create_item(
        title=title, description=description)

    # build return message for the user
    message.message_text = "You have created a new item:"
    message = item_message(new_item, user_integration, message)

    return message


def get_list(args, user_integration, message=None): #pylint: disable=unused-argument
    """YellowAnt command to get a list of todo items of a user.

    Args:
        args (dict): Key-value pair of arguments passed from YellowAnt.
        user_integration (yellowant_api.models.UserIntegration): User integration data.
        message (MessageClass, optional): Message to add details to.

    Returns:
        MessageClass: Message containing details of a user's todo list.
    """
    message = message or MessageClass()

    todo_list = TodoSDK(token=user_integration.user.id).get_list()

    # inform the user if the todo list is empty
    if not todo_list:
        message.message_text = "Your todo list is empty"
        return message

    # create message with the list of todos
    message.message_text = "Here are your todo items:"
    message = items_message(todo_list, user_integration, message)
    return message


def get_item(args, user_integration, message=None):
    """YellowAnt command to get an item.

    Args:
        args (dict): Key-value pair of arguments passed from YellowAnt.
        user_integration (yellowant_api.models.UserIntegration): User integration data.
        message (MessageClass, optional): Message to add details to.

    Returns:
        MessageClass: Message containing details of an item.
    """
    message = message or MessageClass()

    # verify args
    try:
        # since an item's id is supposed to be an integer, we will try casting the argument `id` to an int
        item_id = int(args.get("id"))
    except (TypeError, ValueError):
        # inform the user that they need to provide a valid integer id
        message.message_text = "You need to provide an integer value for the argument `id`."
        return message

    # inform the user if the item was not found by the id
    try:
        item = TodoSDK(token=user_integration.user.id).get_item(id=item_id)
        # create message for the found item
        message.message_text = "Here are the item details:"
        message = item_message(item, user_integration, message)
    except TodoSDK.DoesNotExist: #pylint: disable=no-member
        message.message_text = "Could not find todo item with the id: {}".format(
            item_id)

    return message


def update_item(args, user_integration, message=None):
    """YellowAnt command to update an item.

    Args:
        args (dict): Key-value pair of arguments passed from YellowAnt.
        user_integration (yellowant_api.models.UserIntegration): User integration data.
        message (MessageClass, optional): Message to add details to.

    Returns:
        MessageClass: Message containing details of a updated item.
    """
    message = message or MessageClass()

    # verify args
    title = args.get("title")
    description = args.get("description")
    try:
        # since an item's id is supposed to be an integer, we will try casting the argument `id` to an int
        item_id = int(args.get("id"))
    except (TypeError, ValueError):
        # inform the user that they need to provide a valid integer id
        message.message_text = "You need to provide an integer value for the argument `id`."
        return message

    try:
        updated_item = TodoSDK(token=user_integration.user.id).update_item(
            id=item_id, title=title, description=description)
        # create message with the updated item
        message.message_text = "Here are the updated item details:"
        message = item_message(updated_item, user_integration, message)
    except TodoSDK.DoesNotExist: #pylint: disable=no-member
        message.message_text = "Could not find todo item with the id: {}".format(
            item_id)

    return message


def delete_item(args, user_integration, message=None):
    """YellowAnt command to delete an item.

    Args:
        args (dict): Key-value pair of arguments passed from YellowAnt.
        user_integration (yellowant_api.models.UserIntegration): User integration data.
        message (MessageClass, optional): Message to add details to.

    Returns:
        MessageClass: Message containing details of the remaining list of todo items.
    """
    message = message or MessageClass()

    # verify args
    try:
        # since an item's id is supposed to be an integer, we will try casting the argument `id` to an int
        item_id = int(args.get("id"))
    except (TypeError, ValueError):
        # inform the user that they need to provide a valid integer id
        message.message_text = "You need to provide an integer value for the argument `id`."
        return message

    try:
        todo_list = TodoSDK(
            token=user_integration.user.id).delete_item(id=item_id)
        # create message with the list of todos
        if not todo_list:
            message.message_text = "Your todo list is empty."
        else:
            message.message_text = "Here are your todo items:"
            message = items_message(todo_list, user_integration, message)
        return message
    except TodoSDK.DoesNotExist: #pylint: disable=no-member
        message.message_text = "Could not find todo item with the id: {}".format(
            item_id)

    return message
