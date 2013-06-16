#-*- coding:utf-8 -*-

import unittest
import yahoo
import conf

class TestYahoo(unittest.TestCase):
	def setUp(self):
		self.condition = yahoo.Condition(conf.APP_ID)

	def test_morph_ma(self):
		self.condition.set_sentence(u'明日')
		self.condition.set_results('ma')
		self.condition.set_response('surface,reading,pos,feature,baseform')

		ma = yahoo.MorphologicalAnalysis()
		result_set = ma.morph(self.condition)

		self.assertEqual(u'明日', result_set.ma_result.word_list[0].surface)
		self.assertEqual(u'あした', result_set.ma_result.word_list[0].reading)
		self.assertEqual(u'名詞', result_set.ma_result.word_list[0].pos)
		self.assertEqual(u'明日', result_set.ma_result.word_list[0].baseform)

	def test_morph_uniq(self):
		self.condition.set_sentence(u'明日')
		self.condition.set_results('uniq')
		self.condition.set_response('surface,reading,pos,feature,baseform')

		ma = yahoo.MorphologicalAnalysis()
		result_set = ma.morph(self.condition)

		self.assertEqual(u'明日', result_set.uniq_result.word_list[0].surface)
		self.assertEqual('', result_set.uniq_result.word_list[0].reading)
		self.assertEqual(u'名詞', result_set.uniq_result.word_list[0].pos)
		self.assertEqual(u'明日', result_set.uniq_result.word_list[0].baseform)

	def test_morph_both(self):
		self.condition.set_sentence(u'明日')
		self.condition.set_results('ma,uniq')
		self.condition.set_response('surface,reading,pos,feature,baseform')

		ma = yahoo.MorphologicalAnalysis()
		result_set = ma.morph(self.condition)

		self.assertEqual(u'明日', result_set.ma_result.word_list[0].surface)
		self.assertEqual(u'明日', result_set.uniq_result.word_list[0].surface)

	def test_morph_noexist_uniq_result(self):
		self.condition.set_sentence(u'明日')
		self.condition.set_results('ma')
		self.condition.set_response('surface,reading,pos,feature,baseform')

		ma = yahoo.MorphologicalAnalysis()
		result_set = ma.morph(self.condition)

		self.assertRaises(AttributeError, lambda: result_set.uniq_result.word_list[0])

	def test_morph_noexist_ma_result(self):
		self.condition.set_sentence(u'明日')
		self.condition.set_results('uniq')
		self.condition.set_response('surface,reading,pos,feature,baseform')

		ma = yahoo.MorphologicalAnalysis()
		result_set = ma.morph(self.condition)

		self.assertRaises(AttributeError, lambda: result_set.ma_result.word_list[0])


if __name__ == '__main__':
	unittest.main()