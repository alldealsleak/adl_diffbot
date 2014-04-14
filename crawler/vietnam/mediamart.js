var request = require('request');
var cheerio = require('cheerio');

var company = 'mediamart';
var country_code = 'vn';
var limit = 20;

var mainUrl = 'http://mediamart.vn';
var localhost = 'http://localhost:8000/';
var dev = 'http://128.199.213.210/';

var serverUsed = dev;

var getCurrentUrl = serverUsed + 'get-current-urls/?country_code=' +
    country_code + '&company=' + company + '&limit=' + limit;
var saveProductsUrl = serverUsed + 'save-products/';

var products = [];
function saveProducts () {
    request.post(
        saveProductsUrl,
        {form: {
            data: JSON.stringify({products: products}),
            company: company,
            country_code: country_code
        }},
        function (err, resp, body) {
            if (!err && resp.statusCode == 200) {
                products = [];
                getCurrentUrls();
            }
            else {
                console.log(err);
            }
        }
    );
}

function crawl (i, productUrls) {
    if (i<productUrls.length) {
        var category = productUrls[i].category__name;
        var url = productUrls[i].link;

        request(url, function (err, resp, body) {
            if (err)
                throw err;
            $ = cheerio.load(body);

            var productId = $('span:contains("Mã hàng:")').text();
            var title = $('h1[itemprop="name"]').text();
            var description = $('div[itemprop="description"]').text();
            var regularPrice = $('div.p-price.p-price-market span.price').text();
            var saveAmount = $('div.p-price.p-price-save span.price').text();
            var mediaLink = $('a.pro-image-large img').attr('src');
            var mediaCaption = $('a.pro-image-large img').attr('alt');
            var merchant = '';

            var product = {
                'url': url,
                'product_id': productId,
                'title': title,
                'description': description,
                'category': category,
                'regular_price': regularPrice,
                'save_amount': saveAmount,
                'merchant': merchant,
                'media_link': mediaLink,
                'media_caption': mediaCaption
            };
            console.log(product.url);

            products.push(product);

            if ((i+1) < productUrls.length) {
                crawl(i+1, productUrls);
            }
            else {
                saveProducts(products);
            }
        });
    }
}

function getCurrentUrls() {
    request({
        url: getCurrentUrl,
        json: true,
    }, function (err, resp, body) {
        if (!err && resp.statusCode == 200) {
            crawl (0, body);
        }
        else {
            console.log(err);
        }
    });
}

getCurrentUrls();
