const puppeteer = require('puppeteer');

const url = 'https://particulier.edf.fr/fr/accueil/gestion-contrat/options/tempo.html';
const elementIds = ['a11y-today', 'a11y-tomorrow'];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    // Attendre que les éléments soient chargés
    await page.waitForSelector('#a11y-today');
    await page.waitForSelector('#a11y-tomorrow');

    const classNames = await page.evaluate((ids) => {
        return ids.map(id => {
            const element = document.getElementById(id);
            return element ? element.className : null;
        });
    }, elementIds);

    console.log(JSON.stringify(classNames));

    await browser.close();
})();