from gettext import _current_domain
from IPython.display import HTML
from _codecs import encode
from html import escape
from pandas.io.common import _is_url
import string
# coding: utf-8

# In[4]:

def get_csv(_from,_to,_datetime,_pax,_currency):
        import json
        import numpy as np
        import urllib.request as urllib
        import pandas as pd
        import time
        from skyscanner.skyscanner import Flights
        # live exchange rates
        forex=urllib.urlopen("http://api.fixer.io/latest").read().decode('utf-8')
        forex=json.loads(forex)

        pref_cur=_currency

        #api keys
        key1= 'yu127659046789830628689581357894'
        key2= 'prtl6749387986743898559646983194'
        key3= 'nt715939468423055307709599462293'
        key4= 'yu264122863541578255073284413510'
        key5= 'yu216224472936393022503819569049'
        key6= 'yu989879633228513818405823595252'


        #country code,currency,language

        params=[['UK','GBP','en-GB'],['SG','SGD','en-SG'],['MY','MYR','ms-MY'],['ID','IDR','id-ID'],['BR','BRL','pt-BR'],['MX','MXN','es-MX'],['US','USD','en-US']]      
        params=params[0:3]
        count_key=0
        count=0
        for param in params:  
            if count_key<5:
                api_key=key1
            elif count_key<10:
                api_key=key2
            elif count_key<15:
                api_key=key3
            elif count_key==15:
                count_key=0
            elif count_key<20:
                api_key=key4
            elif count_key<25:
                api_key=key5
            elif count_key<30:
                api_key=key6
            elif count_key==30:
                count_key=0
            flights_service = Flights(api_key)
            result = flights_service.get_result(
            country=param[0],
            currency=param[1],
            locale=param[2],
            originplace=_from+'-sky',    
            destinationplace=_to + '-sky',
            outbounddate=_datetime,
            inbounddate='',
            adults=int(_pax)).parsed
            if result is None :
                break
            #time.sleep(2)
            cnames=['Carriers','Country','Arrival','Departure','Duration(mins)','Number of stops','Price','Price (Original Currency)','Book']
            
            for x in result['Itineraries']:
            
                out_id=x['OutboundLegId']
                x1=x['PricingOptions']
                for x2 in x1:
                    price_orig=float(x2['Price'])
                    price=x2['Price']/forex['rates'][param[1]]*forex['rates'][pref_cur]
                    dl=x2['DeeplinkUrl']
            #print(price)
                for r in result['Legs']:
                    if r['Id']==out_id: 
                        arrival=r['Arrival']
                        departure=r['Departure']
                        duration=r['Duration']
                        num_stops=len(r['Stops'])
                        carriers=[]
                        for i in r['FlightNumbers']:
                            for c in result['Carriers']:
                                if c['Id']==i['CarrierId']:
                                    carriers.append(c['Name'])
                if count==0:                    
                    df=pd.DataFrame([[carriers,param[0],arrival,departure,duration,num_stops,price,"{0}".format(price_orig),dl]],columns=cnames)
                    
                else :
                    df1=pd.DataFrame([[carriers,param[0],arrival,departure,duration,num_stops,price,"{0}".format(price_orig),dl]],columns=cnames)
                    frames=[df,df1]
                    df=pd.concat(frames)
            count=count+1
            count_key=count_key+1
        
        pd.options.display.max_colwidth = 1000
        data=df.sort_values(by='Price')
        #data.to_csv('fareresultsnew.csv',index = False)
        """df['DeeplinkUrl'] = "<a href=\""+data['DeeplinkUrl']+"\">Click here to Book</a>"""
        HTML(data.to_html('./templates/Results.html',index = False))
        
# 

