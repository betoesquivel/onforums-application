# OnForumS: Mini Guardian
App to automatically summarize the discussion comments on a given article from the Guardian.
Group project application for the OnForumS task at University of Essex. This merges all modules developed so far.

# Pre-requisites
The app requires Python and MongoDB to be installed on the local machine, with a MongoDB process running on the default port.

# Installation
First, install the Python dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

Then, open a Python shell and enter the following:

```python
import nltk
nltk.download()
```

Which will open the NLTK GUI for downloading model packages. Look for the english tokenizer package called 'punkt', and hit 'Download'.

After that, you should be all set.

# User Guide
In order to actually start the server, run the following command on console, from the project's root directory:

```bash
python app.py
```

The server should start listening on port 5000, so just head over to http://localhost:5000/.

On the input bar that appears at the top of the page, enter the URL of an article from The Guardian which has some comments on it. Then click the big blue 'Summarize!' button, and wait. Depending on the amount of comments, the summarization process might take a few minutes.

Note that once an article has been previously processed, it will be stored on MongoDB, which means that the next time you request the same URL, the result will be almost instantaneous.
