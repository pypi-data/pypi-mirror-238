#!/usr/bin/env python
# coding: utf-8
# 趋势分析工具Trend Analysis Tools 
# 开发人：蔡权周
# 第一部分：导入基本模块及初始化 ########################################################################
# 导入一些基本模块
import warnings #line:7
import traceback #line:8
import ast #line:9
import re #line:10
import xlrd #line:11
import xlwt #line:12
import openpyxl #line:13
import pandas as pd #line:14
import numpy as np #line:15
import math #line:16
import tkinter as Tk #line:17
from tkinter import ttk #line:18
from tkinter import *#line:19
import tkinter .font as tkFont #line:20
from tkinter import filedialog ,dialog ,PhotoImage #line:21
from tkinter .messagebox import showinfo #line:22
from tkinter .scrolledtext import ScrolledText #line:23
import collections #line:24
from collections import Counter #line:25
import datetime #line:26
from datetime import datetime ,timedelta #line:27
from tkinter import END #line:28
import xlsxwriter #line:29
import os #line:30
import time #line:31
import threading #line:32
import pip #line:33
import matplotlib as plt #line:34
import requests #line:35
import random #line:36
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:38
from matplotlib .figure import Figure #line:39
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:40
from matplotlib .ticker import PercentFormatter #line:41
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:42
pd .options .display .float_format ="{:,.12f}".format #line:43
global TT_ori #line:45
global TT_biaozhun #line:46
global TT_modex #line:47
global TT_ori_backup #line:48
global version_now #line:49
global usergroup #line:50
global setting_cfg #line:51
global csdir #line:52
TT_biaozhun ={}#line:53
TT_ori =""#line:54
TT_modex =0 #line:55
TT_ori_backup =""#line:56
version_now ="0.0.18"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:61
if csdir =="":#line:62
    csdir =str (os .path .dirname (__file__ ))#line:63
    csdir =csdir +csdir .split ("treadtools")[0 ][-1 ]#line:64
def extract_zip_file (OO0O0000OO0O00000 ,OO00OOOO000000OO0 ):#line:73
    import zipfile #line:75
    if OO00OOOO000000OO0 =="":#line:76
        return 0 #line:77
    with zipfile .ZipFile (OO0O0000OO0O00000 ,'r')as O0OO00000000OO000 :#line:78
        for OOOO0O0OOO0OO0O00 in O0OO00000000OO000 .infolist ():#line:79
            OOOO0O0OOO0OO0O00 .filename =OOOO0O0OOO0OO0O00 .filename .encode ('cp437').decode ('gbk')#line:81
            O0OO00000000OO000 .extract (OOOO0O0OOO0OO0O00 ,OO00OOOO000000OO0 )#line:82
def get_directory_path (OOOO00OO000OOO0OO ):#line:88
    global csdir #line:90
    if not (os .path .isfile (os .path .join (OOOO00OO000OOO0OO ,'规则文件.xls'))):#line:92
        extract_zip_file (csdir +"def.py",OOOO00OO000OOO0OO )#line:97
    if OOOO00OO000OOO0OO =="":#line:99
        quit ()#line:100
    return OOOO00OO000OOO0OO #line:101
def convert_and_compare_dates (O0OO0O000OOO0000O ):#line:105
    import datetime #line:106
    O0OO0000O0000O0OO =datetime .datetime .now ()#line:107
    try :#line:109
       O000OOO0000OOO000 =datetime .datetime .strptime (str (int (int (O0OO0O000OOO0000O )/4 )),"%Y%m%d")#line:110
    except :#line:111
        print ("fail")#line:112
        return "已过期"#line:113
    if O000OOO0000OOO000 >O0OO0000O0000O0OO :#line:115
        return "未过期"#line:117
    else :#line:118
        return "已过期"#line:119
def read_setting_cfg ():#line:121
    global csdir #line:122
    if os .path .exists (csdir +'setting.cfg'):#line:124
        text .insert (END ,"已完成初始化\n")#line:125
        with open (csdir +'setting.cfg','r')as OO0O0O00O0O0O0OOO :#line:126
            OOO0O00O000O000O0 =eval (OO0O0O00O0O0O0OOO .read ())#line:127
    else :#line:128
        OO00OOO00O0000O0O =csdir +'setting.cfg'#line:130
        with open (OO00OOO00O0000O0O ,'w')as OO0O0O00O0O0O0OOO :#line:131
            OO0O0O00O0O0O0OOO .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:132
        text .insert (END ,"未初始化，正在初始化...\n")#line:133
        OOO0O00O000O000O0 =read_setting_cfg ()#line:134
    return OOO0O00O000O000O0 #line:135
def open_setting_cfg ():#line:138
    global csdir #line:139
    with open (csdir +"setting.cfg","r")as OO0O0OOO0OO0O000O :#line:141
        O000O00OOOOO0000O =eval (OO0O0OOO0OO0O000O .read ())#line:143
    return O000O00OOOOO0000O #line:144
def update_setting_cfg (O0O00O0000O0OOO00 ,OO0000000OOOOO00O ):#line:146
    global csdir #line:147
    with open (csdir +"setting.cfg","r")as OOO00O000OO00000O :#line:149
        O00OO00O00O0OOOOO =eval (OOO00O000OO00000O .read ())#line:151
    if O00OO00O00O0OOOOO [O0O00O0000O0OOO00 ]==0 or O00OO00O00O0OOOOO [O0O00O0000O0OOO00 ]=="11111180000808":#line:153
        O00OO00O00O0OOOOO [O0O00O0000O0OOO00 ]=OO0000000OOOOO00O #line:154
        with open (csdir +"setting.cfg","w")as OOO00O000OO00000O :#line:156
            OOO00O000OO00000O .write (str (O00OO00O00O0OOOOO ))#line:157
def generate_random_file ():#line:160
    OO0OOOOO00OO0OOO0 =random .randint (200000 ,299999 )#line:162
    update_setting_cfg ("sidori",OO0OOOOO00OO0OOO0 )#line:164
def display_random_number ():#line:166
    global csdir #line:167
    OO0OOO0OO0000O000 =Toplevel ()#line:168
    OO0OOO0OO0000O000 .title ("ID")#line:169
    O0O00OOOO0O0OOOO0 =OO0OOO0OO0000O000 .winfo_screenwidth ()#line:171
    OO00O0000O000000O =OO0OOO0OO0000O000 .winfo_screenheight ()#line:172
    O000OO0000OOOOO0O =80 #line:174
    OO00O000O0O000O0O =70 #line:175
    O0O0000O0OO000OO0 =(O0O00OOOO0O0OOOO0 -O000OO0000OOOOO0O )/2 #line:177
    O0OO00O0O0O0O0O00 =(OO00O0000O000000O -OO00O000O0O000O0O )/2 #line:178
    OO0OOO0OO0000O000 .geometry ("%dx%d+%d+%d"%(O000OO0000OOOOO0O ,OO00O000O0O000O0O ,O0O0000O0OO000OO0 ,O0OO00O0O0O0O0O00 ))#line:179
    with open (csdir +"setting.cfg","r")as OOO0OO0O0O00O0O0O :#line:182
        OO000O0OO0OO0O0O0 =eval (OOO0OO0O0O00O0O0O .read ())#line:184
    O0OO0OO0O00OO0O00 =int (OO000O0OO0OO0O0O0 ["sidori"])#line:185
    O0OOOOO0000O000OO =O0OO0OO0O00OO0O00 *2 +183576 #line:186
    print (O0OOOOO0000O000OO )#line:188
    O00O00OOO00000OOO =ttk .Label (OO0OOO0OO0000O000 ,text =f"机器码: {O0OO0OO0O00OO0O00}")#line:190
    OOOOO00O0000O0000 =ttk .Entry (OO0OOO0OO0000O000 )#line:191
    O00O00OOO00000OOO .pack ()#line:194
    OOOOO00O0000O0000 .pack ()#line:195
    ttk .Button (OO0OOO0OO0000O000 ,text ="验证",command =lambda :check_input (OOOOO00O0000O0000 .get (),O0OOOOO0000O000OO )).pack ()#line:199
