"""
Tools to play with Ceasar cyphers (https://en.wikipedia.org/wiki/Caesar_cipher).

    >>> from codify import ceasar_cypher
    >>> ceasar_cypher("Hi, I'm Bob!")
    "ij, j'n cpc!"

Note that every letter is lower-cased now. This is because ``ceasar_cypher`` preprocesses all phrases with
``str.lower`` by default. You can stop this by specifying ``preprocess=None``, but note that, then, upper case
letters won't be transformed (since they're not mapped by the default ``letter_transformer``).

    >>> ceasar_cypher("Hi, I'm Bob!", preprocess=None)
    "Hj, I'n Bpc!"

The key to the cypher is ``letter_transformer`` which defines the letter mapping.
The most general way to specify this is through a function, but most of the time you specify it through a mapping:
an explicit ``{transform_this: into_this, and_this: into_that, ...}`` ``dict``.

If you don't specify any ``letter_transformer``, as above, the default is taken to be a cylclic mapping over the
whole alphabet with an ``offset=1``.

You can change that offset to another number:

    >>> ceasar_cypher("Hi, I'm Bob!", letter_transformer=4)
    "lm, m'q fsf!"
    >>> ceasar_cypher("Hi, I'm Bob!", letter_transformer=-3)
    "ef, f'j yly!"

Here's an example of specifying ``letter_transformer`` as an explicit ``dict``:

    >>> ceasar_cypher("Hi, I'm Bob!", letter_transformer={'b': 'd', 'i': 'o'})
    "ho, o'm dod!"

You also have tools that will create such mappings for you, based on jumping by a fixed ``offset`` in one
(``mk_letter_map_from_offset``) or several (``multiple_cycles_letter_transformer``) letter cycles.
Below is an example using ``offset=1`` on vowels and consonants separately.

    >>> from codify import vowel_separated_letter_transformer
    >>> vowel_separated_letter_trans = vowel_separated_letter_transformer(offset=1)
    >>> list(vowel_separated_letter_trans.items())[:9]
    [('a', 'e'), ('e', 'i'), ('i', 'o'), ('o', 'u'), ('u', 'a'), ('b', 'c'), ('c', 'd'), ('d', 'f'), ('f', 'g')]

This makes cyphers more readable:

    >>> ceasar_cypher("Hi, I'm Bob!".lower(), letter_transformer=vowel_separated_letter_trans)
    "jo, o'n cuc!"
    >>> ceasar_cypher("jo, o'n cuc!", letter_transformer=invert_mapping(vowel_separated_letter_trans))
    "hi, i'm bob!"

"""
from typing import Union, Dict, Callable
from functools import lru_cache

LetterTransformer = Union[int, Dict[str, str], Callable[[str], str]]

DFLT_ALPHABET = ''.join(map(chr, range(ord('a'), (ord('z') + 1))))


def letter_plus_offset(letter, offset=1, alphabet=DFLT_ALPHABET):
    """
    >>> letter_plus_offset('a', 4)
    'e'
    >>> letter_plus_offset('z', 2)
    'b'
    >>> letter_plus_offset('a', offset=2, alphabet='aeiou')
    'i'
    """
    letter = letter.lower()
    assert letter in alphabet, f'That letter is out of range: {letter}'
    idx = alphabet.index(letter) + offset
    return alphabet[idx % len(alphabet)]


def mk_letter_map_from_offset(offset=1, alphabet=DFLT_ALPHABET):
    return {from_: letter_plus_offset(from_, offset, alphabet) for from_ in alphabet}


def _cycles_are_disjoint(cycles):
    from itertools import chain

    t = list(chain(*cycles))
    return len(set(t)) == len(t)


def _cycles_cover_alphabet(cycles, alphabet=DFLT_ALPHABET):
    from itertools import chain

    t = list(chain(*cycles))
    return set(t) == set(alphabet)


def multiple_cycles_letter_transformer(
    *letter_cycles, offset=1, alphabet=DFLT_ALPHABET
):
    """See vowel_separated_letter_transformer for a particular case."""
    assert _cycles_are_disjoint(letter_cycles)
    assert _cycles_cover_alphabet(letter_cycles, alphabet)

    def gen():
        for cycle in letter_cycles:
            yield from mk_letter_map_from_offset(offset, alphabet=cycle).items()

    return dict(gen())


def vowel_separated_letter_transformer(
    offset=1, vowels='aeiou', alphabet=DFLT_ALPHABET
):
    """A ceasar cypher with a fixed offset, but where the offset works on vowels and consonants cycles
    instead of the whole alphabet.

    It's a particular case of ``multiple_cycles_letter_transformer``.

    >>> vowel_sep = vowel_separated_letter_transformer()
    >>> list(vowel_sep.items())[:9]
    [('a', 'e'), ('e', 'i'), ('i', 'o'), ('o', 'u'), ('u', 'a'), ('b', 'c'), ('c', 'd'), ('d', 'f'), ('f', 'g')]
    """
    consonants = ''.join((x for x in alphabet if x not in vowels))
    return multiple_cycles_letter_transformer(
        vowels, consonants, offset=offset, alphabet=alphabet
    )


def get_letter_transformer(letter_transformer: LetterTransformer = 1):
    if isinstance(letter_transformer, int):
        letter_transformer = mk_letter_map_from_offset(letter_transformer)
    if isinstance(letter_transformer, dict):
        return lambda x: letter_transformer.get(x, x)
    else:
        assert callable(letter_transformer)
        return letter_transformer


def ceasar_cypher(
    phrase: str, letter_transformer: LetterTransformer = 1, preprocess=str.lower
):
    letter_transformer = get_letter_transformer(letter_transformer)
    if preprocess:
        phrase = preprocess(phrase)
    return ''.join([letter_transformer(letter) for letter in phrase])


def invert_mapping(d: dict):
    inverse_d = {v: k for k, v in d.items()}
    assert len(inverse_d) == len(d), f'Mapping had collisions when inverting: {d}'
    return inverse_d


@lru_cache
def get_simple_words(max_n_words=100_000, alphabet=DFLT_ALPHABET):
    from idiom import most_frequent_words
    from lexis import Lemmas

    words = set(Lemmas()) & most_frequent_words(max_n_words)
    return set(word for word in words if set(word.lower()).issubset(alphabet))


def closed_words(letter_transformer: LetterTransformer = 1, words=None):
    """
    My daughter "invented" the (a->b, b->c, ...) Ceasar cypher (https://en.wikipedia.org/wiki/Caesar_cipher)
    one day and proceeded in translating everyone's names and many other words.
    One day she stumbled on a word whose transformation was a valid english word itself.
    She was very excited about it.
    I told her daddy would ask the computer what other such words there were.
    Here's that.

    """
    if words is None:
        words = get_simple_words()
    for word in words:
        cyphered_word = ceasar_cypher(word, letter_transformer)
        if cyphered_word in words:
            yield word, cyphered_word
