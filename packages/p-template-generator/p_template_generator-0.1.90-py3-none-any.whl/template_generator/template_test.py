import sys
import os
import subprocess
import json
import shutil
import zipfile
from template_generator import template
from template_generator import binary
from template_generator import server_generator

def updateRes(rootDir):
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                return
        if root != files:
            break

def test(searchPath):
    rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
    updateRes(rootDir)
    config = {
        "input":[
            os.path.join(rootDir, "res", "1.png"),
            os.path.join(rootDir, "res", "2.png"),
            os.path.join(rootDir, "res", "3.png"),
            os.path.join(rootDir, "res", "4.png"),
            ],
        "template":os.path.join(rootDir, "res", "tp"),
        "params":{},
        "output":os.path.join(rootDir, "res", "out.mp4")
        }
    with open(os.path.join(rootDir, "res", "param.config"), 'w') as f:
        json.dump(config, f)

    command = f'template --input "{os.path.join(rootDir, "res", "param.config")}"'
    print(f"test template command => {command}")
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while cmd.poll() is None:
        print(cmd.stdout.readline().rstrip().decode('utf-8'))

def testAigc(cnt):
    for i in range(0,cnt):
        try:
            inputs = []
            output_width = 100
            output_height = 100
            fn_name = "aicamera"
            params = {"batch_count":1,"batch_size":1,"cfg_scale":7,"creative_strength":1,"denoising_strength":1,"era":"spaceSuit","face_index":1,"fn_name":"aicamera","func":"d849eff2cfb2d09a0bb7ae573e69b1cc.png","height":1536,"musicUrl":"","negative_prompt":"","package_url":"https://m-beta-yesdesktop.2tianxin.com/upload/beta/undefined/6079/2763/607947D9CFD52763.zip","prompt":"","restore_faces":True,"sampler_index":"DPM++ SDE Karras","scratch":1,"seed":-1,"steps":25,"text_mark_url":"","type":"image","user_file_name":"d59e9302-f17f-4468-aa23-5b3fd3d44685.png","user_url":"","width":1152}
            server_generator.MecordAIGC().testTask(348 , inputs, fn_name, params, output_width, output_height)
            print("pushed one!")
        except:
            print("")
# testAigc(30)
# def testToon():
#     try:
#         inputs = []
#         output_width = 100
#         output_height = 100
#         fn_name = "Toon"
#         params = {"batch_count":1,"batch_size":1,"cfg_scale":8,"creative_strength":1,"denoising_strength":1,"fn_name":"Toon","height":1024,"model_name":"toonyou_beta6.safetensors","musicUrl":"","negative_prompt":"","package_url":"https://m.mecordai.com/upload/prod/background_img/6065/4068/6065116F5E8E9104068.zip","prompt":"","restore_faces":False,"sampler_index":"DPM++ 2M Karras","seed":-1,"steps":30,"text_mark_url":"","type":"image","user_file_name":"resize_6cc1dbabdec15875b221275e02f30e50_exif.jpg","user_url":"","width":1024}
#         MecordAIGC().testTask(200, inputs, fn_name, params, output_width, output_height)
#         print("pushed one!")
#     except:
#         print("")

# def psnr(target, ref, scale):
#     target_data = np.array(target)
#     target_data = target_data[scale:-scale,scale:-scale]
 
#     ref_data = np.array(ref)
#     ref_data = ref_data[scale:-scale,scale:-scale]
 
#     diff = ref_data - target_data
#     diff = diff.flatten('C')
#     rmse = math.sqrt(np.mean(diff ** 2.) )
#     return 20*math.log10(1.0/rmse)

# import cv2
# import numpy as np
# import math
# def calculate_psnr(original_img, compressed_img):
#     img1 = cv2.imread(original_img)
#     img2 = cv2.imread(compressed_img)

#     gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#     mse = np.mean((gray_img1 - gray_img2) ** 2)

#     if mse == 0:
#         return float('inf')

#     max_pixel = 255.0
#     psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
#     return psnr

# from skimage.metrics import structural_similarity as compare_ssim
# def calculate_ssim(original_img, compressed_img):
#     img1 = cv2.imread(original_img)
#     img2 = cv2.imread(compressed_img)
#     gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#     score, diff = compare_ssim(gray1, gray2, full=True)
#     return score

# psnr_score = calculate_psnr("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "C:\\Users\\123\\Downloads\\3333\\mohu.jpg")
# print(f"================== PSNR分数为：{psnr_score:.2f}")
# psnr_score = calculate_psnr("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "E:\\template\\111111111111111111111111111111111111111111package\\test\\out.png")
# print(f"================== PSNR分数为：{psnr_score:.2f}")
# psnr_score = calculate_psnr("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "E:\\template\\111111111111111111111111111111111111111111package\\test\\out_stb.png")
# print(f"================== PSNR分数为：{psnr_score:.2f}")

# ssim_score = calculate_ssim("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "C:\\Users\\123\\Downloads\\3333\\mohu.jpg")
# print(f"================== SSIM分数为：{ssim_score:.2f}")
# ssim_score = calculate_ssim("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "E:\\template\\111111111111111111111111111111111111111111package\\test\\out.png")
# print(f"================== SSIM分数为：{ssim_score:.2f}")
# ssim_score = calculate_ssim("C:\\Users\\123\\Downloads\\3333\\heidao-shu_video-cover.jpg",
#                              "E:\\template\\111111111111111111111111111111111111111111package\\test\\out_stb.png")
# print(f"================== SSIM分数为：{ssim_score:.2f}")