def check_input (O0000O0OOOO0O0000 ,O00O00OO000OOOO0O ):#line:201
    try :#line:205
        O0OOOOO00OO00OOOO =int (str (O0000O0OOOO0O0000 )[0 :6 ])#line:206
        O0O00O00O0O0OO00O =convert_and_compare_dates (str (O0000O0OOOO0O0000 )[6 :14 ])#line:207
    except :#line:208
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:209
        return 0 #line:210
    if O0OOOOO00OO00OOOO ==O00O00OO000OOOO0O and O0O00O00O0O0OO00O =="未过期":#line:212
        update_setting_cfg ("sidfinal",O0000O0OOOO0O0000 )#line:213
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:214
        quit ()#line:215
    else :#line:216
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:217
def Tread_TOOLS_fileopen (O0OOOOOOOO00OO00O ):#line:225
    ""#line:226
    global TT_ori #line:227
    global TT_ori_backup #line:228
    global TT_biaozhun #line:229
    warnings .filterwarnings ('ignore')#line:230
    if O0OOOOOOOO00OO00O ==0 :#line:232
        OOO000OOOOOO00000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:233
        O00OOO0OO0O0OOOOO =[pd .read_excel (OOOO0O0O000O0OOOO ,header =0 ,sheet_name =0 )for OOOO0O0O000O0OOOO in OOO000OOOOOO00000 ]#line:234
        O00OOOOO000000OO0 =pd .concat (O00OOO0OO0O0OOOOO ,ignore_index =True ).drop_duplicates ()#line:235
        try :#line:236
            O00OOOOO000000OO0 =O00OOOOO000000OO0 .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:237
        except :#line:238
            pass #line:239
        TT_ori_backup =O00OOOOO000000OO0 .copy ()#line:240
        TT_ori =Tread_TOOLS_CLEAN (O00OOOOO000000OO0 ).copy ()#line:241
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:243
        text .insert (END ,"\n数据校验：\n")#line:244
        text .insert (END ,TT_ori )#line:245
        text .see (END )#line:246
    if O0OOOOOOOO00OO00O ==1 :#line:248
        O000OO0000OOOOOOO =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:249
        TT_biaozhun ["关键字表"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:250
        TT_biaozhun ["产品批号"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:251
        TT_biaozhun ["事件发生月份"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:252
        TT_biaozhun ["事件发生季度"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:253
        TT_biaozhun ["规格"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:254
        TT_biaozhun ["型号"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:255
        TT_biaozhun ["设置"]=pd .read_excel (O000OO0000OOOOOOO ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:256
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:257
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:258
        text .see (END )#line:259
def Tread_TOOLS_check (O00OO0O0O000O00O0 ,O00O000OOO00O0O0O ,O00OO0OOOO0O00000 ):#line:261
        ""#line:262
        global TT_ori #line:263
        O0O0OOOOO0OO0O0O0 =Tread_TOOLS_Countall (O00OO0O0O000O00O0 ).df_psur (O00O000OOO00O0O0O )#line:264
        if O00OO0OOOO0O00000 ==0 :#line:266
            Tread_TOOLS_tree_Level_2 (O0O0OOOOO0OO0O0O0 ,0 ,TT_ori .copy ())#line:268
        O0O0OOOOO0OO0O0O0 ["核验"]=0 #line:271
        O0O0OOOOO0OO0O0O0 .loc [(O0O0OOOOO0OO0O0O0 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=O0O0OOOOO0OO0O0O0 .loc [(O0O0OOOOO0OO0O0O0 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:272
        if O0O0OOOOO0OO0O0O0 ["核验"].sum ()>0 :#line:273
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (O0O0OOOOO0OO0O0O0 ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:274
def Tread_TOOLS_tree_Level_2 (OOOOOO0O0OO00OOOO ,O000O0O0OOOOOO00O ,OOOOO0O00000O0000 ,*O00OOO0OOO0O00000 ):#line:276
    ""#line:277
    global TT_ori_backup #line:279
    O00OOOOO0OOO00OOO =OOOOOO0O0OO00OOOO .columns .values .tolist ()#line:281
    O000O0O0OOOOOO00O =0 #line:282
    OO0000OO0OOO00000 =OOOOOO0O0OO00OOOO .loc [:]#line:283
    OO0OO0OO000O000O0 =0 #line:287
    try :#line:288
        OOOOOO0OO00OO00O0 =O00OOO0OOO0O00000 [0 ]#line:289
        OO0OO0OO000O000O0 =1 #line:290
    except :#line:291
        pass #line:292
    OOOOOO0O0OOOOOO00 =Toplevel ()#line:295
    OOOOOO0O0OOOOOO00 .title ("报表查看器")#line:296
    O0OOO00OOOO000O0O =OOOOOO0O0OOOOOO00 .winfo_screenwidth ()#line:297
    O00O00O0000OO000O =OOOOOO0O0OOOOOO00 .winfo_screenheight ()#line:299
    O0O0O00000OOOOOOO =1300 #line:301
    O00OOO00000OOOOO0 =600 #line:302
    OO0O0O000O0OOOOOO =(O0OOO00OOOO000O0O -O0O0O00000OOOOOOO )/2 #line:304
    O0O0000OO00OOO0OO =(O00O00O0000OO000O -O00OOO00000OOOOO0 )/2 #line:305
    OOOOOO0O0OOOOOO00 .geometry ("%dx%d+%d+%d"%(O0O0O00000OOOOOOO ,O00OOO00000OOOOO0 ,OO0O0O000O0OOOOOO ,O0O0000OO00OOO0OO ))#line:306
    OOOO000O0O0O0OOO0 =ttk .Frame (OOOOOO0O0OOOOOO00 ,width =1300 ,height =20 )#line:307
    OOOO000O0O0O0OOO0 .pack (side =BOTTOM )#line:308
    O00OO000OOO0OOOOO =ttk .Frame (OOOOOO0O0OOOOOO00 ,width =1300 ,height =20 )#line:310
    O00OO000OOO0OOOOO .pack (side =TOP )#line:311
    if 1 >0 :#line:315
        O0OOOO0OO0000OOO0 =Button (OOOO000O0O0O0OOO0 ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO0000OO0OOO00000 [:-1 ],OOOOOO0OO00OO00O0 ,[OOO0O00O0OO00OOOO for OOO0O00O0OO00OOOO in OO0000OO0OOO00000 .columns if (OOO0O00O0OO00OOOO not in [OOOOOO0OO00OO00O0 ])],"关键字趋势图",100 ),)#line:325
        if OO0OO0OO000O000O0 ==1 :#line:326
            O0OOOO0OO0000OOO0 .pack (side =LEFT )#line:327
        O0OOOO0OO0000OOO0 =Button (OOOO000O0O0O0OOO0 ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO0000OO0OOO00000 [:-1 ],OOOOOO0OO00OO00O0 ,[OO000O0OO00O0O000 for OO000O0OO00O0O000 in OO0000OO0OOO00000 .columns if (OO000O0OO00O0O000 in ["该元素总数量"])],"关键字趋势图",100 ),)#line:337
        if OO0OO0OO000O000O0 ==1 :#line:338
            O0OOOO0OO0000OOO0 .pack (side =LEFT )#line:339
        O0O00000OOOO0OO0O =Button (OOOO000O0O0O0OOO0 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (OO0000OO0OOO00000 ),)#line:349
        O0O00000OOOO0OO0O .pack (side =LEFT )#line:350
        O0O00000OOOO0OO0O =Button (OOOO000O0O0O0OOO0 ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (OO0000OO0OOO00000 ,OOOOOO0OO00OO00O0 ),)#line:360
        if "关键字标记"not in OO0000OO0OOO00000 .columns and "报告编码"not in OO0000OO0OOO00000 .columns :#line:361
            if "对象"not in OO0000OO0OOO00000 .columns :#line:362
                O0O00000OOOO0OO0O .pack (side =LEFT )#line:363
        O0O00000OOOO0OO0O =Button (OOOO000O0O0O0OOO0 ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (OO0000OO0OOO00000 .copy ()),)#line:373
        if "对象"in OO0000OO0OOO00000 .columns :#line:374
            O0O00000OOOO0OO0O .pack (side =LEFT )#line:375
        OO0OOOO0O0OO000OO =Button (OOOO000O0O0O0OOO0 ,text ="行数:"+str (len (OO0000OO0OOO00000 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:385
        OO0OOOO0O0OO000OO .pack (side =LEFT )#line:386
    O0O0O0OOOOO00000O =OO0000OO0OOO00000 .values .tolist ()#line:389
    O0OOOO00O00OO0OOO =OO0000OO0OOO00000 .columns .values .tolist ()#line:390
    OO0O0OOOOO0O0O000 =ttk .Treeview (O00OO000OOO0OOOOO ,columns =O0OOOO00O00OO0OOO ,show ="headings",height =45 )#line:391
    for OOO0OO0OO0O00OO0O in O0OOOO00O00OO0OOO :#line:393
        OO0O0OOOOO0O0O000 .heading (OOO0OO0OO0O00OO0O ,text =OOO0OO0OO0O00OO0O )#line:394
    for OOOO00OO000OO0O0O in O0O0O0OOOOO00000O :#line:395
        OO0O0OOOOO0O0O000 .insert ("","end",values =OOOO00OO000OO0O0O )#line:396
    for O000000000O00O000 in O0OOOO00O00OO0OOO :#line:397
        OO0O0OOOOO0O0O000 .column (O000000000O00O000 ,minwidth =0 ,width =120 ,stretch =NO )#line:398
    OO0OOOOO00OOO0O0O =Scrollbar (O00OO000OOO0OOOOO ,orient ="vertical")#line:400
    OO0OOOOO00OOO0O0O .pack (side =RIGHT ,fill =Y )#line:401
    OO0OOOOO00OOO0O0O .config (command =OO0O0OOOOO0O0O000 .yview )#line:402
    OO0O0OOOOO0O0O000 .config (yscrollcommand =OO0OOOOO00OOO0O0O .set )#line:403
    OO0OO00O0OO00OOOO =Scrollbar (O00OO000OOO0OOOOO ,orient ="horizontal")#line:405
    OO0OO00O0OO00OOOO .pack (side =BOTTOM ,fill =X )#line:406
    OO0OO00O0OO00OOOO .config (command =OO0O0OOOOO0O0O000 .xview )#line:407
    OO0O0OOOOO0O0O000 .config (yscrollcommand =OO0OOOOO00OOO0O0O .set )#line:408
    def O0O0000000OO0OOO0 (O0OO0O00O00OO0O0O ,OOOOOOOO0OO0O00O0 ,O0OOO0OOO000O0000 ):#line:410
        for OO0000O0O000O0O0O in OO0O0OOOOO0O0O000 .selection ():#line:413
            O0OO000O0OOOOOOOO =OO0O0OOOOO0O0O000 .item (OO0000O0O000O0O0O ,"values")#line:414
            O0O0OOOOOO0O0O0O0 =dict (zip (OOOOOOOO0OO0O00O0 ,O0OO000O0OOOOOOOO ))#line:415
        if "该分类下各项计数"in OOOOOOOO0OO0O00O0 :#line:417
            OO0O0OOOO0000O00O =OOOOO0O00000O0000 .copy ()#line:418
            OO0O0OOOO0000O00O ["关键字查找列"]=""#line:419
            for OO000O00O00000O00 in TOOLS_get_list (O0O0OOOOOO0O0O0O0 ["查找位置"]):#line:420
                OO0O0OOOO0000O00O ["关键字查找列"]=OO0O0OOOO0000O00O ["关键字查找列"]+OO0O0OOOO0000O00O [OO000O00O00000O00 ].astype ("str")#line:421
            O00OO00OOOO0OOOOO =OO0O0OOOO0000O00O .loc [OO0O0OOOO0000O00O ["关键字查找列"].str .contains (O0O0OOOOOO0O0O0O0 ["关键字标记"],na =False )].copy ()#line:422
            O00OO00OOOO0OOOOO =O00OO00OOOO0OOOOO .loc [~O00OO00OOOO0OOOOO ["关键字查找列"].str .contains (O0O0OOOOOO0O0O0O0 ["排除值"],na =False )].copy ()#line:423
            Tread_TOOLS_tree_Level_2 (O00OO00OOOO0OOOOO ,0 ,O00OO00OOOO0OOOOO )#line:429
            return 0 #line:430
        if "报告编码"in OOOOOOOO0OO0O00O0 :#line:432
            O00OOO0OOO00O00O0 =Toplevel ()#line:433
            OO00O00OO00OO000O =O00OOO0OOO00O00O0 .winfo_screenwidth ()#line:434
            OOO00OO000OO00O0O =O00OOO0OOO00O00O0 .winfo_screenheight ()#line:436
            OOO0O0O0OOO00O00O =800 #line:438
            OOO0O0O000O0O0O0O =600 #line:439
            OO000O00O00000O00 =(OO00O00OO00OO000O -OOO0O0O0OOO00O00O )/2 #line:441
            O00000O0O0O0O0OO0 =(OOO00OO000OO00O0O -OOO0O0O000O0O0O0O )/2 #line:442
            O00OOO0OOO00O00O0 .geometry ("%dx%d+%d+%d"%(OOO0O0O0OOO00O00O ,OOO0O0O000O0O0O0O ,OO000O00O00000O00 ,O00000O0O0O0O0OO0 ))#line:443
            O00O0O0O00O000OOO =ScrolledText (O00OOO0OOO00O00O0 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:447
            O00O0O0O00O000OOO .pack (padx =10 ,pady =10 )#line:448
            def OOOOOO00O0000O0O0 (event =None ):#line:449
                O00O0O0O00O000OOO .event_generate ('<<Copy>>')#line:450
            def OO0O000O00O0O0O00 (O000OO0OO00O00O00 ,O00000OOO0OOOOO0O ):#line:451
                O0OOO000O00OOO000 =open (O00000OOO0OOOOO0O ,"w",encoding ='utf-8')#line:452
                O0OOO000O00OOO000 .write (O000OO0OO00O00O00 )#line:453
                O0OOO000O00OOO000 .flush ()#line:455
                showinfo (title ="提示信息",message ="保存成功。")#line:456
            OO000OO0OOO0OO000 =Menu (O00O0O0O00O000OOO ,tearoff =False ,)#line:458
            OO000OO0OOO0OO000 .add_command (label ="复制",command =OOOOOO00O0000O0O0 )#line:459
            OO000OO0OOO0OO000 .add_command (label ="导出",command =lambda :thread_it (OO0O000O00O0O0O00 ,O00O0O0O00O000OOO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =O0O0OOOOOO0O0O0O0 ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:460
            def OO00O00O000OO0OO0 (O0OO0OO0000OOOOOO ):#line:462
                OO000OO0OOO0OO000 .post (O0OO0OO0000OOOOOO .x_root ,O0OO0OO0000OOOOOO .y_root )#line:463
            O00O0O0O00O000OOO .bind ("<Button-3>",OO00O00O000OO0OO0 )#line:464
            O00OOO0OOO00O00O0 .title (O0O0OOOOOO0O0O0O0 ["报告编码"])#line:466
            for O0OOO0OO0OO000000 in range (len (OOOOOOOO0OO0O00O0 )):#line:467
                O00O0O0O00O000OOO .insert (END ,OOOOOOOO0OO0O00O0 [O0OOO0OO0OO000000 ])#line:469
                O00O0O0O00O000OOO .insert (END ,"：")#line:470
                O00O0O0O00O000OOO .insert (END ,O0O0OOOOOO0O0O0O0 [OOOOOOOO0OO0O00O0 [O0OOO0OO0OO000000 ]])#line:471
                O00O0O0O00O000OOO .insert (END ,"\n")#line:472
            O00O0O0O00O000OOO .config (state =DISABLED )#line:473
            return 0 #line:474
        O00000O0O0O0O0OO0 =O0OO000O0OOOOOOOO [1 :-1 ]#line:477
        OO000O00O00000O00 =O0OOO0OOO000O0000 .columns .tolist ()#line:479
        OO000O00O00000O00 =OO000O00O00000O00 [1 :-1 ]#line:480
        O0O0O000O000O0OO0 ={'关键词':OO000O00O00000O00 ,'数量':O00000O0O0O0O0OO0 }#line:482
        O0O0O000O000O0OO0 =pd .DataFrame .from_dict (O0O0O000O000O0OO0 )#line:483
        O0O0O000O000O0OO0 ["数量"]=O0O0O000O000O0OO0 ["数量"].astype (float )#line:484
        Tread_TOOLS_draw (O0O0O000O000O0OO0 ,"帕累托图",'关键词','数量',"帕累托图")#line:485
        return 0 #line:486
    OO0O0OOOOO0O0O000 .bind ("<Double-1>",lambda OO0OOO000O0OOOOOO :O0O0000000OO0OOO0 (OO0OOO000O0OOOOOO ,O0OOOO00O00OO0OOO ,OO0000OO0OOO00000 ),)#line:494
    OO0O0OOOOO0O0O000 .pack ()#line:495
class Tread_TOOLS_Countall ():#line:497
    ""#line:498
    def __init__ (OO0000000OO0OO00O ,OO0O0O0O0000O000O ):#line:499
        ""#line:500
        OO0000000OO0OO00O .df =OO0O0O0O0000O000O #line:501
    def df_psur (OO00000O0OO000O00 ,OOO0O000OO000O0O0 ,*O0OO0OOO0O00OO00O ):#line:503
        ""#line:504
        global TT_biaozhun #line:505
        O0000O00OO0000000 =OO00000O0OO000O00 .df .copy ()#line:506
        OO0O00000OOOOO00O =len (O0000O00OO0000000 .drop_duplicates ("报告编码"))#line:508
        OO000OO0OO00OOO00 =OOO0O000OO000O0O0 .copy ()#line:511
        OOO000OO0OO00O0O0 =TT_biaozhun ["设置"]#line:514
        if OOO000OO0OO00O0O0 .loc [1 ,"值"]:#line:515
            OOOO000O0O0000O0O =OOO000OO0OO00O0O0 .loc [1 ,"值"]#line:516
        else :#line:517
            OOOO000O0O0000O0O ="透视列"#line:518
            O0000O00OO0000000 [OOOO000O0O0000O0O ]="未正确设置"#line:519
        O0OOOO00OO000OO0O =""#line:521
        OO000O0O00OO000O0 ="-其他关键字-"#line:522
        for OO00OO0OO000OO00O ,O00OOOOO0OOOO000O in OO000OO0OO00OOO00 .iterrows ():#line:523
            OO000O0O00OO000O0 =OO000O0O00OO000O0 +"|"+str (O00OOOOO0OOOO000O ["值"])#line:524
            O00OO0000O0O000O0 =O00OOOOO0OOOO000O #line:525
        O00OO0000O0O000O0 [3 ]=OO000O0O00OO000O0 #line:526
        O00OO0000O0O000O0 [2 ]="-其他关键字-|"#line:527
        OO000OO0OO00OOO00 .loc [len (OO000OO0OO00OOO00 )]=O00OO0000O0O000O0 #line:528
        OO000OO0OO00OOO00 =OO000OO0OO00OOO00 .reset_index (drop =True )#line:529
        O0000O00OO0000000 ["关键字查找列"]=""#line:533
        for OO0000000000OO0O0 in TOOLS_get_list (OO000OO0OO00OOO00 .loc [0 ,"查找位置"]):#line:534
            O0000O00OO0000000 ["关键字查找列"]=O0000O00OO0000000 ["关键字查找列"]+O0000O00OO0000000 [OO0000000000OO0O0 ].astype ("str")#line:535
        O0000OOO00000O00O =[]#line:538
        for OO00OO0OO000OO00O ,O00OOOOO0OOOO000O in OO000OO0OO00OOO00 .iterrows ():#line:539
            OO0000OOO0O000O0O =O00OOOOO0OOOO000O ["值"]#line:540
            OO000O0OO0O0O00OO =O0000O00OO0000000 .loc [O0000O00OO0000000 ["关键字查找列"].str .contains (OO0000OOO0O000O0O ,na =False )].copy ()#line:541
            if str (O00OOOOO0OOOO000O ["排除值"])!="nan":#line:542
                OO000O0OO0O0O00OO =OO000O0OO0O0O00OO .loc [~OO000O0OO0O0O00OO ["关键字查找列"].str .contains (str (O00OOOOO0OOOO000O ["排除值"]),na =False )].copy ()#line:543
            OO000O0OO0O0O00OO ["关键字标记"]=str (OO0000OOO0O000O0O )#line:545
            OO000O0OO0O0O00OO ["关键字计数"]=1 #line:546
            if len (OO000O0OO0O0O00OO )>0 :#line:548
                OOO00000O00O0000O =pd .pivot_table (OO000O0OO0O0O00OO .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OOOO000O0O0000O0O ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:558
                OOO00000O00O0000O =OOO00000O00O0000O [:-1 ]#line:559
                OOO00000O00O0000O .columns =OOO00000O00O0000O .columns .droplevel (0 )#line:560
                OOO00000O00O0000O =OOO00000O00O0000O .reset_index ()#line:561
                if len (OOO00000O00O0000O )>0 :#line:564
                    OOOOO00000O000O0O =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",OO000O0OO0O0O00OO ,1000 ))).replace ("Counter({","{")#line:565
                    OOOOO00000O000O0O =OOOOO00000O000O0O .replace ("})","}")#line:566
                    OOOOO00000O000O0O =ast .literal_eval (OOOOO00000O000O0O )#line:567
                    OOO00000O00O0000O .loc [0 ,"事件分类"]=str (TOOLS_get_list (OOO00000O00O0000O .loc [0 ,"关键字标记"])[0 ])#line:569
                    OOO00000O00O0000O .loc [0 ,"该分类下各项计数"]=str ({O0O0O0O000O0000OO :OO00OO0O0000OO0OO for O0O0O0O000O0000OO ,OO00OO0O0000OO0OO in OOOOO00000O000O0O .items ()if STAT_judge_x (str (O0O0O0O000O0000OO ),TOOLS_get_list (OO0000OOO0O000O0O ))==1 })#line:570
                    OOO00000O00O0000O .loc [0 ,"其他分类各项计数"]=str ({O0O000000O0000OO0 :OO0O0000O0OOOOO0O for O0O000000O0000OO0 ,OO0O0000O0OOOOO0O in OOOOO00000O000O0O .items ()if STAT_judge_x (str (O0O000000O0000OO0 ),TOOLS_get_list (OO0000OOO0O000O0O ))!=1 })#line:571
                    OOO00000O00O0000O ["查找位置"]=O00OOOOO0OOOO000O ["查找位置"]#line:572
                    O0000OOO00000O00O .append (OOO00000O00O0000O )#line:575
        O0OOOO00OO000OO0O =pd .concat (O0000OOO00000O00O )#line:576
        O0OOOO00OO000OO0O =O0OOOO00OO000OO0O .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:581
        O0OOOO00OO000OO0O =O0OOOO00OO000OO0O .reset_index ()#line:582
        O0OOOO00OO000OO0O ["All占比"]=round (O0OOOO00OO000OO0O ["All"]/OO0O00000OOOOO00O *100 ,2 )#line:584
        O0OOOO00OO000OO0O =O0OOOO00OO000OO0O .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:585
        for OO0O0OO0OOOO000O0 ,O00OOO0O0OOO0OO0O in OO000OO0OO00OOO00 .iterrows ():#line:588
            O0OOOO00OO000OO0O .loc [(O0OOOO00OO000OO0O ["关键字标记"].astype (str )==str (O00OOO0O0OOO0OO0O ["值"])),"排除值"]=O00OOO0O0OOO0OO0O ["排除值"]#line:589
            O0OOOO00OO000OO0O .loc [(O0OOOO00OO000OO0O ["关键字标记"].astype (str )==str (O00OOO0O0OOO0OO0O ["值"])),"查找位置"]=O00OOO0O0OOO0OO0O ["查找位置"]#line:590
        O0OOOO00OO000OO0O ["排除值"]=O0OOOO00OO000OO0O ["排除值"].fillna ("-没有排除值-")#line:592
        O0OOOO00OO000OO0O ["报表类型"]="PSUR"#line:595
        del O0OOOO00OO000OO0O ["index"]#line:596
        try :#line:597
            del O0OOOO00OO000OO0O ["未正确设置"]#line:598
        except :#line:599
            pass #line:600
        return O0OOOO00OO000OO0O #line:601
    def df_find_all_keword_risk (OO00OOO0OOO00O000 ,O0OO0O0O0O0O00OOO ,*OOO00O000000O0OO0 ):#line:604
        ""#line:605
        global TT_biaozhun #line:606
        O0OO00OOO00OO00OO =OO00OOO0OOO00O000 .df .copy ()#line:608
        O0O00OOO0OO0OO00O =time .time ()#line:609
        O0OO0000000OOO0O0 =TT_biaozhun ["关键字表"].copy ()#line:611
        O000OOO0O0OOOO00O ="作用对象"#line:613
        O0OO00O0O0OOOO000 ="报告编码"#line:615
        OO000000OOOO0000O =O0OO00OOO00OO00OO .groupby ([O000OOO0O0OOOO00O ]).agg (总数量 =(O0OO00O0O0OOOO000 ,"nunique"),).reset_index ()#line:618
        O0000O0OO0O0OOO0O =[O000OOO0O0OOOO00O ,O0OO0O0O0O0O00OOO ]#line:620
        O0O000OOOOOO000OO =O0OO00OOO00OO00OO .groupby (O0000O0OO0O0OOO0O ).agg (该元素总数量 =(O000OOO0O0OOOO00O ,"count"),).reset_index ()#line:624
        OO00O0OO0O0000O00 =[]#line:626
        O0OOO0OO0OOOO00OO =0 #line:630
        OO0OO00O00000000O =int (len (OO000000OOOO0000O ))#line:631
        for OOOO000OOO000OOOO ,OOOOOO0OOO0OOO0OO in zip (OO000000OOOO0000O [O000OOO0O0OOOO00O ].values ,OO000000OOOO0000O ["总数量"].values ):#line:632
            O0OOO0OO0OOOO00OO +=1 #line:633
            O0OO00000OO00O000 =O0OO00OOO00OO00OO [(O0OO00OOO00OO00OO [O000OOO0O0OOOO00O ]==OOOO000OOO000OOOO )].copy ()#line:634
            for OO0OOOOOOO0OOOOO0 ,O0O0OO00OO0OOOO0O ,O0OO0000000O000O0 in zip (O0OO0000000OOO0O0 ["值"].values ,O0OO0000000OOO0O0 ["查找位置"].values ,O0OO0000000OOO0O0 ["排除值"].values ):#line:636
                    OO0OO0OO0000OO00O =O0OO00000OO00O000 .copy ()#line:637
                    O0O0O0OOOO00O00O0 =TOOLS_get_list (OO0OOOOOOO0OOOOO0 )[0 ]#line:638
                    OO0OO0OO0000OO00O ["关键字查找列"]=""#line:640
                    for O000OOOO000O000O0 in TOOLS_get_list (O0O0OO00OO0OOOO0O ):#line:641
                        OO0OO0OO0000OO00O ["关键字查找列"]=OO0OO0OO0000OO00O ["关键字查找列"]+OO0OO0OO0000OO00O [O000OOOO000O000O0 ].astype ("str")#line:642
                    OO0OO0OO0000OO00O .loc [OO0OO0OO0000OO00O ["关键字查找列"].str .contains (OO0OOOOOOO0OOOOO0 ,na =False ),"关键字"]=O0O0O0OOOO00O00O0 #line:644
                    if str (O0OO0000000O000O0 )!="nan":#line:649
                        OO0OO0OO0000OO00O =OO0OO0OO0000OO00O .loc [~OO0OO0OO0000OO00O ["关键字查找列"].str .contains (O0OO0000000O000O0 ,na =False )].copy ()#line:650
                    if (len (OO0OO0OO0000OO00O ))<1 :#line:652
                        continue #line:654
                    OOO00O0OOO0O00OO0 =STAT_find_keyword_risk (OO0OO0OO0000OO00O ,[O000OOO0O0OOOO00O ,"关键字"],"关键字",O0OO0O0O0O0O00OOO ,int (OOOOOO0OOO0OOO0OO ))#line:656
                    if len (OOO00O0OOO0O00OO0 )>0 :#line:657
                        OOO00O0OOO0O00OO0 ["关键字组合"]=OO0OOOOOOO0OOOOO0 #line:658
                        OOO00O0OOO0O00OO0 ["排除值"]=O0OO0000000O000O0 #line:659
                        OOO00O0OOO0O00OO0 ["关键字查找列"]=O0O0OO00OO0OOOO0O #line:660
                        OO00O0OO0O0000O00 .append (OOO00O0OOO0O00OO0 )#line:661
        if len (OO00O0OO0O0000O00 )<1 :#line:664
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:665
            return 0 #line:666
        O0O00OOOO00O00O0O =pd .concat (OO00O0OO0O0000O00 )#line:667
        O0O00OOOO00O00O0O =pd .merge (O0O00OOOO00O00O0O ,O0O000OOOOOO000OO ,on =O0000O0OO0O0OOO0O ,how ="left")#line:670
        O0O00OOOO00O00O0O ["关键字数量比例"]=round (O0O00OOOO00O00O0O ["计数"]/O0O00OOOO00O00O0O ["该元素总数量"],2 )#line:671
        O0O00OOOO00O00O0O =O0O00OOOO00O00O0O .reset_index (drop =True )#line:673
        if len (O0O00OOOO00O00O0O )>0 :#line:676
            O0O00OOOO00O00O0O ["风险评分"]=0 #line:677
            O0O00OOOO00O00O0O ["报表类型"]="keyword_findrisk"+O0OO0O0O0O0O00OOO #line:678
            O0O00OOOO00O00O0O .loc [(O0O00OOOO00O00O0O ["计数"]>=3 ),"风险评分"]=O0O00OOOO00O00O0O ["风险评分"]+3 #line:679
            O0O00OOOO00O00O0O .loc [(O0O00OOOO00O00O0O ["计数"]>=(O0O00OOOO00O00O0O ["数量均值"]+O0O00OOOO00O00O0O ["数量标准差"])),"风险评分"]=O0O00OOOO00O00O0O ["风险评分"]+1 #line:680
            O0O00OOOO00O00O0O .loc [(O0O00OOOO00O00O0O ["计数"]>=O0O00OOOO00O00O0O ["数量CI"]),"风险评分"]=O0O00OOOO00O00O0O ["风险评分"]+1 #line:681
            O0O00OOOO00O00O0O .loc [(O0O00OOOO00O00O0O ["关键字数量比例"]>0.5 )&(O0O00OOOO00O00O0O ["计数"]>=3 ),"风险评分"]=O0O00OOOO00O00O0O ["风险评分"]+1 #line:682
            O0O00OOOO00O00O0O =O0O00OOOO00O00O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:684
        OOO000OO00000OOO0 =O0O00OOOO00O00O0O .columns .to_list ()#line:694
        O000OO0OOOOO000O0 =OOO000OO00000OOO0 [OOO000OO00000OOO0 .index ("关键字")+1 ]#line:695
        OOOOO0O0OOOOO0OO0 =pd .pivot_table (O0O00OOOO00O00O0O ,index =O000OO0OOOOO000O0 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:706
        OOOOO0O0OOOOO0OO0 .columns =OOOOO0O0OOOOO0OO0 .columns .droplevel (0 )#line:707
        OOOOO0O0OOOOO0OO0 =pd .merge (OOOOO0O0OOOOO0OO0 ,O0O00OOOO00O00O0O [[O000OO0OOOOO000O0 ,"该元素总数量"]].drop_duplicates (O000OO0OOOOO000O0 ),on =[O000OO0OOOOO000O0 ],how ="left")#line:710
        del OOOOO0O0OOOOO0OO0 ["All"]#line:712
        OOOOO0O0OOOOO0OO0 .iloc [-1 ,-1 ]=OOOOO0O0OOOOO0OO0 ["该元素总数量"].sum (axis =0 )#line:713
        print ("耗时：",(time .time ()-O0O00OOO0OO0OO00O ))#line:715
        return OOOOO0O0OOOOO0OO0 #line:718
def Tread_TOOLS_bar (OOO0O0000OOOOOOOO ):#line:726
         ""#line:727
         O0OO000000OO00000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:728
         O0000OOOO0O000OO0 =[pd .read_excel (O0O00O0OO0OOO00OO ,header =0 ,sheet_name =0 )for O0O00O0OO0OOO00OO in O0OO000000OO00000 ]#line:729
         O00000OOO0O0O0OO0 =pd .concat (O0000OOOO0O000OO0 ,ignore_index =True )#line:730
         OOO000OOO0OO0O00O =pd .pivot_table (O00000OOO0O0O0OO0 ,index ="对象",columns ="关键词",values =OOO0O0000OOOOOOOO ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:740
         del OOO000OOO0OO0O00O ["All"]#line:742
         OOO000OOO0OO0O00O =OOO000OOO0OO0O00O [:-1 ]#line:743
         Tread_TOOLS_tree_Level_2 (OOO000OOO0OO0O00O ,0 ,0 )#line:745
def Tread_TOOLS_analysis (O0OOO00O0O0O00OOO ):#line:750
    ""#line:751
    import datetime #line:752
    global TT_ori #line:753
    global TT_biaozhun #line:754
    if len (TT_ori )==0 :#line:756
       showinfo (title ="提示",message ="您尚未导入原始数据。")#line:757
       return 0 #line:758
    if len (TT_biaozhun )==0 :#line:759
       showinfo (title ="提示",message ="您尚未导入规则。")#line:760
       return 0 #line:761
    O0O000O0O000O00O0 =TT_biaozhun ["设置"]#line:763
    TT_ori ["作用对象"]=""#line:764
    for OO0000O00O0OO00OO in TOOLS_get_list (O0O000O0O000O00O0 .loc [0 ,"值"]):#line:765
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [OO0000O00O0OO00OO ].fillna ("未填写").astype ("str")#line:766
    OO00OO0OO0OO0000O =Toplevel ()#line:769
    OO00OO0OO0OO0000O .title ("单品分析")#line:770
    OO00O00OO000O0O00 =OO00OO0OO0OO0000O .winfo_screenwidth ()#line:771
    O00OOOOOOOO0OOO0O =OO00OO0OO0OO0000O .winfo_screenheight ()#line:773
    OOO0O0000O0OOOOO0 =580 #line:775
    OOOO0O00OO0O00OOO =80 #line:776
    O0OOOO0O000000O00 =(OO00O00OO000O0O00 -OOO0O0000O0OOOOO0 )/1.7 #line:778
    O00OO0OOO0O0O0OO0 =(O00OOOOOOOO0OOO0O -OOOO0O00OO0O00OOO )/2 #line:779
    OO00OO0OO0OO0000O .geometry ("%dx%d+%d+%d"%(OOO0O0000O0OOOOO0 ,OOOO0O00OO0O00OOO ,O0OOOO0O000000O00 ,O00OO0OOO0O0O0OO0 ))#line:780
    O0OOO000OO00O0OO0 =Label (OO00OO0OO0OO0000O ,text ="作用对象：")#line:783
    O0OOO000OO00O0OO0 .grid (row =1 ,column =0 ,sticky ="w")#line:784
    OO000000O0OOO0O0O =StringVar ()#line:785
    O000OOOO0O000OO00 =ttk .Combobox (OO00OO0OO0OO0000O ,width =25 ,height =10 ,state ="readonly",textvariable =OO000000O0OOO0O0O )#line:788
    O000OOOO0O000OO00 ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:789
    O000OOOO0O000OO00 .current (0 )#line:790
    O000OOOO0O000OO00 .grid (row =1 ,column =1 )#line:791
    O0OO00OOOOO0OOO00 =Label (OO00OO0OO0OO0000O ,text ="分析对象：")#line:793
    O0OO00OOOOO0OOO00 .grid (row =1 ,column =2 ,sticky ="w")#line:794
    O0OO0OOO0OO000000 =StringVar ()#line:797
    OOOOOOO000O0OO0O0 =ttk .Combobox (OO00OO0OO0OO0000O ,width =15 ,height =10 ,state ="readonly",textvariable =O0OO0OOO0OO000000 )#line:800
    OOOOOOO000O0OO0O0 ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:801
    OOOOOOO000O0OO0O0 .current (0 )#line:803
    OOOOOOO000O0OO0O0 .grid (row =1 ,column =3 )#line:804
    O0OOO0O0O00OO000O =Label (OO00OO0OO0OO0000O ,text ="事件发生起止时间：")#line:809
    O0OOO0O0O00OO000O .grid (row =2 ,column =0 ,sticky ="w")#line:810
    OO000OOO0000O0O0O =Entry (OO00OO0OO0OO0000O ,width =10 )#line:812
    OO000OOO0000O0O0O .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:813
    OO000OOO0000O0O0O .grid (row =2 ,column =1 ,sticky ="w")#line:814
    OO0OO0OO0O0O00OOO =Entry (OO00OO0OO0OO0000O ,width =10 )#line:816
    OO0OO0OO0O0O00OOO .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:817
    OO0OO0OO0O0O00OOO .grid (row =2 ,column =2 ,sticky ="w")#line:818
    O0O00OO0OOOOO0O00 =Button (OO00OO0OO0OO0000O ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OOOO0O000OO00 .get (),OOOOOOO000O0OO0O0 .get (),OO000OOO0000O0O0O .get (),OO0OO0OO0O0O00OOO .get (),1 ))#line:829
    O0O00OO0OOOOO0O00 .grid (row =3 ,column =3 ,sticky ="w")#line:830
    O0O00OO0OOOOO0O00 =Button (OO00OO0OO0OO0000O ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OOOO0O000OO00 .get (),OOOOOOO000O0OO0O0 .get (),OO000OOO0000O0O0O .get (),OO0OO0OO0O0O00OOO .get (),0 ))#line:840
    O0O00OO0OOOOO0O00 .grid (row =3 ,column =2 ,sticky ="w")#line:841
    O0O00OO0OOOOO0O00 =Button (OO00OO0OO0OO0000O ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OOOO0O000OO00 .get (),OOOOOOO000O0OO0O0 .get (),OO000OOO0000O0O0O .get (),OO0OO0OO0O0O00OOO .get (),2 ))#line:851
    O0O00OO0OOOOO0O00 .grid (row =3 ,column =1 ,sticky ="w")#line:852
def Tread_TOOLS_doing (O0O0OO00O0OO00OOO ,OO0O0O00OOO000O0O ,O0OO0O00O00OOO0OO ,OO0000O00O0OOO00O ,O0000OO0O0000O0OO ,O0000OOOO0O0OO0OO ):#line:854
    ""#line:855
    global TT_biaozhun #line:856
    O0O0OO00O0OO00OOO =O0O0OO00O0OO00OOO [(O0O0OO00O0OO00OOO ["作用对象"]==OO0O0O00OOO000O0O )].copy ()#line:857
    OO0000O00O0OOO00O =pd .to_datetime (OO0000O00O0OOO00O )#line:859
    O0000OO0O0000O0OO =pd .to_datetime (O0000OO0O0000O0OO )#line:860
    O0O0OO00O0OO00OOO =O0O0OO00O0OO00OOO [((O0O0OO00O0OO00OOO ["事件发生日期"]>=OO0000O00O0OOO00O )&(O0O0OO00O0OO00OOO ["事件发生日期"]<=O0000OO0O0000O0OO ))]#line:861
    text .insert (END ,"\n数据数量："+str (len (O0O0OO00O0OO00OOO )))#line:862
    text .see (END )#line:863
    if O0000OOOO0O0OO0OO ==0 :#line:865
        Tread_TOOLS_check (O0O0OO00O0OO00OOO ,TT_biaozhun ["关键字表"],0 )#line:866
        return 0 #line:867
    if O0000OOOO0O0OO0OO ==1 :#line:868
        Tread_TOOLS_tree_Level_2 (O0O0OO00O0OO00OOO ,1 ,O0O0OO00O0OO00OOO )#line:869
        return 0 #line:870
    if len (O0O0OO00O0OO00OOO )<1 :#line:871
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:872
        return 0 #line:873
    Tread_TOOLS_check (O0O0OO00O0OO00OOO ,TT_biaozhun ["关键字表"],1 )#line:874
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (O0O0OO00O0OO00OOO ).df_find_all_keword_risk (O0OO0O00O00OOO0OO ),1 ,0 ,O0OO0O00O00OOO0OO )#line:877
def STAT_countx (OO000O0OOOO00O0OO ):#line:887
    ""#line:888
    return OO000O0OOOO00O0OO .value_counts ().to_dict ()#line:889
def STAT_countpx (OOOOOOOO0O0O0000O ,O00OOO000O00OOOOO ):#line:891
    ""#line:892
    return len (OOOOOOOO0O0O0000O [(OOOOOOOO0O0O0000O ==O00OOO000O00OOOOO )])#line:893
def STAT_countnpx (O0OOO00OOOO00000O ,O000O000O0OOOO0O0 ):#line:895
    ""#line:896
    return len (O0OOO00OOOO00000O [(O0OOO00OOOO00000O not in O000O000O0OOOO0O0 )])#line:897
def STAT_get_max (OOOO0000OOO0OO0O0 ):#line:899
    ""#line:900
    return OOOO0000OOO0OO0O0 .value_counts ().max ()#line:901
def STAT_get_mean (O0OO00OO000O00OOO ):#line:903
    ""#line:904
    return round (O0OO00OO000O00OOO .value_counts ().mean (),2 )#line:905
def STAT_get_std (OOO0O0O00OO0O0OOO ):#line:907
    ""#line:908
    return round (OOO0O0O00OO0O0OOO .value_counts ().std (ddof =1 ),2 )#line:909
def STAT_get_95ci (OOO00000OOO0O0OOO ):#line:911
    ""#line:912
    return round (np .percentile (OOO00000OOO0O0OOO .value_counts (),97.5 ),2 )#line:913
def STAT_get_mean_std_ci (O0OOO00O00O00O00O ,OO00000O0O000OO0O ):#line:915
    ""#line:916
    warnings .filterwarnings ("ignore")#line:917
    OOO0O0OO00OOO0OO0 =TOOLS_strdict_to_pd (str (O0OOO00O00O00O00O ))["content"].values /OO00000O0O000OO0O #line:918
    O00O0O0O00000OO0O =round (OOO0O0OO00OOO0OO0 .mean (),2 )#line:919
    OOO0OO0000O0OO000 =round (OOO0O0OO00OOO0OO0 .std (ddof =1 ),2 )#line:920
    O0000O00OOO00OO00 =round (np .percentile (OOO0O0OO00OOO0OO0 ,97.5 ),2 )#line:921
    return pd .Series ((O00O0O0O00000OO0O ,OOO0OO0000O0OO000 ,O0000O00OOO00OO00 ))#line:922
def STAT_findx_value (O0O00000OO00OO0O0 ,OO0OOO0OOO0OOOO00 ):#line:924
    ""#line:925
    warnings .filterwarnings ("ignore")#line:926
    O0OOO0OO0O0O0O0OO =TOOLS_strdict_to_pd (str (O0O00000OO00OO0O0 ))#line:927
    OOOO0O0OOOOOO00OO =O0OOO0OO0O0O0O0OO .where (O0OOO0OO0O0O0O0OO ["index"]==str (OO0OOO0OOO0OOOO00 ))#line:929
    print (OOOO0O0OOOOOO00OO )#line:930
    return OOOO0O0OOOOOO00OO #line:931
def STAT_judge_x (O0OOOOO0O000OOO00 ,O0OOO00O0OOO0OO00 ):#line:933
    ""#line:934
    for O000OO000O0O00O0O in O0OOO00O0OOO0OO00 :#line:935
        if O0OOOOO0O000OOO00 .find (O000OO000O0O00O0O )>-1 :#line:936
            return 1 #line:937
def STAT_basic_risk (OO0O00OOOOO00OO0O ,OOOOOOOOOOO0OO0OO ,OOOO0000000OOOOO0 ,O0OO0O0OOOO0O0OO0 ,OO0O000O0OO0O0O00 ):#line:940
    ""#line:941
    OO0O00OOOOO00OO0O ["风险评分"]=0 #line:942
    OO0O00OOOOO00OO0O .loc [((OO0O00OOOOO00OO0O [OOOOOOOOOOO0OO0OO ]>=3 )&(OO0O00OOOOO00OO0O [OOOO0000000OOOOO0 ]>=1 ))|(OO0O00OOOOO00OO0O [OOOOOOOOOOO0OO0OO ]>=5 ),"风险评分"]=OO0O00OOOOO00OO0O ["风险评分"]+5 #line:943
    OO0O00OOOOO00OO0O .loc [(OO0O00OOOOO00OO0O [OOOO0000000OOOOO0 ]>=3 ),"风险评分"]=OO0O00OOOOO00OO0O ["风险评分"]+1 #line:944
    OO0O00OOOOO00OO0O .loc [(OO0O00OOOOO00OO0O [O0OO0O0OOOO0O0OO0 ]>=1 ),"风险评分"]=OO0O00OOOOO00OO0O ["风险评分"]+10 #line:945
    OO0O00OOOOO00OO0O ["风险评分"]=OO0O00OOOOO00OO0O ["风险评分"]+OO0O00OOOOO00OO0O [OO0O000O0OO0O0O00 ]/100 #line:946
    return OO0O00OOOOO00OO0O #line:947
def STAT_find_keyword_risk (O0000000O00OO00O0 ,OO00O0OO0000O0000 ,OOOOO0000OO0OOOOO ,OOOO0OO0OO0O000O0 ,OOOOO00000OOOOOO0 ):#line:951
        ""#line:952
        OOOOOOO0OO000OOO0 =O0000000O00OO00O0 .groupby (OO00O0OO0000O0000 ).agg (证号关键字总数量 =(OOOOO0000OO0OOOOO ,"count"),包含元素个数 =(OOOO0OO0OO0O000O0 ,"nunique"),包含元素 =(OOOO0OO0OO0O000O0 ,STAT_countx ),).reset_index ()#line:957
        O0O0OOO0O0000OO00 =OO00O0OO0000O0000 .copy ()#line:959
        O0O0OOO0O0000OO00 .append (OOOO0OO0OO0O000O0 )#line:960
        OOOO00000O000O00O =O0000000O00OO00O0 .groupby (O0O0OOO0O0000OO00 ).agg (计数 =(OOOO0OO0OO0O000O0 ,"count"),).reset_index ()#line:963
        OOOO00OO0O00OO0O0 =O0O0OOO0O0000OO00 .copy ()#line:966
        OOOO00OO0O00OO0O0 .remove ("关键字")#line:967
        OOO00O00OOO00OO00 =O0000000O00OO00O0 .groupby (OOOO00OO0O00OO0O0 ).agg (该元素总数 =(OOOO0OO0OO0O000O0 ,"count"),).reset_index ()#line:970
        OOOO00000O000O00O ["证号总数"]=OOOOO00000OOOOOO0 #line:972
        O000OO0OO0O0O0000 =pd .merge (OOOO00000O000O00O ,OOOOOOO0OO000OOO0 ,on =OO00O0OO0000O0000 ,how ="left")#line:973
        if len (O000OO0OO0O0O0000 )>0 :#line:975
            O000OO0OO0O0O0000 [['数量均值','数量标准差','数量CI']]=O000OO0OO0O0O0000 .包含元素 .apply (lambda OO0OOOOOO0O000000 :STAT_get_mean_std_ci (OO0OOOOOO0O000000 ,1 ))#line:976
        return O000OO0OO0O0O0000 #line:977
def STAT_find_risk (O0OOOOOOO00OO0OOO ,OOOOOOOOO0OOOO000 ,OOO0O0000OOOOOO0O ,O0OO0OOOO00O00OOO ):#line:983
        ""#line:984
        OO0O0OO000000O0O0 =O0OOOOOOO00OO0OOO .groupby (OOOOOOOOO0OOOO000 ).agg (证号总数量 =(OOO0O0000OOOOOO0O ,"count"),包含元素个数 =(O0OO0OOOO00O00OOO ,"nunique"),包含元素 =(O0OO0OOOO00O00OOO ,STAT_countx ),均值 =(O0OO0OOOO00O00OOO ,STAT_get_mean ),标准差 =(O0OO0OOOO00O00OOO ,STAT_get_std ),CI上限 =(O0OO0OOOO00O00OOO ,STAT_get_95ci ),).reset_index ()#line:992
        O0000OO00OOO0O0OO =OOOOOOOOO0OOOO000 .copy ()#line:994
        O0000OO00OOO0O0OO .append (O0OO0OOOO00O00OOO )#line:995
        O0OOOOOO000O00OOO =O0OOOOOOO00OO0OOO .groupby (O0000OO00OOO0O0OO ).agg (计数 =(O0OO0OOOO00O00OOO ,"count"),严重伤害数 =("伤害",lambda O00O00O0O0OOO000O :STAT_countpx (O00O00O0O0OOO000O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0000OOOO00OOO0O :STAT_countpx (OO0000OOOO00OOO0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:1002
        O00O00OOO0O00O000 =pd .merge (O0OOOOOO000O00OOO ,OO0O0OO000000O0O0 ,on =OOOOOOOOO0OOOO000 ,how ="left")#line:1004
        O00O00OOO0O00O000 ["风险评分"]=0 #line:1006
        O00O00OOO0O00O000 ["报表类型"]="dfx_findrisk"+O0OO0OOOO00O00OOO #line:1007
        O00O00OOO0O00O000 .loc [((O00O00OOO0O00O000 ["计数"]>=3 )&(O00O00OOO0O00O000 ["严重伤害数"]>=1 )|(O00O00OOO0O00O000 ["计数"]>=5 )),"风险评分"]=O00O00OOO0O00O000 ["风险评分"]+5 #line:1008
        O00O00OOO0O00O000 .loc [(O00O00OOO0O00O000 ["计数"]>=(O00O00OOO0O00O000 ["均值"]+O00O00OOO0O00O000 ["标准差"])),"风险评分"]=O00O00OOO0O00O000 ["风险评分"]+1 #line:1009
        O00O00OOO0O00O000 .loc [(O00O00OOO0O00O000 ["计数"]>=O00O00OOO0O00O000 ["CI上限"]),"风险评分"]=O00O00OOO0O00O000 ["风险评分"]+1 #line:1010
        O00O00OOO0O00O000 .loc [(O00O00OOO0O00O000 ["严重伤害数"]>=3 )&(O00O00OOO0O00O000 ["风险评分"]>=7 ),"风险评分"]=O00O00OOO0O00O000 ["风险评分"]+1 #line:1011
        O00O00OOO0O00O000 .loc [(O00O00OOO0O00O000 ["死亡数量"]>=1 ),"风险评分"]=O00O00OOO0O00O000 ["风险评分"]+10 #line:1012
        O00O00OOO0O00O000 ["风险评分"]=O00O00OOO0O00O000 ["风险评分"]+O00O00OOO0O00O000 ["单位个数"]/100 #line:1013
        O00O00OOO0O00O000 =O00O00OOO0O00O000 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1014
        return O00O00OOO0O00O000 #line:1016
def TOOLS_get_list (OOO00O0O0OOOO0O0O ):#line:1018
    ""#line:1019
    OOO00O0O0OOOO0O0O =str (OOO00O0O0OOOO0O0O )#line:1020
    OOOOO0O0O00O0000O =[]#line:1021
    OOOOO0O0O00O0000O .append (OOO00O0O0OOOO0O0O )#line:1022
    OOOOO0O0O00O0000O =",".join (OOOOO0O0O00O0000O )#line:1023
    OOOOO0O0O00O0000O =OOOOO0O0O00O0000O .split ("|")#line:1024
    O0000O0OO0OO0O000 =OOOOO0O0O00O0000O [:]#line:1025
    OOOOO0O0O00O0000O =list (set (OOOOO0O0O00O0000O ))#line:1026
    OOOOO0O0O00O0000O .sort (key =O0000O0OO0OO0O000 .index )#line:1027
    return OOOOO0O0O00O0000O #line:1028
def TOOLS_get_list0 (OOOO0OO000O0O0000 ,OO00OO0OOO0OO0O00 ,*OO00000OO000OOOOO ):#line:1030
    ""#line:1031
    OOOO0OO000O0O0000 =str (OOOO0OO000O0O0000 )#line:1032
    if pd .notnull (OOOO0OO000O0O0000 ):#line:1034
        try :#line:1035
            if "use("in str (OOOO0OO000O0O0000 ):#line:1036
                OO000O0OO000OOOO0 =OOOO0OO000O0O0000 #line:1037
                OO0OOOO0O0OOO0OO0 =re .compile (r"[(](.*?)[)]",re .S )#line:1038
                OO0O0O000OOOOOOO0 =re .findall (OO0OOOO0O0OOO0OO0 ,OO000O0OO000OOOO0 )#line:1039
                OOO00O0O000O00O00 =[]#line:1040
                if ").list"in OOOO0OO000O0O0000 :#line:1041
                    O0000OOO0OO0OOO00 ="配置表/"+str (OO0O0O000OOOOOOO0 [0 ])+".xls"#line:1042
                    OOOOOO0OO000O0O0O =pd .read_excel (O0000OOO0OO0OOO00 ,sheet_name =OO0O0O000OOOOOOO0 [0 ],header =0 ,index_col =0 ).reset_index ()#line:1045
                    OOOOOO0OO000O0O0O ["检索关键字"]=OOOOOO0OO000O0O0O ["检索关键字"].astype (str )#line:1046
                    OOO00O0O000O00O00 =OOOOOO0OO000O0O0O ["检索关键字"].tolist ()+OOO00O0O000O00O00 #line:1047
                if ").file"in OOOO0OO000O0O0000 :#line:1048
                    OOO00O0O000O00O00 =OO00OO0OOO0OO0O00 [OO0O0O000OOOOOOO0 [0 ]].astype (str ).tolist ()+OOO00O0O000O00O00 #line:1050
                try :#line:1053
                    if "报告类型-新的"in OO00OO0OOO0OO0O00 .columns :#line:1054
                        OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1055
                        OOO00O0O000O00O00 =OOO00O0O000O00O00 .split (";")#line:1056
                        OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1057
                        OOO00O0O000O00O00 =OOO00O0O000O00O00 .split ("；")#line:1058
                        OOO00O0O000O00O00 =[O0O0O000OO000OOO0 .replace ("（严重）","")for O0O0O000OO000OOO0 in OOO00O0O000O00O00 ]#line:1059
                        OOO00O0O000O00O00 =[OO0000OOO000OO000 .replace ("（一般）","")for OO0000OOO000OO000 in OOO00O0O000O00O00 ]#line:1060
                except :#line:1061
                    pass #line:1062
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1065
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split ("、")#line:1066
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1067
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split ("，")#line:1068
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1069
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split (",")#line:1070
                OO0OO000OO00O0OO0 =OOO00O0O000O00O00 [:]#line:1072
                try :#line:1073
                    if OO00000OO000OOOOO [0 ]==1000 :#line:1074
                      pass #line:1075
                except :#line:1076
                      OOO00O0O000O00O00 =list (set (OOO00O0O000O00O00 ))#line:1077
                OOO00O0O000O00O00 .sort (key =OO0OO000OO00O0OO0 .index )#line:1078
            else :#line:1080
                OOOO0OO000O0O0000 =str (OOOO0OO000O0O0000 )#line:1081
                OOO00O0O000O00O00 =[]#line:1082
                OOO00O0O000O00O00 .append (OOOO0OO000O0O0000 )#line:1083
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1084
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split ("、")#line:1085
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1086
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split ("，")#line:1087
                OOO00O0O000O00O00 =",".join (OOO00O0O000O00O00 )#line:1088
                OOO00O0O000O00O00 =OOO00O0O000O00O00 .split (",")#line:1089
                OO0OO000OO00O0OO0 =OOO00O0O000O00O00 [:]#line:1091
                try :#line:1092
                    if OO00000OO000OOOOO [0 ]==1000 :#line:1093
                      OOO00O0O000O00O00 =list (set (OOO00O0O000O00O00 ))#line:1094
                except :#line:1095
                      pass #line:1096
                OOO00O0O000O00O00 .sort (key =OO0OO000OO00O0OO0 .index )#line:1097
                OOO00O0O000O00O00 .sort (key =OO0OO000OO00O0OO0 .index )#line:1098
        except ValueError2 :#line:1100
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1101
            return False #line:1102
    return OOO00O0O000O00O00 #line:1104
def TOOLS_strdict_to_pd (O00O0O00OO000000O ):#line:1105
    ""#line:1106
    return pd .DataFrame .from_dict (eval (O00O0O00OO000000O ),orient ="index",columns =["content"]).reset_index ()#line:1107
def Tread_TOOLS_view_dict (OOOOOO0OO000OO00O ,O0O000O00O0OOO000 ):#line:1109
    ""#line:1110
    O0OOO0O0O0O00O00O =Toplevel ()#line:1111
    O0OOO0O0O0O00O00O .title ("查看数据")#line:1112
    O0OOO0O0O0O00O00O .geometry ("700x500")#line:1113
    O00O000OOO00O0O00 =Scrollbar (O0OOO0O0O0O00O00O )#line:1115
    O0O0O0O0O0O0O0000 =Text (O0OOO0O0O0O00O00O ,height =100 ,width =150 )#line:1116
    O00O000OOO00O0O00 .pack (side =RIGHT ,fill =Y )#line:1117
    O0O0O0O0O0O0O0000 .pack ()#line:1118
    O00O000OOO00O0O00 .config (command =O0O0O0O0O0O0O0000 .yview )#line:1119
    O0O0O0O0O0O0O0000 .config (yscrollcommand =O00O000OOO00O0O00 .set )#line:1120
    if O0O000O00O0OOO000 ==1 :#line:1121
        O0O0O0O0O0O0O0000 .insert (END ,OOOOOO0OO000OO00O )#line:1123
        O0O0O0O0O0O0O0000 .insert (END ,"\n\n")#line:1124
        return 0 #line:1125
    for OOO00O0OO000OO0OO in range (len (OOOOOO0OO000OO00O )):#line:1126
        O0O0O0O0O0O0O0000 .insert (END ,OOOOOO0OO000OO00O .iloc [OOO00O0OO000OO0OO ,0 ])#line:1127
        O0O0O0O0O0O0O0000 .insert (END ,":")#line:1128
        O0O0O0O0O0O0O0000 .insert (END ,OOOOOO0OO000OO00O .iloc [OOO00O0OO000OO0OO ,1 ])#line:1129
        O0O0O0O0O0O0O0000 .insert (END ,"\n\n")#line:1130
def Tread_TOOLS_fashenglv (OO000O000OO000OO0 ,OOOOOOOOOOOO0OOOO ):#line:1133
    global TT_biaozhun #line:1134
    OO000O000OO000OO0 =pd .merge (OO000O000OO000OO0 ,TT_biaozhun [OOOOOOOOOOOO0OOOO ],on =[OOOOOOOOOOOO0OOOO ],how ="left").reset_index (drop =True )#line:1135
    O0O0OO0OOO0O0OOO0 =OO000O000OO000OO0 ["使用次数"].mean ()#line:1137
    O0O0O0OOOOOO0OOO0 =OO000O000OO000OO0 ["使用次数"].isnull ()#line:1139
    if O0O0O0OOOOOO0OOO0 .any ():#line:1140
        OO0000O00O00O000O =OO000O000OO000OO0 [OOOOOOOOOOOO0OOOO ][O0O0O0OOOOOO0OOO0 ].tolist ()#line:1141
        OO0000O00O00O000O .remove ("All")#line:1142
    else :#line:1143
        OO0000O00O00O000O =[]#line:1144
    if len (OO0000O00O00O000O )!=0 :#line:1146
        showinfo (title ="提示",message =str (OO0000O00O00O000O )+"没有分母，用均值"+str (O0O0OO0OOO0O0OOO0 )+"填充计算。")#line:1147
    OO000O000OO000OO0 ["使用次数"]=OO000O000OO000OO0 ["使用次数"].fillna (int (O0O0OO0OOO0O0OOO0 ))#line:1149
    OOO0OO0OO0O000O00 =OO000O000OO000OO0 ["使用次数"][:-1 ].sum ()#line:1150
    OO000O000OO000OO0 .iloc [-1 ,-1 ]=OOO0OO0OO0O000O00 #line:1151
    OO0O00000000OO00O =[OOO0O00000OOOO00O for OOO0O00000OOOO00O in OO000O000OO000OO0 .columns if (OOO0O00000OOOO00O not in ["使用次数",OOOOOOOOOOOO0OOOO ])]#line:1152
    for OO00OOO00OOO00OOO ,OOO0O00O00OO0OO0O in OO000O000OO000OO0 .iterrows ():#line:1153
        for OO0O0OOO00OO00O0O in OO0O00000000OO00O :#line:1154
            OO000O000OO000OO0 .loc [OO00OOO00OOO00OOO ,OO0O0OOO00OO00O0O ]=int (OOO0O00O00OO0OO0O [OO0O0OOO00OO00O0O ])/int (OOO0O00O00OO0OO0O ["使用次数"])#line:1155
    del OO000O000OO000OO0 ["使用次数"]#line:1156
    Tread_TOOLS_tree_Level_2 (OO000O000OO000OO0 ,1 ,1 ,OOOOOOOOOOOO0OOOO )#line:1157
def TOOLS_save_dict (O0O00O0OOO000O00O ):#line:1159
    ""#line:1160
    O0O000OOO0O0O0OOO =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】.xls",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1166
    try :#line:1167
        O0O00O0OOO000O00O ["详细描述T"]=O0O00O0OOO000O00O ["详细描述T"].astype (str )#line:1168
    except :#line:1169
        pass #line:1170
    try :#line:1171
        O0O00O0OOO000O00O ["报告编码"]=O0O00O0OOO000O00O ["报告编码"].astype (str )#line:1172
    except :#line:1173
        pass #line:1174
    try :#line:1175
        OO000OOOOO000OO0O =re .search ("\【(.*?)\】",O0O000OOO0O0O0OOO )#line:1176
        O0O00O0OOO000O00O ["对象"]=OO000OOOOO000OO0O .group (1 )#line:1177
    except :#line:1178
        pass #line:1179
    OOOOO000O0O0O0OO0 =pd .ExcelWriter (O0O000OOO0O0O0OOO ,engine ="xlsxwriter")#line:1180
    O0O00O0OOO000O00O .to_excel (OOOOO000O0O0O0OO0 ,sheet_name ="字典数据")#line:1181
    OOOOO000O0O0O0OO0 .close ()#line:1182
    showinfo (title ="提示",message ="文件写入成功。")#line:1183
def Tread_TOOLS_DRAW_histbar (OOO0O0OOOO0OO00OO ):#line:1187
    ""#line:1188
    OO0O0O0O00O0OO0OO =Toplevel ()#line:1191
    OO0O0O0O00O0OO0OO .title ("直方图")#line:1192
    O0OOOO0O00OO00OO0 =ttk .Frame (OO0O0O0O00O0OO0OO ,height =20 )#line:1193
    O0OOOO0O00OO00OO0 .pack (side =TOP )#line:1194
    O000OO000O00OO00O =Figure (figsize =(12 ,6 ),dpi =100 )#line:1196
    O00OOO0O0O0OO0O00 =FigureCanvasTkAgg (O000OO000O00OO00O ,master =OO0O0O0O00O0OO0OO )#line:1197
    O00OOO0O0O0OO0O00 .draw ()#line:1198
    O00OOO0O0O0OO0O00 .get_tk_widget ().pack (expand =1 )#line:1199
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1201
    plt .rcParams ['axes.unicode_minus']=False #line:1202
    O0OO0O0OO000O0O0O =NavigationToolbar2Tk (O00OOO0O0O0OO0O00 ,OO0O0O0O00O0OO0OO )#line:1204
    O0OO0O0OO000O0O0O .update ()#line:1205
    O00OOO0O0O0OO0O00 .get_tk_widget ().pack ()#line:1206
    OO0OOO0O00O0O0000 =O000OO000O00OO00O .add_subplot (111 )#line:1208
    OO0OOO0O00O0O0000 .set_title ("直方图")#line:1210
    O00OOO0OOOOO00O00 =OOO0O0OOOO0OO00OO .columns .to_list ()#line:1212
    O00OOO0OOOOO00O00 .remove ("对象")#line:1213
    O0000O0OO0OO000OO =np .arange (len (O00OOO0OOOOO00O00 ))#line:1214
    for O0O0OOO00O0000000 in O00OOO0OOOOO00O00 :#line:1218
        OOO0O0OOOO0OO00OO [O0O0OOO00O0000000 ]=OOO0O0OOOO0OO00OO [O0O0OOO00O0000000 ].astype (float )#line:1219
    OOO0O0OOOO0OO00OO ['数据']=OOO0O0OOOO0OO00OO [O00OOO0OOOOO00O00 ].values .tolist ()#line:1221
    OOO00O0OOO0000000 =0 #line:1222
    for O00OOOOO00OOO0O0O ,OO0OO00O000O00000 in OOO0O0OOOO0OO00OO .iterrows ():#line:1223
        OO0OOO0O00O0O0000 .bar ([OO0OOOO0O0OOO0OOO +OOO00O0OOO0000000 for OO0OOOO0O0OOO0OOO in O0000O0OO0OO000OO ],OOO0O0OOOO0OO00OO .loc [O00OOOOO00OOO0O0O ,'数据'],label =O00OOO0OOOOO00O00 ,width =0.1 )#line:1224
        for O0000O00OO0O00O0O ,OOOO0O00OOO0O0000 in zip ([O0O00O0O000O0OOOO +OOO00O0OOO0000000 for O0O00O0O000O0OOOO in O0000O0OO0OO000OO ],OOO0O0OOOO0OO00OO .loc [O00OOOOO00OOO0O0O ,'数据']):#line:1227
           OO0OOO0O00O0O0000 .text (O0000O00OO0O00O0O -0.015 ,OOOO0O00OOO0O0000 +0.07 ,str (int (OOOO0O00OOO0O0000 )),color ='black',size =8 )#line:1228
        OOO00O0OOO0000000 =OOO00O0OOO0000000 +0.1 #line:1230
    OO0OOO0O00O0O0000 .set_xticklabels (OOO0O0OOOO0OO00OO .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1232
    OO0OOO0O00O0O0000 .legend (OOO0O0OOOO0OO00OO ["对象"])#line:1236
    O00OOO0O0O0OO0O00 .draw ()#line:1239
def Tread_TOOLS_DRAW_make_risk_plot (OO00O0OO0O0O00O0O ,OO0OO0OO0O00OO0O0 ,OO0O0O0OO0O0O0OOO ,O00OO0000OOO0000O ,O000000O0OOO0O0OO ,*OO0O000000O0O00O0 ):#line:1241
    ""#line:1242
    O0O000O0O0O000OOO =Toplevel ()#line:1245
    O0O000O0O0O000OOO .title (O00OO0000OOO0000O )#line:1246
    OO00OOOOO00OO0000 =ttk .Frame (O0O000O0O0O000OOO ,height =20 )#line:1247
    OO00OOOOO00OO0000 .pack (side =TOP )#line:1248
    OO00OOOOOOOO0OOOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1249
    OOO0O00OO0O00OOO0 =FigureCanvasTkAgg (OO00OOOOOOOO0OOOO ,master =O0O000O0O0O000OOO )#line:1250
    OOO0O00OO0O00OOO0 .draw ()#line:1251
    OOO0O00OO0O00OOO0 .get_tk_widget ().pack (expand =1 )#line:1252
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1254
    plt .rcParams ['axes.unicode_minus']=False #line:1255
    OOOOOOO0O0OO000OO =NavigationToolbar2Tk (OOO0O00OO0O00OOO0 ,O0O000O0O0O000OOO )#line:1257
    OOOOOOO0O0OO000OO .update ()#line:1258
    OOO0O00OO0O00OOO0 .get_tk_widget ().pack ()#line:1259
    OOO0OOOOOOO0000OO =OO00OOOOOOOO0OOOO .add_subplot (111 )#line:1261
    OOO0OOOOOOO0000OO .set_title (O00OO0000OOO0000O )#line:1263
    OOO0O00O0000O0O00 =OO00O0OO0O0O00O0O [OO0OO0OO0O00OO0O0 ]#line:1264
    if O000000O0OOO0O0OO !=999 :#line:1267
        OOO0OOOOOOO0000OO .set_xticklabels (OOO0O00O0000O0O00 ,rotation =-90 ,fontsize =8 )#line:1268
    OO0O0O00O0O000O00 =range (0 ,len (OOO0O00O0000O0O00 ),1 )#line:1271
    for O00OOO00OO0OO00O0 in OO0O0O0OO0O0O0OOO :#line:1276
        OO00OOOOOO0O0O0OO =OO00O0OO0O0O00O0O [O00OOO00OO0OO00O0 ].astype (float )#line:1277
        if O00OOO00OO0OO00O0 =="关注区域":#line:1279
            OOO0OOOOOOO0000OO .plot (list (OOO0O00O0000O0O00 ),list (OO00OOOOOO0O0O0OO ),label =str (O00OOO00OO0OO00O0 ),color ="red")#line:1280
        else :#line:1281
            OOO0OOOOOOO0000OO .plot (list (OOO0O00O0000O0O00 ),list (OO00OOOOOO0O0O0OO ),label =str (O00OOO00OO0OO00O0 ))#line:1282
        if O000000O0OOO0O0OO ==100 :#line:1285
            for O0O000O000O00OO00 ,OO00OO0OO0000OOO0 in zip (OOO0O00O0000O0O00 ,OO00OOOOOO0O0O0OO ):#line:1286
                if OO00OO0OO0000OOO0 ==max (OO00OOOOOO0O0O0OO )and OO00OO0OO0000OOO0 >=3 and len (OO0O0O0OO0O0O0OOO )!=1 :#line:1287
                     OOO0OOOOOOO0000OO .text (O0O000O000O00OO00 ,OO00OO0OO0000OOO0 ,(str (O00OOO00OO0OO00O0 )+":"+str (int (OO00OO0OO0000OOO0 ))),color ='black',size =8 )#line:1288
                if len (OO0O0O0OO0O0O0OOO )==1 and OO00OO0OO0000OOO0 >=0.01 :#line:1289
                     OOO0OOOOOOO0000OO .text (O0O000O000O00OO00 ,OO00OO0OO0000OOO0 ,str (int (OO00OO0OO0000OOO0 )),color ='black',size =8 )#line:1290
    try :#line:1300
        if OO0O000000O0O00O0 [0 ]:#line:1301
            O0OO00OO00O0OO0OO =OO0O000000O0O00O0 [0 ]#line:1302
    except :#line:1303
        O0OO00OO00O0OO0OO ="ucl"#line:1304
    if len (OO0O0O0OO0O0O0OOO )==1 :#line:1306
        if O0OO00OO00O0OO0OO =="更多控制线分位数":#line:1308
            OO0OOOOO00OOO00OO =OO00O0OO0O0O00O0O [OO0O0O0OO0O0O0OOO ].astype (float ).values #line:1309
            OOO0O0OO000OO00OO =np .median (OO0OOOOO00OOO00OO )#line:1310
            OO0OO0OO0OO000OOO =np .percentile (OO0OOOOO00OOO00OO ,25 )#line:1311
            OO0O0OO0000O0O000 =np .percentile (OO0OOOOO00OOO00OO ,75 )#line:1312
            O0O00OO00O0OO0O00 =OO0O0OO0000O0O000 -OO0OO0OO0OO000OOO #line:1313
            O0OO0000000O0O000 =OO0O0OO0000O0O000 +1.5 *O0O00OO00O0OO0O00 #line:1314
            OOOOOO0OO0O0O0OOO =OO0OO0OO0OO000OOO -1.5 *O0O00OO00O0OO0O00 #line:1315
            OOO0OOOOOOO0000OO .axhline (OOOOOO0OO0O0O0OOO ,color ='c',linestyle ='--',label ='异常下限')#line:1318
            OOO0OOOOOOO0000OO .axhline (OO0OO0OO0OO000OOO ,color ='r',linestyle ='--',label ='第25百分位数')#line:1320
            OOO0OOOOOOO0000OO .axhline (OOO0O0OO000OO00OO ,color ='g',linestyle ='--',label ='中位数')#line:1321
            OOO0OOOOOOO0000OO .axhline (OO0O0OO0000O0O000 ,color ='r',linestyle ='--',label ='第75百分位数')#line:1322
            OOO0OOOOOOO0000OO .axhline (O0OO0000000O0O000 ,color ='c',linestyle ='--',label ='异常上限')#line:1324
            OOO00000OO0OO0OO0 =ttk .Label (O0O000O0O0O000OOO ,text ="中位数="+str (OOO0O0OO000OO00OO )+"; 第25百分位数="+str (OO0OO0OO0OO000OOO )+"; 第75百分位数="+str (OO0O0OO0000O0O000 )+"; 异常上限(第75百分位数+1.5IQR)="+str (O0OO0000000O0O000 )+"; IQR="+str (O0O00OO00O0OO0O00 ))#line:1325
            OOO00000OO0OO0OO0 .pack ()#line:1326
        elif O0OO00OO00O0OO0OO =="更多控制线STD":#line:1328
            OO0OOOOO00OOO00OO =OO00O0OO0O0O00O0O [OO0O0O0OO0O0O0OOO ].astype (float ).values #line:1329
            O0O0O0O0O0O0OO0O0 =OO0OOOOO00OOO00OO .mean ()#line:1330
            O0000OO00O000OOO0 =OO0OOOOO00OOO00OO .std ()#line:1331
            O0O000OO0OO0OO000 =O0O0O0O0O0O0OO0O0 +3 *O0000OO00O000OOO0 #line:1332
            OO00O0OOOO00O0O0O =O0000OO00O000OOO0 -3 *O0000OO00O000OOO0 #line:1333
            OOOOO0O00O00OO000 =O0O0O0O0O0O0OO0O0 -1.96 *O0000OO00O000OOO0 /math .sqrt (len (OO0OOOOO00OOO00OO ))#line:1334
            O0OO00O00OOOOOO00 =O0O0O0O0O0O0OO0O0 +1.96 *O0000OO00O000OOO0 /math .sqrt (len (OO0OOOOO00OOO00OO ))#line:1335
            OOO0OOOOOOO0000OO .axhline (O0O000OO0OO0OO000 ,color ='r',linestyle ='--',label ='UCL')#line:1336
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 +2 *O0000OO00O000OOO0 ,color ='m',linestyle ='--',label ='μ+2σ')#line:1337
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 +O0000OO00O000OOO0 ,color ='m',linestyle ='--',label ='μ+σ')#line:1338
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 ,color ='g',linestyle ='--',label ='CL')#line:1339
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 -O0000OO00O000OOO0 ,color ='m',linestyle ='--',label ='μ-σ')#line:1340
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 -2 *O0000OO00O000OOO0 ,color ='m',linestyle ='--',label ='μ-2σ')#line:1341
            OOO0OOOOOOO0000OO .axhline (OO00O0OOOO00O0O0O ,color ='r',linestyle ='--',label ='LCL')#line:1342
            O0OOO00OO0OOOO0OO =ttk .Label (O0O000O0O0O000OOO ,text ="mean="+str (O0O0O0O0O0O0OO0O0 )+"; std="+str (O0000OO00O000OOO0 )+"; 99.73%:UCL(μ+3σ)="+str (O0O000OO0OO0OO000 )+"; LCL(μ-3σ)="+str (OO00O0OOOO00O0O0O ))#line:1344
            O0OOO00OO0OOOO0OO .pack ()#line:1345
            OOO00000OO0OO0OO0 =ttk .Label (O0O000O0O0O000OOO ,text ="68.26%:μ+σ="+str (O0O0O0O0O0O0OO0O0 +O0000OO00O000OOO0 )+"; 95.45%:μ+2σ="+str (O0O0O0O0O0O0OO0O0 +2 *O0000OO00O000OOO0 ))#line:1347
            OOO00000OO0OO0OO0 .pack ()#line:1348
        else :#line:1350
            OO0OOOOO00OOO00OO =OO00O0OO0O0O00O0O [OO0O0O0OO0O0O0OOO ].astype (float ).values #line:1351
            O0O0O0O0O0O0OO0O0 =OO0OOOOO00OOO00OO .mean ()#line:1352
            O0000OO00O000OOO0 =OO0OOOOO00OOO00OO .std ()#line:1353
            O0O000OO0OO0OO000 =O0O0O0O0O0O0OO0O0 +3 *O0000OO00O000OOO0 #line:1354
            OO00O0OOOO00O0O0O =O0000OO00O000OOO0 -3 *O0000OO00O000OOO0 #line:1355
            OOO0OOOOOOO0000OO .axhline (O0O000OO0OO0OO000 ,color ='r',linestyle ='--',label ='UCL')#line:1356
            OOO0OOOOOOO0000OO .axhline (O0O0O0O0O0O0OO0O0 ,color ='g',linestyle ='--',label ='CL')#line:1357
            OOO0OOOOOOO0000OO .axhline (OO00O0OOOO00O0O0O ,color ='r',linestyle ='--',label ='LCL')#line:1358
            O0OOO00OO0OOOO0OO =ttk .Label (O0O000O0O0O000OOO ,text ="mean="+str (O0O0O0O0O0O0OO0O0 )+"; std="+str (O0000OO00O000OOO0 )+"; UCL(μ+3σ)="+str (O0O000OO0OO0OO000 )+"; LCL(μ-3σ)="+str (OO00O0OOOO00O0O0O ))#line:1359
            O0OOO00OO0OOOO0OO .pack ()#line:1360
    OOO0OOOOOOO0000OO .set_title ("控制图")#line:1363
    OOO0OOOOOOO0000OO .set_xlabel ("项")#line:1364
    OO00OOOOOOOO0OOOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1365
    OOO0OO000OOOO0O0O =OOO0OOOOOOO0000OO .get_position ()#line:1366
    OOO0OOOOOOO0000OO .set_position ([OOO0OO000OOOO0O0O .x0 ,OOO0OO000OOOO0O0O .y0 ,OOO0OO000OOOO0O0O .width *0.7 ,OOO0OO000OOOO0O0O .height ])#line:1367
    OOO0OOOOOOO0000OO .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1368
    OOO00000OO0OO0000 =StringVar ()#line:1371
    OO0OOO0OO0O0O0OOO =ttk .Combobox (OO00OOOOO00OO0000 ,width =15 ,textvariable =OOO00000OO0OO0000 ,state ='readonly')#line:1372
    OO0OOO0OO0O0O0OOO ['values']=OO0O0O0OO0O0O0OOO #line:1373
    OO0OOO0OO0O0O0OOO .pack (side =LEFT )#line:1374
    OO0OOO0OO0O0O0OOO .current (0 )#line:1375
    O00O0000O000000O0 =Button (OO00OOOOO00OO0000 ,text ="控制图（单项-UCL(μ+3σ)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00O0OO0O0O00O0O ,OO0OO0OO0O00OO0O0 ,[O0000O0OOO0O0O0OO for O0000O0OOO0O0O0OO in OO0O0O0OO0O0O0OOO if OOO00000OO0OO0000 .get ()in O0000O0OOO0O0O0OO ],O00OO0000OOO0000O ,O000000O0OOO0O0OO ))#line:1385
    O00O0000O000000O0 .pack (side =LEFT ,anchor ="ne")#line:1386
    OOOO0OO00O00OOO0O =Button (OO00OOOOO00OO0000 ,text ="控制图（单项-UCL(标准差法)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00O0OO0O0O00O0O ,OO0OO0OO0O00OO0O0 ,[O000O0O0OO0O00OO0 for O000O0O0OO0O00OO0 in OO0O0O0OO0O0O0OOO if OOO00000OO0OO0000 .get ()in O000O0O0OO0O00OO0 ],O00OO0000OOO0000O ,O000000O0OOO0O0OO ,"更多控制线STD"))#line:1394
    OOOO0OO00O00OOO0O .pack (side =LEFT ,anchor ="ne")#line:1395
    OOOO0OO00O00OOO0O =Button (OO00OOOOO00OO0000 ,text ="控制图（单项-分位数）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00O0OO0O0O00O0O ,OO0OO0OO0O00OO0O0 ,[OO00000OO0O000000 for OO00000OO0O000000 in OO0O0O0OO0O0O0OOO if OOO00000OO0OO0000 .get ()in OO00000OO0O000000 ],O00OO0000OOO0000O ,O000000O0OOO0O0OO ,"更多控制线分位数"))#line:1403
    OOOO0OO00O00OOO0O .pack (side =LEFT ,anchor ="ne")#line:1404
    O0OO0OOOOO000OO00 =Button (OO00OOOOO00OO0000 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00O0OO0O0O00O0O ,OO0OO0OO0O00OO0O0 ,OO0O0O0OO0O0O0OOO ,O00OO0000OOO0000O ,0 ))#line:1413
    O0OO0OOOOO000OO00 .pack (side =LEFT ,anchor ="ne")#line:1415
    OOO0O00OO0O00OOO0 .draw ()#line:1416
def Tread_TOOLS_draw (O00OO0O0OO0O0OOO0 ,O0OO0OO00O0OOOO0O ,OOOO0OOO0O000OOOO ,OO00OO0OO000O0OOO ,O00OOO0OOOOOO00O0 ):#line:1418
    ""#line:1419
    warnings .filterwarnings ("ignore")#line:1420
    O00OOO0O0OO000O0O =Toplevel ()#line:1421
    O00OOO0O0OO000O0O .title (O0OO0OO00O0OOOO0O )#line:1422
    O00OO0O0O00O0OOO0 =ttk .Frame (O00OOO0O0OO000O0O ,height =20 )#line:1423
    O00OO0O0O00O0OOO0 .pack (side =TOP )#line:1424
    O0O000000OOOO0O00 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1426
    O00OO00OO00O00OO0 =FigureCanvasTkAgg (O0O000000OOOO0O00 ,master =O00OOO0O0OO000O0O )#line:1427
    O00OO00OO00O00OO0 .draw ()#line:1428
    O00OO00OO00O00OO0 .get_tk_widget ().pack (expand =1 )#line:1429
    OO0O00OO000O0OOOO =O0O000000OOOO0O00 .add_subplot (111 )#line:1430
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1432
    plt .rcParams ['axes.unicode_minus']=False #line:1433
    O0OOO000000000OO0 =NavigationToolbar2Tk (O00OO00OO00O00OO0 ,O00OOO0O0OO000O0O )#line:1435
    O0OOO000000000OO0 .update ()#line:1436
    O00OO00OO00O00OO0 .get_tk_widget ().pack ()#line:1438
    try :#line:1441
        OOOO0O0000000O0OO =O00OO0O0OO0O0OOO0 .columns #line:1442
        O00OO0O0OO0O0OOO0 =O00OO0O0OO0O0OOO0 .sort_values (by =OO00OO0OO000O0OOO ,ascending =[False ],na_position ="last")#line:1443
    except :#line:1444
        O0OOO0OOO00OOO0OO =eval (O00OO0O0OO0O0OOO0 )#line:1445
        O0OOO0OOO00OOO0OO =pd .DataFrame .from_dict (O0OOO0OOO00OOO0OO ,TT_orient =OOOO0OOO0O000OOOO ,columns =[OO00OO0OO000O0OOO ]).reset_index ()#line:1448
        O00OO0O0OO0O0OOO0 =O0OOO0OOO00OOO0OO .sort_values (by =OO00OO0OO000O0OOO ,ascending =[False ],na_position ="last")#line:1449
    if ("日期"in O0OO0OO00O0OOOO0O or "时间"in O0OO0OO00O0OOOO0O or "季度"in O0OO0OO00O0OOOO0O )and "饼图"not in O00OOO0OOOOOO00O0 :#line:1453
        O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ]=pd .to_datetime (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],format ="%Y/%m/%d").dt .date #line:1454
        O00OO0O0OO0O0OOO0 =O00OO0O0OO0O0OOO0 .sort_values (by =OOOO0OOO0O000OOOO ,ascending =[True ],na_position ="last")#line:1455
    elif "批号"in O0OO0OO00O0OOOO0O :#line:1456
        O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ]=O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ].astype (str )#line:1457
        O00OO0O0OO0O0OOO0 =O00OO0O0OO0O0OOO0 .sort_values (by =OOOO0OOO0O000OOOO ,ascending =[True ],na_position ="last")#line:1458
        OO0O00OO000O0OOOO .set_xticklabels (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],rotation =-90 ,fontsize =8 )#line:1459
    else :#line:1460
        O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ]=O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ].astype (str )#line:1461
        OO0O00OO000O0OOOO .set_xticklabels (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],rotation =-90 ,fontsize =8 )#line:1462
    OOOOO0OO0OOOO00OO =O00OO0O0OO0O0OOO0 [OO00OO0OO000O0OOO ]#line:1464
    O0OOO000O0O0OOO00 =range (0 ,len (OOOOO0OO0OOOO00OO ),1 )#line:1465
    OO0O00OO000O0OOOO .set_title (O0OO0OO00O0OOOO0O )#line:1467
    if O00OOO0OOOOOO00O0 =="柱状图":#line:1471
        OO0O00OO000O0OOOO .bar (x =O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],height =OOOOO0OO0OOOO00OO ,width =0.2 ,color ="#87CEFA")#line:1472
    elif O00OOO0OOOOOO00O0 =="饼图":#line:1473
        OO0O00OO000O0OOOO .pie (x =OOOOO0OO0OOOO00OO ,labels =O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],autopct ="%0.2f%%")#line:1474
    elif O00OOO0OOOOOO00O0 =="折线图":#line:1475
        OO0O00OO000O0OOOO .plot (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],OOOOO0OO0OOOO00OO ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1476
    elif "帕累托图"in str (O00OOO0OOOOOO00O0 ):#line:1478
        OO000000O0O0O0000 =O00OO0O0OO0O0OOO0 [OO00OO0OO000O0OOO ].fillna (0 )#line:1479
        OO00O000OOOOO0OO0 =OO000000O0O0O0000 .cumsum ()/OO000000O0O0O0000 .sum ()*100 #line:1483
        O00OO0O0OO0O0OOO0 ["百分比"]=round (O00OO0O0OO0O0OOO0 ["数量"]/OO000000O0O0O0000 .sum ()*100 ,2 )#line:1484
        O00OO0O0OO0O0OOO0 ["累计百分比"]=round (OO00O000OOOOO0OO0 ,2 )#line:1485
        O0OOO00O0OOO000OO =OO00O000OOOOO0OO0 [OO00O000OOOOO0OO0 >0.8 ].index [0 ]#line:1486
        OOOOO00O00OO00000 =OO000000O0O0O0000 .index .tolist ().index (O0OOO00O0OOO000OO )#line:1487
        OO0O00OO000O0OOOO .bar (x =O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],height =OO000000O0O0O0000 ,color ="C0",label =OO00OO0OO000O0OOO )#line:1491
        OO00O0OOO0OOO0OO0 =OO0O00OO000O0OOOO .twinx ()#line:1492
        OO00O0OOO0OOO0OO0 .plot (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],OO00O000OOOOO0OO0 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1493
        OO00O0OOO0OOO0OO0 .yaxis .set_major_formatter (PercentFormatter ())#line:1494
        OO0O00OO000O0OOOO .tick_params (axis ="y",colors ="C0")#line:1499
        OO00O0OOO0OOO0OO0 .tick_params (axis ="y",colors ="C1")#line:1500
        for OOOOO00O0O000O0O0 ,O0O0OOO0000OO000O ,O0O00OOOOO0OOO0OO ,O000O00O000O000OO in zip (O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],OO000000O0O0O0000 ,O00OO0O0OO0O0OOO0 ["百分比"],O00OO0O0OO0O0OOO0 ["累计百分比"]):#line:1502
            OO0O00OO000O0OOOO .text (OOOOO00O0O000O0O0 ,O0O0OOO0000OO000O +0.1 ,str (int (O0O0OOO0000OO000O ))+", "+str (int (O0O00OOOOO0OOO0OO ))+"%,"+str (int (O000O00O000O000OO ))+"%",color ='black',size =8 )#line:1503
        if "超级帕累托图"in str (O00OOO0OOOOOO00O0 ):#line:1506
            OOO00O00O000OO0OO =re .compile (r'[(](.*?)[)]',re .S )#line:1507
            O0O00OOOOOOO0OO0O =re .findall (OOO00O00O000OO0OO ,O00OOO0OOOOOO00O0 )[0 ]#line:1508
            OO0O00OO000O0OOOO .bar (x =O00OO0O0OO0O0OOO0 [OOOO0OOO0O000OOOO ],height =O00OO0O0OO0O0OOO0 [O0O00OOOOOOO0OO0O ],color ="orangered",label =O0O00OOOOOOO0OO0O )#line:1509
    O0O000000OOOO0O00 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1514
    OOO0000OOOOO00O00 =OO0O00OO000O0OOOO .get_position ()#line:1515
    OO0O00OO000O0OOOO .set_position ([OOO0000OOOOO00O00 .x0 ,OOO0000OOOOO00O00 .y0 ,OOO0000OOOOO00O00 .width *0.7 ,OOO0000OOOOO00O00 .height ])#line:1516
    OO0O00OO000O0OOOO .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1517
    O00OO00OO00O00OO0 .draw ()#line:1520
    if len (OOOOO0OO0OOOO00OO )<=20 and O00OOO0OOOOOO00O0 !="饼图"and O00OOO0OOOOOO00O0 !="帕累托图":#line:1523
        for OO0OO00OOOOOO00O0 ,O000OOO000O0O000O in zip (O0OOO000O0O0OOO00 ,OOOOO0OO0OOOO00OO ):#line:1524
            OOO0OOOOO00OO0000 =str (O000OOO000O0O000O )#line:1525
            O0OOO00O0O0OO0OOO =(OO0OO00OOOOOO00O0 ,O000OOO000O0O000O +0.3 )#line:1526
            OO0O00OO000O0OOOO .annotate (OOO0OOOOO00OO0000 ,xy =O0OOO00O0O0OO0OOO ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1527
    OO0O0O0OOOO000000 =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O00OO0O0OO0O0OOO0 ),)#line:1537
    OO0O0O0OOOO000000 .pack (side =RIGHT )#line:1538
    O0O0OO0OO0O00OO00 =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (O00OO0O0OO0O0OOO0 ,1 ))#line:1542
    O0O0OO0OO0O00OO00 .pack (side =RIGHT )#line:1543
    OOOOO000OO000OO0O =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (O00OO0O0OO0O0OOO0 ,O0OO0OO00O0OOOO0O ,OOOO0OOO0O000OOOO ,OO00OO0OO000O0OOO ,"饼图"),)#line:1551
    OOOOO000OO000OO0O .pack (side =LEFT )#line:1552
    OOOOO000OO000OO0O =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (O00OO0O0OO0O0OOO0 ,O0OO0OO00O0OOOO0O ,OOOO0OOO0O000OOOO ,OO00OO0OO000O0OOO ,"柱状图"),)#line:1559
    OOOOO000OO000OO0O .pack (side =LEFT )#line:1560
    OOOOO000OO000OO0O =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (O00OO0O0OO0O0OOO0 ,O0OO0OO00O0OOOO0O ,OOOO0OOO0O000OOOO ,OO00OO0OO000O0OOO ,"折线图"),)#line:1566
    OOOOO000OO000OO0O .pack (side =LEFT )#line:1567
    OOOOO000OO000OO0O =Button (O00OO0O0O00O0OOO0 ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (O00OO0O0OO0O0OOO0 ,O0OO0OO00O0OOOO0O ,OOOO0OOO0O000OOOO ,OO00OO0OO000O0OOO ,"帕累托图"),)#line:1574
    OOOOO000OO000OO0O .pack (side =LEFT )#line:1575
def helper ():#line:1581
    ""#line:1582
    OOOOO00000O0OOO0O =Toplevel ()#line:1583
    OOOOO00000O0OOO0O .title ("程序使用帮助")#line:1584
    OOOOO00000O0OOO0O .geometry ("700x500")#line:1585
    OOO00O000O0OO0000 =Scrollbar (OOOOO00000O0OOO0O )#line:1587
    O000O0OOO0O00OOO0 =Text (OOOOO00000O0OOO0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1588
    OOO00O000O0OO0000 .pack (side =RIGHT ,fill =Y )#line:1589
    O000O0OOO0O00OOO0 .pack ()#line:1590
    OOO00O000O0OO0000 .config (command =O000O0OOO0O00OOO0 .yview )#line:1591
    O000O0OOO0O00OOO0 .config (yscrollcommand =OOO00O000O0OO0000 .set )#line:1592
    O000O0OOO0O00OOO0 .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1597
    O000O0OOO0O00OOO0 .config (state =DISABLED )#line:1598
def Tread_TOOLS_CLEAN (OOOO0OOO0OOO00O0O ):#line:1602
        ""#line:1603
        OOOO0OOO0OOO00O0O ["报告编码"]=OOOO0OOO0OOO00O0O ["报告编码"].astype ("str")#line:1605
        OOOO0OOO0OOO00O0O ["产品批号"]=OOOO0OOO0OOO00O0O ["产品批号"].astype ("str")#line:1607
        OOOO0OOO0OOO00O0O ["型号"]=OOOO0OOO0OOO00O0O ["型号"].astype ("str")#line:1608
        OOOO0OOO0OOO00O0O ["规格"]=OOOO0OOO0OOO00O0O ["规格"].astype ("str")#line:1609
        OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"]=OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1611
        OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"]=OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1612
        OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"]=OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1613
        OOOO0OOO0OOO00O0O ["产品名称"]=OOOO0OOO0OOO00O0O ["产品名称"].str .replace ("*","※",regex =False )#line:1615
        OOOO0OOO0OOO00O0O ["产品批号"]=OOOO0OOO0OOO00O0O ["产品批号"].str .replace ("(","（",regex =False )#line:1617
        OOOO0OOO0OOO00O0O ["产品批号"]=OOOO0OOO0OOO00O0O ["产品批号"].str .replace (")","）",regex =False )#line:1618
        OOOO0OOO0OOO00O0O ["产品批号"]=OOOO0OOO0OOO00O0O ["产品批号"].str .replace ("*","※",regex =False )#line:1619
        OOOO0OOO0OOO00O0O ['事件发生日期']=pd .to_datetime (OOOO0OOO0OOO00O0O ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1622
        OOOO0OOO0OOO00O0O ["事件发生月份"]=OOOO0OOO0OOO00O0O ["事件发生日期"].dt .to_period ("M").astype (str )#line:1626
        OOOO0OOO0OOO00O0O ["事件发生季度"]=OOOO0OOO0OOO00O0O ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1627
        OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"]=OOOO0OOO0OOO00O0O ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1631
        OOOO0OOO0OOO00O0O ["产品批号"]=OOOO0OOO0OOO00O0O ["产品批号"].fillna ("未填写")#line:1632
        OOOO0OOO0OOO00O0O ["型号"]=OOOO0OOO0OOO00O0O ["型号"].fillna ("未填写")#line:1633
        OOOO0OOO0OOO00O0O ["规格"]=OOOO0OOO0OOO00O0O ["规格"].fillna ("未填写")#line:1634
        return OOOO0OOO0OOO00O0O #line:1636
def thread_it (O0OO000000O00OOO0 ,*OOO0OOOO000000O00 ):#line:1640
    ""#line:1641
    O0OO00O0OOOOO0OO0 =threading .Thread (target =O0OO000000O00OOO0 ,args =OOO0OOOO000000O00 )#line:1643
    O0OO00O0OOOOO0OO0 .setDaemon (True )#line:1645
    O0OO00O0OOOOO0OO0 .start ()#line:1647
def showWelcome ():#line:1650
    ""#line:1651
    O0O000O000000O000 =roox .winfo_screenwidth ()#line:1652
    OOOO00O00OO0O0O00 =roox .winfo_screenheight ()#line:1654
    roox .overrideredirect (True )#line:1656
    roox .attributes ("-alpha",1 )#line:1657
    OOO000OOOOO00O00O =(O0O000O000000O000 -475 )/2 #line:1658
    OOOOOO000OOO00O00 =(OOOO00O00OO0O0O00 -200 )/2 #line:1659
    roox .geometry ("675x140+%d+%d"%(OOO000OOOOO00O00O ,OOOOOO000OOO00O00 ))#line:1661
    roox ["bg"]="royalblue"#line:1662
    OOO000O000O0O0O0O =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1665
    OOO000O000O0O0O0O .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1666
    OOOO0OO0OO00O00OO =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1673
    OOOO0OO0OO00O00OO .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1674
def closeWelcome ():#line:1677
    ""#line:1678
    for OOOOO0OOOOOO0O0O0 in range (2 ):#line:1679
        root .attributes ("-alpha",0 )#line:1680
        time .sleep (1 )#line:1681
    root .attributes ("-alpha",1 )#line:1682
    roox .destroy ()#line:1683
if __name__ =='__main__':#line:1687
    pass #line:1688
root =Tk ()#line:1689
root .title ("医疗器械警戒趋势分析工具Trend Analysis Tools V"+str (version_now ))#line:1690
sw_root =root .winfo_screenwidth ()#line:1691
sh_root =root .winfo_screenheight ()#line:1693
ww_root =700 #line:1695
wh_root =620 #line:1696
x_root =(sw_root -ww_root )/2 #line:1698
y_root =(sh_root -wh_root )/2 #line:1699
root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:1700
root .configure (bg ="steelblue")#line:1701
try :#line:1704
    frame0 =ttk .Frame (root ,width =100 ,height =20 )#line:1705
    frame0 .pack (side =LEFT )#line:1706
    B_open_files1 =Button (frame0 ,text ="导入原始数据",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,0 ),)#line:1719
    B_open_files1 .pack ()#line:1720
    B_open_files3 =Button (frame0 ,text ="导入分析规则",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,1 ),)#line:1733
    B_open_files3 .pack ()#line:1734
    B_open_files3 =Button (frame0 ,text ="趋势统计分析",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_analysis ,0 ),)#line:1749
    B_open_files3 .pack ()#line:1750
    B_open_files3 =Button (frame0 ,text ="直方图（数量）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"数量"))#line:1763
    B_open_files3 .pack ()#line:1764
    B_open_files3 =Button (frame0 ,text ="直方图（占比）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"百分比"))#line:1775
    B_open_files3 .pack ()#line:1776
    B_open_files3 =Button (frame0 ,text ="查看帮助文件",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (helper ))#line:1787
    B_open_files3 .pack ()#line:1788
    B_open_files3 =Button (frame0 ,text ="更改用户分组",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (display_random_number ))#line:1799
    B_open_files3 .pack ()#line:1800
except :#line:1801
    pass #line:1802
text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF",font ="微软雅黑")#line:1806
text .pack ()#line:1807
text .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1812
text .insert (END ,"\n\n")#line:1813
def A000 ():#line:1815
    pass #line:1816
setting_cfg =read_setting_cfg ()#line:1820
generate_random_file ()#line:1821
setting_cfg =open_setting_cfg ()#line:1822
if setting_cfg ["settingdir"]==0 :#line:1823
    showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:1824
    filepathu =filedialog .askdirectory ()#line:1825
    path =get_directory_path (filepathu )#line:1826
    update_setting_cfg ("settingdir",path )#line:1827
setting_cfg =open_setting_cfg ()#line:1828
random_number =int (setting_cfg ["sidori"])#line:1829
input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:1830
day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:1831
sid =random_number *2 +183576 #line:1832
if input_number ==sid and day_end =="未过期":#line:1833
    usergroup ="用户组=1"#line:1834
    text .insert (END ,usergroup +"   有效期至：")#line:1835
    text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:1836
else :#line:1837
    text .insert (END ,usergroup )#line:1838
text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:1839
roox =Toplevel ()#line:1843
tMain =threading .Thread (target =showWelcome )#line:1844
tMain .start ()#line:1845
t1 =threading .Thread (target =closeWelcome )#line:1846
t1 .start ()#line:1847
root .lift ()#line:1851
root .attributes ("-topmost",True )#line:1852
root .attributes ("-topmost",False )#line:1853
root .mainloop ()#line:1854
