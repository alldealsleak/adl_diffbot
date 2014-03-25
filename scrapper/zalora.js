var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'zalora';
var country_code = 'sg';

var mainUrl = 'http://www.zalora.sg';
var start_url = 'http://www.zalora.sg/beauty/';
var dealUrls = [];

var localhost = 'http://localhost:8000/add-current-urls/';
var dev = 'http://128.199.213.210/add-current-urls/';


function printDeals() {
    request.post(
        dev,
        {form: {
            data: JSON.stringify({urls: dealUrls}),
            company: company,
            country_code: country_code
        }},
        function (err, resp, body) {
            if (!err && resp.statusCode == 200) {
                console.log(body);
            }
            else {
                console.log('Passed ' + dealUrls.length + 'urls');
            }
        }
    );
}

(function loop() {
    request(start_url, function (err, resp, body) {
        if (err)
            throw err;
        $ = cheerio.load(body);

        var nextPage = $('a[title="Next"]').attr('href');

        $('ul#productsCatalog li > a.itm-link').each(function () {
            dealUrls.push(mainUrl + $(this).attr('href'));
        });

        if (nextPage) {
            start_url = 'http://www.zalora.sg' + nextPage;
            loop();
        } else {
            printDeals();
        }
    });
}());
