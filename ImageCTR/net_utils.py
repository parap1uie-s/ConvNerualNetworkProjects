import os
import numpy as np
import tensorflow as tf
import h5py
import math

def load_dataset():
    train_dataset = h5py.File('data/train.h5', "r")
    train_set_img_orig = np.array(train_dataset["train_set_image"][:]) # your train set features
    train_set_csr_orig = np.array(train_dataset["train_set_csr"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

    test_dataset = h5py.File('data/test.h5', "r")
    test_set_img_orig = np.array(test_dataset["test_set_image"][:]) # your train set features
    test_set_csr_orig = np.array(test_dataset["test_set_csr"][:]) # your train set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your train set labels
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return train_set_img_orig, train_set_csr_orig, train_set_y_orig, test_set_img_orig, test_set_csr_orig, test_set_y_orig

def load_dataset_onehot():
    train_dataset = h5py.File('data/train_onehot.h5', "r")
    train_set_img_orig = np.array(train_dataset["train_set_image"][:]) # your train set features
    train_set_csr_orig = np.array(train_dataset["train_set_csr"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

    test_dataset = h5py.File('data/test_onehot.h5', "r")
    test_set_img_orig = np.array(test_dataset["test_set_image"][:]) # your train set features
    test_set_csr_orig = np.array(test_dataset["test_set_csr"][:]) # your train set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your train set labels
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return train_set_img_orig, train_set_csr_orig, train_set_y_orig, test_set_img_orig, test_set_csr_orig, test_set_y_orig

def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
    """
    Creates a list of random minibatches from (X, Y)
    
    Arguments:
    X -- input data, of shape (input size, number of examples) (m, Hi, Wi, Ci)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples) (m, n_y)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.
    
    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:,:,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:,:,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches


def convert_to_one_hot(Y,classes):
    ret = np.zeros((len(Y),classes))
    for key in range(len(Y)):
        ret[key, Y[key]] = 1
    return ret