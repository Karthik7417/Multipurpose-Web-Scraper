MONGODB_HOST = 
MONGODB_PORT = 
MONGODB_DATABASE = 

AWS_ACCESS_KEY_ID = 
AWS_SECRET_ACCESS_KEY = 
REGION_NAME = 
DEBUG_QUEUE_URL = 

QUEUE_URL = 

EMAIL_PATTERN = r"[a-z0-9_.-]+@(?:[a-z0-9_-]+\.)+[a-z]+"
PHONE_PATTERN = r"(\+?\d?[\( -]{0,2}\d{3}[\) -]{0,2}\d{3}[ -]?\d{2}[ -]?\d{2}|\be?x?\.?\s?\d{4})"
SCHOOL_NAME_PATTERN = r"(?:(?:[A-Z][A-Za-z.-]+)%EDGE_PATTERN%\s)+(?:School|Elementary|Academy)"
SCHOOL_NAME_BLACKLIST = ["Middle School", "High School"]
SCHOOL_NAME_EDGE_WORDS = ["A", "About", "After", "Also", "An", "As", "Before", "Bus", "Email", "My", "No", "Our",
                          "Safe", "Sister", "Summer", "The", "Your", "Will"]
NOT_A_NAME_DICTIONARY_PATH = "pythonScripts/resources/not_a_name.dic"
STANFORD_LNG_MODEL_PATH = "pythonScripts/resources/stanford-ner-3.9.1/classifiers/english.all.3class.distsim.crf.ser.gz"
STANFORD_NER_PATH = "pythonScripts/resources/stanford-ner-3.9.1/stanford-ner.jar"
