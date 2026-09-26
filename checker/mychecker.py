#!/usr/bin/env python3
from ctf_gameserver import checkerlib
import requests
import logging
from checker_util import CheckerException, handle_errors, generate_creds, random_template, random_multi_template, random_image, generate_text, generate_message
import tarfile
import io
import random
import pymupdf
import base64
import time
import re

LANGS = [
"Dravuun",
"Irixo7",
"Mnemosh",
"Xyrrathi",
]

class TemplateChecker(checkerlib.BaseChecker):
    session: requests.Session = None

    def url(self):
        return f"http://[{self.ip}]:1986/"

    def login(self, uname, pw):
        logging.info(f"Logging in with {uname=}, {pw=}")
        if self.session: self.session.close()
        self.session = requests.Session()
        form_data = {"username": uname, "password": pw}
        r = self.session.post(self.url() + "login", data=form_data)
        if "Login successful" not in r.text:
            raise CheckerException(f"Failed to login with {uname=}, {pw=}, {r.status_code=}", self.session)
        else:
            logging.info("Successfully logged in")


    def register_and_login(self, uname, pw):
        logging.info(f"Registering with {uname=}, {pw=}")
        form_data = {"username": uname, "password": pw}
        if self.session: self.session.close()
        self.session = requests.Session()
        r = self.session.post(self.url() + "register", data=form_data)
        if "Registration successful" not in r.text:
            raise CheckerException(f"Failed to register with {uname=}, {pw=}, {r.status_code}", self.session)
        else:
            logging.info("Successfully registered and logged in")

    def fetch_profile(self):
        r = self.session.get(self.url() + "profile")
        return r.text

    def translation_history(self):
        r = self.session.get(self.url() + "translation_history")
        return r.text

    def download_file(self, project_name):
        r = self.session.get(self.url() + f"download_file/{project_name}")
        return r.content

    def getuid(self):
        profile = self.fetch_profile()

        m = re.search(r'User-Id:</span>\s*<span class="field-value">([0-9a-fA-F-]{36})</span>',
            profile,
        )
        if m:
            uid = m.group(1)
            logging.info(f"Fetched uid {uid}")
            return m.group(1)
        else:
            raise CheckerException("Failed to obtain uid", self.session)


    def create_archive(self, filename, file_data, image_name, image_data):
        fh = io.BytesIO()
        with tarfile.open(fileobj=fh, mode="w:") as tar:
            info = tarfile.TarInfo(filename)
            file_bytes = file_data.encode()
            info.size = len(file_bytes)
            tar.addfile(info, io.BytesIO(initial_bytes=file_bytes))
            info = tarfile.TarInfo(image_name)
            info.size = len(image_data)
            tar.addfile(info, io.BytesIO(initial_bytes=image_data))
        return fh.getvalue()

    def translate_file(self, filename, file_data, lang):
        logging.info(f"Performing translation to language {lang}")
        file = {'file': (filename, file_data, 'multipart/form-data')}
        data = {"lang": lang}
        r = self.session.post(self.url() + "convert_file", files=file, data=data)
        if r.status_code != 200:
            raise CheckerException(f"Translation of file failed with status {r.status_code}", self.session)
        return r.content

    def translate_archive(self, project_name, archive_data, lang):
        file = {'file': (project_name, archive_data, 'multipart/form-data')}
        template_data = {"lang": lang}
        r = self.session.post(self.url() + "convert_file", files=file, data=template_data)
        if r.status_code != 200:
            raise CheckerException(f"Translation of file failed with status {r.status_code}", self.session)
        return r.content

    def translate_text(self, text):
        data = {"to_translate": base64.b64encode(text.encode())}
        logging.info(f"Translating {text}")
        if self.session:
            r = self.session.post(self.url() + "translate_text", data=data)
        else:
            r = requests.post(self.url() + "translate_text", data=data)
        if r.status_code != 200:
            raise CheckerException(f"""Translation of text failed with status {r.status_code}.
                                   {r.text=}""", self.session)
        else:
            translation = base64.b64decode(r.text).decode("utf-8", "ignore")
            logging.info(f"Translation returned: {r.text} => {translation}")
        return translation

    @handle_errors()
    def check_translate_text(self):
        logging.info("Checking translation of text")
        (text, expected_translation) = generate_text()
        self.session = None
        translation = self.translate_text(text)
        if translation != expected_translation:
            raise CheckerException(f"Wrong translation. Expected '{expected_translation}', received '{translation}'", self.session)
        logging.info("Text translation succeeded!")


    # Check single typst file translation
    # randomly choose one of n random typst templates
    # insert random text into template
    # translate via server with random font
    # check if pdf has correct font
    # check if pdf contains correct text(via title)
    @handle_errors()
    def check_translate_file(self):
        logging.info("Checking translation of single .typ file")
        (uname, pw) = generate_creds()
        self.register_and_login(uname, pw)
        (filename, data, title) = random_template()
        lang = random.choice(LANGS)
        t1 = time.time()
        pdf = self.translate_file(filename, data, lang)
        t2 = time.time()
        print(f"translate_file:\t{t2-t1}")
        doc = pymupdf.open(stream=pdf, filetype="pdf")
        text = doc[0].get_text()
        fonts = doc[0].get_fonts()
        if not lang in fonts[0][3]:
            raise CheckerException(f"Wrong font, couldnt find {lang} in {fonts}", self.session)
        if not title in text:
            raise CheckerException(f"Wrong title, couldnt find {title} in {text}", self.session)
        logging.info("Translation of single .typ file succeeded!")

    # Check typst archive translation
    # choose random typst template
    # insert reference to image in one chapter
    # fill other chapters with random text
    # bundle main.typ and image to .tar.gz
    # translate via server with random font
    # check if pdf has correct font
    # check if pdf contains correct text(via title)
    @handle_errors()
    def check_translate_archive(self):
        logging.info("Checking translation of archive")
        (uname, pw) = generate_creds()
        self.register_and_login(uname, pw)
        (template_name, template_data, title) = random_multi_template()
        (image_name, image_data) = random_image()
        lang = random.choice(LANGS)
        archive_data = self.create_archive("main.typ", template_data, "image.jpg", image_data)
        archive_name = template_name.split(".")[0] + ".tar"
        pdf = self.translate_archive(archive_name, archive_data, lang)
        doc = pymupdf.open(stream=pdf, filetype="pdf")
        text = doc[0].get_text()
        fonts = doc[0].get_fonts()
        if not lang in fonts[0][3]:
            raise CheckerException(f"Wrong font, couldnt find {lang} in {fonts}", self.session)
        if not title in text:
            raise CheckerException(f"Wrong title, couldnt find {title} in {text}", self.session)
        logging.info("Translation of archive succeeded!")

    @handle_errors()
    def check_feedback(self):
        logging.info("Checking feedback form")
        data = {"email": "",
                "message": generate_message()}
        logging.info(f"Sending {data}")
        if self.session:
            r = self.session.post(self.url() + "contact_form", data=data)
        else:
            r = requests.post(self.url() + "contact_form", data=data)
        if not "Thank you for your feeback!" in r.text:
            raise CheckerException("Feedback form check failed lol")
        logging.info("Feedback form check succeeded!")

    
    def check_service(self):
        checks = [
            self.check_translate_archive,
            self.check_translate_file,
            self.check_translate_text,
            self.check_feedback
        ]
        random.shuffle(checks)
        for check in checks:
            res = check()
            if res != checkerlib.CheckResult.OK:
                return res
            logging.info("Check DONE\n")
        return checkerlib.CheckResult.OK

    @handle_errors()
    def place_flag(self, tick: int) -> checkerlib.CheckResult:
        # FLAG 1 in translation history
        flag = checkerlib.get_flag(tick, 0)
        (uname, pw) = generate_creds()
        checkerlib.store_state(str(tick)+"_0", {"flag": flag, "uname": uname, "pw": pw})
        self.register_and_login(uname, pw)
        self.translate_text(flag + ".")
        uid = self.getuid()
        checkerlib.set_flagid(uid, 0)
        logging.info("Flag 1 placed")

        # FLAG 2 in pdf
        flag = checkerlib.get_flag(tick, 1)
        (uname, pw) = generate_creds()
        self.register_and_login(uname, pw) 
        lang = random.choice(LANGS)
        content = f"`{flag}`"
        _ = self.translate_file("flag.typ", content, lang)
        checkerlib.store_state(str(tick)+"_1", {"flag": flag, "uname": uname, "pw": pw})
        uid = self.getuid()
        checkerlib.set_flagid(uid, 1)
        logging.info("Flag 2 placed")

        return checkerlib.CheckResult.OK

    @handle_errors(checkerlib.CheckResult.FLAG_NOT_FOUND)
    def check_flag(self, tick: int) -> checkerlib.CheckResult:
        # FLAG 1 in translation history
        state = checkerlib.load_state(str(tick)+"_0")
        if state is None:
            logging.error("Unable to load state for flag_0. Cant check flag.")
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        self.login(state["uname"], state["pw"])
        translation_history = self.translation_history()
        if state["flag"] not in translation_history:
            logging.error("Couldnt find flag 1")
            logging.error(f"Should be in {translation_history}")
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        logging.info("Flag 1 check success")

        # FLAG 2
        state = checkerlib.load_state(str(tick)+"_1")
        if state is None:
            logging.error("Unable to load state for flag_1. Cant check flag.")
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        self.login(state["uname"], state["pw"])
        pdf = self.download_file("flag")
        doc = pymupdf.open(stream=pdf, filetype="pdf")
        text = doc[0].get_text()
        if state["flag"] not in text:
            logging.error(f"Couldnt find flag 2: {state["flag"]}")
            logging.error(f"Should be in {text}")
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        logging.info("Flag 2 check success")

        return checkerlib.CheckResult.OK

if __name__ == '__main__':
    t1 = time.time()
    checkerlib.run_check(TemplateChecker)
    print(f"Whole run took {time.time()-t1}s")
