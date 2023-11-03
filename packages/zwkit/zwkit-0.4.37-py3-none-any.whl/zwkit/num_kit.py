import pandas as pd


def date_split(data):
    data_cp = data.copy()
    data_cp.reset_index(drop=True, inplace=True)
    result = []
    if len(data) == 1:
        result.append([data_cp[0], data_cp[0]])
        return result
    else:
        data_diff = data_cp.diff()
        data_diff.iloc[0] = 1

        # 获取断点列表
        break_point = data_diff[data_diff != 1].index.tolist()
        if len(break_point) == 0:
            result.append([data_cp[0], data_cp[len(data_cp) - 1]])
            return result
        else:
            first_point = 0
            # 根据断点列表切分data
            for i in break_point:
                _data = data_cp[first_point:i]
                _data.reset_index(drop=True, inplace=True)
                result.append([_data[0], _data[len(_data) - 1]])
                first_point = i
            # 最后一个断点后面的数据
            _data = data_cp[first_point:]
            _data.reset_index(drop=True, inplace=True)
            result.append([_data[0], _data[len(_data) - 1]])
    return result


# # main函数
# if __name__ == '__main__':
#     # 新建一个pandas 内容是年份
#     data = pd.DataFrame({'year': [2014, 2015, 2018, 2020]})
#     # 调用函数
#     result = date_split(data['year'])
#     print(result)
