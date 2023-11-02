
# <(\"[^\"]*\"|'[^']*'|[^'\">])*> [re for identify tags]
# <accession>(.*?)</accession> [select content written between accession tags]
import re, requests

class tagsHandler:

    def tag_name(self, tag_name, markup_string):
        return re.findall('<%s>(.*?)</%s>'%tag_name, markup_string)
# ref- https://www.ebi.ac.uk/proteins/api/doc/exampleScripts.html

tags = tagsHandler()

def ProtSeqence(geneName, top=100, offset=0):
    URL = "https://www.ebi.ac.uk/proteins/api/coordinates?offset=%s&size=%s&gene=%s"%(offset, top, geneName)
    r = requests.get(URL, headers={ "Accept" : "application/xml"})
    try:
        ass_seq = zip(tags.tag_name('accession', r.text), 
                      tags.tag_name('sequence', r.text))
        return dict(ass_seq)
    
    except ConnectionError:
        return "Https error server not responding"


def Get_SimilarProteinID(accession, len=100, offset=0, GEN_TYPE='xml'):
    URL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=%s&size=%s&accession=%s"%(offset, len, accession)
    r = requests.get(URL, headers={ "Accept" : "application/%s"%GEN_TYPE})
    response = r.text
    return tags.tag_name('accession', response)

####################################### END OF THE PROGRAM ###################################

# print(Get_SimilarProteinID('P21802'))
# print(ProtSeqence('FGFR2'))