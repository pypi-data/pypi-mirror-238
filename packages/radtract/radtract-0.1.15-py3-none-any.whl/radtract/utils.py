# Copyright © 2023 German Cancer Research Center (DKFZ), Division of Medical Image Computing
#
# SPDX-License-Identifier: Apache-2.0

from dipy.io.streamline import load_trk, save_trk
from fury.io import save_polydata
from fury.utils import lines_to_vtk_polydata, numpy_to_vtk_colors
from dipy.io.stateful_tractogram import Space, StatefulTractogram
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from fury.colormap import distinguishable_colormap
import joblib
import pandas as pd
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from scipy import stats
import seaborn as sns


def save_trk_streamlines(streamlines: nib.streamlines.array_sequence.ArraySequence, filename: str, reference_image: nib.Nifti1Image):
    """
    Convenience function to save streamlines to a trk file
    :param filename: filename of trk file
    """
    fib = StatefulTractogram(streamlines, reference_image, Space.RASMM)
    save_trk(fib, filename, bbox_valid_check=False)


def load_trk_streamlines(filename: str):
    """
    Convenience function to load streamlines from a trk file
    :param filename: filename of trk file
    :return: streamlines in dipy format
    """
    fib = load_trk(filename, "same", bbox_valid_check=False)
    streamlines = fib.streamlines
    return streamlines

def save_as_vtk_fib(streamlines, out_filename, colors=None):

    polydata, _ = lines_to_vtk_polydata(streamlines)
    if colors is not None:
        vtk_colors = numpy_to_vtk_colors(colors)
        vtk_colors.SetName("FIBER_COLORS")
        polydata.GetPointData().AddArray(vtk_colors)
    save_polydata(polydata=polydata, file_name=out_filename, binary=True)


def plot_parcellation(nifti_file, mip_axis):
    """
    
    """

    image = nib.load(nifti_file)
    data = image.get_fdata()
    mip = np.max(data, axis=mip_axis)
    nb_labels = len(np.unique(mip)) - 1
    fury_cmap = distinguishable_colormap(nb_colors=nb_labels)
    fury_cmap = [np.array([0, 0, 0, 1])] + fury_cmap
    mpl_cmap = ListedColormap(fury_cmap)
    plt.imshow(mip.T, cmap=mpl_cmap, origin='lower')
    plt.show()


def estimate_ci(y_true, y_scores):
    classes = np.unique(y_true)
    y_true_bin = label_binarize(y_true, classes=classes)
    ci_size = 0

    if len(classes) > 2:

        auc_scores = []
        for i in range(len(classes)):
            # Compute ROC curve and ROC area for each class
            fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_scores[:, i])
            roc_auc = auc(fpr, tpr)
            auc_scores.append(roc_auc)

        # Compute the standard error and the confidence intervals for each class
        conf_intervals = []
        for i in range(len(classes)):
            n1 = sum(y_true_bin[:, i])
            n2 = len(y_true_bin[:, i]) - n1
            roc_auc = auc_scores[i]
            
            q1 = roc_auc / (2.0 - roc_auc)
            q2 = 2 * roc_auc ** 2 / (1.0 + roc_auc)
            se = np.sqrt((roc_auc * (1 - roc_auc) + (n1 - 1) * (q1 - roc_auc ** 2) + (n2 - 1) * (q2 - roc_auc ** 2)) / (n1 * n2))

            conf_interval = stats.norm.interval(0.95, loc=roc_auc, scale=se)
            conf_intervals.append(conf_interval)

        # Compute weighted average of AUC scores and confidence intervals
        weights = [sum(y_true_bin[:, i]) for i in range(len(classes))]
        avg_auc_score = np.average(auc_scores, weights=weights)
        avg_conf_interval = [np.average([conf_intervals[i][j] for i in range(len(classes))], weights=weights) for j in range(2)]
        ci_size = avg_auc_score - avg_conf_interval[0]
        return ci_size, avg_auc_score

    else:

        # Compute ROC curve
        fpr, tpr, thresholds = roc_curve(y_true, y_scores[:, 1])
        roc_auc = auc(fpr, tpr)

        # Compute the standard error and the confidence intervals
        n1 = sum(y_true)
        n2 = len(y_true) - n1
        
        q1 = roc_auc / (2.0 - roc_auc)
        q2 = 2 * roc_auc ** 2 / (1.0 + roc_auc)
        se = np.sqrt((roc_auc * (1 - roc_auc) + (n1 - 1) * (q1 - roc_auc ** 2) + (n2 - 1) * (q2 - roc_auc ** 2)) / (n1 * n2))

        conf_interval = stats.norm.interval(0.95, loc=roc_auc, scale=se)
        ci_size = roc_auc - conf_interval[0]
        return ci_size, roc_auc


def load_results(result_pkl):
    
    aucs = dict()
    aucs['AUROC'] = []
    aucs['CI'] = []
    aucs['p'] = []
    aucs['y'] = []

    p, y = joblib.load(result_pkl)
    nsamples = len(p)//10
    
    for rep in range(10):
        p_rep = p[rep*nsamples:(rep+1)*nsamples]
        y_rep = y[rep*nsamples:(rep+1)*nsamples]

        ci, roc_auc = estimate_ci(y_rep, p_rep)

        aucs['AUROC'].append(roc_auc)
        aucs['CI'].append(ci)
        aucs['p'].append(p_rep)
        aucs['y'].append(y_rep)

    aucs = pd.DataFrame(aucs)
    return aucs


def is_inside(index, image):
    """
    Checks if a given index is inside the image.
    :param index:
    :param image:
    :return:
    """
    for i in range(3):
        if index[i] < 0 or index[i] > image.shape[i] - 1:
            return False
    return True



def main():
    pass


if __name__ == '__main__':
    main()
