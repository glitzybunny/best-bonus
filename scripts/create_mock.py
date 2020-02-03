"""

?WHAT THE SCRIPT DOES???
The script creates mock(fake) data for testing/development purposes.


Mock data(fake data) - data for testing current app to see functionality during real work
A word 'mock' and 'fake' have the same meaning in the context of the scipt. 

Suplier - A bonus suplier. E.g. Online-casino, Betting company, CS:GO app, Poker room .......whatever
A word 'casino' and 'suplier' have the same meaning in the context of the scipt. 


FBA(Fake Bonus Amount) argument.
FCA(Fake Casino Amount) argument.



?POSSIBLE ARGUMENTS:
!It takes only integer digits as arugments
! Arguments are positional. So the order is important. 
e.g. 
python manage.py runscript create_mock --script-args 100 10
The line above takes as argument 10 and 100. 100 is FBA, and 10 is FCA

python manage.py runscript create_mock --script-args 10 100
The line above takes as argument 100 and 10. 10 is FBA, and 100 is FCA
! So you should be carefull with that


first argument -- FBA. Removes all mock Bonus data
second argument -- FCA. Removes all mock Suplier/Casino data


?HOW TO RUN THE SCRIPT:
python manage.py runscript create_mock --script-args 10 100
create_mock is the script
10 - is first argument. FBA
100 - is second argument. FCA


?Exmples of using the scipt for solving real-world issues: 
1) Creating 100 Mock Bonuses
python manage.py runscript create_mock --script-args 10
10 - is FBA(Fake Bonus Amount) argument

2) Creating 100 Mock Bonuses and 10 mock Casinos
python manage.py runscript create_mock --script-args 100 10
100 - is FBA(Fake Bonus Amount) argument
10 - is FCA(Fake Casino Amount) argument

"""
import sys
import datetime
from loremipsum import get_sentence
from random import randrange, randint, choice
from django.utils import timezone

from core import models


# showBonuses returns all existing bonuses from current DB
def showBonuses():
    # Fetch all bonuses and return them
    all_bonuses = models.Bonus.objects.all()

    return all_bonuses


# bonusMockData function creates mock Bonus records in DB
# fba(int) - Fake Bonus Amount. Amount of mock bonuses what will be created.
# 
# e.g. bonusMockData(100) --> Creates(and saves) 100 records of Bonus model.

#? You can recognise mock data by 'two_word_desc' field. If data is mock it always will contain "TESTING RECORD"
def bonusMockData(fba):

    # Creates bonus instance for fda(look above to know what FDA means) times
    for b in range(int(fba)):

        # Creates bonus filling it with random generated data in some fields 
        mock_object = models.Bonus.objects.create(two_word_desc=f'TESTING RECORD {b}',
        bonus_digit=randrange(4000), bonus_desc=get_sentence(5),
        suplier=models.Suplier.objects.get(pk=randint(1, models.Suplier.objects.count())),
        dep_bool=choice([True, False]), dep=randint(1, 10000), 
        doe=timezone.now() + datetime.timedelta(days=30),
        wager=randint(1,100), bonus_type=choice((0,1)),
        )
        
        print(mock_object)

    print(f"\n{fba} records for Bonus model are created successfully!!!")
    print('Check out your DB or go onto the app webpage to see results!!!\n')



# casinoMockData function creates mock Suplier/Casino records in DB
# fca(int) - Fake Casino Amount. Amount of mock caisnos what will be created.
# 
# e.g. casinoMockData(10) --> Creates(and save) 10 mock records of Suplier model.

#? You can recognise mock data by 'title' field. If data is mock it always will contain "TESTING RECORD"
# ! BELOW MUST BE THE SAME LOOP CODE FOR CREATING CASINO INSTANCE
# ! Finish the function
def casinoMockData(fca):

    # Creates casino instance for fca(look above to know what FCA means) times
    for c in range(int(fca)):
        pass



# !DO NOT TOUCH THE FUNCTION BELOW
# !This file must implement a run() function.
# ?This is what gets called when you run the script
def run(*args):
    print(args)
    try:
    # If we get 2 args it creates mock bonus data and mock casino data. 
    # The args are FBA, FCA. See above to know what it means.
        if len(args) == 2:
            bonusMockData(args[0])
            casinoMockData(args[1])

    # If we get one argument or whatever besides two aruguments.
    # It creates mock bonus data. The argument is FBA(see above what it means).
        elif len(args) == 1:
            bonusMockData(args[0])
        else:
            print("Wrong amount or order of arguments!!!!")
        print(showBonuses())
    
    except:
        print("SOMETHING GOT WRONG. EXCEPTION WAS RAISED")
        print("THE SCRIPT IS GETTING DOWN")
