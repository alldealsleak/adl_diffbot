var request = require('request');
var cheerio = require('cheerio');
var querystring = require('querystring');


var company = 'zalora';
var country_code = 'sg';

var mainUrl = 'http://www.zalora.sg';
var url = 'http://www.zalora.sg/beauty/';
var dealUrls = [];
var token = '953051970fc6bd63d53ca290c11651e2';
var diffbotUrl = 'http://api.diffbot.com/v2/product'


function printDeals() {
    request.post(
        'http://localhost:8000/add-current-urls/',
        {form: {
            data: JSON.stringify({urls: dealUrls}),
            company: company,
            country_code: country_code
        }},
        function (err, resp, body) {
            if (!err && resp.statusCode == 200) {
                console.log(body);
            }
            else {
                console.log('Passed ' + dealUrls.length + 'urls');
            }
        }
    );
}

(function loop() {
    request(url, function (err, resp, body) {
        if (err)
            throw err;
        $ = cheerio.load(body);

        var nextPage = $('a[title="Next"]').attr('href');

        $('ul#productsCatalog li > a.itm-link').each(function () {
            dealUrls.push(mainUrl + $(this).attr('href'));
        });

        if (nextPage) {
            url = 'http://www.zalora.sg' + nextPage;
            loop();
        } else {
            printDeals();
        }
    });
}());



{
    u'description': u'Item is non-refundable and non-returnable.\nFormulated with the revolutionary Stem-Acanax Complex that penetrates deep to improve skin from within. Pores to be less visible in 1 day. Improves radical firmness in 10 days. So you can feel the youthful beauty of 10 years ago.\nSize: 80g',
    u'title': u'STEMPOWER 80g',
    u'media':
        [{u'xpath': u'/html[1]/body[1]/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[2]/a[1]/span[2]/img[1]', 
        u'caption': u'STEMPOWER 80g',
        u'link': u'http://static04-sg.zalora.com/p/sk-ii-1405-23069-1-product.jpg',
        u'primary': True, u'type': u'image'}],
    u'brand': u'SK-II',
    u'offerPrice': u'219.00',
    u'availability': True,
    u'productId': u'SK790BE67MBOSG'}
