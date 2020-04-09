# Huffman's Compression Algorithm

<p align="center">
  <img src="https://media.giphy.com/media/duXkd6NG5MwOKomroU/giphy.gif">
</p>

Implemented via [this video](https://www.youtube.com/watch?v=NjhJJYHpYsg). Read more [here](https://en.wikipedia.org/wiki/Huffman_coding). Fixed byte decoding/encoding issue with help [from this post](# https://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
). Actual [motivating factor](https://arxiv.org/abs/2004.02872) along with avoiding an international relations essay. [What I like to think motivated me](https://www.youtube.com/watch?v=NH2lwGzBruM).



## Stats

Compressed the entire [Illiad](http://www.gutenberg.org/ebooks/6130) and compared against [ASCII encoding](http://www.asciitable.com/).

```
Compressed size: 54.4% of original                                                                                      
Size of huffman compressed file: 446.6kb                                                                                
Size of ascii compressed file: 807.45kb                                                                                 
Size of  uncompressed file: 820.89kb                                                                                    
Time to encode Huffman: 1.5512933731079102                                                                              
Time to encode ASCII: 5.0967748165130615                                                                                
Time to decode Huffman: 2.7544658184051514  
```
