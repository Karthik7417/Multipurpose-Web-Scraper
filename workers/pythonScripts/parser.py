from pythonScripts.extractor.html import get_html_features, get_html_name_stats
from pythonScripts.extractor.email import get_emails
from pythonScripts.extractor.names import get_names
from pythonScripts.extractor.context import get_context
from pythonScripts.data import insert_parsed_page_complete, get_input_pages


def extract_all(task_id, page_id):
    html, page_id, website_id= get_input_pages(task_id, page_id)
    html_features = get_html_features(html)
    emails_data = get_emails(html_features["html_clean"])
    names_data = get_names(html_features["html_clean"])
    html_ner = get_html_name_stats(html_features["html_clean"], list(map(lambda x: x["name"], names_data["names"])))
    context = get_context(html_ner["html_ner"], html_ner["html_name_stats"], names_data["names"])

    # features = {"html_stats": html_features["html_stats"],
    #             "html_name_stats": html_ner["html_name_stats"],
    #             "html_clean": html_features["html_clean"],
    #             "page_text": html_features["page_text"],
    #             "html_ner": html_ner["html_ner"],
    #             "emails": emails_data["emails"],
    #             "user_names": emails_data["user_names"],
    #             "domains": emails_data["domains"],
    #             "names": names_data["names"],
    #             "resolved_names": context["resolved_names"],
    #             "resolved_context": context["resolved_context"],
    #             "resolution_score": context["resolution_score"]
    #             }
    for entity in context["resolved_context"]:
        #print(entity['name'])
        insert_parsed_page_complete(task_id=task_id, page_id=page_id, website_id=website_id, entity_name=str(entity['name']),
                                    entity_context=str(html_features["html_clean"]),parsing_tags={'role': entity['role'], 'email': entity['email'], 'phone': entity['phone']} )
    return None
