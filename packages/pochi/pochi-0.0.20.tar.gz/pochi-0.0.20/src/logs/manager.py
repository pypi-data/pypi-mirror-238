from logs import messages


class LoggingManager(object):
    @staticmethod
    def __load_log_message(name):
        if hasattr(messages, name):
            return getattr(messages, name)
        else:
            return "Error: Message not found."

    @staticmethod
    def display_message(name, arguments=None):
        try:
            if arguments is None:
                message = LoggingManager.__load_log_message(name)
            if isinstance(arguments, list):
                message = LoggingManager.__load_log_message(name).format(*arguments)
            else:
                message = LoggingManager.__load_log_message(name).format(arguments)
            print(message)
        except Exception as e:
            print("Error: Not able to display messa: {}".format(name))

    @staticmethod
    def display_single_message(message):
        print(message)
