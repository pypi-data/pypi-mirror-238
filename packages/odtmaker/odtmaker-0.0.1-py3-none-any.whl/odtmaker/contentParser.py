import re


class ContentParserException(Exception):
    pass


class _ContentParserInternalException(Exception):
    pass


class _TokenEndNotFound(_ContentParserInternalException):
    pass


class _InvalidTokenStart(_ContentParserInternalException):

    def __init__(self, start_got):
        super().__init__(self)

        self._start_got = start_got


class ContentParser(object):

    REGION_NAME_START = ['', ' ', '\n']
    REGION_NAME_END = ':'
    REGION_NAME_CONSECUTIVE_SEPARATOR = ','
    REGION_CONTENTS_START = ['{']
    REGION_CONTENTS_END = '}'
    REGION_CONTENTS_CONSECUTIVE_SEPARATOR = '|'
    # TODO Escape these characteres!

    def parse(self, raw_data):
        self._regions = {}

        # TODO Speed optimized, better with a generator
        self._raw_data = '\n'.join(raw_data)
        self._start = 0

        state = 'searching region name'

        while not self._finish():
            try:
                match state:
                    case 'searching region name':
                        region_names = self._searchRegionName()

                        state = 'searching contents end'

                    case 'searching contents end':
                        region_contents_list = self._searchRegionContents()

                        region_name_generator = region_names.split(ContentParser.REGION_NAME_CONSECUTIVE_SEPARATOR)
                        region_contents_generator = region_contents_list.split(ContentParser.REGION_CONTENTS_CONSECUTIVE_SEPARATOR)

                        for region_name, region_contents in zip(region_name_generator, region_contents_generator):
                            self._regions[region_name] = region_contents

                        state = 'searching region name'

            except _ContentParserInternalException as exception:
                raise self._externalize_exception(state, exception)

        return self._regions


    def _externalize_exception(self, state, exception):
        match state:
                case 'searching region name':
                    message = 'Region name end not found'

                case 'searching contents end':
                    message = f'Invalid content start (got "{exception._start_got}")'

        return ContentParserException(message)


    def _finish(self):
        return self._start >= len(self._raw_data)


    def _searchRegionName(self):
        return self._searchToken(ContentParser.REGION_NAME_START, ContentParser.REGION_NAME_END)


    def _searchRegionContents(self):
        return self._searchToken(ContentParser.REGION_CONTENTS_START, ContentParser.REGION_CONTENTS_END)


    def _searchToken(self, token_start_list, token_end):
        end = self._raw_data.find(token_end, self._start)

        if end == -1:
            raise _TokenEndNotFound()

        end += len(token_end)

        raw_token = self._raw_data[self._start:end]

        token_start, token_start_position = self._getLastTokenStart(raw_token, token_start_list)

        if token_start is None:
            raise _InvalidTokenStart(raw_token[:len(token_end)])

        self._start = end

        return raw_token[token_start_position + len(token_start):-len(token_end)]


    def _getLastTokenStart(self, raw_token, token_start_list):
        if '' in token_start_list:
            rightest_token_str, rightest_token_position = '', 0
        else:
            rightest_token_str, rightest_token_position = None, -1

        for index, token in enumerate(token_start_list):
            if token == '':
                continue

            if (token_position := raw_token.rfind(token)) != -1:
                if token_position > rightest_token_position:
                    rightest_token_str = token
                    rightest_token_position = token_position

        return rightest_token_str, rightest_token_position

