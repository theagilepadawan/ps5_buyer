const config = require('./config.json');
const puppeteer = require('puppeteer-core');

const username = config.username;
const password = config.password;
//const PRODUCT_URL = "https://coop.no/sortiment/obs-sortiment/elektronikk/underholdning/konsoll/playstation-5-playstation-5-optisk/?variantCode=885614";
const PRODUCT_URL = "http://localhost:5000";
const checkout_URL = "https://coop.no/checkout/checkouttotal/";

(async () => {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: false
    });
    const page = await browser.newPage();
    await page.setCacheEnabled(false);
    await page.setViewport({width: 1366, height: 1400});
    await page.goto(PRODUCT_URL, {waitUntil: 'networkidle2'});

    while (true) {
        try {
            await page.click("[aria-label=Kjøp]");
            break;
        } catch (err) {
            await page.reload({waitUntil: 'networkidle2'});
        }
    }

    await page.goto(checkout_URL, {waitUntil: "networkidle2"});
    await page.type("input[name='username']", username);
    await page.type("input[name='password']", password);

    await Promise.all([
        page.waitForNavigation(), // The promise resolves after navigation has finished
        page.keyboard.press('Enter')
    ]);

    await page.waitForSelector("input[type='checkbox']", {waitUntil: "networkidle2"})
    await page.click("input[id='02_default_60_873_99743']")
    await page.click("input[id='30f65eb5-e33d-44ba-8e1f-867ad3ac92d0']")
    await page.click("input[type='checkbox']");

    await Promise.all([
        page.waitForNavigation(), // The promise resolves after navigation has finished
        page.keyboard.press('Enter')
    ]);

    await page.waitForSelector("#ssg");
    await page.type('#ssg', "04089147757");

    await page.click("#phoneNumber", {clickCount: 3})
    await page.type('#phoneNumber', "+4792820911");

    await page.click("#chkConfirmation")
    //await page.click("#okButton")


    await new Promise(r => setTimeout(r, 200000));

    await browser.close();
})();
