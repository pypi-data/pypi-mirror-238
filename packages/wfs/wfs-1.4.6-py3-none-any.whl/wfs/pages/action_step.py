import re
from wfs.utils.parseexcel import ParseExcel
from wfs.utils.common import id_generator, check_word_order, getaction_datalist, get_action_dict, getlocator_direct


def get_test_steps(test_object_repo, test_data_json, tstepx, steps_line, testdata, action, actiondesc, ptname):
    try:
        data = None
        action_data = action.split('\n')

        if str(action_data[steps_line]).startswith('@'):
            data = get_at_startoff(test_object_repo, steps_line, testdata, action, actiondesc, tstepx, ptname)
        else:
            if '|' not in action:
                ### Not for mobile app tests only portal based tests
                data = get_no_pipe(steps_line, testdata, action, actiondesc, tstepx, ptname)
            else:
                data = get_with_pipe(test_object_repo, steps_line, testdata, action, actiondesc, tstepx, ptname)
            # print(data)
        return data
    except Exception as e:
        return 'Error : ' + str(e)


def get_pipe_extractor(getdescp, tstepx, action_item, test_data_item, actionxdesc):
    data = []
    if len(getdescp) == 1:
        elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity = getdescp[0]
        datax = locatorIdentity + '|' + elementIdentity + '|' + actionIdentity + '|' + actionxdesc + '|' + \
                tstepx + '|' + action_item + '|' + test_data_item + '|' + felements + '|' + itemIdentity + \
                '|' + id_generator()
        data.append(datax)
        # jsonfile.write(str(datax) + '\n')
    else:
        for xdata in range(len(getdescp)):
            elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity = \
                getdescp[xdata]
            # print(elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity)
            aItem, tItem = str(action_item).split('&'), str(test_data_item).split('&')
            datax = locatorIdentity + '|' + elementIdentity + '|' + actionIdentity + '|' + description + '|' + \
                    tstepx + '|' + aItem[xdata] + '|' + tItem[
                        xdata] + '|' + felements + '|' + itemIdentity + \
                    '|' + id_generator()
            data.append(datax)
    return data


def get_action_description(get_excel_data, action_description, ptname):
    getdesp = []
    if '&' in action_description:
        get_action = action_description.split('&')
        for actiondesc in get_action:
            for xdescrip in range(0, len(get_excel_data)):
                if get_excel_data[xdescrip]['Description'] == actiondesc:
                    if ptname in ['Android', 'iOS']:
                        if ptname == 'Android':
                            elementIdentity = get_excel_data[xdescrip]['Elements1']
                        else:
                            elementIdentity = get_excel_data[xdescrip]['Elements2']
                    else:
                        elementIdentity = get_excel_data[xdescrip]['Elements']
                    locatorIdentity = get_excel_data[xdescrip]['Locators']
                    actionIdentity = get_excel_data[xdescrip]['Action']
                    description = get_excel_data[xdescrip]['Description']
                    felements = get_excel_data[xdescrip]['FetchElements']
                    itemIdentity = get_excel_data[xdescrip]['Item']
                    getx = elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity
                    getdesp.append(getx)
                    # print(getdesp)
    else:
        for xdescrip in range(0, len(get_excel_data)):
            if action_description == get_excel_data[xdescrip]['Description']:
                if ptname in ['Android', 'iOS']:
                    if ptname == 'Android':
                        elementIdentity = get_excel_data[xdescrip]['Elements1']
                    else:
                        elementIdentity = get_excel_data[xdescrip]['Elements2']
                else:
                    elementIdentity = get_excel_data[xdescrip]['Elements']
                locatorIdentity = get_excel_data[xdescrip]['Locators']
                actionIdentity = get_excel_data[xdescrip]['Action']
                description = get_excel_data[xdescrip]['Description']
                felements = get_excel_data[xdescrip]['FetchElements']
                itemIdentity = get_excel_data[xdescrip]['Item']
                getx = elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity
                getdesp.append(getx)
                break
    # print(getdesp)
    return getdesp


def get_test_action_data(steps_line, testdata, action, actiondesc):
    testdata = testdata.split('\n')
    testxdata = testdata[steps_line]

    actiondata = action.split('\n')
    actionxdata = actiondata[steps_line].split('|')

    actiondesc = actiondesc.split('\n')
    actionxdesc = actiondesc[steps_line]
    return testxdata, actionxdata[0], actionxdata[1], actionxdata[2], actionxdesc, actionxdata


