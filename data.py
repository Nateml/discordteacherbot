from urllib.request import urlopen, Request
import urllib.request
import re

class Summary(object):
    
    def __init__(self):
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        with urlopen(Request(url="https://www.worldometers.info/coronavirus/", headers=headers)) as source: #opens covid-19 stat page
            self.html = source.read().decode() # read, convert bytes to string

            self.deaths = re.findall("([0-9,]+)(?= Deaths)", self.html)[0] #deaths
            self.tot_cases = re.findall("([0-9,]+)(?= Cases)", self.html)[0] #total cases

            active_case_index = self.html.find("Active Cases") #index where string "Active Cases" is found
            ac_patch = self.html[active_case_index:]
            self.active_cases = re.findall("(?<=\"number-table-main\">)[0-9,]+", ac_patch)[0]

    def country(self, country):
        country_patch = re.findall(">%s<.+?</tr>" % country, self.html, re.DOTALL) #get all html for the country's row in the websites table
        #country_patch = self.html[country_index:]
        columns = re.findall("\">[0-9,\\+]+?</td>|\">.*?</td>" , country_patch[0], re.DOTALL) #seperate each column
        nums = []
        for column in columns: ##isolate number in each column of country's row and append to list nums
            try:
                num = re.findall("[0-9,]+", column, re.DOTALL)[0]
                nums.append(num)
            except(IndexError):
                nums.append("0")
        
        
        

        self.country_data = {}
        self.country_data["total_cases"] = nums[0]
        self.country_data["new_cases"] = nums[1]
        self.country_data["total_deaths"] = nums[2]
        self.country_data["total_recovered"] = nums[3]
        self.country_data["active_cases"] = nums[4]
        self.country_data["serious_cases"] = nums[5]
        self.country_data["cases_per_mill"] = nums[6]


    def localSit(self):
        return ("%s TOTAL CASES \n%s NEW CASES\n%s DEATHS" % (self.country_data["total_cases"], self.country_data["new_cases"], self.country_data["total_deaths"]))


    def __str__(self):
        return ("%s DEATHS \n%s ACTIVE CASES \n%s TOTAL CASES" % (self.deaths, self.active_cases, self.tot_cases))