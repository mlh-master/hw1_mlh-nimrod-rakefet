# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_ctg_df = CTG_features.copy()
    # Drop the extra features DR in our case
    cols = CTG_features.columns.drop(extra_feature)
    # Change to NaN non numbers with the help of to_numeric
    c_ctg_df = c_ctg_df[cols].apply(pd.to_numeric, errors='coerce')
    # Convert to a Dictionary and remove from all NaN values
    #c_ctg_full = c_ctg_df.to_dict()
    c_ctg = {k: [elem for elem in v if not np.isnan(elem)] for (k, v) in c_ctg_df.items()}
    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_cdf_df = CTG_features.copy()
    # Drop the extra features DR in our case
    cols = CTG_features.columns.drop(extra_feature)
    # Change to NaN non numbers with the help of to_numeric
    c_cdf_df = c_cdf_df[cols].apply(pd.to_numeric, errors='coerce')
    c_cdf = {k: [np.random.choice(v[v.notnull()].array) if np.isnan(elem) else elem for elem in v] for (k, v) in c_cdf_df.items()}

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    d_summary = c_feat.describe(include='all')
    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_no_outlier = {k: [elem if ((elem >= d_summary.at['25%', k]) & (elem <= d_summary.at['75%', k])) else np.nan for elem in v] for (k, v) in c_feat.items()}
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    filt_feature = {}
    c_cdf_temp = c_cdf.copy()
    c_cdf_temp[feature] = [elem if (elem < thresh) else np.nan for elem in c_cdf[feature]]
    filt_feature = nan2num_samp(c_cdf_temp, []) #Fill nans with random numbers
    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    modes = ['standard' 'MinMax' 'mean']
    nsd_res = CTG_features;
    if mode == 'standard':
        nsd_res = {k: [(elem-np.mean(v.array))/np.std(v.array) for elem in v] for (k, v) in CTG_features.items()}
    if mode == 'MinMax':
        nsd_res = {k: [(elem-np.min(v.array))/(np.max(v.array) - np.min(v.array)) for elem in v] for (k, v) in CTG_features.items()}
    if mode == 'mean':
        nsd_res = {k: [(elem-np.mean(v.array))/(np.max(v.array) - np.min(v.array)) for elem in v] for (k, v) in CTG_features.items()}
    if flag=='True':
        # Histograms to compare before and after normalization of 2 features:
        place_in_win = 0
        fig, (up_ax, down_ax) = plt.subplots(2, 2)
        axes = [up_ax, down_ax]
        for feat in selected_feat:
            CTG_features.hist(feat, bins=100, ax=axes[place_in_win][0])
            plt.suptitle(feat)
            pd.DataFrame(nsd_res).hist(feat, bins=100, ax=axes[place_in_win][1])
            plt.suptitle('Original                                    Normelized ' +  mode)
            place_in_win += 1
        plt.tight_layout()
        plt.show()
    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)
