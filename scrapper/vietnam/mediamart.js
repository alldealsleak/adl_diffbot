var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'mediamart';
var country_code = 'vn';

var mainUrl = 'http://mediamart.vn';
var categoryUrls = [
    ['http://mediamart.vn/smartphones', 'mobiles'], // phone
    ['http://mediamart.vn/laptop', 'laptops'], // laptops
    ['http://mediamart.vn/chuot', 'accessories'], // accessories
    ['http://mediamart.vn/tin-hoc/', 'accessories'] // accessories
]
var page;

var localhost = 'http://localhost:8000/add-current-urls/';
var dev = 'http://128.199.213.210/add-current-urls/';
var requestUrl = dev;


function printDeals(category, productUrls) {
    request.post(
        requestUrl,
        {form: {
            data: JSON.stringify({product_urls: productUrls}),
            company: company,
            category: category,
            country_code: country_code
        }},
        function (err, resp, body) {
            if (!err && resp.statusCode == 200) {
                console.log(body);
            }
            else {
                console.log('Passed ' + productUrls.length + ' urls');
            }
        }
    );
}

function crawl(i) {
    var productUrls = [];
    console.log(categoryUrls.length);
    if (i<categoryUrls.length) {
        page = 1;
        startUrl = categoryUrls[i][0];
        category = categoryUrls[i][1];
        (function loop() {
            request(startUrl, function (err, resp, body) {
                if (err)
                    throw err;
                $ = cheerio.load(body);

                page += 1;
                var hasNextpage = false;
                $('li.temp-pro-item-li').each(function () {
                    hasNextpage = true;
                    var productUrl = mainUrl + $(this).find('p.name > a.zp').attr('href');
                    var merchant = $(this).find('p.brand').text();
                    productUrls.push({
                        'url': productUrl,
                        'merchant': merchant
                    });
                });

                if (hasNextpage) {
                    nextPage = categoryUrls[i][0] + '?page=' + page;
                    startUrl = nextPage;
                    loop();
                } else {
                    printDeals(category, productUrls);
                    productUrls = [];
                    if ((i+1) < categoryUrls.length)
                        crawl(i+1);
                }
                printDeals(category, productUrls);
            });
        }());
    }
}

crawl(0);



