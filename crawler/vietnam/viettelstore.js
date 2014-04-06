var request = require('request');
var cheerio = require('cheerio');

var company = 'viettel store';
var country_code = 'vn';
var limit = 20;

var mainUrl = 'https://viettelstore.vn';
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

            var title = $('h3').text();
            var description = $('.product-feature').text();
            var offerPrice = $('strong.fcOrange.fs15').text();
            var mediaLink = $('a#imgPAvatar img').attr('src');
            var mediaCaption = $('a#imgPAvatar img').attr('alt');
            var merchant = $('div.breadcrumb ul li:nth-last-child(3) a').text();

            var product = {
                'url': url,
                'title': title,
                'description': description,
                'category': category,
                'offer_price': offerPrice,
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
