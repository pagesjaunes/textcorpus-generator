# WTF is it ?
textcorpus-generator is tool that aims to generate a corpus of sentences for learning tasks.
It has been built at SolocalGroup to create artificial data for slotFilling and intend detections.

# Install and requirements
The project requires python 3.4+.
Before running the generator, install the dependencies with pip :

```
pip install -r requirements.txt
```

# Running unit test
To check that all is ok, run the unit tests with pytest :

```
pytest test/
```

# Running main generator
To generate a corpus run the main generator
```
"""
    Text corpus generation

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--utterance=int] [--debug]

Options:
    --help                  Displays help message
    --templates=filepath    Sets the path to the template file
    --dictionaries=path     Sets the path to the dictionary directory
    --output_path=path      Sets the path where to write the generated corpus
    --utterance=int         Number of utterances over a template for a given
    --debug                 Debug version of the script

"""
```

# Template format

The engine iterates over all the lines of a given template file and creates as many sentences as the expansion forms give.
Dealing with several forms is done with two main features :

- Optional words, set by parenthesis piped separated sequence ;
- Dictionary words, set by "B-label" and "X-label" special tags

## Multi form pattern

Setting parenthesis tells the engine that it must iterates over each item of the sequence to create as many sequences as the set size.
For instance :

```
I (like|love|am fan of) (badminton|saucisses)
```

will be expanded as :

```
I like badminton
I like saucisses
I love badminton
I love saucisses
I am fan of badminton
I am fan of saucisses
```

## Dictionaries

Templates support dictionary references, that makes a sentence generic. Two types of dictionaries are supported :

- B form : a 'B-label' tag refers to a csv file 'B-label.csv' that contains all occurences that 'B-label' represents. At generation time, the word or expression taken from the dictionary are connected to a "B-label / I-label" representation.
- X form : a 'X-label' tag refers to a csv file 'X-label.csv' that contains all occurences that 'X-label' represents. At generation time, the word or expression taken from the dictionary are connected to a "O" representation.

For instance, engine can deal with such a template :
```
I X-want to go to B-city
```

assuming that two files exist :

X-want.csv :

```
want
would like
would be happy
```

B-city.csv :
```
Paris
Vern sur seiche
Roma
```

For each iteration over the template file, the engine will randomly pick some data in the dictionaries and generates different forms :

```
I would like to go to Vern sur seiche
I would be happy to go to Roma
```

associated to the IOB representation :

```
O O O O O O B-city I-city I-city
O O O O O O O B-city
```

## Combo

Of course, dictionaries and multi form pattern can be associated

```
I (juste want|X-want) to rent (a B-product|some B-product) in (B-city|B-zipcode)

```

> Note that # character is supported and can be used at the beginning of a line to skip it from sentence generation.

