var request = require('request');
var cheerio = require('cheerio');

var company = 'mainguyen';
var country_code = 'vn';

var mainUrl = 'http://www.mainguyen.vn';
var categoryUrls = [
    ['http://www.mainguyen.vn/dien-thoai/mobiado.html', 'mobiles', 'MOBIADO'],
    ['http://www.mainguyen.vn/dien-thoai/bellperre.html', 'mobiles', 'BELLPERRE'],
    ['http://www.mainguyen.vn/dien-thoai/tonino-lamborghini.html', 'mobiles', 'TONINO LAMBORGHINI'],
    ['http://www.mainguyen.vn/dien-thoai/apple.html', 'mobiles', 'APPPLE'],
    ['http://www.mainguyen.vn/dien-thoai/samsung.html', 'mobiles', 'SAMSUNG'],
    ['http://www.mainguyen.vn/dien-thoai/nokia.html', 'mobiles', 'NOKIA'],
    ['http://www.mainguyen.vn/dien-thoai/htc.html', 'mobiles', 'HTC'],
    ['http://www.mainguyen.vn/dien-thoai/sony.html', 'mobiles', 'SONY'],
    ['http://www.mainguyen.vn/dien-thoai/lg.html', 'mobiles', 'LG'],
    ['http://www.mainguyen.vn/dien-thoai/asus.html', 'mobiles', 'ASUS'],
    ['http://www.mainguyen.vn/dien-thoai/blackberry.html', 'mobiles', 'BLACKBERRY'],
    ['http://www.mainguyen.vn/dien-thoai/oppo.html', 'mobiles', 'OPPO'],
    ['http://www.mainguyen.vn/dien-thoai/pantech.html', 'mobiles', 'PANTECH'],
    ['http://www.mainguyen.vn/dien-thoai/lenovo.html', 'mobiles', 'LENOVO'],
    ['http://www.mainguyen.vn/dien-thoai/sharp.html', 'mobiles', 'SHARP'],

    ['http://www.mainguyen.vn/may-tinh-bang/apple.html', 'tablets', 'APPLE'],
    ['http://www.mainguyen.vn/may-tinh-bang/samsung.html', 'tablets', 'SAMSUNG'],
    ['http://www.mainguyen.vn/may-tinh-bang/nokia.html', 'tablets', 'NOKIA'],
    ['http://www.mainguyen.vn/may-tinh-bang/sony.html', 'tablets', 'SONY'],
    ['http://www.mainguyen.vn/may-tinh-bang/lg.html', 'tablets', 'LG'],
    ['http://www.mainguyen.vn/may-tinh-bang/asus.html', 'tablets', 'ASUS'],
    ['http://www.mainguyen.vn/may-tinh-bang/lenovo.html', 'tablets', 'LENOVO'],
    ['http://www.mainguyen.vn/may-tinh-bang/hp.html', 'tablets', 'HP'],

    ['http://www.mainguyen.vn/phu-kien/phu-kien-galaxy-s5-s5-zoom-gear-2-gear-fit.html', 'accessories', 'SAMSUNG'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-galaxy-s4-s3.html', 'accessories', 'SAMSUNG'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-bb-z10-q10.html', 'accessories', 'BLACKBERRY'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-galaxy-note.html', 'accessories', 'SAMSUNG'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-macbook.html', 'accessories', 'APPLE'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-galaxy-s-ii.html', 'accessories', 'SAMSUNG'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-galaxy-tab.html', 'accessories', 'SAMSUNG'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-iphone-ipod.html', 'accessories', 'APPLE'],
    ['http://www.mainguyen.vn/phu-kien/phu-kien-ipad.html', 'accessories', 'APPLE'],
    ['http://www.mainguyen.vn/phu-kien/sac-nhanh-sac-xe-hoi.html', 'accessories', 'NOKIA'],
    ['http://www.mainguyen.vn/phu-kien/linh-kien-blackberry.html', 'accessories', 'BLACKBERRY']
  
];

var localhost = 'http://localhost:8000/add-current-urls/';
var dev = 'http://128.199.213.210/add-current-urls/';
var requestUrl = localhost;


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
        merchant = categoryUrls[i][2];
        (function loop() {
            request(startUrl, function (err, resp, body) {
                console.log(startUrl);
                if (err)
                    throw err;
                $ = cheerio.load(body);

                $('.left_block_ct div.prod_item a.prod_item_img').each(function () {
                    var productUrl = mainUrl + $(this).attr('href');
                    productUrls.push({
                        'url': productUrl,
                        'merchant': merchant
                    });
                });

                saveProductUrls(category, productUrls);
                productUrls = [];
                if ((i+1) < categoryUrls.length)
                    crawl(i+1);
            });
        }());
    }
}

crawl(0);



