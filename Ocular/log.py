import pandas

def logger(logData):

    dictionary = {}
    dictionary['name'] = [logData[0]]
    dictionary['age'] = [logData[1]]
    dictionary['sex'] = [logData[2]]
    dictionary['email'] = [logData[3]]
    dictionary['pass1'] = [logData[4]]

    df = pandas.DataFrame(dictionary, columns= ['name', 'age', 'sex', 'email', 'pass1'])

    df.to_csv (r'log.csv', header=True)
