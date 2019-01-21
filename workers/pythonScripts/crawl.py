import tldextract
from pythonScripts.data import insert_scraped_page
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from pythonScripts.queue_jobs import crawl_website
import time


def crawl(task_id, website_id, website_url, depth):
    if (depth==-1):
        return None
    else:
        try:
            html = urlopen(website_url)
        except:
            html= "NA"
            print("Invalid website_url", website_url)
        start_time= time.time()
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all("a", href=re.compile("([A-Za-z0-9_:()])+"))
        page_domain = tldextract.extract(website_url).domain
        try:
            page_title = soup.title.string
        except:
            page_title = "NA"
        content_tags = set([tag.name for tag in soup.find_all()])
        insert_scraped_page(task_id=task_id, website_id=website_id, page_url=website_url, page_domain=page_domain,
                            page_title=page_title, html=str(soup), content_tags=str(content_tags))
        parts = website_url.split('//', 1)
        base_url = parts[0] + '//' + parts[1].split('/', 1)[0]
        end_time= time.time()
        print("Time taken for crawling : ", end_time-start_time)
        extensionsToCheck = (".epub", ".mobi", ".docx", ".doc", ".opf", ".7z", ".ibooks", ".cbr", ".avi", ".mkv", ".mp4", ".jpg", ".jpeg",
                             ".png", ".gif", ".pdf", ".iso", ".rar", ".tar", ".tgz", ".zip", ".dmg", ".exe")
        if(depth>0):
            print("For depth = ", depth, "and website url", website_url, "the total number of links generated=",
                  len(set(links)))
            for link in set(links):
                try:
                    if(urlopen(base_url + link['href'])):
                        if (base_url + link['href']).endswith(extensionsToCheck)==False:
                            if tldextract.extract(base_url + link['href']).domain in page_domain:
                                #valid_link.append(str(link['href']))
                                crawl_website(task_id= task_id, website_id= website_id, website_url= base_url + link['href'], crawl_depth= depth-1)
                                #print("The lamda function has the following website_url=", base_url + link['href'])
                except:
                    try:
                        if(urlopen(link['href'])):
                            if (link['href']).endswith(extensionsToCheck) == False:
                                if tldextract.extract(link['href']).domain in page_domain:
                                    #valid_link.append(str(link['href']))
                                    crawl_website(task_id= task_id, website_id= website_id, website_url= link['href'], crawl_depth= depth-1)
                                    #print("The lamda function has the following direct website_url=", link['href'])
                    except:
                        #print("Did not go to Lambda")
                        #invalid_link.append(str(base_url+link['href']))
                        continue
            print("Task Ends for website=", website_url)
    return None
