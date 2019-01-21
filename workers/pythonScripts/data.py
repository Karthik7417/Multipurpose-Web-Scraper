from bson import ObjectId
from pymongo import MongoClient
from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


def get_input_pages(task_id, page_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        pages = conn[MONGODB_DATABASE]["{}_pages".format(task_id)].find_one(ObjectId(page_id))
    html = pages.get('html')
    page_id = str(pages.get('_id'))
    website_id = pages.get("website_id")
    return html, page_id, website_id


def insert_parsed_entities(task_id, documents):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        conn[MONGODB_DATABASE]["{}_entities".format(task_id)].insert(documents)


def insert_scraped_page(task_id, website_id, page_url, page_domain, page_title, html, content_tags):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        conn[MONGODB_DATABASE]["{}_pages".format(task_id)].insert_one({"website_id": ObjectId(str(website_id)),
                                                                       "page_url": page_url,
                                                                       "page_domain": page_domain,
                                                                       "page_title": page_title,
                                                                       "html": html,
                                                                       "content_tags": content_tags})


def insert_parsed_page_complete(task_id, page_id, website_id, entity_name, entity_context, parsing_tags):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:

        conn[MONGODB_DATABASE]["{}_entities".format(task_id)].insert_one({"page_id": ObjectId(str(page_id)),
                                                                          "website_id": ObjectId(str(website_id)),
                                                                          "entity_name": entity_name,
                                                                          "entity_context": entity_context,
                                                                          "parsing_tags": parsing_tags})


def insert_validated_website(task_id, website_id, website_url):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        conn[MONGODB_DATABASE]["{}_validated".format(task_id)].update_one(
            {"_id": ObjectId(website_id)}, {"$set": {"website_url": website_url}}, upsert=True)
