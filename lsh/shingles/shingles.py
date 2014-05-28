from lsh.utils import strings_utils

DEFAULT_SHINGLE_SIZE = 4

class ShingleType(object):
    W_SHINGLES = "w-shingles"
    K_SHINGLES = "k-shingles"

    @classmethod
    def is_valid(cls, type):
        if type == cls.W_SHINGLES or type == cls.K_SHINGLES:
            return True
        return False

def shingle_generator(doc_generator, size=DEFAULT_SHINGLE_SIZE, type=ShingleType.K_SHINGLES):
    """
        Generator a set of shingles from each given document returned by the document generator.
        :param doc_generator: generator that returns documents as strings
        :param size: size of w-shingles or k-shingles
        :param type: determines the type of shingles to create. (valid values => w-shingles or k-shingles)
        :return: generator that returns a set of shingles, k-shingles are represented as a set of strings, w-shingles are
        represented as a set of tuples
    """
    if not ShingleType.is_valid(type):
        raise ValueError('%s is not a valid shingle type. Valid types are "w-shingles or k-shingles. Please use ShinglesType.' % type)

    if type == ShingleType.K_SHINGLES:
        for s in _k_shingles_generator(doc_generator, size):
            yield s
    else:
        for s in _w_shingles_generator(doc_generator, size):
            yield s

def _w_shingles_generator(doc_generator, size=DEFAULT_SHINGLE_SIZE):
    """
        Generator that yields set of w-shingles
        :param doc_generator: generator that returns documents as strings
        :param size: size of w-shingles
        :return: yields set of shingles (set of tuples), yields None if it can't generate set of shingles
    """

    for doc in doc_generator:
        if doc:
            #step 1: tokenize string
            tokens = tuple(strings_utils.tokenize(doc))

            #step 2: remove punctuation, make string lower case
            tokens = tuple(map(strings_utils.normalize, tokens))

            #step 3: do stemming TODO - implement stemming funciton, for now just returns what was passed in
            tokens = tuple(map(strings_utils.get_stem, tokens))

            #step 4: create shingle tupule and add to list
            yield set(_get_list_of_shingles(tokens, size))
        else:
            yield None

def _k_shingles_generator(doc_generator, size=DEFAULT_SHINGLE_SIZE):
    """
        Generator that yields set of k-shingles
        :param doc_generator: generator that returns documents as strings
        :param size: size of k-shingles
        :return: yields set of shingles (set of strings), yields None if it can't generate set of shingles
    """

    for doc in doc_generator:
        if doc:
            #step 1: remove all white space from the string
            cleaned_doc = strings_utils.remove_all_whitespace(doc)

            #step 2: remove punctuation and make all lower case
            cleaned_doc = strings_utils.normalize(cleaned_doc)

            #step 3: get singles and add to set
            yield set(_get_list_of_shingles(cleaned_doc, size))
        else:
            yield None

def _get_list_of_shingles(doc, size=DEFAULT_SHINGLE_SIZE):
    """
        Creates a list of shingles (strings)
        :param doc: doc to create shingles from
        :type doc: string
        :param size: size of shingle
        :type size: int
        :return: list of shingles (strings), will return an empty list if doc is None or empty
    """

    if doc:
        return [doc[i:i + size] for i in range(len(doc) - size + 1)]
    else:
        return []

#TODO for dev testing only remove when done
# if __name__ == '__main__':
#
#     def test_generator_string():
#         yield "abcdefghijcklmnop."
#
#     def test_generator_string_words():
#         yield "do or do not there is no try!"
#
#     print "testing k-shingles"
#     for s in shingle_generator(test_generator_string()):
#         print s
#
#     print "testing w-shingles"
#     for s in shingle_generator(test_generator_string_words(), type=ShingleType.W_SHINGLES):
#         print s