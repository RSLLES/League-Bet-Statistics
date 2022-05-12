const fs = require('fs');

const cst = require('./config')
const scrapper = require("./scrapper");

async function main ()
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

    // XVBF
    var display = ""
    if (process.argv.includes("--xvfb")) {
        console.log('Starting new xvfb screen.')
        const Xvfb = require('xvfb');
        var xvfb = new Xvfb({
            silent: true,
            xvfb_args: ["-screen", "0", '1280x720x24', "-ac"],
        });
        await xvfb.start((err)=>{if (err) console.error(err)})
        display = `--display=${xvfb._display}`
        console.log(`Screen is ${xvfb._display}`)
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
            '--window-size=' + cst.window_size,
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
    process.exit();
});
