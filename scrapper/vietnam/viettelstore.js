var request = require('request');
var cheerio = require('cheerio');

var company = 'viettel store';
var country_code = 'vn';

var mainUrl = 'https://viettelstore.vn';
var categoryUrls = [
    ['https://viettelstore.vn/Home/San-pham,Dien-thoai/', 'mobiles'],

    ['https://viettelstore.vn/Home/San-pham,May-tinh-bang/', 'tablets'],

    ['https://viettelstore.vn/Home/San-pham,Laptop/', 'laptops'],

    ['https://viettelstore.vn/Home/San-pham,Phu-kien,Phu-kien-dien-thoai,Cap-dau-doc-the/', 'accessories'],
    ['https://viettelstore.vn/Home/San-pham,Phu-kien,Phu-kien-dien-thoai,LoaTai-nghe/', 'accessories'],
    ['https://viettelstore.vn/Home/San-pham,Phu-kien,Phu-kien-dien-thoai,The-nho-2/', 'accessories'],
    ['https://viettelstore.vn/Home/San-pham,Phu-kien,Phu-kien-dien-thoai,Bao-da-op-lung-2/', 'accessories']
];

var localhost = 'http://localhost:8000/add-current-urls/';
var dev = 'http://128.199.213.210/add-current-urls/';
var requestUrl = dev;


function saveProductUrls(category, productUrls) {
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
                console.log(err);
            }
        }
    );
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

                var nextPage = $('a.next').attr('href');

                $('a.ptip').each(function () {
                    var productUrl = $(this).attr('href');
                    var merchant = '';
                    productUrls.push({
                        'url': productUrl,
                        'merchant': merchant
                    });
                });

                console.log(nextPage);

                if (nextPage.indexOf('http') > -1) {
                    startUrl = nextPage;
                    loop();
                } else {
                    saveProductUrls(category, productUrls);
                    if ((i+1) < categoryUrls.length)
                        crawl(i+1);
                }
            });
        }());
    }
}

crawl(0);



