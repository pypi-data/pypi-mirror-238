import pandasflow as pdf
import pandas as pd


y_true = pd.Series([10, 10, 10, 10, 10])
y_pred = pd.Series([5, 5, 7, 5, 5])
weights = pd.Series([1, 1, 1, 1, 1])

print('default')
prev = pdf.metrics.mean_error(y_true, y_pred, r=True)
print('\nw\\prev')
pdf.metrics.mean_error(y_true, y_pred, previous=prev)
print('\nw\\prev&round')
pdf.metrics.mean_error(y_true, y_pred, previous=prev, round_=3)