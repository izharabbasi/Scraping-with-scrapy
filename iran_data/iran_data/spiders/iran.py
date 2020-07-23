# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IranSpider(CrawlSpider):
    name = 'iran'
    allowed_domains = ['www.irct.ir']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'

    def clean_output(self, data):
        try:
            return data.strip()
        except AttributeError:
            return ''

    def start_requests(self):
        yield scrapy.Request(url='https://www.irct.ir/search/result?query=Iran',headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='result-title']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[1]"), process_request='set_user_agent')
    )
   

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='page-header']/h1/text()").get(),
            'summary': self.clean_output(response.xpath("normalize-space(/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/div/dl/dd/div/text())").get()),
            'IRCT_registration_number':self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[1]/dd[2]/div/div[1]/strong/text())").get()),
            'Registration_date': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[1]/dd[2]/div/div[2]/strong/text())").get()),
            'Registration_timing': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[1]/dd[2]/div/div[3]/strong/text())").get()),
            'Last_update': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[1]/dd[2]/div/div[5]/strong/text())").get()),
            'Update_count': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[1]/dd[2]/div/div[6]/strong/text())").get()),
            'Registrant_information_name': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[2]/dd/div/div[1]/div[2]/text())").get()),
            'Name_of_organization_or_entity': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[2]/dd/div/div[2]/div[2]/text())").get()),
            'Country': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[2]/dd/div/div[3]/div[2]/text())").get()),
            'Phone': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[2]/dd/div/div[4]/div[2]/text())").get()),
            'Email_address': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[2]/dd/div/div[5]/div[2]/text())").get()),
            'Recruitment_status': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[3]/dd[1]/strong/text())").get()),
            'Funding_source' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[3]/dd[2]/div/text())").get()),
            'Expected_recruitment_start_date': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[5]/dd[1]/text())").get()),
            'Expected_recruitment_end_date' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[5]/dd[2]/text())").get()),
            'Actual_recruitment_start_date': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[5]/dd[3]/div/text())").get()),
            'Actual_recruitment_end_date' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[5]/dd[4]/div/text())").get()),
            'Trial_completion_date' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[5]/dd[5]/div/text())").get()),
            'Scientific_title': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[6]/dd/text())").get()),
            'Public_title' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[7]/dd[1]/text())").get()),
            'Purpose': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[7]/dd[2]/text())").get()),
            'Inclusion/Exclusion_criteria': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[7]/dd[3]/text())").get()),
            'Age': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[7]/dd[4]/text())").get()),
            'Gender': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[7]/dd[5]/text())").get()),
            'Phase': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[1]/text())").get()),
            'Groups_that_have_been_masked' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[2]/em/text())").get()),
            'Sample_size': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[3]/div/text())").get()),
            'Randomization_(investigators_opinion)' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[4]/text())").get()),
            'Randomization_description' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[5]/text())").get()),
            'Blinding_(investigators_opinion)' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[6]/text())").get()),
            'Blinding_description': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[7]/text())").get()),
            'Placebo': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[8]/text())").get()),
            'Assignment': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[9]/text())").get()),
            'Other_design_features' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/dl[8]/dd[10]/text())").get()),
            'Name_of_ethics_committee' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[1]/div/div[1]/div[2]/text())").get()),
            'Street_address': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[1]/div/div[3]/div[2]/text())").get()),
            'City': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[1]/div/div[5]/div[2]/text())").get()),
            'Postal_code': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[1]/div/div[7]/div[2]/text())").get()),
            'Approval_date': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[2]/text())").get()),
            'Ethics_committee_reference_number': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[4]/div/div/dl/dd[3]/text())").get()),
            'Description_of_health_condition_studied' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[5]/div/div/dl/dd[1]/text())").get()),
            'ICD-10_code': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[5]/div/div/dl/dd[2]/text())").get()),
            'ICD-10_code_description' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[5]/div/div/dl/dd[3]/text())").get()),
            'Primary_outcomes_Description': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[6]/div/div/dl/dd[1]/text())").get()),
            'Timepoint': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[6]/div/div/dl/dd[2]/text())").get()),
            'Method_of_measurement' :self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[6]/div/div/dl/dd[3]/text())").get()),
            'Intervention_groups_Description': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[8]/div/div/dl/dd[1]/text())").get()),
            'Category': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[8]/div/div/dl/dd[2]/text())").get()),
            'Name_of_recruitment_center' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[9]/div/div/dl/dd/div/div[1]/div[2]/text())").get()),
            'recruitment_center_Street_address' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[9]/div/div/dl/dd/div/div[5]/div[2]/text())").get()),
            'recruitment_center_City': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[9]/div/div/dl/dd/div/div[7]/div[2]/text())").get()),
            'Sponsor_Name_of_organization_/_entity' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[1]/div/div[1]/div[2]/text())").get()),
            'Sponsor_Full_name_of_responsible_person' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[1]/div/div[3]/div[2]/text())").get()),
            'Sponsor_Street_address' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[1]/div/div[5]/div[2]/text())").get()),
            'Sponsor_City': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[1]/div/div[7]/div[2]/text())").get()),
            'Is_the_source_of_funding_the_same_sponsor_organization/entity?': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[4]/text())").get()),
            'Title_of_funding_source' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[5]/text())").get()),
            'Proportion_provided_by_this_source': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[6]/text())").get()),
            'Public_or_private_sector' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[7]/i/text())").get()),
            'Domestic_or_foreign_origin' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[8]/i/text())").get()),
            'Category_of_foreign_source_of_funding' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[9]/i/text())").get()),
            'Type_of_organization_providing_the_funding' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[10]/div/div/dl/dd[11]/i/text())").get()),
            'Person_responsible_for_general_inquiries_Name_of_organization_or_entity' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[1]/div[2]/text())").get()),
            'Full_name_of_responsible_person' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[3]/div[2]/text())").get()),
            'responsible_person_Position' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[5]/div[2]/text())").get()),
            'responsible_person_Street_address' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[9]/div[2]/text())").get()),
            'responsible_person_City' : self.clean_output(response.xpath('normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[11]/div[2]/text())').get()),
            'responsible_person_Phone' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[14]/div[2]/text())").get()),
            'responsible_person_Email' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[11]/div/dl/dd/div/div[16]/div[2]/text())").get()),
            'Person_responsible_for_scientific_inquiries_Name_of_organization_or_entity': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[1]/div[2]/text())").get()),
            'Full_name_of_responsible_person_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[3]/div[2]/text())").get()),
            'responsible_person_Position_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[5]/div[2]/text())").get()),
            'responsible_person_Street_address_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[9]/div[2]/text())").get()),
            'responsible_person_City_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[11]/div[2]/text())").get()),
            'responsible_person_Phone_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[14]/div[2]/text())").get()),
            'responsible_person_email_for_scientific_inquiries' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[12]/div/dl/dd/div/div[16]/div[2]/text())").get()),
            'Person_responsible_for_updating_data_Name_of_organization_or_entity': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[1]/div[2]/text())").get()),
            'Full_name_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[3]/div[2]/text())").get()),
            'Position_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[5]/div[2]/text())").get()),
            'Street_address_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[9]/div[2]/text())").get()),
            'City_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[11]/div[2]/text())").get()),
            'Phone_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[14]/div[2]/text())").get()),
            'Email_of_responsible_person_for_updating_data' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[13]/div/dl/dd/div/div[16]/div[2]/text())").get()),
            'Deidentified_Individual_Participant_Data_Set_(IPD)' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[1]/i/text())").get()),
            'Study_Protocol' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[2]/i/text())").get()),
            'Statistical_Analysis_Plan' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[3]/i/text())").get()),
            'Informed_Consent_Form' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[4]/i/text())").get()),
            'Clinical_Study_Report' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[5]/i/text())").get()),
            'Analytic_Code': self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[6]/i/text())").get()),
            'Data_Dictionary' : self.clean_output(response.xpath("normalize-space(//html/body/div[1]/div[3]/div[2]/div[3]/div[14]/div/dl/dd[7]/i/text())").get())
        }
