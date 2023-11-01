import pandas as pd, requests, os

class globalmartAPI:
    def __init__(self, endpoint, base_url=None, header=None):
        self.base_url = base_url
        self.endpoint = endpoint
        self.headers = header
    
    def getrecords(self, no_of_records=100, limit=30, offset=0):
        final_data = []
        offset=0
        # params = {"offset": offset, "limit": limit}
        while no_of_records!=0:
            if no_of_records<limit:
                response = requests.get(self.base_url+self.endpoint+f'?offset={offset}&limit={no_of_records}', headers=self.headers)
                response_data = response.json() 
                final_data.extend(response['data']) 
                return final_data
            
            response = requests.get(self.base_url+self.endpoint+f'?offset={offset}&limit={limit}', headers=self.headers)
            response_data = response.json() 
            next_endpoint = response_data['next']
            params= next_endpoint.split('&')[0].split('=')[1]
            final_data.extend(response_data['data'])
            no_of_records = no_of_records - limit
        
        return final_data
                
        
    def json_to_df(self, json_inp):
        df = pd.json_normalize(json_inp)
        cleaned_col_names = [x if(len(x.split('.')) == 1) else x.split('.')[-1] for x in df.columns]
        df_columns = cleaned_col_names
        return df 
    
class Order:
    def __init__(self, df) -> None:
        self.df =df
    def calculate_total( self, order_id):
        return self.df[self.df["order_id"] == order_id]["sales_amt"].sum().round(2)
    

class Order_discount(Order):
    def __init__(self, df) -> None:
        super().__init__(df)
        
    def calculate_total( self, order_id):
        self.df = self.df.assign(
            sales_amount_updated = lambda x: x["sales_amt"]*(1-x["discount"])
        )
        filtered_df = self.df[self.df["order_id"]==order_id]
        return filtered_df[self.df["sales_amount_updated"]].sum().round(2)
    


