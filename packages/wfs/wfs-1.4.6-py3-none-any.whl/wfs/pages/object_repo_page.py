from poium import Page
from cdxg.logging import log
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from cdxg.appium_lab import AppiumLab
from waiting import wait
import time
import json
import re
from pathlib import Path
import traceback

mypath = Path.cwd()


def get_find_element(driver: WebDriver, element, locate, action_item, text=None):
    locatorx = (locate, element)
    try:
        if text is not None:
            if action_item == 'text' or action_item == 'link_text':
                getalltext = WebDriverWait(driver, 15).until(ec.text_to_be_present_in_element(locatorx, text))
                gtext = None
                if getalltext:
                    gtext = text
                return gtext
        else:
            return WebDriverWait(driver, 15).until(ec.visibility_of_element_located(locator=locatorx))
    except Exception:
        return WebDriverWait(driver, 15).until(ec.presence_of_element_located(locator=locatorx))


def get_find_elements(driver: WebDriver, element, locate, action_item, text=None):
    locatorx = (locate, element)
    try:
        if text is not None:
            if action_item == 'text':
                getalltext = WebDriverWait(driver, 15).until(ec.text_to_be_present_in_element(locatorx, text))
                gtext = None
                if getalltext:
                    gtext = text
                return gtext
        else:
            return WebDriverWait(driver, 15).until(ec.visibility_of_all_elements_located(locator=locatorx))
    except Exception:
        return WebDriverWait(driver, 15).until(ec.presence_of_all_elements_located(locator=locatorx))


