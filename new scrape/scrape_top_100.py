import os
import requests
from bs4 import BeautifulSoup
import random
import csv
import time


#MAX urls from site:
#output on list websites_and_sizes
#format:
# [ name of site ] [ size of index ] [rest observed sizes]


MAX_URLS = 1000

def get_size_of_page(url):
  try:
    response = requests.get(url)

    if response.status_code == 200:
      content = response.content
      size_in_bytes = len(content)
      size_in_kb = size_in_bytes / 1024
    return (size_in_kb)
  except:
     print("" + url + "wrong! Didnt recieved code 200")
     return -1


def check_mother_url(url,mother_url):
  comparisons =  []
  comparisons.append("https://www." + mother_url)
  comparisons.append("http://www." + mother_url)
  comparisons.append("http://" + mother_url)
  comparisons.append("https://" + mother_url)


  comparison_with_trail_backslash = comparisons.copy()
  for item in comparisons:
    comparison_with_trail_backslash.append(item+"/")

  for item in comparison_with_trail_backslash:
    if url == item:
      return False

  return True


def get_random_urls_recursive_limit(url, mother_url, depth=3, num_urls=3, max_total_urls=MAX_URLS+5):

    total_urls_visited = 0
    valid_hrefs = []

    def recursive_helper(current_url, mother_url, current_depth):
        nonlocal total_urls_visited

        if total_urls_visited >= max_total_urls or current_depth > depth or current_url in visited_urls:
            return

        try:
            # Make a GET request to the current URL
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0"}
            response = requests.get(current_url, headers=headers)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Get the content of the current page
                html_content = response.text

                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find all the anchor tags (links) in the HTML
                all_links = soup.find_all('a')

                # Extract href attribute from each link
                hrefs = [link.get('href') for link in all_links if link.get('href') is not None]

                # Filter out empty and non-HTTP URLs
                hrefs = [href for href in hrefs if href.startswith('http')]


                #keep only  valid items:
                for item in hrefs:
                  if not (item in visited_urls):
                    if mother_url in item:
                      valid_hrefs.append(item)
                if len(valid_hrefs) == 0:
                  print(hrefs)
                  exit()
                # Select random URLs from the valid ones
                random_urls = random.sample(valid_hrefs, min(num_urls, len(valid_hrefs)))


                # Display the random URLs
                #print(f"Random URLs from {current_url} (Depth {current_depth}):")
                #for idx, random_url in enumerate(random_urls, start=1):
                #    print(f"{idx}. {random_url}")

  
               # Mark the current URL as visited  
                #is it the same as the mother url? for example without the www. as a prefix

                
                visited_urls.add(current_url)
               
                total_urls_visited += 1

                # Recursively call the function for each random URL
                for new_url in random_urls:
                    recursive_helper(new_url, mother_url, current_depth + 1)

            else:
                print(f"Failed to retrieve {current_url}. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # Start the recursive process with the initial URL
    recursive_helper(url, mother_url, 0)



input_file = "news100.csv"
print ("URLS per site = ", MAX_URLS)

websites = []

with open(input_file) as file:
  for item in file:
    websites.append(item.rstrip())

#wget index.php
#wget 

websites_and_sizes = []
counter = 0
for site in websites:


  counter+=1

  print("Running for ", counter, "/",len(websites)+1,": ", site)
  try:
    

    appended_new_row = []
    appended_new_row.append(site)
    sizes = []
    basic_url = "https://www." + site

    visited_urls = set()
    try:
      get_random_urls_recursive_limit(basic_url,site)
    except:
      basic_url = "https://" + site
      get_random_urls_recursive_limit(basic_url,site)

  #we will remove any instances of the mother url to add only one
  #for example we might have https://foo.org and https://www.foo.org
   

    url_list = []
    for item in visited_urls:
      if  check_mother_url(item,site):
        url_list.append(item)
    


    if len(url_list) > len(set(url_list)):
      print("Error, visited url's has two values that are the same!")
      exit()

    #make sure we have MAX_URLS element
    url_list = url_list[:MAX_URLS]
    #print(url_list)

    size_of_index =round(get_size_of_page(basic_url) / 5) * 5
    appended_new_row.append(size_of_index)
    

    for sub_url in url_list:
      #round number to the next multiplicate of 5
      size_of_url = round(get_size_of_page(sub_url) / 5) * 5

      sizes.append(size_of_url)
    if (all(v == 0 for v in sizes)):
      continue;
    appended_new_row.append(sizes)

    websites_and_sizes.append(appended_new_row)
  except:
    print("Cannot scrape site", site)
print(websites_and_sizes)

print("Sucessfully scraped ", len(websites_and_sizes), "sites")
with open('scraped_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  for i in range(len(websites_and_sizes)):
    writer.writerow(websites_and_sizes[i]) # Use writerow for single list

