import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from models.performance import Performance
from models.session import Session

class Normalization(object):

    #
    # Calculates 
    #
    def calculate_quantiles(self, user_key: str) -> float:

        # Defines weights with which tie
        weights: [float] = [-0.25, -0.25, -0.25, -0.25, -1, 1, 1, 1,]
        
        # Gets all performances achieved so far.
        df: pd.core.frame.DataFrame = Database().get_performances()

        # If no data is recorded yet, the user will be put
        # by default in a middle difficulty class.
        if df.empty is True: return 'class_03'
        
        # Calculates the average performance 
        df: pd.core.frame.DataFrame = self.choose_first_performance(df)

        df: pd.core.frame.DataFrame = self.normalize_performances(df)

        skill_scores = (
            
            weights[0] * df['gaps'] +
            weights[1] * df['op_1'] +
            weights[2] * df['op_2'] +
            weights[3] * df['op_3'] +
            weights[4] * df['time'] +
            weights[5] * df['score'] +
            weights[6] * df['progress'] +
            weights[7] * df['difficulty']

        )

        quintile1: str = np.percentile(skill_scores, 20)
        quintile2: str = np.percentile(skill_scores, 40)
        quintile3: str = np.percentile(skill_scores, 60)
        quintile4: str = np.percentile(skill_scores, 80)
        quintile5: str = np.percentile(skill_scores, 100)

        columns: [str] = ['difficulty_class']

        # Defines a new dataframe intended to store 
        # the difficulty class in which a user is
        # sorted in.
        df = pd.DataFrame(columns=columns).astype(float)

        difficulty_class: str = 'class_03'

        # Iterates over all elements of the skill_scores
        # dataframe.
        for index, score in enumerate(skill_scores):

            if (score <= quintile1):   difficulty_class = 'class_01'
            elif (score <= quintile2): difficulty_class = 'class_02'
            elif (score <= quintile3): difficulty_class = 'class_03'
            elif (score <= quintile4): difficulty_class = 'class_04'
            elif (score <= quintile5): difficulty_class = 'class_05'
            
            df = df.append(pd.DataFrame([difficulty_class], columns=columns, index=[skill_scores.index.values[index]]))

        return df.loc[user_key]['difficulty_class']
    
    #
    #
    #
    def normalize_performances(self, input: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:

        # Checks whether the input dataframe is empty.
        # If that is the case, the empty input dataframe
        # gets returned.
        if input.empty is True: return input

        # Defines the column descriptions for the dataframe that
        # is meant to be returned.
        columns: [str] = ['gaps', 'op_1', 'op_2', 'op_3', 'score', 'time', 'progress', 'difficulty']

        # Creates an empty dataframe intended to hold normalized
        # performance values. 
        df = pd.DataFrame(columns=columns).astype(float)
        
        # Checks whether only one value is stored in the input
        # dataframe.
        if len(input) is 1:

            # Converts the entries of the dataframe to a list.
            a = np.array(input.values.tolist())
            
            # Replaces all values that are greater than 1 by 1.
            normalized_performance = np.where(a > 1, 1, a).tolist()

            # The normalized performance is written to the output
            # dataframe.
            df = pd.DataFrame(normalized_performance, columns=columns, index=[input.iloc[0].name])

        else:
            
            # Writes the input dataframe to the output dataframe.
            df = input

            # Substracts the minimum column values from the dataframe.
            df -= input.min()

            # Divides by the max of of the columns.
            df /= df.max()

            # Since there is chance that the maximum of a column might
            # be zero for an extremely small dataset, NaN values are replaced
            # by zeros.
            df = df.fillna(0)

        # Returns a normalized dataframe.
        return df
        
    # 
    # Chooses the first performances achieved by
    # participants.
    #
    def choose_first_performance(self, input: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        
        # Returns an empty dataframe if the input dataframe 
        # does not contain any entries.
        if input.empty is True: return input

        # Defines the column descriptions for the dataframe that
        # is meant to be returned.
        columns: [str] = ['gaps', 'op_1', 'op_2', 'op_3', 'score', 'time', 'progress', 'difficulty']

        # Defines an empty dataframe intended to hold the
        # average performances of all users.
        df = pd.DataFrame(columns=columns).astype(float)

        # Assigns the index of the first row of the input
        # dataframe which refers to the user key of the user.
        current_user: str = ''

        # Iterates over the entire input dataframe.
        for index, values in enumerate(np.array(input)):

            # Checks whether the current row belongs to
            # the user stored in the current_user variable.
            if current_user != input.iloc[index].name:

                # Pushes the row of the current iteration
                # of the loop on the temporary dataframe.
                df = df.append(pd.DataFrame([values], columns=columns, index=[input.iloc[index].name]))

                current_user = input.iloc[index].name

        # Returns the average performance across all users.
        return df

if __name__ == "__main__":

    db = Database()
    n = Normalization()
    
    input = db.get_performances()
    input = n.choose_first_performance(input)

    df = n.calculate_quantiles('user_016')
