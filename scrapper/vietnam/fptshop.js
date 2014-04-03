var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');

var company = 'fptshop';
var country_code = 'vn';

var mainUrl = 'http://fptshop.com.vn';
var categoryUrls = [
    ['http://fptshop.com.vn/dien-thoai', 'mobiles'], // phone
    ['http://fptshop.com.vn/may-tinh-bang-2', 'tablets'], // tablets
    ['http://fptshop.com.vn/may-tinh-xach-tay', 'laptops'], // laptops
    ['http://fptshop.com.vn/phu-kien-3', 'accessories'] // laptops
];
var firstPageStr = '?pagenumber=1&X-Requested-With=XMLHttpRequest';

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
                console.log('Passed ' + productUrls.length + 'urls');
            }
        }
    );
    console.log(productUrls);
}


function crawl(i) {
    var productUrls = [];
    if (i<categoryUrls.length) {
        startUrl = categoryUrls[i][0] + firstPageStr;
        category = categoryUrls[i][1];
        (function loop() {
            request(startUrl, function (err, resp, body) {
                if (err)
                    throw err;
                $ = cheerio.load(body);

                var nextPage = $('a:contains("Tiếp tục")').attr('href');

                $('div.spTextTitle > a').each(function () {
                    var productUrl = mainUrl + $(this).attr('href');
                    var merchant = '';
                    productUrls.push({
                        'url': productUrl,
                        'merchant': merchant
                    });
                });

                if (nextPage) {
                    startUrl = mainUrl + nextPage;
                    loop();
                } else {
                    printDeals(category, productUrls);
                    if ((i+1) < categoryUrls.length)
                        crawl(i+1);
                }
            });
        }());
    }
}

crawl(0);



