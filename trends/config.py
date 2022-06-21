import numpy as np

config = {
    
    #############
    ### Paths ###
    #############

    "PROCESSED_DIR" : "data/processed",
    "SAVE_DIR" : "trends/best_selectors",


    #################
    ### Variables ###
    #################

    "STD" : 0.1,
    "NB_GRAPH" : 7,

    # Age threshold in seconds.
    # 3 weeks = 3600*24*7*3
    "age_threshold" : (age_threshold := 3600*24*7*2),

    # Weight at age threshold. Here, at 3 weeks, values must have 50% of their original weight
    "value_at_age_threshold" : (value_at_age_threshold := 0.5),

    # Maths : v = exp(-a/A) => A = -a/log(v)
    "AGE_THRESHOLD" : -age_threshold/np.log(value_at_age_threshold),
}