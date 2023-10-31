# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023-10-27 16:40:37
# @Copyright:  www.shujiajia.com  Inc. All rights reserved.
# Description: 注意：本内容仅限于数据堂公司内部传阅，禁止外泄以及用于其他的商业目的
# -------------------------------------------------------------------------------
import os
from pathlib import Path
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def download_file(url, save_path):
    headers = {}
    if os.path.exists(save_path):
        # 如果文件已存在，则发送Range头部，实现可续下载
        headers['Range'] = f"bytes={os.path.getsize(save_path)}-"
    response = requests.get(url, stream=True, headers=headers)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, ncols=100, desc=save_path.name)
    with open(save_path, 'ab') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        # 下载不完整，删除文件
        os.remove(save_path)


def download_files(urls, save_dir):
    """_summary_

    Args:
        urls: [url,url,url]
        save_dir: save path
    """
    progress_bar = tqdm(total=len(urls), ncols=100, desc="下载进度")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for url in urls:
            file_name = url.split('/')[-1]
            save_path = Path(save_dir).joinpath(file_name)
            futures.append(executor.submit(download_file, url, save_path))
        for future in as_completed(futures):
            if future.done():
                future.result()
                progress_bar.update()


if __name__ == '__main__':
    urls = [
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_2107130715161.jpeg",
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_2107150739490.jpg",
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_2107150739571.jpg",
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_2107150740179.jpg",
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_2107150740342.jpg",
        "https://images.cnblogs.com/cnblogs_com/yunhgu/1999467/t_21071507412446.jpg",
    ]
    save_dir = r"D:\guoyunhui\测试工具\save"
    download_files(urls, save_dir)
