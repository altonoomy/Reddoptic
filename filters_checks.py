from credentials import reddit
import user_interaction
import re
import prawcore
from colorama import Fore #for terminal colors
from colorama import Style  #for terminal colors
from datetime import datetime

def check_user(user):
	try:
		if hasattr(reddit.redditor(user), 'fullname'):
			print(f"{Fore.GREEN}{user}{Style.RESET_ALL} exists!")
			print(f'Searching {Fore.GREEN}{user}{Style.RESET_ALL}!')
			return True
		elif hasattr(reddit.redditor(user), 'is_suspended'):
			print(f'User {Fore.GREEN}{user}{Style.RESET_ALL} is {Fore.RED}suspended{Style.RESET_ALL}!')
			return False
		else:
			print(f"User {Fore.GREEN} {user} {Style.RESET_ALL} does not {Fore.RED} exist {Style.RESET_ALL}!)")
	except prawcore.ResponseException as e:
		print(f"{Fore.GREEN}{user}{Style.RESET_ALL} {Fore.RED}does not exist!{Style.RESET_ALL}!")

def filter_content(user, content_subs, content_occurence_sorted, *filters, **userargs):
	keyword_occurence = []
	content = []
	sort_chosen = None
	sort_options = ['Subreddit', 'Keyword', 'Activity']
	content_type = (userargs.get('content_type'))

	try:
		subreddit = userargs.get('subreddit')[0]
		print(f'userargs subreddit: {subreddit}')
	except TypeError as e:
		subreddit = None
		
	try:
		keyword = userargs.get('keyword')[0]
		print(f"Keywords: {keyword}")
	except TypeError as e:
		keyword = None		

	print(f"\n #  | {content_type.capitalize()} subreddits:  | {content_type.capitalize()} #: ")	
	print("------------------------------------------")
	for count, sub in enumerate(content_occurence_sorted):#was sorted_comment_subs
		#print(f'({count:>3}) {sub:<25}| {user_comment_subs.count(sub):^5}|') #sorts by alphabetical order
		print(f'|{count:>3}| {sub:<25}| {content_occurence_sorted.get(sub):^5}|')
	# ISSUE BELOW: CHECKING FOR NSFW MAKES IT SO LIST COMES OUT ONE BY ONE INSTEAD OF ALL AT ONCE. TO MAKE IT ALL AT ONCE, DELETE NSFW CHECK

		#if check_nsfw(sub):
		#	print(f'|{count:>3}| {Fore.MAGENTA}{sub:<25}{Style.RESET_ALL}| {content_occurence_sorted.get(sub):^5}|')
		#else:
		#	print(f'|{count:>3}| {sub:<25}| {content_occurence_sorted.get(sub):^5}|')
	print(f'Total : {len(content_subs)}')
	
	#ARGUMENTS PROVIDED
	try:
		if keyword == None and subreddit == None:
			if bool(content_occurence_sorted) == True:
				sort_chosen = user_interaction.content_sort_choice(content_occurence_sorted)
		if keyword != None and subreddit != None:
			for subreddit in subreddit:
				print(f"Searching: {subreddit}")
				for contents in content_subs:
					if contents.subreddit.display_name.casefold() == subreddit.casefold():
						for word in keyword:
							if check_keyword(contents, keyword):
								content.append(contents)
								keyword_occurence.append(word)#keeps count of keywords found
		elif keyword != None:
			#for contents in reddit.redditor(user).comments.top(limit=None): #CHANGE TO CONTENT_SUBS?
			for contents in content_subs:
					for word in keyword:
						if check_keyword(contents, str(word)):
							content.append(contents)
							keyword_occurence.append(word)#keeps count of keywords found
		if subreddit != None:
			print(f"Subreddit(s): {subreddit}")
			for contents in content_subs:
				for sub in subreddit:
					if contents.subreddit.display_name.casefold() == sub.casefold():
						content.append(contents)
		for keyword in set(keyword_occurence):
					print(f'{keyword} found {keyword_occurence.count(keyword)} times.')
	except (TypeError, UnboundLocalError):
		pass

	
	# sort chosen[0] -->  int(sort_choice)
	# sort chosen[1] -->  sort_keyword_choice


	if sort_chosen is not None:
		print("\nACCOUNT COMMENTS")
		print("----------------\n")

		#SORTING OPTIONS WORK CODE
		if int(filters[0]) == 0:
			if sort_chosen[0] == sort_options.index('Subreddit'): #SUBREDDIT
				print(f"Searching following subreddits: {sort_chosen[1]}")
				for sub in sort_chosen[1]:
				#FIND SIMPLER WAY FOR CHANGING CONTENT RECEIVED FROM WHAT INPUT WAS GIVEN E.G. COMMENTS/SUBMISSIONS
					for content_post in content_subs:
						if content_post.subreddit.display_name.casefold() == sub.casefold(): #was sort_chosen[1].casefold():
								content.append(content_post)
			
			if sort_chosen[0] == sort_options.index('Keyword'): #KEYWORD
				
				print(f"Searching for the following keyword(s): {sort_chosen[1]}\n") #SORT CHOSEN CHANGED FROM 1 TO 0, had .split() 
				for comment in content_subs:
					for keyword in sort_chosen[1]: #was sort_chosen[1].split()
						if check_keyword(comment, keyword):
							content.append(comment)
							keyword_occurence.append(keyword)#keeps count of keywords found
				for keyword in set(keyword_occurence):
					print(f'{keyword} found {keyword_occurence.count(keyword)} times.')
			
			elif sort_chosen[0] == sort_options.index('Activity'): #ACTIVITY
				print('Under construction')
				
		elif int(filters[0]) == 1:
			for comment in reddit.redditor(user).comments.controversial(time_filter=str(time_filter)):
				content.append(comment)
	return content


def check_keyword(content, keyword):
	"""
	Searches for keyword in comments and submissions. 
	Checks submission self text as well as title.
	"""
	pattern = re.compile(fr'{keyword}.*', re.IGNORECASE)
	try:
		matches = re.findall(pattern, content.body) #searches through comment bodies
	except AttributeError:
		if content.is_self:
			matches = re.findall(pattern, content.selftext) #searches inside submission self text posts
			matches = re.findall(pattern, content.title) # searches title as well
		else:
			matches = re.findall(pattern, content.title)			
	if matches:
		print(f"Found match --> {keyword}")
		return True


def check_nsfw(subreddit):
	if reddit.subreddit(subreddit).over18:
		return True


def in_time_range(content, trange):
	"""
	Checks if content is within trange.
	Checks if input is just a year
	*Checks if input is a range e.g. dd/mm/yyyy dd/mm/yyy
	*Checks for wildcards

	*WIP
	"""
	comment_created_utc = content.created_utc
	datetime.fromtimestamp(comment_created_utc).year
	if len(trange) == 4:
		if int(trange)  == int(datetime.fromtimestamp(comment_created_utc).year):
			#print(f'{Fore.GREEN}match{Style.RESET_ALL}')
			return True
		else:
			return False