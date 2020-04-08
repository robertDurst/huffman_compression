# Huffman's Compression Algorithm

Implemented via [this video](https://www.youtube.com/watch?v=NjhJJYHpYsg). Read more [here](https://en.wikipedia.org/wiki/Huffman_coding). Fixed byte decoding/encoding issue with help [from this post](https://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
). Actual [motivating factor](https://arxiv.org/abs/2004.02872) along with avoiding an internation relations essay. What I like to think motivated me:

[![IMAGE ALT TEXT HERE](https://news.mlh.io/wp-content/uploads/2015/06/2.png)](https://www.youtube.com/watch?v=NH2lwGzBruM)

## Stats

Compressed the entire [Illiad](http://www.gutenberg.org/ebooks/6130) and compared against [ASCII encoding](http://www.asciitable.com/).

```
Compressed size: 54.4% of original                                                                                      
Size of huffman compressed file: 446.6kb                                                                                
Size of ascii compressed file: 807.45kb                                                                                 
Size of  uncompressed file: 820.89kb                                                                                    
Time to encode Huffman: 1.55 sec                                                                           
Time to encode ASCII: 5.10 sec                                                                           
Time to decode Huffman: 2.75 sec
```
