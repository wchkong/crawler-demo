import requests,openpyxl

#建立excel表
joblist=[]
wb=openpyxl.Workbook()
sheet=wb.active
sheet.title='智联招聘数据'
sheet['A1']='职位名称'
sheet['B1']='薪资'
sheet['C1']='工作经验'

#爬虫
keyword=str(input('请输入查找职位的关键字：'))
url='https://fe-api.zhaopin.com/c/i/sou'
headers={
    'Referer': 'https://sou.zhaopin.com/?p=2&jl=653&et=2&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&kt=3&sf=0&st=0',

    }
for n in range(5):
    params={
        'start': str(90*n),
        'pageSize': '90',
        'cityId': '653',
        'salary': '0,0',
        'workExperience': '-1',
        'education':'4',
        'companyType': '-1',
        'employmentType': '2',
        'jobWelfareTag': '-1',
        'kw': keyword,
        'kt': '3',
        'at': '9faf2d5cc87b4141a33c493c248ce1eb',
        'rt': 'c678689ef9144475b2030fe55c12fe5c',
        '_v': '0.53075950',
        'userCode': '638259962',
        'x-zp-page-request-id': '9eb3c2c955dd4a8db3c8224a177ebdd5-1567575573029-133510',
        'x-zp-client-id': 'cd7e0b11-a761-4a2f-a8be-2e6a9da3f068'

        }

    res=requests.get(url,headers=headers,params=params)
    jsonres=res.json()
    positions=jsonres['data']['results']

    for position in positions:
        jobname=position['jobName']
        salary=position['salary']
        workingExp=position['workingExp']['name']
        joblist.append([jobname,salary,workingExp])

#写入excel
for row in joblist:
    sheet.append(row)

wb.save('智联招聘数据.xlsx')
print('数据爬取成功！')