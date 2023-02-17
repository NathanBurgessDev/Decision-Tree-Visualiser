from model_settings.classifiers.DecisionTreeClassifierSettings import DecisionTreeClassifierSettings
from model_settings.ClassifierSettings import ClassifierSettings

class ClassifierSettingsFactory():

    def Factory(classifier):
        settings = {
            "Decision Tree Classifier" : DecisionTreeClassifierSettings,
            "Gradient Boosted Classifier" : ClassifierSettings,
            None : ClassifierSettings
        }
        return settings[classifier]()