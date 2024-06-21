for row in archive.iterrows():
    try:
        decision_variables = [row[attr] for attr in problem.parameter_names]
    except AttributeError:
        print('errpr')


