import configparser
import os
import random
import string
import time
import xlrd
import ffmpeg
from wfs.utils.parseexcel import ParseExcel
from pathlib import Path

mypath = Path.cwd()
data_file_path = mypath / "conf.ini"
config = configparser.ConfigParser()


def readlastine(filepath):
    with open(filepath, 'r') as f:
        last_linex = f.readlines()
        if len(last_linex) == 1:
            last_line = last_linex[0]
        elif len(last_linex) > 1:
            last_line = last_linex[-1]
        else:
            last_line = 'NA'
    return last_line


def generate_object_repo(test_object_repo, test_generate):
    getallxm = ParseExcel(test_object_repo).get_all_rows_columns_data()
    # log.info('Fetch all Generate Object repo: ' + str(getallxm))
    with open(test_generate, 'w') as f:
        f.write('from poium import Page, Element, Elements\n\n\n')
        f.write('class Object_Repo_Page(Page):\n\n')
        for getxl in getallxm:
            if getxl['BasePage'] is not None and getxl['BasePage'] != 'BasePage':
                if getxl['FetchElements'] == 'M':
                    felements = 'Elements'
                else:
                    felements = 'Element'
                f.write(
                    '\telement_' + getxl['Description'] + ' = ' + str(felements) + '(' + getxl['Locators'] + '="' +
                    getxl['Elements'] + '", describe="' + getxl['Description'] + '")\n')
        f.close()


def delete_line_with_word(file_name, word):
    """Delete lines from a file that contains a given word / sub-string """
    delete_line_by_condition(file_name, lambda x: word in x)


def delete_line_by_condition(original_file, condition):
    """ In a file, delete the lines at line number in given list"""
    dummy_file = original_file + '.bak'
    is_skipped = False
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # if current line matches the given condition then skip that line
            if condition(line) == False:
                write_obj.write(line)
            else:
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)


def getData(xlFilename, sheetname):
    data = []
    wbook = xlrd.open_workbook(xlFilename)
    sheet = wbook.sheet_by_name(sheetname)
    for i in range(1, sheet.nrows):
        data.append([sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3),
                     sheet.cell_value(i, 4), sheet.cell_value(i, 5), sheet.cell_value(i, 6), sheet.cell_value(i, 7),
                     sheet.cell_value(i, 8), sheet.cell_value(i, 9), sheet.cell_value(i, 10)])
    # print(data)
    return data


def get_all_data(xlfilename, sheetname):
    wbook = ParseExcel(xlfilename)
    sheet = wbook.set_sheet_by_name(sheetname)
    totalrows = sheet.max_row
    totalcols = sheet.max_column
    sheet_data = []

    for rows in sheet.iter_rows():
        row_cells = []
        for cell in rows:
            row_cells.append(cell.value)
        sheet_data.append(row_cells)
    datasheet = []
    for i in range(2, len(sheet_data) + 1):
        datalist = []
        for j in range(1, totalcols + 1):
            data = sheet.cell(row=i, column=j).value
            datalist.insert(j, data)
        # datasheet.append(sheet_data[i][j] + ", " + str(sheet_data[i][j]))
        datasheet.insert(i, datalist)
    return datasheet


def get_tags(rtype='smoke'):
    config.read(data_file_path)
    gettag = config['Tags']
    test_tags = gettag['run_type']
    if rtype is not None:
        rty = rtype.split(',')
        ttags = test_tags.split(',')
        if len(rty) == 1 and len(ttags) >= 1:
            if test_tags.find(rty[0]) != -1:
                t_xgs = None
                for txgs in ttags:
                    if txgs == rty[0]:
                        t_xgs = txgs
                return t_xgs
        else:
            xtype, txn = [], None
            for tgs in ttags:
                for rxt in rty:
                    if rxt == tgs:
                        txn = rxt
                        break
                if txn == tgs:
                    xtype.append('Y')
                else:
                    xtype.append('N')
            if 'Y' in list(set(xtype)):
                return rtype


