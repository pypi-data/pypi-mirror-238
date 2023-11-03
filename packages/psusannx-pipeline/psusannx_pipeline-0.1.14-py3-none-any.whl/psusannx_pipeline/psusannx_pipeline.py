from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline
import numpy as np 
import pandas as pd
from category_encoders.cat_boost import CatBoostEncoder
from sklearn.preprocessing import StandardScaler


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Select certain columns from a dataframe for preprocessing"""

    def __init__(self, columns=[]):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X[self.columns]


class CorrectNegPoints(TransformerMixin, BaseEstimator):
    """Any negative league table points in the table will be replaced with zeros"""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()
        
        # Replace any of the negative points (deducted for going into administration) with zero
        X_["Home_team_points"] = np.where(X_.Home_team_points < 0, 0, X_.Home_team_points) 
        X_["Away_team_points"] = np.where(X_.Away_team_points < 0, 0, X_.Away_team_points)
        
        return X_


class BucketFormations(TransformerMixin, BaseEstimator):
    """Bucket infrequent formations (less than cutoff) into their own category called 'other'"""
    
    def __init__(self, cutoff=300):
        self.cutoff = cutoff
    
    def fit(self, X, y=None):
        
        # Get the number of times each formation appears in the data
        home_formations = X.Home_formation.value_counts()
        away_formations = X.Away_formation.value_counts()
        total_formations = (home_formations + away_formations).fillna(1)
        
        # Create a list of all formations that appear less than the cutoff in total
        mapping_list = list(total_formations[total_formations < self.cutoff].index)

        # Map any formation that appears less than the cutoff times in total to 'other'
        formations_dict = {}

        # Loop over all formations that appear less than cutoff times and create a mapping for them
        for i in range(len(mapping_list)):
            formations_dict[mapping_list[i]] = "other"

        # Print out the mapping dictionary
        print(formations_dict)
        
        # Create an attribute of the class
        self.formations_dict = formations_dict
        
        return self
    
    def transform(self, X, y=None):
        
        # Make a copy of the input dataframe
        X_ = X.copy()
        
        # Map all the infrequent formations to 'other'
        X_ = X_.replace(self.formations_dict)
        
        return X_
    

class GetLogRatios(TransformerMixin, BaseEstimator):
    """Get the log ratios between the home team & away team features"""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()
        
        # Replace all zeros with 0.001 to avoid inf and na values when taking logs
        X_ = X_.replace(0, 0.001)
        
        # Get the log of the ratios between some home and away team comparison features
        X_["Log_Goals_for_ratio"] = np.log(X_.Home_team_goals_for / X_.Away_team_goals_for)
        X_["Log_Goals_against_ratio"] = np.log(X_.Home_team_goals_against / X_.Away_team_goals_against)
        X_["Log_Wins_ratio"] = np.log(X_.Home_team_wins / X_.Away_team_wins)
        X_["Log_Losses_ratio"] = np.log(X_.Home_team_loses / X_.Away_team_loses)
        X_["Log_Draws_ratio"] = np.log(X_.Home_team_draws / X_.Away_team_draws)
        X_["Log_Points_ratio"] = np.log(X_.Home_team_points / X_.Away_team_points)
        X_["Log_Form_ratio"] = np.log(X_.Home_form / X_.Away_form)
        X_["Log_League_pos_ratio"] = np.log(X_.Home_league_pos / X_.Away_league_pos)
        X_["Log_Elo_ratio"] = np.log(X_.Home_elo / X_.Away_elo)
        X_["Log_Odds_ratio"] = np.log(X_.Home_odds / X_.Away_odds)
        X_["Log_h2h_recent"] = np.log(X_.H2H_recent_home / X_.H2H_recent_away)
        X_["Log_h2h_exact"] = np.log(X_.H2H_exact_home / X_.H2H_exact_away)
        X_["Log_avg_xg_ratio"] = np.log(X_.Home_avg_xg / X_.Away_avg_xg)
        X_["Log_weighted_avg_xg_ratio"] = np.log(X_.Home_weighted_avg_xg / X_.Away_weighted_avg_xg)
        X_["Log_home_goals_for_against_il5g_ratio"] = np.log(X_.Home_avg_goals_il5g / X_.Home_avg_goals_against_il5g)
        X_["Log_away_goals_for_against_il5g_ratio"] = np.log(X_.Away_avg_goals_il5g / X_.Away_avg_goals_against_il5g)
        
        return X_
    
    
class GetPercentagesAndPerGame(TransformerMixin, BaseEstimator):
    """Calculate the %'s & per game figures for the home & away teams"""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()
        
        # Create the % and per game figures
        X_["Home_team_win_%"] = X_.Home_team_wins / X_.Home_team_played
        X_["Away_team_win_%"] = X_.Away_team_wins / X_.Away_team_played

        X_["Home_team_lose_%"] = X_.Home_team_loses / X_.Home_team_played
        X_["Away_team_lose_%"] = X_.Away_team_loses / X_.Away_team_played

        X_["Home_team_draw_%"] = X_.Home_team_draws / X_.Home_team_played
        X_["Away_team_draw_%"] = X_.Away_team_draws / X_.Away_team_played

        X_["Home_team_points_per_game"] = X_.Home_team_points / X_.Home_team_played
        X_["Away_team_points_per_game"] = X_.Away_team_points / X_.Away_team_played

        X_["Home_team_goals_for_per_game"] = X_.Home_team_goals_for / X_.Home_team_played
        X_["Away_team_goals_for_per_game"] = X_.Away_team_goals_for / X_.Away_team_played

        X_["Home_team_goals_against_per_game"] = X_.Home_team_goals_against / X_.Home_team_played
        X_["Away_team_goals_against_per_game"] = X_.Away_team_goals_against / X_.Away_team_played
        
        return X_
    

