import pandas as pd
import __main__ as main
from multiprocessing.pool import ThreadPool
import numpy as np
import pickle
if not hasattr(main, '__file__'):
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm
class reconcilliation:
    def __init__(self,source_filepath:str,destination_filepath:str,fields_to_reconcile:list, source_delimiter=",",destination_delimiter=","):
        """Reconcile two csv files based on a list of fields

        Args:
            source_filepath (str): path to the source csv file
            destination_filepath (str): path to the destination csv file
            fields_to_reconcile (list): list of fields to reconcile, the first field in the list is the primary key
        """
        self.threads = 50
        self.source_filepath = source_filepath
        self.destination_filepath = destination_filepath
        self.fields_to_reconcile = fields_to_reconcile
        src = pd.read_csv(source_filepath,delimiter=source_delimiter)
        self.source_df = src
        dst = pd.read_csv(destination_filepath,delimiter=destination_delimiter)
        self.destination_df = dst
        self.reconcile()
        self.missing = pd.DataFrame(columns=self.source_df.columns)
        

    def reconcile(self,source_field_include=[],destination_field_include=[]):
        """Reconcile the source and destination csv files, creating a new dataframe with the reconciled data, 
        the new dataframe will have every other row be the source field and the destination field
        defines a count for number of exact matches from the source to the destination and the number or partial and exact matches
        """
        # create self.reconciled_df, every other column should be re-labled to source_FIELDNAME, destination_FIELDNAME,source_FIELDNAME2, destination_FIELDNAME2 ect.
        new_column_names = []
        self.matched_count = 0
        self.partial_count = 0
        self.missing_count = 0
        # merge dataframes based on the first field in the fields_to_reconcile list
        self.reconciled_df = pd.merge(self.source_df,self.destination_df,on=self.fields_to_reconcile[0],how="outer",indicator=True,suffixes=("","_destination"),)
        #add match_type as column
        self.reconciled_df["match_type"] = ""
        #compare fields in the fields_to_reconcile list, if they match set the match_type to exact, if they do not match set the match_type to partial
        for field in self.fields_to_reconcile[1:]:
            self.reconciled_df[field+"_is_match"] = np.where((self.reconciled_df[field] == self.reconciled_df[field+"_destination"]) and (self.reconciled_df["_merge"] == "both"),True,False)
            # self.reconciled_df[(self.reconciled_df[field] != self.reconciled_df[field+"_destination"]) and (self.reconciled_df["_merge"] == "both")]["match_type"] = "partial"
        
        #if all existing _is_match columns are True and the _merge column is both, set the match_type to exact
        #if any existing _is_match columns are False and the _merge column is both, set the match_type to partial
        self.reconciled_df.loc[(self.reconciled_df["_merge"] == "both") & (self.reconciled_df[[field+"_is_match" for field in self.fields_to_reconcile[1:]]].all(axis=1)),"match_type"] = "exact"
        self.reconciled_df.loc[(self.reconciled_df["_merge"] == "both") & (self.reconciled_df[[field+"_is_match" for field in self.fields_to_reconcile[1:]]].any(axis=1)),"match_type"] = "partial"
        #if the _merge column is left_only, set the match_type to missing
        self.reconciled_df.loc[self.reconciled_df["_merge"] == "left_only","match_type"] = "missing"

    def pickle_me(self,filepath):
        """pickle the reconciled dataframe

        Args:
            filepath (str): filepath to pickle the reconcilliation object
        """
        if filepath[-4:] != ".pkl":
            filepath = filepath+".pkl"
        with open(filepath,"wb") as f:
            pickle.dump(self,f)

    def _compare_row(self,row):
        """Compare a row from the reconciled dataframe

        Args:
            row (pandas.Series): row from the reconciled dataframe

        Returns:
            bool: True if the rows match, False if they do not
        """
        for field in self.fields_to_reconcile[1:]:
            source_field = field+"_source"
            destination_field = field+"_destination"
            if row[source_field] != row[destination_field]:
                return False
        return True
        
    def preview(self):
        """Preview the reconciled dataframe
        """
        return self.reconciled_df.head()

