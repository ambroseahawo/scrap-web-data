import scrapy
from scrapy.http.request import Request
import re
from lxml import html
from web_data.items import WebDataItem

class DataScraperSpider(scrapy.Spider):
    name = "data_scraper"
    allowed_domains = ["business.site"]
    start_urls = []

    def start_requests(self):
        with open("urls.txt", 'r') as urls_file:
            all_urls = urls_file.readlines()
            for each_url in all_urls:
                if self.allowed_domains[0] in each_url:
                    yield Request(str(each_url).strip(), callback=self.parse)
        
    def parse(self, response):
        # link
        # title
        # sub heading
        # button link
        # hero image link
        # testimonials
        # description
        # gallery image links
        # map link
        # phone number
        # get directions link
        # address details
        # business hours
        
        item = WebDataItem()
        
        title = response.xpath('//h1[@class="hero__title hY9UDb "]//span//text()').get()
        # self.log(title)
        item["title"] = title
        
        sub_heading_notification = response.xpath('//div[@class="notification "]//span[@class="notification-content"]//text()').get()
        sub_heading_info = response.xpath('//div[@class="hero__strapline teQaN "]//text()').get()
        sub_heading = f'{sub_heading_notification}, {sub_heading_info}'.encode('ascii', 'ignore').decode('ascii')
        # self.log(sub_heading)
        item["sub_heading"] = sub_heading
        
        hero_button_text = response.xpath('//a[@id="primary_cta"]//span//text()').get()
        hero_button_link = response.xpath('//a[@id="primary_cta"]/@href').get()
        full_text_link = f'{hero_button_text} -> {hero_button_link}'
        # self.log(full_text_link)
        item["button_link"] = full_text_link
        
        hero_image_link = response.xpath('//picture//img/@src').get()
        # self.log(hero_image_link)
        item["hero_image_link"] = hero_image_link
        
        testimonials_section = response.xpath('//div[@class="EIjale"]//div[@class="iTushb"]').getall()
        testimonials_array = []
        
        for each_section in testimonials_section:
            html_section = html.fromstring(each_section)
            try:
                section_quote = html_section.xpath('//q//text()')
                # self.log(section_quote)
                if section_quote == []:
                    section_quote = None
            except:
                section_quote = None
            
            try:
                quote_cite = html_section.xpath('//cite//text()')
                # self.log(quote_cite)
                if quote_cite == []:
                    quote_cite = None
            except:
                quote_cite = None
            if section_quote is not None and quote_cite is not None:
                testimonial = f'"{section_quote[0]}" {quote_cite[0]}'
            elif section_quote is None and quote_cite is not None:
                testimonial = f'{quote_cite[0]}'
            else:
                testimonial = f'"{section_quote[0]}"'
            testimonials_array.append(testimonial)
        testimonials = ', '.join(testimonials_array)
        # self.log(testimonials)
        item["testimonials"] = testimonials
        
        description_title = response.xpath('//span[@class="lead__title-content"]//text()').get()
        description_text_array = response.xpath('//div[@class="lead__summary-content"]//text()').getall()
        description_text = '\n'.join(description_text_array) 
        full_description = f'{description_title}\n{description_text}'
        # self.log(full_description)
        item["description"] = full_description
        
        gallery_images_array = response.xpath('//div[@id="gallery"]//picture//img/@src').getall()
        gallery_images = ', '.join(gallery_images_array)
        # self.log(gallery_images)
        item["gallery_images"] = gallery_images
        
        map_link = response.xpath('//div[@id="details"]//div[@class="IQ1KEb"]//a/@href').get()
        # self.log(map_link)
        item["map_link"] = map_link

        telephone = response.xpath('//div[@id="details"]//div[@data-field="phone"]//a/@href').get()
        # self.log(telephone)
        item['telephone'] = telephone
        
        contact = response.xpath('//div[@id="details"]//div[@data-field="phone"]//ul//li//text()').get()
        # self.log(contact)
        item['contact'] = contact
        
        address_link = response.xpath('//div[@id="details"]//div[@data-field="address"]//a/@href').get()
        # self.log(address_link)
        item['directions_link'] = address_link
        
        extracted_address = response.xpath('//div[@id="details"]//div[@data-field="address"]//address//div//text()').getall()
        address = ', '.join(extracted_address)
        # self.log(address)
        item['address_details'] = address
        
        business_days = response.xpath('//div[@id="details"]//table[@itemprop="openingHours"]//th//text()').getall()
        # self.log(business_days)
        business_hours = response.xpath('//div[@id="details"]//table[@itemprop="openingHours"]//td//span//text()').getall()
        clean_business_hours = []
        hours_pattern = None
        modified_hours_range = None
        
        for index, hours_range in enumerate(business_hours):
            clean_hours_range = hours_range.encode('ascii', 'ignore').decode('ascii')
            if "AM" in str(clean_hours_range):
                hours_pattern = r'AM(\d)'
                modified_hours_range = re.sub(hours_pattern, r'AM - \1', clean_hours_range)
            elif "am" in str(clean_hours_range):
                hours_pattern = r'am(\d)'
                modified_hours_range = re.sub(hours_pattern, r'am - \1', clean_hours_range)
            elif "12:00" in str(clean_hours_range):
                hours_pattern = r'12:00(\d)'
                modified_hours_range = re.sub(hours_pattern, r'12:00 - \1', clean_hours_range)
            else:
                pass
            days_hours = f'{business_days[index]} {modified_hours_range}'
            clean_business_hours.append(days_hours)
        # self.log(clean_business_hours)
        business_days_hours = ', '.join(clean_business_hours)
        # self.log(business_days_hours)
        item['business_hours'] = business_days_hours
        
        item['site'] = response.url
        
        yield item
        