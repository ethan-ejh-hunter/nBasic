import unittest

import preprocessor

prep = preprocessor.Preprocessor


def runPreprocessorOn(lines):
    p = prep(readFileName=None, lines=lines)
    p.preprocess()
    return p


class MyTestCase(unittest.TestCase):
    def doesItRaise(self, exception, list):
        self.assertRaises(SyntaxError, prep(readFileName=None, lines=list).preprocess())

    def testLabels(self):
        list = ["label start", "12345", "abcds", "@start"]
        self.assertEqual(runPreprocessorOn(list).lines, ['12345', 'abcds', '@0'])

    def testVariables(self):
        list = ["var 1234"]
        self.assertRaises(SyntaxError, prep(readFileName=None, lines=list).preprocess())
        list = ['var abc', 'abc', '123']
        self.assertEqual(runPreprocessorOn(list).lines, ['0', '123'])


if __name__ == '__main__':
    unittest.main()
