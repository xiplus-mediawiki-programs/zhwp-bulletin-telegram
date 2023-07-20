cfg = {
    'url': 'https://zh.wikipedia.org/w/index.php?title=Template:Bulletin/ajax&action=render&uselang=zh-tw',
    'hide_bulletin_regex': r'提名維基獎勵|頁面需維基化',
    'telegram': {
        'token': '',
        'chats': {
            -123456: {
                'new': '#新 {0}',
                'archive': '#已存檔 {0}',
            },
        },
    },
    'database': {
        'host': 'localhost',
        'user': '',
        'passwd': '',
        'db': '',
        'table_prefix': 'zhwiki_bulletin_',
        'charset': 'utf8mb4',
    },
}