def get_at_startoff(test_object_repo, steps_line, testdata, action, actiondesc, tstepx, ptname):
    action_data = action.split('\n')
    gat, actiondata = str(action_data[steps_line]).split('@')
    testdata = testdata.split('\n')
    test_data_item = testdata[steps_line]
    actiondesc = actiondesc.split('\n')
    actionxdesc = actiondesc[steps_line]
    matches = None
    if ('{' in actionxdesc or '}' in actionxdesc) or ('*' in actionxdesc):
        pattern = r'[{*](.*?)[}*]'
        # Use re.findall to extract the words
        matches = re.findall(pattern, actionxdesc)

    if actiondata in ['url', 'xurl']:
        data = ['None|None|None|' + actionxdesc + '|' + \
                tstepx + '|' + actiondata + '|' + test_data_item + '|None|None|' + id_generator()]
    else:
        get_excel_data = ParseExcel(test_object_repo).get_values_by_key('Description', aname=actiondata)
        print('Before: ' + str(get_excel_data))
        for item in range(len(get_excel_data)):
            if matches:
                if len(matches) > 1:
                    action_item = '&'.join(matches)
                # print(action_item)
                if matches[item] != 'xx':
                    get_excel_data[item]['Action'] = matches[item]
            else:
                action_item = get_excel_data[item]['Action']
        print('After: ' + str(get_excel_data))

        getdescp = get_action_description(get_excel_data, actiondata, ptname)

        data = get_pipe_extractor(getdescp, tstepx, action_item, test_data_item, actionxdesc)

    return data


def get_no_pipe(steps_line, testdata, action, actiondesc, tstepx, ptname):
    input_string, testdata, actiondesc = getaction_datalist(action, steps_line, testdata, actiondesc)
    data = []
    if 'then' in input_string:
        getacn = str(input_string).split('then')
        getdatatest = str(testdata).split('|')
        for xaction in range(0, len(getacn)):
            actionx = check_word_order(getacn[xaction])
            action, daction, felem = get_action_dict(actionx)
            data.append(
                'xpath|' + str(getacn[xaction]) + '|' + str(action) + '|click_find_enter|' + str(tstepx) + '|' +
                str(action) + '|' + str(getdatatest[xaction]) + '|' + str(felem) + '|' + str(actiondesc) + '|XXXX')
    else:
        actionx = check_word_order(input_string)
        action, daction, felem = get_action_dict(actionx)
        if action in ['url', 'xurl']:
            data.append('None|None|None|' + actiondesc + '|' + \
                        tstepx + '|' + action + '|' + testdata + '|None|None|' + id_generator())
        else:
            data.append(
                'xpath|' + str(input_string) + '|' + str(action) + '|click_find_enter|' + str(tstepx) + '|' + str(
                    action) + '|' + str(testdata) + '|' + str(felem) + '|' +
                str(actiondesc) + '|XXXX')
    return data


def get_with_pipe(test_object_repo, steps_line, testdata, action, actiondesc, tstepx, ptname):
    test_data_item, action_no, action_page_item, action_item, actionxdesc, actiondata = get_test_action_data(steps_line,
                                                                                                             testdata,
                                                                                                             action,
                                                                                                             actiondesc)
    getaction_details = getlocator_direct(action=actiondata, desptn=actionxdesc)
    if getaction_details is None:
        get_excel_data = ParseExcel(test_object_repo).get_values_by_key('BasePage', action_page_item, 'Description',
                                                                        actionxdesc)
        getdescp = get_action_description(get_excel_data, actionxdesc, ptname)
    else:
        getdescp = getaction_details
    if test_data_item != "***" and action_item != "***" and action_no != '00' or test_data_item == "***" and \
            action_item != "***" and action_no != '00':
        data = get_pipe_extractor(getdescp, tstepx, action_item, test_data_item, actionxdesc)
    elif action_no == '00' and action_item != "***":
        data = ['None|None|None|' + actionxdesc + '|' + \
                tstepx + '|' + action_item + '|' + test_data_item + '|None|None|' + id_generator()]
    else:
        pass
        # data = data
    return data
