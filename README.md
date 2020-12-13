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


