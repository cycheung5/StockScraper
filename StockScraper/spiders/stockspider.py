import scrapy 

class stockspider(scrapy.Spider):
    name = "stocks"
    scrape_url = input("enter site: ")
    start_urls = [scrape_url]

    def parse(self, response):
        current = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div')
        stock_t1 = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody')
        stock_t2 = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
        yield {
            'company' : response.css('h1::text').get(),
            'current_price' : current.css('span::text')[0].get(),
            'current_drop' : current.css('span::text')[1].get().split(" ")[0],
            'current_perc_drop' : current.css('span::text')[1].get().split(" ")[1][1:-2],
            'prev_close' : stock_t1.css('tr td span::text')[1].get(),
            'bid' : stock_t1.css('tr td span::text')[5].get(),
            'ask' : stock_t1.css('tr td span::text')[7].get(),
            'day_range' : stock_t1.css('tr td::text')[0].get(),
            'PE_ratio' : stock_t2.css('tr td span::text')[5].get()
        }


