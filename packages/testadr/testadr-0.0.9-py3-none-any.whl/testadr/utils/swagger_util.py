# @Time    : 2022/2/11 9:00
# @Author  : kang.yang@qizhidao.com
# @File    : swagger.py
import requests
import urllib3

urllib3.disable_warnings()


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def get_swagger_data(swagger_url):
    """
    通过swagger接口获取接口列表
    @param swagger_url:
    @return: [
        ['请求方法', '项目名', '模块名', '模块描述', '接口名', '接口描述'],
        ...
    ]
    """
    # 请求url，获取返回的json
    res = requests.get(swagger_url, verify=False)
    # print(res.text)
    data_json: dict = res.json()
    # print(data_json)
    # 获取接口所属模块
    project: str = data_json.get('basePath')
    project = project.split('/')[1]
    # 获取tag名称和描述的映射关系
    tags = data_json.get('tags')
    tag_dict = {}
    for tag in tags:
        name = tag.get('name')
        des = tag.get('description')
        if name not in tag_dict:
            tag_dict[name] = des
    # print(tag_dict)
    # 获取接口信息
    paths = data_json.get('paths')
    print(len(paths))
    api_list = []
    for apiPath, value in paths.items():
        apiPath = f'/{project}{apiPath}'
        apiPath = apiPath.replace('{', '')
        apiPath = apiPath.replace('}', '')
        for method, content in value.items():
            tag = content['tags'][0]
            if is_chinese(tag):
                moduleDesc = tag
                moduleName = tag_dict[tag]
            else:
                moduleName = tag
                moduleDesc = tag_dict[tag]
            moduleDesc = moduleDesc.replace("'", "")
            moduleDesc = moduleDesc.replace('"', '')

            apiDesc: str = content['summary']
            apiDesc = apiDesc.replace("'", "")
            apiDesc = apiDesc.replace('"', '')
            params = [item for item in content.get('parameters', [])]
            for i, param in enumerate(params):
                _in = param.get("in")
                _param = None
                if _in == 'body':
                    _schema = param.get("schema")
                    if _schema.get("originalRef", None) is not None:
                        _ref = _schema["originalRef"]
                        try:
                            _param = data_json["definitions"][_ref]['properties']
                        except:
                            _param = param
                            _param["type"] = "--"
                    else:
                        _items = _schema.get("items", None)
                        if _items is not None:
                            if _items.get('originalRef', None) is not None:
                                _ref = _schema["items"]["originalRef"]
                                _param = data_json["definitions"][_ref]['properties']
                                _param = [_param]
                            else:
                                _param = param
                                _param["type"] = param["schema"]["items"]["type"]
                                _param = [_param]
                        else:
                            _param = param
                            _param["type"] = param["schema"]["type"]

                if _param is not None:
                    params[i] = {"in": "body", "value": _param}

            api_list.append([method, project, moduleName, moduleDesc, apiPath, apiDesc, params])
    # for index, api in enumerate(api_list):
    #     print(index, api)
    return api_list


if __name__ == '__main__':
    get_swagger_data("http://app-test-lan.qizhidao.com/kz-bff-scrm/v2/api-docs?group=%E4%BC%81%E7%9F%A5%E9%81%93")









