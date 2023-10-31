import sys
import os
import time
import json
import threading
from urllib.parse import urlparse
from pathlib import Path
import requests
import zipfile
from urllib.parse import *
import shutil
import hashlib
from mecord.pb import mecord_ext_pb2 
from mecord.pb import rpcinput_pb2 

COUNTRY_DOMAIN = {
    "us" : "https://api.mecordai.com/proxymsg",
    "sg" : "https://api-sg.mecordai.com/proxymsg",
    "test" : "https://mecord-beta.2tianxin.com/proxymsg"
}
class MecordService:
    def _domain(self, country):
        domain = COUNTRY_DOMAIN["us"]
        if country.lower() in COUNTRY_DOMAIN:
            domain = COUNTRY_DOMAIN[country.lower()]
        return domain
        
    def __init__(self):
        self.checking = False
        self.result = False, "Unknow"
        self.checkUUID = ""
        self.checkCount = 0

    def _post(self, country, request, function):
        req = request.SerializeToString()
        opt = {
            "lang": "zh-Hans",
            "region": "CN",
            "appid": "80",
            "application": "template_res",
            "version": "1.0",
            "uid": "1",
        }
        input_req = rpcinput_pb2.RPCInput(obj="mecord.mecord.MecordExtObj", func=function, req=req, opt=opt)
        s = requests.session()
        try:
            requests.adapters.DEFAULT_RETRIES = 2
            s.keep_alive = False
            s.headers.update({'Connection':'close'})
            res = s.post(url=self._domain(country), data=input_req.SerializeToString())
            if res.status_code == 200:
                res_content = res.content
                res.close()
                pb_rsp = rpcinput_pb2.RPCOutput()
                pb_rsp.ParseFromString(res_content)
                if pb_rsp.ret == 0:
                    return 0, "", pb_rsp.rsp
                else:
                    return pb_rsp.ret, pb_rsp.desc, "" 
        except Exception as e:
            return -1, f"error : {e}", ""
        finally:
            s.close()
    
    def getPackageUrlWithTid(self, tid):
        for service_country in ["us", "sg", "test"]:
            req = mecord_ext_pb2.PostTemplateListReq()
            req.page=0
            req.page_size=1
            req.name=""
            req.tid=tid
            rsp = mecord_ext_pb2.PostTemplateListRsp()
            r1, r2, r3 = self._post(service_country, req, "PostTemplateList")
            if r1 == 0:
                rsp.ParseFromString(r3)
                if rsp.count==1:
                    return rsp.items[0].pkg_url
        return None

def _download_template_dir():
    dd = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".download")
    if os.path.exists(dd) == False:
        os.makedirs(dd)
    return dd

def checkTemplateIs30(tid_dir):
    requiredList = [
        os.path.join(tid_dir, "template.proj")
    ]
    optionList = [
        os.path.join(tid_dir, "skyinput0.conf"),
        os.path.join(tid_dir, "inputList.conf")
    ]
    required = True
    for ii in requiredList:
        if os.path.exists(ii) == False:
            required = False
            break
    hasOption = False
    for jj in optionList:
        if os.path.exists(jj):
            hasOption = True
            break
    return required and hasOption

def calculate_hash(s):
    hash_object = hashlib.sha256()
    hash_object.update(s.encode('utf-8'))
    hash_value = hash_object.hexdigest()
    return hash_value

def getTemplateWithTid(tid):
    pkg_url = MecordService().getPackageUrlWithTid(tid)
    if pkg_url:
        tid_dir = os.path.join(_download_template_dir(), f"{tid}_{calculate_hash(pkg_url)}")
        if os.path.exists(tid_dir):
            if checkTemplateIs30(tid_dir):
                return tid_dir
            else:
                shutil.rmtree(tid_dir)

        #clear old zip or dir
        for root,dirs,files in os.walk(_download_template_dir()):
            for dir in dirs:
                if dir.find("_") <= 0:
                    continue
                name = dir[0:dir.rindex("_")]
                if name == tid:
                    shutil.rmtree(os.path.join(_download_template_dir(), dir))
            if root != files:
                break

        zipSavePath = os.path.join(_download_template_dir(), f"{tid}.zip")
        if os.path.exists(zipSavePath):
            os.remove(zipSavePath)
        s = requests.session()
        s.keep_alive = False
        file = s.get(pkg_url, verify=False)
        with open(zipSavePath, "wb") as c:
            c.write(file.content)
        s.close()
        if os.path.exists(zipSavePath):
            try:
                with zipfile.ZipFile(zipSavePath, "r") as zipf:
                    zipf.extractall(tid_dir)
                os.remove(zipSavePath)
                if checkTemplateIs30(tid_dir):
                    return tid_dir
                else:
                    shutil.rmtree(tid_dir)
            except:
                if os.path.exists(tid_dir):
                    shutil.rmtree(tid_dir)
    return None
        
# print(getTemplateWithTid("TEMPLATE_WANSHENGJIE_HENG"))
# result_url_path = urlparse("https://m.mecordai.com/template/7b8a9e6b1f024eb29bbb4e6ba3af73a7.zip").path
# savePath = os.path.join(_download_template_dir(), f"{Path(result_url_path).stem}{Path(result_url_path).suffix}")
# print(savePath)
# savePath1 = os.path.join(_download_template_dir(), f"{Path(result_url_path).stem}")
# print(savePath1)