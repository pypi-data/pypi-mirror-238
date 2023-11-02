VAR_NAVER_STATEMENT = 'var naver='
HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ko",
    "Content-Type": "application/json",
    "referer": "https://pcmap.place.naver.com/",
    "Origin": "https://pcmap.place.naver.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}




def parse_naver_var_in_script_texts(script_texts):
    naver_string = None
    for script_text in script_texts:
        if script_text.string is None:
            continue
        if VAR_NAVER_STATEMENT in script_text.string:
            naver_string = script_text.string
            break

    return naver_string
