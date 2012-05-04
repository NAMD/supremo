# -*- coding:utf-8 -*-
'''
Created on Apr 19, 2012

@author: cyg
'''

from nltk.corpus import stopwords as nltk_stop
from BeautifulSoup import BeautifulSoup as bfs
import re


PLACEHOLDER = u'!AAA'
stopwords = nltk_stop.words('portuguese')
stopwords = stopwords + [u'!aaa'
, u'não'
, u'nÃo'
, u''
#, ''
, u'm'
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
, u'das'
, u'dos'
, u'ag'
, u'a'
, u'o'
, u'b'
, u't'
, u'c'
, u'desse'
, u'dessa'
, u'desta'
, u'desta'
, u'ai'
, u'...'
, u'``'
, u'§'
, u'é'
, u're'
, u'i'
, u'ii'
, u'iii'
, u'iv'
, u'n'
, u'lei'
, u'art'
, u'rel'
, u'min'
, u'rtj'
, u'relator'
, u'artigo'
, u'ministro'
, u'ministra'
, u'adalício'
, u'nogueira'
, u'adriano'
, u'josé'
, u'leal'
, u'adv'
, u'bento'
, u'de'
, u'faria'
, u'conselho'
, u'geminiano'
, u'da'
, u'franca'
, u'gonçalves'
, u'de'
, u'oliveira'
, u'luiz'
, u'gallotti'
, u'aldir'
, u'passarinho'
, u'ayres'
, u'britto'
, u'carlos'
, u'madeira'
, u'carlos'
, u'velloso'
, u'cármen'
, u'lúcia'
, u'célio'
, u'borja'
, u'celso'
, u'de'
, u'mello'
, u'cezar'
, u'peluso'
, u'cunha'
, u'peixoto'
, u'dias'
, u'toffoli'
, u'djaci'
, u'falcão'
, u'ellen'
, u'gracie'
, u'eros'
, u'grau'
, u'francisco'
, u'rezek'
, u'gilmar'
, u'mendes'
, u'ilmar'
, u'galvão'
, u'joaquim'
, u'barbosa'
, u'marco'
, u'aurélio'
, u'maurício'
, u'corrêa'
, u'menezes'
, u'direito'
, u'moreira'
, u'alves'
, u'nelson'
, u'jobim'
, u'néri'
, u'da'
, u'silveira'
, u'octavio'
, u'gallotti'
, u'oscar'
, u'corrêa'
, u'paulo'
, u'brossard'
, u'rafael'
, u'mayer'
, u'ricardo'
, u'lewandowski'
, u'sepúlveda'
, u'pertence'
, u'soares'
, u'muñoz'
, u'sydney'
, u'sanches'
, u'thompson'
, u'flores'
, u'presidente'
, u'nelson'
, u'hungria'
, u'ribeiro'
, u'da'
, u'costa'
, u'ubaldino'
, u'do'
, u'amaral'
, u'vice-presidente'
, u'vilas'
, u'boas'
, u'rel.'
, u'min.'
, u'publique-se'
, u'publique-se.'
]
bi_stopwords = [ 'supremo tribunal', 'tribunal federal']

def extract_ementa_n_decisao_from_html(html):
    clean_ementa_results = ''
    clean_decisao_results = ''

    decisao_texto = bfs(html.strip('[]'))#,  fromEncoding='ISO8859-1')
    strong_tags = decisao_texto.findAll('strong')
    for candidate_ementa_tag in strong_tags:
        clean_ementa = None
        if candidate_ementa_tag.text == 'Ementa':
            clean_ementa = candidate_ementa_tag.parent.contents[-1]
            if clean_ementa:
                clean_ementa_results = str(clean_ementa)
    pre_tags = decisao_texto.findAll('pre')
    for candidate_decisao_tag in pre_tags:
        clean_decisao = None
        if candidate_decisao_tag.previous.previous == 'Decisão':
            clean_decisao = candidate_decisao_tag.text
            if clean_decisao:
                clean_decisao_results = clean_decisao
        pass
    return (clean_ementa_results, clean_decisao_results)

def clean_tokens(all_tokens):
    '''Correct tokenization errors and replace unwanted tokens with
    PLACEHOLDER'''
    print '***', all_tokens
    unwanted_tokens = [u"º", u"°", u"6.É", u"3.Daí"]
    unwanted_regexps_str = [r"(\d+)", r"(\d+)(\.)*", r"(\d+)/*", r"\-(\w+)*"]
    unwanted_regexps = [re.compile(x) for x in unwanted_regexps_str]
    word_dot_regexp = re.compile(r"(\w+)\.")
    for index, local_token in enumerate(all_tokens):
        local_token = local_token.decode('utf-8')
        if not local_token:
            all_tokens[index] = PLACEHOLDER
            continue
        for unwanted_token in unwanted_tokens:
            if unwanted_token in local_token:
                all_tokens[index] = PLACEHOLDER
                continue
        if word_dot_regexp.match(local_token):
            x = unicode(local_token[0:-1])
            all_tokens[index] = x
        for unwanted_regexp in unwanted_regexps:
            if unwanted_regexp.match(local_token):
                all_tokens[index] = PLACEHOLDER
                continue
    return all_tokens


#if __name__ == '__main__':
#    x = [('a','b'),('a','c'),('a','d'),('a','e'),('a','f')]
#    r = x
#    print r
