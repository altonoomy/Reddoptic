import filters_checks
from display_content import display_content
from credentials import reddit
import os
import sys
from colorama import Fore
from colorama import Style
from datetime import datetime
from itertools import islice


def user_subs(user, content_filter, *time_filter, **userargs):
	"""
	Searches user submissions

	time_filter[0] is all, hour, day, week, month, year
	time_filter[1] is time range
	"""
	user_submissions = [] #ALL user submissions
	user_submission_subs = [] #ALL subreddits where user submitted
	subreddit_occurence = {} #OCCURENCE of posts per subreddit

	if time_filter[0] == 'range':
		for submission in reddit.redditor(user).submissions.hot(limit=None):
			if filter_checks.in_time_range(submission, time_filter[1]):
				user_submission_subs.append(submission)

	#user top comment subreddits
	elif time_filter[0] == 'all':
		for submission in reddit.redditor(user).submissions.hot(limit=None):#changed limit from time_filter to None bc of error
			user_submission_subs.append(submission) #was submission.subreddit.display_name
	else:
		for submission in reddit.redditor(user).submissions.top(time_filter=time_filter[0]):#changed limit from time_filter to None bc of error
			user_submission_subs.append(submission)	

	#list of unique subreddits	
	#unique_submission_subs = set(user_submission_subs)
	unique_submission_subs = set(x.subreddit.display_name for x in user_submission_subs)
	sorted_submission_subs = sorted(unique_submission_subs)

	#extracts occurence of each subreddit display name from the list of the submission subreddits
	for sub in sorted_submission_subs:
		subreddit_occurence[sub] = [x.subreddit.display_name for x in user_submission_subs].count(sub)
	
	#for occurence of subreddits ie dictionary of subreddits listed by posts
	subreddit_occurence_sorted = dict(sorted(subreddit_occurence.items(), key=lambda item: item[1], reverse=True))

	user_submissions = filters_checks.filter_content(user, user_submission_subs, subreddit_occurence_sorted, content_filter, time_filter, subreddit=userargs.get('subreddit'), keyword= userargs.get('keyword'), content_type='comments')

	#PRINTS THE USER SUB'S INFO
	if user_submissions:
		if time_filter[0] != 'all':
				print(f"Showing comments from the past {time_filter[0]}.")
		else:
			print(f'Showing comments from {time_filter[0]} time.')	
		print("----------------------------------------------\n")
		count = 1
		for submission in user_submissions:
			print(f"{count}") #prints number in total found
			count += 1
			display_content(submission, count)
	else:
		print(f"{Fore.RED}Nothing here...{Style.RESET_ALL}\n")

def user_comments(user, content_filter, *time_filter, **userargs):
	"""
	time_filter[0] is all, hour, week, etc.
	time_filter[1] is time range
	"""
	comments = []
	user_comment_subs = [] 
	comment_occurence = {} #key pair values of subreddit and number of comments per sub
	keyword_occurence = [] #keeps count of keywords found 
	if time_filter[0] == 'range':
		for comment in reddit.redditor(user).comments.hot(limit=None):
			if filters_checks.in_time_range(comment, time_filter[1]):
				user_comment_subs.append(comment)
	
	#user top comment subreddits
	elif time_filter[0] == 'all':
		for comment in reddit.redditor(user).comments.hot(limit=None):#changed limit from time_filter to None bc of error
			user_comment_subs.append(comment)
	else:
		for comment in reddit.redditor(user).comments.top(time_filter=time_filter[0]):#changed limit from time_filter to None bc of error;also changing top to hot will BREAK it.
			user_comment_subs.append(comment)

	#list of unique subreddits	
	unique_comment_subs = set([x.subreddit.display_name for x in user_comment_subs])
	
	#list of unique subreddits in alphabetical order
	sorted_comment_subs = sorted(unique_comment_subs)

	#PRINTS SUBS AS THEY ARE FOUND (SLOWER OUTPUT i.e. verbose mode)
	#print("\nComment subreddit overview:")
	#print("-----------------------------")
	#for comment_sub in sorted_comment_subs:
	#	if check_nsfw(comment_sub):
	#		print(f'{comment_sub}*')
	#	else:
	#		print(comment_sub)

	for sub in sorted_comment_subs:
		comment_occurence[sub] = [x.subreddit.display_name for x in user_comment_subs].count(sub)
		
	#for comment occurence
	comment_occurence_sorted = dict(sorted(comment_occurence.items(), key=lambda item: item[1], reverse=True))

	comments = filters_checks.filter_content(user, user_comment_subs, comment_occurence_sorted, content_filter, time_filter, subreddit=userargs.get('subreddit'), keyword= userargs.get('keyword'), content_type='comments')
				
	#DISPLAYS COMMENTS PER SUBREDDIT
	if comments:
		if time_filter[0] != 'all':
				print(f"Showing comments from the past {time_filter[0]}.")
		else:
			print(f'Showing comments from {time_filter[0]} time.')	
		print("----------------------------------------------\n")
		count = 1
		for comment in comments:
			print(f"{count}") #prints number in total found
			count += 1
			display_content(comment, count)
	else:
		print(f"{Fore.RED}Nothing here...{Style.RESET_ALL}\n")

