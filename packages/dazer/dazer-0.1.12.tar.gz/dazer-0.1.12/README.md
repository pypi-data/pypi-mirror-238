# DAZER (DAtaset siZe Effect estimatoR)

## Class Subsampler with examples

```python
import dazer

subsampler = dazer.Subsampler(df, dataset.keep_ratio, .2)

df_test = subsampler.extract_test()

df_test = subsampler.extract_test(subsample_factor=.2, random_state=101)

df_train_1 = subsampler.subsample(subsample_factor=.1, random_state=101)
df_train_2 = subsampler.subsample(subsample_factor=.2, random_state=101)
df_train_3 = subsampler.subsample(subsample_factor=.3, random_state=101)
```

## Class Classifier with examples

```python
import dazer

y_test = df_test[target_column] == target_value
X_test = df_test.drop([target_column], axis=1)

y_train = df_train_1[target_column] == target_value
X_train = df_train_1.drop([target_column], axis=1)

classifier = dazer.Classifier(X_train, y_train, X_test, y_test)
model, evaluation = classifier.train_test_random_forest(random_state=101, model_path='models/model_1.joblib', scoring='f1')
```

## Run unittests

`python3 -m unittest discover tests`