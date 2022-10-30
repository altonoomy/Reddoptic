import filters_checks
import os
from datetime import datetime
from colorama import Fore #for terminal colors
from colorama import Style

def display_content(content, *count):
	try:
		text = f"{content.submission.title}"
	except AttributeError:
		text = f"{content.title}"
	target = "https://www.reddit.com" + str(content.permalink) #was comment.submission.url
	screen = os.get_terminal_size()
	border = ["=" for x in range(0,int(screen.columns))] #creates border equal to size of terminal width
	content_date = datetime.fromtimestamp(content.created_utc)

	if content:
		#border = ["=" for x in range(0,(len(text)+10))] #creates border that is equal to size of title plus spaces and vote length
		print(''.join(border))
		try:
			print(f"| {Fore.YELLOW}{content.score}({content.upvote_ratio * 100}%){Style.RESET_ALL} | {Style.BRIGHT}{Fore.RED}\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\{Style.RESET_ALL}|") #UPVOTES / POST TITLE
		except AttributeError:
			print(f"| {Fore.YELLOW}{content.score} {Style.RESET_ALL} | {Style.BRIGHT}{Fore.RED}\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\{Style.RESET_ALL}|")
		print(''.join(border))
		#print(f"| {datetime.utcfromtimestamp(content.created_utc)} ")
		print(f'| {datetime.fromtimestamp(content.created_utc).strftime("%a, %b %d %Y, %H:%M:%S %Z")} ')
		print(''.join(border))
		if filters_checks.check_nsfw(content.subreddit.display_name):
			print(f"| {Fore.MAGENTA}{content.subreddit.display_name}{Style.RESET_ALL}")
		else:
			print(f"| {content.subreddit.display_name}")
		print(''.join(border))
		print("\n") 
		try:
			content_body = content.body.split('\\n', 1)[0]
			print(f"{content_body}")
			print("\n")
		except AttributeError:
			if content.selftext:
				print(f"{content.selftext}")
				print("\n")

		print(''.join(border))
		print("\n")

def display_banner():
	banner_text = """
	                                                                                        	  ...'',,,,,,'...                            
                               .,:ccc:;,''..                                                           .';ldk0KXXNNNNXK0kdl;'.                        
                             .:kXNWWWNNXK0Oxoc:;,''....                                            ..;oOXNWWWWMMMMMMMMMMWWWNKkl;..                    
                            .cKWMMMMMMMMMMWWWWNNNXKOkxdl;;,'....                                 .;oOXWWMMMMMMMMMMMMMMMMMMMMMWWXOl,.                  
                            .dNMMMMMMMMMMMMMMMMMMMMWWWWWNNNX0Oxdl:;,,'....                     .,d0NMMMMMMMMMMMMMMMMMMMMMMMMMMMMWN0o,.                
                           .cOWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNXK0kxolc:;,''....         .lONMMMMMMMWNXK000OOOOO000KXNWMMMMMMWNOc.               
                           ;kXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNNX0Okxoc;;,'...,dXWMMMWNKOxdl:,'.........',cldkOKWMMMMWXd,.             
                          .cKMMMMMMMMMWX000XNWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNNX0kOKNMMWXOxl;'''.               .''':ox0XWMWNO:             
                          .oNMMMMMMMMMNx,.';lodxkO00KXNWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWMMWKxc,',:cool:;,.           'llc:,',cxKWMNd'            
                         .;kNMMMMMMMMWKc.       ...',:lodxOO0KXNNWMMMMMMMMMMMMMMMMMMMMMMMMMMMWKx:,;cxKNKd:dXWKc.           .oKNKxc,':xKN0o'           
                         'o0WMMMMMMMWKx,                  ...,:cloxkkO0KXNWWWMMMMMMMMMMMMMMWKxc;lkKNWWNO:.:kOx;             :ONWWNKxc;cx0O:           
                         :0WMMMMMMMMNO:.                            ..',:loddxkO00KXNWWMMWXOl;lOXWMMMW0o'  ...              'o0WMMMWXOl;ox:           
                        .lXMMMMMMMMMNd.                                       ...';:lodxkko:cxKWMMMMMW0o'                   'o0WMMMMMWKxo:.           
                        .dNMMMMMMMMMXl.                                                 ..;oxO00XNWMMWNk;                   ;kNWMMWNX00Oko'           
                       .:ONMMMMMMMMNO;                                                    :0K0kxkO00XNWXd'                 'dNWNXK0Okxk0KO:           
                       ,xXWMMMMMMMW0l'                                                    'o0NWNKOkxkkOOkd;.             .;dkOOOkxkOKNWN0l'           
                       c0WMMMMMMMMNx,                                                      'dNMMMWWNX0kxxkxl,.         .,lxkxdk0XNWWMMMNd.            
                      .lXMMMMMMMMMXl.                                                       :ONWMMMMMWWWNNXKOxollcccllodOKXXNWWWMMMMMWXk;             
                      'dNMMMMMMMMWKc                                                        .,xXMMMMMMMMMMMMWWWWWWWWWWWWWMMMMMMMMMMMWXd'              
                     'l0WMMMMMMMWXx,                                                          'o0WMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMW0o'               
                     ;kXWMMMMMMMWO:.                                                           .,dKWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKx;.                
                    .cXMMMMMMMMMNo.                                                              .,oOXNMMMMMMMMMMMMMMMMMMMMMMMNKOo,.                  
                    .oNMMMMMMMMMXl.                                                                 .:ok0XNWMMMMMMMMMMMMMMWX0ko;.                     
                   .;kNMMMMMMMMW0:                                                                     ..;ldkkO0KXNXK0OOkxo:'.                        
                   'o0WMMMMMMMWKd,                                                                           ..';ccc;'...                             
                   :0NMMMMMMMMNx;.                                                                                                                    
                  .lXMMMMMMMMMNo.                                                                                                                     
                  .dNMMMMMMMMMXl.                                                                                                                     
                 .l0WMMMMMMMWNO;                                                                                                                      
                 ;kXWMMMMMMMW0l.                                                                                                                      
                .cXMMMMMMMMMNd'                                                                                                                       
                .lXMMMMMMMMMXl.                                                                                                                       
                ,xNMMMMMMMMWKc                                                                                                                        
               'o0WMMMMMMMWXx,                                                                                                                        
               :ONMMMMMMMMNk:.                                                                                                                        
              .lXMMMMMMMMMNo.                                                                                                                         
              .oNMMMMMMMMWKc.                                                                                                                         
             .:ONMMMMMMMWNk;                                                                                                                          
             'o0WMMMMMMMW0o'                                                                                                                          
             :ONMMMMMMMMNx;.                                                                                                                          
            .lXMMMMMMMMMNo.                                                                                                                           
            ,xNMMMMMMMMWKc.                                                                                                                           
           .l0WMMMMMMMMN0:                                                                                               
							    _/_/_/                    _/        _/                        _/      _/            
							   _/    _/    _/_/      _/_/_/    _/_/_/    _/_/    _/_/_/    _/_/_/_/        _/_/_/   
							  _/_/_/    _/_/_/_/  _/    _/  _/    _/  _/    _/  _/    _/    _/      _/  _/          
							 _/    _/  _/        _/    _/  _/    _/  _/    _/  _/    _/    _/      _/  _/           
							_/    _/    _/_/_/    _/_/_/    _/_/_/    _/_/    _/_/_/        _/_/  _/    _/_/_/      
							                                                 _/                                     
							                                                _/                                      										                                                                                     
	"""
	print(banner_text)

