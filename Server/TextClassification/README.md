# Text Classifier

A python3 classifier that assigns a category to some given texts using a machine learning model and saves the model to the hard disk for faster reuse.

## Usage in a python script:
First, import the TextClassifier class from the TextClassifier module. This would look something like this:

	from TextClassifier import TextClassifier
Then, create a TextClassifier object with the getTextClassifier static method supplying a path to the data set. This would look something like this:

	data_set_path = 'data/bbc'
	tc = TextClassifier.getTextClassifier(data_set_path)
This method saves and loads the text classifier with the pickle module to a binary file local to the data set (something like 'data/bbc/pickle_data.bin') to avoid computing the ML model from scratch every time an object is created. To force the computation even if the pickle_data.bin file exists, pass forceRecompute=True to the static method like this:

	tc = TextClassifier.getTextClassifier(data_set_path, forceRecompute=True)

This object can the be reused indefinetly to predict a category for new texts using the predictTexts() method by supplying a list of strings as a parameter:

    categories, internalCategoryIndexes = tc.predictTexts([text1, text2, text3])
    print('The prediction for the first text is', categories[0])

A concrete use example can be found in useExample.py