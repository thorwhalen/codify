# codify
Generate codes


To install:	```pip install codify```



# Qr code


```python

from codify.qr_coding import qrcode_img_of

qrcode_img_of('https://github.com/thorwhalen')
```



![png](https://raw.githubusercontent.com/thorwhalen/codify/master/data/img/output_4_0.png)


And if you wanted to save that, you just do:

```python
qrcode_img_of('https://github.com/thorwhalen').save('qr_code_of_my_website.png')
```


But qr codes aren't just for links. They're just a means to implement text->image->text error compressed and robust communication pipeline.

For example...


```python
some_long_text = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
It was popularised in the 1960s with the release of Letraset sheets containing 
Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""
qrcode_img_of(some_long_text)
```




![png](https://raw.githubusercontent.com/thorwhalen/codify/master/data/img/output_6_0.png)

    



Obviously, this could get out of hand. 

But if all you're doing is wanting to send a fingerprint (a hash) of some text, for verification or legal purposes. 

For this, you can use sha256 for example...


```python
from codify import bytes_to_sha256
bytes_to_sha256(some_long_text.encode()).hex()
```



    'a1a2423753693304b35308d019a37bbb12b8e8c36e07c02d1e448f28927ea557'



```python
from codify.qr_coding import qrcode_img_of_sha256
qrcode_img_of_sha256(some_long_text)
```



![png](https://raw.githubusercontent.com/thorwhalen/codify/master/data/img/output_10_0.png)


# Ceasar Cyphers

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

    

