from unittest import TestCase, skip
from odtmaker.contentParser import ContentParser, ContentParserException


class ContentParserTests(TestCase):

    def test_simplest_region(self):
        regions = ContentParser().parse(['region_name:{region contents}'])

        self.assertIsNotNone(regions)
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions['region_name'], 'region contents')


    def test_should_ignore_garbage_between_regions(self):
        regions = ContentParser().parse(['subtitle1:{sub title 1 contents} ignored garbage subtitle2:{sub title 2 contents} more ignored garbage subtitle3:{sub title 3 contents}', ])

        self.assertEqual(len(regions), 3)
        self.assertEqual(regions['subtitle1'], 'sub title 1 contents')
        self.assertEqual(regions['subtitle2'], 'sub title 2 contents')
        self.assertEqual(regions['subtitle3'], 'sub title 3 contents')


    def test_multiple_line_region(self):
        regions = ContentParser().parse(['region_name:{region', 'contents}'])

        self.assertEqual(len(regions), 1)
        self.assertEqual(regions['region_name'], 'region\ncontents')


    def test_invalid_contents_start_should_raise_exception(self):
        with self.assertRaises(ContentParserException) as context:
            ContentParser().parse(['region_name:/region contents}'])

        self.assertEqual(str(context.exception), 'Invalid content start (got "/")')


    def test_region_name_not_closed_should_raise_exception(self):
        with self.assertRaises(ContentParserException) as context:
            ContentParser().parse(['region_name   {region contents}'])

        self.assertEqual(str(context.exception), 'Region name end not found')


    def test_consecutive_regions(self):
        regions = ContentParser().parse(['region1,region2,region3:{contents 1|contents 2|contents 3}'])

        self.assertEqual(len(regions), 3)
        self.assertEqual(regions['region1'], 'contents 1')
        self.assertEqual(regions['region2'], 'contents 2')
        self.assertEqual(regions['region3'], 'contents 3')

