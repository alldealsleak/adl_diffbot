var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'zalora';
var country_code = 'sg';

var mainUrl = 'http://www.zalora.sg';
var url = 'http://www.zalora.sg/beauty/';
var dealUrls = [];
var token = '953051970fc6bd63d53ca290c11651e2';
var diffbotUrl = 'http://api.diffbot.com/v2/product'


function printDeals() {
    request.post(
        'http://localhost:8000/add-current-urls/',
        {form: {
            data: JSON.stringify({urls: dealUrls}),
            company: company,
            country_code: country_code
        }},
        function (err, resp, body) {
            if (!err && resp.statusCode == 200) {
                console.log(body);
            }
        }
    );
}

(function loop() {
    request(url, function (err, resp, body) {
        if (err)
            throw err;
        $ = cheerio.load(body);

        var nextPage = $('a[title="Next"]').attr('href');

        $('ul#productsCatalog li > a.itm-link').each(function () {
            dealUrls.push(mainUrl + $(this).attr('href'));
        });

        if (nextPage) {
            url = 'http://www.zalora.sg' + nextPage;
            loop();
        } else {
            printDeals();
        }
    });
}());
