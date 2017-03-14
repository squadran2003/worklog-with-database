import datetime
import os
import time
from collections import OrderedDict

from models import *


def help_text():
	"""Application documentation"""

	clear_screen()
	print("*"*10)
	print("A GUIDE TO USING THE APP.\n"
		   "To add a new task enter n\n"
			"To view previous tasks type v\n"
			"To search for previously saved tasks type s\n\n"
			"VALIDATION\n"
			"Enter time spent in format %H:%M, 1 hr 30 mnts\n"
			"would be entered as 01:30\n\n"
			"Dates should be entered in the format dd/mm/yyyy\n\n"
			"AMENDS\n"
			"When editing a record, you can leave a field blank\n"
			"if you want it to retain its old values")

	
def type_of_search():
	"""this method asks the user for a 
	type of search"""
	
	display_message("Your search options")
	search_type = input("find by d[ate]\n"
			 			"find by e[mployee]\n"
			 			"find by s[earch term]\n"
			 			"find by date r[ange]\n"
						">> ".replace('\t','').lower())	
	if search_type not in "edsr" or not search_type:
		clear_screen()
		input("Did not recognise your search option! [press enter]")
		return type_of_search()
	else:
		return search_type
	
		
def display_message(msg):
	"""this method takes a message
	and prints it with a bit of styling
	around it"""
	
	clear_screen()
	print("*"*50)
	print(msg)
	print("*"*50)
	
	  
def get_notes(option='a'):
	"""this method asks the user
	to supply notes for the task,
	if the passed in parameter is a,
	the user is adding a new task else
	he is trying to edit a task, in which 
	case a return value of blank is acceptable"""
	
	notes = input("Any notes to enter for this task >> ")
	if not  notes and option != 'e':
		input("You have not entered any notes! [press enter]")
	else:
		return notes
    

def get_task_name(option='a'):
	"""asks the user for the task name,
	if the passed in parameter is a,
	the user is adding a new task else
	he is trying to edit a task, in which 
	case a return value of blank is acceptable"""
	
	task = input("Please enter the name of the task >> ")
	if not task and option != 'e':
		input("You have not entered a task! [press enter]")
		return get_task_name()
	else:
		return task
    

def get_task_time(option='a'):
	"""getting the time taken
	to complete a task, if the passed in parameter is a,
	the user is adding a new task else
	he is trying to edit a task, in which 
	case a return value of blank is acceptable"""
	
	task_time = input("How long did your task take? [H:M] >> ".strip().replace("\t",""))
	
	if not_valid_time(task_time) and option != 'e':
		input("You did not enter the date in\n"
				"the correct format!! [press enter] >> ")
		return get_task_time()
	else:
		return task_time
                

def get_date_options():
	"""returns a dict of dates 
	saved with a integer to represent
	the date"""

	dates = {}
	count = 0
	tasks = Entry.select()
	for task in tasks:
		date = task.Date
		# prevent duplicates being added to the dict
		if date in dates.values():
			pass
		else:
			count +=1
			dates[count] = task.Date

	return dates


def get_date_option_from_user(dates):
	"""this method will take a dict,
	print it out to the screen and get
	the user to choose an option, based
	on the option it returns the appropriate
	date"""

	for key,val in dates.items():
		print("{}: {}".format(str(key),val))
	result = input("Please select a date where 1 is the first date\n "
					"in the list >> ")

	if not result:
		input("Please select a date! [press enter] ")
		return get_date_option_from_user(dates)
	elif int(result) not in dates.keys():
		input("Please check your option, its not in the list [press enter]")
		return get_date_option_from_user(dates)
	else:
		#return the option the user has chosen
		for key,val in dates.items():
			if int(result) == key:
				return val
			else:
				pass


def get_date_range():
	"""this method gets a date range
	from the user"""

	dates = []
	date_1 = input("Enter first date in the range > ")
	date_2 = input("Enter second date in the range > ")
	if valid_date(date_1) and valid_date(date_2):
		date_1 = datetime.datetime.strptime(date_1,'%d/%m/%Y').date()
		date_2 = datetime.datetime.strptime(date_2,'%d/%m/%Y').date()
		dates.append(date_1)
		dates.append(date_2)
	else:
		input("Please check your date format [press enter]")
		return get_date_range()
	return dates


def valid_date(date):
	"""check to see if the date is in the correct format"""
	try:
		date = datetime.datetime.strptime(date, '%d/%m/%Y')
		return True
	except:
		return False


def not_valid_time(user_input):
	"""This method takes user_input
	and validates it against a time
	format"""
	
	try:
		user_input = datetime.datetime.strptime(user_input,'%H:%M')
	except:
		return True
	else:
		return False	


def clear_screen():
	os.system('cls' if os.name =='nt' else 'clear')


def create_task(employee, task_name, time_spent,
				notes):
	
	"""create a new task"""
	
	date = datetime.date.today().strftime('%Y-%m-%d')
	# write the task to the databases

	try:
		Entry.create(Date = date, employee = employee, task_name = task_name,
				time_spent = time_spent, notes = notes)
		print("Task created successfully!")
	except  Exception as e:
		print("Error writing task: {}".format(e))
	
	
