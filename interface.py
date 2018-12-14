from my_plotly import *
from scraping import *
from countries_articles import *
import sys
import os

def update():
    os.remove('state_media_cache.sqlite')
    get_rt_data()
    get_cctv_data()
    get_dw_data()

def __main__():
    update()
    commands = '''
list countries:
result: lists the names of all of the countries that are currently in the database

plot country <country_name>:
results: displays all of the article bias data for a single country since data collection began.
valid inputs: The name of any country in the database.

plot today <country>:
results: displays all of the article bias data for a single country from data collected today.
valid inputs: The name of any country in the database.

plot all:
displays the article bias values for all time on a scatterplot.

plot today:
displays all of article bias values from each website today

help:
lists all available commands

update:
updates the database

exit:
exits the program
    '''
    user_error_msg = "I didn't understand that. Please type 'help' if you need help."
    country_name = ""
    country_lst = []
    for country in Country.objects:
        country_lst.append(country.name.lower())

    user_inp = input(('Welcome! Here are the commands: \n{}\n\nPlease enter a command: ').format(commands))
    while True:
        if len(user_inp.lower().split()) == 1:
            [command] = user_inp.lower().split()
            if command == 'help':
                print(commands)
            elif command == 'update':
                update()
                print("The update is complete.")
            elif command == 'exit':
                print("Goodbye!")
                sys.exit()
            else:
                print(user_error_msg)
        elif len(user_inp.lower().split()) == 2:
            [command, command_2] = user_inp.lower().split()
            if command == 'list' and command_2 == 'countries':
                print( "Here are the available countries: " + str(country_lst))
            elif command == 'plot':
                if command_2 == 'all':
                    plot_all()
                elif command_2 == 'today':
                    plot_day_all()
                elif command_2 in country_lst: # this isn't in the commands, but error handles as a prediction that the user wants to plot all from a country
                    plot_country_all(command_2)
                else:
                    print(user_error_msg)
            else:
                print(user_error_msg)
        elif len(user_inp.lower().split()) == 3:
            [command, command_2, param] = user_inp.lower().split()
            if command == 'plot' and command_2 == 'today' and param in country_lst:
                    plot_country_day(param)
            elif command == 'plot' and command_2 == 'country' and param in country_lst:
                    plot_country_all(param)
            else:
                print (param)
                print(user_error_msg)
        else:
            print(user_error_msg)
        user_inp = input('\nPlease enter a command: ')


if __name__ == '__main__':
    __main__()
