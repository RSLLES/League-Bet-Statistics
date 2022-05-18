const fs = require('fs');

const cst = require('./config')
const scrapper = require("./scrapper");

async function main () {
    try{
        // Start XVBF
        var display = "";
        var xvfb = null;
        if (process.argv.includes("--xvfb")) {
            console.log('Starting new xvfb screen.');
            const Xvfb = require('xvfb');
            xvfb = new Xvfb({
                silent: true,
                // reuse : true, # Does not seem to work
                xvfb_args: ["-screen", "0", cst.xvfb_windows_size , "-ac"],
            });
            xvfb.startSync();
            display = `--display=${xvfb._display}`;
            console.log(`Display is ${xvfb._display}`);
        }

        // Main Programme
        try {
            await launch(display);
        } catch (err) {
            console.log(`FATAL ERROR : ${err}`);
        }
    
    
        // Kill XVBF
        if (process.argv.includes("--xvfb")) {
            console.log(`Killing display ${xvfb._display}`);
            xvfb.stopSync();
        }

    } catch (err) {
        console.log(`FATAL ERROR while dealing with XVBF screen : ${err}`);
    }
}

async function launch (display)
{
    // Load info :
    const proxy = await (async function () {
        try {
            const rawdata = fs.readFileSync(cst.proxy_config_path);
            console.log("Successfully got proxy settings from proxy.json");
            return JSON.parse(rawdata);
        } catch(err) {
            console.error("No proxy used.");
            return null;
        }
    })();

    // Puppeteer
    const puppeteer = require('puppeteer-extra');

    const stealthPlugin = require('puppeteer-extra-plugin-stealth');
    puppeteer.use(stealthPlugin());
    
    if (proxy != null) {
        const proxyPlugin = require('puppeteer-extra-plugin-proxy');
        puppeteer.use(proxyPlugin(proxy));
    }

    // Path
    var executablePath = null;
    for (const arg of process.argv){
        if (arg.includes("--path=")){
            executablePath = arg.split("=")[1];
            console.log(`Chromium path is ${executablePath}`)
        }
    }

    // Error Handling
    var browser = null;
    var i = 0;
    do {
        console.log("(" + (i+1).toString() + ") Opening browser.")
        if (browser != null) {await browser.close();}
        browser = await build_browser(puppeteer, display, executablePath);
        if (i >= cst.max_browser_opening){
            console.error("Reached max number of tries to open web browser. Please check your connection / your proxy settings.");
            process.exit();
        }
        i+=1
    } while ((! await browser_ready(browser)))

    // Scrapers
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(0); 
    await scrapper(page);
}

async function build_browser(puppeteer, display, executablePath){
    cfg = {
        headless: false,
        slowMo: 10,
        args : [
            `--window-size=${cst.window_size[0]},${cst.window_size[1]}`,
            "--no-sandbox",
            display
        ]
    };
    if (executablePath != null){
        cfg.executablePath = executablePath
    }

    return await puppeteer.launch(cfg);
}

async function browser_ready(browser){
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(0);
    try{
        await page.goto(cst.test_website_url);
        return true;
    }
    catch (error){
        if (error.message.includes("ERR_CONNECTION_RESET")) { 
            console.log("Error with Proxy. Retry");
        } else {throw error;}
    }
    return false;
}

main().then( () => {
    console.log("Exit.");
    process.exit();
});