def find_row_number_within_range(test_case_data, start_variable, end_variable):
    workbook = ParseExcel(test_case_data).workbook
    found_start = False
    found_end = False
    start_row = None
    end_row = None
    sheet_name_start = None
    sheet_name_end = None

    if end_variable is None or end_variable == "":
        end_variable = start_variable

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        # print(sheet)
        for row_num, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            # print(row_num, row)
            if row[1] == start_variable:
                found_start = True
                start_row = row_num
                sheet_name_start = sheet.title
            if row[1] == end_variable:
                found_end = True
                end_row = row_num
                sheet_name_end = sheet.title

            if found_start and found_end:
                break
        # print(start_row, end_row, sheet_name_start, sheet_name_end)
    workbook.close()
    if start_row is not None and end_row is not None and start_row <= end_row:
        return {'sLine': start_row, 'eLine': end_row, 'sheet_name': sheet_name_start}
    else:
        return "Start or end variable not found in the specified range.", 0
    # return start_row, end_row, sheet_name_start, sheet_name_end


def is_valid_value(value):
    if ',' in value:
        # Check if it's a comma-separated list of values
        values = value.split(',')
        for val in values:
            if not val.strip().isdigit():
                return False
        return True
    return value.isdigit()


def exeLiner(test_case_data, exeLine):
    global sName
    if is_valid_value(exeLine):
        if exeLine is not None:
            if ',' in exeLine:
                values = exeLine.split(',')
                gvalues = list(map(int, values))
                # print(f"The argument --l is a list of integers: {list(map(int, values))}")
                return ','.join(str(item) for item in gvalues)
        else:
            # print(f"The argument --l is an integer: {int(exeLine)}")
            return str(exeLine[0]) + ',' + str(exeLine[0])
    else:
        if ',' in exeLine:
            start_row, end_row = exeLine.split(',')
        else:
            start_row, end_row = exeLine, None
        getLine = find_row_number_within_range(test_case_data, start_row, end_row)
        exeLine = str(getLine['sLine']) + ',' + str(getLine['eLine'])
        sName = str(getLine['sheet_name'])
    return exeLine, sName