def user_info(user):
	name = reddit.redditor(user).name
	verified_email = reddit.redditor(user).has_verified_email
	mod = reddit.redditor(user).is_mod
	admin = reddit.redditor(user).is_employee
	friend = reddit.redditor(user).is_friend
	created_time = int(reddit.redditor(user).created_utc)
	karma_comment = reddit.redditor(user).comment_karma
	karma_link = reddit.redditor(user).link_karma
	karma_total = karma_comment + karma_link

	user_subreddit = reddit.redditor(user).subreddit
	
	border = ["=" for x in range(0,30)] #creates border that is equal to size of title plus spaces and vote length
	print("ACCOUNT INFO")
	print(''.join(border))
	print(f"Username: | {Fore.GREEN}{Style.BRIGHT}{name}{Style.RESET_ALL} |\n")
	try:
		print(f"{user_subreddit.public_description:<10}\n")
	except AttributeError:
		pass
	print(''.join(border))
	if admin and mod and friend:
		print(f"| {Fore.RED}Admin{Style.RESET_ALL} | {Fore.WHITE}Moderator{Style.RESET_ALL} | {Fore.YELLOW}Friend{Style.RESET_ALL} |")
	elif admin and mod:
		print(f"| {Fore.RED}Admin{Style.RESET_ALL} | {Fore.WHITE}Moderator{Style.RESET_ALL} |")
	elif admin:	
		print(f"| {Fore.RED}Admin{Style.RESET_ALL} |")
	elif mod:
		print(f"| {Fore.WHITE}Moderator{Style.RESET_ALL} |")
	try:
		if filters_checks.check_nsfw(user_subreddit.display_name):
			print(f"| {Fore.MAGENTA}NSFW{Style.RESET_ALL} |")
	except AttributeError:
		pass
	print(''.join(border))

	date_time_now = datetime.now()
	acc_creation_date_time =  datetime.fromtimestamp(created_time)
	duration = date_time_now - acc_creation_date_time
	duration_in_s = duration.total_seconds()

	years = divmod(duration_in_s, 31536000)
	months = divmod(years[1], 2629800)
	days = duration.days
	days = divmod(months[1], 86400)
	hours = divmod(days[1], 3600)
	minutes = divmod(hours[1], 60)

	print(f'| {acc_creation_date_time.strftime("%a, %b %d %Y, %H:%M:%S %Z")} |')
	print(f'| {int(years[0])} years, {int(months[0])} months, {int(days[0])} days,\n {int(hours[0])} hours, and {int(minutes[0])} minutes old. |')
	print(''.join(border))
	print(f'| Comment Karma    | {"{:,}".format(karma_comment):^7} |')
	print(f'| Submission Karma | {"{:,}".format(karma_link):^7} |')
	print(''.join(border))

	#DECIDING WHETHER OR NOT TO KEEP BELOW AS IT IS PRACTICALLY USELESS, HAVEN'T SEEN ANY SUB THAT ISN'T u_(users name)
	#if user_subreddit:
	#	if check_nsfw(user_subreddit.display_name):
	#		print(f"Subreddit name: {Fore.MAGENTA}{user_subreddit.display_name}{Style.RESET_ALL}")
	#	else:
	#		print(f"Subreddit name: {user_subreddit.display_name}")
	#	print(f"Subscriber count: {user_subreddit.subscribers}")
		#print(f"Is NSFW? {user_subreddit.over18}")
		#print(f"Banner link: {None}")
		#print(f"Description: {user_subreddit.public_description}\n")
	if admin or mod:
		print("\nModerator of:")
		print("-------------")
		for subreddit in reddit.redditor(user).moderated():
			if filters_checks.check_nsfw(subreddit.display_name):
				print(f"{Fore.MAGENTA}{subreddit.display_name}{Style.RESET_ALL}")
			else:
				print(subreddit.display_name)
	print('\n')
	print("Input option separated by a space: ")
	print("Press q to quit.")
	stats_menu = ["Top Comments", "Lowest Comments", "Top Posts", "Lowest Posts", "Trophy Case", ]
	for count, option in enumerate(stats_menu):
		print(f'|{count+1}| {option}')
	
	#ACCOUNT STATS
	while True:
		try:
			stats_choice = input()
			if len(stats_choice) == 1:
				if stats_choice.casefold() == 'q':
					break
			for option in stats_choice.split():
				if int(option) not in range(1, len(stats_menu)):
					print("Choice not in range. Try another option.")
					continue
			if stats_choice: 
				for option in stats_choice.split():
					if int(option)-1 == stats_menu.index('Top Comments'):
						print("Getting top comments!")
						get_top_comments(name)
					if int(option)-1 == stats_menu.index('Lowest Comments'):
						print("Getting lowest comments!")
						get_low_comments(name)
					if int(option)-1 == stats_menu.index('Top Posts'):
						print("Getting highest posts!")
						get_top_posts(name)
					if int(option)-1 == stats_menu.index('Lowest Posts'):
						print("Getting lowest posts!")
						get_low_posts(name)
					if int(option)-1 == stats_menu.index("Trophy Case"):
						print("Getting trophy case!")
						get_trophy_case(name)
			break
		except ValueError as e: 
			print(sys.exc_info()[2])
			print(e)

