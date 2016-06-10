# encoding:utf-8
from SOAPpy import SOAPProxy
from datetime import datetime

class MoDis(object):
    '''
    如果文件未上传到网络,则得不到下载地址
    测试:依次输入:MOD021KM,5,2008-10-23,2008-10-23
    '''
    def __init__(self):
        self.url = 'http://modwebsrv.modaps.eosdis.nasa.gov/axis2/services/MODAPSservices'
        self.client = SOAPProxy(self.url)

    # 检查日期的正确性
    def is_valid_date(self, date_string):

        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
            if date <= datetime.now():
                return True
            else:
                return False
        except:
            return False

    # 得到文件ID
    def get_id(self):
        product_code = raw_input('Enter Product Code (default:MOD09):')
        collection = raw_input('Enter Collection  Number:')

        start_date = raw_input('Enter Start Date(YYYY-MM-DD):')
        while not self.is_valid_date(start_date):
            start_date = raw_input('Wrong start date code,please enter again:')

        stop_date = raw_input('Enter Stop Date(YYYY-MM-DD):')
        while not self.is_valid_date(start_date):
            start_date = raw_input('Wrong stop date code,please enter again:')

        id_list = self.client.searchForFiles(
                                         product=product_code if product_code else 'MOD09',
                                         collection=collection,
                                         start=start_date,
                                         stop=stop_date,
                                         coordsOrTiles='global',
                                         dayNightBoth='DNB',
                                         north='90',
                                         south='-90',
                                         west='-180',
                                         east='180',
                                         )
        # 对ID分组,防止ID过多网站不响应
        group_number = divmod(len(id_list), 130)[0]
        print id_list,group_number
        if group_number > 0:
            id_lists = []
            start = 0
            for i in range(group_number):
                id_lists.append(id_list[start:start+130])
                start += 130
            id_lists.append(id_list[start:])
            print id_lists, len(id_lists)
        else:
            id_lists = id_list
        return id_lists

    #获得下载地址
    def get_urls(self):
        id_lists = self.get_id()
        for ids in id_lists:
            print ','.join(ids)
            urls = self.client.getFileUrls(fileIds=','.join(ids))
            print urls
            # 写入文件
            with open('modisurls.txt','a+') as f:
                f.write('\n'.join(urls) + '\n')

if __name__ == '__main__':
    modis = MoDis()
    modis.get_urls()
