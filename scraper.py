from selenium import webdriver
from selenium.webdriver.common.by import By

# set cookie shit here
"""
Name: string
Byline: string
Description: string
Location: string
Education: array[
School Name : string
degree : string
start : string/unix timestamp
end : string/unix timestamp
]
"""


class Scrapper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        #self.token = token

    def run(self, URL: str):
        self.driver = webdriver.Chrome( options=self.options)
        try:
            self.driver.get("https://www.linkedin.com/login")
            self.driver.find_element(
                    By.XPATH, "//input[@id='username']"
                ).send_keys(self.email)
            self.driver.find_element(
                By.XPATH, "//input[@id='password']"
            ).send_keys(self.password)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            try:
    #            self.driver.get("https://www.linkedin.com")
    #            self.driver.add_cookie({"name": "li_at", "value": self.token})
                self.driver.get(URL)
            except Exception as e:
                print("ERROR UNABLE TO GET INFO")
                print(e)
            self.driver.implicitly_wait(5)
            name = (
                self.driver.find_element(
                    By.XPATH, "//div[@class='dCPfpVvGRbxtgoRoBjKZHhpzpsWnyaSqjgQ']/span/a/h1"
                )
                .text
            )
            byline = self.driver.find_element(
                By.XPATH, "//div[@class='text-body-medium break-words']"
            ).text
            location = (
                self.driver.find_element(
                    By.XPATH, "//div[@class='iOFQhnpWXJcOwLVMAcmqeWnUpOWvCXysrcQ mt2']"
                )
                .find_elements(By.TAG_NAME, "span")[0]
                .text
            )
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(2)
            about = (
                self.driver.find_element(By.XPATH, "//div[@class='display-flex ph5 pv3']")
                .find_elements(By.TAG_NAME, "span")[0]
                .text
            )
            pfp_link = self.driver.find_element(
                By.XPATH,
                "//div[@class='pv-top-card__non-self-photo-wrapper ml0']/button/img",
            ).get_attribute("src")
            print(
                "name",
                name,
                "\nbyline",
                byline,
                "\nlocation",
                location,
                "\nabout",
                about,
                "\npfp_link",
                pfp_link,
            )
            education_list = self.driver.find_elements(
                By.XPATH,
                "//div[@id='education']/../div[@class='pvs-list__outer-container']/ul/*",
            )
            educations = []
            for element in education_list:
                url_link = element.find_element(By.TAG_NAME, "img").get_attribute("src")
                uni_name = element.find_elements(By.TAG_NAME, "span")[0].text
                try:
                    year_period = element.find_element(
                        By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']"
                    ).text
                except Exception as e:
                    year_period = None
            #print(
            #    "url_link",
            #    url_link,
            #    "\nuni_name",
            #    uni_name,
            #    "\nyear_period",
            #    year_period,
            #)
                educations.append(
                    {"URL": url_link, "name": uni_name, "year_period": year_period}
                )
            experience_list = self.driver.find_elements(
                By.XPATH,
                "//div[@id='experience']/../div[@class='pvs-list__outer-container']/ul/li",
            )
            experiences = []
            #print("\nExperiences",experience_list,"\nlength", len(experience_list))
            for element in experience_list:
                url_link = element.find_element(By.TAG_NAME, "img").get_attribute("src")
                company_role = element.find_elements(
                    By.XPATH,
                ".//div/div/div/div/div/div/div/div/span",
                )[0].text
                company_name = element.find_elements(
                    By.XPATH,
                    ".//div/div/div/div/span[@class='t-14 t-normal']/span",
                )[0].text
                try:
                    company_year_period = (
                        element.find_elements(
                        By.XPATH,
                        ".//div/div/div/div/span[@class='t-14 t-normal t-black--light']/span",
                    )[0]
                    .text
                    )
                except Exception as e:
                    print("error", e)
                    company_year_period = None
            #try:
            #    company_location = (
            #        element.find_elements(
            #            By.XPATH,
            #            "//div[@class='display-flex flex-column full-width']/span[@class='t-14 t-normal t-black--light']",
            #        )[1]
            #        .find_elements(By.TAG_NAME, "span")[0]
            #        .text
            #    )
            #except Exception as e:
            #    print("error", e)
            #    company_location = ""
            #print(
            #   "url_link",
            #    url_link,
            #    "\ncompany_role",
            #    company_role,
            #    "company_year_period",
            #    company_year_period,
            #    "company_name",
            #    company_name,
                #"company_location",
                #company_location,
            #)
                experiences.append({
                    "URL" : url_link,
                    "role" : company_role,
                    "year_period" : company_year_period,
                    "name" : company_name,
                    #"location" : company_location
                })
            self.driver.quit()
            return {
                "name": name,
                "byline": byline,
                "location": location,
                "description": about,
                "pfp_link": pfp_link,
                "educations": educations,
                "experiences" : experiences,
            }
        except Exception as e:
            print("error: ", e)
            self.driver.quit()


if __name__ == "__main__":
    # test shit
    x = Scrapper(
        "AQEDAUw0o-sBBMRhAAABjfyBtCUAAAGOII44JU0A0TBi7c2jZD2-KIXV2L8gHjBPPikrzGrmStescEUmTZ-QGKewxlMBBY_5OOdzWy0MYhATjo8fOkaeJBdf6uVrKkbYlVTRCT1d6hE-RmCOprw177K3"
    )
    x.run("https://www.linkedin.com/in/williamhgates/")