def get_trophy_case(user):
	print(f"{user}'s trophy case:")
	trophies = reddit.redditor(user).trophies()

	screen = os.get_terminal_size()
	border = ["=" for x in range(0,int(screen.columns))]

	print(f"Trophy name\t\t|Unlocked\t|Context")
	for trophy in reddit.redditor(user).trophies():
		print(''.join(border))
		trophy_name = trophy.name #name doesn't get colored if you use attribute
		sys.stdout.write(f"{Fore.YELLOW}{trophy_name:<23}{Style.RESET_ALL} |")

		if trophy.description != None:
			sys.stdout.write(f" {trophy.description:^12} |")
		context_link = "https://www.reddit.com" + str(trophy.url)

		if str(trophy.url)[:1] == '/':
			sys.stdout.write(f" {context_link:<5} ")
		elif trophy.url != None:
			print(f' {trophy.url}')
		#print(trophy.name, sep='    ', end='', flush=True)

		print('\n')
	print(''.join(border))


	"""
	old way of printing trophies, prints new line for each item
	for trophy in reddit.redditor(user).trophies():
		border = ["=" for x in range(0,(len(trophy.name)))]
		trophy_name = trophy.name #name doesn't get colored if you use attribute
		print(''.join(border))
		print(f'{Fore.YELLOW}{trophy_name}{Style.RESET_ALL}')
		if trophy.description != None:
			print(f'Unlocked: {trophy.description}')
		context_link = "https://www.reddit.com" + str(trophy.url)
		#if trophy.url != None:
		#	print(f'Context: {trophy.url}')
		if str(trophy.url)[:1] == '/':
			print(f'Context: {context_link}')
		elif trophy.url != None:
			print(f'Context: {trophy.url}')
	print(''.join(border))
	print('\n')
	"""

def get_top_posts(user):
	top_posts = {}
	for post in reddit.redditor(user).submissions.top(limit=None):
		top_posts[post] = post.score
	top_posts_sorted = dict(sorted(top_posts.items(), key=lambda item: item[1], reverse=True))

	for post in islice(top_posts_sorted.items(), 5):
		display_content(post[0])

def get_low_posts(user):
	low_posts = {}
	for post in reddit.redditor(user).submissions.controversial(limit=None):
		low_posts[post] = post.score
	low_posts_sorted = dict(sorted(low_posts.items(), key=lambda item: item[1], reverse=False))

	for post in islice(low_posts_sorted.items(), 5):
		display_content(post[0])

def get_top_comments(user):
	top_comments = {}
	for comment in reddit.redditor(user).comments.top(limit=None):
		top_comments[comment] = comment.score
	top_comments_sorted = dict(sorted(top_comments.items(), key=lambda item: item[1], reverse=True))

	#comment[0] --> comment ID
	#comment[1] == comment votes

	for comment in islice(top_comments_sorted.items(), 5):
		display_content(comment[0])

def get_low_comments(user):
	low_comments = {}
	for comment in reddit.redditor(user).comments.controversial(limit=None):
		low_comments[comment] = comment.score
	low_comments_sorted = dict(sorted(low_comments.items(), key=lambda item: item[1], reverse=False))

	for comment in islice(low_comments_sorted.items(), 5):
		display_content(comment[0])