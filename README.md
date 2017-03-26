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
python generate_corpus.py --help

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--iterations=int] [--debug]
```