def generate_test_object_repo(test_case_data, pfix='FMS_', dx=None, ptname=None, sheetname=None, exeLine=None):
    sLine, eLine = 2, None
    getxcl = ParseExcel(test_case_data)
    getallxm = getxcl.get_sheetnames()
    getxmall = []

    try:
        if sheetname:
            for y in eval(sheetname):
                for x in range(0, len(getallxm)):
                    if x == y or getallxm[x] == y:
                        getxmall.append(getallxm[x])
                        break
            # Update getallxm with the filtered values
            getallxm = getxmall
    except Exception:
        sheetname_list = sheetname.split(',')  # Split the string into a list of sheet names
        for y in sheetname_list:
            if y in getallxm:  # Check if the sheet name is in the getallxm list
                getxmall.append(y)
        # Update getallxm with the filtered values
        getallxm = getxmall

    if exeLine is not None and sheetname is None:
        exeLine = exeLiner(test_case_data, exeLine)
        sLine, eLine = str(exeLine[0]).split(',')
        getallxm = [str(exeLine[1])]
    elif sheetname is not None and exeLine is None or sheetname is None and exeLine is None:
        sLine, eLine = sLine, eLine
    else:
        if ',' in exeLine:
            sLine, eLine = str(exeLine).split(',')
        else:
            sLine, eLine = exeLine, None
    if dx:
        pathdata_file = mypath / 'test_dir' / 'test_zigapp.py'
    else:
        pathdata_file = mypath / 'test_dir' / 'test_onefms.py'
    with open(pathdata_file, 'w') as f:
        f.write('import os\n')
        f.write('import cdxg\n')
        f.write('import configparser\n')
        f.write('from cdxg import file_data\n')

        # f.write('from wfs.pages.action_step import get_test_steps\n')
        f.write('from wfs.utils.action_test_item import get_tags\n')
        if dx is None:
            f.write('from wfs.pages.object_repo_page import object_repox\n')
        f.write('from cdxg.logging import log\n')
        f.write('from wfs.utils.desired_actions import getdepend\n')
        f.write('from wfs.utils.common import Create_New_Report, get_results, get_line_dict\n\n')
        # if dx:
        #    f.write('from confapp import pax_session, drv_session\n\n')

        f.write('BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))\n')
        f.write('data_file_path = os.path.join(BASE_PATH, "conf.ini")\n')
        f.write('config = configparser.ConfigParser()\n')
        f.write('config.read(data_file_path)\n')
        if dx:
            f.write('test_case_data = config.get("MobileHost", "test_case_data")\n')
            f.write('test_data_json = config.get("MobileHost", "test_data_json")\n')
            f.write("test_object_repo = config.get('MobileHost', 'test_object_repo')\n")
        else:
            f.write('test_case_data = config.get("Xldata", "test_case_data")\n')
            f.write('test_data_json = config.get("Xldata", "test_data_json")\n')
            f.write("test_object_repo = config.get('Xldata', 'test_object_repo')\n")
        f.write('test_tags = config.get("Tags", "run_type")\n')
        if dx:
            f.write('xreport = config.get("MobileHost", "test_report")\n')
            twx = 'Mobile'
        else:
            f.write('base_url = config.get("Url", "base_url")\n')
            f.write('xreport = config.get("Xldata", "test_report")\n')
            twx = 'Web'
        f.write('reportpath = Create_New_Report(report=xreport)\n\n\n')
        f.write('line = ' + str(sLine) + '\n')
        f.write('end_line = ' + str(eLine) + '\n\n\n')

        for i, getxl in enumerate(getallxm):
            if pfix in getxl and 'CommonCase' not in getxl:
                f.write('class Test_' + str(i) + str(twx) + '_' + str(getxl) + '(cdxg.TestCase):\n\n')
                if dx is None:
                    f.write('\tdef start(self):\n')
                    f.write('\t\tself.lpage = object_repox(self.driver)\n')
                    f.write("\t\tself.baseUrl = f'{base_url}'\n\n")

                    appx = 'one'
                else:
                    appx = 'zig'

                f.write('\t@file_data(test_case_data, line=line, end_line=end_line, sheet="' + str(getxl) + '")\n')
                f.write(
                    '\tdef test_' + str(appx) + str(
                        getxl) + '(self, testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, rtype,\n')
                f.write('\t\t\t\t\t\t\tcase, depend, incidentids):\n')
                f.write('\t\t""""""\n')
                f.write('\t\tif rtype and case is not None:\n')
                f.write('\t\t\txtype = rtype + "," + case\n')
                f.write('\t\telse:\n')
                f.write('\t\t\txtype = rtype if case is None else case\n')
                f.write('\t\tif get_tags(xtype):\n')
                f.write('\t\t\tlog.info("TestCase : " + str(ustory) + "-" + str(testcase))\n')
                f.write('\t\t\tlog.info("Test_Tags : " + str(get_tags(xtype)))\n\n')
                f.write('\t\tfeatures = "' + str(getxl) + '"\n')
                f.write("\t\tself.maxDiff = None\n")
                f.write('\t\tif "skip" not in xtype and xtype == get_tags(xtype) and xtype is not None:\n')
                f.write(
                    '\t\t\tdependdata = testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend\n')
                if dx is None and ptname is None:
                    f.write(
                        '\t\t\tgtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, self.baseUrl, self.driver, ptname=None)\n')
                else:
                    f.write(
                        '\t\t\tgtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, url=None, driver=None, ptname="' + str(
                            ptname) + '")\n')
                # f.write("\t\t\tprint(gtres)\n")
                f.write("\t\t\tfor xgres in gtres:\n")
                f.write("\t\t\t\tif 'Error' in xgres or gtres == 'Y' or xgres == 'Y':\n")
                f.write(
                    "\t\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, xgres, \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\texresults, gtres, lpage=self.lpage, results='FAILED', fontx='FC2C03', sshots=features, incidentids=incidentids)\n")
                f.write('\t\t\t\t\tself.xFail(gtres)\n')
                f.write('\t\t\t\t\tbreak\n')
                f.write("\t\t\t\tif xgres.endswith('YES'):\n")
                f.write(
                    "\t\t\t\t\tif '>>' in str(aresults) and not str(aresults).startswith('>>') and not str(aresults).endswith('>>'):\n")
                f.write("\t\t\t\t\t\taresults = get_line_dict(ptname=" + str(ptname) + ", dname=aresults)\n")
                f.write("\t\t\t\t\tacresults = str(xgres)+'>>'+str(aresults)\n")
                f.write(
                    "\t\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, acresults, \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\texresults, gtres, lpage=self.lpage, results='PASSED', fontx='35FC03', sshots=None, incidentids=incidentids)\n")
                f.write('\t\t\t\t\tbreak\n')
                f.write('\t\telse:\n')
                f.write('\t\t\tif rtype == "skip":\n')
                f.write('\t\t\t\tself.xSkip(testcase + ": Testcase Skipped, Due to not much information")\n')
                f.write(
                    "\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, 'Testcase Skipped', \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\t\t\texresults, lpage=self.lpage, results='SKIPPED', fontx='F4D25A', sshots=None, incidentids=incidentids)\n")
                f.write('\t\t\telse:\n')
                f.write(
                    '\t\t\t\tself.skipTest(reason="Test execution based on Tags :" + str(test_tags) + ": Excludes the rest")\n')
                f.write('\n\n')
    f.close()


