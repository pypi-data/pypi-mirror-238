import json
import os.path
import time

from urllib.parse import urlparse
from allure import *


class AllureData:
    """解析allure_results的数据"""

    def __init__(self, result_path='report'):
        self.result_path = result_path

    def get_files(self):
        """获取以result.json结尾的文件列表"""
        file_list = []
        for filename in os.listdir(self.result_path):
            if filename.endswith('result.json'):
                file_list.append(filename)

        if not file_list:
            raise KeyError('报告数据为空')

        return [os.path.join(self.result_path, item) for item in os.listdir(self.result_path) if
                item.endswith('result.json')]

    @staticmethod
    def get_file_content(file_path):
        """获取文件内容并转成json"""
        with open(file_path, 'r', encoding='UTF-8') as f:
            content = json.load(f)
        return content

    def parser_content(self, content):
        """解析执行结果"""
        name = content.get('name')
        status = content.get('status')
        full_name = content.get('fullName')
        description = content.get('description')
        parameters = content.get('parameters', None)
        log_name = [os.path.join(self.result_path, item.get('source')) for item in content.get('attachments') if
                    item.get('name') == 'log'][0]
        log_data = open(log_name, 'r', encoding='utf8').read()
        start = content.get('start')
        end = content.get('stop')
        cost = (end - start) / 1000
        if cost > 60:
            cost = '{}min'.format(round(cost / 60, 1))
        else:
            cost = '{}s'.format(round((end - start) / 1000, 1))
        case_data = {
            "title": name,
            "name": full_name,
            "description": description,
            "log": log_data,
            "status": status,
            "start_time": start,
            "end_time": end,
            "cost": cost,
            "parameters": parameters
        }
        return case_data

    @staticmethod
    def remove_duplicate(json_contents):
        """去除失败重试的重复结果"""
        case_list = []
        no_repeat_tags = []
        for item in json_contents:
            full_name = item["name"]
            parameters = item["parameters"]
            if (full_name, parameters) not in no_repeat_tags:
                no_repeat_tags.append((full_name, parameters))
                case_list.append(item)
            else:
                for case in case_list:
                    if case.get('name') == full_name and case.get('parameters') == parameters:
                        if case.get('status') != 'passed':
                            case_list.remove(case)
                            case_list.append(item)
        return case_list

    def get_results(self):
        """获取对外的测试结果列表"""
        file_list = self.get_files()
        result_list = []
        for file in file_list:
            content = self.get_file_content(file)
            parser_content = self.parser_content(content)
            result_list.append(parser_content)
        return self.remove_duplicate(result_list)

    def get_interfaces(self):
        case_list = self.get_results()
        interface_list = []
        for case in case_list:
            log = case.get('log')
            for line in log.split("\n"):
                if 'url]: ' in line:
                    interface = line.strip().split('url]: ')[1]
                    parsed_url = urlparse(interface)
                    path = parsed_url.path
                    method = line.strip().split('[method]: ')[1].split()[0].lower()
                    interface_list.append((method, path))

        interface_list = list(set(interface_list))
        return interface_list

    def get_statistical_data(self):
        case_list = self.get_results()

        # 获取用例统计数据
        passed_list = []
        fail_list = []
        for case in case_list:
            status = case.get('status')
            if status == 'passed':
                passed_list.append(case)
            else:
                fail_list.append(case)
        total = len(case_list)
        passed = len(passed_list)
        failed = len(fail_list)
        rate = round((passed / total) * 100, 2)

        # 获取整个任务的开始和结束时间
        start_time_timestamp, end_time_timestamp = case_list[0].get('start_time'), case_list[0].get('end_time')
        for case in case_list:
            inner_start = case.get('start_time')
            inner_end = case.get('end_time')
            if inner_start < start_time_timestamp:
                start_time_timestamp = inner_start
            if inner_end > end_time_timestamp:
                end_time_timestamp = inner_end

        # 时间戳转成日期
        start_time, end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_timestamp / 1000)), \
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_timestamp / 1000))
        cost = (end_time_timestamp - start_time_timestamp) / 1000
        if cost > 60:
            cost = '{}min'.format(round(cost / 60, 1))
        else:
            cost = '{}s'.format(round((end_time_timestamp - start_time_timestamp) / 1000, 1))

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'rate': rate,
            'start': start_time,
            'end': end_time,
            'cost': cost
        }

    @property
    def report_data(self):
        return {
            "summary": self.get_statistical_data(),
            "interfaces": self.get_interfaces(),
            "tests": [
                {
                    "id": i+1,
                    "title": case.get("title"),
                    "name": case.get("name"),
                    "status": case.get("status"),
                    "cost": case.get("cost"),
                    "log": case.get("log")
                } for i, case in enumerate(self.get_results())
            ]
        }


def get_allure_data(result_path):
    """兼容邮件和钉钉的调用"""
    return AllureData(result_path).get_statistical_data()

