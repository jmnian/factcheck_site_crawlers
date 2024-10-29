import csv
import re

with open('/Users/jimmynian/code/AMICA/tfc_crawler/tfc_raw.csv', 'r', encoding='utf-16') as infile:
    # Open the output file
    with open('tfc_structured.csv', 'w', encoding='utf-16', newline='') as outfile:
        # Create a CSV writer
        writer = csv.writer(outfile)

        # Write the header row to the output file
        writer.writerow(['URL', 'Status/Result', 'Claim', 'Date', 'Fact Checked/Verified', 
                        'Background', 'Verified', 'Conclusion'])
        
        # Read the input file
        status = {'錯誤': 'False', '部分錯誤': 'False Partially', '事實釐清': 'Fact Clarification'}
        reader = csv.reader(infile)
        i = 1
        url_regex = re.compile(r'(https?://\S+)')
        for row in reader:
            print("on row", i)
            i += 1
            content = row[1]
            url = row[0]
            result = content.split('】')[0].lstrip('【')
            if result not in status:
                continue
            else:
                result = status[result]
            claim = content.split('】')[1].split('【')[0]
            date = ""
            if '【報告將隨時更新 ' in content:
                date = content.split('【報告將隨時更新 ')[1].split('版】')[0]
            fact_checked = ""
            if '經查： ' in content:
                fact_checked = content.split('經查： ')[1].split('背景 ')[0]
            if '版】 ' in fact_checked:
                fact_checked = fact_checked.split('版】 ')[1]
            background = ""
            if '背景 ' in content:
                background = content.split('背景 ')[1].split('查核 ')[0]
            verify = ""
            if '查核 ' in content:
                verify = content.split('查核 ')[1].split('結論 ')[0]
            conclusion = ""
            if '結論 ' in content:
                conclusion = content.split('結論 ')[1].split('馬上訂閱TFC電子報')[0]
            if '版】 ' in conclusion:
                conclusion = conclusion.split('版】 ')[1]

            writer.writerow([url, result, claim, date, fact_checked, background, verify, conclusion])