class Object_Repo_Page(Page):

    def __int__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def locators_ready(self, greadyx, textn=None):
        elementlocate, action_item = None, None
        locator_identity, element_identity, action_item, fetchlements = greadyx
        if locator_identity == 'id_' and fetchlements == 'S' or locator_identity == 'id' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.ID, action_item, text=textn)
        elif locator_identity == 'id_' and fetchlements == 'M' or locator_identity == 'id' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.ID, action_item, text=textn)
        elif locator_identity == 'xpath' and fetchlements == 'S' or locator_identity == 'XPATH' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.XPATH, action_item, text=textn)
        elif locator_identity == 'xpath' and fetchlements == 'M' or locator_identity == 'XPATH' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.XPATH, action_item, text=textn)
        elif locator_identity == 'apacid' and fetchlements == 'S' or locator_identity == 'APACID' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, AppiumBy.ACCESSIBILITY_ID, action_item)
        elif locator_identity == 'apacid' and fetchlements == 'M' or locator_identity == 'APACID' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.ACCESSIBILITY_ID, action_item)
        elif locator_identity == 'css' and fetchlements == 'S' or locator_identity == 'CSS' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.CSS_SELECTOR, action_item, text=textn)
        elif locator_identity == 'css' and fetchlements == 'M' or locator_identity == 'CSS' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.CSS_SELECTOR, action_item, text=textn)
        elif locator_identity == 'tag' and fetchlements == 'S' or locator_identity == 'TAG' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.TAG_NAME, action_item, text=textn)
        elif locator_identity == 'tag' and fetchlements == 'M' or locator_identity == 'TAG' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.TAG_NAME, action_item, text=textn)
        else:
            if locator_identity == 'class' and fetchlements == 'S' or locator_identity == 'CLASS' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, By.CLASS_NAME, action_item, text=textn)
            elif locator_identity == 'class' and fetchlements == 'M' or locator_identity == 'CLASS' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, By.CLASS_NAME, action_item, text=textn)
            if locator_identity == 'apclass' and fetchlements == 'S' or locator_identity == 'APCLASS' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.CLASS_NAME, action_item,
                                                 text=textn)
            elif locator_identity == 'apclass' and fetchlements == 'M' or locator_identity == 'APCLASS' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.CLASS_NAME, action_item,
                                                  text=textn)
            elif locator_identity == 'apid' and fetchlements == 'S' or locator_identity == 'APID' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.ID, action_item, text=textn)
            elif locator_identity == 'apid' and fetchlements == 'M' or locator_identity == 'APID' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.ID, action_item, text=textn)
            elif locator_identity == 'apxpath' and fetchlements == 'S' or locator_identity == 'apXPATH' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.XPATH, action_item, text=textn)
            elif locator_identity == 'apxpath' and fetchlements == 'M' or locator_identity == 'APXPATH' and fetchlements == 'M':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.XPATH, action_item, text=textn)
            else:
                pass
        # print(elementlocate)
        return elementlocate

    def clickable_element(self, greadyx):
        try:
            locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitem = getjsonlist()
            get_elements_to_find = find_element_click(by=locator_identity, expression=element_identity,
                                                      search_window=self.driver, felements=fetchlements)
            return get_elements_to_find  # find_element_click(by=locator_identity, expression=element_identity, search_window=self.driver)
        except Exception as e:
            raise

    def element_in_frames(self, greadyx):
        locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitems = getjsonlist()
        locatorsplit = locator_identity.split('**')
        # print(locatorsplit)
        frame_locator, dom_locator = locatorsplit
        elementsplit = element_identity.split('**')
        # print(elementsplit)
        frame_element, dom_element = elementsplit
        switch_in_frames(self.driver, frame_element, frame_locator, action_item)
        if dom_locator == 'id_' and fetchlements == 'S' or dom_locator == 'id' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, dom_element, By.ID, action_item)
        elif dom_locator == 'id_' and fetchlements == 'M' or dom_locator == 'id' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, dom_element, By.ID, action_item)
        elif dom_locator == 'xpath' and fetchlements == 'S' or dom_locator == 'XPATH' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, dom_element, By.XPATH, action_item)
        else:
            elementlocate = get_find_elements(self.driver, dom_element, By.XPATH, action_item)
        return elementlocate

    def back_to_default(self):
        self.driver.switch_to.default_content()

    def gethidden(self, greadyx):
        locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitems = getjsonlist()
        if locator_identity in ['css', 'js']:
            return self.driver.execute_script("return document.querySelector('" + str(element_identity) + "')")
        else:
            return 'No elements allowed other than CSS or JS'

    def get_inject_data(self, elements, attriname):
        elementx = []
        if len(elements) > 0:
            for i, element in enumerate(elements):
                random_value = attriname + '_' + str(i)  # f"aaa{i + 1}"
                self.driver.execute_script(f"arguments[0].setAttribute('id', '{random_value}');", element)
                return elementx.append(element)
        else:
            self.driver.execute_script(f"arguments[0].setAttribute('id', '{attriname}');", elements)
            return elementx.append(elements)

    def get_attribute_value(self, element, attribute_name):
        return self.driver.execute_script(f"return arguments[0].getAttribute('{attribute_name}');", element)

    def get_attribute_values(self, element):
        # Get all attributes and their values for the element
        element_attributes = self.driver.execute_script(
            "var items = {}; "  # Create an empty JavaScript object
            "for (var i = 0; i < arguments[0].attributes.length; i++) { "
            "  items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value; "
            "} "
            "return items;", element)

        # Print the attributes and their values
        xattrib = []
        for attribute, value in element_attributes.items():
            xattrib.append(f"{attribute}: {value}")
        return xattrib

    def set_attributes_values(self, elements, attribValues, btnname=None):
        # Define the custom attribute name and values
        try:
            attribute_name = "id"
            # attribute_values = attribValues  # Replace with your desired values
            # Iterate through the elements and set the custom attribute with distinct values
            xattrib = []
            # for i, element in enumerate(elements):
            for i in range(0, len(elements)):
                element = elements[i]
                if btnname is None:
                    attribute_value = attribValues + str(i + 1)
                else:
                    attribute_value = attribValues[i]
                self.driver.execute_script(f"arguments[0].setAttribute(arguments[1], arguments[2]);", element,
                                           attribute_name,
                                           attribute_value)
                xattrib.append(f"element {i + 1} to: {attribute_name}: {attribute_value}")
                getsourcehtml = self.getHtmlsource(id=attribute_value)
                print(getsourcehtml)
                # print(f"Set {attribute_name} for element {i + 1} to: {attribute_value}")
            return xattrib, attribute_value
        except Exception as e:
            raise

    def getHtmlsource(self, id=None, xpath=None):
        try:
            if id:
                script = f"return document.querySelector('#{id}').outerHTML;"
                outerHTML = self.driver.execute_script(script)

            if xpath:
                # Use an Explicit Wait to wait for the element to be present
                element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, xpath)))
                # Now, you can execute the JavaScript to get the outerHTML
                script = f"return arguments[0].outerHTML;"
                outerHTML = self.driver.execute_script(script, element)

            if outerHTML:
                return f"outerHTML of the element: {outerHTML}"
            else:
                return "Element not found."
        except Exception as e:
            raise

    def get_source_xpath(self, greadyx=None, textmatch=None, refkey=None, action=None, felem=None):
        try:
            if textmatch and greadyx[0] == 'xpath':
                if len(textmatch) == 2 and action  in ['type', 'select']:
                    # texta,placeb = str(textmatch).split(',')
                    texta = textmatch
                    holdt = "//*[text()='" + texta[0] + "']/..//*[@placeholder='" + texta[1] + "']"
                    log.info('Locate Selector : '+str(holdt))
                else:
                    texta = textmatch
                    if refkey == 2 and action == 'type':
                        holdt = "//*[@placeholder='"+texta[0]+"']"
                    elif refkey == 3 and action == 'type':
                        holdt = "//*[text()='" + texta[0] + "']/..//*[@placeholder]"
                    elif refkey == 5 and action == 'click':
                        holdt = "//*[text()='" + texta[0] + "']/..//*[@role='combobox']"
                    else:
                        holdt = "//*[text()='"+texta[0]+ "']"
                    log.info('Locate Selector : ' + str(holdt))

            def getHold(pathlocate):
                if pathlocate:
                    pathlocate = (greadyx[0], pathlocate, *greadyx[2:])
                    getelementx = self.get_elements(greadyx=pathlocate)
                    outerHTML = []
                    for elementx in getelementx:
                        script = f"return arguments[0].outerHTML;"
                        outer = self.driver.execute_script(script, elementx)
                        outerHTML.append(outer)

                return outerHTML, pathlocate

            hsource, pathlocator = getHold(pathlocate=holdt)
            if len(hsource) > 1 and felem != 'M':
                return 'Error : InvalidSelector >> find the exact to locate selector element or no placeholder ' \
                       'attribute defined for if textbox or textarea, so use usual way of Selector as normal as ' \
                       '//xpath[@type=button] or css selector or id'
            else:
                return pathlocator
        except Exception as e:
            raise

    def all_texts_page(self, getcount=None, gxcount=None):
        galltext = []

        def deffx(text_lines):
            for line in text_lines:
                if line.strip():  # Filter out empty lines
                    # print(line.strip())
                    galltext.append(line.strip())
            return galltext

        if gxcount is None:
            # Execute JavaScript to retrieve all text content on the page
            all_text_inner = self.driver.execute_script("return document.documentElement.innerText")
            text_lines_inner = all_text_inner.split('\n')
            all_text_outer = self.driver.execute_script("return document.documentElement.outerText")
            # Split the text into lines (you can process it further as needed)
            text_lines_outer = all_text_outer.split('\n')
            # Convert both lists to sets to remove duplicates
            if getcount:
                set_AA = deffx(text_lines_outer)
                merged_list = get_text_count(glist=set_AA)
            else:
                set_AA = set(deffx(text_lines_outer))
                set_BB = set(deffx(text_lines_inner))
                # Merge the sets and convert them back to a list
                merged_list = list(set_AA.union(set_BB))
            return merged_list
        else:
            set_AA = deffx(gxcount)
            merged_list = get_text_count(glist=set_AA)
            return merged_list

    def upload_file_data(self, elempath='input[type=file]'):
        uploaddata = f"""
        function uploadFile() {{
            var fileInput = document.querySelector('{elempath}');
            fileInput.style.display = 'block';
            fileInput.style.visibility = 'visible';
        }}
        uploadFile();
        """
        self.driver.execute_script(uploaddata)

    def get_elements(self, greadyx):
        try:
            getlocator = elementRef(locatorIdentity=greadyx[0])
            locatorx = (getlocator, greadyx[1])
            # getelements = WebDriverWait(self.driver, 30).until(ec.presence_of_all_elements_located(locatorx))
            getelements = get_presented_elements(self.driver, locatorx)
            # print(getelements)
            return getelements
        except Exception as e:
            traceback.print_exc()

    def get_element(self, greadyx):
        try:
            getlocator = elementRef(locatorIdentity=greadyx[0])
            locatorx = (getlocator, greadyx[1])
            # getelements = WebDriverWait(self.driver, 30).until(ec.presence_of_all_elements_located(locatorx))
            getelements = get_presented_elements(self.driver, locatorx)
            return getelements
        except Exception as e:
            traceback.print_exc()

    def get_inject_mobile_data(self, elements, attriname, ptname):
        element_attribute = elements
        element_value = attriname
        elementx = []
        if len(elements) > 0:
            if ptname == 'Android':
                for i, element in enumerate(elements):
                    random_value = attriname + '_' + str(i)  # f"aaa{i + 1}"
                    self.driver.execute_script('mobile: shell', {
                        'command': 'input',
                        'args': ['text', f'new UiSelector().description("{element_attribute}={element_value}")']
                    })
                    return elementx.append(element)
        else:
            self.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', f'[{element_attribute}="{element_value}"]']
            })
            return elementx.append(elements)
        # Android
        # element = driver.find_element(MobileBy.XPATH, f'//*[@content-desc="{element_attribute}={element_value}"]')
        # iOS
        # element = driver.find_element(MobileBy.XPATH, f'//*[@{element_attribute}="{element_value}"]')

    def getscrolled(self, elementx):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elementx)

    def get_action_chains(self):
        return ActionChains(self.driver)

    def go_to_previous_page(self, hide_keyboard: bool = False):
        if hide_keyboard:
            self.hide_keyboard()
        self.driver.back()

    def hide_keyboard(self):
        wait(lambda: self.driver.is_keyboard_shown(),
             timeout_seconds=10)
        self.driver.hide_keyboard()

    def get_current_url(self):
        return self.driver.current_url

    def get_touch_actions(self):
        return TouchAction(self.driver)

    def get_appium_lab(self):
        return AppiumLab(self.driver)

    def screen_shots(self, screenshot_path):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenName = f"failure_{screenshot_path}_{timestamp}.png"
        snamex = mypath / 'reports' / 'screenshots' / screenName
        self.driver.save_screenshot(str(snamex))
        return snamex

    def get_alert(self):
        getxx = self.driver.execute_cdp_cmd('Runtime.evaluate', {'expression': "alert('hello world')"})
        return getxx

    def get_endpoint_list(self, target):
        response_body_list = []
        request_log = self.driver.get_log('performance')
        for i in range(len(request_log)):
            message = json.loads(request_log[i]['message'])
            message = message['message']['params']
            try:
                request = message['request']
            except KeyError:
                continue
            current_url = request['url']
            current_method = request['method']
            if target in current_url:
                response_body_list.append({
                    'currentURL': current_url,
                    'method': current_method
                })
                headers = request.get('headers', {})
                if 'Authorization' in headers:
                    desired_lines = headers
        return response_body_list, desired_lines

    def get_response_body_list(self, api_url):
        response_body_list = []
        options = []
        resprec = []
        gxa = []
        request_log = self.driver.get_log('performance')
        for i in range(len(request_log)):
            aaxmessage = json.loads(request_log[i]['message'])
            if aaxmessage['message']['method'] == 'Network.responseReceived':
                msgg = aaxmessage['message']['params']
                request = msgg['response']['url']
                if request.find(api_url) != -1:
                    requestid = msgg['requestId']
                    try:
                        method = msgg['response']['headers']['access-control-allow-methods']
                    except Exception as e:
                        method = 'XXX'
                    allx = requestid, method, request
                    resprec.append(allx)
            else:
                bbxmessage = aaxmessage['message']['params']
                try:
                    requestxxm = bbxmessage['request']
                except KeyError:
                    continue
                current_url = requestxxm['url']
                current_method = requestxxm['method']
                if api_url in current_url and current_method in ['GET', 'POST', 'PUT']:
                    current_reqid = bbxmessage['requestId']
                    allx = current_reqid, current_method, current_url
                    options.append(allx)
        for recv in resprec:
            for opn in options:
                if recv[2] == opn[2]:
                    xlta = recv[0], opn[1], recv[2]
                    gxa.append(xlta)
        for xid in gxa:
            try:
                response = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': xid[0]})
                response_body_list.append({
                    'response_body': response['body'],
                    'url': xid[2],
                    'method': xid[1]
                })
            except:
                next
        # print(response_body_list)
        return response_body_list

    def getdetailsResponse_body(self, api_url):
        logs_json = []
        responses = []
        response_body_list = []
        logs = self.driver.get_log("performance")
        body = ""
        for log in logs:
            logs_json.append(json.loads(log["message"])["message"])
        for log in logs_json:
            if (log['method'] == 'Network.responseReceived'):
                responses.append(log['params'])
        for response in responses:
            if (response['response']['url'].find(api_url) != -1):  # if right request load body then
                # Use second request first is expaired with cookies.
                try:
                    body = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": response['requestId']})
                    json_body = json.loads(body['body'])
                    # print(json_body)
                    response_body_list.append({
                        'response_body': json_body,
                        'url': response['response']['url']
                    })
                except:
                    next
        return response_body_list

    def success_call_back(self, locatorx):

        def success_callback(element):
            return element.text

        def error_callback(e):
            return f"An error occurred: {str(e)}"

        # Example usage: Wait for an element to be visible and get its text
        result = custom_wait(
            self.driver,
            timeout=10,
            condition=ec.visibility_of_element_located(locatorx),
            success_callback=success_callback,
            error_callback=error_callback
        )
        ec.visibility_of_element_located()


