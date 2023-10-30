def snp_dw(location):
    import time
    print("welcome users\n")
    time.sleep(3)
    print(
        "Do read the docunetation on pypi to understand it better")
    time.sleep(5)
    print("\n\n","make sure we are using chrome browser and don't worry about your chrome version ,its all now automated")
    time.sleep(3)
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    import os
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # setting up driver

    "Taking in the locus id"
    locus = open(location, "r")
    for i in locus:

        "Setting Up elements and locus"
        driver.get("https://snp-seek.irri.org/_snp.zul")
        Genelocus = driver.find_element(By.XPATH,
                                        "/html/body/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/div/div/table/tbody[1]/tr[4]/td[2]/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td[3]/span/input")
        search_button = driver.find_element(By.XPATH,
                                            "/html/body/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/div/div/table/tbody[1]/tr[5]/td[3]/div/table/tbody/tr/td/table/tbody/tr[1]/td/button")
        csv_button = driver.find_element(By.XPATH,
                                         "/html/body/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td/table/tbody/tr[3]/td/div/div[2]/div[1]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[3]/button")
        time.sleep(2)

        Genelocus.send_keys(i)
        driver.implicitly_wait(30)
        try:
            search_button.click()
            csv_button.click()
            time.sleep(5)
        except:
            print(i, "not found")
            continue
        # driver.implicitly_wait(1000)
        # csv_button.click()

        # driver.implicitly_wait(1000)
        # time.sleep(5)

    driver.quit()
    print("Thanks for using our program\n\nAuthor @Sudipan Paul")





