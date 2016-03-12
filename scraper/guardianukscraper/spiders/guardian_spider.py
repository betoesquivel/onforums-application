import scrapy

from guardianukscraper.items import Article, Comment

class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = [
        "http://www.theguardian.com/world/2016/feb/09/draft-snoopers-charter-fails-on-spying-powers-and-privacy-protections"
    ]

    def parse(self, response):
        '''
        Parse the article, and yield a request to parse the comments if there is a
        comment section.
        '''
        article = Article()
        article['title']          = response.xpath('//h1[@itemprop="headline"]/text()').extract()[0]
        article['desc']           = response.xpath('//meta[@itemprop="description"]/@content').extract()[0]
        article['author']         = response.xpath('//span[@itemprop="author"]//span[@itemprop="name"]/text()').extract()[0]
        article['date_published'] = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract()[0]
        article['body']           = response.xpath('//div[@itemprop="articleBody"]//p/text()').extract()
        article['keywords']       = response.xpath('//a[@itemprop="keywords"]/text()').extract()
        article['comments_url']   = response.xpath('//a[@data-link-name="View all comments"]/@href').extract()[0]
        article['comments']       = []

        url = article['comments_url']
        request = scrapy.Request(url, callback=self.parse_comments)
        request.meta['article'] = article
        yield request

    def parse_comments(self, response):
        article = response.meta['article']
        page_comments = response.xpath('//li[@itemtype="http://schema.org/Comment"]')

        for c in page_comments:
            comment = Comment()

            comment['comment_id']       = c.xpath('@data-comment-id').extract()
            comment['author']           = c.xpath('@data-comment-author').extract()
            comment['author_id']        = c.xpath('@data-comment-author-id').extract()
            comment['reply_count']      = c.xpath('@data-comment-replies').extract()
            comment['timestamp']        = c.xpath('@data-comment-timestamp').extract()
            comment['reply_to_author']  = c.xpath('.//span[@class="d-comment__reply-to-author"]').extract()
            comment['reply_to_comment'] = c.xpath('.//a[contains(@href, "#comment-")]/@href').extract()
            comment['content']          = c.xpath('.//div[@itemprop="text"]/descendant-or-self::text()').extract()

            article['comments'].append(comment)

        current_page = response.xpath('//span[@tabindex="0"]/text()').extract()[0]
        next_page = int(current_page) + 1
        xpath_to_next_page_url = "//a[@data-page='{0}']/@href".format(next_page)
        next_page_url = response.xpath(xpath_to_next_page_url).extract()

        if next_page_url:
            url = next_page_url[0]
            request = scrapy.Request(url, callback=self.parse_comments)
            request.meta['article'] = article
            yield request
        else:
            yield article
