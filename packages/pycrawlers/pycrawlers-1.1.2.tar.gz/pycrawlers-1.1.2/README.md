# crawlers

## 介绍
爬虫集合

## 可获取的项目

1. huggingface 上的模型文件
2. 无反爬的网站


## 项目示例

### 1.  hugging face



    from pycrawlers import huggingface

    urls = ['https://huggingface.co/albert-base-v2/tree/main',
            'https://huggingface.co/dmis-lab/biosyn-sapbert-bc5cdr-disease/tree/main']
    
    paths = ['./model_1/albert-base-v2', './model_2/']
    # 实例化类
    # 使用默认 base_url (https://huggingface.co)
    hg = huggingface()
    # 自定义 base_uel
    # hg = huggingface('https://huggingface.co')
    # 输入 huggingface 的 token，下载需要权限的模型或数据集
    # token = "xxxxxyyyyywwwwwccccc"
    # hg = huggingface(token=token)
    
    # 1. 单个获取
    # 1.1 使用默认保存位置（'./'）
    hg.get_data(urls[0])
    
    # 1.2 自定义保存地址
    # hg.get_data(urls[0], paths[0])
    
    # 2.批量获取
    # 2.1 使用默认保存位置（'./'）
    hg.get_batch_data(urls)
    
    # 2.2 自定义保存地址
    # hg.get_batch_data(urls, paths)

### 2.  通用抓取网页
可以抓取那些反爬不厉害的网站。
注意：需安装 mongodb，数据将会存储在 mongodb里

#### 2.1  简单使用


    from pycrawlers import crawl_website

    mongo_host = ''
    mongo_port = '27017'
    db_name = 'huxiu'
    id_collection_name = 'huxiu_id'
    collection_name = 'huxiu'
    base_url = 'https://www.huxiu.com'
    
    
    crawl_website(mongo_host, mongo_port, db_name, id_collection_name, collection_name, base_url)

#### 2.2  进阶使用
可以使用url filter 过滤不想抓取的网页，比如视频、图片


    from pycrawlers import crawl_website
    from pycrawlers.websites.url_filters import filter_video_photo

    mongo_host = ''
    mongo_port = '27017'
    db_name = 'huxiu'
    id_collection_name = 'huxiu_id'
    collection_name = 'huxiu'
    base_url = 'https://www.huxiu.com'
    
    """
    url_filter 也可以自己定义
    """
    # photo_type = ['bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd',
    #               'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp', 'avif', 'apng']
    # 
    # video_type = ['wmv', 'asf', 'asx', 'rm', 'rmvb', 'mp4', '3gp', 'mov', 'm4v', 'avi',
    #               'dat', 'mkv', 'flv', 'vob', 'mpeg']
    # 
    # 
    # def filter_video_photo(url: str):
    #     all_types = photo_type + video_type
    #     for i in all_types:
    #         if url.endswith('.' + i):
    #             return False
    #     return True
      
    crawl_website(mongo_host, mongo_port, db_name, id_collection_name, collection_name, base_url, url_filter=filter_video_photo)


