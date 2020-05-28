# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name: Richter Jordaan
# Collaborators: None
# Time: 4:00

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2000)
TESTING_INTERVAL = range(2000, 2017)

############################################
#    Begin helper code - do not modify     #
############################################
class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Parameters:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Parameters:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Parameters:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Parameters:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - np.mean(x))**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

##########################
#    End helper code     #
##########################

def linear_reg(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Parameters:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """
    #first find averages
    x_avg = np.mean(x)
    y_avg = np.mean(y)
    
    #now find the slope from given formula
    m_numerator = 0.0
    m_denom = 0.0
    
    for i in range(len(x)):
        m_numerator += (x[i]-x_avg)*(y[i]-y_avg)#this part contributes to numerator
        m_denom += (x[i]-x_avg)**2#this part contributes to denominator
    
    #return m and b
    return (m_numerator/m_denom, y_avg-(m_numerator/m_denom)*x_avg)


def total_squared_error(x, y, m, b):
    '''
    Calculates the total squared error of the linear regression model given the set
    of data points and the regression line. 

    Parameters:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    '''
    squared_error = 0.0 #total squared error
    
    for i in range(len(x)): #add square of difference between observed and predicted y val
        squared_error += (y[i]-m*x[i]-b)**2
        
    return squared_error


def fit_models(x, y, degrees):
    """
    Generates a list of polynomial regression models with degrees, specified by
    degrees, for the given set of data points. Note, the list of models should appear 
    in the same order as their corresponding integer in the degrees parameter.

    Parameters:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    #for each i, append to list and then return the list, can use list comprehension
    return [np.polyfit(x,y,degrees[i]) for i in range(len(degrees))]


def evaluate_models_training(x, y, models, display_graphs):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (i.e. the model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        Degree of your regression model,
        R-squared of your model evaluated on the given data points,
        and standard error/slope (if this model is linear).

    R-squared and standard error/slope should be rounded to 4 decimal places.

    Parameters:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the R-squared value for each model
    """
    #np.polyval(p,x)
    #sklearn.metrics.r2score(y_true, y_pred)
    
    r_squared_values = [] #list of r-squared values for each model
    
    for i in range(len(models)):
        
        #get predicted y values, using list comprehension
        y_pred = [np.polyval(models[i],x[index]) for index in range(len(x))]
        
        #get r_squared value for model
        r_squared_values.append(r2_score(y, y_pred))
             
        if display_graphs: #display graph
            plt.plot(x,y,'b.')#plot data points in blue with dots
            plt.plot(x,y_pred,'r')
            plt.xlabel("Year")#add x label
            plt.ylabel("Avg Temperature (Celcius)")#y label
            
            deg = len(models[i])-1 #degree of polynomial
            title = "Model degree: " + str(deg) + ", R-squared value: " + str(round(r_squared_values[i],4))
            
            if deg == 1:#if degree is 1, calculate SE/slope and add to title
                se_over_slope = standard_error_over_slope(x, y, np.array(y_pred), models[i])
                title = title + " SE over slope: " + str(round(se_over_slope,4))
                
            plt.title(title) #add title
            plt.show()#show graph
        
    return r_squared_values


def get_cities_averages(dataset, cities, years):
    """
    For each year in the given range of years, computes the average of the
    annual temperatures in the given cities.

    Parameters:
        dataset: instance of Dataset
        cities: a list of the names of cities to include in the average
            annual temperature calculation
        years: a list of years to evaluate the average annual temperatures at

    Returns:
        a 1-d numpy array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avgs = np.zeros(len(years))#create numpy array of fixed size, now with all 0s
    
    for i in range(len(years)):
        sum_temps = 0#find sum of all temps
        for city in cities:#add city's mean temp to sum
            sum_temps += np.mean(dataset.get_daily_temps(city,years[i]))
        
        avgs[i] = sum_temps/len(cities)#assign avg temp among all cities for that year
        
    return avgs
        

        


def identify_extreme_trend(x, y, length, positive_slope):
    """
    Parameters:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope with the sign specified by positive_slope and j-i = length. 
        Note the range (i,j) we are considering will be i inclusive, j exclusive.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have the same slope (within the
        acceptable tolerance), (2,5) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    #linear_reg(x,y)
    
    max_index=-1 #a negative index represents no possible solutions yet
    extreme_slope = 0 #the best possible slope
    
    for i in range(len(x)-length-1):
        j=i+length
        slope = linear_reg(x[i:j],y[i:j])[0]#calculate slope of range of i and j
        
        case1 = positive_slope and (slope - 1E-8) > extreme_slope#new best positive
        case2 = not positive_slope and slope<0 and (abs(slope)- 1E-8) > abs(extreme_slope) #new best neg
        if case1 or case2:#if new best slope, update index and best slope value
            max_index = i
            extreme_slope = slope
    #return indices, but if no valid slopes exist, max_index is still -1, so will return None
    return (max_index,max_index+length) if max_index>=0 else None


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Parameters:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    #TODO
    sum_squared_error = 0.0 #square of denominator of rmse
    
    for i in range(len(y)):
        sum_squared_error += (y[i]-estimated[i])**2#square of error
    return (sum_squared_error/len(y))**(1/2)#square root of error squared sum divided by n


def evaluate_models_testing(x, y, models, display_graphs):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Parameters:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    rmse_vals = [] #list of RMSE values for each model
    
    for model in models:
        y_pred = [np.polyval(model,x[index]) for index in range(len(x))]#calculate estimated
        
        rmse_vals.append(round(rmse(y,y_pred),4)) #compute and append rmse val
        
                     
        if display_graphs: #display graph
            plt.plot(x,y,'b.')#plot data points in blue with dots
            plt.plot(x,y_pred,'r')
            plt.xlabel("Year")#add x label
            plt.ylabel("Avg Temperature (Celcius)")#y label
            
            deg = len(model)-1 #degree of polynomial
            title = "Model degree: " + str(deg) + ", RMSE: " + str(rmse_vals[-1])
            
            plt.title(title) #add title
            plt.show()#show graph
        
    return rmse_vals


if __name__ == '__main__':
    
    pass

    data = Dataset("data.csv")
    
    # Problem 4A
    print("Problem 4A")
    x = list(range(1961,2017))
    y = [data.get_temp_on_date('SAN FRANCISCO', 12, 12, x[i]) for i in range(len(x))]
    poly = fit_models(x,y,[1])
    print("Linear regression on December 12 temperature in SF from 1961 to 2017")
    r_val = evaluate_models_training(x, y, poly, True)
    
    # Problem 4B
    print("Problem 4B")
    y2 = get_cities_averages(data,['SAN FRANCISCO'],x)
    poly = fit_models(x,y2,[1])
    r_val = evaluate_models_training(x, y2, poly, True)

    # Problem 5B
    print("Problem 5B")
    print("Increase in Tampa weather")
    x = list(range(1961,2017))
    y = get_cities_averages(data,['TAMPA'],x)
    i,j = identify_extreme_trend(x,y,30,True)
    print("max increase in avg temp per year: ",round(linear_reg(x[i:j],y[i:j])[0],4))
    print("start year:",x[i], ", end year (inclusive):",x[j]-1)
    print("Model of 30 year temp below")
    
    #plot model
    poly = fit_models(x[i:j],y[i:j],[1])
    r_val = evaluate_models_training(x[i:j], y[i:j], poly, True)

    # Problem 5C
    print("Problem 5C")
    print("Decrease in Tampa weather")
    x = list(range(1961,2017))
    y = get_cities_averages(data,['TAMPA'],x)
    i,j = identify_extreme_trend(x,y,15,False)
    print("max decrease in avg temp per year: ",round(linear_reg(x[i:j],y[i:j])[0],4))
    print("start year:",x[i], ", end year (inclusive):",x[j]-1)
    print("Model of 15 year temp below")
    
    #plot model
    poly = fit_models(x[i:j],y[i:j],[1])
    r_val = evaluate_models_training(x[i:j], y[i:j], poly, True)

    # Problem 6B
    print("Problem 6B")
    print("Training interval")
    x = list(TRAINING_INTERVAL)
    y = get_cities_averages(data,CITIES,x)
    poly = fit_models(x,y,[2,10])
    r_val = evaluate_models_training(x, y, poly, True)
    
    #testing
    x = list(TESTING_INTERVAL)
    print("Testing interval")
    y = get_cities_averages(data,CITIES,x)
    rmse_values = evaluate_models_testing(x, y, poly, True)
