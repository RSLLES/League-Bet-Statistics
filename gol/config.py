#################
### CONSTANTS ###
#################
time_between_request = 5
past_days_to_scrape = 6


#########################
### Website Selectors ###
#########################
url_last_match = "https://gol.gg/esports/ajax.home.php"
url_timeline = lambda id : f"https://gol.gg/game/stats/{id}/page-timeline/"
date_format = "%Y-%m-%d" # Used by GOL
selectors = {
    'nav_menu' : "li.nav-item.game-menu-button,li.nav-item.game-menu-button-active",
    'teams_names' : 'div.col-12.blue-line-header,div.col-12.red-line-header',
    "timeline" : "table.nostyle.timeline.trhover",
}

################
### Timeline ###
################
timeline = {
    "timecode" : {
        'idx' : 0
    },

    "colors" : {
        'idx' : 1,
        'attr' : 'src',
        'blue' : '../_img/blueside-icon.png',
        'red' : '../_img/redside-icon.png'
    },

    "actions" : {
        'idx' : 4,
        'attr' : 'src',
        'kill' : '../_img/kill-icon.png',
        'tower' : '../_img/tower-icon.png',
        'herald' : '../_img/herald-icon.png',
        'drake' : [
            '../_img/mountain-dragon.png', 
            '../_img/ocean-dragon.png',
            '../_img/hextech-dragon.png'
        ],
        'elder' : '../_img/elder-dragon.png',
        'nashor' : '../_img/nashor-icon.png',
        'inhib' : '../_img/inhib-icon.png',
        'nexus' : '../_img/nexus-icon.png'
    }
}


##################################
### Correctifs with Team Names ###
##################################

correctifs = {
    "Five" : "5",
    "TP" : "Phantasm"
}