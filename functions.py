#!/usr/bin/env python
# coding: utf-8

# # Functions (SharkAttacks_dataset)

# In[4]:


import pandas as pd

def categorize_injury(df):
    
    """Function that categorize the type of injury and returns
    the dataframe with a new column called injury_category"""
    
    def categorize_single_injury(injury):  
        if isinstance(injury, str):
            lower_injury = injury.lower()
            if any(word in lower_injury for word in ['bitten', 'severe injuries', 
                                                     'multiple injuries','severe injurys',
                                                     'severe injury', 'severe']):
                return 'Severe'
            elif 'fatal' in lower_injury or 'remains' in lower_injury:
                return 'Fatal'
            elif any(word in lower_injury for word in ['lacerations','minor injury', 'no injury', 'injury']):
                return 'Minor/No Injury'
            else:
                return 'Unknown'
        else:
            return 'Unknown'
    
    df['injury_category'] = df['injury'].apply(categorize_injury)
    
    return df

def rename_col(columns):
    return columns.lower().replace(" ", "_")

def filtering_australia_2000(df):
    """ To filter the  dataframe to only include rows where country Australia and year > 2000"""
  
    df = df[df['country'] == 'AUSTRALIA']
    condition = df["year"] > 2000
    df = df[condition]
    df.reset_index(drop=True, inplace=True)
    
    return df

def drop_columns(df):
    df.dropna(how='all')
    df = df.drop(['unnamed:_21', 'unnamed:_22', 
                  'case_number', 'case_number.1','href',
                  'href_formula', 'pdf', 'original_order', 
                  "unnamed:_11"], axis=1)
    return df

def clean_activity(df):
   
    """Clean the "activity" column in DataFrame by categorizing activities and labeling others as 'other_activities'."""
    
    df["activity"].fillna("Invalid", inplace=True)
    df["activity"] = df["activity"].str.lower().str.replace(' ', '_')
    
    activity_keywords = {
        "fishing": "fishing",
        "swimming": "swimm",
        "surfing": "surf",
        "snorkeling": "snorkeling",
        "diving": "diving",
        "kayaking": "kayaking"}
    
    # Apply categorization
    for activity, keyword in activity_keywords.items():
        df["activity"] = df["activity"].apply(lambda x: activity if isinstance(x, str) and keyword in x else x)

    # Define keywords to be excluded in 'other_activities'
    keywords = ["fishing", "swimming", "surfing", "snorkeling", "diving", "kayaking"]

    # Apply 'other_activities' label to entries not containing the keywords
    df["activity"] = df["activity"].apply(lambda x: "other_activities" if isinstance(x, str) and not any(keyword in x for keyword in keywords) else x)
   
    return df


def clean_attack_type(df):

    mapping = {"unconfirmed" : "Unprovoked",
               "Unverified" : "Unprovoked",
               "?" : "Unprovoked" ,
               "Unconfirmed"  : "Unprovoked",
               " Provoked" : "Provoked",
               "Boat" : "Watercraft",
               "Under investigation" : "Invalid",
               "Questionable" : "Invalid"}

    df["type"] = df['type'].replace(mapping)
    
    return df

def clean_injury(injury):
    
    if isinstance(injury, str):
        if any(word in injury.lower() for word in ['bitten', 'severe injuries', 'multiple injuries', 'severe injurys', 'severe injury', 'severe']):
            return 'Severe'
        elif 'fatal' in injury.lower() or 'remains' in injury.lower():
            return 'Fatal'
        elif 'provoked incident' in injury.lower():
            return 'Provoked Incident'
        elif any(word in injury.lower() for word in ['lacerations', 'minor injury', 'no injury', 'injury']):
            return 'Minor/No Injury'
        else:
            return 'Unknown'
    else:
        return 'Unknown'

def clean_time(df):
    """ Cleaning and formatting of "time" column data"""
    
    df["time"].fillna("invalid", inplace=True)
    df["time"] = df["time"].str.lower().str.replace(' ', '_')
    
    mapping_time1 = {"midday" : "morning",
                "after_noon":"afternoon",
                "late_afternoon": "afternoon",
                "--" : "invalid",
                "sunset":"evening",
                "p.m." : "afternoon"}

    df["time"] = df['time'].replace(mapping_time1)
    
    return df   

def new_time(df):
    
    """Creating a new column with time categories"""
    
    #First defines a new column containing only entries showing the letter "h" or NaN values
    
    df["time_hour"] = df["time"].apply(lambda x: x if "h" in x else "0")
    
    # Formatting the mispelled or inconsistent values        
    mapping_time = {"before_10h00" : "10h00",
                    "-16h30":"16h00",
                    "0": "24h00",
                    "night" : "24h00",
                    "19h00,_dusk" : "19h00",
                    "midnight" : "24h00" ,
                    "sometime_between_06h00_&_08hoo"  : "07h00",
                    "before_07h00" : "06h00",
                    "09h00_-10h00" : "09h00",
                    "20h45_(sunset)" : "20h45"}
    
    df["time_hour"] = df['time_hour'].replace(mapping_time)
    
    # Including in the new column only the hour so the first numbers before "h" and converting the numbers to integers
    
    df["time_hour"] = df["time_hour"].apply(lambda x: x.split("h")[0])
    df["time_hour"] = df["time_hour"].astype(int)
    
    # Createing time categories in the new column associated with the hours of column "time"
            
    def combine_time_columns(row):
    
        """ Combines the two columns of time = "time" and "time_hour" 
        by considering first the entries of the column "time_hour". 
        The function returns the Dataframe with the complete new column time_hour """
    
        if row["time"] == "invalid":
            return "invalid"
        if row["time"] == "morning":
            return "morning"
        if row["time"] == "afternoon":
            return "afternoon"
        if row["time"] == "evening":
            return "evening"
        else:
            return row["time_hour"]
    
    df["time_of_day"] = df.apply(combine_time_columns, axis=1)  
            
    
    return df

def clean_state(df):
    
    mapping = {"New  South Wales" : "New South Wales",
           "New South ales" : "New South Wales",
           "New South Wales " : "New South Wales" ,
           "Westerm Australia"  : "Western Australia",
           "Western  Australia" : "Western Australia",
           "Northern Territory " : "Northern Territory"}

    df["state"] = df['state'].replace(mapping)
    
    return df

def check_provoked(df):
    
    for injury in df["injury"]:
        if isinstance(injury, str) and 'provoked' in injury.lower():
            return 'Provoked'
        else:
            return 'Unprovoked'
 
    return df


# In[ ]:




