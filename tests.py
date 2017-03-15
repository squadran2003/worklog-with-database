import unittest
from unittest.mock import Mock
from test import support
from worklog import *
import models

class WorklogTests(unittest.TestCase):



	@classmethod
	def setUpClass(self):
		
		# running the setup method only once

		self.tasks = Entry.select()
		self.stdout = None
		self.stdin = None
		self.task_name = get_task_name('a')
		self.task_name_edit = get_task_name('e')
		self.employee_name = get_employee_name('a')
		self.employee_name_edit = get_employee_name('e')
		self.task_time = get_task_time('a')
		self.task_time_edit = get_task_time('e')
		self.notes = get_notes('a')
		self.notes_edit = get_notes('e')
		
		
	
	
	def test_display_tasks(self):
		"""test to see if it returns a particular
		string when there are no tasks to show"""

		
		#task is an empty list
		self.tasks = []
		with support.captured_stdout() as self.stdout:
			display_tasks(self.tasks)

		self.check_assertion('Sorry no results to display!\n')



	def test_view_entries(self):
		"""check that display_tasks is called with no issues
		when the default parameters are applied to view_tasks"""

		view_tasks = Mock()
		self.assertTrue(view_tasks.return_type(display_tasks([])))

	
	def test_type_of_search(self):
		"""check that the result type is
		one of the desired options"""
		
		result  =  type_of_search()
		self.assertIn(result, "edsrt")



	def test_get_task_name(self):
		"""check that return value is not blank,
		when a user is adding a task, but at the
		same time test that the return value can be blank
		or not in an edit context"""

		self.assertNotEqual(self.task_name, '')
		self.assertEqual(self.task_name_edit,'')


	def test_get_task_time(self):
		"""check that the return type is not blank when 
		a new task is getting created but can be blank 
		when in an edit context, also check that the return 
		type is the same function when the user enters blank"""

		self.assertNotEqual(self.task_time, '')
		self.assertEqual(self.task_time_edit,'')



	def test_get_notes(self):
		"""check that the return type is not blank when 
		a new task is getting created but can be blank 
		when in an edit context"""

		self.assertNotEqual(self.notes, '')
		self.assertEqual(self.notes_edit,'')


	def test_get_date_range(self):
		"""check that the list returned is not empty"""

		result = get_date_range()
		self.assertNotEqual(len(result), 0)
	
	
	def test_get_employee_name_edit(self):
		"""check that the return type is not blank when 
		a new task is getting created but can be blank 
		when in an edit context"""

		self.assertNotEqual(self.employee_name, '')
		self.assertEqual(self.employee_name_edit,'')


	def test_not_valid_time(self):
		"""check the function returns true
		when the time format is wrong"""

		user_input = not_valid_time('60:01')

		self.assertTrue(user_input)


	def test_valid_date(self):
		"""Check to see if false is returned when 
		the date is in the wrong format"""

		result = valid_date('2017-03-02')
		self.assertFalse(result)

	
	def test_get_date_options(self):
		"""check that the dictionary returned is not
		empty"""

		dict  = get_date_options()
		length = len(dict)

		self.assertNotEqual(length, 0)


	def test_create_task(self):
		"""test that a task gets created"""

		with support.captured_stdout() as self.stdout:
			create_task(self.employee_name,self.task_name,
						self.task_time, self.notes)
		self.check_assertion("Task created successfully!\n")



	def test_edit_task(self):
		"""test that a task gets updated"""

		task = Entry.get(id='7')
		with support.captured_stdout() as self.stdout:
			edit_task(task,self.employee_name_edit,self.task_name_edit,
						self.task_time_edit, self.notes_edit)
		self.check_assertion("Task updated\n")


	
	def test_delete_task(self):
		"""test to see if a task gets deleted successfully"""

		task = Entry.get(Entry.id=='6')
		delete_task(task)
		user_input = self.get_input()
		if user_input =='y':
			with support.captured_stdout() as self.stdout:
				delete_task(task)
			self.check_assertion("Task deleted!\n")

	
	def check_assertion(self, msg):

		self.assertEqual(self.stdout.getvalue(), msg)

	
	def test_main(self):
		print("enter q when prompted!")
		result  = main()
		self.assertEqual(result, None)


	def get_input(self):
		'''this method captures input from the console'''

		with support.captured_stdin() as self.stdin:
			return self.stdin.readline()

		
if __name__ == '__main__':
	print("*"*50)
	print("For each input request leave the second blank, for\n"
		"options, enter a value in the options")
	print("*"*50)
	unittest.main()


