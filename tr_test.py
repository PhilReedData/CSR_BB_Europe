import codecs
import textrazor

fileInSmall = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/2009_20_GB0005758098_CR1.txt"
apiFile = "textrazor-apikey.txt"

def getPlainTextFromTXTPath(path):
    text = u''
    with codecs.open(path, 'r', encoding='utf8', errors='ignore') as fileIn:
        text = fileIn.read()
    return text

textrazor.api_key = getPlainTextFromTXTPath(apiFile)
client = textrazor.TextRazor(extractors=["topics"])
client.set_cleanup_mode("cleanHTML")
client.set_classifiers(["textrazor_newscodes"])

response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

print "------------------"
print "BBC article"
print "------------------"
print "Topics:"
for topic in response.topics():
    if topic.score > 0.9:
        print topic.label, topic.score
        
print ""
print "Categories:"
for category in response.categories():
    if category.score > 0.6:
        print category.label, category.score

        
print ""
print "------------------"
print "CSR report small"
print "------------------"
text = getPlainTextFromTXTPath(fileInSmall)
client.set_cleanup_mode("raw")
response = client.analyze(text)

print "Topics:"
for topic in response.topics():
    if topic.score > 0.9:
        print topic.label, topic.score
        
print ""
print "Categories:"
for category in response.categories():
    if category.score > 0.6:
        print category.label, category.score

        
