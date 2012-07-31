# -*- coding:utf-8 -*-
'''
Created on Apr 19, 2012

@author: cyg
'''
from nltk.corpus import stopwords as nltk_stop
import re
###############################################################################
PLACEHOLDER = u'!AAA'
stopwords = nltk_stop.words('portuguese')
stopwords = stopwords + [u'!aaa'
         , u'não'
         , u''
         , u"''"
         , u'('
         , u')'
         , u'-'
         , u'%'
         , u'&'
         , u','
         , u'$'
         , u'--'
         , u'.'
         , u':'
         , u';'
         , u'__len__'
         , u'de'
         , u'a'
         , u'o'
         , u'b'
         , u't'
         , u'c'
         , u'...'
         , u'``'
         , u'§'
         , u'é'
         , u're'
         , u'i'
         , u'ii'
         , u'iii'
         , u'iv'
         ]
###############################################################################
def clean_tokens(all_tokens): # correct tokenization errors and replace unwanted tokens with PLACEHOLDER
    for local_count in range(len(all_tokens)):
#    try:
        try: local_token = all_tokens[local_count]
        except: break
        if not local_token: break
        
        ### 
        if "º" in all_tokens[local_count]:
            all_tokens[local_count] = PLACEHOLDER
        ### 
        if "°" in all_tokens[local_count]:
            all_tokens[local_count] = PLACEHOLDER
        ### 
        if "6.É" in all_tokens[local_count]:
            all_tokens[local_count] = PLACEHOLDER
        ### 
        if "3.Daí" in all_tokens[local_count]:
            all_tokens[local_count] = PLACEHOLDER
        ### 
        m = re.match(r"(\w+)\.", all_tokens[local_count])
        if m:
#                print all_tokens[local_count]
            x = unicode(all_tokens[local_count][0:-1])
            all_tokens[local_count] = x
        ###
        p = re.match(r"(\d+)", all_tokens[local_count])
        if p: 
#                    print ' ',all_tokens[local_count], 
            all_tokens[local_count] = PLACEHOLDER
        ###
        n = re.match(r"(\d+)(\.)*", all_tokens[local_count])
        if n: 
#                    print ' ',all_tokens[local_count], 
            all_tokens[local_count] = PLACEHOLDER
        ###
        q = re.match(r"(\d+)/*", all_tokens[local_count])
        if q: 
#                    print ' ',all_tokens[local_count], 
            all_tokens[local_count] = PLACEHOLDER
        ###
        r = re.match(r"\-(\w+)*", all_tokens[local_count])
        if r: 
#                    print ' ',all_tokens[local_count], 
            all_tokens[local_count] = PLACEHOLDER
        ###
#    except: 
#        print 'ERROR AT TOKEN',all_tokens[local_count],' ...COUNT',local_count,'. CONTINUING.'
#        continue
    return all_tokens




