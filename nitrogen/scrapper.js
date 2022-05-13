// IMPORTATION
const moment = require('moment');
const fs = require('fs');

const utils = require('./utils');
const cst = require('./config');



async function main (page){
    await page.goto(cst.nitrogen_betting_page_url);
    await utils.think();
    await swapToEuropeanOdds(page);
    
    var date = null;
    var lastNumberOfMatches = 0;
    var matchs = null;
    var nbLoop = 0;
    
    do
    {
        matchs = await utils.$$(page, cst.selectors.matchLine.div);
        const lastMatch = matchs[matchs.length - 1];

        // On verifie si la date du dernier match nous suffit
        // Ce check est inutile si le nombre de match n'a pas changé
        if (matchs.length != lastNumberOfMatches)
        {
            lastNumberOfMatches = matchs.length;

            await utils.think();
            date = await _getDateFromMatch(lastMatch);
        }
        
        // On effectue un scorll
        const positionFirstMatch = await utils.getMiddle(matchs[0]);
        const x = Math.max(positionFirstMatch.x, parseInt(cst.window_size[0]/2))
        const y = Math.max(positionFirstMatch.y, parseInt(cst.window_size[1]/2))
        await page.mouse.move(x, y);
        await utils.reaction();
        await page.mouse.wheel({ deltaY: cst.scrolling_speed });
        await utils.reaction();
            

        nbLoop += 1;
        process.stdout.write('(' + nbLoop + ') Scrolling \r');
    } while (!dateIsOlderThan(date, cst.time_threshold) && nbLoop < cst.max_scroll)

    // On retourne les urls et les dates
    var matchsInLine = await Promise.all(
        matchs.map(async function (match) {
            const date = await _getDateFromMatch(match);
            const endUrl =          await utils.getUrl(await utils.$(match, cst.selectors.matchLine.url));
            const numberOfBets =    await utils.getText(await utils.$(match, cst.selectors.matchLine.numberOfBets));
            return {
                url : cst.base_nitrogen_url + endUrl,
                date : date,
                numberOfBets : parseInt(numberOfBets),
            };
        })
    );

    // Filtrage : On ne garde que les matchs qui commencent dans moins de 24h et qui ont plus de 10 paris
    const results = await Promise.all(
        matchsInLine.map(async (value) => value.date != null && !dateIsOlderThan(value.date, cst.time_threshold) && value.numberOfBets >= cst.minNumOfBets)
    );
    matchsInLine = matchsInLine.filter((_, index) => results[index]);

    // Lecture : On charge l'historique
    open_file = async function (path, msg, def) {
        try {
            const rawdata = fs.readFileSync(path);
            return JSON.parse(rawdata);
        } catch(err) {
            console.error("WARNING : Can't find " + path + ".");
            console.error(msg);
            return def;
        }
    }
    var old_ids = await open_file(cst.processed_id_file_path, msg="No past ID loaded.", def={scraped : []});
    var data = await open_file(cst.data_file_path, msg="Starting with a blank array.", def = {});

    // Recuperer les differentes lignes
    for (const match of matchsInLine){
        await page.goto(match.url);
        await utils.think();
        await utils.waitForElement(page, cst.selectors.matchPage.mainDiv);
        await utils.autoScroll(page);

        // On recuperer les noms
        var teamNames = null;
        try{
            teamNames = await Promise.all(
                (await utils.$2(page, cst.selectors.matchPage.teamNames)).map(utils.getText) 
            );
        }
        catch{
            console.error("Can't find teams' names.  Skipped.")
            continue
        }

        // Check l'ID pour ne pas refaire un match déjà traité
        const id = utils.hash(match.url);
        console.log("Teams Names : " + teamNames + " | ID = " + id);

        if (old_ids['scraped'].includes(id)){
            console.log("Already processed. Skipped.");
        }
        else {

            // Main div
            const mainDiv = await utils.$(page, cst.selectors.matchPage.mainDiv);
            const tds = await utils.$$(mainDiv, cst.selectors.matchPage.betDiv + "," + cst.selectors.matchPage.titleDiv);

            var currentSection = null;
            var map = null;
            var boLengthEstimation = 1;
            var infos = {
                teamNames : {
                    t1 : teamNames[0],
                    t2 : teamNames[1]
                },
                date : {
                    time : match.date.format("HH:mm"),
                    day : match.date.format("D"),
                    month : match.date.format("M"),
                    year : match.date.format("YYYY"),
                }
            };

            for (const td of tds){

                const className = await utils.getClasses(td);

                // Si c'est un titre
                if (className == utils.fromSelectorToClass(cst.selectors.matchPage.titleDiv)){
                    currentSection = utils.formatString(utils.replaceTeamsNames(await utils.getText(td), teamNames));
                    [currentSection, map, boLengthEstimation] = utils.fromatSectionAndUpdateBOLength(currentSection, boLengthEstimation);
                }

                // Si c'est une boite de paris, et que le match n'est pas répété
                if (className == utils.fromSelectorToClass(cst.selectors.matchPage.betDiv) && map != null){
                    // Recupere toutes les boites
                    const boxes = await utils.$$(td, cst.selectors.matchPage.individualBet, true)
                    for (const box of boxes){
                        var name = await utils.getTextFromSelector(box, cst.selectors.uniqueBet.betName, wait=false);
                        var odd = await utils.getTextFromSelector(box, cst.selectors.uniqueBet.betOdd, wait=false);
                        
                        name = utils.formatString(utils.replaceTeamsNames(name, teamNames));
                        odd = parseFloat(odd).toFixed(2);

                        infos = add_key(infos, map);
                        infos[map] = add_key(infos[map], currentSection);
                        infos[map][currentSection][name] = odd;
                        console.log(map + "." + currentSection + "." + name + " : " + odd);
                    }
                }
            }
            // Ajout du BO et log
            infos.BOLength = boLengthEstimation;
            
            console.log("Match successfully scraped.");
            data[id] = infos;
            old_ids.scraped.push(id);
        }
    }

    // Saving
    fs.writeFileSync(cst.data_file_path, JSON.stringify(data),"utf-8");
    console.log("Data saved.");

    fs.writeFileSync(cst.processed_id_file_path, JSON.stringify(old_ids),"utf-8");
    console.log("IDs scraped saved.");
}

function add_key(json, key){
    if (!(key in json)){ json[key] = {};}
    return json;
    
}

async function _getDateFromMatch(match) {
    var date = await utils.$(match, cst.selectors.matchLine.date, true);
    if (date != null){
        date = moment(await utils.getText(date), cst.nitrogen_date_format);
    }
    return date;
}


function dateIsOlderThan (date, hours){
    return (date != null && date.diff(moment(), "hours") >= hours);
}


async function swapToEuropeanOdds (page) {
    await utils.clickViaSelector(page, cst.selectors.oddsType);
    await utils.clickViaSelector(page, cst.selectors.oddsDecimalOption);
}

module.exports = main