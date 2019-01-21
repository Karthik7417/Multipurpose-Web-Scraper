from urllib.request import urlopen
from pythonScripts.data import insert_validated_website
from pws import Bing


def process_validate_url(task_id, website_id, website_url, keywords):
    """
    This functions takes uses the website_url to validate if the link works, if not it uses the keywords to return most relevant url
    :param task_id:
    :param website_id:
    :param website_url:
    :param keywords:
    :return: None
    """
    try:
        urlopen(website_url)
        response = website_url
    except:
        print('Website not working - Trying Bing Search ')
        res = Bing.search(keywords, 5, 0)
        for r in res["results"]:
            response = r.get("link", None)
            if "facebook.com" not in response and "usnews.com" not in response and "google.com" not in response and ".gov/" not in response \
                    and "greatschools.org" not in response and "schooldigger.com" not in response and "areavibes.com" not in response and "mapquest.com" not in response \
                    and "wikipedia.org" not in response and "niche.com" not in response and "trulia.com" not in response and "zillow.com" not in response \
                    and "localschooldirectory.com" not in response and "schoolfamily.com" not in response and "redfin.com" not in response:
                break

    insert_validated_website(task_id=task_id, website_id=website_id, website_url=response)

    return None
