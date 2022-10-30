# Reddoptic
A reddit application that allows keyword searches, subreddit and time range filtering of user comments and submissions. 

# Setup
1. Create a [reddit personal use script application](https://www.reddit.com/prefs/apps/)
2. Edit auth.json and input account details from step 1.
3. Run 'pip install -r requirements.txt'

# Usage:
  `usage: reddoptic.py [-h] [-u username] [-f filter] [-t time filter] [-r range] [-I] [-S] [-C] [-A]
                      [-k word [word ...]] [-s name [name ...]] [-n]

  options:
    -h, --help            show this help message and exit
    -u username, --user username
                          Username of reddit user.
    -f filter, --filter filter
                          Content filter: (0) top, (1) controversial, (2) hot, (3) new. (Default: Top)
    -t time filter, --tfilter time filter
                          Time filter: all, hour, day, week, month, year. (Default: All)
    -r range, --range range
                          Time range filter. Can be range in format mm/dd/yyyy mm/dd/yyyy or just yyyy. Wildcards
                          allowed.
    -I, --info            Only show general user information.
    -S, --submissions     Only search submissions.
    -C, --comments        Only search comments.
    -A, --allinfo         Gives everything. Account information, submissions, and comments!
    -k word [word ...], --keyword word [word ...]
                          Keyword(s) used to search submissions/comments.
    -s name [name ...], --subreddit name [name ...]
                          Subreddit(s) used to filter submissions/comments.
    -n, --nsfw            Only show NSFW comments/submissions.`
