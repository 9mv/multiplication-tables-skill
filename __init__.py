from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
#from mycroft.util import LOG#, extract_number
from mycroft.util import LOG
from mycroft.util.parse import extract_number, extract_numbers
from mycroft.skills.context import adds_context, removes_context
#from lingua_franca.parse import extract_number
from random import randrange, choice
import os

class MultiplicationTables(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__()


    def initialize(self):
        self.table = 0                  # multiplication table to practise. Initial value is 0. -1 = any table. 1 to 10 are specific number tables.
        self.currentAnswer = 0          # Answer the user has to guess for the current operation.
        self.retries = 0                # Stores number of retries for current multiplication
        self.numbers = {}               # Dictionary of values that will be used to multiply.
        self.playing = False            # Bool that indicates if the user is currently in-game.
        self.ordered = True             # Ordered by default.
        self.repeat = False             # True when Mycroft has to repeat the question.
        self.askAgain = True            # Variable to avoid asking the question of which table again when already repeated once.
        self.failed = 0                 # Count of failed multiplications


    def initializeTables(self):
        # any table
        if self.table == -1:
            # create dictionary with key = each multiplication table to ask, which has a value = list of numbers to multiply by that table.
            for i in range(1,11):
                self.numbers[i]=list(range(1,11))
        else:
            self.numbers[self.table] = list(range(1,11))


    def nextNum(self):
        if self.table == -1:
            if len(self.numbers) != 0:
                if len(list(self.numbers.values())[0])==0:
                    del self.numbers[list(self.numbers.keys())[0]]
                currentTable = list(self.numbers.keys())[0]
                return currentTable, self.numbers[currentTable].pop(0)
        else:
            if self.numbers[self.table] != []:
                return self.table, self.numbers[self.table].pop(0)
        return None


    def randomNum(self):
        """
        Returns a random int from the list of remaining numbers for that table.
        """
        # if any table
        if self.table == -1:
            # if dictionary is empty
            if len(self.numbers) != 0:
                # delete empty entries
                for entry in self.numbers:
                    if self.numbers[entry] == []:
                        self.numbers.pop(entry)
                # currentTable is a random key from the ones inside numbers dictionary
                currentTable = choice(list(self.numbers.keys()))
                # delete a value from the list associated with currentTable key
                return currentTable, self.numbers[currentTable].pop(randrange(0,len(self.numbers[currentTable])))
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
        self.remove_context('InGame')
        if (not forcedFinish):
            if self.retries == 3:
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
            if (self.table != -1 and len(self.numbers[self.table])==0) and (not self.repeat):
                self.endGame()                 
            elif(self.table == -1 and len(self.numbers) == 0)  and (not self.repeat):
                self.endGame()   
            else:
                # if repeat is False, new numbers to ask are obtained.
                if not self.repeat:
                    if self.ordered:
                        n1, n2 = self.nextNum()
                    else:
                        n1, n2 = self.randomNum()

                    if self.retries == 3:
                        self.failed +=1
                        answer = self.get_response('give.answer', {'answer':self.currentAnswer, 'n1': n1, 'n2': n2}, on_fail = 'repeat', num_retries=2)
                        
                    else:
                        answer = self.get_response('multiplication', {'n1': n1, 'n2': n2}, on_fail = 'repeat', num_retries=2)
                    self.retries = 0
                    self.currentAnswer = n1*n2

                if self.analyseAnswer(answer):
                    self.repeat = False
                    #self.speak_dialog('correct.answer')
                else:
                    self.repeat = True

                    if answer is not None:
                        self.retries +=1
                        if self.retries == 3:
                            # this way, on the next iteration, a new operation will be asked and the correct answer for this one will be given.
                            self.repeat = False
                        # we keep ansking until 3 retries
                        else:
                            answer = self.get_response('wrong.answer',{'n1': n1, 'n2': n2}, on_fail = 'repeat', num_retries=2)
                    else:
                        self.endGame(True)


    @intent_handler(IntentBuilder('InitTablesIntent').require('ask').require('tables').optionally('multiply').optionally('numbers').optionally('any').optionally('unordered'))
    def handle_multiplication_tables(self, message):
        numberCheck = message.data.get('numbers')
        anyCheck = message.data.get('any')
        unorderedCheck = message.data.get('unordered')

        if unorderedCheck:
            self.ordered = False
        
        # if skill does not detect any keyword
        if numberCheck is None and anyCheck is None:
            self.set_context('InitTablesContext')
            self.speak_dialog('which', expect_response=True)
            #Completar
        # if skill detects both any tables or specific tables keyword
        elif numberCheck is not None and anyCheck is not None:
            self.set_context('InitTablesContext')
            self.speak_dialog('which.table', expect_response=True)
        # skill detects only one of them
        else:
            # keyword of specific number
            if numberCheck is not None:
                self.table = extract_number(numberCheck, lang = self.lang)
                # if number can't be extracted
                if (self.table not in range(1,11)):
                    self.set_context('InitTablesContext')
                    self.speak_dialog('which.table', expect_response=True)
                else:
                    self.speak_dialog('number.response', {'number': str(self.table)})
            # keyword of any table
            else:
                self.table = -1
                self.speak_dialog('any.response')
            if self.table:
                self.playing = True
                self.set_context('InGame')
                self.initializeTables()
                self.askOperation()


    @intent_handler(IntentBuilder('WhichTableIntent').optionally('any').optionally('numbers').optionally('unordered').optionally('ordered').require('InitTablesContext').build())
    def handle_multiplication_tables_response(self, message):
        self.remove_context('InitTablesContext')
        numberCheck = message.data.get('numbers')
        unorderedCheck = message.data.get('unordered')
        orderedCheck = message.data.get('ordered')

        # check ordered
        if unorderedCheck:
            self.ordered = False
        # if both ordered and unordered are mentioned, ordered will have priority
        if orderedCheck:
            self.ordered = True

        # if no number is detected
        if numberCheck is None:
            # check if any table option is asked
            anyCheck = message.data.get('any')
            # any table
            if anyCheck is not None:
                self.set_context('InGame')
                self.table = -1
                self.initializeTables()
                self.speak_dialog('any.response')
                self.playing = True
                self.askOperation()
            # no specific table nor any table
            else:
                if self.askAgain:
                    self.askAgain = False
                    self.set_context('InitTablesContext')
                    self.speak_dialog('which.table', expect_response=True)
        # specific table detected
        else:
            self.table = extract_number(numberCheck, lang = self.lang)

            if (self.table not in range(1,11)):
                    self.set_context('InitTablesContext')
                    self.speak_dialog('which.table', expect_response=True)
            else:
                self.set_context('InGame')
                self.initializeTables()
                self.speak_dialog('number.response', {'number': str(self.table)})
                self.playing = True
                self.askOperation()     


def create_skill():
    return MultiplicationTables()