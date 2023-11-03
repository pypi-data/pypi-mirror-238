# psusannx_pipeline

A package that contains the custom classes & sklearn preprocessing pipeline object to be used in the PSUSANNX project. Creating the package will allow the custom classes to be imported into any script (like standard sklearn preprocessors) and used. In particular once the pipeline has been fit to data, this package will allow the fitted transformer to be pickled out as a file and read into another script that has this package imported too.

This package was created to be used as a subpackage in a wider project - PSUSANNX.

## Custom Transformers

- CorrectNegPoints
- BucketFormations
- GetLogRatios
- GetPercentagesAndPerGame
- GetDifferences
- CatboostEncodeFormations
- DropFeatures
- CustomScaler

## Installation

``` python
pip install psusannx_pipeline
```

## Usage

This pipeline is to be used on a specific dataframe.

```python
# Import all the custom classes & pipeline object
from psusannx_pipeline.pipeline import *

# Fit the processing pipeline to the data
data_preprocessed = preprocessing_pipeline.fit_transform(data).dropna()
```

Now save the fitted preprocessing pipeline out to a pkl file so it can be used in other scripts.

```python
# Import pickle for serialization
import pickle

# Save out the preprocessing pipeline to be used in processing the new predictions
pickle.dump(preprocessing_pipeline, open("preprocessing_pipeline.pkl", "wb"))
```

## Notes

- The package is quite restricted in what it can do, but it only needs to do things that are required by the parent project so there won't be much development.
