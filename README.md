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
The generator is controlled by the number of sentences it must generate : parameter --sentences (100000 by default).
By default, the distribution of sentences by intention is uniform. It is possible to specify the distribution using an instance of Balancer
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
    --sentences=int         Number of sentences to generate (minimum)
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
I (like|love|am fan of) (badminton|sausages)
```

will be expanded as :

```
I like badminton
I like sausages
I love badminton
I love sausages
I am fan of badminton
I am fan of sausages
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
I (just want|X-want) to rent (a B-product|some B-product) in (B-city|B-zipcode)

```

> Note that # character is supported and can be used at the beginning of a line to skip it from sentence generation.

## Introduce variation in entity generation

It is possible to have several patterns of a same entity : a given entity may be relied to as many dictionaries as you want, simply suffix the file name / tag name with the # character.
For instance, the entity representing a "Professional" may be used in different way, according to its activity :

- Health => I want an appointement in Chicago with Doctor House as soon as possible
- Food => I need to contact Mario to fix a water leak
- ...

Both Mario and Doctor House have to be tagged as "B-Pro" but can't be in the same file. For this use case, simply add a "#attribute" to the main "B-Pro" pattern.
Sentences in the template file will look like :

- I want an appointement in B-city with B-pro#health as soon as possible
- I need to contact B-pro#plumber to fix a water leak

They are relied to two dictionaries :

- B-pro#health.csv
- B-pro#plumber.csv

And they generate these IOB forms :

- I want an appointement in Chicago with Doctor House as soon as possible : O O O O B-city O B-pro I-Pro as soon as possible
- I need to contact Mario to fix a water leak : O O O O B-pro O O O O O