class GetDifferences(TransformerMixin, BaseEstimator):
    """Calculate differences between certain features as new features"""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()
        
        # Calculate Goal Difference for both teams 
        X_["Home_goal_diff"] = X_.Home_team_goals_for - X_.Home_team_goals_against
        X_["Away_goal_diff"] = X_.Away_team_goals_for - X_.Away_team_goals_against
        X_["Goal_diff_diff"] = X_.Home_goal_diff - X_.Away_goal_diff

        # Calculate the differences between some variables
        X_["Recent_h2h_diff"] = X_.H2H_recent_home - X_.H2H_recent_away
        X_["Exact_h2h_diff"] = X_.H2H_exact_home - X_.H2H_exact_away
        X_["Win_%_diff"] = X_["Home_team_win_%"] - X_["Away_team_win_%"]
        X_["Lose_%_diff"] = X_["Home_team_lose_%"] - X_["Away_team_lose_%"]
        X_["Draw_%_diff"] = X_["Home_team_draw_%"] - X_["Away_team_draw_%"]
        X_["Points_per_game_diff"] = X_.Home_team_points_per_game - X_.Away_team_points_per_game
        X_["Goals_for_per_game_diff"] = X_.Home_team_goals_for_per_game - X_.Away_team_goals_for_per_game
        X_["Goals_against_per_game_diff"] = X_.Home_team_goals_against_per_game - X_.Away_team_goals_against_per_game
        X_["Elo_diff"] = X_.Home_elo - X_.Away_elo
        X_["Elo_prob_diff"] = X_.Home_elo_prob - X_.Away_elo_prob
        X_["Odds_diff"] = X_.Home_odds - X_.Away_odds
        
        return X_


class CatboostEncodeFormations(TransformerMixin, BaseEstimator):
    """Encode formation values with the catboost encoder"""

    def __init__(self):

        # Instantiate the encoder along with the class
        self.encoder = CatBoostEncoder() 

    def fit(self, X, y=None):
        """Make sure X is a dataframe and y is a series for this to work"""

        # Fit the encoder to the data
        self.encoder.fit(X[["Home_formation", "Away_formation"]], X.Result.map({"Home":0, "Draw":1, "Away":2}))

        return self

    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()

        # Replace the formation columns with the encoded data
        X_[["Home_formation", "Away_formation"]] = self.encoder.transform(X_[["Home_formation", "Away_formation"]])

        return X_


class DropFeatures(TransformerMixin, BaseEstimator):
    """Drop certain features that should not be used in modelling"""

    def __init__(self, feature_list=[]):

        self.feature_list = feature_list

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()

        # Drop the features in feature_list
        X_ = X_.drop(columns = self.feature_list, errors="ignore")

        return X_ 


class CustomScaler(TransformerMixin, BaseEstimator):
    """Apply the scikit-learn standard scaler transformer but return the values in a dataframe"""

    def __init__(self, feature_list=[]):

        # Instantiate the standard scaler
        self.scaler = StandardScaler()

        # Store the feature_list as a class attribute
        self.feature_list = feature_list

    def fit(self, X, y=None):

        # Fit the scaler to the data
        self.scaler.fit(X[self.feature_list])

        return self

    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()

        # Standardise the columns but keep the dataframe object
        X_[self.feature_list] = pd.DataFrame(self.scaler.transform(X_[self.feature_list]), columns=self.feature_list)

        return X_
    

