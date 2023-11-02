
# there are many types of loss functions which use for finding accuracy of our alorithems
# this is our goal to reduse error of our model by decrease losses, to getting the optimum value '*w' and '*b' 
class loss_function():
    '''Loss function is use to determine the error between predicted and actual labels,
    also for the machine to find the optimum value of 'w' and 'b' during training a set
    takes list of the feature and labels (respective x and y), and w and b (initialize with 0.0) '''
    # loding actual and predicted data rows as list form to initialize different types of losses
    def __init__(self, y, x, w=0.0, b=0.0):
        # initially define value of 'w' and 'b' which is 0.0 by default
        (self.y, self.x, self.w, self.b) = (y, x, w, b)
    
    # -----'N' is always define total numbers of data points in actual dataset##----- #

    # L2 loss is stands for mean square error (MSE)
    # returns a floating point of value
    def L2_loss(self):
        ''' L2 loss for finding the mean square error of a predicted list and
        actual list of labels'''
        error = 0.0
        N = len(self.x)
        for i in range(N):
            # increases error value by mean of sqare of predicted and actual data points
            error += (self.y[i] - (self.w*self.x[i]+self.b))**2
        return error/float(N)

    # this is only a local program to calculate difference of actual and predicted data points
    # and returns a list of errors 
    def absolute_error(self):
        errors = []
        N = len(self.x)
        for i in range(N):
            # directly substract the value of actual and predicted points
            errors.append((self.w*self.x[i]+self.b) - self.y[i])
        return errors
    
    # L1 loss is stands for mean absolute error (MAE)
    # returns floating point
    def L1_loss(self):
        errors = 0.0
        N = len(self.x)
        for i in range(N):
            # applying calculation upto range
            errors += self.y[i] - self.w*self.x[i]+self.b
        return errors/float(N)
   
   # SSE is nothing but sum of square error returns the list of errors
    def SSE(self):
        errors = []
        N = len(self.x)
        for i in range(N):
            # adding the prediction and actual of square
            errors.append((self.y[i] - (self.w*self.x[i]+self.b))**2)
        return errors

    # RMSD - root mean square, MSE is divided by total number of list of predictions
    # and after finding root of it's result
    def RMSD(self):
        N = len(self.x)
        # ---->>> **0.5 is use for finding 'root' <<<---- #
        return (self.L2_loss()/N)**0.5
    
    # the hinge loss is a loss function used for training classifiers. the hinge loss is
    # used for "maximum margin" classification, most notably for support vector machine (SVM)
    def hinge(self):
        hinge = []
        N = len(self.x)
        for i in range(N):
            hinge.append(max(0, 1 - (self.w*self.x[i]+self.b) * self.y[i]))
        # returns list of errors
        return hinge


def covarince(x_set, y_set):
    x_mean = statistics(x_set).mean()
    y_mean = statistics(y_set).mean()
    addtion = 0.0
    n = len(x_set)
    for x, y in zip(x_set, y_set):
        addtion += (x - x_mean)*(y - y_mean)
    return addtion/n


# statistics use formulas that's find mean, median, variance and std. deviation
# takes a list of feature 'X' return output as float
# but in the case of median it's returns 
class statistics():
    """
    statistics class function is use for the performing basic task about, finding mean or the avg. value of set, variance,
    median and standard deviation.
    """
    def __init__(self, x_set):
        self.x = x_set
        self.N = len(x_set)

    def mean(self):
        Elements = sum(self.x)
        return Elements/float(self.N)

    def variance(self):
        mean = self.mean()
        sumation = 0.0
        for i in self.x:
            sumation += (i - mean)**2
        return sumation/self.N

    def median(self):
        if self.N % 2 == 0:
            term = int((self.N + 1)/2)
            return self.x[term-1]
        else:
            d = self.N/2
            term = int(d + (d +1)/2)
            return self.x[term-1]    
    
    def standard_dev(self):
        mean = self.mean()
        sumation = 0.0
        for i in self.x:
            sumation += (i - mean)**2
        return (sumation/self.N)**0.5


# we need a way to determine if there is linear correlation or not, so we calculate what is know 
# as the PRODUCT-MOMENT CORRELATION COEFFICIENT.
def Product_moment_CC(x_set, y_set):
    std_y = statistics(y_set).standard_dev()
    std_x = statistics(x_set).standard_dev()
    x_mean = statistics(x_set).mean()
    y_mean = statistics(y_set).mean()
    addtion = 0.0
    n = len(x_set)
    for x, y in zip(x_set, y_set):
        addtion += (x - x_mean)*(y - y_mean)
    covar = addtion/n
    return covar/std_x*std_y

