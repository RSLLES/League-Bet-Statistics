// ##### BRIQUES #####
// All the base functions that interact with the webpage
async function _wait (ms){
    delay = () => new Promise(resolve => setTimeout(resolve, ms));
    await delay();
}

function _round (n){
    return Math.floor(n*100)/100;
}

function _normal (mean, sigma) {
    var u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    var u = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
    return u*sigma + mean;
}

function _normalClipped (mean, sigma, threshold=100) {
    const u = _normal (mean, sigma)
    if (u < threshold) {
        return threshold;
    }
    return u;
}

async function _think (){
    await _wait(_normalClipped(1500, 300));
}
async function _reaction (){
    await _wait(_normalClipped(500, 100));
}


const N_retry_wait_bet_promise = 2;
async function _waitForElement (page, selector, verbose=true) {
    var i = 0;
    while (i < N_retry_wait_bet_promise)
    {
        const t = Date.now();
        try {
            await page.waitForSelector(selector);
            return;
        } catch (error) {
            if (verbose)
            {
                console.log("[" + i + "/" + N_retry_wait_bet_promise + "] Searching " + selector + "(" + (Date.now() - t) + ")");
            }
        }
        i+=1;
    }
    throw new Error("Can't find " + selector)
}

async function _waitForElements(page, selector_1, selector_2)
{
    return Promise.race([
        _waitForElement(page, selector_1, false).then( ()=> { return 1 } ).catch(),
        _waitForElement(page, selector_2, false).then( ()=> { return 2 } ).catch()
    ]);
}

async function _$ (page, selector, ignoreIfNotFind=false, wait=true)
{
    if (!ignoreIfNotFind){
        await _waitForElement(page, selector);
        if (wait) await _think();
    }
    else{
        if (wait) await _reaction();
    }
    return page.$(selector);
}

async function _$2 (page, selector, ignoreIfNotFind=false)
{
    var all = await _$$(page, selector, ignoreIfNotFind);
    return (all.length == 2) ? all : null;
}

async function _$$ (page, selector, ignoreIfNotFind=false)
{
    if (!ignoreIfNotFind){
        await _waitForElement(page, selector);
        await _think();
    }
    else{
        await _reaction();
    }
    return page.$$(selector);
}

async function _getMiddle (elem) {
    try{
        const boundingBox = await elem.boundingBox();
        var x = boundingBox.x == null ? 0 : boundingBox.x;
        var y = boundingBox.y == null ? 0 : boundingBox.y;
        return {
            x : x + boundingBox.width / 2,
            y : y + boundingBox.height / 2
        }

    } catch {
        return {x : 0, y : 0};
    }
}

async function autoScroll(page) {
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}

async function _extractFromTD(td, selec){
    const bothElem = await _$2(td, selec, true);
    if (bothElem == null){
        return null;
    }
    return bothElem;
}

function _equalCoordinates(a, b){
    return (_round(a.x) == _round(b.x) && _round(a.y) == _round(b.y))
}

async function _getUrl (a) {
    return await a.evaluate(e => e.getAttribute('href'));
}

async function _getText (elem) {
    return await elem.evaluate(e => e.textContent);
}

async function _getTextFromSelector (page, selec, wait=true){
    return await _getText(await _$(page, selec, ignoreIfNotFind = false, wait = wait));
}

async function _click (elem){
    await _reaction();
    await elem.click();
    await _reaction();
}

async function _clickViaSelector(page, selector, ignoreIfNotFind=false){
    await _reaction();
    const elem = await _$(page, selector, ignoreIfNotFind);
    if (elem == null) {return};

    await _think();
    await _click(elem);
}

async function _getClasses(e){
    return await (await e.getProperty('className')).jsonValue();
    // return all;
}

function _fromSelectorToClass(selec){
    return selec.split(".").pop();
}

function _replaceTeamsNames(betName, teamNames){
    return betName.replace(teamNames[0], "t1_").replace(teamNames[1], "t2_");
}

function _formatString(str){
    return str.replace(/[^a-z0-9-+_\.]/gi,'').toLowerCase();
}

function _add(json, key, value){
    if (key in json){
        json[key] = value;
    }
    else{
        json[key] = {}
    }
}

function _fromatSectionAndUpdateBOLength(currentSection, boLengthEstimation){
    if (currentSection.includes("map1")){
        return [currentSection.replace("map1", ""), "map", Math.max(boLengthEstimation, 1)];
    }
    if (currentSection.includes("map2")){
        return [currentSection.replace("map2", ""), null, Math.max(boLengthEstimation, 3)];
    }
    if (currentSection.includes("map3")){
        return [currentSection.replace("map3", ""), null, Math.max(boLengthEstimation, 5)];
    }
    return [currentSection, "global", boLengthEstimation];
}

function _hash(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        var char = str.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}

// Export
module.exports = {
    wait : _wait,
    normal : _normal,
    normalClipped : _normalClipped,
    think : _think,
    reaction : _reaction,
    waitForElement : _waitForElement,
    waitForElements : _waitForElements,
    clickViaSelector : _clickViaSelector,
    extractFromTD : _extractFromTD,
    autoScroll : autoScroll,
    getMiddle : _getMiddle,
    $ : _$,
    $$ : _$$,
    $2 : _$2,
    getClasses: _getClasses,
    equalCoordinates : _equalCoordinates,
    getUrl : _getUrl,
    getText : _getText,
    getTextFromSelector : _getTextFromSelector,
    fromSelectorToClass : _fromSelectorToClass,
    replaceTeamsNames : _replaceTeamsNames,
    formatString : _formatString,
    fromatSectionAndUpdateBOLength : _fromatSectionAndUpdateBOLength,
    add : _add,
    hash : _hash,
}