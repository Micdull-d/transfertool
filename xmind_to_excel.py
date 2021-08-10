from xmindparser import xmind_to_dict
import re
import xlwt

class xmind_to_xls():
    def xmind_num(self,value):
        """获取xmind标题个数"""
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def xmind_title(self,value):
        """获取xmind标题内容"""
        return value['title']

    def  xmind_cat(self,filename):
        '''调试函数，打印内容用的'''
        self.out = xmind_to_dict(filename)
        self.story = self.out[0]['topic']['topics']
        self.num=len(self.story)
        print(self.out)
        print(self.out[0]['topic']['title'])
        print(self.num)
        return self.story,self.num

    def write_excel(self,xmind_file,caselevel='',autocov='',casetype=''):
        '''生成excel文件函数'''
        self.f=xlwt.Workbook()
        self.sheet1 =self.f.add_sheet('sheet1',cell_overwrite_ok=True)
        #self.row0 = ['storyid', '需求名称', '测试用例名称', '执行步骤', '预期结果', '服务名称', '版本', '执行人员']
        #self.row0 = ['需求名称', '测试用例名称', '执行步骤', '预期结果', '服务名称', '版本', '执行人员']
        #self.row0为表格第一行内容
        self.row0 = ["需求名称","用例名称","前置条件","执行步骤","预期结果","用例等级",'自动化覆盖','用例类型']
        #生成第一行
        for i in range(0,len(self.row0)):
            self.sheet1.write(0,i,self.row0[i])
        #将xmind文件内容转换为字典格式
        self.out = xmind_to_dict(xmind_file)
        #print('out=',self.out)
        #将表格文件名设置为xmind一级标题
        self.xls_name=self.out[0]['topic']['title']
        #print('xls_name=',self.xls_name)
        #story为xmind二级标题以后内容
        self.story = self.out[0]['topic']['topics']
        #print('story=',self.story)
        #二级标题个数
        self.storynum = len(self.story)
        #print('storynum=',self.storynum)
        j=1 #用例计算器
        z = 0  # 用例结果数计数器
        for i in range(0, self.storynum):
            #storyname为二级标题名称，设置为需求名称
            self.storyname = self.story[i]['title']
            print('storyname=', self.storyname)
            #self.regex_str = ".*[\[【](.+?)[\]】].*"
            #self.storyid_reg = re.match(self.regex_str, self.storyname)
            #print(self.storyid_reg)
            #if self.storyid_reg:
            #    self.storyid=self.storyid_reg.group(1)#正则取出用例编号
            #   print(self.storyid_reg.group(1))
            self.case = self.story[i]['topics'][i]
            self.casenum = len(self.case)
            print('case=', self.case)
            print('casenum=', self.casenum)
            #self.testcase_num=self.xmind_num(self.story[i]['topics'][0])
            #print('testcase_num=', self.testcase_num)
            #for k in range(0,self.testcase_num):
            for k in range(0, self.casenum):
                #self.testcase=self.story[i]['topics'][0]['topics'][k]
                #print('testcase=', self.testcase)
                self.casename = self.story[i]['topics'][k]['title']
                self.testcase_t = self.story[i]['topics'][k]['topics']
                print('casename=', self.casename)
                print('testcase_t=', self.testcase_t) 
                self.testcase = self.story[i]['topics'][k]['topics'][0]
                
                print('testcase=', self.testcase)
                print('casename=', self.casename)
                self.precondition =self.xmind_title(self.testcase)
                self.testcase_stepnum=self.xmind_num(self.testcase) #每个用例的步骤数量
                self.sheet1.write(k + i + z + j, 0, self.storyname) #需求名称
                self.sheet1.write(k + i + z + j, 1, self.casename) #用例名称，需要修改
                self.sheet1.write(k + i + z + j, 2, self.precondition) #前置条件
                self.sheet1.write(k + i + z + j, 5, caselevel) #用例等级
                self.sheet1.write(k + i + z + j, 6, autocov) #自动化覆盖
                self.sheet1.write(k + i + z + j, 7, casetype) #用例类型
                #self.sheet1.write(k + i + z + j, 0, self.storyid)
                #取出三级标题作为用例名称
                #for c in range(0, self.casenum):
                #    self.casename = self.story[i]['topics'][c]['title']
                #   print('casename=',self.casename)
                for x  in range(0,self.testcase_stepnum):
                    self.testcase_step=self.testcase['topics'][x]
                    self.teststep_title=self.xmind_title(self.testcase_step) #用例步骤名称
                    self.teststep_num=self.xmind_num(self.testcase_step) #用例步骤个数
                    if self.teststep_num != 0:
                        for y in range(0,self.teststep_num):
                            self.test_results=self.testcase_step['topics'][y]
                            self.test_result=self.xmind_title(self.test_results)#预期结果
                            self.sheet1.write(k + i + z + j+y+1, 3, self.teststep_title)
                            self.sheet1.write(k + i + z + j + y+1, 4, self.test_result)
                        z = z + y+1
                    else:
                        self.test_result=' '
                        self.sheet1.write(k + i + z + j+1  , 3, self.teststep_title)
                        self.sheet1.write(k + i + z + j+1 , 4, self.test_result)
                        z = z + 1
            j=j+k
        self.f.save(self.xls_name+'.xls') #xls名称取xmind主题名称

if __name__ == '__main__':
     xmind_file = "test.xmind"  # xmind文件
     caselevel='P3'
     autocov='未完成'
     casetype='回归用例'
     xmind_to_xls().write_excel(xmind_file,caselevel,autocov,casetype)
     xmind_to_xls().xmind_cat(xmind_file)