def display_banner_small():
	banner_text = """

                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                     :!77~^^^.                                      :^7Y5GBBBBG5J7^:                
                   .5&@@@@@&&BPP5Y?7!^..                         :7P#@@@@@@@@@@@@@@BP7:             
                   ~&@@@@@@@@@@@@@@@@&&&BP5J77!~^:.            :Y#@@@@@@@@@@@@@@@@@@@@#Y:           
                  ^P@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#BGG5YJ!^^:..7#@@@@#GPY?77!!77?YPB#@@@@#7          
                  !@@@@@@@#YYG#&@@@@@@@@@@@@@@@@@@@@@@@@@@@&B#@@@P?!^!!.         !7^7JP@@@Y         
                 :Y@@@@@@@Y  ...:~!!Y5PGB#&&@@@@@@@@@@@@@@@@@@&Y!!YB&JJ@@!       :J&BJ!~5&&?.       
                 ?#@@@@@@P!             .:^^~!7J5GB#&&&@@@@@&J7Y#@@@P^:?7:        ^P@@@BJ7YB.       
                 P@@@@@@@?                          :^~!?JY5!JB@@@@@5:            :5@@@@@BY7        
                ~B@@@@@@#~                                 .GBP5GB#&@?.           ?@&#BG5PBG.       
               .P&@@@@@&?:                                  !B@@BGPP5PY~        ~YP5PPGB@@B!        
               :&@@@@@@&.                                    J#@@@@@&###PYJJJJY5###&&@@@@#?         
              :J&@@@@@&P.                                     ~G@@@@@@@@@@@@@@@@@@@@@@@@G~          
              ~#@@@@@@G~                                        7G@@@@@@@@@@@@@@@@@@@@G7            
              ?@@@@@@@5                                           ^?PB&@@@@@@@@@@&BP?^              
             ~P@@@@@@#?                                              .^~7?YPPY?7!^.                 
             Y@@@@@@@J:  ____          _     _             _   _      
            .P@@@@@@@!  |  _ \\ ___  __| | __| | ___  _ __ | |_(_) ___ 
           .J#@@@@@@P^  | |_) / _ \\/ _` |/ _` |/ _ \\| '_ \\| __| |/ __|
           .#@@@@@@&~   |  _ <  __/ (_| | (_| | (_) | |_) | |_| | (__ 
           ~&@@@@@@#.   |_| \\_\\___|\\__,_|\\__,_|\\___/| .__/ \\__|_|\\___|
          ^P@@@@@@#J                                |_|               
          !@@@@@@@P.    by AltoNoomy                                                                            
         :Y@@@@@@&Y                                                                                 
         7B@@@@@@P!                                                                                 
         5@@@@@@@?                                                                                  
        !B@@@@@@&!
     
	"""
	print(banner_text)