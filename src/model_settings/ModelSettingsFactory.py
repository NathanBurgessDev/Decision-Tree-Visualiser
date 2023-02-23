from model_settings.classifiers.DecisionTreeClassifierSettings import DecisionTreeClassifierSettings
from model_settings.classifiers.GradientBoostingClassifierSettings import GradientBoostingClassifierSettings
from model_settings.regressors.DecisionTreeRegressorSettings import DecisionTreeRegressorSettings
from model_settings.regressors.GradientBoostingRegressorSettings import GradientBoostingRegressorSettings
from model_settings.regressors.RandomForestRegressorSettings import RandomForestRegressorSettings
from model_settings.classifiers.RandomForestClassifierSettings import RandomForestClassifierSettings
from model_settings.classifiers.SVMClassifierSettings import SVMClassifierSettings
from model_settings.regressors.SVMRegressorSettings import SVMRegressorSettings

from model_settings.ModelSettings import ClassifierSettings


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
            "Decision Tree Regressor" : DecisionTreeRegressorSettings,
            "Gradient Boosted Classifier" : GradientBoostingClassifierSettings,
            "Gradient Boosted Regressor" : GradientBoostingRegressorSettings,
            "Random Forest Classifier" : RandomForestClassifierSettings,
            "Random Forest Regressor" : RandomForestRegressorSettings,
            "SVM Classifier" : SVMClassifierSettings,
            "SVM Regressor" : SVMRegressorSettings,
            None : ClassifierSettings
        }
        return settings[classifier]()