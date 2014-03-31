var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'phongvu';
var country_code = 'vn';

var mainUrl = 'http://phongvu.vn';
var categoryUrls = [
    ['http://phongvu.vn/san-pham-apple/iphone-1676c.html', 'mobiles'], // phone
    ['http://phongvu.vn/dien-thoai/dien-thoai-di-dong-1192c.html', 'mobiles'], // phone
    ['http://phongvu.vn/may-tinh/phu-kien-may-xach-tay-1163c.html', 'laptops'], // laptops
    ['http://phongvu.vn/san-pham-apple/macbook-1253c.html', 'laptops'], // laptops
    ['http://phongvu.vn/thiet-bi-tin-hoc/monitor-112c.html', 'monitors'], // monitors
    ['http://phongvu.vn/may-tinh/may-tinh-de-ban-pc-336c.html', 'desktops'], // desktops
    ['http://phongvu.vn/san-pham-apple/imac-1604c.html', 'desktops'], // desktops
    ['http://phongvu.vn/may-tinh/may-tinh-bang-tablet-1596c.html', 'tablets'], // tablets
    ['http://phongvu.vn/san-pham-apple/ipad-1675c.html', 'tablets'], // tablets
    ['http://phongvu.vn/may-tinh/phu-kien-may-tinh-bang-1618c.html', 'accessories'], // accessories
    ['http://phongvu.vn/thiet-bi-tin-hoc/keyboard-mouse-115c.html', 'accessories'] // accessories
]

var localhost = 'http://localhost:8000/add-current-urls/';
var dev = 'http://128.199.213.210/add-current-urls/';
var requestUrl = dev;


function printDeals(category, productUrls) {
    // request.post(
    //     requestUrl,
    //     {form: {
    //         data: JSON.stringify({product_urls: productUrls}),
    //         company: company,
    //         category: category,
    //         country_code: country_code
    //     }},
    //     function (err, resp, body) {
    //         if (!err && resp.statusCode == 200) {
    //             console.log(body);
    //         }
    //         else {
    //             console.log('Passed ' + productUrls.length + 'urls');
    //         }
    //     }
    // );
    console.log(productUrls);
}

function crawl(i) {
    var productUrls = [];
    if (i<categoryUrls.length) {
        startUrl = categoryUrls[i][0];
        category = categoryUrls[i][1];
        (function loop() {
            request(startUrl, function (err, resp, body) {
                if (err)
                    throw err;
                $ = cheerio.load(body);

                var nextPage = $('a:contains("Tiếp theo")').attr('href');
                $('div.bottomsp li.tensp > a').each(function () {
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



