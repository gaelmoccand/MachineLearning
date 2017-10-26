# -*- coding: utf-8 -*-
"""Useful methods for project 1"""
import numpy as np
from helpers import batch_iter # for the batch_iter CHECK if need to copy PAST down here

# ***************************************************
# COSTS
# ***************************************************
def calculate_mse(e):
    """Calculate the mse from the input vector"""
    N = len(e)
    mse = e.T.dot(e)/(2*N)
    return mse
    
def compute_loss(y, tx, w):
    """Calculate the loss.

    You can calculate the loss using mse or mae.
    """
    error = y - tx.dot(w)
    return calculate_mse(error)

# ***************************************************
# GRADIENT DESCENT
# ***************************************************
def compute_gradient(y, tx, w):
    """Compute the gradient."""
    error = y - tx.dot(w)
    N = len(error)
    grad = -tx.T.dot(error)/N
    
    return grad, error


def gradient_descent(y, tx, initial_w, max_iters, gamma):
    """Gradient descent algorithm."""
    # Define parameters to store w and loss
    ws = [initial_w]
    losses = []
    w = initial_w
    for n_iter in range(max_iters):
        # Compute gradient and loss
        grad, error = compute_gradient(y, tx, w)
        loss = compute_mse(error)
        # Update w by gradient
        w = w - gamma*grad
        # store w and loss
        ws.append(w)
        losses.append(loss)
        print("Gradient Descent({bi}/{ti}): loss={l}, w0={w0}, w1={w1}".format(
              bi=n_iter, ti=max_iters - 1, l=loss, w0=w[0], w1=w[1]))

    return losses, ws

# ***************************************************
# LEAST SQUARES
# ***************************************************    
def least_squares_GD(y, tx, initial_w, max_iters, gamma):
    """Linear regression using gradient descent"""
    raise NotImplementedError
    

def least_squares_SGD(y, tx, initial_w, max_iters, gamma):
    """Linear regression using stochastic gradient descent"""
    # Define parameters to store w and loss
    ws = [initial_w]
    losses = []
    w = initial_w
    for n_iter in range(max_iters):
        for minibatch_y, minibatch_tx in batch_iter(y, tx, 1): # set batch size to 128
            grad,_=compute_gradient(minibatch_y,minibatch_tx,w) # compute the stochastic gradient using the minibatches
            w = w - (gamma)*grad # update the w
            loss = compute_loss(y,tx,w)# compute the loss using the entire sets
            ws.append(w)#save w
            losses.append(loss) #save the loss
        print("Stochastic Gradient Descent({bi}/{ti}): loss={l}, w0={w0}, w1={w1}".format(
              bi=n_iter, ti=max_iters - 1, l=loss, w0=w[0], w1=w[1]))    
    return losses, ws
    

def least_squares(y, tx):
    """Least squares regression using normal equations"""
    # We want to solve the linear system Aw = b...
    # ...with A being the Gram Matrix...
    A = tx.T.dot(tx)
    # ... and b being the transpose of tx times y    """Least squares regression using normal equations"""
    
    b = tx.T.dot(y)
    # solve linear system using the QR decomposition
    return np.linalg.solve(A, b)
    
# ***************************************************
# REGRESSION
# ***************************************************
def ridge_regression(y, tx, lambda_):
    """Ridge regression using normal equations"""
    # We want to solve the linear system Ax = b
    # A is the sum of the Gram matrix and the identidy multiplied by lambda
    lambda_id = tx.shape[0]*lambda_*np.identity(tx.shape[1])
    gram_mat = tx.T.dot(tx)
    A = gram_mat + lambda_id
    
    # b is the product between tx transposed and y
    b = tx.T.dot(y)
    
    # Solve with the QR decomposition
    return np.linalg.solve(A, b)

    
def logistic_regression(y, tx, initial_w, max_iters, gamma):
    """Logistic regression using gradient descent"""
    # Define parameters to store w and loss
    ws = [initial_w]
    losses = []
    w = initial_w
    for n_iter in range(max_iters):
        # compute the sigmoid function
        Xw = tx.dot(w);
        sigma = np.exp(Xw)/(1 + np.exp(Xw));
        # then the loss
        tmp = -y.T.dot(np.log(sigma)) + (y-1).T.dot(np.log(1 - sigma));
        # this returns an element of size (1,1) -> reshape
        loss = np.squeeze(tmp);
        # Compute the gradient of the loss w.r.t w
        grad = tx.T.dot(sigma-y);
        # Update w by gradient
        w = w - gamma*grad
        # store w and loss
        ws.append(w)
        losses.append(loss)
        print("Gradient Descent({bi}/{ti}): loss={l}, w0={w0}, w1={w1}".format(
              bi=n_iter, ti=max_iters - 1, l=loss, w0=w[0], w1=w[1]))

    return losses, ws


def reg_logistic_regression(y, tx, lambda_, initial_w, max_iters, gamma):
    """Regularized logistic regression using gradient descent or SGD"""    
    raise NotImplementedError