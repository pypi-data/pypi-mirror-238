import sys
import os
import subprocess
import json
import random
import logging
import shutil
from PIL import Image
from pathlib import Path

from template_generator import binary
from template_generator import aigc_input
from template_res import template as template_res_search

def getCommandResult(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        else:
            return ""
    except subprocess.CalledProcessError as e:
        logging.info(f"getCommandResult fail {e}")
        return ""
    
def getBinary(searchPath, useHardware=False):
    binaryPath = ""
    if sys.platform == "win32":
        binaryPath = os.path.join(os.path.join(binary.skymediaPath(searchPath), "win"), "TemplateProcess.exe")
    elif sys.platform == "linux":
        binaryPath = os.path.join(binary.skymediaPath(searchPath), "linux", "TemplateProcess.out")
        if os.path.exists(binaryPath):
            cmd = subprocess.Popen(f"chmod 755 {binaryPath}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while cmd.poll() is None:
                print(cmd.stdout.readline().rstrip().decode('utf-8'))
        #check env
        if os.path.exists("/usr/lib/libskycore.so") == False:
            print(f"=== begin setup env")
            setupShell = os.path.join(binary.skymediaPath(searchPath), "linux", "setup.sh")
            if os.path.exists(setupShell):
                print(f"=== sh {setupShell}")
                getCommandResult(f"sh {setupShell}")
            if os.path.exists("/usr/lib/libskycore.so") == False:
                raise Exception("linux environment error")
        if len(getCommandResult("echo $XDG_SESSION_TYPE")) <= 0 and len(getCommandResult("echo $DISPLAY")) <= 0 and useHardware:
            #no x11 or wayland , check Xvfb
            displayShell = os.path.join(binary.skymediaPath(searchPath), "linux", "display.sh")
            if os.path.exists(displayShell):
                print(f"=== sh {displayShell}")
                cmd1 = subprocess.Popen(f"sh {displayShell}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                while cmd1.poll() is None:
                    print(cmd1.stdout.readline().rstrip().decode('utf-8'))

            
    if os.path.exists(binaryPath):
        return os.path.dirname(binaryPath), os.path.basename(binaryPath)
    else:
        return "", ""
    
def transcode(f):
    try:
        file_name = Path(f).name
        ext = file_name[file_name.index("."):].lower()
        if ext in [".webp"]:
            image = Image.open(f, "r")
            format = image.format
            if format.lower() == "webp":
                newFile = f"{f}.png"
                image.save(newFile, "png")
                image.close()
                return True, newFile
    except:
        return False, f
    return False, f
    
def resetInput(data, tmp_file_cache):
    newInput = []
    for s in data["input"]:
        needDeleteSrc, newSrc = transcode(s)
        if needDeleteSrc:
            tmp_file_cache.append(newSrc)
        newInput.append(newSrc)
    data["input"] = newInput
    
def resetTemplate(data, searchPath):
    template_path = data["template"]
    if os.path.exists(template_path):
        return
    #local random effects
    randomEffectPath = binary.randomEffectPath(searchPath)
    local_random_template_path = os.path.join(randomEffectPath, template_path)
    if os.path.exists(local_random_template_path):
        data["template"] = local_random_template_path
        return
    #template info with mecord server
    server_templates = template_res_search.listTemplate(searchPath, template_path)
    if len(server_templates) > 0:
        data["template"] = server_templates[0]["path"]
        return
    raise Exception(f"template {template_path} not found")
    
def isAdaptiveSize(data):
    template_path = data["template"]
    templateName = os.path.basename(template_path)
    if "template" in templateName or templateName == "AIGC_1":
        return True
    return False

def maybeMesa(useHardware=False):
    if sys.platform == "linux":
        if len(getCommandResult("echo $XDG_SESSION_TYPE")) <= 0 and len(getCommandResult("echo $DISPLAY")) <= 0:
            #no (x11 or wayland) and (xvfb not found)
            return True
        elif useHardware:
            return False
        else:
            return True
    else:
        return False

def maybeSoftWare(useHardware=False):
    if sys.platform == "linux":
        if os.path.exists("/usr/lib/x86_64-linux-gnu/libnvcuvid.so") and os.path.exists("/usr/lib/x86_64-linux-gnu/libnvidia-encode.so") and useHardware:
            return False
        else:
            return True
    else:
        return True
    
def realCommand(cmd):
    if sys.platform != "win32":
        return "./" + " ".join(cmd)
    else:
        return cmd
    
def executeTemplate(data, searchPath, useAdaptiveSize, useHardware=False, printLog=True):
    binary_dir, binary_file = getBinary(searchPath, useHardware)
    if len(binary_dir) <= 0:
        raise Exception("binary not found")

    tmp_file_cache = []
    tmp_dir_cache = []
    output_path = ""
    if isinstance(data, (dict)):
        output_path = data["output"]
        resetInput(data, tmp_file_cache)
        resetTemplate(data, searchPath)
        useAdaptiveSize = useAdaptiveSize or isAdaptiveSize(data)
        aigc_input.preProcessAIGC(data,tmp_file_cache,tmp_dir_cache)
    elif isinstance(data, (list)):
        for it in data:
            output_path = it["output"]
            resetInput(it, tmp_file_cache)
            resetTemplate(it, searchPath)
            useAdaptiveSize = useAdaptiveSize or isAdaptiveSize(it)
            aigc_input.preProcessAIGC(it,tmp_file_cache,tmp_dir_cache)

    inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{random.randint(100,99999999)}.in")
    tmp_file_cache.append(inputArgs)
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w') as f:
        json.dump(data, f)

    extArgs = []
    #--adaptiveSize
    if useAdaptiveSize:
        extArgs += ["--adaptiveSize", "true"]
    #--fontDir
    fontPath = binary.fontPath(searchPath)
    if os.path.exists(fontPath):
        extArgs += ["--fontDir", fontPath]
    #--subEffectDir
    subPath = binary.subEffectPath(searchPath)
    if os.path.exists(subPath):
        extArgs += ["--subEffectDir", subPath]
    #--gpu
    if sys.platform == "linux" and maybeMesa(useHardware):
        extArgs += ["--call_mesa"]
    if sys.platform == "linux" and maybeSoftWare(useHardware):
        extArgs += ["--call_software"]

    command = [binary_file, "--config", inputArgs] + extArgs
    command = realCommand(command)
    if printLog:
        print(f"=== executeTemplate => {command}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
    if result.returncode == 0:
        for t in tmp_file_cache:
            os.remove(t)
        for t in tmp_dir_cache:
            shutil.rmtree(t)
        #check one output
        if os.path.exists(output_path) == False:
            logging.info(f"output file not found")
            raise Exception("output file not found")
        if printLog:
            print(result.stdout.decode(encoding="utf8", errors="ignore"))
    else:
        for t in tmp_file_cache:
            os.remove(t)
        for t in tmp_dir_cache:
            shutil.rmtree(t)
        err_msg = result.stdout.decode(encoding="utf8", errors="ignore")
        logging.info(f"executeTemplate err {err_msg}")
        if printLog:
            print(err_msg)
        raise Exception(f"template process exception!")
    
def generateTemplate(config, output, searchPath, useHardware=False, printLog=True):        
    binary_dir, binary_file = getBinary(searchPath, useHardware)
    if len(binary_dir) <= 0:
        raise Exception("binary not found")
    
    if os.path.exists(config) == False:
        raise Exception("input config not exist")

    if os.path.exists(output) == False:
        os.makedirs(output)

    command = [binary_file, "--project", config ,"-y", output]
    command = realCommand(command)
    if printLog:
        print(f"=== generateTemplate => {command}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
    if result.returncode != 0:
        err_msg = result.stdout.decode(encoding="utf8", errors="ignore")
        logging.info(f"generateTemplate err {err_msg}")
        if printLog:
            print(err_msg)
        raise Exception(f"generate template exception!")
    
def decrypt(path, searchPath):
    binary_dir, binary_file = getBinary(searchPath)
    if len(binary_dir) <= 0:
        raise Exception("binary not found")

    command = [binary_file, "--decrypt", path]
    command = realCommand(command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
    if result.returncode == 0:
        return 
    else:
        raise Exception(f"decrypt process exception!")
    