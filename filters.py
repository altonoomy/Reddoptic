



def filter_content(content, content_subs, content_occurence_sorted, content_type, *filters, **userargs):
	keyword_occurence = []
	sort_chosen = None
	sort_options = ['Subreddit', 'Keyword', 'Activity']
	
	try:
		subreddit = userargs.get('subreddit')[0]
		print(f"Subreddits: {subreddit}")
	except TypeError as e:
		subreddit = None
		print(e) #REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE TEST PRINT
	try:
		keyword = userargs.get('keyword')[0]
		print(f"Keywords: {keyword}")
	except TypeError as e:
		keyword = None
		
	#print(f'sub: {subreddit}, kw: {keyword}')

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
	
	try:
		if keyword == None and subreddit == None:
			if bool(content_occurence_sorted) == True:
				sort_chosen = content_sort_choice(content_occurence_sorted)
		if keyword != None and subreddit != None:
			for subreddit in subreddit:
				print(f"Searching: {subreddit}")
				for contents in content_subs:
					if contents.subreddit.display_name.casefold() == subreddit.casefold():
						for word in keyword:
							if check_keyword(contents, keyword):
								content.append(contents)
								keyword_occurence.append(word)#keeps count of keywords found
				#for keyword in set(keyword_occurence):
				#	print(f'{keyword} found {keyword_occurence.count(keyword)} times.')
		elif keyword != None:
			for contents in content_subs:
					#if contents.subreddit.display_name.casefold() == subreddit.casefold():
					for word in keyword:
						if check_keyword(contents, keyword):
							content.append(contents)
							keyword_occurence.append(word)#keeps count of keywords found
				#for keyword in set(keyword_occurence):
				#	print(f'{keyword} found {keyword_occurence.count(keyword)} times.')
		elif subreddit != None:
			for subreddit in subreddit:
				if contents.subreddit.display_name.casefold() == subreddit.casefold():
					content.append(contents)
					keyword_occurence.append(word)#keeps count of keywords found
		for keyword in set(keyword_occurence):
					print(f'{keyword} found {keyword_occurence.count(keyword)} times.')
	except (TypeError, UnboundLocalError):
		pass

	#print(f'filters: {filters[0], filters[1]}')	#TEST PRINT REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE	
	

	if sort_chosen is not None:
		print("\nACCOUNT COMMENTS")
		print("----------------\n")

		#SORTING OPTIONS WORK CODE
		if int(filters[0]) == 0:
			if sort_chosen[0] == sort_options.index('Subreddit'): #SUBREDDIT
				print(sort_chosen[1])
				
				#FIND SIMPLER WAY FOR CHANGING CONTENT RECEIVED FROM WHAT INPUT WAS GIVEN E.G. COMMENTS/SUBMISSIONS
				if content_type == 'comments':
					#for comment in reddit.redditor(user).comments.top(limit=None):#all gives less results than None. limit was changed from timefilter. all comments are now shown.
					for comment in content_subs:
						if comment.subreddit.display_name.casefold() == sort_chosen[1].casefold():
							content.append(comment)
				elif content_type == 'submissions':
					for submission in reddit.redditor(user).submissions.top(limit=None):#all gives less results than None. limit was changed from timefilter. all comments are now shown.
						if submission.subreddit.display_name.casefold() == sort_chosen[1].casefold():
							content.append(submission)
			
			if sort_chosen[0] == sort_options.index('Keyword'): #KEYWORD
				print(sort_chosen[1])
				print(f"Searching for the following keyword(s): {sort_chosen[1].split()}\n") #SORT CHOSEN CHANGED FROM 1 TO 0
				print(filters[1][0])
				for comment in content_subs:
				#for comment in reddit.redditor(user).comments.hot(limit=None):#PROBLEM: DOESN'T SEARCH ANY COMMENTS if its time_filter, IF CHANGED TO LIMIT=NONE, WILL SEARCH COMMENTS BUT WON'T FILTER FOR TIME
					#print(comment.body)
					for keyword in sort_chosen[1].split():
						pattern = re.compile(fr'{keyword}.*', re.IGNORECASE)
						matches = re.findall(pattern, comment.body)
						#regex_keyword = re.search(f".*{keyword}.*", str(comment))
						if matches:
							print(f"Found match --> {keyword}")
							content.append(comment)
							keyword_occurence.append(keyword)#keeps count of keywords found
							match_count = 0
							match_count += 1
						#below is old method for finding matches, 	
						#for word in comment.body.split():
						#		if str(keyword).casefold() == word.casefold():
						#			print(f"Found match --> {keyword}")
						#			comments.append(comment)
						#			keyword_occurence.append(keyword)
						#			match_count = 0
						#			match_count += 1
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
	for word in keyword:
		pattern = re.compile(fr'{word}.*', re.IGNORECASE)
		try:
			matches = re.findall(pattern, content.body) #searches through comment bodies
		except AttributeError:
			if content.is_self:
				matches = re.findall(pattern, content.selftext) #searches inside submission self text posts
				matches = re.findall(pattern, content.title) # searches title as well
			else:
				matches = re.findall(pattern, content.title)
		if matches:
			print(f"Found match --> {word}")
			return True


def check_nsfw(subreddit):
	if reddit.subreddit(subreddit).over18:
		return True


def in_time_range(content, trange):
	"""
	Checks if content is within trange
	"""
	comment_created_utc = content.created_utc
	datetime.fromtimestamp(comment_created_utc).year
	if len(trange) == 4:
		if int(trange)  == int(datetime.fromtimestamp(comment_created_utc).year):
			#print(f'{Fore.GREEN}match{Style.RESET_ALL}')
			return True
		else:
			return False