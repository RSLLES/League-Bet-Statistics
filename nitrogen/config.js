// Scrapper constants

module.exports = {
    // #############
    // ### PATHS ###
    // #############
    proxy_config_path : "config/proxy.json",
    data_file_path : "data/data_unmatched.json",
    processed_id_file_path : "data/id_history.json",


    // ############
    // ### URLS ###
    // ############
    test_website_url : "https://icanhazip.com/",
    base_nitrogen_url : "https://amped.nitrogensports.eu",
    nitrogen_betting_page_url : "https://amped.nitrogensports.eu/esports/league-of-legends",


    // ###############
    // ### BROWSER ###
    // ###############
    max_browser_opening : 20,
    xvfb_windows_size : '1920x1080x24',
    window_size : "1920,1080",
    scrolling_speed : 200,
    

    // #################
    // ### SCRAPPING ###
    // #################
    time_threshold : 48, // How many hours to scrape games ahead from now
    minNumOfBets : 2, // How many bets should a game have to be scrapped, otherwise it skips it.
    nitrogen_date_format : 'DD MMM HH:mm',
    
    
    // #################
    // ### SELECTORS ###
    // #################
    selectors : selectors = {
        oddsType : "body > div.app > div > div > div:nth-child(1) > div > div:nth-child(3)",
        oddsDecimalOption :"body > div.app > div > div > div:nth-child(1) > div > div:nth-child(3) > div > div.kQyk8.hXjns > div > div:nth-child(2) > span",
    
        matchLine : {
            div : "div.CIXLg",
            url : "a.vgAKr.nhhlw",
            date : "div.LCkt7",
            numberOfBets : "a.QjV8s"
        },
    
        matchPage : {
            teamNames : "h2.f_moG",
            mainDiv: "div.USNxA",
            betDiv : "div.BkdmE",
            titleDiv: "div.rzXPb",
            individualBet : "button.vsHeu.xnKGz",
        },
        
        uniqueBet : {
            betName: "div.vgAKr.XoOd9",
            betOdd: "div.tFiVV.AEcjI",
        },
    }
}