def mixedcharacters(k=5):
    mixed_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return mixed_chars


def getextra(keyitem, ustory, kword, rstring, ptname):
    if '*.*' in keyitem:
        keyitem = str(keyitem).replace('*.*', '_' + str(mixedcharacters()))
    ptn = 'web'
    if ptname:
        ptn = 'mobile'
    with open(mypath / 'test_data' / ptn / 'get_text_item.txt', 'a+') as ftxt:
        ftxt.write(ustory + '|' + keyitem + '|' + kword + '|' + rstring + '|\n')
    return keyitem


def getxxextra(keyitem, ustory, kword, rstring, retnx, ptname):
    ptn = 'web'
    if ptname:
        ptn = 'mobile'
    with open(mypath / 'test_data' / ptn / 'text_data_repo.txt', 'a+') as ftxt:
        ftxt.write(ustory + '|' + keyitem + '|' + kword + '|' + rstring + '|' + retnx + '|\n')
    return keyitem


def getmultipleKeys(keyitem):
    getlen = []
    if ',' in keyitem:
        getsplit = str(keyitem).split(',')
        for xlen in getsplit:
            getlen.append(getextra(xlen))
    else:
        getlen.append(keyitem)
    return getlen


def capture_frame(driver, output_file):
    # Capture the screenshot using Selenium
    screenshot = driver.get_screenshot_as_png()

    # Save the screenshot to a file
    with open(output_file, 'wb') as file:
        file.write(screenshot)


def start_video_recording(driver):
    # Start video recording using ffmpeg
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_video_file = mypath / 'reports' / "videos" / f"scenario_{timestamp}.mp4"
    # Set the output video file path
    # output_video_file = 'output.mp4'

    # Start recording frames
    ffmpeg_process = (
        ffmpeg
        .input('pipe:', format='png', framerate=30)
        .output(output_video_file, pix_fmt='yuv420p')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    # Capture frames at regular intervals
    for frame_number in range(300):  # Capture 300 frames
        capture_frame(driver, 'frame{:03d}.png'.format(frame_number))
    return ffmpeg_process


def stop_video_recording(ffmpeg_process):
    # Stop video recording
    # Close the ffmpeg process
    ffmpeg_process.stdin.write("q")
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
