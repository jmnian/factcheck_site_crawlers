import csv
import re
# Open the input file
with open('/Users/jimmynian/code/AMICA/piyaoba_crawler/piyaoba.csv', 'r', encoding='utf-16') as infile:
    # Open the output file
    with open('piyaoba_structured.csv', 'w', encoding='utf-16', newline='') as outfile:
        # Create a CSV writer
        writer = csv.writer(outfile)

        # Write the header row to the output file
        writer.writerow(['URL', 'Status/Result', 'Post Headline', 'Post Published Date', 'Source of Misinfo', 
                        'Date of Misinfo First Appear on the Internet', 'Background', 'Conclusion', 'Reference Links'])
        
        # Read the input file
        status = {'真': '真 True', '假': '假 Fake', '半真半假': '半真半假 Half Half', '缺乏背景': '缺乏背景 Lack of Background', 
                  '以偏概全': '以偏概全 Overgeneralize', '叙述不全': '叙述不全 Incomplete Narrative', '部分错误': '部分错误 Partially False', }
        reader = csv.reader(infile)
        i = 1
        url_regex = re.compile(r'(https?://\S+)')
        for row in reader:
            print("on row", i)
            if i == 1 or i == 2:
                i += 1 
                continue
            
            content = row[1]
            url = row[0]
            result = status[content.split('】')[0].lstrip('【')]
            headline = content.split('】')[1].split('【')[0]
            post_date = ""
            if '日期】' in content:
                post_date = content.split('日期】')[1].split('【')[0]

            source = ""
            if '来源' in content:
                source = content.split('来源')[1].split('【')[0]
            if '】' in source:
                source = source.split('】')[1]

            appear_date = content.split()[-1]

            background = ""
            if '事实核查】' in content:
                background = content.split('事实核查】')[1].split('结论：')[0]
            elif '完整故事' in content:
                background = content.split('完整故事')[1].split('结论：')[0]

            conclusion = ""
            if '结论：' in content:
                conclusion = content.split('结论：')[1].split('：')[0]
            urls = url_regex.findall(content)
            reference = ', '.join(urls)
            # Write the info to a new line
            writer.writerow([url, result, headline, post_date, source, appear_date, 
                             background, conclusion, reference])
            
            i+=1 