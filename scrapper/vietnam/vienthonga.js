var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'vienthonga';
var country_code = 'vn';

var mainUrl = 'http://www.vienthonga.vn';
var categoryUrls = [
    ['http://www.vienthonga.vn/dien-thoai-smartphones/apple-iphone/', 'mobiles', 'Apple'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/samsung/', 'mobiles', 'Samsung'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/nokia/', 'mobiles', 'Nokia'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/htc/', 'mobiles', 'HTC'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/sony/', 'mobiles', 'Sony'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/blackberry/', 'mobiles', 'Blackberry'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/lenovo/', 'mobiles', 'Lenovo'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/q-mobile/', 'mobiles', 'Q-Mobile'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/mobiistar/', 'mobiles', 'Mobiistar'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/oppo/', 'mobiles', 'OPPO'],
    ['http://www.vienthonga.vn/dien-thoai-smartphones/gionee/', 'mobiles', 'Gionee'],

    ['http://www.vienthonga.vn/laptop/laptop-apple/', 'laptops', 'Apple'],
    ['http://www.vienthonga.vn/laptop/laptop-acer/', 'laptops', 'Acer'],
    ['http://www.vienthonga.vn/laptop/laptop-asus/', 'laptops', 'Asus'],
    ['http://www.vienthonga.vn/laptop/laptop-dell/', 'laptops', 'Dell'],
    ['http://www.vienthonga.vn/laptop/laptop-ibm-lenovo/', 'laptops', 'Lenovo'],
    ['http://www.vienthonga.vn/laptop/laptop-hp/', 'laptops', 'HP'],
    ['http://www.vienthonga.vn/laptop/laptop-sony/', 'laptops', 'Sony'],
    ['http://www.vienthonga.vn/laptop/laptop-samsung/', 'laptops', 'Samsung'],
    ['http://www.vienthonga.vn/laptop/laptop-toshiba/', 'laptops', 'Toshiba'],

    ['http://www.vienthonga.vn/may-tinh-bang/apple-ipad/', 'tablets', 'Apple'],
    ['http://www.vienthonga.vn/may-tinh-bang/samsung-tablet/', 'tablets', 'Samsung'],
    ['http://www.vienthonga.vn/may-tinh-bang/asus/', 'tablets', 'Asus'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-sony/', 'tablets', 'Sony'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-lg/', 'tablets', 'LG'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-lenovo/', 'tablets', 'lenovo'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-hp/', 'tablets', 'HP'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-kingcom/', 'tablets', 'Kingcom'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-coby/', 'tablets', 'Coby'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-ainol-novo/', 'tablets', 'Ainol Novo'],
    ['http://www.vienthonga.vn/may-tinh-bang/may-tinh-bang-foxconn/', 'tablets', 'Foxconn'],

    ['http://www.vienthonga.vn/linh-phu-kien/apple/', 'accessories', 'Apple'],
    ['http://www.vienthonga.vn/linh-phu-kien/samsung-vn-2/', 'accessories', 'Samsung'],
    ['http://www.vienthonga.vn/linh-phu-kien/phu-kien-chinh-hang-nokia-vn-2/', 'accessories', 'Nokia'],
    ['http://www.vienthonga.vn/linh-phu-kien/bao-da/', 'accessories', 'Bao da'],
    ['http://www.vienthonga.vn/linh-phu-kien/ban-phim/', 'accessories', 'Ban phim'],
    ['http://www.vienthonga.vn/linh-phu-kien/cap/', 'accessories', 'Cap']
];
var page;

var localhost = 'http://localhost:8000/save-products/';
var dev = 'http://128.199.213.210/save-products/';
var requestUrl = dev;


function saveProducts(category, products) {
    request.post(
        requestUrl,
        {form: {
            data: JSON.stringify({products: products}),
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
    var products = [];
    if (i<categoryUrls.length) {
        page = 1;
        startUrl = categoryUrls[i][0];
        category = categoryUrls[i][1];
        merchant = categoryUrls[i][2];
        (function loop() {
            request(startUrl, function (err, resp, body) {
                if (err)
                    throw err;
                $ = cheerio.load(body);

                page += 1;
                var hasNextpage = false;

                $('.product-container').each(function () {
                    hasNextpage = true;
                    var url = $(this).find('.product-info h4 a').attr('href');
                    var title = $(this).find('.product-info h4').text();
                    var description = $(this).find('.product-descr').text();
                    var offerPrice = $(this).find('.div-list-discount').text();
                    var media_link = mainUrl + $(this).find('.product-item-image img').attr('src');
                    var media_caption = $(this).find('.product-item-image img').attr('alt');

                    products.push({
                        'url': mainUrl + url,
                        'title': title,
                        'description': description,
                        'offer_price': offerPrice,
                        'merchant': merchant,
                        'media_link': media_link,
                        'media_caption': media_caption
                    });
                });

                if (hasNextpage) {
                    nextPage = categoryUrls[i][0] + 'page-' + page;
                    startUrl = nextPage;
                    loop();
                } else {
                    saveProducts(category, products);
                    if ((i+1) < categoryUrls.length)
                        crawl(i+1);
                }
            });
        }());
    }
}

crawl(0);



