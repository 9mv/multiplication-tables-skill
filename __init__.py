from mycroft import MycroftSkill, intent_file_handler


class MultiplicationTables(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tables.multiplication.intent')
    def handle_tables_multiplication(self, message):
        self.speak_dialog('tables.multiplication')


def create_skill():
    return MultiplicationTables()

