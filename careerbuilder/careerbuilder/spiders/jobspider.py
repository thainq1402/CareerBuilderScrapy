import scrapy
from scrapy.http import TextResponse

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["careerbuilder.vn"]
    start_urls = ["https://careerbuilder.vn/tim-viec-lam.html"]

    def parse(self, response):
        domain = response.css('ul.list-jobs') ## Get all link in 'Tim viec lam theo nganh nghe' , Clas list job
        for sub_domain in domain:
            ##Get all links in 'TÌM VIỆC LÀM BÁN HÀNG / TIẾP THỊ', this variable contain multiple links
            sub_domain_links = sub_domain.css('li span a::attr(href)').getall()  
            for job_links in sub_domain_links:
                ## Get a single link in in job_link_class and go into it and get the url for each job 
                    yield response.follow(job_links,callback=self.parse_job_links)
        pass    

    
    def parse_job_links(self,response):
        ## contain multiple class title 
        job_classes = response.css('div.title')

        for job_class in job_classes:
            job_url = job_class.css('h2 a.job_link::attr(href)').get()
            ## job_url : contain the link to job detail 
            yield response.follow(job_url, callback=self.parse_job_detail)
            


    
        ##next page
        netx_job_page = response.css('.pagination a::attr(href)').get()
        if netx_job_page is not None:
            yield response.follow(netx_job_page,callback = self.parse_job_links)   
             
                

    def parse_job_detail(self,response):
        ## this method will go into each job link to get detail of the job 
        job_detail_content = response.css('.job-detail-content .detail-row')
        detail_box = response.css('.detail-box')
        yield{
    
            'TenCV'         : response.css('div.job-desc h1.title::text').get().encode('utf-8').decode('utf-8'),
            'CongTy '       : response.css('div.job-desc a.employer::text').get(),
            'DiaDiem'       : detail_box[0].css('.map p a::text').getall(),
            'NgayCapNhat'   : detail_box[1].css('ul li p::text').get(),
            'NganhNghe'     : detail_box[1].css('ul li:nth-child(2) p a::text ').getall(),
            'HinhThuc'      : detail_box[1].css('ul li:nth-child(3) p::text ').get(),
            'Luong'         : detail_box[2].css('ul li:first-child p::text').get(),
            'KinhNghiem'    : detail_box[2].css('ul li:nth-child(2) p::text').get(),
            'CapBac'        : detail_box[2].css('ul li:nth-child(3) p::text').get(),
            'HanNopCV'      : detail_box[2].css('ul li:last-child p::text').get(),
            'PhucLoi'       : job_detail_content[0].css('.welfare-list li::text').getall(),
            'MoTa'          : job_detail_content[1].css('p::text').getall(),
            'YeuCau'        : job_detail_content[2].css('p::text').getall(),
            'ThongTinKhac'  : job_detail_content[3].css('.content_fck ul li::text').getall(),
            'LinkCV'        : response.url
        }

