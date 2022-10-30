import get_content
import filters_checks
import display_content
import user_interaction

import argparse 
import logging
from colorama import init #for windows


logger = logging.getLogger(__name__)


def main():
	global user
	init() #filters ansi escape on windows, for colorama
	
	if get_arguments() == True:
		exit()
	else:
		display_content.display_banner_small()
		user = user_interaction.get_user()
		user_interaction.menu()

def get_arguments():
	parser = argparse.ArgumentParser()

	parser.add_argument("-u", "--user", metavar="username", help="Username of reddit user.", type=str)
	parser.add_argument("-f", '--filter', metavar="filter", help="Content filter: (0) top, (1) controversial, (2) hot, (3) new. (Default: Top)", default=0)
	parser.add_argument("-t", '--tfilter', metavar="time filter", help="Time filter: all, hour, day, week, month, year. (Default: All)", default='all')
	parser.add_argument("-r", '--range', metavar='range', help="Time range filter. Can be range in format mm/dd/yyyy mm/dd/yyyy or just yyyy. Wildcards allowed.")
	parser.add_argument("-I", "--info", help="Only show general user information.", action='store_true')
	parser.add_argument("-S", "--submissions", help="Only search submissions.", action='store_true')
	parser.add_argument("-C", "--comments", help="Only search comments.", action='store_true')
	parser.add_argument("-A", "--allinfo", help="Gives everything. Account information, submissions, and comments!", action='store_true')
	parser.add_argument("-k", "--keyword", metavar="word",  help="Keyword(s) used to search submissions/comments.", action='append', nargs='+')
	parser.add_argument("-s", "--subreddit", metavar="name", help="Subreddit(s) used to filter submissions/comments.", action='append', nargs='+')
	parser.add_argument("-n", "--nsfw", help="Only show NSFW comments/submissions.", action='store_true')

	args = parser.parse_args()
	
	while args.user is not None:
		try:
			if args.user:
				filters_checks.check_user(args.user)
			if not args.range: #if no range arguments present, will just search; else, sets tfilter to range set by user
				if args.info:
					print("Getting user information!")
					get_content.user_info(args.user)
				if args.comments:
					print(f"Getting comments!")
					get_content.user_comments(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
				if args.submissions:
					print(f"Getting submissions!")
					get_content.user_subs(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
				if args.allinfo:
					print("Getting user information!")
					get_content.user_info(args.user)
					print(f"\nGetting comments within range of {args.range}!\n")
					get_content.user_comments(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
					print(f"\nGetting submissions within range of {args.range}!\n")
					get_content.user_subs(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
			else:
				args.tfilter = 'range'
				if args.comments:
					print(f"Getting comments within range of {args.range}!")
					#subreddit = args.subreddit
					get_content.user_comments(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
				elif args.submissions:
					print(f'Getting submissions within range of {args.range}!')
					get_content.user_subs(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
				elif args.allinfo:
					print("Getting user information!")
					get_content.user_info(args.user)
					print(f"\nGetting comments within range of {args.range}!\n")
					get_content.user_comments(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)
					print(f"\nGetting submissions within range of {args.range}!\n")
					get_content.user_subs(args.user, args.filter, args.tfilter, args.range, subreddit=args.subreddit, keyword=args.keyword)


		except ValueError as e: 
			logger.error(error)
			raise
		else:
			return True


if __name__=="__main__":
	main()