def object_repox(driver):
    return Object_Repo_Page(driver)


def find_element_click(by, expression, search_window=None, timeout=32, ignore_exception=None, poll_frequency=4,
                       felements=None):
    if ignore_exception is None:
        ignore_exception = []

    ignore_exception.append(NoSuchElementException)
    end_time = time.time() + timeout
    while True:
        try:
            by = elementRef(locatorIdentity=by)
            if felements == 'S':
                # web_element = WebDriverWait(search_window, 10).until(ec.element_to_be_clickable((by, expression)))
                # print(web_element)
                web_element = search_window.find_element(by=by, value=expression)
                search_window.execute_script("arguments[0].click();", web_element)
                return 'YY'
            else:
                web_element = search_window.find_elements(by=by, value=expression)
                # web_element.click()
                return web_element
        except tuple(ignore_exception) as e:
            if time.time() > end_time:
                time.sleep(poll_frequency)
                break
        except Exception as e:
            raise
    return 'NN'


def switch_in_frames(driver: WebDriver, element, locate, action_item):
    # print(element, locate, action_item)
    locatorx = (locate, element)
    return WebDriverWait(driver, 30).until(ec.frame_to_be_available_and_switch_to_it(locator=locatorx))


def wait_for_element_to_vanish(webelement):
    is_displayed = webelement.is_displayed()
    start_time = get_current_time_in_millis()
    time_interval_in_seconds = 5
    while is_displayed and not is_time_out(start_time, time_interval_in_seconds):
        is_displayed = webelement.is_displayed()
    return not is_displayed


