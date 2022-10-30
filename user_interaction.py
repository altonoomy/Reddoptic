import get_content
import user_interaction
from credentials import reddit

import sys
import prawcore
from colorama import Fore
from colorama import Style  #for terminal colors
from datetime import datetime

def get_user():
	global user
	
	while True:
		user = str(input("Input a username: "))

		if len(user) < 3 or len(user) > 20:
			print("Username length not accepted.")
			continue
		
		try:
			if hasattr(reddit.redditor(user), 'fullname'):
				print(f'Searching {Fore.GREEN}{user}{Style.RESET_ALL}!')
				break
			elif hasattr(reddit.redditor(user), 'is_suspended'):
				print(f'User {Fore.GREEN}{user}{Style.RESET_ALL} is {Fore.RED}suspended{Style.RESET_ALL}!')
				continue
			else:
				print(f"User {Fore.GREEN} {user} {Style.RESET_ALL} does not {Fore.RED} exist {Style.RESET_ALL}!)")
		except prawcore.ResponseException as e:
			print(f"{Fore.GREEN}{user}{Style.RESET_ALL} {Fore.RED}does not exist!{Style.RESET_ALL}!")
			continue
		else:
			break
	return user


def menu():
	menu = ["Account info", "Account submissions", "Account comments", "All of the above"]

	print("What info would you like?")
	print("Press Q to quit.")
	
	#PRINT MENU
	for count, option in enumerate(menu):
		print(f'|{count+1}| {option}')
	
	while True:
		try:
			menu_option = input("Waiting for option...")
			if menu_option.casefold() == 'q':
				exit()
			elif int(menu_option) not in range(1, len(menu)+1):
				print("Option is out of range. Try again.")
				continue
		except ValueError:
			print("Sorry, that is an invalid option. Try again.")
			continue
		else:
			break
	#MAIN PROGRAM LOOP
	while True:
		try:
			if menu[int(menu_option)-1] == "Account info":
				pass
			else:
				filters_chosen = user_interaction.option_filters(menu_option)
				content_filter = filters_chosen[0] #top, controversial
				content_sort = filters_chosen[1] #all, hour, week, day, month, year
				time_range = filters_chosen[2] #user input can be range of mm/dd/yyyy with or w/o wildcards, or just range of a year
				print(f'Searching time range: {Fore.YELLOW}{str(time_range)}{Style.RESET_ALL}')


			if menu_option.casefold() == 'q':
				quit()
			elif int(menu_option) in range(1, len(menu)+1):
				if str(menu[int(menu_option)-1]) == "Account info":
					print(f"Gimme general account info as of {datetime.now()}.")
					get_content.user_info(user)
					quit()
				elif str(menu[int(menu_option)-1]) == "Account submissions":
					print(f"Gimme account submissions as of {datetime.now()}.")
					get_content.user_subs(user, content_filter, content_sort, time_range)
					while True:
						if user_interaction.continue_search(menu[int(menu_option)]) == True:
							get_content.user_subs(user, content_filter, content_sort, time_range)
						else:
							quit()
				elif str(menu[int(menu_option)-1]) == "Account comments":
					print(f"Gimme account comments as of {datetime.now()}.")
					get_content.user_comments(user, content_filter, content_sort, time_range)
					while True:
						if user_interaction.continue_search(menu[int(menu_option)]) == True:
							get_content.user_comments(user, content_filter, content_sort, time_range)
						else:
							quit()
				elif str(menu[int(menu_option)-1]) == "All of the above":
					print("Gimme it all!")
					get_content.user_info(user)
					get_content.user_subs(user, content_filter, content_sort, time_range)
					get_content.user_comments(user, content_filter, content_sort, time_range)
					quit()
				else:
					print("Come on! Pick something!")
					continue

		except (ValueError, AttributeError) as e : 
			#print(e)
			logger.error(e)
			raise
		else:
			break


def quit():
	quit_menu = ['y', 'n']
	while True:
		try:
			print(f"Keep searching {Fore.GREEN}{user}{Style.RESET_ALL}? (Y/N)")
			continue_option = input()
			if continue_option in quit_menu:
				if continue_option.casefold() == 'y':
					menu()
				elif continue_option.casefold() == 'n':
					pass
			else:
				print("What's so hard about yes or no???")
				continue
			quit_option = input("Would you like to perform another search? (Y/N)")
			if quit_option in quit_menu:
				if quit_option.casefold() ==  'y':
					main()
				elif quit_option.casefold() == 'n':
					print('Goodbye!')
					sys.exit()
			else:
				print("That's not yes or no! Try again.")
				continue
		except ValueError:
			print("Not a valid option. Try again.")
			continue
		else:
			break


def continue_search(content):
	while True:
		try:
			cont_submissions = input(f"Continue {content.casefold()} search? (Y/n) ")
			if cont_submissions:
				if cont_submissions.casefold() == 'y':
					return True
				elif cont_submissions.casefold() == 'n':
					return False
		except ValueError:
			print("Not a valid option. Try again.")
			continue
		else:
			break


