#-*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup


class Condition(object):
    '''
    yahoo Morphologial analysis api condition.
    see http://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html
    '''

    def __init__(self, appid):
        '''
        Args:
            appid: yahoo api id
        '''
        self.sentence = ''
        self.results = ''
        self.response = ''
        self.filter = ''
        self.ma_response = ''
        self.ma_filter = ''
        self.uniq_response = ''
        self.uniq_filter = ''
        self.uniq_by_baseform = ''

        self.appid = appid

    def set_sentence(self, sentence):
        '''
        Args:
            sentence: string search word
        Returns:
            void
        '''
        self.sentence = sentence

    def set_results(self, results='ma'):
        '''
        Args:
            results: string
            ma,uniq
            Please separated by commas if you want to specify more than one.
        '''
        self.results = results

    def set_response(self, response):
        '''
        Args:
            response: string
            surface,reading,pos,baseform,feature.
            Please separated by commas(,) if you want to specify more than one.
            example:
            surface,reading
        '''
        self.response = response

    def set_filter(self, filter):
        '''
        Args:
            filter: string
            1-9.
            Please separeted by | if you want to specify more than one.
            example: 1
            |2|3

        '''
        self.filter = filter

    def set_ma_response(self, ma_response):
        self.ma_response = ma_response

    def set_ma_filter(self, ma_filter):
        self.ma_filter = ma_filter

    def set_uniq_response(self, uniq_response):
        self.uniq_response = uniq_response

    def set_uniq_filter(self, uniq_filter):
        self.uniq_filter = uniq_filter

    def set_uniq_by_baseform(self, uniq_by_baseform):
        self.uniq_by_baseform = uniq_by_baseform

    def to_parameter(self):
        '''
        Returns:
            (string) as url parameter
        Raise:
            ParameterAbsenceError
        '''
        if not self.appid or not self.sentence or not self.results:
            raise ParameterAbsenceError
            ('appid or sentence or result is not set')

        query = {
            'sentence': self.sentence.encode('utf-8'),
            'appid': self.appid,
            'results': self.results,
            'response': self.response,
            'filter': self.filter,
            'ma_response': self.ma_response,
            'ma_filter': self.ma_filter,
            'uniq_response': self.uniq_response,
            'uniq_filter': self.uniq_filter,
            'uniq_by_baseform': self.uniq_by_baseform
        }

        return urllib.urlencode(query)


class ParameterAbsenceError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MorphologicalAnalysis(object):

    def __init__(self):
        self.URL = 'http://jlp.yahooapis.jp/MAService/V1/parse?'

    def morph(self, condition):
        '''
        Args:
            condition: yahoo.Condition
        Returns:
            yahoo.ResultSet
        Raise:
            urllib2.HTTPError
        '''
        try:
            self.condition = condition
            url = self.URL + condition.to_parameter()
            response = urllib2.urlopen(url, 'POST')
        except:
            print(url)
            raise

        return self.parse_response(response.read())

    def parse_response(self, xml):
        soup = BeautifulSoup(xml)
        results = self.condition.results.split(',')
        resultSet = ResultSet()
        if 'ma' in results:
            resultSet.ma_result = self.parse_ma(soup)
        if 'uniq' in results:
            resultSet.uniq_result = self.parse_uniq(soup)

        return resultSet

    def parse_ma(self, soup):
        ma_result = soup.resultset.ma_result
        total_count = ma_result.total_count
        filtered_count = ma_result.filtered_count
        words = [
            Word(
                surface=word.surface.get_text()
                if word.find('surface') else '',
                reading=word.reading.get_text()
                if word.find('reading') else '',
                pos=word.pos.get_text() if word.find('pos') else '',
                baseform=word.baseform.get_text()
                if word.find('baseform') else '',
                feature=word.feature.get_text() if word.find('feature') else ''
            )
            for word in ma_result.word_list
        ]

        return Result(total_count, filtered_count, words)

    def parse_uniq(self, soup):
        uniq_result = soup.resultset.uniq_result
        total_count = uniq_result.total_count
        filtered_count = uniq_result.filtered_count
        words = [
            Word(
                count=int(word.count.get_text()),
                surface=word.surface.get_text()
                if word.find('surface') else '',
                reading=word.reading.get_text()
                if word.find('reading') else '',
                pos=word.pos.get_text() if word.find('pos') else '',
                baseform=word.baseform.get_text()
                if word.find('baseform') else '',
                feature=word.feature.get_text() if word.find('feature') else ''
            )
            for word in uniq_result.word_list
        ]

        return Result(total_count, filtered_count, words)


class ResultSet(object):
    def __init__(self):
        self.ma_result = ''
        self.uniq_result = ''


class Result(object):
    def __init__(self, total_count, filtered_count, word_list):
        self.total_count = total_count
        self.filtered_count = filtered_count
        self.word_list = word_list


class Word(object):
    def __init__(self, count=0, surface='',
                 reading='', pos='', baseform='', feature=''):
        self.count = count
        self.surface = surface
        self.reading = reading
        self.pos = pos
        self.baseform = baseform
        self.feature = feature