def edit_task(task, employee, task_name, time_spent,
				notes):

	"""edit a task"""

	clear_screen()
	
	if not employee:
		employee = task.employee
	if not task_name:
		task_name = task.task_name
	if time_spent == '':
		time_spent = task.time_spent
	if notes =='':
		notes = task.notes

	try:
		task = Entry.update(employee = employee, task_name = task_name, 
							time_spent = time_spent,
							notes = notes).where(Entry.id == task.id)
		task.execute()
		print("Task updated")
	except Exception as e:
		print("Error updating task: {}".format(e))


def search_entries():
	"""Perform search on previously saved entries"""
	
	search = type_of_search()
	if search =='d':
		display_message("Here are your options to choose from")
		dates = get_date_options()
		date = get_date_option_from_user(dates)
		clear_screen()
		display_message("Here are your results!")
		view_tasks('d',date)
	elif search == 'e':
		employee = input("please enter a employee name >>  ")
		if not employee:
			input("You have not entered a employee name!")
			return search_entries()
		else:
			clear_screen()
			display_message("Here are your results!")
			view_tasks('e',employee)
	elif search == 's':
		text = input("Please enter a text to search by ")
		if not text:
			input("Please enter some text! [press enter]")
			return search_entries()
		else:
			clear_screen()
			display_message("Here are your results!")
			view_tasks('s',text)
	elif search =='r':
		date_range = get_date_range()
		clear_screen()
		display_message("Here are your results!")
		view_tasks('r',date_range)			

			
def delete_task(task):
	"""delete a task"""

	clear_screen()
	result = input("Are you sure you want to delete this task [Yn]").lower()
	if result =='y':
		task.delete_instance()
		print("Task deleted!")
	

def get_employee_name(option = 'a'):
	"""ask the user for their name,
	if e is passed as an argument, a blank
	input is allowed"""

	name = input("Your name is ? >> ").lower().strip()

	if not name and option != 'e':
		input("Please enter your name [press enter] ")
		return get_employee_name()
	else:
		return name


def view_tasks(search_type=None , search_val = None):
	"""view tasks"""

	clear_screen()
	tasks = None
	#search by date
	if search_type =='d' and search_val:
		tasks = Entry.select().where(Entry.Date == search_val)
	#searching by employee
	elif search_type =='e' and search_val:
		tasks = Entry.select().where(Entry.employee == search_val)
	#searching by text in the task name and notes
	elif search_type == 's' and search_val:
		tasks = Entry.select().where(
				(Entry.task_name.contains(search_val))|
				(Entry.notes.contains(search_val))
			)
	elif search_type == 'r' and search_val:
		tasks = Entry.select().where(
				(Entry.Date >= search_val[0])& (Entry.Date <= search_val[1])
			)
	else:
		tasks = Entry.select()

	display_tasks(tasks)
	
	
def display_tasks(tasks):
	""" this method takes tasks
	as a argument, validates and prints it out
	to the console"""

	# check for results
	if len(tasks) < 1:
		print("Sorry no results to display!")
	else:
		display_message("Here are your results")
		for entry in tasks:
			print("\n\n"+"="*50)
			print("ID,Date,Employee name,Task name,Time spent,Notes")
			print("{},{},{},"
				"{},{},{}".format(entry.id,entry.Date.strftime('%d/%m/%Y'), entry.employee,
								entry.task_name,entry.time_spent.strftime('%H:%M'),
								entry.notes))
			print("\n"+"="*50)
			# only show next where there are more than 1 record
			if len(tasks) > 1:
				print("n[ext] record")
			print("e[dit] record ")
			print("d[elete] record")
			print("q[uit]")

			choice = input("Action: ").lower().strip()
			if choice == 'q':
				break
			elif choice =='e':
				# if the user edits a record but does not supply any input
				# the old values are retained
				employee = get_employee_name('e')
				task_name = get_task_name('e')
				time_spent = get_task_time('e')
				notes = get_notes('e')
				edit_task(entry, employee, task_name,time_spent,
							notes)	
			elif choice =='d':
				delete_task(entry)


def intro_text():
	print("*"*50)
	print("Worklog. App that lets you record work related\n"
		"information, it allows you to view and search\n"
		"previously saved tasks")


menu = OrderedDict([
			('n',create_task), 
			('v',view_tasks),
			('s',search_entries),
			('h',help_text),
		]

	)


def main():
	user_input = None
	while user_input != 'q':
		print("\n\n"+"="*50)
		print("Press q to quit")
		if user_input != 'q':
			for key,value in menu.items():
				print("{}) {}".format(key,value.__doc__))
		
		user_input = input("Action:  ").lower().strip()
		if user_input in menu:
			if user_input =='n':
				clear_screen()
				display_message('Create new task!')
				employee = get_employee_name('e')
				task_name = get_task_name('e')
				time_spent = get_task_time('e')
				notes = get_notes('e')
				menu[user_input](employee,task_name,time_spent,
								notes)
			else:
				menu[user_input]()
			

if __name__ == '__main__':
	initialise()
	intro_text()
	main()