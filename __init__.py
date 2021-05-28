from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
#from mycroft.util import LOG#, extract_number
from mycroft.util import LOG
from mycroft.util.parse import extract_number, extract_numbers
from mycroft.skills.context import adds_context, removes_context
#from lingua_franca.parse import extract_number
from random import randrange, choice
import time


class MultiplicationTables(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__()


    def getRandomInt(self):
        return randrange(1,11)


    def initialize(self):
        self.table = 0                  # multiplication table to practise. Initial value is 0. -1 = all tables. 1 to 10 are specific number tables.
        self.currentAnswer = 0          # Answer the user has to guess for the current operation.
        self.retries = 0                # Stores number of retries for current multiplication
        self.MAX_RETRIES = self.settings.get('max_retries', 3)  # number of maximum attempts to provide a wrong answer before counting it as failed.
        self.failed = 0                 # Count of failed multiplications
        self.numbers = {}               # Dictionary of values that will be used to multiply.
        self.playing = False            # Bool that indicates if the user is currently in-game.
        self.ordered = True             # Ordered by default.
        self.repeat = False             # True when Mycroft has to repeat the question.
        self.askAgain = True            # Variable to avoid asking the question of which table again when already repeated once.


    def validator(self, utterance):
        return True if extract_number(utterance) or self.voc_match(utterance, 'finish') else False


    def initializeTables(self):
        # all tables
        if self.table == -1:
            # create dictionary with key = each multiplication table to ask, which has a value = list of numbers to multiply by that table.
            for i in range(1,11):
                self.numbers[i]=list(range(1,11))
        else:
            self.numbers[self.table] = list(range(1,11))


    def nextNum(self):
        """
        Returns the first multiplication table figuring as a key in self.numbers (lowest number) with first number (lowest) on its list associated as value.
        """
        # if all tables
        if self.table == -1:
            if len(self.numbers) != 0:
                currentTable = list(self.numbers.keys())[0]
                number = self.numbers[currentTable].pop(0)
                if len(list(self.numbers.values())[0])==0:
                    del self.numbers[list(self.numbers.keys())[0]]
                return currentTable, number
        # if specific table
        else:
            if self.numbers[self.table] != []:
                return self.table, self.numbers[self.table].pop(0)
        return None


    def randomNum(self):
        """
        Returns an int representing a multiplication table (random key from self.numbers) and random int from the list of remaining numbers for that table.
        """
        # if all tables
        if self.table == -1:
            # if dictionary is empty
            if len(self.numbers) != 0:
                # currentTable is a random key from the ones inside numbers dictionary
                currentTable = choice(list(self.numbers.keys()))
                # delete a value from the list associated with currentTable key
                number = self.numbers[currentTable].pop(randrange(0,len(self.numbers[currentTable])))
                # delete empty entries
                for entry in list(self.numbers):
                    if self.numbers[entry] == []:
                        del self.numbers[entry]
                return currentTable, number
        # if specific table
        else:
            if self.numbers[self.table] != []:
                return self.table, self.numbers[self.table].pop(randrange(0,len(self.numbers[self.table])))
        return None


    def checkAnswer(self, answeredNumber): 
        # comparison between int from correct answer and int from answered number
        if (self.currentAnswer == int(answeredNumber)):
            return True     #Correct answer
        else:
            return False    #Wrong answer


    def analyseAnswer(self, answer):
        if answer is not None:
            # obtain answered number
            answeredNumber = extract_number(answer, lang = self.lang)
            # if its a number
            if answeredNumber:
                isCorrect = self.checkAnswer(answeredNumber)
                return isCorrect
        # if its not a number/no answer
        return False


    def endGame(self, forcedFinish=False):
        self.playing = False
        if (not forcedFinish):
            if self.retries == self.MAX_RETRIES:
                self.failed +=1
                self.speak_dialog('end.answer', {'answer':self.currentAnswer, 'failed':self.failed})
            else:
                if self.failed!=0:
                    self.speak_dialog('end.game.failures', {'failed':self.failed})
                else:
                    self.speak_dialog('end.game')
        else:
            self.speak_dialog('forced.finish')
        self.initialize()


    def askOperation(self):
        answer = 0
        while self.playing:
            # if there are no more numbers remaining to multiply
            if ((self.table != -1 and len(self.numbers[self.table])==0) and (not self.repeat)) or \
                ((self.table == -1 and len(self.numbers) == 0)  and (not self.repeat)):
                self.endGame()
            else:
                # if repeat is False, new numbers to ask are obtained.
                if not self.repeat:
                    if self.ordered:
                        n1, n2 = self.nextNum()
                    else:
                        n1, n2 = self.randomNum()

                    if self.retries == self.MAX_RETRIES:
                        self.failed +=1
                        answer = self.get_response('give.answer', {'answer':self.currentAnswer, 'n1': n1, 'n2': n2}, validator = self.validator, on_fail = 'repeat', num_retries=2)
                        
                    else:
                        answer = self.get_response('multiplication', {'n1': n1, 'n2': n2}, validator = self.validator, on_fail = 'repeat', num_retries=2)
                    self.retries = 0
                    self.currentAnswer = n1*n2

                # check if the user has spoken any finish keyword to end the game
                if self.voc_match(answer, 'finish'):
                    # for random multiplications we count an interrupted finish as a normal finish
                    self.endGame(False if self.table == -1 else True)
                    break

                if self.analyseAnswer(answer):
                    self.repeat = False
                else:
                    self.repeat = True

                    if answer is not None:
                        self.retries +=1
                        if self.retries == self.MAX_RETRIES:
                            # this way, on the next iteration, a new operation will be asked and the correct answer for this one will be given.
                            self.repeat = False
                        # we keep asking until MAX_RETRIES retries
                        else:
                            answer = self.get_response('wrong.answer',{'n1': n1, 'n2': n2}, validator = self.validator, on_fail = 'repeat', num_retries=2)
                    else:
                        self.endGame(True)


    def handle_utterance(self, message, response):
        numberCheck = message.data.get('numbers')
        anyCheck = message.data.get('any')
        disorderedCheck = message.data.get('disordered')
        allCheck = message.data.get('all') if response else None

        # check if more than a keyword was triggered
        checkCount = sum(1 for check in [numberCheck, anyCheck, allCheck] if check)

        if disorderedCheck:
            self.ordered = False

        if response:
            if message.data.get('ordered'):
                self.ordered = True

        # if no number is detected
        if numberCheck is None and anyCheck is None and allCheck is None:
            if (response and self.askAgain) or not response:
                self.set_context('InitTablesContext')
                if response:
                    self.askAgain = False
                    self.speak_dialog('which.table', expect_response=True)
                else:
                    self.speak_dialog('which', expect_response=True)
        # both any and specific are asked. if numberCheck is == 0 it might be an erroneous table of 1 detection.
        elif (checkCount == 2  and numberCheck != "1") or checkCount == 3:
            self.set_context('InitTablesContext')
            self.speak_dialog('which.table', expect_response=True)
        # skill detects only one of them
        else:
            # all tables
            if allCheck:
                self.table = -1
                self.speak_dialog('any.response')
                # all tables is disordered by default
                self.ordered = False
            # any table
            elif anyCheck:
                self.table = self.getRandomInt()
                self.speak_dialog('number.any.response', {'number': str(self.table)})
            # specific table
            else:
                self.table = extract_number(numberCheck, lang = self.lang)
                if (self.table not in range(1,11)):
                        self.set_context('InitTablesContext')
                        self.speak_dialog('which.table', expect_response=True)
                        self.table = 0
                else:
                    self.speak_dialog('number.response', {'number': str(self.table)})

            if self.table:
                time.sleep(5)
                self.playing = True
                self.initializeTables()
                self.askOperation()


    @intent_handler(IntentBuilder('InitTablesIntent').require('ask').require('tables').optionally('multiply').optionally('numbers').optionally('any').optionally('disordered'))
    def handle_multiplication_tables(self, message):
        """
        Initialize game. If user has not specified, Mycroft will ask which table.
        """
        LOG.info("PRIMER")
        self.handle_utterance(message, False)


    @intent_handler(IntentBuilder('WhichTableIntent').optionally('any').optionally('numbers').optionally('all').optionally('disordered').optionally('ordered').require('InitTablesContext').build())
    def handle_multiplication_tables_response(self, message):
        """
        User provides details about game.
        """
        LOG.info("SEGON")
        self.remove_context('InitTablesContext')
        self.handle_utterance(message, True)


    @intent_handler("ask.multiplications.intent")
    def handle_ask_multiplications(self, message):
        """
        Ask random multiplications recursively until 100 operations are asked or user cancels game.
        """
        LOG.info("TERCER")
        LOG.info(self.MAX_RETRIES)

        self.table = -1
        self.speak_dialog('any.response')
        time.sleep(5)
        self.playing = True
        # Disordered operations by default
        self.ordered = True if self.voc_match(message.data['utterance'], 'ordered') else False
        self.initializeTables()
        self.askOperation()


def create_skill():
    return MultiplicationTables()