import scrapy 
from scrapy.shell import inspect_response

class stockspider(scrapy.Spider):
    name = "stocks"
    symbol = input("Symbol: ")
    start_urls = [
        "https://finance.yahoo.com/quote/{sym}?p={sym}&.tsrc=fin-srch".format(sym=symbol)
        ]

    # Prevent redirect 
    def start_requests(self):
        request = scrapy.Request(url=self.start_urls[0], callback=self.parse)         
        request.meta['dont_redirect'] = True  
        request.meta['handle_httpstatus_list'] = [302]        
        return [request]
        

    def parse(self, response):
        inspect_response(response, self) # Enters scrapy shell in command line 
        current = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div')
        stock_t1 = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody')
        stock_t2 = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
        results = { 
            "company" : response.css('h1::text').get(),
            "current_price" : current.css('span::text')[0].get(),
            "current_diff" : current.css('span::text')[1].get().split(" ")[0],
            "current_perc_diff" : current.css('span::text')[1].get().split(" ")[1][1:-1],
            "prev_close" : stock_t1.css('tr td span::text')[1].get(),
            "bid" : stock_t1.css('tr td span::text')[5].get(),
            "ask" : stock_t1.css('tr td span::text')[7].get(),
            "day_range" : stock_t1.css('tr td::text')[0].get(),
            "PE_ratio" : stock_t2.css('tr td span::text')[5].get()
        }
        results["company"]
        with open('output.txt', 'w') as output:
            out =  '"company" : {comp} \n"current_price" : {curr_p} \n"current_diff" : {curr_diff} \n"current_perc_diff" : {curr_perc} \n"prev_close" : {prev_close} \n"bid" : {bid} \n"ask" : {ask} \n"day_range" : {day_range} \n"PE_ratio : {PE_ratio}"'.format(comp=results["company"], curr_p=results["current_price"], curr_diff=results["current_diff"], curr_perc=results["current_perc_diff"], prev_close=results["prev_close"], bid=results["bid"], ask=results["ask"], day_range=results["day_range"], PE_ratio=results["PE_ratio"])
            output.write(out)
            output.close()

        # Scrape the news 
        news_page = response.xpath('//*[@id="Col1-3-Summary-Proxy"]/section/div/div')
        news = "https://finance.yahoo.com" + news_page.css("a::attr(href)").get()
        if news is not None: 
            news = response.urljoin(news)
            yield scrapy.Request(news, callback=self.parseNews)

    def parseNews(self, response):
        all_news = response.xpath('//*[@id="latestQuoteNewsStream-0-Stream"]/ul')
        titles = all_news.css("a::text").getall()
        links = all_news.css("a::attr(href)").getall()
        with open('output.txt', 'a') as output: 
            output.write("\nNews : [")
            for i in range(0, len(titles)):
                out = "\n" + titles[i] + " : " + links[i] + ","
                output.write(out)

            output.write("\n]")
            output.close()
        # Is not a static website. Loads more news when you scroll down. Need to figure out how to get more news
            


