try:
    import requests
except ImportError:
    raise ImportError("The package 'requests' is not installed.")

try:
    from boilerpy3 import extractors, exceptions as bpe
except ImportError:
    raise ImportError("The package 'boilerpy3' is not installed.")

try:
    from nltk.tokenize import sent_tokenize
except ImportError:
    raise ImportError("The package 'nltk' is not installed. Once installed, install the 'punkt' tokenizer")

EXTRARGS = {
    0:'article',
    1:'lrgcontent',
    2:'canola',
    3:'everything',
    4:'numword',
    5:'article_sent',
    6:'everythingminwrd'
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

#Input: 
# 'url':        A valid privacy policy website url to extract from
# 'model':      Specifies which extraction model to use.  Defaults
#               to 'default'. Also accepts 'article', 'lrgcontent',
#               'canola' (recommended), 'everything', 'numword',
#               'article_sent', and 'everythingminwrd'
# 'tokenized':  Specifies if a string is returned, or a sentence
#               tokenized list using the 'punkt' dataset from nltk
# Output:
# str, list, or None if an error exists
def extractText(url, model='default',tokenized=False):

    # Selecting the extractor model
    extr = extractors.DefaultExtractor()
    if model == EXTRARGS[0]:
        extr = extractors.ArticleExtractor()
    elif model == EXTRARGS[1]:
        extr = extractors.LargestContentExtractor()
    elif model == EXTRARGS[2]:
        extr = extractors.CanolaExtractor()
    elif model == EXTRARGS[3]:
        extr = extractors.KeepEverythingExtractor()
    elif model == EXTRARGS[4]:
        extr = extractors.NumWordsRulesExtractor()
    elif model == EXTRARGS[5]:
        extr = extractors.ArticleSentencesExtractor()
    elif model == EXTRARGS[6]:
        extr = extractors.KeepEverythingWithMinKWordsFilter()


    #Attempt to retrieve the webpage
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.InvalidSchema:
        return None
    

    #Attempt to extract policy contents
    try:
        content = extr.get_content(response.text)
        content = content.replace('\n', ' ')
    except bpe.HTMLExtractionError:
        return None

    #Tokenize the extracted text if specified
    if tokenized:
        content = sent_tokenize(content)

    return content