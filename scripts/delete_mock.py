"""

?WHAT THE SCRIPT DOES???
The script deletes mock(fake) data what had been created for testing/development purposes.
!It will be extremely useful for deploying the project


Mock data(fake data) - data for testing current app to see functionality during real work
A word 'mock' and 'fake' have the same meaning in the context of the scipt. 

Suplier - A bonus suplier. E.g. Online-casino, Betting company, CS:GO app, Poker room .......whatever
A word 'casino' and 'suplier' have the same meaning in the context of the scipt. 


?POSSIBLE ARGUMENTS:
! The order of arguments is not important

all -- removes all mock data(casinos/supliers,bonuses). Default argument.
bonus -- removes mock Bonus data(all testing bonuses)
casino -- removes mock Suplier data(all testing casinos/supliers)

NO ARGS -- if you does enter any argument. The script executes with default 'all' argument.
           it will remove all mock data(casinos/supliers,bonuses).


?HOW TO RUN THE SCRIPT:
python manage.py runscript delete_mock
delete_mock is the script 


?Exmples of using the scipt for solving real-world issues: 

1) Deleting all mock data(casino, bonuses....)
python manage.py runscript delete_mock --script-args all
or
python manage.py runscript delete_mock --script-args


2) Deleting bonus mock data
python manage.py runscript delete_mock --script-args bonus


3) Deleting casino mock data
python manage.py runscript delete_mock --script-args casino

"""
from core import models



# Function removes all bonus mock data from DB
# Function fetches mock bonuses by two_word_desc(like a title) field 
#? If data is mock it will always contain "TESTING RECORD"   
def removeBonusMockData():
    #Fetch testing records
    testing_records = models.Bonus.objects.filter(two_word_desc__icontains='TESTING RECORD')
    print("Testing records have been found:")
    print(testing_records)

    # Deletes testing records
    print(testing_records.delete())
    print('BONUS testing records have been deleted successfully!!!\n')


# Function removes all casino/suplier mock data from DB
# Function fetches mock casino by title field 
#
#? If data is mock it will always contain "TESTING APP"
def removeCasinoMockData():
    #! You should also fetch and delete casino testing records here

    print('SUPLIER testing records have been deleted successfully!!!\n')
    pass


# !DO NOT TOUCH THE FUNCTION BELOW
# !This file must implement a run() function.
# ?This is what gets called when you run the script
def run(*args):
    print(args)

    # If no args or 'all' is recieved as argument - it deletes all mock data(casinos, bonuses)
    if  len(args) == 0 or 'all' in args:
        removeBonusMockData()
        removeCasinoMockData()

    # Checks if 'bonus' is recieved as argument - it deletes mock bonus records
    elif 'bonus' in args:
        removeBonusMockData()

    # Checks if 'casino' is recieved as argument - it deletes mock casino records
    elif 'casino' in args:
        removeCasinoMockData()