def click_until_interactable(webelement):
    element_is_interactable = False
    start_time = get_current_time_in_millis()
    counter = 1
    if webelement:
        while not element_is_interactable and not is_time_out(start_time, 10):
            try:
                webelement.click()
                element_is_interactable = True
            except (ElementNotInteractableException, ElementClickInterceptedException) as e:
                counter = counter + 1
    return element_is_interactable


def get_current_time_in_millis():
    return 10000


def is_time_out(start_time_millis, waiting_interval_seconds):
    return start_time_millis + waiting_interval_seconds * 1000


def elementRef(locatorIdentity):
    if locatorIdentity == 'apclass':
        return AppiumBy.CLASS_NAME
    if locatorIdentity == 'apacid':
        return AppiumBy.ACCESSIBILITY_ID
    if locatorIdentity == 'apid':
        return AppiumBy.ID
    if locatorIdentity == 'apxpath':
        return AppiumBy.XPATH
    if locatorIdentity == 'class':
        return By.CLASS_NAME
    if locatorIdentity == 'css':
        return By.CSS_SELECTOR
    if locatorIdentity == 'id_':
        return By.ID
    if locatorIdentity == 'xpath':
        return By.XPATH


def get_text_count(glist):
    AAA = glist
    # Create a dictionary to store counts
    item_counts = {}
    for item in AAA:
        item = item.strip()  # Remove leading/trailing whitespace
        item_counts[item] = item_counts.get(item, 0) + 1
    # Format the counts
    formatted_counts = []
    for item, count in item_counts.items():
        formatted_counts.append(f"{item}({count})")
    # Join the formatted counts into a single string
    # output = ', '.join(formatted_counts)
    print(formatted_counts)
    return formatted_counts


def custom_wait(driver, timeout, condition, success_callback, error_callback):
    try:
        element = WebDriverWait(driver, timeout).until(condition)
        return success_callback(element)
    except Exception as e:
        return error_callback(e)


def custom_wait_for_elements(driver, timeout, conditions):
    for condition in conditions:
        try:
            elements = WebDriverWait(driver, timeout).until(condition)
            if elements:
                return elements
        except Exception as e:
            continue
    raise Exception("None of the conditions were met")


def get_presented_elements(driver, locatorsx):
    # Define the conditions you want to check in order
    conditions = [
        ec.visibility_of_all_elements_located(locatorsx),
        ec.visibility_of_any_elements_located(locatorsx),
        ec.presence_of_all_elements_located(locatorsx),
    ]
    try:
        elements = custom_wait_for_elements(driver, timeout=10, conditions=conditions)
        return elements
        # for element in elements:
        #    print(element.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_presented_element(driver, locatorsx):
    # Define the conditions you want to check in order
    conditions = [
        ec.visibility_of_element_located(locatorsx),
        ec.presence_of_element_located(locatorsx),
    ]
    try:
        elements = custom_wait_for_elements(driver, timeout=10, conditions=conditions)
        return elements
        # for element in elements:
        #    print(element.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
