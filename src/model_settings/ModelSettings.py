from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Parent class of all classifier specific settings. 
As a result all classifier settings e.g. "DecisionTreeClassifierSettings"
will have attributes :
classifierLayout : html structure of the settings
parameters : An array of all accepted parameters
classifier : A class reference to the correct classifier

"""
class ClassifierSettings():

    '''
    The following variables are text used in parameter tooltips. The information they contain
    is sourced from the sci-kit learn website.
    '''

    criterion = 'The function to measure the quality of a split.'
    splitter = 'The strategy used to choose the split at each node.'
    max_depth = 'The maximum depth of the tree.'
    min_samples_split = 'The minimum number of samples required to split an internal node.'
    min_samples_leaf = 'The minimum number of samples required to be at a leaf node.'
    min_weight_fraction_leaf = 'The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node.'
    max_features = 'The number of features to consider when looking for the best split'
    random_state = 'Controls the randomness of the estimator. The features are always randomly permuted at each split, even if splitter is set to "best".'
    max_leaf_nodes = 'Grow a tree with max_leaf_nodes in best-first fashion.'
    min_impurity_decrease = 'A node will be split if this split induces a decrease of the impurity greater than or equal to this value.'
    ccp_alpha = 'Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.'
    loss = 'The loss function to be optimized. ‘log_loss’ refers to binomial and multinomial deviance, the same as used in logistic regression. It is a good choice for classification with probabilistic outputs. For loss ‘exponential’, gradient boosting recovers the AdaBoost algorithm.'
    learning_rate = 'Learning rate shrinks the contribution of each tree by learning_rate. There is a trade-off between learning_rate and n_estimators.'
    n_estimators = 'The number of boosting stages to perform. Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance.'
    subsample = 'The fraction of samples to be used for fitting the individual base learners.'
    init = 'An estimator object that is used to compute the initial predictions.'
    verbose = 'Enable verbose output. If 1 then it prints progress and performance once in a while (the more trees the lower the frequency). If greater than 1 then it prints progress and performance for every tree.'
    warm_start = 'When set to True, reuse the solution of the previous call to fit and add more estimators to the ensemble, otherwise, just erase the previous solution.'
    validation_fraction = 'The proportion of training data to set aside as validation set for early stopping.'
    n_iter_no_change = 'Used to decide if early stopping will be used to terminate training when validation score is not improving.'
    tol = 'Tolerance for the early stopping. When the loss is not improving by at least tol for n_iter_no_change iterations (if set to a number), the training stops.'
    bootstrap = 'Whether bootstrap samples are used when building trees. If False, the whole dataset is used to build each tree.'
    oob_score = 'Whether to use out-of-bag samples to estimate the generalization score. Only available if bootstrap=True.'
    n_jobs = 'The number of jobs to run in parallel. fit, predict, decision_path and apply are all parallelized over the trees. None means 1. -1 means using all processors.'
    max_samples = 'If bootstrap is True, the number of samples to draw from X to train each base estimator.'
    C = 'Regularization parameter. The strength of the regularization is inversely proportional to C. Must be strictly positive.'
    kernel = 'Specifies the kernel type to be used in the algorithm.'
    degree = 'Degree of the polynomial kernel function (‘poly’). Must be non-negative.'
    gamma = 'Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.'
    coef0 = 'Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’.'
    shrinking = 'Whether to use the shrinking heuristic.'
    probability = 'Whether to enable probability estimates.'
    cache_size = 'Specify the size of the kernel cache (in MB).'
    class_weight = 'Set the parameter C of class i to class_weight[i]*C for SVC. If not given, all classes are supposed to have weight one.'
    max_iter = 'Hard limit on iterations within solver, or -1 for no limit.'
    decision_function_shape = 'Whether to return a one-vs-rest (‘ovr’) decision function of shape (n_samples, n_classes) as all other classifiers, or the original one-vs-one (‘ovo’) decision function of libsvm which has shape (n_samples, n_classes * (n_classes - 1) / 2).'
    break_ties = 'Hard limit on iterations within solver, or -1 for no limit'
    def __init__(self):
        self.classifierLayout = [html.Div(id = "empty-settings", children=[])]
        self.parameters = []
        self.classifier = None
