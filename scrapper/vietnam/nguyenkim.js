var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'nguyenkim';
var country_code = 'vn';

var mainUrl = 'http://www.nguyenkim.com';
var categoryUrls = [
    ['http://www.nguyenkim.com/dien-thoai-di-dong/', 'mobiles'], // phone
    ['http://www.nguyenkim.com/may-tinh-xach-tay/', 'laptops'], // laptops
    ['http://www.nguyenkim.com/man-hinh-lcd-vi-tinh/', 'monitors'], // monitors
    ['http://www.nguyenkim.com/may-tinh-de-ban/', 'desktops'], // desktops
    ['http://www.nguyenkim.com/may-tinh-bang/', 'tablets'], // tablets
    ['http://www.nguyenkim.com/phu-kien-tin-hoc/', 'accessories'] // accessories
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
                console.log('Passed ' + productUrls.length + 'urls');
            }
        }
    );
    console.log(productUrls);
}

function crawl(i) {
    var productUrls = [];
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
                $('div.block_title_sp_home_new > a.product-title').each(function () {
                    hasNextpage = true;
                    var productUrl = mainUrl + $(this).attr('href');
                    var merchant = '';
                    productUrls.push({
                        'url': productUrl,
                        'merchant': merchant
                    });
                });

                if (hasNextpage) {
                    nextPage = categoryUrls[i][0] + 'page-' + page;
                    console.log(nextPage);
                    startUrl = nextPage;
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