class FillNA(TransformerMixin, BaseEstimator):
    """Fill any missing values with zeros"""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        # Create a copy of the input dataframe
        X_ = X.copy()
        
        # Replace any of the null values with 0
        X_ = X_.fillna(0)
        
        return X_


########## LINEUP MODEL PIPELINE ##########

# Set up a list of columns to select for the lineup model pipeline
lineup_model_cols = [
    "Result", # Needed for catboost encoders but not for predictions
    "Home_odds", "Draw_odds", "Away_odds",
    "Home_formation",
    "Home_GK", 
    "Home_LWB", "Home_LB", "Home_CB1", "Home_CB2", "Home_CB3", "Home_RB", "Home_RWB", 
    "Home_CDM1", "Home_CDM2", "Home_LM", "Home_CM1", "Home_CM2", "Home_CM3", "Home_RM", "Home_CAM1", "Home_CAM2", "Home_CAM3", 
    "Home_LW", "Home_ST1", "Home_ST2", "Home_RW",
    "Home_sub_1", "Home_sub_2", "Home_sub_3", "Home_sub_4", "Home_sub_5", "Home_sub_6", "Home_sub_7", "Home_sub_8", "Home_sub_9",

    "Away_formation",
    "Away_GK", 
    "Away_LWB", "Away_LB", "Away_CB1", "Away_CB2", "Away_CB3", "Away_RB", "Away_RWB", 
    "Away_CDM1", "Away_CDM2", "Away_LM", "Away_CM1", "Away_CM2", "Away_CM3", "Away_RM", "Away_CAM1", "Away_CAM2", "Away_CAM3",
    "Away_LW", "Away_ST1", "Away_ST2", "Away_RW",
    "Away_sub_1", "Away_sub_2", "Away_sub_3", "Away_sub_4", "Away_sub_5", "Away_sub_6", "Away_sub_7", "Away_sub_8", "Away_sub_9"
]

# Set up a list of columns to scale for the lineup model pipeline
lineup_model_cols_to_scale = [
    "Home_odds", "Draw_odds", "Away_odds",
    "Home_formation",
    "Home_GK", 
    "Home_LWB", "Home_LB", "Home_CB1", "Home_CB2", "Home_CB3", "Home_RB", "Home_RWB", 
    "Home_CDM1", "Home_CDM2", "Home_LM", "Home_CM1", "Home_CM2", "Home_CM3", "Home_RM", "Home_CAM1", "Home_CAM2", "Home_CAM3", 
    "Home_LW", "Home_ST1", "Home_ST2", "Home_RW",
    "Home_sub_1", "Home_sub_2", "Home_sub_3", "Home_sub_4", "Home_sub_5", "Home_sub_6", "Home_sub_7", "Home_sub_8", "Home_sub_9",

    "Away_formation",
    "Away_GK", 
    "Away_LWB", "Away_LB", "Away_CB1", "Away_CB2", "Away_CB3", "Away_RB", "Away_RWB", 
    "Away_CDM1", "Away_CDM2", "Away_LM", "Away_CM1", "Away_CM2", "Away_CM3", "Away_RM", "Away_CAM1", "Away_CAM2", "Away_CAM3",
    "Away_LW", "Away_ST1", "Away_ST2", "Away_RW",
    "Away_sub_1", "Away_sub_2", "Away_sub_3", "Away_sub_4", "Away_sub_5", "Away_sub_6", "Away_sub_7", "Away_sub_8", "Away_sub_9"
]

# Setup a list of columns to drop from the data for the lineup model pipeline
lineup_model_cols_to_drop = [
    "Result"
]

# Create the preprocessing pipeline object for the lineup model
lineup_model_pipeline = Pipeline(steps = [

    ("Select the columns we want for the lineup model", ColumnSelector(lineup_model_cols)),
    
    ("Bucket the Infrequent Formations", BucketFormations(cutoff=100)),

    ("Encode Formations", CatboostEncodeFormations()),

    ("Drop features not used in modelling", DropFeatures(lineup_model_cols_to_drop)),

    ("Standardize all columns", CustomScaler(lineup_model_cols_to_scale)),
    
    ("Fill in missing values with 0", FillNA())
    
])


########## FINAL MODEL PIPELINE ##########

