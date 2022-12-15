import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import datetime

def request_url(url):
    """
    This function serves to request API and follows the structure given by ArtBeat API doc

    Parameter
    ---------
    url = xml input  
    """
    xml_data = requests.get(url).content
    soup = BeautifulSoup(xml_data, features="xml")
    texts = str(soup.findAll(text=True))
    child = soup.find("Event")
    
    Name = []
    Type = []
    Media = []
    Description = []
    Image = []
    Karma = []
    Price = []
    Datestart = []
    Dateend = []
    Permanentevent = []
    Distance = []
    Datum = []
    Latitude = []
    Longitude = []
    Address = []
    Phone = []
    Area = []
    while True:
        try:
            Name.append(child.find('Name').get_text())
        except:
            Name.append(None)

        try:
            Type.append(child.find('Type').get_text())
        except:
            Type.append(None)     

        try:
            mediaList = child.find_all('Media')
            tempMedia =[]
            for i in range(len(mediaList)):
                tempMedia.append(mediaList[i].get_text())
            Media.append(" ".join(tempMedia))
        except:
            Media.append(None)
        
        try:
            Description.append(child.find('Description').get_text())
        except:
            Description.append(None)

        try:
            Image.append(child.find('Image').get_text())
        except:
            Image.append(None)

        try:
            Karma.append(child.find('Karma').get_text())
        except:
            Karma.append(None)
            
        try:
            Price.append(child.find('Price').get_text())
        except:
            Price.append(None)

        try:
            Datestart.append(child.find('DateStart').get_text())
        except:
            Datestart.append(None)
        
        try:
            Dateend.append(child.find('DateEnd').get_text())
        except:
            Dateend.append(None)

        try:
            Permanentevent.append(child.find('PermanentEvent').get_text())
        except:
            Permanentevent.append(None)   

        try:
            Distance.append(child.find('Distance').get_text())
        except:
            Distance.append(None)    

        try:
            Datum.append(child.find('Datum').get_text())
        except:
            Datum.append(None) 

        try:
            Longitude.append(child.find('Longitude').get_text())
        except:
            Longitude.append(None) 

        try:
            Latitude.append(child.find('Latitude').get_text())
        except:
            Latitude.append(None) 

        try:
            Address.append(child.find('Address').get_text())
        except:
            Address.append(None)

        try:
            Area.append(child.find('Area').get_text())
        except:
            Area.append(None)

        try:
            Phone.append(child.find('Phone').get_text())
        except:
            Phone.append(None)        
        try:   
            child = child.find_next_sibling('Event')
        except:
            break
    
    data = []
    data = pd.DataFrame({"Name":Name,
                         "Type":Type,
                         "Media":Media,
                         "Description":Description,
                         "Image":Image, 
                         "Karma":Karma,
                         "Price":Price,
                         "Date Start":Datestart,
                         "Date End":Dateend, 
                         "Datum":Datum,
                         "Longitude":Longitude, 
                         "Latitude":Latitude,
                         "Address":Address,
                         "Area":Area,
                         "Phone":Phone})
    return data

def transform(xml_list):
    """
    This function serves to transform a given list of xml API into a dataframe, without cleaning

    Parameter
    ---------
    xml_list = a list of xml(s)
    """
    temp = pd.DataFrame()
    for i in range(len(xml_list)):
        data = request_url(xml_list[i])
        temp = pd.concat([temp, data], ignore_index = True)
    return temp

def transform_clean(xml_list):
    """
    This function serves to transform a given list of xml API into a dataframe
    and also clean the DataFrame in the following ways:
        1. transform some scripting language into appropriate format
        2. transform variables into appropriate types

    Parameter
    ---------
    xml_list = a list of xml(s)
    
    """
    temp = pd.DataFrame()
    temp_clean = pd.DataFrame()
    for i in range(len(xml_list)):
        data = request_url(xml_list[i])
        temp = pd.concat([temp, data], ignore_index = True)

    temp_clean = temp[temp['Name'].notna()].reset_index() # drop the missing events; if an event doesn't exist, it won't have Name.
    temp_clean = temp_clean.drop("index",axis = 1) # fix index

    for i in range(len(temp_clean["Description"])): # Some descriptions have some scripting language that needs to be fixed for clearer display
        temp_clean.loc[i,"Description"] = re.sub('&quot;','"',temp_clean.loc[i,"Description"])
        temp_clean.loc[i,"Description"] = re.sub('\\r\\n','',temp_clean.loc[i,"Description"])
        temp_clean.loc[i,"Description"] = re.sub('\[Image:.+\]','',temp_clean.loc[i,"Description"])
    
    temp_clean["Date Start"] = pd.to_datetime(temp_clean["Date Start"],errors='coerce')
    temp_clean["Date End"] = pd.to_datetime(temp_clean["Date End"],errors='coerce')
    temp_clean["Karma"] = pd.to_numeric(temp_clean["Karma"],errors='coerce')
    temp_clean["Longitude"] = pd.to_numeric(temp_clean["Longitude"],errors='coerce')
    temp_clean["Latitude"] = pd.to_numeric(temp_clean["Latitude"],errors='coerce')   
    return temp_clean

def get_event_info(df, **kwargs):
    """
    This function serves to get the information of the events that meet the criteria,
    and return a dataframe.

    The function uses up to three case insensitve argument values to filter through 
    the dataframe, and all events that
    match with any argument are included in the new dataset. Duplicates are dropped.

    Parameter
    ---------
    df = a dataframe that follows the structure of the previous settings
    **kwargs can take in three arguments:
    Type, Name, and Media
    """ 
    temp = pd.DataFrame()
    try:
        temp = pd.concat([temp,df[df['Type'].str.contains(kwargs["Type"],case =False)]],ignore_index=True)
    except:
        temp = temp
    try:
        temp = pd.concat([temp,df[df['Name'].str.contains(kwargs["Name"],case =False)]],ignore_index=True)
    except: temp = temp

    try:
        temp = pd.concat([temp,df[df['Media'].str.contains(kwargs["Media"],case =False)]],ignore_index=True)
    except:
         temp = temp
    if temp.empty:
        return temp
    else:
        temp = temp.drop_duplicates()
        return temp

def get_current_event_info(df):
    """
    This function serves to get the information of all the current events as of
    the day of the search and return a dataframe.

    Since all permanent events' Date End is marked as 0000-00-00 in the XML,
    this function first transform these permanent events' Date End to 2030-12-31
    in an attempt to represent the permanent aspect. A date that is too far ahead
    will trigger the out of bounds nanoesecond timestamp error, but the date can 
    be altered to reflect the course of time.

    Parameter
    ---------
    df = a dataframe that follows the structure of the previous settings
    """ 

    d1 = datetime.datetime(2030,12,31,00,00,00) # to fix out of bounds nanosecond timestamp
    d2 = datetime.datetime.today()
    temp = pd.DataFrame()
    df["Date End"] = df["Date End"].fillna(d1)
    temp = pd.concat([temp,df.loc[df['Date End'] > d2]],ignore_index= True)
    return temp
