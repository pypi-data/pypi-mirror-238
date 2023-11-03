import sklearn
import numpy as np

def precision_recall_f1_score (label, prediction):
    label = label.copy ()
    prediction = prediction.copy ()
    for i in range (1, label.shape [-1]):
        label [:,:,i] *= (i + 1)
        prediction [:,:,i] *= (i + 1)
    y_true_f = label.flatten().astype (int)
    y_pred_f = prediction.flatten().astype (int)
    return sklearn.metrics.precision_recall_fscore_support (y_true_f, y_pred_f, average = 'macro') [:3]

binary_precision_recall_f1_score = precision_recall_f1_score