# Set up a list of columns to select for the final model pipeline
final_model_cols = [
    "Result",
    "Home_formation", "Away_formation",
    "Home_form", "Away_form",
    "Home_home_form", "Away_away_form",
    "Home_rolling_form", "Away_rolling_form",
    "Home_location_rolling_form", "Away_location_rolling_form",

    "Home_team_played", "Away_team_played",
    "Home_league_pos", "Away_league_pos",
    "Home_team_wins", "Away_team_wins",
    "Home_team_draws", "Away_team_draws",
    "Home_team_loses", "Away_team_loses",
    "Home_team_goals_for", "Away_team_goals_for",
    "Home_avg_goals_il5g", "Away_avg_goals_il5g",
    "Home_team_goals_against", "Away_team_goals_against",
    "Home_avg_goals_against_il5g", "Away_avg_goals_against_il5g",
    "Home_team_points", "Away_team_points",

    "H2H_recent_home", "H2H_recent_draw", "H2H_recent_away", "H2H_recent_goal_diff",
    "H2H_exact_home", "H2H_exact_draw", "H2H_exact_away", "H2H_exact_goal_diff",
    
    "Home_elo", "Away_elo",
    "Home_elo_prob", "Away_elo_prob",
    "Home_avg_xg", "Away_avg_xg",
    "Home_weighted_avg_xg", "Away_weighted_avg_xg",
    
    "Home_odds",
    "Draw_odds",
    "Away_odds",

    "Home_nn_prob", 
    "Draw_nn_prob", 
    "Away_nn_prob", 
    "NN_prob_diff"
]

# Set up a list of columns to scale in the final model pipeline
final_model_cols_to_scale = [

    "Home_formation", "Away_formation",
    "Home_form", "Away_form",
    "Home_home_form", "Away_away_form",
    "Home_rolling_form", "Away_rolling_form",
    "Home_location_rolling_form", "Away_location_rolling_form",

    "Home_team_played", "Away_team_played",
    "Home_league_pos", "Away_league_pos",
    "Home_team_wins", "Away_team_wins",
    "Home_team_draws", "Away_team_draws",
    "Home_team_loses", "Away_team_loses",
    "Home_team_goals_for", "Away_team_goals_for",
    "Home_avg_goals_il5g", "Away_avg_goals_il5g",
    "Home_team_goals_against", "Away_team_goals_against",
    "Home_avg_goals_against_il5g", "Away_avg_goals_against_il5g",
    "Home_team_points", "Away_team_points",

    "H2H_recent_home", "H2H_recent_draw", "H2H_recent_away", "H2H_recent_goal_diff",
    "H2H_exact_home", "H2H_exact_draw", "H2H_exact_away", "H2H_exact_goal_diff",
    
    "Home_elo", "Away_elo",
    "Home_elo_prob", "Away_elo_prob",
    "Home_avg_xg", "Away_avg_xg",
    "Home_weighted_avg_xg", "Away_weighted_avg_xg",
    
    "Home_odds",
    "Draw_odds",
    "Away_odds",

    "Home_nn_prob", 
    "Draw_nn_prob", 
    "Away_nn_prob", 
    "NN_prob_diff",
    
    "Log_Goals_for_ratio", 
    "Log_Goals_against_ratio", 
    "Log_Wins_ratio", 
    "Log_Losses_ratio", 
    "Log_Draws_ratio", 
    "Log_Points_ratio", 
    "Log_League_pos_ratio",
    "Log_home_goals_for_against_il5g_ratio", 
    "Log_away_goals_for_against_il5g_ratio",
    "Home_goal_diff", 
    "Away_goal_diff", 
    "Goal_diff_diff",
    "Log_Form_ratio",
    "Log_Elo_ratio", 
    "Log_Odds_ratio",
    "Log_avg_xg_ratio", 
    "Log_weighted_avg_xg_ratio",
    "Log_h2h_recent", 
    "Log_h2h_exact", 
    "Recent_h2h_diff", 
    "Exact_h2h_diff", 
    "Elo_diff", 
    "Odds_diff",
    "Points_per_game_diff", 
    "Goals_for_per_game_diff", 
    "Goals_against_per_game_diff"
]


final_model_cols_to_drop = [
    "Result"
]


# Create the preprocessing pipeline object for the final model
final_model_pipeline = Pipeline(steps = [

    ("Select the columns we want for the final model", ColumnSelector(final_model_cols)),
    
    ("Correct Negative Points", CorrectNegPoints()),
    
    ("Bucket the Infrequent Formations", BucketFormations(cutoff=250)),
    
    ("Get the Log Ratios of Some Features", GetLogRatios()),
    
    ("Get Percentages & Per Game Figures", GetPercentagesAndPerGame()),
    
    ("Get Home/Away Differences", GetDifferences()),

    ("Encode Formations", CatboostEncodeFormations()),

    ("Drop features not used in modelling", DropFeatures(final_model_cols_to_drop)),
    
    ("Standardize all columns", CustomScaler(final_model_cols_to_scale))
    
])