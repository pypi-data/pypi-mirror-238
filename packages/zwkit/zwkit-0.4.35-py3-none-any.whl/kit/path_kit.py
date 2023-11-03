import os


def create_dir(path):
    """
    判断文件是否存在
    不存在则创建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


import platform

# 判断当前系统是mac还是windows
def get_system():
    """
    判断当前系统是mac还是windows
    :return:
    """
    import platform
    system = platform.system()
    if system == 'Windows':
        return 'Windows'
    elif system == 'Darwin':
        return 'Mac'
    else:
        return 'Linux'



def get_system_dir(cloud:str,pj:str):
    platform = get_system()
    if platform == 'Windows':
        return f'//{cloud}//file//{pj}//'
    elif platform == 'Mac':
        return f'/Volumes/{cloud}/file/{pj}/'
    else:
        return f'/mnt/{cloud}/file/{pj}/'



def get_system_data_dir(cloud:str,pj:str,data:str):
    platform = get_system()
    if platform == 'Windows':
        return f'//{cloud}//file//{pj}//{data}//'
    elif platform == 'Mac':
        return f'/Volumes/{cloud}/file/{pj}/{data}/'
    else:
        return f'/mnt/{cloud}/file/{pj}/{data}/'