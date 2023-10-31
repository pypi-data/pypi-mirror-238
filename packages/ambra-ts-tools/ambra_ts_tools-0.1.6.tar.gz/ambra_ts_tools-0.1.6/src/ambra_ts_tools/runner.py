import requests
import pickle
import pandas as pd
import json
import time 
import re 
import importlib
from ambra_ts_tools.Ambra_Clone.V2.ambra_environment import ambra_environment
import __main__ as main
if not hasattr(main, '__file__'):
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm
"""
Template CSV runner -- example here is for a study/sync api call. study_id parameter uses the uuid column of the csv file specified by the user
User input can be caputured by setting a variable = input("prompt: ")
"""
class runner:
    def __init__(self,url,sid,endpoint,reader_data:pd.DataFrame,params={"uuid":"{uuid}"},delimiter=",",threads=30):
        self.url = url
        self.sid = sid
        self.endpoint = endpoint
        # self.csv_file = csv_file
        self.params = params
        self.failed_df = pd.DataFrame(columns=reader_data.columns)
        self.reader_data = reader_data
        self.failed_df = pd.DataFrame(columns=self.reader_data.columns)
        self.failed_df['reason'] = ""
        self.thread_count = threads
        self.responses = []
        self.env = ambra_environment(sid,url)
        self.prep_requests()

    def prep_requests(self,df=None):
        self.reqs = []
        if df == None:
            df = self.reader_data
        pbar = tqdm(df.iterrows(),total=len(df))
        pbar.set_description("loading file")
        for i, csv_row in pbar:
            if self.endpoint == "/bundle": 
                bundle_reqs = []
                if isinstance(self.params,list):
                    for req in self.params:
                        r = {}
                        for k,v in req.items():
                            if isinstance(v,str):
                                r[k] = self.make_replacements(v,csv_row,re.findall('((?<!\{)\{(?!\{){1}[^}]+\})',v))
                            else:
                                r[k] = v
                        r['sid'] = self.sid
                        bundle_reqs.append(r)
                    self.reqs.append(json.dumps(bundle_reqs))
                    # response = self.send_requests_bundle(reqs)
                    # self.responses.append(response)
                else:
                    print("params must be a list of dictionaries when using the bundle endpoint")
                    raise "params must be a list of dictionaries when using the bundle endpoint"
            else:
                req = self.create_request(csv_row)
                self.reqs.append(req)
    def preview_data(self):
        pd.DataFrame(self.reqs).head()

    def run(self):
        self.success_count = 0
        self.failed_count = 0

        self.responses = self.env.multiprocess_ambra_request(self.reqs,endpoint=self.endpoint,pbar=True,threads=self.thread_count)
        # self._handle_responses(self.reqs)
        # self.summarize_responses()
    def run_sample(self):
        sample_data = self.reqs[:5]
        response = []
        for row in sample_data:
            print("request: ",row)
            response = self.env.handle_ambra_request(self.endpoint,row)
            print("response: ", response,"\n")
                
    def make_replacements(self,v,csv_row,tokens_to_replace):
        for token in tokens_to_replace:
            csv_fieldname = token.replace("{","").replace("}","")
            if csv_fieldname in csv_row:
                replace_value = str(csv_row[csv_fieldname])
                v =  v.replace(token,replace_value)
            else:
                print(token + " not found in csv")
        return v
    def create_request(self,csv_row):
        req = {
                'URL':self.endpoint,
                "sid":self.sid,
            }
        for k in self.params:
            replace_value = None
            v = self.params[k]
            tokens_to_replace = re.findall('((?<!\{)\{(?!\{){1}[^}]+\})',v)
            if len(tokens_to_replace) == 0:
                req[k] = v
            else:
                req[k] = self.make_replacements(v,csv_row,tokens_to_replace)
        return req

    def _handle_responses(self,reqs,response=None):
        if response == None:
            response = self.responses
        for ind, r in enumerate(response):
            if len(r)>2 and r[0]=="{" and r[-1]=="}":
                r = json.loads(r)
                # sort dictionary by key
                r = {k: r[k] for k in sorted(r)}
            elif len(r)>2 and r[0]=="[" and r[-1]=="]":
                r = json.loads(r)
                r = [ {k: i[k] for k in sorted(i)} for i in r]
            if isinstance(r,list):
                for res in r: 
                    if res.get('status') != "OK":             
                        failed_study = self.reader_data.iloc[[ind]].to_dict('records')[0]
                        failed_study['reason'] = str(res)
                        self.failed_count+=1
                        self.failed_df = self.failed_df.append(failed_study,ignore_index=True)
                        break
                self.success_count+=1
            elif not isinstance(r,str) and r.get('status') != "OK":
                self.failed_count+=1
                failed_study = self.reader_data.iloc[[ind]].copy()
                failed_study['reason'] = str(r)
                self.failed_df = self.failed_df.append(failed_study,ignore_index=True)
            else:
                self.success_count+=1
        return self.responses
    
    def summarize_responses(self):
        #print a success and failure count. Failures are counted from the failed_df dataframe. Su
        print("successes: ", self.success_count)
        print("failures: ", self.failed_count)
        print("distinct errors: ")
        #print distinct values in self.failed_df['reason'] 
        print(self.failed_df['reason'].unique())

    def output_responses_to_csv(self,filename):
        pd.DataFrame(self.responses).to_csv(filename)
    def output_failed_to_csv(self,filename):
        self.failed_df.to_csv(filename)
    def rerun_failed(self):
        self.prep_requests(self.failed_df)
        self.run()
    def pickle_me(self,filepath):
        #pickle self
        if filepath[-4:] != ".pkl":
            filepath = filepath+".pkl"
        with open(filepath,"wb") as f:
            pickle.dump(self,f)
    