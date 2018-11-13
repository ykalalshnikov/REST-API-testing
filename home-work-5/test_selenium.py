def test_search_example(selenium):
    """ 1) Search some phrase in duckduckgo
        2) Click on the first element of search result
        3) Make a screenshot of the page. """

    # Open duckduckgo search page:
    selenium.get('https://duckduckgo.com')

    # Find the field for search text input:
    search_input = selenium.find_element_by_id('search_form_input_homepage')

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('python')

    # Click search button:
    search_button = selenium.find_element_by_id('search_button_homepage')
    search_button.click()

    # Click on the first element
    elem1 = selenium.find_element_by_id("r1-0")
    elem1.click()

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')