def content_sort_choice(content):
	"""
	Asks user for a sorting option. 
	If option chosen is subreddit, user can input number(s), seperated by space, 
	corresponding to sub as printed by get_content, or input name directly. Returns list of chosen subs.
	If option chosen is keyword, user can input keywords seperated by a space. Returns list of keywords.
	If option chosen is Sleuth mode, more options will be given.
	"""
	sort_options = ['Subreddit', 'Keyword', 'Activity'] #copy this in filter_content function in filters_checks AS IS. if updated, update other lists as well
	sorted_subreddits = []
	print("\nSort by: ")
	print("-----------")
	for count, option in enumerate(sort_options):
		print(f'|{count}| {option}')

	while True:
		try:
			sort_choice = input("Choose a sorting option or press enter for no sorting: ")
			if sort_choice.casefold() == 'q':
				break
			elif int(sort_choice) in range(0, len(sort_options)):#
				if int(sort_choice) == sort_options.index('Subreddit'): #SUBREDDIT
					sort_subreddit_choice = input("Input the subreddit(s) name or number(s):")
					sort_subreddit_choice_list = sort_subreddit_choice.split(" ")
					print(sort_subreddit_choice_list)
					#CONVERTS NUMBER CHOSEN TO SUBREDDIT NAME
					for sub in sort_subreddit_choice_list:
						if sub.isnumeric():
							try:								
								num_to_sub = list(content.keys())[int(sub)]								
								sorted_subreddits.append(num_to_sub)															
							except IndexError:
								print(f"Sort option was out of range. Skipping {sub}.")
								continue
						else:
							sorted_subreddits.append(sub)
					return int(sort_choice), sorted_subreddits

				elif int(sort_choice) == sort_options.index('Keyword'): #KEYWORD
					sort_keyword_choice = input("Input keyword(s) separated by a space:")
					sort_keyword_choice = sort_keyword_choice.split(" ")
					return int(sort_choice), sort_keyword_choice

				elif sort_choice == 3: #activity
					None
			else:
				print('Not in range')
				continue
		except (ValueError, AttributeError) as e:
			print(f"errorr: {e}")
			print("Sorry, that is not a valid choice. Try again.")
			#sort_choice = input("Choose a sorting option: ")
			continue
		else:
			break


def option_filters(menu_option):
	if menu_option is not None:
		while True:
			try:
				filter_options = ["Top", "Controversial"]
				print("Choose filter (Default: Top): ")
				for count,option in enumerate(filter_options):
					print(f"|{count}| {option}")
				get_filter = input()

				if get_filter == "": #if Enter pressed, defaults to 0
					get_filter = 0 #default option is top
					break
				elif int(get_filter) not in range(0,2):
					print("Option is out of range. Try again.")
					continue
			except ValueError:
				print("Sorry, that is an invalid option. Try again.")
				continue
			else:
				break

		while True:
			try:
				time_filter_options = ["All", "Hour", "Day", "Week", "Month", "Year", "Specific range", "",] #added "" for auto option
				print("Choose a time filter (Default: All): ")
				for count,option in enumerate(time_filter_options[:-1]):
					print(f"|{count}| {option}")
				get_time_filter = input()
				if get_time_filter.isnumeric():
					if int(get_time_filter) not in range(0,(len(time_filter_options)-1)): #-1 bc included "" in list above
						print("Option is out of range. Try again.")
						continue
				elif get_time_filter.capitalize() not in time_filter_options:
					print("Not a valid filter. Try again.")
					continue
				else:
					break
			except ValueError:
				print("Sorry, that is an invalid option. Try again.")
				continue
			else:
				break
		#for default option
		if get_time_filter == "":
			time_filter = 'all'
			time_range_filter = None
		if get_time_filter.isnumeric(): 
			#time_filter = None
			print(time_filter_options[int(get_time_filter)])
			if time_filter_options[int(get_time_filter)] == 'Specific range':
				time_filter = 'range' #CHANGED FROM NONE
				time_range_filter = get_time_range()
			else:
				time_filter = str(time_filter_options[int(get_time_filter)]).casefold()
				time_range_filter = None
		elif get_time_filter.isalpha():
			time_filter = get_time_filter.casefold()

		return get_filter, time_filter, time_range_filter


def get_time_range():
	"""
	This function asks user for range in dd/mm/yyyy
	"""
	today = datetime.today()
	while True:
		try:
			time_range = input("Input range: (mm/dd/yyyy) separated by space. Wildcards allowed.")
			#splits time range into list with each list splitting range apart
			time_range_parts = [x.split("/") for x in str(time_range).split(" ")]

			#time_range_parts[0] gives first range, 
			#[1] gives second range; [0][n] gives day, month, year respectively.

			if len(time_range) not in range(4,21):
				print(f"{Fore.RED}Only one range allowed.{Style.RESET_ALL}")
				continue
			elif len(time_range_parts) > 2:
				print("Too many ranges.")
				continue
			if len(time_range) > 4: 
				for t in time_range_parts:
					if int(t[0]) > 12 or int(t[1]) > 31 or int(t[2]) > 2999:
						print(f'{Fore.RED}Impossible date input!{Style.RESET_ALL}')
				continue
			if len(time_range) == 4 and int(time_range) in range(2005, (int(datetime.now().year)+1)): #CASE: only single year given
				return time_range_parts
			else:
				print(f"Impossible range >:(")
				continue
		except ValueError as e: print(e)
		else:
			break
	return time_range_parts