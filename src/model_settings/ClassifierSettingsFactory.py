from model_settings.classifiers.DecisionTreeClassifierSettings import DecisionTreeClassifierSettings
from model_settings.ClassifierSettings import ClassifierSettings


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Using the factory method, this class will return the
correct settings object determined by the classifier type.


Note : Settings for gradient boosted are not currently implemented hence
returning 'ClassifierSettings'

"""
class ClassifierSettingsFactory():

    def Factory(classifier):
        settings = {
            "Decision Tree Classifier" : DecisionTreeClassifierSettings,
            "Gradient Boosted Classifier" : ClassifierSettings,
            None : ClassifierSettings
        }
        return settings[classifier]()