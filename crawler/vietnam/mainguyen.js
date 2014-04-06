var request = require('request');
var cheerio = require('cheerio');

var company = 'mainguyen';
var country_code = 'vn';
var limit = 20;

var mainUrl = 'http://www.mainguyen.vn';
var localhost = 'http://localhost:8000/';
var dev = 'http://128.199.213.210/';

var serverUsed = localhost;

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
        var merchant = productUrls[i].merchant;
        var url = productUrls[i].link;

        request(url, function (err, resp, body) {
            if (err)
                throw err;
            $ = cheerio.load(body);

            var title = $('h1.left_block_title').text();
            var description = $('.prod_dt_desc_list').text();
            var offerPrice = $('.prod_dt_price').text();
            var mediaLink = mainUrl + $('.cprod_dt_img img').attr('src');
            var mediaCaption = $('.cprod_dt_img img').attr('alt');

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
            console.log(body);
            crawl (0, body);
        }
        else {
            console.log(err);
        }
    });
}

getCurrentUrls();
