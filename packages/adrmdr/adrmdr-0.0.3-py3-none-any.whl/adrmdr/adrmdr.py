#!/usr/bin/env python
# coding: utf-8
import tkinter as Tk #line:11
import os #line:12
import traceback #line:13
import ast #line:14
import re #line:15
import xlrd #line:16
import xlwt #line:17
import openpyxl #line:18
import pandas as pd #line:19
import numpy as np #line:20
import math #line:21
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:23
import tkinter .font as tkFont #line:24
from tkinter .messagebox import showinfo #line:25
from tkinter .scrolledtext import ScrolledText #line:26
import matplotlib as plt #line:27
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:28
from matplotlib .figure import Figure #line:29
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:30
import collections #line:31
from collections import Counter #line:32
import datetime #line:33
from datetime import datetime ,timedelta #line:34
import xlsxwriter #line:35
import time #line:36
import threading #line:37
import warnings #line:38
from matplotlib .ticker import PercentFormatter #line:39
import sqlite3 #line:40
from sqlalchemy import create_engine #line:41
from sqlalchemy import text as sqltext #line:42
import webbrowser #line:44
global ori #line:47
ori =0 #line:48
global auto_guize #line:49
global biaozhun #line:52
global dishi #line:53
biaozhun =""#line:54
dishi =""#line:55
global ini #line:59
ini ={}#line:60
ini ["四个品种"]=1 #line:61
import random #line:64
import requests #line:65
global version_now #line:66
global usergroup #line:67
global setting_cfg #line:68
global csdir #line:69
global peizhidir #line:70
version_now ="0.0.3"#line:71
usergroup ="用户组=0"#line:72
setting_cfg =""#line:73
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:74
if csdir =="":#line:75
    csdir =str (os .path .dirname (__file__ ))#line:76
    csdir =csdir +csdir .split ("adrmdr")[0 ][-1 ]#line:77
title_all ="药械妆不良反应报表统计分析工作站 V"+version_now #line:80
title_all2 ="药械妆不良反应报表统计分析工作站 V"+version_now #line:81
def extract_zip_file (O0000OO00O000O0O0 ,O00O0O0O000OO0O00 ):#line:88
    import zipfile #line:90
    if O00O0O0O000OO0O00 =="":#line:91
        return 0 #line:92
    with zipfile .ZipFile (O0000OO00O000O0O0 ,'r')as OO0OOO0O0000OO0OO :#line:93
        for O00O00O0O000000O0 in OO0OOO0O0000OO0OO .infolist ():#line:94
            O00O00O0O000000O0 .filename =O00O00O0O000000O0 .filename .encode ('cp437').decode ('gbk')#line:96
            OO0OOO0O0000OO0OO .extract (O00O00O0O000000O0 ,O00O0O0O000OO0O00 )#line:97
def get_directory_path (OOOOO00OO0O000OO0 ):#line:103
    global csdir #line:105
    if not (os .path .isfile (os .path .join (OOOOO00OO0O000OO0 ,'0（范例）比例失衡关键字库.xls'))):#line:107
        extract_zip_file (csdir +"def.py",OOOOO00OO0O000OO0 )#line:112
    if OOOOO00OO0O000OO0 =="":#line:114
        quit ()#line:115
    return OOOOO00OO0O000OO0 #line:116
def convert_and_compare_dates (O0000000O00O0OOO0 ):#line:120
    import datetime #line:121
    OO0000OOOO00000OO =datetime .datetime .now ()#line:122
    try :#line:124
       OOOO0OO00000OO0O0 =datetime .datetime .strptime (str (int (int (O0000000O00O0OOO0 )/4 )),"%Y%m%d")#line:125
    except :#line:126
        print ("fail")#line:127
        return "已过期"#line:128
    if OOOO0OO00000OO0O0 >OO0000OOOO00000OO :#line:130
        return "未过期"#line:132
    else :#line:133
        return "已过期"#line:134
def read_setting_cfg ():#line:136
    global csdir #line:137
    if os .path .exists (csdir +'setting.cfg'):#line:139
        text .insert (END ,"已完成初始化\n")#line:140
        with open (csdir +'setting.cfg','r')as OO0O000O0O0000O00 :#line:141
            O0OOO00O0OO0000OO =eval (OO0O000O0O0000O00 .read ())#line:142
    else :#line:143
        OO000OO0OO00O0OOO =csdir +'setting.cfg'#line:145
        with open (OO000OO0OO00O0OOO ,'w')as OO0O000O0O0000O00 :#line:146
            OO0O000O0O0000O00 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:147
        text .insert (END ,"未初始化，正在初始化...\n")#line:148
        O0OOO00O0OO0000OO =read_setting_cfg ()#line:149
    return O0OOO00O0OO0000OO #line:150
def open_setting_cfg ():#line:153
    global csdir #line:154
    with open (csdir +"setting.cfg","r")as OOO0O0O0O0OO00OOO :#line:156
        OO0OO0O00O0000OO0 =eval (OOO0O0O0O0OO00OOO .read ())#line:158
    return OO0OO0O00O0000OO0 #line:159
def update_setting_cfg (O0O0OO0OO00000000 ,O00O0000O0O00OOOO ):#line:161
    global csdir #line:162
    with open (csdir +"setting.cfg","r")as O0O00O000OOOOOOOO :#line:164
        O00000OO0OOOO0000 =eval (O0O00O000OOOOOOOO .read ())#line:166
    if O00000OO0OOOO0000 [O0O0OO0OO00000000 ]==0 or O00000OO0OOOO0000 [O0O0OO0OO00000000 ]=="11111180000808":#line:168
        O00000OO0OOOO0000 [O0O0OO0OO00000000 ]=O00O0000O0O00OOOO #line:169
        with open (csdir +"setting.cfg","w")as O0O00O000OOOOOOOO :#line:171
            O0O00O000OOOOOOOO .write (str (O00000OO0OOOO0000 ))#line:172
def generate_random_file ():#line:175
    O00OO00O0OO0O000O =random .randint (200000 ,299999 )#line:177
    update_setting_cfg ("sidori",O00OO00O0OO0O000O )#line:179
def display_random_number ():#line:181
    global csdir #line:182
    O00OO0O0O0O0OOO00 =Toplevel ()#line:183
    O00OO0O0O0O0OOO00 .title ("ID")#line:184
    OO0O0O0OOO00000O0 =O00OO0O0O0O0OOO00 .winfo_screenwidth ()#line:186
    O00OO0OOOOOO00OO0 =O00OO0O0O0O0OOO00 .winfo_screenheight ()#line:187
    O000O00O0O00000O0 =80 #line:189
    OOO0OOOOOO0O0OO0O =70 #line:190
    O000O00OO0OOOOO00 =(OO0O0O0OOO00000O0 -O000O00O0O00000O0 )/2 #line:192
    OOO00O0OO00O000O0 =(O00OO0OOOOOO00OO0 -OOO0OOOOOO0O0OO0O )/2 #line:193
    O00OO0O0O0O0OOO00 .geometry ("%dx%d+%d+%d"%(O000O00O0O00000O0 ,OOO0OOOOOO0O0OO0O ,O000O00OO0OOOOO00 ,OOO00O0OO00O000O0 ))#line:194
    with open (csdir +"setting.cfg","r")as O00O0000O00OO000O :#line:197
        OO000OO0OO00000OO =eval (O00O0000O00OO000O .read ())#line:199
    O00O0O0O0O00O0O0O =int (OO000OO0OO00000OO ["sidori"])#line:200
    O00OO0000OO000O0O =O00O0O0O0O00O0O0O *2 +183576 #line:201
    print (O00OO0000OO000O0O )#line:203
    OO0OOOO0O00O00000 =ttk .Label (O00OO0O0O0O0OOO00 ,text =f"机器码: {O00O0O0O0O00O0O0O}")#line:205
    OO00O0O0OO0000O00 =ttk .Entry (O00OO0O0O0O0OOO00 )#line:206
    OO0OOOO0O00O00000 .pack ()#line:209
    OO00O0O0OO0000O00 .pack ()#line:210
    ttk .Button (O00OO0O0O0O0OOO00 ,text ="验证",command =lambda :check_input (OO00O0O0OO0000O00 .get (),O00OO0000OO000O0O )).pack ()#line:214
def check_input (O00OOO0000000O000 ,OO0O0O0O00O0OO000 ):#line:216
    try :#line:220
        O0O0000000OO0O00O =int (str (O00OOO0000000O000 )[0 :6 ])#line:221
        OO00O0O00O00OO0O0 =convert_and_compare_dates (str (O00OOO0000000O000 )[6 :14 ])#line:222
    except :#line:223
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:224
        return 0 #line:225
    if O0O0000000OO0O00O ==OO0O0O0O00O0OO000 and OO00O0O00O00OO0O0 =="未过期":#line:227
        update_setting_cfg ("sidfinal",O00OOO0000000O000 )#line:228
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:229
        quit ()#line:230
    else :#line:231
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:232
def update_software (O00O00OO00OO00O00 ):#line:237
    global version_now #line:239
    text .insert (END ,"当前版本为："+version_now +",正在检查更新...(您可以同时执行分析任务)")#line:240
    try :#line:241
        OO0O00O0O0000OOO0 =requests .get (f"https://pypi.org/pypi/{O00O00OO00OO00O00}/json",timeout =2 ).json ()["info"]["version"]#line:242
    except :#line:243
        return "...更新失败。"#line:244
    if OO0O00O0O0000OOO0 >version_now :#line:245
        text .insert (END ,"\n最新版本为："+OO0O00O0O0000OOO0 +",正在尝试自动更新....")#line:246
        pip .main (['install',O00O00OO00OO00O00 ,'--upgrade'])#line:248
        text .insert (END ,"\n您可以开展工作。")#line:249
        return "...更新成功。"#line:250
def TOOLS_ror_mode1 (O0O0OOOO0O00OO0OO ,OOOOOOOO0O00O00O0 ):#line:267
	O0O000O0OO0O00O00 =[]#line:268
	for O0O00OO0OOO00OO0O in ("事件发生年份","性别","年龄段","报告类型-严重程度","停药减药后反应是否减轻或消失","再次使用可疑药是否出现同样反应","对原患疾病影响","不良反应结果","关联性评价"):#line:269
		O0O0OOOO0O00OO0OO [O0O00OO0OOO00OO0O ]=O0O0OOOO0O00OO0OO [O0O00OO0OOO00OO0O ].astype (str )#line:270
		O0O0OOOO0O00OO0OO [O0O00OO0OOO00OO0O ]=O0O0OOOO0O00OO0OO [O0O00OO0OOO00OO0O ].fillna ("不详")#line:271
		O0000000O000OO0OO =0 #line:273
		for OO0OOOO00OO00OOOO in O0O0OOOO0O00OO0OO [OOOOOOOO0O00O00O0 ].drop_duplicates ():#line:274
			O0000000O000OO0OO =O0000000O000OO0OO +1 #line:275
			O000OOO0000O00O00 =O0O0OOOO0O00OO0OO [(O0O0OOOO0O00OO0OO [OOOOOOOO0O00O00O0 ]==OO0OOOO00OO00OOOO )].copy ()#line:276
			O00OOO0000OOOO0O0 =str (OO0OOOO00OO00OOOO )+"计数"#line:278
			OO0O00OOO0OOO0OOO =str (OO0OOOO00OO00OOOO )+"构成比(%)"#line:279
			OOO00000000OO00O0 =O000OOO0000O00O00 .groupby (O0O00OO0OOO00OO0O ).agg (计数 =("报告编码","nunique")).sort_values (by =O0O00OO0OOO00OO0O ,ascending =[True ],na_position ="last").reset_index ()#line:280
			OOO00000000OO00O0 [OO0O00OOO0OOO0OOO ]=round (100 *OOO00000000OO00O0 ["计数"]/OOO00000000OO00O0 ["计数"].sum (),2 )#line:281
			OOO00000000OO00O0 =OOO00000000OO00O0 .rename (columns ={O0O00OO0OOO00OO0O :"项目"})#line:282
			OOO00000000OO00O0 =OOO00000000OO00O0 .rename (columns ={"计数":O00OOO0000OOOO0O0 })#line:283
			if O0000000O000OO0OO >1 :#line:284
				OO000OOO00OO000OO =pd .merge (OO000OOO00OO000OO ,OOO00000000OO00O0 ,on =["项目"],how ="outer")#line:285
			else :#line:286
				OO000OOO00OO000OO =OOO00000000OO00O0 .copy ()#line:287
		OO000OOO00OO000OO ["类别"]=O0O00OO0OOO00OO0O #line:289
		O0O000O0OO0O00O00 .append (OO000OOO00OO000OO .copy ().reset_index (drop =True ))#line:290
	OO0OO00O00000OO0O =pd .concat (O0O000O0OO0O00O00 ,ignore_index =True ).fillna (0 )#line:293
	OO0OO00O00000OO0O ["报表类型"]="KETI"#line:294
	TABLE_tree_Level_2 (OO0OO00O00000OO0O ,1 ,OO0OO00O00000OO0O )#line:295
def TOOLS_ror_mode2 (OO00O0O0000000OOO ,OO0000OOO0000O0OO ):#line:297
	O000OO0OOO00OO00O =Countall (OO00O0O0000000OOO ).df_ror (["产品类别","产品名称"]).reset_index ()#line:298
	O000OO0OOO00OO00O ["四分表"]=O000OO0OOO00OO00O ["四分表"].str .replace ("(","")#line:299
	O000OO0OOO00OO00O ["四分表"]=O000OO0OOO00OO00O ["四分表"].str .replace (")","")#line:300
	O000OO0OOO00OO00O ["ROR信号（0-否，1-是）"]=0 #line:301
	O000OO0OOO00OO00O ["PRR信号（0-否，1-是）"]=0 #line:302
	for O00OO00O00OOO0OOO ,OO00OOOOO0O0OOOO0 in O000OO0OOO00OO00O .iterrows ():#line:303
		OO0OO0OO00OOOO0OO =tuple (OO00OOOOO0O0OOOO0 ["四分表"].split (","))#line:304
		O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"a"]=int (OO0OO0OO00OOOO0OO [0 ])#line:305
		O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"b"]=int (OO0OO0OO00OOOO0OO [1 ])#line:306
		O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"c"]=int (OO0OO0OO00OOOO0OO [2 ])#line:307
		O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"d"]=int (OO0OO0OO00OOOO0OO [3 ])#line:308
		if int (OO0OO0OO00OOOO0OO [1 ])*int (OO0OO0OO00OOOO0OO [2 ])*int (OO0OO0OO00OOOO0OO [3 ])*int (OO0OO0OO00OOOO0OO [0 ])==0 :#line:309
			O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"分母核验"]=1 #line:310
		if OO00OOOOO0O0OOOO0 ['ROR值的95%CI下限']>1 and OO00OOOOO0O0OOOO0 ['出现频次']>=3 :#line:311
			O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"ROR信号（0-否，1-是）"]=1 #line:312
		if OO00OOOOO0O0OOOO0 ['PRR值的95%CI下限']>1 and OO00OOOOO0O0OOOO0 ['出现频次']>=3 :#line:313
			O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"PRR信号（0-否，1-是）"]=1 #line:314
		O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"事件分类"]=str (TOOLS_get_list (O000OO0OOO00OO00O .loc [O00OO00O00OOO0OOO ,"特定关键字"])[0 ])#line:315
	O000OO0OOO00OO00O =pd .pivot_table (O000OO0OOO00OO00O ,values =["出现频次",'ROR值',"ROR值的95%CI下限","ROR信号（0-否，1-是）",'PRR值',"PRR值的95%CI下限","PRR信号（0-否，1-是）","a","b","c","d","分母核验","风险评分"],index ='事件分类',columns ="产品名称",aggfunc ='sum').reset_index ().fillna (0 )#line:317
	try :#line:320
		O0O0OO0O0OOO0O00O =peizhidir +"0（范例）比例失衡关键字库.xls"#line:321
		if "报告类型-新的"in OO00O0O0000000OOO .columns :#line:322
			O000OO0OO0O0OO000 ="药品"#line:323
		else :#line:324
			O000OO0OO0O0OO000 ="器械"#line:325
		O000O00OOOO000OOO =pd .read_excel (O0O0OO0O0OOO0O00O ,header =0 ,sheet_name =O000OO0OO0O0OO000 ).reset_index (drop =True )#line:326
	except :#line:327
		pass #line:328
	for O00OO00O00OOO0OOO ,OO00OOOOO0O0OOOO0 in O000O00OOOO000OOO .iterrows ():#line:330
		O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"].str .contains (OO00OOOOO0O0OOOO0 ["值"],na =False ),"器官系统损害"]=TOOLS_get_list (OO00OOOOO0O0OOOO0 ["值"])[0 ]#line:331
	try :#line:334
		OOO0O00O000OO0O0O =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:335
		try :#line:336
			O000000000000O0O0 =pd .read_excel (OOO0O00O000OO0O0O ,sheet_name ="onept",header =0 ,index_col =0 ).reset_index ()#line:337
		except :#line:338
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:339
		try :#line:341
			O000O00O000O0O0OO =pd .read_excel (OOO0O00O000OO0O0O ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:342
		except :#line:343
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:344
		O000000000000O0O0 =pd .concat ([O000O00O000O0O0OO ,O000000000000O0O0 ],ignore_index =True ).drop_duplicates ("code")#line:346
		O000000000000O0O0 ["code"]=O000000000000O0O0 ["code"].astype (str )#line:347
		O000OO0OOO00OO00O ["事件分类"]=O000OO0OOO00OO00O ["事件分类"].astype (str )#line:348
		O000000000000O0O0 ["事件分类"]=O000000000000O0O0 ["PT"]#line:349
		O0000OOOOO00O0O0O =pd .merge (O000OO0OOO00OO00O ,O000000000000O0O0 ,on =["事件分类"],how ="left")#line:350
		for O00OO00O00OOO0OOO ,OO00OOOOO0O0OOOO0 in O0000OOOOO00O0O0O .iterrows ():#line:351
			O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"]==OO00OOOOO0O0OOOO0 ["事件分类"],"Chinese"]=OO00OOOOO0O0OOOO0 ["Chinese"]#line:352
			O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"]==OO00OOOOO0O0OOOO0 ["事件分类"],"PT"]=OO00OOOOO0O0OOOO0 ["PT"]#line:353
			O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"]==OO00OOOOO0O0OOOO0 ["事件分类"],"HLT"]=OO00OOOOO0O0OOOO0 ["HLT"]#line:354
			O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"]==OO00OOOOO0O0OOOO0 ["事件分类"],"HLGT"]=OO00OOOOO0O0OOOO0 ["HLGT"]#line:355
			O000OO0OOO00OO00O .loc [O000OO0OOO00OO00O ["事件分类"]==OO00OOOOO0O0OOOO0 ["事件分类"],"SOC"]=OO00OOOOO0O0OOOO0 ["SOC"]#line:356
	except :#line:357
		pass #line:358
	data ["报表类型"]="KETI"#line:361
	TABLE_tree_Level_2 (O000OO0OOO00OO00O ,1 ,O000OO0OOO00OO00O )#line:362
def TOOLS_ror_mode3 (O0O0OO000OO0O000O ,OOOO000O0O0OOOO00 ):#line:364
	O0O0OO000OO0O000O ["css"]=0 #line:365
	TOOLS_ror_mode2 (O0O0OO000OO0O000O ,OOOO000O0O0OOOO00 )#line:366
def STAT_pinzhong (OOO0O0O0O000O00OO ,O000OO0O000OO00OO ,OO0OO00OOO000O0OO ):#line:368
	O0O00000OOO0O00O0 =[O000OO0O000OO00OO ]#line:370
	if OO0OO00OOO000O0OO ==-1 :#line:371
		OO0O0OOOO0000OOO0 =OOO0O0O0O000O00OO .drop_duplicates ("报告编码").copy ()#line:372
		OOO0000000OOO00O0 =OO0O0OOOO0000OOO0 .groupby ([O000OO0O000OO00OO ]).agg (计数 =("报告编码","nunique")).sort_values (by =O000OO0O000OO00OO ,ascending =[True ],na_position ="last").reset_index ()#line:373
		OOO0000000OOO00O0 ["构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:374
		OOO0000000OOO00O0 [O000OO0O000OO00OO ]=OOO0000000OOO00O0 [O000OO0O000OO00OO ].astype (str )#line:375
		OOO0000000OOO00O0 ["报表类型"]="dfx_deepview"+"_"+str (O0O00000OOO0O00O0 )#line:376
		TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OO0O0OOOO0000OOO0 )#line:377
	if OO0OO00OOO000O0OO ==1 :#line:379
		OO0O0OOOO0000OOO0 =OOO0O0O0O000O00OO .copy ()#line:380
		OOO0000000OOO00O0 =OO0O0OOOO0000OOO0 .groupby ([O000OO0O000OO00OO ]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:381
		OOO0000000OOO00O0 ["构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:382
		OOO0000000OOO00O0 ["报表类型"]="dfx_deepview"+"_"+str (O0O00000OOO0O00O0 )#line:383
		TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OO0O0OOOO0000OOO0 )#line:384
	if OO0OO00OOO000O0OO ==4 :#line:386
		OO0O0OOOO0000OOO0 =OOO0O0O0O000O00OO .copy ()#line:387
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("好转",na =False ),"不良反应结果2"]="好转"#line:388
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("痊愈",na =False ),"不良反应结果2"]="痊愈"#line:389
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("无进展",na =False ),"不良反应结果2"]="无进展"#line:390
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("死亡",na =False ),"不良反应结果2"]="死亡"#line:391
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("不详",na =False ),"不良反应结果2"]="不详"#line:392
		OO0O0OOOO0000OOO0 .loc [OO0O0OOOO0000OOO0 ["不良反应结果"].str .contains ("未好转",na =False ),"不良反应结果2"]="未好转"#line:393
		OOO0000000OOO00O0 =OO0O0OOOO0000OOO0 .groupby (["不良反应结果2"]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:394
		OOO0000000OOO00O0 ["构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:395
		OOO0000000OOO00O0 ["报表类型"]="dfx_deepview"+"_"+str (["不良反应结果2"])#line:396
		TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OO0O0OOOO0000OOO0 )#line:397
	if OO0OO00OOO000O0OO ==5 :#line:399
		OO0O0OOOO0000OOO0 =OOO0O0O0O000O00OO .copy ()#line:400
		OO0O0OOOO0000OOO0 ["关联性评价汇总"]="("+OO0O0OOOO0000OOO0 ["评价状态"].astype (str )+"("+OO0O0OOOO0000OOO0 ["县评价"].astype (str )+"("+OO0O0OOOO0000OOO0 ["市评价"].astype (str )+"("+OO0O0OOOO0000OOO0 ["省评价"].astype (str )+"("+OO0O0OOOO0000OOO0 ["国家评价"].astype (str )+")"#line:402
		OO0O0OOOO0000OOO0 ["关联性评价汇总"]=OO0O0OOOO0000OOO0 ["关联性评价汇总"].str .replace ("(nan","",regex =False )#line:403
		OO0O0OOOO0000OOO0 ["关联性评价汇总"]=OO0O0OOOO0000OOO0 ["关联性评价汇总"].str .replace ("nan)","",regex =False )#line:404
		OO0O0OOOO0000OOO0 ["关联性评价汇总"]=OO0O0OOOO0000OOO0 ["关联性评价汇总"].str .replace ("nan","",regex =False )#line:405
		OO0O0OOOO0000OOO0 ['最终的关联性评价']=OO0O0OOOO0000OOO0 ["关联性评价汇总"].str .extract ('.*\((.*)\).*',expand =False )#line:406
		OOO0000000OOO00O0 =OO0O0OOOO0000OOO0 .groupby ('最终的关联性评价').agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:407
		OOO0000000OOO00O0 ["构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:408
		OOO0000000OOO00O0 ["报表类型"]="dfx_deepview"+"_"+str (['最终的关联性评价'])#line:409
		TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OO0O0OOOO0000OOO0 )#line:410
	if OO0OO00OOO000O0OO ==0 :#line:412
		OOO0O0O0O000O00OO [O000OO0O000OO00OO ]=OOO0O0O0O000O00OO [O000OO0O000OO00OO ].fillna ("未填写")#line:413
		OOO0O0O0O000O00OO [O000OO0O000OO00OO ]=OOO0O0O0O000O00OO [O000OO0O000OO00OO ].str .replace ("*","",regex =False )#line:414
		O0OO0O0OO0OOOO0O0 ="use("+str (O000OO0O000OO00OO )+").file"#line:415
		OO0O00O0OOO00OO0O =str (Counter (TOOLS_get_list0 (O0OO0O0OO0OOOO0O0 ,OOO0O0O0O000O00OO ,1000 ))).replace ("Counter({","{")#line:416
		OO0O00O0OOO00OO0O =OO0O00O0OOO00OO0O .replace ("})","}")#line:417
		OO0O00O0OOO00OO0O =ast .literal_eval (OO0O00O0OOO00OO0O )#line:418
		OOO0000000OOO00O0 =pd .DataFrame .from_dict (OO0O00O0OOO00OO0O ,orient ="index",columns =["计数"]).reset_index ()#line:419
		OOO0000000OOO00O0 ["构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:421
		OOO0000000OOO00O0 ["报表类型"]="dfx_deepvie2"+"_"+str (O0O00000OOO0O00O0 )#line:422
		TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OOO0O0O0O000O00OO )#line:423
	if OO0OO00OOO000O0OO ==2 or OO0OO00OOO000O0OO ==3 :#line:427
		OOO0O0O0O000O00OO [O000OO0O000OO00OO ]=OOO0O0O0O000O00OO [O000OO0O000OO00OO ].astype (str )#line:428
		OOO0O0O0O000O00OO [O000OO0O000OO00OO ]=OOO0O0O0O000O00OO [O000OO0O000OO00OO ].fillna ("未填写")#line:429
		O0OO0O0OO0OOOO0O0 ="use("+str (O000OO0O000OO00OO )+").file"#line:431
		OO0O00O0OOO00OO0O =str (Counter (TOOLS_get_list0 (O0OO0O0OO0OOOO0O0 ,OOO0O0O0O000O00OO ,1000 ))).replace ("Counter({","{")#line:432
		OO0O00O0OOO00OO0O =OO0O00O0OOO00OO0O .replace ("})","}")#line:433
		OO0O00O0OOO00OO0O =ast .literal_eval (OO0O00O0OOO00OO0O )#line:434
		OOO0000000OOO00O0 =pd .DataFrame .from_dict (OO0O00O0OOO00OO0O ,orient ="index",columns =["计数"]).reset_index ()#line:435
		print ("正在统计，请稍后...")#line:436
		O0OOOO0O0O00O000O =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:437
		try :#line:438
			O0OOOO000000OOOO0 =pd .read_excel (O0OOOO0O0O00O000O ,sheet_name ="simple",header =0 ,index_col =0 ).reset_index ()#line:439
		except :#line:440
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:441
			return 0 #line:442
		try :#line:443
			OO00O00OO0O0O000O =pd .read_excel (O0OOOO0O0O00O000O ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:444
		except :#line:445
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:446
			return 0 #line:447
		O0OOOO000000OOOO0 =pd .concat ([OO00O00OO0O0O000O ,O0OOOO000000OOOO0 ],ignore_index =True ).drop_duplicates ("code")#line:448
		O0OOOO000000OOOO0 ["code"]=O0OOOO000000OOOO0 ["code"].astype (str )#line:449
		OOO0000000OOO00O0 ["index"]=OOO0000000OOO00O0 ["index"].astype (str )#line:450
		OOO0000000OOO00O0 =OOO0000000OOO00O0 .rename (columns ={"index":"code"})#line:452
		OOO0000000OOO00O0 =pd .merge (OOO0000000OOO00O0 ,O0OOOO000000OOOO0 ,on =["code"],how ="left")#line:453
		OOO0000000OOO00O0 ["code构成比(%)"]=round (100 *OOO0000000OOO00O0 ["计数"]/OOO0000000OOO00O0 ["计数"].sum (),2 )#line:454
		O0OO000OOO00O0000 =OOO0000000OOO00O0 .groupby ("SOC").agg (SOC计数 =("计数","sum")).sort_values (by ="SOC计数",ascending =[False ],na_position ="last").reset_index ()#line:455
		O0OO000OOO00O0000 ["soc构成比(%)"]=round (100 *O0OO000OOO00O0000 ["SOC计数"]/O0OO000OOO00O0000 ["SOC计数"].sum (),2 )#line:456
		O0OO000OOO00O0000 ["SOC计数"]=O0OO000OOO00O0000 ["SOC计数"].astype (int )#line:457
		OOO0000000OOO00O0 =pd .merge (OOO0000000OOO00O0 ,O0OO000OOO00O0000 ,on =["SOC"],how ="left")#line:458
		if OO0OO00OOO000O0OO ==3 :#line:460
			O0OO000OOO00O0000 ["具体名称"]=""#line:461
			for O0OO0O0OOOOO0O00O ,O00O0OOOOOO0O00OO in O0OO000OOO00O0000 .iterrows ():#line:462
				OO0O00OO0O0000O0O =""#line:463
				OOOO000O0OO000OO0 =OOO0000000OOO00O0 .loc [OOO0000000OOO00O0 ["SOC"].str .contains (O00O0OOOOOO0O00OO ["SOC"],na =False )].copy ()#line:464
				for O0OOOO0O000OO0O00 ,O00OO00OO0OO0OO0O in OOOO000O0OO000OO0 .iterrows ():#line:465
					OO0O00OO0O0000O0O =OO0O00OO0O0000O0O +str (O00OO00OO0OO0OO0O ["PT"])+"("+str (O00OO00OO0OO0OO0O ["计数"])+")、"#line:466
				O0OO000OOO00O0000 .loc [O0OO0O0OOOOO0O00O ,"具体名称"]=OO0O00OO0O0000O0O #line:467
			O0OO000OOO00O0000 ["报表类型"]="dfx_deepvie2"+"_"+str (["SOC"])#line:468
			TABLE_tree_Level_2 (O0OO000OOO00O0000 ,1 ,OOO0000000OOO00O0 )#line:469
		if OO0OO00OOO000O0OO ==2 :#line:471
			OOO0000000OOO00O0 ["报表类型"]="dfx_deepvie2"+"_"+str (O0O00000OOO0O00O0 )#line:472
			TABLE_tree_Level_2 (OOO0000000OOO00O0 ,1 ,OOO0O0O0O000O00OO )#line:473
	pass #line:476
def DRAW_pre (OOO0O0O0OO0O000O0 ):#line:478
	""#line:479
	OO0O0O00OOOOOOOO0 =list (OOO0O0O0OO0O000O0 ["报表类型"])[0 ].replace ("1","")#line:487
	if "dfx_org监测机构"in OO0O0O00OOOOOOOO0 :#line:489
		OOO0O0O0OO0O000O0 =OOO0O0O0OO0O000O0 [:-1 ]#line:490
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"报告图","监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:491
	elif "dfx_org市级监测机构"in OO0O0O00OOOOOOOO0 :#line:492
		OOO0O0O0OO0O000O0 =OOO0O0O0OO0O000O0 [:-1 ]#line:493
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"报告图","市级监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:494
	elif "dfx_user"in OO0O0O00OOOOOOOO0 :#line:495
		OOO0O0O0OO0O000O0 =OOO0O0O0OO0O000O0 [:-1 ]#line:496
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"报告单位图","单位名称","报告数量","超级托帕斯图(严重伤害数)")#line:497
	elif "dfx_deepview"in OO0O0O00OOOOOOOO0 :#line:500
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"柱状图",OOO0O0O0OO0O000O0 .columns [0 ],"计数","柱状图")#line:501
	elif "dfx_chiyouren"in OO0O0O00OOOOOOOO0 :#line:503
		OOO0O0O0OO0O000O0 =OOO0O0O0OO0O000O0 [:-1 ]#line:504
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及持有人图","上市许可持有人名称","总报告数","超级托帕斯图(总待评价数量)")#line:505
	elif "dfx_zhenghao"in OO0O0O00OOOOOOOO0 :#line:507
		OOO0O0O0OO0O000O0 ["产品"]=OOO0O0O0OO0O000O0 ["产品名称"]+"("+OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"]+")"#line:508
		DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及产品图","产品","证号计数","超级托帕斯图(严重伤害数)")#line:509
	elif "dfx_pihao"in OO0O0O00OOOOOOOO0 :#line:511
		if len (OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:512
			OOO0O0O0OO0O000O0 ["产品"]=OOO0O0O0OO0O000O0 ["产品名称"]+"("+OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"]+"--"+OOO0O0O0OO0O000O0 ["产品批号"]+")"#line:513
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及批号图","产品","批号计数","超级托帕斯图(严重伤害数)")#line:514
		else :#line:515
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及批号图","产品批号","批号计数","超级托帕斯图(严重伤害数)")#line:516
	elif "dfx_xinghao"in OO0O0O00OOOOOOOO0 :#line:518
		if len (OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:519
			OOO0O0O0OO0O000O0 ["产品"]=OOO0O0O0OO0O000O0 ["产品名称"]+"("+OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"]+"--"+OOO0O0O0OO0O000O0 ["型号"]+")"#line:520
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及型号图","产品","型号计数","超级托帕斯图(严重伤害数)")#line:521
		else :#line:522
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及型号图","型号","型号计数","超级托帕斯图(严重伤害数)")#line:523
	elif "dfx_guige"in OO0O0O00OOOOOOOO0 :#line:525
		if len (OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:526
			OOO0O0O0OO0O000O0 ["产品"]=OOO0O0O0OO0O000O0 ["产品名称"]+"("+OOO0O0O0OO0O000O0 ["注册证编号/曾用注册证编号"]+"--"+OOO0O0O0OO0O000O0 ["规格"]+")"#line:527
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及规格图","产品","规格计数","超级托帕斯图(严重伤害数)")#line:528
		else :#line:529
			DRAW_make_one (OOO0O0O0OO0O000O0 ,"涉及规格图","规格","规格计数","超级托帕斯图(严重伤害数)")#line:530
	elif "PSUR"in OO0O0O00OOOOOOOO0 :#line:532
		DRAW_make_mutibar (OOO0O0O0OO0O000O0 ,"总数量","严重","事件分类","总数量","严重","表现分类统计图")#line:533
	elif "keyword_findrisk"in OO0O0O00OOOOOOOO0 :#line:535
		OOOOOOOOOO00OOOOO =OOO0O0O0OO0O000O0 .columns .to_list ()#line:537
		O0OO0000OOO00O00O =OOOOOOOOOO00OOOOO [OOOOOOOOOO00OOOOO .index ("关键字")+1 ]#line:538
		O0O0OOOO0OO000000 =pd .pivot_table (OOO0O0O0OO0O000O0 ,index =O0OO0000OOO00O00O ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:549
		O0O0OOOO0OO000000 .columns =O0O0OOOO0OO000000 .columns .droplevel (0 )#line:550
		O0O0OOOO0OO000000 =O0O0OOOO0OO000000 [:-1 ].reset_index ()#line:551
		O0O0OOOO0OO000000 =pd .merge (O0O0OOOO0OO000000 ,OOO0O0O0OO0O000O0 [[O0OO0000OOO00O00O ,"该元素总数量"]].drop_duplicates (O0OO0000OOO00O00O ),on =[O0OO0000OOO00O00O ],how ="left")#line:553
		del O0O0OOOO0OO000000 ["All"]#line:555
		DRAW_make_risk_plot (O0O0OOOO0OO000000 ,O0OO0000OOO00O00O ,[OO0O0000OOOO0O00O for OO0O0000OOOO0O00O in O0O0OOOO0OO000000 .columns if OO0O0000OOOO0O00O !=O0OO0000OOO00O00O ],"关键字趋势图",100 )#line:560
def DRAW_make_risk_plot (OO00O0O0OO000OO0O ,OOOO000O0O000OOOO ,O0000OOOO0OO0OO0O ,O00O00OO000O0OO00 ,O0OO0OOO0O00OO00O ):#line:565
    ""#line:566
    OO0O0000OO0OO0O00 =Toplevel ()#line:569
    OO0O0000OO0OO0O00 .title (O00O00OO000O0OO00 )#line:570
    OOO0000OO0O00O0OO =ttk .Frame (OO0O0000OO0OO0O00 ,height =20 )#line:571
    OOO0000OO0O00O0OO .pack (side =TOP )#line:572
    OOO0OO000O000000O =Figure (figsize =(12 ,6 ),dpi =100 )#line:574
    O00OO0OOOO00OO00O =FigureCanvasTkAgg (OOO0OO000O000000O ,master =OO0O0000OO0OO0O00 )#line:575
    O00OO0OOOO00OO00O .draw ()#line:576
    O00OO0OOOO00OO00O .get_tk_widget ().pack (expand =1 )#line:577
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:579
    plt .rcParams ['axes.unicode_minus']=False #line:580
    OOO000OO000000O00 =NavigationToolbar2Tk (O00OO0OOOO00OO00O ,OO0O0000OO0OO0O00 )#line:582
    OOO000OO000000O00 .update ()#line:583
    O00OO0OOOO00OO00O .get_tk_widget ().pack ()#line:584
    OOOOOO0O000OOO000 =OOO0OO000O000000O .add_subplot (111 )#line:586
    OOOOOO0O000OOO000 .set_title (O00O00OO000O0OO00 )#line:588
    O000O00O000O0OO00 =OO00O0O0OO000OO0O [OOOO000O0O000OOOO ]#line:589
    if O0OO0OOO0O00OO00O !=999 :#line:592
        OOOOOO0O000OOO000 .set_xticklabels (O000O00O000O0OO00 ,rotation =-90 ,fontsize =8 )#line:593
    O0O00OO0O0OO00OOO =range (0 ,len (O000O00O000O0OO00 ),1 )#line:596
    try :#line:601
        OOOOOO0O000OOO000 .bar (O000O00O000O0OO00 ,OO00O0O0OO000OO0O ["报告总数"],color ='skyblue',label ="报告总数")#line:602
        OOOOOO0O000OOO000 .bar (O000O00O000O0OO00 ,height =OO00O0O0OO000OO0O ["严重伤害数"],color ="orangered",label ="严重伤害数")#line:603
    except :#line:604
        pass #line:605
    for OO0000OOOOOOOO00O in O0000OOOO0OO0OO0O :#line:608
        O0000O0000O0O0OO0 =OO00O0O0OO000OO0O [OO0000OOOOOOOO00O ].astype (float )#line:609
        if OO0000OOOOOOOO00O =="关注区域":#line:611
            OOOOOO0O000OOO000 .plot (list (O000O00O000O0OO00 ),list (O0000O0000O0O0OO0 ),label =str (OO0000OOOOOOOO00O ),color ="red")#line:612
        else :#line:613
            OOOOOO0O000OOO000 .plot (list (O000O00O000O0OO00 ),list (O0000O0000O0O0OO0 ),label =str (OO0000OOOOOOOO00O ))#line:614
        if O0OO0OOO0O00OO00O ==100 :#line:617
            for O00O0O000O00O0O0O ,OOO0000O000O0OO00 in zip (O000O00O000O0OO00 ,O0000O0000O0O0OO0 ):#line:618
                if OOO0000O000O0OO00 ==max (O0000O0000O0O0OO0 )and OOO0000O000O0OO00 >=3 :#line:619
                     OOOOOO0O000OOO000 .text (O00O0O000O00O0O0O ,OOO0000O000O0OO00 ,(str (OO0000OOOOOOOO00O )+":"+str (int (OOO0000O000O0OO00 ))),color ='black',size =8 )#line:620
    if len (O0000OOOO0OO0OO0O )==1 :#line:630
        O00O0O0OO00OO0000 =OO00O0O0OO000OO0O [O0000OOOO0OO0OO0O ].astype (float ).values #line:631
        OOO0O0O00000OOO0O =O00O0O0OO00OO0000 .mean ()#line:632
        O0O0O0O0OO00OOOOO =O00O0O0OO00OO0000 .std ()#line:633
        OO0OO0O0OO000OO00 =OOO0O0O00000OOO0O +3 *O0O0O0O0OO00OOOOO #line:634
        O000O000O0O00O00O =O0O0O0O0OO00OOOOO -3 *O0O0O0O0OO00OOOOO #line:635
        OOOOOO0O000OOO000 .axhline (OOO0O0O00000OOO0O ,color ='r',linestyle ='--',label ='Mean')#line:637
        OOOOOO0O000OOO000 .axhline (OO0OO0O0OO000OO00 ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:638
        OOOOOO0O000OOO000 .axhline (O000O000O0O00O00O ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:639
    OOOOOO0O000OOO000 .set_title ("曲线图")#line:643
    OOOOOO0O000OOO000 .set_xlabel ("项")#line:644
    OOO0OO000O000000O .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:645
    O0000O0000O000000 =OOOOOO0O000OOO000 .get_position ()#line:646
    OOOOOO0O000OOO000 .set_position ([O0000O0000O000000 .x0 ,O0000O0000O000000 .y0 ,O0000O0000O000000 .width *0.7 ,O0000O0000O000000 .height ])#line:647
    OOOOOO0O000OOO000 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:648
    O00OOO000O0OO0O0O =StringVar ()#line:672
    OOOO0000OOO00000O =ttk .Combobox (OOO0000OO0O00O0OO ,width =15 ,textvariable =O00OOO000O0OO0O0O ,state ='readonly')#line:673
    OOOO0000OOO00000O ['values']=O0000OOOO0OO0OO0O #line:674
    OOOO0000OOO00000O .pack (side =LEFT )#line:675
    OOOO0000OOO00000O .current (0 )#line:676
    O00OO00O000O0OO0O =Button (OOO0000OO0O00O0OO ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OO00O0O0OO000OO0O ,OOOO000O0O000OOOO ,[OOOOO00O000O0OO00 for OOOOO00O000O0OO00 in O0000OOOO0OO0OO0O if O00OOO000O0OO0O0O .get ()in OOOOO00O000O0OO00 ],O00O00OO000O0OO00 ,O0OO0OOO0O00OO00O ))#line:684
    O00OO00O000O0OO0O .pack (side =LEFT ,anchor ="ne")#line:685
    OO0O0OO0O00O00O0O =Button (OOO0000OO0O00O0OO ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (OO00O0O0OO000OO0O ,OOOO000O0O000OOOO ,O0000OOOO0OO0OO0O ,O00O00OO000O0OO00 ,0 ))#line:693
    OO0O0OO0O00O00O0O .pack (side =LEFT ,anchor ="ne")#line:694
    O00OO0OOOO00OO00O .draw ()#line:696
def DRAW_make_one (OOO0OO0O0000OO0O0 ,O00O0O0OOOOOOO000 ,OO00O00O0O0OO00O0 ,OOO000OOO0O0OOOO0 ,OOO0OO0O000OO00O0 ):#line:699
    ""#line:700
    warnings .filterwarnings ("ignore")#line:701
    O0OOOOO00OO0000OO =Toplevel ()#line:702
    O0OOOOO00OO0000OO .title (O00O0O0OOOOOOO000 )#line:703
    OO000OOOO0OO0000O =ttk .Frame (O0OOOOO00OO0000OO ,height =20 )#line:704
    OO000OOOO0OO0000O .pack (side =TOP )#line:705
    O00OO00OO0000OOO0 =Figure (figsize =(12 ,6 ),dpi =100 )#line:707
    O00000O000O000000 =FigureCanvasTkAgg (O00OO00OO0000OOO0 ,master =O0OOOOO00OO0000OO )#line:708
    O00000O000O000000 .draw ()#line:709
    O00000O000O000000 .get_tk_widget ().pack (expand =1 )#line:710
    O000O00O0O0O00O0O =O00OO00OO0000OOO0 .add_subplot (111 )#line:711
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:713
    plt .rcParams ['axes.unicode_minus']=False #line:714
    OOOOOOOO0O0O0O00O =NavigationToolbar2Tk (O00000O000O000000 ,O0OOOOO00OO0000OO )#line:716
    OOOOOOOO0O0O0O00O .update ()#line:717
    O00000O000O000000 .get_tk_widget ().pack ()#line:719
    try :#line:722
        O0OOO0O0OOO0O0O0O =OOO0OO0O0000OO0O0 .columns #line:723
        OOO0OO0O0000OO0O0 =OOO0OO0O0000OO0O0 .sort_values (by =OOO000OOO0O0OOOO0 ,ascending =[False ],na_position ="last")#line:724
    except :#line:725
        O0OO000O00OO000O0 =eval (OOO0OO0O0000OO0O0 )#line:726
        O0OO000O00OO000O0 =pd .DataFrame .from_dict (O0OO000O00OO000O0 ,orient =OO00O00O0O0OO00O0 ,columns =[OOO000OOO0O0OOOO0 ]).reset_index ()#line:729
        OOO0OO0O0000OO0O0 =O0OO000O00OO000O0 .sort_values (by =OOO000OOO0O0OOOO0 ,ascending =[False ],na_position ="last")#line:730
    if ("日期"in O00O0O0OOOOOOO000 or "时间"in O00O0O0OOOOOOO000 or "季度"in O00O0O0OOOOOOO000 )and "饼图"not in OOO0OO0O000OO00O0 :#line:734
        OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ]=pd .to_datetime (OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],format ="%Y/%m/%d").dt .date #line:735
        OOO0OO0O0000OO0O0 =OOO0OO0O0000OO0O0 .sort_values (by =OO00O00O0O0OO00O0 ,ascending =[True ],na_position ="last")#line:736
    elif "批号"in O00O0O0OOOOOOO000 :#line:737
        OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ]=OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ].astype (str )#line:738
        OOO0OO0O0000OO0O0 =OOO0OO0O0000OO0O0 .sort_values (by =OO00O00O0O0OO00O0 ,ascending =[True ],na_position ="last")#line:739
        O000O00O0O0O00O0O .set_xticklabels (OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],rotation =-90 ,fontsize =8 )#line:740
    else :#line:741
        OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ]=OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ].astype (str )#line:742
        O000O00O0O0O00O0O .set_xticklabels (OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],rotation =-90 ,fontsize =8 )#line:743
    O00OO0OOO0OOO00OO =OOO0OO0O0000OO0O0 [OOO000OOO0O0OOOO0 ]#line:745
    OO0OO00O00OO0OO00 =range (0 ,len (O00OO0OOO0OOO00OO ),1 )#line:746
    O000O00O0O0O00O0O .set_title (O00O0O0OOOOOOO000 )#line:748
    if OOO0OO0O000OO00O0 =="柱状图":#line:752
        O000O00O0O0O00O0O .bar (x =OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],height =O00OO0OOO0OOO00OO ,width =0.2 ,color ="#87CEFA")#line:753
    elif OOO0OO0O000OO00O0 =="饼图":#line:754
        O000O00O0O0O00O0O .pie (x =O00OO0OOO0OOO00OO ,labels =OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],autopct ="%0.2f%%")#line:755
    elif OOO0OO0O000OO00O0 =="折线图":#line:756
        O000O00O0O0O00O0O .plot (OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],O00OO0OOO0OOO00OO ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:757
    elif "托帕斯图"in str (OOO0OO0O000OO00O0 ):#line:759
        OO00OOOOOOO0O0O0O =OOO0OO0O0000OO0O0 [OOO000OOO0O0OOOO0 ].fillna (0 )#line:760
        O00O00OOO0OOO0O00 =OO00OOOOOOO0O0O0O .cumsum ()/OO00OOOOOOO0O0O0O .sum ()*100 #line:764
        OO00OOOO0OOO00OO0 =O00O00OOO0OOO0O00 [O00O00OOO0OOO0O00 >0.8 ].index [0 ]#line:766
        O00000OO00O00O0O0 =OO00OOOOOOO0O0O0O .index .tolist ().index (OO00OOOO0OOO00OO0 )#line:767
        O000O00O0O0O00O0O .bar (x =OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],height =OO00OOOOOOO0O0O0O ,color ="C0",label =OOO000OOO0O0OOOO0 )#line:771
        O000O000000000O00 =O000O00O0O0O00O0O .twinx ()#line:772
        O000O000000000O00 .plot (OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],O00O00OOO0OOO0O00 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:773
        O000O000000000O00 .yaxis .set_major_formatter (PercentFormatter ())#line:774
        O000O00O0O0O00O0O .tick_params (axis ="y",colors ="C0")#line:779
        O000O000000000O00 .tick_params (axis ="y",colors ="C1")#line:780
        if "超级托帕斯图"in str (OOO0OO0O000OO00O0 ):#line:783
            O0OOOO0O0OO0OOO0O =re .compile (r'[(](.*?)[)]',re .S )#line:784
            OO0OOOOOO000O00OO =re .findall (O0OOOO0O0OO0OOO0O ,OOO0OO0O000OO00O0 )[0 ]#line:785
            O000O00O0O0O00O0O .bar (x =OOO0OO0O0000OO0O0 [OO00O00O0O0OO00O0 ],height =OOO0OO0O0000OO0O0 [OO0OOOOOO000O00OO ],color ="orangered",label =OO0OOOOOO000O00OO )#line:786
    O00OO00OO0000OOO0 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:788
    OO0O0O0OO0O00OO00 =O000O00O0O0O00O0O .get_position ()#line:789
    O000O00O0O0O00O0O .set_position ([OO0O0O0OO0O00OO00 .x0 ,OO0O0O0OO0O00OO00 .y0 ,OO0O0O0OO0O00OO00 .width *0.7 ,OO0O0O0OO0O00OO00 .height ])#line:790
    O000O00O0O0O00O0O .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:791
    O00000O000O000000 .draw ()#line:794
    if len (O00OO0OOO0OOO00OO )<=20 and OOO0OO0O000OO00O0 !="饼图":#line:797
        for OO0OOO00OOO0OOO0O ,OO000000000000OO0 in zip (OO0OO00O00OO0OO00 ,O00OO0OOO0OOO00OO ):#line:798
            OOOOO000O0OOOO000 =str (OO000000000000OO0 )#line:799
            OOOO0000OOO000OOO =(OO0OOO00OOO0OOO0O ,OO000000000000OO0 +0.3 )#line:800
            O000O00O0O0O00O0O .annotate (OOOOO000O0OOOO000 ,xy =OOOO0000OOO000OOO ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:801
    O0O0O0OO000000OO0 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OOO0OO0O0000OO0O0 ),)#line:811
    O0O0O0OO000000OO0 .pack (side =RIGHT )#line:812
    O0OOOO0000O00O0O0 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,text ="查看原始数据",command =lambda :TOOLS_view_dict (OOO0OO0O0000OO0O0 ,0 ))#line:816
    O0OOOO0000O00O0O0 .pack (side =RIGHT )#line:817
    O0O00O000O000O000 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,text ="饼图",command =lambda :DRAW_make_one (OOO0OO0O0000OO0O0 ,O00O0O0OOOOOOO000 ,OO00O00O0O0OO00O0 ,OOO000OOO0O0OOOO0 ,"饼图"),)#line:825
    O0O00O000O000O000 .pack (side =LEFT )#line:826
    O0O00O000O000O000 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,text ="柱状图",command =lambda :DRAW_make_one (OOO0OO0O0000OO0O0 ,O00O0O0OOOOOOO000 ,OO00O00O0O0OO00O0 ,OOO000OOO0O0OOOO0 ,"柱状图"),)#line:833
    O0O00O000O000O000 .pack (side =LEFT )#line:834
    O0O00O000O000O000 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,text ="折线图",command =lambda :DRAW_make_one (OOO0OO0O0000OO0O0 ,O00O0O0OOOOOOO000 ,OO00O00O0O0OO00O0 ,OOO000OOO0O0OOOO0 ,"折线图"),)#line:840
    O0O00O000O000O000 .pack (side =LEFT )#line:841
    O0O00O000O000O000 =Button (OO000OOOO0OO0000O ,relief =GROOVE ,text ="托帕斯图",command =lambda :DRAW_make_one (OOO0OO0O0000OO0O0 ,O00O0O0OOOOOOO000 ,OO00O00O0O0OO00O0 ,OOO000OOO0O0OOOO0 ,"托帕斯图"),)#line:848
    O0O00O000O000O000 .pack (side =LEFT )#line:849
def DRAW_make_mutibar (O00O00OOOOO000000 ,O00O0O000O0O0O000 ,O00000000O000O00O ,OO0OOO00O00O0O0O0 ,OO0000OOOOO0OOO0O ,OO0O00OOO00OO000O ,O00O0O0OOOO0O00OO ):#line:850
    ""#line:851
    O0O0OO0O00O0OO00O =Toplevel ()#line:852
    O0O0OO0O00O0OO00O .title (O00O0O0OOOO0O00OO )#line:853
    OOOO0OOOO0O00OO0O =ttk .Frame (O0O0OO0O00O0OO00O ,height =20 )#line:854
    OOOO0OOOO0O00OO0O .pack (side =TOP )#line:855
    OOO0OO0OOOO0OOO0O =0.2 #line:857
    OOO0O00O00OO0O0OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:858
    OO00O0O0O00OO00OO =FigureCanvasTkAgg (OOO0O00O00OO0O0OO ,master =O0O0OO0O00O0OO00O )#line:859
    OO00O0O0O00OO00OO .draw ()#line:860
    OO00O0O0O00OO00OO .get_tk_widget ().pack (expand =1 )#line:861
    O0O0OOOOO000OOOO0 =OOO0O00O00OO0O0OO .add_subplot (111 )#line:862
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:864
    plt .rcParams ['axes.unicode_minus']=False #line:865
    OOO0OOOO0OOOO0O0O =NavigationToolbar2Tk (OO00O0O0O00OO00OO ,O0O0OO0O00O0OO00O )#line:867
    OOO0OOOO0OOOO0O0O .update ()#line:868
    OO00O0O0O00OO00OO .get_tk_widget ().pack ()#line:870
    O00O0O000O0O0O000 =O00O00OOOOO000000 [O00O0O000O0O0O000 ]#line:871
    O00000000O000O00O =O00O00OOOOO000000 [O00000000O000O00O ]#line:872
    OO0OOO00O00O0O0O0 =O00O00OOOOO000000 [OO0OOO00O00O0O0O0 ]#line:873
    OO00O00O00O000OOO =range (0 ,len (O00O0O000O0O0O000 ),1 )#line:875
    O0O0OOOOO000OOOO0 .set_xticklabels (OO0OOO00O00O0O0O0 ,rotation =-90 ,fontsize =8 )#line:876
    O0O0OOOOO000OOOO0 .bar (OO00O00O00O000OOO ,O00O0O000O0O0O000 ,align ="center",tick_label =OO0OOO00O00O0O0O0 ,label =OO0000OOOOO0OOO0O )#line:879
    O0O0OOOOO000OOOO0 .bar (OO00O00O00O000OOO ,O00000000O000O00O ,align ="center",label =OO0O00OOO00OO000O )#line:882
    O0O0OOOOO000OOOO0 .set_title (O00O0O0OOOO0O00OO )#line:883
    O0O0OOOOO000OOOO0 .set_xlabel ("项")#line:884
    O0O0OOOOO000OOOO0 .set_ylabel ("数量")#line:885
    OOO0O00O00OO0O0OO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:887
    OOO00O0O0O00O0OO0 =O0O0OOOOO000OOOO0 .get_position ()#line:888
    O0O0OOOOO000OOOO0 .set_position ([OOO00O0O0O00O0OO0 .x0 ,OOO00O0O0O00O0OO0 .y0 ,OOO00O0O0O00O0OO0 .width *0.7 ,OOO00O0O0O00O0OO0 .height ])#line:889
    O0O0OOOOO000OOOO0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:890
    OO00O0O0O00OO00OO .draw ()#line:892
    O000O00OOOO0OO0OO =Button (OOOO0OOOO0O00OO0O ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O00O00OOOOO000000 ),)#line:899
    O000O00OOOO0OO0OO .pack (side =RIGHT )#line:900
def CLEAN_hzp (O0O000000000O0O00 ):#line:905
    ""#line:906
    if "报告编码"not in O0O000000000O0O00 .columns :#line:907
            O0O000000000O0O00 ["特殊化妆品注册证书编号/普通化妆品备案编号"]=O0O000000000O0O00 ["特殊化妆品注册证书编号/普通化妆品备案编号"].fillna ("-未填写-")#line:908
            O0O000000000O0O00 ["省级评价结果"]=O0O000000000O0O00 ["省级评价结果"].fillna ("-未填写-")#line:909
            O0O000000000O0O00 ["生产企业"]=O0O000000000O0O00 ["生产企业"].fillna ("-未填写-")#line:910
            O0O000000000O0O00 ["提交人"]="不适用"#line:911
            O0O000000000O0O00 ["医疗机构类别"]="不适用"#line:912
            O0O000000000O0O00 ["经营企业或使用单位"]="不适用"#line:913
            O0O000000000O0O00 ["报告状态"]="报告单位评价"#line:914
            O0O000000000O0O00 ["所属地区"]="不适用"#line:915
            O0O000000000O0O00 ["医院名称"]="不适用"#line:916
            O0O000000000O0O00 ["报告地区名称"]="不适用"#line:917
            O0O000000000O0O00 ["提交人"]="不适用"#line:918
            O0O000000000O0O00 ["型号"]=O0O000000000O0O00 ["化妆品分类"]#line:919
            O0O000000000O0O00 ["关联性评价"]=O0O000000000O0O00 ["上报单位评价结果"]#line:920
            O0O000000000O0O00 ["规格"]="不适用"#line:921
            O0O000000000O0O00 ["器械故障表现"]=O0O000000000O0O00 ["初步判断"]#line:922
            O0O000000000O0O00 ["伤害表现"]=O0O000000000O0O00 ["自觉症状"]+O0O000000000O0O00 ["皮损部位"]+O0O000000000O0O00 ["皮损形态"]#line:923
            O0O000000000O0O00 ["事件原因分析"]="不适用"#line:924
            O0O000000000O0O00 ["事件原因分析描述"]="不适用"#line:925
            O0O000000000O0O00 ["调查情况"]="不适用"#line:926
            O0O000000000O0O00 ["具体控制措施"]="不适用"#line:927
            O0O000000000O0O00 ["未采取控制措施原因"]="不适用"#line:928
            O0O000000000O0O00 ["报告地区名称"]="不适用"#line:929
            O0O000000000O0O00 ["上报单位所属地区"]="不适用"#line:930
            O0O000000000O0O00 ["持有人报告状态"]="不适用"#line:931
            O0O000000000O0O00 ["年龄类型"]="岁"#line:932
            O0O000000000O0O00 ["经营企业使用单位报告状态"]="不适用"#line:933
            O0O000000000O0O00 ["产品归属"]="化妆品"#line:934
            O0O000000000O0O00 ["管理类别"]="不适用"#line:935
            O0O000000000O0O00 ["超时标记"]="不适用"#line:936
            O0O000000000O0O00 =O0O000000000O0O00 .rename (columns ={"报告表编号":"报告编码","报告类型":"伤害","报告地区":"监测机构","报告单位名称":"单位名称","患者/消费者姓名":"姓名","不良反应发生日期":"事件发生日期","过程描述补充说明":"使用过程","化妆品名称":"产品名称","化妆品分类":"产品类别","生产企业":"上市许可持有人名称","生产批号":"产品批号","特殊化妆品注册证书编号/普通化妆品备案编号":"注册证编号/曾用注册证编号",})#line:955
            O0O000000000O0O00 ["时隔"]=pd .to_datetime (O0O000000000O0O00 ["事件发生日期"])-pd .to_datetime (O0O000000000O0O00 ["开始使用日期"])#line:956
            O0O000000000O0O00 .loc [(O0O000000000O0O00 ["省级评价结果"]!="-未填写-"),"有效报告"]=1 #line:957
            O0O000000000O0O00 ["伤害"]=O0O000000000O0O00 ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:958
            try :#line:959
	            O0O000000000O0O00 =TOOL_guizheng (O0O000000000O0O00 ,4 ,True )#line:960
            except :#line:961
                pass #line:962
            return O0O000000000O0O00 #line:963
def CLEAN_yp (OOO00OO0000OOOO00 ):#line:968
    ""#line:969
    if "报告编码"not in OOO00OO0000OOOO00 .columns :#line:970
        if "反馈码"in OOO00OO0000OOOO00 .columns and "报告表编码"not in OOO00OO0000OOOO00 .columns :#line:972
            OOO00OO0000OOOO00 ["提交人"]="不适用"#line:974
            OOO00OO0000OOOO00 ["经营企业或使用单位"]="不适用"#line:975
            OOO00OO0000OOOO00 ["报告状态"]="报告单位评价"#line:976
            OOO00OO0000OOOO00 ["所属地区"]="不适用"#line:977
            OOO00OO0000OOOO00 ["产品类别"]="无源"#line:978
            OOO00OO0000OOOO00 ["医院名称"]="不适用"#line:979
            OOO00OO0000OOOO00 ["报告地区名称"]="不适用"#line:980
            OOO00OO0000OOOO00 ["提交人"]="不适用"#line:981
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"反馈码":"报告表编码","序号":"药品序号","新的":"报告类型-新的","报告类型":"报告类型-严重程度","用药-日数":"用法-日","用药-次数":"用法-次",})#line:994
        if "唯一标识"not in OOO00OO0000OOOO00 .columns :#line:999
            OOO00OO0000OOOO00 ["报告编码"]=OOO00OO0000OOOO00 ["报告表编码"].astype (str )+OOO00OO0000OOOO00 ["患者姓名"].astype (str )#line:1000
        if "唯一标识"in OOO00OO0000OOOO00 .columns :#line:1001
            OOO00OO0000OOOO00 ["唯一标识"]=OOO00OO0000OOOO00 ["唯一标识"].astype (str )#line:1002
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"唯一标识":"报告编码"})#line:1003
        if "医疗机构类别"not in OOO00OO0000OOOO00 .columns :#line:1004
            OOO00OO0000OOOO00 ["医疗机构类别"]="医疗机构"#line:1005
            OOO00OO0000OOOO00 ["经营企业使用单位报告状态"]="已提交"#line:1006
        try :#line:1007
            OOO00OO0000OOOO00 ["年龄和单位"]=OOO00OO0000OOOO00 ["年龄"].astype (str )+OOO00OO0000OOOO00 ["年龄单位"]#line:1008
        except :#line:1009
            OOO00OO0000OOOO00 ["年龄和单位"]=OOO00OO0000OOOO00 ["年龄"].astype (str )+OOO00OO0000OOOO00 ["年龄类型"]#line:1010
        OOO00OO0000OOOO00 .loc [(OOO00OO0000OOOO00 ["报告类型-新的"]=="新的"),"管理类别"]="Ⅲ类"#line:1011
        OOO00OO0000OOOO00 .loc [(OOO00OO0000OOOO00 ["报告类型-严重程度"]=="严重"),"管理类别"]="Ⅲ类"#line:1012
        text .insert (END ,"剔除已删除报告和重复报告...")#line:1013
        if "删除标识"in OOO00OO0000OOOO00 .columns :#line:1014
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 [(OOO00OO0000OOOO00 ["删除标识"]!="删除")]#line:1015
        if "重复报告"in OOO00OO0000OOOO00 .columns :#line:1016
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 [(OOO00OO0000OOOO00 ["重复报告"]!="重复报告")]#line:1017
        OOO00OO0000OOOO00 ["报告类型-新的"]=OOO00OO0000OOOO00 ["报告类型-新的"].fillna (" ")#line:1020
        OOO00OO0000OOOO00 .loc [(OOO00OO0000OOOO00 ["报告类型-严重程度"]=="严重"),"伤害"]="严重伤害"#line:1021
        OOO00OO0000OOOO00 ["伤害"]=OOO00OO0000OOOO00 ["伤害"].fillna ("所有一般")#line:1022
        OOO00OO0000OOOO00 ["伤害PSUR"]=OOO00OO0000OOOO00 ["报告类型-新的"].astype (str )+OOO00OO0000OOOO00 ["报告类型-严重程度"].astype (str )#line:1023
        OOO00OO0000OOOO00 ["用量用量单位"]=OOO00OO0000OOOO00 ["用量"].astype (str )+OOO00OO0000OOOO00 ["用量单位"].astype (str )#line:1024
        OOO00OO0000OOOO00 ["规格"]="不适用"#line:1026
        OOO00OO0000OOOO00 ["事件原因分析"]="不适用"#line:1027
        OOO00OO0000OOOO00 ["事件原因分析描述"]="不适用"#line:1028
        OOO00OO0000OOOO00 ["初步处置情况"]="不适用"#line:1029
        OOO00OO0000OOOO00 ["伤害表现"]=OOO00OO0000OOOO00 ["不良反应名称"]#line:1030
        OOO00OO0000OOOO00 ["产品类别"]="无源"#line:1031
        OOO00OO0000OOOO00 ["调查情况"]="不适用"#line:1032
        OOO00OO0000OOOO00 ["具体控制措施"]="不适用"#line:1033
        OOO00OO0000OOOO00 ["上报单位所属地区"]=OOO00OO0000OOOO00 ["报告地区名称"]#line:1034
        OOO00OO0000OOOO00 ["未采取控制措施原因"]="不适用"#line:1035
        OOO00OO0000OOOO00 ["报告单位评价"]=OOO00OO0000OOOO00 ["报告类型-新的"].astype (str )+OOO00OO0000OOOO00 ["报告类型-严重程度"].astype (str )#line:1036
        OOO00OO0000OOOO00 .loc [(OOO00OO0000OOOO00 ["报告类型-新的"]=="新的"),"持有人报告状态"]="待评价"#line:1037
        OOO00OO0000OOOO00 ["用法temp日"]="日"#line:1038
        OOO00OO0000OOOO00 ["用法temp次"]="次"#line:1039
        OOO00OO0000OOOO00 ["用药频率"]=(OOO00OO0000OOOO00 ["用法-日"].astype (str )+OOO00OO0000OOOO00 ["用法temp日"]+OOO00OO0000OOOO00 ["用法-次"].astype (str )+OOO00OO0000OOOO00 ["用法temp次"])#line:1045
        try :#line:1046
            OOO00OO0000OOOO00 ["相关疾病信息[疾病名称]-术语"]=OOO00OO0000OOOO00 ["原患疾病"]#line:1047
            OOO00OO0000OOOO00 ["治疗适应症-术语"]=OOO00OO0000OOOO00 ["用药原因"]#line:1048
        except :#line:1049
            pass #line:1050
        try :#line:1052
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"提交日期":"报告日期"})#line:1053
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"提交人":"报告人"})#line:1054
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"报告状态":"持有人报告状态"})#line:1055
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"所属地区":"使用单位、经营企业所属监测机构"})#line:1056
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"医院名称":"单位名称"})#line:1057
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"批准文号":"注册证编号/曾用注册证编号"})#line:1058
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"通用名称":"产品名称"})#line:1059
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"生产厂家":"上市许可持有人名称"})#line:1060
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"不良反应发生时间":"事件发生日期"})#line:1061
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"不良反应名称":"器械故障表现"})#line:1062
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"不良反应过程描述":"使用过程"})#line:1063
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"生产批号":"产品批号"})#line:1064
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:1065
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"剂型":"型号"})#line:1066
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"报告人评价":"关联性评价"})#line:1067
            OOO00OO0000OOOO00 =OOO00OO0000OOOO00 .rename (columns ={"年龄单位":"年龄类型"})#line:1068
        except :#line:1069
            text .insert (END ,"数据规整失败。")#line:1070
            return 0 #line:1071
        OOO00OO0000OOOO00 ['报告日期']=OOO00OO0000OOOO00 ['报告日期'].str .strip ()#line:1074
        OOO00OO0000OOOO00 ['事件发生日期']=OOO00OO0000OOOO00 ['事件发生日期'].str .strip ()#line:1075
        OOO00OO0000OOOO00 ['用药开始时间']=OOO00OO0000OOOO00 ['用药开始时间'].str .strip ()#line:1076
        return OOO00OO0000OOOO00 #line:1078
    if "报告编码"in OOO00OO0000OOOO00 .columns :#line:1079
        return OOO00OO0000OOOO00 #line:1080
def CLEAN_qx (OOOO0O00O00O00OO0 ):#line:1082
		""#line:1083
		if "使用单位、经营企业所属监测机构"not in OOOO0O00O00O00OO0 .columns and "监测机构"not in OOOO0O00O00O00OO0 .columns :#line:1085
			OOOO0O00O00O00OO0 ["使用单位、经营企业所属监测机构"]="本地"#line:1086
		if "上市许可持有人名称"not in OOOO0O00O00O00OO0 .columns :#line:1087
			OOOO0O00O00O00OO0 ["上市许可持有人名称"]=OOOO0O00O00O00OO0 ["单位名称"]#line:1088
		if "注册证编号/曾用注册证编号"not in OOOO0O00O00O00OO0 .columns :#line:1089
			OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号"]#line:1090
		if "事件原因分析描述"not in OOOO0O00O00O00OO0 .columns :#line:1091
			OOOO0O00O00O00OO0 ["事件原因分析描述"]="  "#line:1092
		if "初步处置情况"not in OOOO0O00O00O00OO0 .columns :#line:1093
			OOOO0O00O00O00OO0 ["初步处置情况"]="  "#line:1094
		text .insert (END ,"\n正在执行格式规整和增加有关时间、年龄、性别等统计列...")#line:1097
		OOOO0O00O00O00OO0 =OOOO0O00O00O00OO0 .rename (columns ={"使用单位、经营企业所属监测机构":"监测机构"})#line:1098
		OOOO0O00O00O00OO0 ["报告编码"]=OOOO0O00O00O00OO0 ["报告编码"].astype ("str")#line:1099
		OOOO0O00O00O00OO0 ["产品批号"]=OOOO0O00O00O00OO0 ["产品批号"].astype ("str")#line:1100
		OOOO0O00O00O00OO0 ["型号"]=OOOO0O00O00O00OO0 ["型号"].astype ("str")#line:1101
		OOOO0O00O00O00OO0 ["规格"]=OOOO0O00O00O00OO0 ["规格"].astype ("str")#line:1102
		OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1103
		OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1104
		OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1105
		OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1106
		OOOO0O00O00O00OO0 ["产品名称"]=OOOO0O00O00O00OO0 ["产品名称"].str .replace ("*","※",regex =False )#line:1107
		OOOO0O00O00O00OO0 ["产品批号"]=OOOO0O00O00O00OO0 ["产品批号"].str .replace ("(","（",regex =False )#line:1108
		OOOO0O00O00O00OO0 ["产品批号"]=OOOO0O00O00O00OO0 ["产品批号"].str .replace (")","）",regex =False )#line:1109
		OOOO0O00O00O00OO0 ["产品批号"]=OOOO0O00O00O00OO0 ["产品批号"].str .replace ("*","※",regex =False )#line:1110
		OOOO0O00O00O00OO0 ["伤害与评价"]=OOOO0O00O00O00OO0 ["伤害"]+OOOO0O00O00O00OO0 ["持有人报告状态"]#line:1113
		OOOO0O00O00O00OO0 ["注册证备份"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]#line:1114
		OOOO0O00O00O00OO0 ['报告日期']=pd .to_datetime (OOOO0O00O00O00OO0 ['报告日期'],format ='%Y-%m-%d',errors ='coerce')#line:1117
		OOOO0O00O00O00OO0 ['事件发生日期']=pd .to_datetime (OOOO0O00O00O00OO0 ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1118
		OOOO0O00O00O00OO0 ["报告月份"]=OOOO0O00O00O00OO0 ["报告日期"].dt .to_period ("M").astype (str )#line:1120
		OOOO0O00O00O00OO0 ["报告季度"]=OOOO0O00O00O00OO0 ["报告日期"].dt .to_period ("Q").astype (str )#line:1121
		OOOO0O00O00O00OO0 ["报告年份"]=OOOO0O00O00O00OO0 ["报告日期"].dt .to_period ("Y").astype (str )#line:1122
		OOOO0O00O00O00OO0 ["事件发生月份"]=OOOO0O00O00O00OO0 ["事件发生日期"].dt .to_period ("M").astype (str )#line:1123
		OOOO0O00O00O00OO0 ["事件发生季度"]=OOOO0O00O00O00OO0 ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1124
		OOOO0O00O00O00OO0 ["事件发生年份"]=OOOO0O00O00O00OO0 ["事件发生日期"].dt .to_period ("Y").astype (str )#line:1125
		if ini ["模式"]=="器械":#line:1129
			OOOO0O00O00O00OO0 ['发现或获知日期']=pd .to_datetime (OOOO0O00O00O00OO0 ['发现或获知日期'],format ='%Y-%m-%d',errors ='coerce')#line:1130
			OOOO0O00O00O00OO0 ["时隔"]=pd .to_datetime (OOOO0O00O00O00OO0 ["发现或获知日期"])-pd .to_datetime (OOOO0O00O00O00OO0 ["事件发生日期"])#line:1131
			OOOO0O00O00O00OO0 ["报告时限"]=pd .to_datetime (OOOO0O00O00O00OO0 ["报告日期"])-pd .to_datetime (OOOO0O00O00O00OO0 ["发现或获知日期"])#line:1132
			OOOO0O00O00O00OO0 ["报告时限"]=OOOO0O00O00O00OO0 ["报告时限"].dt .days #line:1133
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>20 )&(OOOO0O00O00O00OO0 ["伤害"]=="严重伤害"),"超时标记"]=1 #line:1134
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>30 )&(OOOO0O00O00O00OO0 ["伤害"]=="其他"),"超时标记"]=1 #line:1135
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>7 )&(OOOO0O00O00O00OO0 ["伤害"]=="死亡"),"超时标记"]=1 #line:1136
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["经营企业使用单位报告状态"]=="审核通过"),"有效报告"]=1 #line:1138
		if ini ["模式"]=="药品":#line:1141
			OOOO0O00O00O00OO0 ['用药开始时间']=pd .to_datetime (OOOO0O00O00O00OO0 ['用药开始时间'],format ='%Y-%m-%d',errors ='coerce')#line:1142
			OOOO0O00O00O00OO0 ["时隔"]=pd .to_datetime (OOOO0O00O00O00OO0 ["事件发生日期"])-pd .to_datetime (OOOO0O00O00O00OO0 ["用药开始时间"])#line:1143
			OOOO0O00O00O00OO0 ["报告时限"]=pd .to_datetime (OOOO0O00O00O00OO0 ["报告日期"])-pd .to_datetime (OOOO0O00O00O00OO0 ["事件发生日期"])#line:1144
			OOOO0O00O00O00OO0 ["报告时限"]=OOOO0O00O00O00OO0 ["报告时限"].dt .days #line:1145
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>15 )&(OOOO0O00O00O00OO0 ["报告类型-严重程度"]=="严重"),"超时标记"]=1 #line:1146
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>30 )&(OOOO0O00O00O00OO0 ["报告类型-严重程度"]=="一般"),"超时标记"]=1 #line:1147
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>15 )&(OOOO0O00O00O00OO0 ["报告类型-新的"]=="新的"),"超时标记"]=1 #line:1148
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["报告时限"]>1 )&(OOOO0O00O00O00OO0 ["报告类型-严重程度"]=="死亡"),"超时标记"]=1 #line:1149
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["评价状态"]!="未评价"),"有效报告"]=1 #line:1151
		OOOO0O00O00O00OO0 .loc [((OOOO0O00O00O00OO0 ["年龄"]=="未填写")|OOOO0O00O00O00OO0 ["年龄"].isnull ()),"年龄"]=-1 #line:1153
		OOOO0O00O00O00OO0 ["年龄"]=OOOO0O00O00O00OO0 ["年龄"].astype (float )#line:1154
		OOOO0O00O00O00OO0 ["年龄"]=OOOO0O00O00O00OO0 ["年龄"].fillna (-1 )#line:1155
		OOOO0O00O00O00OO0 ["性别"]=OOOO0O00O00O00OO0 ["性别"].fillna ("未填写")#line:1156
		OOOO0O00O00O00OO0 ["年龄段"]="未填写"#line:1157
		try :#line:1158
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄类型"]=="月"),"年龄"]=OOOO0O00O00O00OO0 ["年龄"].values /12 #line:1159
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄类型"]=="月"),"年龄类型"]="岁"#line:1160
		except :#line:1161
			pass #line:1162
		try :#line:1163
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄类型"]=="天"),"年龄"]=OOOO0O00O00O00OO0 ["年龄"].values /365 #line:1164
			OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄类型"]=="天"),"年龄类型"]="岁"#line:1165
		except :#line:1166
			pass #line:1167
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values <=4 ),"年龄段"]="0-婴幼儿（0-4）"#line:1168
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values >=5 ),"年龄段"]="1-少儿（5-14）"#line:1169
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values >=15 ),"年龄段"]="2-青壮年（15-44）"#line:1170
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values >=45 ),"年龄段"]="3-中年期（45-64）"#line:1171
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values >=65 ),"年龄段"]="4-老年期（≥65）"#line:1172
		OOOO0O00O00O00OO0 .loc [(OOOO0O00O00O00OO0 ["年龄"].values ==-1 ),"年龄段"]="未填写"#line:1173
		OOOO0O00O00O00OO0 ["规整后品类"]="N"#line:1177
		OOOO0O00O00O00OO0 =TOOL_guizheng (OOOO0O00O00O00OO0 ,2 ,True )#line:1178
		if ini ['模式']in ["器械"]:#line:1181
			OOOO0O00O00O00OO0 =TOOL_guizheng (OOOO0O00O00O00OO0 ,3 ,True )#line:1182
		OOOO0O00O00O00OO0 =TOOL_guizheng (OOOO0O00O00O00OO0 ,"课题",True )#line:1186
		try :#line:1188
			OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"]=OOOO0O00O00O00OO0 ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1189
		except :#line:1190
			pass #line:1191
		OOOO0O00O00O00OO0 ["数据清洗完成标记"]="是"#line:1193
		OOOOO0O0OO00OOOO0 =OOOO0O00O00O00OO0 .loc [:]#line:1194
		return OOOO0O00O00O00OO0 #line:1195
def TOOLS_fileopen ():#line:1201
    ""#line:1202
    warnings .filterwarnings ('ignore')#line:1203
    OOOO0OOOOOO0O0000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1204
    OOOO00OOOOOOO000O =Useful_tools_openfiles (OOOO0OOOOOO0O0000 ,0 )#line:1205
    try :#line:1206
        OOOO00OOOOOOO000O =OOOO00OOOOOOO000O .loc [:,~OOOO00OOOOOOO000O .columns .str .contains ("^Unnamed")]#line:1207
    except :#line:1208
        pass #line:1209
    ini ["模式"]="其他"#line:1211
    O00OO0O0000O0000O =OOOO00OOOOOOO000O #line:1212
    TABLE_tree_Level_2 (O00OO0O0000O0000O ,0 ,O00OO0O0000O0000O )#line:1213
def TOOLS_pinzhong (O00000OO0O00000O0 ):#line:1216
    ""#line:1217
    O00000OO0O00000O0 ["患者姓名"]=O00000OO0O00000O0 ["报告表编码"]#line:1218
    O00000OO0O00000O0 ["用量"]=O00000OO0O00000O0 ["用法用量"]#line:1219
    O00000OO0O00000O0 ["评价状态"]=O00000OO0O00000O0 ["报告单位评价"]#line:1220
    O00000OO0O00000O0 ["用量单位"]=""#line:1221
    O00000OO0O00000O0 ["单位名称"]="不适用"#line:1222
    O00000OO0O00000O0 ["报告地区名称"]="不适用"#line:1223
    O00000OO0O00000O0 ["用法-日"]="不适用"#line:1224
    O00000OO0O00000O0 ["用法-次"]="不适用"#line:1225
    O00000OO0O00000O0 ["不良反应发生时间"]=O00000OO0O00000O0 ["不良反应发生时间"].str [0 :10 ]#line:1226
    O00000OO0O00000O0 ["持有人报告状态"]="待评价"#line:1228
    O00000OO0O00000O0 =O00000OO0O00000O0 .rename (columns ={"是否非预期":"报告类型-新的","不良反应-术语":"不良反应名称","持有人/生产厂家":"上市许可持有人名称"})#line:1233
    return O00000OO0O00000O0 #line:1234
def Useful_tools_openfiles (O00O0O0O00O000O00 ,O00000OO00O0OO0OO ):#line:1239
    ""#line:1240
    OO00000OOOO0O00O0 =[pd .read_excel (OO0O00O00O0O0OO0O ,header =0 ,sheet_name =O00000OO00O0OO0OO )for OO0O00O00O0O0OO0O in O00O0O0O00O000O00 ]#line:1241
    O0OOO0000000OOO0O =pd .concat (OO00000OOOO0O00O0 ,ignore_index =True ).drop_duplicates ()#line:1242
    return O0OOO0000000OOO0O #line:1243
def TOOLS_allfileopen ():#line:1245
    ""#line:1246
    global ori #line:1247
    global ini #line:1248
    global data #line:1249
    ini ["原始模式"]="否"#line:1250
    warnings .filterwarnings ('ignore')#line:1251
    O0OO0O0000O0OOO0O =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1253
    ori =Useful_tools_openfiles (O0OO0O0000O0OOO0O ,0 )#line:1254
    try :#line:1258
        OOOO00OOO0OO00O0O =Useful_tools_openfiles (O0OO0O0000O0OOO0O ,"报告信息")#line:1259
        if "是否非预期"in OOOO00OOO0OO00O0O .columns :#line:1260
            ori =TOOLS_pinzhong (OOOO00OOO0OO00O0O )#line:1261
    except :#line:1262
        pass #line:1263
    ini ["模式"]="其他"#line:1265
    try :#line:1267
        ori =Useful_tools_openfiles (O0OO0O0000O0OOO0O ,"字典数据")#line:1268
        ini ["原始模式"]="是"#line:1269
        if "UDI"in ori .columns :#line:1270
            ini ["模式"]="器械"#line:1271
            data =ori #line:1272
        if "报告类型-新的"in ori .columns :#line:1273
            ini ["模式"]="药品"#line:1274
            data =ori #line:1275
        else :#line:1276
            ini ["模式"]="其他"#line:1277
    except :#line:1278
        pass #line:1279
    try :#line:1282
        ori =ori .loc [:,~ori .columns .str .contains ("^Unnamed")]#line:1283
    except :#line:1284
        pass #line:1285
    if "UDI"in ori .columns and ini ["原始模式"]!="是":#line:1289
        text .insert (END ,"识别出为器械报表,正在进行数据规整...")#line:1290
        ini ["模式"]="器械"#line:1291
        ori =CLEAN_qx (ori )#line:1292
        data =ori #line:1293
    if "报告类型-新的"in ori .columns and ini ["原始模式"]!="是":#line:1294
        text .insert (END ,"识别出为药品报表,正在进行数据规整...")#line:1295
        ini ["模式"]="药品"#line:1296
        ori =CLEAN_yp (ori )#line:1297
        ori =CLEAN_qx (ori )#line:1298
        data =ori #line:1299
    if "光斑贴试验"in ori .columns and ini ["原始模式"]!="是":#line:1300
        text .insert (END ,"识别出为化妆品报表,正在进行数据规整...")#line:1301
        ini ["模式"]="化妆品"#line:1302
        ori =CLEAN_hzp (ori )#line:1303
        ori =CLEAN_qx (ori )#line:1304
        data =ori #line:1305
    if ini ["模式"]=="其他":#line:1308
        text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:1309
        data =ori #line:1310
        O0OO0OO00O00O0000 =Menu (root )#line:1311
        root .config (menu =O0OO0OO00O00O0000 )#line:1312
        try :#line:1313
            ini ["button"][0 ].pack_forget ()#line:1314
            ini ["button"][1 ].pack_forget ()#line:1315
            ini ["button"][2 ].pack_forget ()#line:1316
            ini ["button"][3 ].pack_forget ()#line:1317
            ini ["button"][4 ].pack_forget ()#line:1318
        except :#line:1319
            pass #line:1320
    else :#line:1322
        ini ["清洗后的文件"]=data #line:1323
        ini ["证号"]=Countall (data ).df_zhenghao ()#line:1324
        text .insert (END ,"\n数据读取成功，行数："+str (len (data )))#line:1325
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1326
        try :#line:1327
            ini ["button"][0 ].pack_forget ()#line:1328
            ini ["button"][1 ].pack_forget ()#line:1329
            ini ["button"][2 ].pack_forget ()#line:1330
            ini ["button"][3 ].pack_forget ()#line:1331
            ini ["button"][4 ].pack_forget ()#line:1332
        except :#line:1333
            pass #line:1334
        O00OO000O0OO000OO =Button (frame0 ,text ="地市统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("市级监测机构"),1 ,ori ),)#line:1345
        O00OO000O0OO000OO .pack ()#line:1346
        O0O000O0000O0OOO0 =Button (frame0 ,text ="县区统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("监测机构"),1 ,ori ),)#line:1359
        O0O000O0000O0OOO0 .pack ()#line:1360
        OO0OOOO00O000O0OO =Button (frame0 ,text ="上报单位",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_user (),1 ,ori ),)#line:1373
        OO0OOOO00O000O0OO .pack ()#line:1374
        OO0OOO00OOO0OO000 =Button (frame0 ,text ="生产企业",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_chiyouren (),1 ,ori ),)#line:1385
        OO0OOO00OOO0OO000 .pack ()#line:1386
        O0O0OOOOO00000O00 =Button (frame0 ,text ="产品统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ini ["证号"],1 ,ori ,ori ,"dfx_zhenghao"),)#line:1397
        O0O0OOOOO00000O00 .pack ()#line:1398
        ini ["button"]=[O00OO000O0OO000OO ,O0O000O0000O0OOO0 ,OO0OOOO00O000O0OO ,OO0OOO00OOO0OO000 ,O0O0OOOOO00000O00 ]#line:1399
    text .insert (END ,"\n")#line:1401
def TOOLS_sql (O000000OO0O00OO0O ):#line:1403
    ""#line:1404
    warnings .filterwarnings ("ignore")#line:1405
    try :#line:1406
        O0OO00O00OO000OOO =O000000OO0O00OO0O .columns #line:1407
    except :#line:1408
        return 0 #line:1409
    def O00OOO0O0OO000O0O (O00O0OOO00000O00O ):#line:1411
        try :#line:1412
            O0OO00OO00OOO0OOO =pd .read_sql_query (sqltext (O00O0OOO00000O00O ),con =OO000O0OO0OO0O0OO )#line:1413
        except :#line:1414
            showinfo (title ="提示",message ="SQL语句有误。")#line:1415
            return 0 #line:1416
        try :#line:1417
            del O0OO00OO00OOO0OOO ["level_0"]#line:1418
        except :#line:1419
            pass #line:1420
        TABLE_tree_Level_2 (O0OO00OO00OOO0OOO ,1 ,O000000OO0O00OO0O )#line:1421
    OO0000O00O0O0O0OO ='sqlite://'#line:1425
    OO000000O0OOOOOOO =create_engine (OO0000O00O0O0O0OO )#line:1426
    try :#line:1427
        O000000OO0O00OO0O .to_sql ('data',con =OO000000O0OOOOOOO ,chunksize =10000 ,if_exists ='replace',index =True )#line:1428
    except :#line:1429
        showinfo (title ="提示",message ="不支持该表格。")#line:1430
        return 0 #line:1431
    OO000O0OO0OO0O0OO =OO000000O0OOOOOOO .connect ()#line:1433
    O00O00O0000OOO0OO ="select * from data"#line:1434
    O0OOO0OOOO0OO0O0O =Toplevel ()#line:1437
    O0OOO0OOOO0OO0O0O .title ("SQL查询")#line:1438
    O0OOO0OOOO0OO0O0O .geometry ("700x500")#line:1439
    OOO000O00O000O000 =ttk .Frame (O0OOO0OOOO0OO0O0O ,width =700 ,height =20 )#line:1441
    OOO000O00O000O000 .pack (side =TOP )#line:1442
    OO0O00OOO000O0O0O =ttk .Frame (O0OOO0OOOO0OO0O0O ,width =700 ,height =20 )#line:1443
    OO0O00OOO000O0O0O .pack (side =BOTTOM )#line:1444
    try :#line:1447
        OO00O00OOOOO00000 =StringVar ()#line:1448
        OO00O00OOOOO00000 .set ("select * from data WHERE 单位名称='佛山市第一人民医院'")#line:1449
        OOOO0000OO0OOOO00 =Label (OOO000O00O000O000 ,text ="SQL查询",anchor ='w')#line:1451
        OOOO0000OO0OOOO00 .pack (side =LEFT )#line:1452
        O0O0O0OOOO00O0O0O =Label (OOO000O00O000O000 ,text ="检索：")#line:1453
        O00O00O0000O00OOO =Button (OO0O00OOO000O0O0O ,text ="执行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",width =700 ,command =lambda :O00OOO0O0OO000O0O (O000O0OO00OO00OO0 .get ("1.0","end")),)#line:1467
        O00O00O0000O00OOO .pack (side =LEFT )#line:1468
    except EE :#line:1471
        pass #line:1472
    OOO0OOO0OO0OO0O00 =Scrollbar (O0OOO0OOOO0OO0O0O )#line:1474
    O000O0OO00OO00OO0 =Text (O0OOO0OOOO0OO0O0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1475
    OOO0OOO0OO0OO0O00 .pack (side =RIGHT ,fill =Y )#line:1476
    O000O0OO00OO00OO0 .pack ()#line:1477
    OOO0OOO0OO0OO0O00 .config (command =O000O0OO00OO00OO0 .yview )#line:1478
    O000O0OO00OO00OO0 .config (yscrollcommand =OOO0OOO0OO0OO0O00 .set )#line:1479
    def OOOO0OOO0OOOO0000 (event =None ):#line:1480
        O000O0OO00OO00OO0 .event_generate ('<<Copy>>')#line:1481
    def O0O0000O0OOOO000O (event =None ):#line:1482
        O000O0OO00OO00OO0 .event_generate ('<<Paste>>')#line:1483
    def OO000O00OO0O0O0O0 (O0O000O0O000O00OO ,O000OO0OO0O00O000 ):#line:1484
         TOOLS_savetxt (O0O000O0O000O00OO ,O000OO0OO0O00O000 ,1 )#line:1485
    O000OO000000OO0O0 =Menu (O000O0OO00OO00OO0 ,tearoff =False ,)#line:1486
    O000OO000000OO0O0 .add_command (label ="复制",command =OOOO0OOO0OOOO0000 )#line:1487
    O000OO000000OO0O0 .add_command (label ="粘贴",command =O0O0000O0OOOO000O )#line:1488
    O000OO000000OO0O0 .add_command (label ="源文件列",command =lambda :PROGRAM_helper (O000000OO0O00OO0O .columns .to_list ()))#line:1489
    def OOO0OOOO0O0OOO0O0 (OO0OO00OO0O0O00O0 ):#line:1490
         O000OO000000OO0O0 .post (OO0OO00OO0O0O00O0 .x_root ,OO0OO00OO0O0O00O0 .y_root )#line:1491
    O000O0OO00OO00OO0 .bind ("<Button-3>",OOO0OOOO0O0OOO0O0 )#line:1492
    O000O0OO00OO00OO0 .insert (END ,O00O00O0000OOO0OO )#line:1496
def TOOLS_view_dict (OO000O0O0O0OOO0O0 ,OO0OO00OOOO0O00O0 ):#line:1500
    ""#line:1501
    OOOOOOO000OOO00OO =Toplevel ()#line:1502
    OOOOOOO000OOO00OO .title ("查看数据")#line:1503
    OOOOOOO000OOO00OO .geometry ("700x500")#line:1504
    OO00OO000000O0O0O =Scrollbar (OOOOOOO000OOO00OO )#line:1506
    OO0OOOO00OO0O000O =Text (OOOOOOO000OOO00OO ,height =100 ,width =150 )#line:1507
    OO00OO000000O0O0O .pack (side =RIGHT ,fill =Y )#line:1508
    OO0OOOO00OO0O000O .pack ()#line:1509
    OO00OO000000O0O0O .config (command =OO0OOOO00OO0O000O .yview )#line:1510
    OO0OOOO00OO0O000O .config (yscrollcommand =OO00OO000000O0O0O .set )#line:1511
    if OO0OO00OOOO0O00O0 ==1 :#line:1512
        OO0OOOO00OO0O000O .insert (END ,OO000O0O0O0OOO0O0 )#line:1514
        OO0OOOO00OO0O000O .insert (END ,"\n\n")#line:1515
        return 0 #line:1516
    for OOOO0O0O00OOO0OOO in range (len (OO000O0O0O0OOO0O0 )):#line:1517
        OO0OOOO00OO0O000O .insert (END ,OO000O0O0O0OOO0O0 .iloc [OOOO0O0O00OOO0OOO ,0 ])#line:1518
        OO0OOOO00OO0O000O .insert (END ,":")#line:1519
        OO0OOOO00OO0O000O .insert (END ,OO000O0O0O0OOO0O0 .iloc [OOOO0O0O00OOO0OOO ,1 ])#line:1520
        OO0OOOO00OO0O000O .insert (END ,"\n\n")#line:1521
def TOOLS_save_dict (O0O00OO0OO00O00O0 ):#line:1523
    ""#line:1524
    OOO0OOO0O0OO0OOO0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="排序后的原始数据",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1530
    try :#line:1531
        O0O00OO0OO00O00O0 ["详细描述T"]=O0O00OO0OO00O00O0 ["详细描述T"].astype (str )#line:1532
    except :#line:1533
        pass #line:1534
    try :#line:1535
        O0O00OO0OO00O00O0 ["报告编码"]=O0O00OO0OO00O00O0 ["报告编码"].astype (str )#line:1536
    except :#line:1537
        pass #line:1538
    OOO0O0000OO0O000O =pd .ExcelWriter (OOO0OOO0O0OO0OOO0 ,engine ="xlsxwriter")#line:1540
    O0O00OO0OO00O00O0 .to_excel (OOO0O0000OO0O000O ,sheet_name ="字典数据")#line:1541
    OOO0O0000OO0O000O .close ()#line:1542
    showinfo (title ="提示",message ="文件写入成功。")#line:1543
def TOOLS_savetxt (OOO0OO0O00OOO0OO0 ,O000OO0O00OO0OO00 ,OO00OO00OOOO00O0O ):#line:1545
	""#line:1546
	OO0000OO0OOOOO0OO =open (O000OO0O00OO0OO00 ,"w",encoding ='utf-8')#line:1547
	OO0000OO0OOOOO0OO .write (OOO0OO0O00OOO0OO0 )#line:1548
	OO0000OO0OOOOO0OO .flush ()#line:1550
	if OO00OO00OOOO00O0O ==1 :#line:1551
		showinfo (title ="提示信息",message ="保存成功。")#line:1552
def TOOLS_deep_view (O00O00OO0O0O00O00 ,OOOOO00O00000OOO0 ,OOO0O0OO00000O0O0 ,O000O0OOO0OO0000O ):#line:1555
    ""#line:1556
    if O000O0OOO0OO0000O ==0 :#line:1557
        try :#line:1558
            O00O00OO0O0O00O00 [OOOOO00O00000OOO0 ]=O00O00OO0O0O00O00 [OOOOO00O00000OOO0 ].fillna ("这个没有填写")#line:1559
        except :#line:1560
            pass #line:1561
        OO0O0O0OO00O0OOO0 =O00O00OO0O0O00O00 .groupby (OOOOO00O00000OOO0 ).agg (计数 =(OOO0O0OO00000O0O0 [0 ],OOO0O0OO00000O0O0 [1 ]))#line:1562
    if O000O0OOO0OO0000O ==1 :#line:1563
            OO0O0O0OO00O0OOO0 =pd .pivot_table (O00O00OO0O0O00O00 ,index =OOOOO00O00000OOO0 [:-1 ],columns =OOOOO00O00000OOO0 [-1 ],values =[OOO0O0OO00000O0O0 [0 ]],aggfunc ={OOO0O0OO00000O0O0 [0 ]:OOO0O0OO00000O0O0 [1 ]},fill_value ="0",margins =True ,dropna =False ,)#line:1574
            OO0O0O0OO00O0OOO0 .columns =OO0O0O0OO00O0OOO0 .columns .droplevel (0 )#line:1575
            OO0O0O0OO00O0OOO0 =OO0O0O0OO00O0OOO0 .rename (columns ={"All":"计数"})#line:1576
    if "日期"in OOOOO00O00000OOO0 or "时间"in OOOOO00O00000OOO0 or "季度"in OOOOO00O00000OOO0 :#line:1579
        OO0O0O0OO00O0OOO0 =OO0O0O0OO00O0OOO0 .sort_values ([OOOOO00O00000OOO0 ],ascending =False ,na_position ="last")#line:1582
    else :#line:1583
        OO0O0O0OO00O0OOO0 =OO0O0O0OO00O0OOO0 .sort_values (by =["计数"],ascending =False ,na_position ="last")#line:1587
    OO0O0O0OO00O0OOO0 =OO0O0O0OO00O0OOO0 .reset_index ()#line:1588
    OO0O0O0OO00O0OOO0 ["构成比(%)"]=round (100 *OO0O0O0OO00O0OOO0 ["计数"]/OO0O0O0OO00O0OOO0 ["计数"].sum (),2 )#line:1589
    if O000O0OOO0OO0000O ==0 :#line:1590
        OO0O0O0OO00O0OOO0 ["报表类型"]="dfx_deepview"+"_"+str (OOOOO00O00000OOO0 )#line:1591
    if O000O0OOO0OO0000O ==1 :#line:1592
        OO0O0O0OO00O0OOO0 ["报表类型"]="dfx_deepview"+"_"+str (OOOOO00O00000OOO0 [:-1 ])#line:1593
    return OO0O0O0OO00O0OOO0 #line:1594
def TOOLS_easyreadT (O00O00OO0OO000O0O ):#line:1598
    ""#line:1599
    O00O00OO0OO000O0O ["#####分隔符#########"]="######################################################################"#line:1602
    OO000O0O00O00OO00 =O00O00OO0OO000O0O .stack (dropna =False )#line:1603
    OO000O0O00O00OO00 =pd .DataFrame (OO000O0O00O00OO00 ).reset_index ()#line:1604
    OO000O0O00O00OO00 .columns =["序号","条目","详细描述T"]#line:1605
    OO000O0O00O00OO00 ["逐条查看"]="逐条查看"#line:1606
    return OO000O0O00O00OO00 #line:1607
def TOOLS_data_masking (OOOO0OOOO000000O0 ):#line:1609
    ""#line:1610
    from random import choices #line:1611
    from string import ascii_letters ,digits #line:1612
    OOOO0OOOO000000O0 =OOOO0OOOO000000O0 .reset_index (drop =True )#line:1614
    if "单位名称.1"in OOOO0OOOO000000O0 .columns :#line:1615
        O0O0O0000OOO000OO ="器械"#line:1616
    else :#line:1617
        O0O0O0000OOO000OO ="药品"#line:1618
    OOO00O0000OOO0000 =peizhidir +""+"0（范例）数据脱敏"+".xls"#line:1619
    try :#line:1620
        O0OO0OOOO000O0000 =pd .read_excel (OOO00O0000OOO0000 ,sheet_name =O0O0O0000OOO000OO ,header =0 ,index_col =0 ).reset_index ()#line:1623
    except :#line:1624
        showinfo (title ="错误信息",message ="该功能需要配置文件才能使用！")#line:1625
        return 0 #line:1626
    OO00O00OO00O0OO0O =0 #line:1627
    O0000OO00OOOO0O00 =len (OOOO0OOOO000000O0 )#line:1628
    OOOO0OOOO000000O0 ["abcd"]="□"#line:1629
    for OOOOO00OOO00OO000 in O0OO0OOOO000O0000 ["要脱敏的列"]:#line:1630
        OO00O00OO00O0OO0O =OO00O00OO00O0OO0O +1 #line:1631
        PROGRAM_change_schedule (OO00O00OO00O0OO0O ,O0000OO00OOOO0O00 )#line:1632
        text .insert (END ,"\n正在对以下列进行脱敏处理：")#line:1633
        text .see (END )#line:1634
        text .insert (END ,OOOOO00OOO00OO000 )#line:1635
        try :#line:1636
            OOO0OOO000OOOOO0O =set (OOOO0OOOO000000O0 [OOOOO00OOO00OO000 ])#line:1637
        except :#line:1638
            showinfo (title ="提示",message ="脱敏文件配置错误，请修改配置表。")#line:1639
            return 0 #line:1640
        OOOO000OOOO000O0O ={O00O00O0OOO00O0OO :"".join (choices (digits ,k =10 ))for O00O00O0OOO00O0OO in OOO0OOO000OOOOO0O }#line:1641
        OOOO0OOOO000000O0 [OOOOO00OOO00OO000 ]=OOOO0OOOO000000O0 [OOOOO00OOO00OO000 ].map (OOOO000OOOO000O0O )#line:1642
        OOOO0OOOO000000O0 [OOOOO00OOO00OO000 ]=OOOO0OOOO000000O0 ["abcd"]+OOOO0OOOO000000O0 [OOOOO00OOO00OO000 ].astype (str )#line:1643
    try :#line:1644
        PROGRAM_change_schedule (10 ,10 )#line:1645
        del OOOO0OOOO000000O0 ["abcd"]#line:1646
        O0OOO0O0O00O0OOO0 =filedialog .asksaveasfilename (title =u"保存脱敏后的文件",initialfile ="脱敏后的文件",defaultextension ="xlsx",filetypes =[("Excel 工作簿","*.xlsx"),("Excel 97-2003 工作簿","*.xls")],)#line:1652
        OOO0O0OO0O0OO000O =pd .ExcelWriter (O0OOO0O0O00O0OOO0 ,engine ="xlsxwriter")#line:1653
        OOOO0OOOO000000O0 .to_excel (OOO0O0OO0O0OO000O ,sheet_name ="sheet0")#line:1654
        OOO0O0OO0O0OO000O .close ()#line:1655
    except :#line:1656
        text .insert (END ,"\n文件未保存，但导入的数据已按要求脱敏。")#line:1657
    text .insert (END ,"\n脱敏操作完成。")#line:1658
    text .see (END )#line:1659
    return OOOO0OOOO000000O0 #line:1660
def TOOLS_get_new (OOOO0O00OO0OO0O00 ,OO0O000OO000O0O00 ):#line:1662
	""#line:1663
	def O000000000O0000OO (O0O0O00OOOOOOO0OO ):#line:1664
		""#line:1665
		O0O0O00OOOOOOO0OO =O0O0O00OOOOOOO0OO .drop_duplicates ("报告编码")#line:1666
		O0000O0OOO0O00000 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",O0O0O00OOOOOOO0OO ,1000 ))).replace ("Counter({","{")#line:1667
		O0000O0OOO0O00000 =O0000O0OOO0O00000 .replace ("})","}")#line:1668
		import ast #line:1669
		OO0OO00OOO00000O0 =ast .literal_eval (O0000O0OOO0O00000 )#line:1670
		OO000O0OO000OOO00 =TOOLS_easyreadT (pd .DataFrame ([OO0OO00OOO00000O0 ]))#line:1671
		OO000O0OO000OOO00 =OO000O0OO000OOO00 .rename (columns ={"逐条查看":"ADR名称规整"})#line:1672
		return OO000O0OO000OOO00 #line:1673
	if OO0O000OO000O0O00 =="证号":#line:1674
		root .attributes ("-topmost",True )#line:1675
		root .attributes ("-topmost",False )#line:1676
		OOOOO00O0OOOO0OO0 =OOOO0O00OO0OO0O00 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1677
		O0O00OOO0000O0OOO =OOOOO00O0OOOO0OO0 .drop_duplicates ("注册证编号/曾用注册证编号").copy ()#line:1678
		O0O00OOO0000O0OOO ["所有不良反应"]=""#line:1679
		O0O00OOO0000O0OOO ["关注建议"]=""#line:1680
		O0O00OOO0000O0OOO ["疑似新的"]=""#line:1681
		O0O00OOO0000O0OOO ["疑似旧的"]=""#line:1682
		O0O00OOO0000O0OOO ["疑似新的（高敏）"]=""#line:1683
		O0O00OOO0000O0OOO ["疑似旧的（高敏）"]=""#line:1684
		O00O000000000O000 =1 #line:1685
		O0O0000OO0000O0OO =int (len (O0O00OOO0000O0OOO ))#line:1686
		for OOOO0OO0OOO00OO0O ,O00O0O0O0O0000O00 in O0O00OOO0000O0OOO .iterrows ():#line:1687
			OO0OOOO000O000O0O =OOOO0O00OO0OO0O00 [(OOOO0O00OO0OO0O00 ["注册证编号/曾用注册证编号"]==O00O0O0O0O0000O00 ["注册证编号/曾用注册证编号"])]#line:1688
			O0OO000000OO0000O =OO0OOOO000O000O0O .loc [OO0OOOO000O000O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1689
			OO00000000O00000O =OO0OOOO000O000O0O .loc [~OO0OOOO000O000O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1690
			O000O00O0000OOO0O =O000000000O0000OO (O0OO000000OO0000O )#line:1691
			O000000O0O0OO0O00 =O000000000O0000OO (OO00000000O00000O )#line:1692
			O0000O0O00O0OOO00 =O000000000O0000OO (OO0OOOO000O000O0O )#line:1693
			PROGRAM_change_schedule (O00O000000000O000 ,O0O0000OO0000O0OO )#line:1694
			O00O000000000O000 =O00O000000000O000 +1 #line:1695
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O0000O0O00O0OOO00 .iterrows ():#line:1697
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]:#line:1698
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1699
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"所有不良反应"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"所有不良反应"]+OO00OO00O000O0OO0 #line:1700
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000000O0O0OO0O00 .iterrows ():#line:1702
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]:#line:1703
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1704
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"]+OO00OO00O000O0OO0 #line:1705
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]and int (OO0OO00O0O00O00O0 ["详细描述T"])>=2 :#line:1707
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1708
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"]+OO00OO00O000O0OO0 #line:1709
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000O00O0000OOO0O .iterrows ():#line:1711
				if str (OO0OO00O0O00O00O0 ["条目"]).strip ()not in str (O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"])and "分隔符"not in str (OO0OO00O0O00O00O0 ["条目"]):#line:1712
					OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1713
					O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的"]+OO00OO00O000O0OO0 #line:1714
					if int (OO0OO00O0O00O00O0 ["详细描述T"])>=3 :#line:1715
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]+"！"#line:1716
					if int (OO0OO00O0O00O00O0 ["详细描述T"])>=5 :#line:1717
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]+"●"#line:1718
				if str (OO0OO00O0O00O00O0 ["条目"]).strip ()not in str (O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"])and "分隔符"not in str (OO0OO00O0O00O00O0 ["条目"])and int (OO0OO00O0O00O00O0 ["详细描述T"])>=2 :#line:1720
					OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1721
					O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的（高敏）"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的（高敏）"]+OO00OO00O000O0OO0 #line:1722
		O0O00OOO0000O0OOO ["疑似新的"]="{"+O0O00OOO0000O0OOO ["疑似新的"]+"}"#line:1724
		O0O00OOO0000O0OOO ["疑似旧的"]="{"+O0O00OOO0000O0OOO ["疑似旧的"]+"}"#line:1725
		O0O00OOO0000O0OOO ["所有不良反应"]="{"+O0O00OOO0000O0OOO ["所有不良反应"]+"}"#line:1726
		O0O00OOO0000O0OOO ["疑似新的（高敏）"]="{"+O0O00OOO0000O0OOO ["疑似新的（高敏）"]+"}"#line:1727
		O0O00OOO0000O0OOO ["疑似旧的（高敏）"]="{"+O0O00OOO0000O0OOO ["疑似旧的（高敏）"]+"}"#line:1728
		O0O00OOO0000O0OOO =O0O00OOO0000O0OOO .rename (columns ={"器械待评价(药品新的报告比例)":"新的报告比例"})#line:1730
		O0O00OOO0000O0OOO =O0O00OOO0000O0OOO .rename (columns ={"严重伤害待评价比例(药品严重中新的比例)":"严重报告中新的比例"})#line:1731
		O0O00OOO0000O0OOO ["报表类型"]="dfx_zhenghao"#line:1732
		TABLE_tree_Level_2 (O0O00OOO0000O0OOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OOOO0O00OO0OO0O00 )#line:1733
	if OO0O000OO000O0O00 =="品种":#line:1734
		root .attributes ("-topmost",True )#line:1735
		root .attributes ("-topmost",False )#line:1736
		OOOOO00O0OOOO0OO0 =OOOO0O00OO0OO0O00 .groupby (["产品类别","产品名称"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1737
		O0O00OOO0000O0OOO =OOOOO00O0OOOO0OO0 .drop_duplicates ("产品名称").copy ()#line:1738
		O0O00OOO0000O0OOO ["产品名称"]=O0O00OOO0000O0OOO ["产品名称"].str .replace ("*","",regex =False )#line:1739
		O0O00OOO0000O0OOO ["所有不良反应"]=""#line:1740
		O0O00OOO0000O0OOO ["关注建议"]=""#line:1741
		O0O00OOO0000O0OOO ["疑似新的"]=""#line:1742
		O0O00OOO0000O0OOO ["疑似旧的"]=""#line:1743
		O0O00OOO0000O0OOO ["疑似新的（高敏）"]=""#line:1744
		O0O00OOO0000O0OOO ["疑似旧的（高敏）"]=""#line:1745
		O00O000000000O000 =1 #line:1746
		O0O0000OO0000O0OO =int (len (O0O00OOO0000O0OOO ))#line:1747
		for OOOO0OO0OOO00OO0O ,O00O0O0O0O0000O00 in O0O00OOO0000O0OOO .iterrows ():#line:1750
			OO0OOOO000O000O0O =OOOO0O00OO0OO0O00 [(OOOO0O00OO0OO0O00 ["产品名称"]==O00O0O0O0O0000O00 ["产品名称"])]#line:1752
			O0OO000000OO0000O =OO0OOOO000O000O0O .loc [OO0OOOO000O000O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1754
			OO00000000O00000O =OO0OOOO000O000O0O .loc [~OO0OOOO000O000O0O ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1755
			O0000O0O00O0OOO00 =O000000000O0000OO (OO0OOOO000O000O0O )#line:1756
			O000O00O0000OOO0O =O000000000O0000OO (O0OO000000OO0000O )#line:1757
			O000000O0O0OO0O00 =O000000000O0000OO (OO00000000O00000O )#line:1758
			PROGRAM_change_schedule (O00O000000000O000 ,O0O0000OO0000O0OO )#line:1759
			O00O000000000O000 =O00O000000000O000 +1 #line:1760
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O0000O0O00O0OOO00 .iterrows ():#line:1762
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]:#line:1763
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1764
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"所有不良反应"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"所有不良反应"]+OO00OO00O000O0OO0 #line:1765
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000000O0O0OO0O00 .iterrows ():#line:1768
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]:#line:1769
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1770
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"]+OO00OO00O000O0OO0 #line:1771
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]and int (OO0OO00O0O00O00O0 ["详细描述T"])>=2 :#line:1773
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1774
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"]+OO00OO00O000O0OO0 #line:1775
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000O00O0000OOO0O .iterrows ():#line:1777
				if str (OO0OO00O0O00O00O0 ["条目"]).strip ()not in str (O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的"])and "分隔符"not in str (OO0OO00O0O00O00O0 ["条目"]):#line:1778
					OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1779
					O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的"]+OO00OO00O000O0OO0 #line:1780
					if int (OO0OO00O0O00O00O0 ["详细描述T"])>=3 :#line:1781
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]+"！"#line:1782
					if int (OO0OO00O0O00O00O0 ["详细描述T"])>=5 :#line:1783
						O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"关注建议"]+"●"#line:1784
				if str (OO0OO00O0O00O00O0 ["条目"]).strip ()not in str (O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似旧的（高敏）"])and "分隔符"not in str (OO0OO00O0O00O00O0 ["条目"])and int (OO0OO00O0O00O00O0 ["详细描述T"])>=2 :#line:1786
					OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1787
					O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的（高敏）"]=O0O00OOO0000O0OOO .loc [OOOO0OO0OOO00OO0O ,"疑似新的（高敏）"]+OO00OO00O000O0OO0 #line:1788
		O0O00OOO0000O0OOO ["疑似新的"]="{"+O0O00OOO0000O0OOO ["疑似新的"]+"}"#line:1790
		O0O00OOO0000O0OOO ["疑似旧的"]="{"+O0O00OOO0000O0OOO ["疑似旧的"]+"}"#line:1791
		O0O00OOO0000O0OOO ["所有不良反应"]="{"+O0O00OOO0000O0OOO ["所有不良反应"]+"}"#line:1792
		O0O00OOO0000O0OOO ["疑似新的（高敏）"]="{"+O0O00OOO0000O0OOO ["疑似新的（高敏）"]+"}"#line:1793
		O0O00OOO0000O0OOO ["疑似旧的（高敏）"]="{"+O0O00OOO0000O0OOO ["疑似旧的（高敏）"]+"}"#line:1794
		O0O00OOO0000O0OOO ["报表类型"]="dfx_chanpin"#line:1795
		TABLE_tree_Level_2 (O0O00OOO0000O0OOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OOOO0O00OO0OO0O00 )#line:1796
	if OO0O000OO000O0O00 =="页面":#line:1798
		OO00OO00OO0OO00O0 =""#line:1799
		O0OOO0000O0O0OO0O =""#line:1800
		O0OO000000OO0000O =OOOO0O00OO0OO0O00 .loc [OOOO0O00OO0OO0O00 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1801
		OO00000000O00000O =OOOO0O00OO0OO0O00 .loc [~OOOO0O00OO0OO0O00 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1802
		O000O00O0000OOO0O =O000000000O0000OO (O0OO000000OO0000O )#line:1803
		O000000O0O0OO0O00 =O000000000O0000OO (OO00000000O00000O )#line:1804
		if 1 ==1 :#line:1805
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000000O0O0OO0O00 .iterrows ():#line:1806
					if "分隔符"not in OO0OO00O0O00O00O0 ["条目"]:#line:1807
						OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1808
						O0OOO0000O0O0OO0O =O0OOO0000O0O0OO0O +OO00OO00O000O0OO0 #line:1809
			for O000OO0OOO00O000O ,OO0OO00O0O00O00O0 in O000O00O0000OOO0O .iterrows ():#line:1810
				if str (OO0OO00O0O00O00O0 ["条目"]).strip ()not in O0OOO0000O0O0OO0O and "分隔符"not in str (OO0OO00O0O00O00O0 ["条目"]):#line:1811
					OO00OO00O000O0OO0 ="'"+str (OO0OO00O0O00O00O0 ["条目"])+"':"+str (OO0OO00O0O00O00O0 ["详细描述T"])+","#line:1812
					OO00OO00OO0OO00O0 =OO00OO00OO0OO00O0 +OO00OO00O000O0OO0 #line:1813
		O0OOO0000O0O0OO0O ="{"+O0OOO0000O0O0OO0O +"}"#line:1814
		OO00OO00OO0OO00O0 ="{"+OO00OO00OO0OO00O0 +"}"#line:1815
		O00OO00000O00OO00 ="\n可能是新的不良反应：\n\n"+OO00OO00OO0OO00O0 +"\n\n\n可能不是新的不良反应：\n\n"+O0OOO0000O0O0OO0O #line:1816
		TOOLS_view_dict (O00OO00000O00OO00 ,1 )#line:1817
def TOOLS_strdict_to_pd (O000O0000O00O0OOO ):#line:1819
	""#line:1820
	return pd .DataFrame .from_dict (eval (O000O0000O00O0OOO ),orient ="index",columns =["content"]).reset_index ()#line:1821
def TOOLS_xuanze (O00OOO0O00O0000OO ,OO0O0000O00O0000O ):#line:1823
    ""#line:1824
    if OO0O0000O00O0000O ==0 :#line:1825
        OO0O0O0OO0OOOOOOO =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLS",".xls")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1826
    else :#line:1827
        OO0O0O0OO0OOOOOOO =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1828
    O00OOO0O00O0000OO ["temppr"]=""#line:1829
    for OOOOOO00OOO00OOOO in OO0O0O0OO0OOOOOOO .columns .tolist ():#line:1830
        O00OOO0O00O0000OO ["temppr"]=O00OOO0O00O0000OO ["temppr"]+"----"+O00OOO0O00O0000OO [OOOOOO00OOO00OOOO ]#line:1831
    OOO00OOOO00O0OO00 ="测试字段MMMMM"#line:1832
    for OOOOOO00OOO00OOOO in OO0O0O0OO0OOOOOOO .columns .tolist ():#line:1833
        for O00O0OO0000OOO0O0 in OO0O0O0OO0OOOOOOO [OOOOOO00OOO00OOOO ].drop_duplicates ():#line:1835
            if O00O0OO0000OOO0O0 :#line:1836
                OOO00OOOO00O0OO00 =OOO00OOOO00O0OO00 +"|"+str (O00O0OO0000OOO0O0 )#line:1837
    O00OOO0O00O0000OO =O00OOO0O00O0000OO .loc [O00OOO0O00O0000OO ["temppr"].str .contains (OOO00OOOO00O0OO00 ,na =False )].copy ()#line:1838
    del O00OOO0O00O0000OO ["temppr"]#line:1839
    O00OOO0O00O0000OO =O00OOO0O00O0000OO .reset_index (drop =True )#line:1840
    TABLE_tree_Level_2 (O00OOO0O00O0000OO ,0 ,O00OOO0O00O0000OO )#line:1842
def TOOLS_add_c (OOO00OOOOOOO0O00O ,O0OO0O0000OOO00OO ):#line:1844
			OOO00OOOOOOO0O00O ["关键字查找列o"]=""#line:1845
			for O00O00OOOO000OO00 in TOOLS_get_list (O0OO0O0000OOO00OO ["查找列"]):#line:1846
				OOO00OOOOOOO0O00O ["关键字查找列o"]=OOO00OOOOOOO0O00O ["关键字查找列o"]+OOO00OOOOOOO0O00O [O00O00OOOO000OO00 ].astype ("str")#line:1847
			if O0OO0O0000OOO00OO ["条件"]=="等于":#line:1848
				OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O [O0OO0O0000OOO00OO ["查找列"]].astype (str )==str (O0OO0O0000OOO00OO ["条件值"])),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1849
			if O0OO0O0000OOO00OO ["条件"]=="大于":#line:1850
				OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O [O0OO0O0000OOO00OO ["查找列"]].astype (float )>O0OO0O0000OOO00OO ["条件值"]),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1851
			if O0OO0O0000OOO00OO ["条件"]=="小于":#line:1852
				OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O [O0OO0O0000OOO00OO ["查找列"]].astype (float )<O0OO0O0000OOO00OO ["条件值"]),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1853
			if O0OO0O0000OOO00OO ["条件"]=="介于":#line:1854
				OOO0OO0O00O00O00O =TOOLS_get_list (O0OO0O0000OOO00OO ["条件值"])#line:1855
				OOO00OOOOOOO0O00O .loc [((OOO00OOOOOOO0O00O [O0OO0O0000OOO00OO ["查找列"]].astype (float )<float (OOO0OO0O00O00O00O [1 ]))&(OOO00OOOOOOO0O00O [O0OO0O0000OOO00OO ["查找列"]].astype (float )>float (OOO0OO0O00O00O00O [0 ]))),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1856
			if O0OO0O0000OOO00OO ["条件"]=="不含":#line:1857
				OOO00OOOOOOO0O00O .loc [(~OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (O0OO0O0000OOO00OO ["条件值"])),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1858
			if O0OO0O0000OOO00OO ["条件"]=="包含":#line:1859
				OOO00OOOOOOO0O00O .loc [OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (O0OO0O0000OOO00OO ["条件值"],na =False ),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1860
			if O0OO0O0000OOO00OO ["条件"]=="同时包含":#line:1861
				OO000OOOOOO000O0O =TOOLS_get_list0 (O0OO0O0000OOO00OO ["条件值"],0 )#line:1862
				if len (OO000OOOOOO000O0O )==1 :#line:1863
				    OOO00OOOOOOO0O00O .loc [OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [0 ],na =False ),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1864
				if len (OO000OOOOOO000O0O )==2 :#line:1865
				    OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [0 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [1 ],na =False )),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1866
				if len (OO000OOOOOO000O0O )==3 :#line:1867
				    OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [0 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [1 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [2 ],na =False )),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1868
				if len (OO000OOOOOO000O0O )==4 :#line:1869
				    OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [0 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [1 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [2 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [3 ],na =False )),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1870
				if len (OO000OOOOOO000O0O )==5 :#line:1871
				    OOO00OOOOOOO0O00O .loc [(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [0 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [1 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [2 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [3 ],na =False ))&(OOO00OOOOOOO0O00O ["关键字查找列o"].str .contains (OO000OOOOOO000O0O [4 ],na =False )),O0OO0O0000OOO00OO ["赋值列名"]]=O0OO0O0000OOO00OO ["赋值"]#line:1872
			return OOO00OOOOOOO0O00O #line:1873
def TOOL_guizheng (O0OO0000O000OO00O ,O00O00OO00OO0000O ,OOO0OO00OOOOOOOOO ):#line:1876
	""#line:1877
	if O00O00OO00OO0000O ==0 :#line:1878
		OO000OO0OO0O0O000 =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLSX",".xlsx")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1879
		OO000OO0OO0O0O000 =OO000OO0OO0O0O000 [(OO000OO0OO0O0O000 ["执行标记"]=="是")].reset_index ()#line:1880
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in OO000OO0OO0O0O000 .iterrows ():#line:1881
			O0OO0000O000OO00O =TOOLS_add_c (O0OO0000O000OO00O ,O00OO0000O00OOOOO )#line:1882
		del O0OO0000O000OO00O ["关键字查找列o"]#line:1883
	elif O00O00OO00OO0000O ==1 :#line:1885
		OO000OO0OO0O0O000 =pd .read_excel (peizhidir +"0（范例）数据规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1886
		OO000OO0OO0O0O000 =OO000OO0OO0O0O000 [(OO000OO0OO0O0O000 ["执行标记"]=="是")].reset_index ()#line:1887
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in OO000OO0OO0O0O000 .iterrows ():#line:1888
			O0OO0000O000OO00O =TOOLS_add_c (O0OO0000O000OO00O ,O00OO0000O00OOOOO )#line:1889
		del O0OO0000O000OO00O ["关键字查找列o"]#line:1890
	elif O00O00OO00OO0000O =="课题":#line:1892
		OO000OO0OO0O0O000 =pd .read_excel (peizhidir +"0（范例）品类规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1893
		OO000OO0OO0O0O000 =OO000OO0OO0O0O000 [(OO000OO0OO0O0O000 ["执行标记"]=="是")].reset_index ()#line:1894
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in OO000OO0OO0O0O000 .iterrows ():#line:1895
			O0OO0000O000OO00O =TOOLS_add_c (O0OO0000O000OO00O ,O00OO0000O00OOOOO )#line:1896
		del O0OO0000O000OO00O ["关键字查找列o"]#line:1897
	elif O00O00OO00OO0000O ==2 :#line:1899
		text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:1900
		OO0OO0OO00O0O0O0O =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:1901
		O0000OO0000OO0OOO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:1902
		O0OO0OO00OO0000OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:1903
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in OO0OO0OO00O0O0O0O .iterrows ():#line:1904
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["曾用名1"]),"单位名称"]=O00OO0000O00OOOOO ["单位名称"]#line:1905
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["曾用名2"]),"单位名称"]=O00OO0000O00OOOOO ["单位名称"]#line:1906
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["曾用名3"]),"单位名称"]=O00OO0000O00OOOOO ["单位名称"]#line:1907
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["曾用名4"]),"单位名称"]=O00OO0000O00OOOOO ["单位名称"]#line:1908
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["曾用名5"]),"单位名称"]=O00OO0000O00OOOOO ["单位名称"]#line:1909
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["单位名称"]),"医疗机构类别"]=O00OO0000O00OOOOO ["医疗机构类别"]#line:1911
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["单位名称"]),"监测机构"]=O00OO0000O00OOOOO ["监测机构"]#line:1912
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in O0000OO0000OO0OOO .iterrows ():#line:1914
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["监测机构"]==O00OO0000O00OOOOO ["曾用名1"]),"监测机构"]=O00OO0000O00OOOOO ["监测机构"]#line:1915
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["监测机构"]==O00OO0000O00OOOOO ["曾用名2"]),"监测机构"]=O00OO0000O00OOOOO ["监测机构"]#line:1916
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["监测机构"]==O00OO0000O00OOOOO ["曾用名3"]),"监测机构"]=O00OO0000O00OOOOO ["监测机构"]#line:1917
		for O0O0O0O0OOO00OOO0 in O0OO0OO00OO0000OO ["地市列表"]:#line:1919
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["上报单位所属地区"].str .contains (O0O0O0O0OOO00OOO0 ,na =False )),"市级监测机构"]=O0O0O0O0OOO00OOO0 #line:1920
		O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:1923
		O0OO0000O000OO00O ["市级监测机构"]=O0OO0000O000OO00O ["市级监测机构"].fillna ("-未规整的-")#line:1924
	elif O00O00OO00OO0000O ==3 :#line:1926
			OO000000OO0O0OO00 =(O0OO0000O000OO00O .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).aggregate ({"报告编码":"count"}).reset_index ())#line:1931
			OO000000OO0O0OO00 =OO000000OO0O0OO00 .sort_values (by =["注册证编号/曾用注册证编号","报告编码"],ascending =[False ,False ],na_position ="last").reset_index ()#line:1934
			text .insert (END ,"\n开展产品名称规整..")#line:1935
			del OO000000OO0O0OO00 ["报告编码"]#line:1936
			OO000000OO0O0OO00 =OO000000OO0O0OO00 .drop_duplicates (["注册证编号/曾用注册证编号"])#line:1937
			O0OO0000O000OO00O =O0OO0000O000OO00O .rename (columns ={"上市许可持有人名称":"上市许可持有人名称（规整前）","产品类别":"产品类别（规整前）","产品名称":"产品名称（规整前）"})#line:1939
			O0OO0000O000OO00O =pd .merge (O0OO0000O000OO00O ,OO000000OO0O0OO00 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:1940
	elif O00O00OO00OO0000O ==4 :#line:1942
		text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:1943
		O0000OO0000OO0OOO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:1944
		for OOOO0OO00O0OOO0O0 ,O00OO0000O00OOOOO in O0000OO0000OO0OOO .iterrows ():#line:1946
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["中文全称"]),"监测机构"]=O00OO0000O00OOOOO ["归属地区"]#line:1947
			O0OO0000O000OO00O .loc [(O0OO0000O000OO00O ["单位名称"]==O00OO0000O00OOOOO ["中文全称"]),"市级监测机构"]=O00OO0000O00OOOOO ["地市"]#line:1948
		O0OO0000O000OO00O ["监测机构"]=O0OO0000O000OO00O ["监测机构"].fillna ("未规整")#line:1949
		O0OO0000O000OO00O ["市级监测机构"]=O0OO0000O000OO00O ["市级监测机构"].fillna ("未规整")#line:1950
	if OOO0OO00OOOOOOOOO ==True :#line:1951
		return O0OO0000O000OO00O #line:1952
	else :#line:1953
		TABLE_tree_Level_2 (O0OO0000O000OO00O ,0 ,O0OO0000O000OO00O )#line:1954
def TOOL_person (O00OOOOOOOO00OOOO ):#line:1956
	""#line:1957
	O000OOOO00OO0OOO0 =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="专家列表",header =0 ,index_col =0 ,).reset_index ()#line:1958
	for O000O00O00OO00OOO ,OO00OOOOO000OOO0O in O000OOOO00OO0OOO0 .iterrows ():#line:1959
		O00OOOOOOOO00OOOO .loc [(O00OOOOOOOO00OOOO ["市级监测机构"]==OO00OOOOO000OOO0O ["市级监测机构"]),"评表人员"]=OO00OOOOO000OOO0O ["评表人员"]#line:1960
		O00OOOOOOOO00OOOO ["评表人员"]=O00OOOOOOOO00OOOO ["评表人员"].fillna ("未规整")#line:1961
		O000OO000OO0000OO =O00OOOOOOOO00OOOO .groupby (["评表人员"]).agg (报告数量 =("报告编码","nunique"),地市 =("市级监测机构",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:1965
	TABLE_tree_Level_2 (O000OO000OO0000OO ,0 ,O000OO000OO0000OO )#line:1966
def TOOLS_get_list (O00O00OO0OOO00OO0 ):#line:1968
    ""#line:1969
    O00O00OO0OOO00OO0 =str (O00O00OO0OOO00OO0 )#line:1970
    O0OO000OO0OOO000O =[]#line:1971
    O0OO000OO0OOO000O .append (O00O00OO0OOO00OO0 )#line:1972
    O0OO000OO0OOO000O =",".join (O0OO000OO0OOO000O )#line:1973
    O0OO000OO0OOO000O =O0OO000OO0OOO000O .split ("|")#line:1974
    O000OOO00O000O00O =O0OO000OO0OOO000O [:]#line:1975
    O0OO000OO0OOO000O =list (set (O0OO000OO0OOO000O ))#line:1976
    O0OO000OO0OOO000O .sort (key =O000OOO00O000O00O .index )#line:1977
    return O0OO000OO0OOO000O #line:1978
def TOOLS_get_list0 (O0000O00000OO0OO0 ,OO00O0OO0OOO0OO00 ,*O0OOOO0O0O0000O00 ):#line:1980
    ""#line:1981
    O0000O00000OO0OO0 =str (O0000O00000OO0OO0 )#line:1982
    if pd .notnull (O0000O00000OO0OO0 ):#line:1984
        try :#line:1985
            if "use("in str (O0000O00000OO0OO0 ):#line:1986
                OOO00OOOO00O00O0O =O0000O00000OO0OO0 #line:1987
                OO0OO00OOO00OOO0O =re .compile (r"[(](.*?)[)]",re .S )#line:1988
                O00OOO000O00OO0OO =re .findall (OO0OO00OOO00OOO0O ,OOO00OOOO00O00O0O )#line:1989
                OOO000O0OOO00O0O0 =[]#line:1990
                if ").list"in O0000O00000OO0OO0 :#line:1991
                    OOOOO00OO0OO0OOO0 =peizhidir +""+str (O00OOO000O00OO0OO [0 ])+".xls"#line:1992
                    OOOO0O0OO0000OO00 =pd .read_excel (OOOOO00OO0OO0OOO0 ,sheet_name =O00OOO000O00OO0OO [0 ],header =0 ,index_col =0 ).reset_index ()#line:1995
                    OOOO0O0OO0000OO00 ["检索关键字"]=OOOO0O0OO0000OO00 ["检索关键字"].astype (str )#line:1996
                    OOO000O0OOO00O0O0 =OOOO0O0OO0000OO00 ["检索关键字"].tolist ()+OOO000O0OOO00O0O0 #line:1997
                if ").file"in O0000O00000OO0OO0 :#line:1998
                    OOO000O0OOO00O0O0 =OO00O0OO0OOO0OO00 [O00OOO000O00OO0OO [0 ]].astype (str ).tolist ()+OOO000O0OOO00O0O0 #line:2000
                try :#line:2003
                    if "报告类型-新的"in OO00O0OO0OOO0OO00 .columns :#line:2004
                        OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2005
                        OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split (";")#line:2006
                        OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2007
                        OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split ("；")#line:2008
                        OOO000O0OOO00O0O0 =[OO0O00000000OO000 .replace ("（严重）","")for OO0O00000000OO000 in OOO000O0OOO00O0O0 ]#line:2009
                        OOO000O0OOO00O0O0 =[OO0OO0OO000O0O0OO .replace ("（一般）","")for OO0OO0OO000O0O0OO in OOO000O0OOO00O0O0 ]#line:2010
                except :#line:2011
                    pass #line:2012
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2015
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split ("、")#line:2016
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2017
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split ("，")#line:2018
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2019
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split (",")#line:2020
                OOO0OO0OO000OOO0O =OOO000O0OOO00O0O0 [:]#line:2022
                try :#line:2023
                    if O0OOOO0O0O0000O00 [0 ]==1000 :#line:2024
                      pass #line:2025
                except :#line:2026
                      OOO000O0OOO00O0O0 =list (set (OOO000O0OOO00O0O0 ))#line:2027
                OOO000O0OOO00O0O0 .sort (key =OOO0OO0OO000OOO0O .index )#line:2028
            else :#line:2030
                O0000O00000OO0OO0 =str (O0000O00000OO0OO0 )#line:2031
                OOO000O0OOO00O0O0 =[]#line:2032
                OOO000O0OOO00O0O0 .append (O0000O00000OO0OO0 )#line:2033
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2034
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split ("、")#line:2035
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2036
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split ("，")#line:2037
                OOO000O0OOO00O0O0 =",".join (OOO000O0OOO00O0O0 )#line:2038
                OOO000O0OOO00O0O0 =OOO000O0OOO00O0O0 .split (",")#line:2039
                OOO0OO0OO000OOO0O =OOO000O0OOO00O0O0 [:]#line:2041
                try :#line:2042
                    if O0OOOO0O0O0000O00 [0 ]==1000 :#line:2043
                      OOO000O0OOO00O0O0 =list (set (OOO000O0OOO00O0O0 ))#line:2044
                except :#line:2045
                      pass #line:2046
                OOO000O0OOO00O0O0 .sort (key =OOO0OO0OO000OOO0O .index )#line:2047
                OOO000O0OOO00O0O0 .sort (key =OOO0OO0OO000OOO0O .index )#line:2048
        except ValueError2 :#line:2050
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:2051
            return False #line:2052
    return OOO000O0OOO00O0O0 #line:2054
def TOOLS_easyread2 (OOOOOOOOOOOO00OO0 ):#line:2056
    ""#line:2057
    OOOOOOOOOOOO00OO0 ["分隔符"]="●"#line:2059
    OOOOOOOOOOOO00OO0 ["上报机构描述"]=(OOOOOOOOOOOO00OO0 ["使用过程"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["事件原因分析"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["事件原因分析描述"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["初步处置情况"].astype ("str"))#line:2068
    OOOOOOOOOOOO00OO0 ["持有人处理描述"]=(OOOOOOOOOOOO00OO0 ["关联性评价"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["调查情况"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["事件原因分析"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["具体控制措施"].astype ("str")+OOOOOOOOOOOO00OO0 ["分隔符"]+OOOOOOOOOOOO00OO0 ["未采取控制措施原因"].astype ("str"))#line:2079
    OOO0OO0O0O000OOOO =OOOOOOOOOOOO00OO0 [["报告编码","事件发生日期","报告日期","单位名称","产品名称","注册证编号/曾用注册证编号","产品批号","型号","规格","上市许可持有人名称","管理类别","伤害","伤害表现","器械故障表现","上报机构描述","持有人处理描述","经营企业使用单位报告状态","监测机构","产品类别","医疗机构类别","年龄","年龄类型","性别"]]#line:2106
    OOO0OO0O0O000OOOO =OOO0OO0O0O000OOOO .sort_values (by =["事件发生日期"],ascending =[False ],na_position ="last",)#line:2111
    OOO0OO0O0O000OOOO =OOO0OO0O0O000OOOO .rename (columns ={"报告编码":"规整编码"})#line:2112
    return OOO0OO0O0O000OOOO #line:2113
def fenci0 (OO00O0O0O0O00O0O0 ):#line:2116
	""#line:2117
	OO0O0O0O0OOO0OOO0 =Toplevel ()#line:2118
	OO0O0O0O0OOO0OOO0 .title ('词频统计')#line:2119
	OOO00O00OO000O00O =OO0O0O0O0OOO0OOO0 .winfo_screenwidth ()#line:2120
	O00O0O0OO00000O00 =OO0O0O0O0OOO0OOO0 .winfo_screenheight ()#line:2122
	O0OO0000O00O0OOO0 =400 #line:2124
	OOO0OOOOOO0O0OO00 =120 #line:2125
	O000OOOOOO0OO0000 =(OOO00O00OO000O00O -O0OO0000O00O0OOO0 )/2 #line:2127
	OOOOOOOOO0OOOO000 =(O00O0O0OO00000O00 -OOO0OOOOOO0O0OO00 )/2 #line:2128
	OO0O0O0O0OOO0OOO0 .geometry ("%dx%d+%d+%d"%(O0OO0000O00O0OOO0 ,OOO0OOOOOO0O0OO00 ,O000OOOOOO0OO0000 ,OOOOOOOOO0OOOO000 ))#line:2129
	O00OOO0OO00OOOOOO =Label (OO0O0O0O0OOO0OOO0 ,text ="配置文件：")#line:2130
	O00OOO0OO00OOOOOO .pack ()#line:2131
	OOO0OO0OOO0OO0OOO =Label (OO0O0O0O0OOO0OOO0 ,text ="需要分词的列：")#line:2132
	O0O00O0OO0O000O0O =Entry (OO0O0O0O0OOO0OOO0 ,width =80 )#line:2134
	O0O00O0OO0O000O0O .insert (0 ,peizhidir +"0（范例）中文分词工作文件.xls")#line:2135
	OOO0OO0OO0O0O00OO =Entry (OO0O0O0O0OOO0OOO0 ,width =80 )#line:2136
	OOO0OO0OO0O0O00OO .insert (0 ,"器械故障表现，伤害表现")#line:2137
	O0O00O0OO0O000O0O .pack ()#line:2138
	OOO0OO0OOO0OO0OOO .pack ()#line:2139
	OOO0OO0OO0O0O00OO .pack ()#line:2140
	O0OOO000OO000OOOO =LabelFrame (OO0O0O0O0OOO0OOO0 )#line:2141
	OO00OO0OOOOO0OO00 =Button (O0OOO000OO000OOOO ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (tree_Level_2 ,fenci (O0O00O0OO0O000O0O .get (),OOO0OO0OO0O0O00OO .get (),OO00O0O0O0O00O0O0 ),1 ,0 ))#line:2142
	OO00OO0OOOOO0OO00 .pack (side =LEFT ,padx =1 ,pady =1 )#line:2143
	O0OOO000OO000OOOO .pack ()#line:2144
def fenci (OO0OOO000OO00O00O ,O0O00O000O00O00O0 ,OOOO00OOOOO0O0000 ):#line:2146
    ""#line:2147
    import glob #line:2148
    import jieba #line:2149
    import random #line:2150
    try :#line:2152
        OOOO00OOOOO0O0000 =OOOO00OOOOO0O0000 .drop_duplicates (["报告编码"])#line:2153
    except :#line:2154
        pass #line:2155
    def O00OO0O0O00O00OOO (O00OOO00O00OO00O0 ,OOO0000000OOO00OO ):#line:2156
        OO00O000O00O000OO ={}#line:2157
        for OOOOO00O000O0O000 in O00OOO00O00OO00O0 :#line:2158
            OO00O000O00O000OO [OOOOO00O000O0O000 ]=OO00O000O00O000OO .get (OOOOO00O000O0O000 ,0 )+1 #line:2159
        return sorted (OO00O000O00O000OO .items (),key =lambda O0O00O0OOOO0OO000 :O0O00O0OOOO0OO000 [1 ],reverse =True )[:OOO0000000OOO00OO ]#line:2160
    OOOOOO00000OO00OO =pd .read_excel (OO0OOO000OO00O00O ,sheet_name ="初始化",header =0 ,index_col =0 ).reset_index ()#line:2164
    O00000000O0O00OO0 =OOOOOO00000OO00OO .iloc [0 ,2 ]#line:2166
    O00O000OO0OO0OO0O =pd .read_excel (OO0OOO000OO00O00O ,sheet_name ="停用词",header =0 ,index_col =0 ).reset_index ()#line:2169
    O00O000OO0OO0OO0O ["停用词"]=O00O000OO0OO0OO0O ["停用词"].astype (str )#line:2171
    O000OO00000O0O00O =[OOOO0000OOO0OOO0O .strip ()for OOOO0000OOO0OOO0O in O00O000OO0OO0OO0O ["停用词"]]#line:2172
    OOO0OO0O0O00000O0 =pd .read_excel (OO0OOO000OO00O00O ,sheet_name ="本地词库",header =0 ,index_col =0 ).reset_index ()#line:2175
    OOOO000O0O0OOO0O0 =OOO0OO0O0O00000O0 ["本地词库"]#line:2176
    jieba .load_userdict (OOOO000O0O0OOO0O0 )#line:2177
    O000OO0OO00000OO0 =""#line:2180
    OOOO00OO00OOOO00O =get_list0 (O0O00O000O00O00O0 ,OOOO00OOOOO0O0000 )#line:2183
    try :#line:2184
        for OO0O0OO00000O0O0O in OOOO00OO00OOOO00O :#line:2185
            for OOOOO0OO00OOO0000 in OOOO00OOOOO0O0000 [OO0O0OO00000O0O0O ]:#line:2186
                O000OO0OO00000OO0 =O000OO0OO00000OO0 +str (OOOOO0OO00OOO0000 )#line:2187
    except :#line:2188
        text .insert (END ,"分词配置文件未正确设置，将对整个表格进行分词。")#line:2189
        for OO0O0OO00000O0O0O in OOOO00OOOOO0O0000 .columns .tolist ():#line:2190
            for OOOOO0OO00OOO0000 in OOOO00OOOOO0O0000 [OO0O0OO00000O0O0O ]:#line:2191
                O000OO0OO00000OO0 =O000OO0OO00000OO0 +str (OOOOO0OO00OOO0000 )#line:2192
    OO00OOOOO0OO00O00 =[]#line:2193
    OO00OOOOO0OO00O00 =OO00OOOOO0OO00O00 +[OO0OO00OO00OOO0OO for OO0OO00OO00OOO0OO in jieba .cut (O000OO0OO00000OO0 )if OO0OO00OO00OOO0OO not in O000OO00000O0O00O ]#line:2194
    O000O0OOOOOO00O0O =dict (O00OO0O0O00O00OOO (OO00OOOOO0OO00O00 ,O00000000O0O00OO0 ))#line:2195
    OOO0O0000OO00OO00 =pd .DataFrame ([O000O0OOOOOO00O0O ]).T #line:2196
    OOO0O0000OO00OO00 =OOO0O0000OO00OO00 .reset_index ()#line:2197
    return OOO0O0000OO00OO00 #line:2198
def TOOLS_time (OOO0OO00O0OO00OOO ,O0OO0000OO0O00000 ,OOOOOOOOOOOOOOOOO ):#line:2200
	""#line:2201
	OOOO0OO0OO0O0O00O =OOO0OO00O0OO00OOO .groupby ([O0OO0000OO0O00000 ]).agg (报告总数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda OO000O000OOOO0O0O :STAT_countpx (OO000O000OOOO0O0O .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O000O0O0OO0O00O :STAT_countpx (O0O000O0O0OO0O00O .values ,"死亡")),).sort_values (by =O0OO0000OO0O00000 ,ascending =[True ],na_position ="last").reset_index ()#line:2206
	OOOO0OO0OO0O0O00O =OOOO0OO0OO0O0O00O .set_index (O0OO0000OO0O00000 )#line:2207
	OOOO0OO0OO0O0O00O =OOOO0OO0OO0O0O00O .resample ('D').asfreq (fill_value =0 )#line:2209
	OOOO0OO0OO0O0O00O ["time"]=OOOO0OO0OO0O0O00O .index .values #line:2211
	OOOO0OO0OO0O0O00O ["time"]=pd .to_datetime (OOOO0OO0OO0O0O00O ["time"],format ="%Y/%m/%d").dt .date #line:2212
	if OOOOOOOOOOOOOOOOO ==1 :#line:2214
		return OOOO0OO0OO0O0O00O .reset_index (drop =True )#line:2216
	OOOO0OO0OO0O0O00O ["30天累计数"]=OOOO0OO0OO0O0O00O ["报告总数"].rolling (30 ,min_periods =1 ).agg (lambda OOOOOO0OOOOO000O0 :sum (OOOOOO0OOOOO000O0 )).astype (int )#line:2218
	OOOO0OO0OO0O0O00O ["30天严重伤害累计数"]=OOOO0OO0OO0O0O00O ["严重伤害数"].rolling (30 ,min_periods =1 ).agg (lambda OOOOOO00O0OO0OO00 :sum (OOOOOO00O0OO0OO00 )).astype (int )#line:2219
	OOOO0OO0OO0O0O00O ["30天死亡累计数"]=OOOO0OO0OO0O0O00O ["死亡数量"].rolling (30 ,min_periods =1 ).agg (lambda O0OO000000O0O0000 :sum (O0OO000000O0O0000 )).astype (int )#line:2220
	OOOO0OO0OO0O0O00O .loc [(((OOOO0OO0OO0O0O00O ["30天累计数"]>=3 )&(OOOO0OO0OO0O0O00O ["30天严重伤害累计数"]>=1 ))|(OOOO0OO0OO0O0O00O ["30天累计数"]>=5 )|(OOOO0OO0OO0O0O00O ["30天死亡累计数"]>=1 )),"关注区域"]=OOOO0OO0OO0O0O00O ["30天累计数"]#line:2241
	DRAW_make_risk_plot (OOOO0OO0OO0O0O00O ,"time",["30天累计数","30天严重伤害累计数","关注区域"],"折线图",999 )#line:2246
def TOOLS_keti (OO0OO0O00O00O0OO0 ):#line:2250
	""#line:2251
	import datetime #line:2252
	def OO00OOO00OO000O0O (O0OO0OO0O0O0O0O0O ,O00OOOO000O000OO0 ):#line:2254
		if ini ["模式"]=="药品":#line:2255
			O00O00O00O000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:2256
		if ini ["模式"]=="器械":#line:2257
			O00O00O00O000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:2258
		if ini ["模式"]=="化妆品":#line:2259
			O00O00O00O000O0OO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:2260
		O00O0OOOO000O000O =O00O00O00O000O0OO ["权重"][0 ]#line:2261
		O0O00O0OOO0000OOO =O00O00O00O000O0OO ["权重"][1 ]#line:2262
		O000OOO0O0O0000OO =O00O00O00O000O0OO ["权重"][2 ]#line:2263
		O0OO000O000OO0OO0 =O00O00O00O000O0OO ["权重"][3 ]#line:2264
		OO0O0OO0OO0OOOOOO =O00O00O00O000O0OO ["值"][3 ]#line:2265
		OO0OOOO0OO000000O =O00O00O00O000O0OO ["权重"][4 ]#line:2267
		OO00O0O0O00OO0000 =O00O00O00O000O0OO ["值"][4 ]#line:2268
		OO0O000OOOOO0OOO0 =O00O00O00O000O0OO ["权重"][5 ]#line:2270
		OO0OO0O00O0O0OOO0 =O00O00O00O000O0OO ["值"][5 ]#line:2271
		O00O00OO0O0O0O00O =O00O00O00O000O0OO ["权重"][6 ]#line:2273
		O0OO0OOOOOO00O0OO =O00O00O00O000O0OO ["值"][6 ]#line:2274
		O000OOOOOOOO00OO0 =pd .to_datetime (O0OO0OO0O0O0O0O0O )#line:2276
		O0OOO00O00O0O0O0O =O00OOOO000O000OO0 .copy ().set_index ('报告日期')#line:2277
		O0OOO00O00O0O0O0O =O0OOO00O00O0O0O0O .sort_index ()#line:2278
		if ini ["模式"]=="器械":#line:2279
			O0OOO00O00O0O0O0O ["关键字查找列"]=O0OOO00O00O0O0O0O ["器械故障表现"].astype (str )+O0OOO00O00O0O0O0O ["伤害表现"].astype (str )+O0OOO00O00O0O0O0O ["使用过程"].astype (str )+O0OOO00O00O0O0O0O ["事件原因分析描述"].astype (str )+O0OOO00O00O0O0O0O ["初步处置情况"].astype (str )#line:2280
		else :#line:2281
			O0OOO00O00O0O0O0O ["关键字查找列"]=O0OOO00O00O0O0O0O ["器械故障表现"].astype (str )#line:2282
		O0OOO00O00O0O0O0O .loc [O0OOO00O00O0O0O0O ["关键字查找列"].str .contains (OO0O0OO0OO0OOOOOO ,na =False ),"高度关注关键字"]=1 #line:2283
		O0OOO00O00O0O0O0O .loc [O0OOO00O00O0O0O0O ["关键字查找列"].str .contains (OO00O0O0O00OO0000 ,na =False ),"二级敏感词"]=1 #line:2284
		O0OOO00O00O0O0O0O .loc [O0OOO00O00O0O0O0O ["关键字查找列"].str .contains (OO0OO0O00O0O0OOO0 ,na =False ),"减分项"]=1 #line:2285
		O0000OO00000OO0OO =O0OOO00O00O0O0O0O .loc [O000OOOOOOOO00OO0 -pd .Timedelta (days =30 ):O000OOOOOOOO00OO0 ].reset_index ()#line:2287
		O0O0OOOO0OOO0O0OO =O0OOO00O00O0O0O0O .loc [O000OOOOOOOO00OO0 -pd .Timedelta (days =365 ):O000OOOOOOOO00OO0 ].reset_index ()#line:2288
		O0O0OO00OO00O000O =O0000OO00000OO0OO .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("注册证编号/曾用注册证编号","count"),严重伤害数 =("伤害",lambda O0O0OOOO0O0O0O000 :STAT_countpx (O0O0OOOO0O0O0O000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OOO00OO0OO0O0O :STAT_countpx (OO0OOO00OO0OO0O0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),待评价数 =("持有人报告状态",lambda OO0O0O0OOOO000OOO :STAT_countpx (OO0O0O0OOOO000OOO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O00OO0O0OOOOOO0OO :STAT_countpx (O00OO0O0OOOOOO0OO .values ,"严重伤害待评价")),高度关注关键字 =("高度关注关键字","sum"),二级敏感词 =("二级敏感词","sum"),减分项 =("减分项","sum"),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:2310
		O0O00O0OOOOO000OO =O0000OO00000OO0OO .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("型号","count"),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:2315
		O0O00O0OOOOO000OO =O0O00O0OOOOO000OO .drop_duplicates ("注册证编号/曾用注册证编号")#line:2316
		O0OO0O000OO0OO0OO =O0000OO00000OO0OO .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("产品批号","count"),严重伤害数 =("伤害",lambda O000O0OOO00OO0O00 :STAT_countpx (O000O0OOO00OO0O00 .values ,"严重伤害")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:2321
		O0OO0O000OO0OO0OO ["风险评分-影响"]=0 #line:2324
		O0OO0O000OO0OO0OO ["评分说明"]=""#line:2325
		O0OO0O000OO0OO0OO .loc [((O0OO0O000OO0OO0OO ["批号计数"]>=3 )&(O0OO0O000OO0OO0OO ["严重伤害数"]>=1 )&(O0OO0O000OO0OO0OO ["产品类别"]!="有源"))|((O0OO0O000OO0OO0OO ["批号计数"]>=5 )&(O0OO0O000OO0OO0OO ["产品类别"]!="有源")),"风险评分-影响"]=O0OO0O000OO0OO0OO ["风险评分-影响"]+3 #line:2326
		O0OO0O000OO0OO0OO .loc [(O0OO0O000OO0OO0OO ["风险评分-影响"]>=3 ),"评分说明"]=O0OO0O000OO0OO0OO ["评分说明"]+"●符合省中心无源规则+3;"#line:2327
		O0OO0O000OO0OO0OO =O0OO0O000OO0OO0OO .sort_values (by ="风险评分-影响",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2331
		O0OO0O000OO0OO0OO =O0OO0O000OO0OO0OO .drop_duplicates ("注册证编号/曾用注册证编号")#line:2332
		O0O00O0OOOOO000OO =O0O00O0OOOOO000OO [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号","型号计数"]]#line:2333
		O0OO0O000OO0OO0OO =O0OO0O000OO0OO0OO [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号","批号计数","风险评分-影响","评分说明"]]#line:2334
		O0O0OO00OO00O000O =pd .merge (O0O0OO00OO00O000O ,O0O00O0OOOOO000OO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2335
		O0O0OO00OO00O000O =pd .merge (O0O0OO00OO00O000O ,O0OO0O000OO0OO0OO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2337
		O0O0OO00OO00O000O .loc [((O0O0OO00OO00O000O ["证号计数"]>=3 )&(O0O0OO00OO00O000O ["严重伤害数"]>=1 )&(O0O0OO00OO00O000O ["产品类别"]=="有源"))|((O0O0OO00OO00O000O ["证号计数"]>=5 )&(O0O0OO00OO00O000O ["产品类别"]=="有源")),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+3 #line:2341
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-影响"]>=3 )&(O0O0OO00OO00O000O ["产品类别"]=="有源"),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"●符合省中心有源规则+3;"#line:2342
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["死亡数量"]>=1 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+10 #line:2347
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-影响"]>=10 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"存在死亡报告;"#line:2348
		O0O00000O0OOOOOO0 =round (O00O0OOOO000O000O *(O0O0OO00OO00O000O ["严重伤害数"]/O0O0OO00OO00O000O ["证号计数"]),2 )#line:2351
		O0O0OO00OO00O000O ["风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+O0O00000O0OOOOOO0 #line:2352
		O0O0OO00OO00O000O ["评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"严重比评分"+O0O00000O0OOOOOO0 .astype (str )+";"#line:2353
		O0OOOOOO0O00OOO00 =round (O0O00O0OOO0000OOO *(np .log (O0O0OO00OO00O000O ["单位个数"])),2 )#line:2356
		O0O0OO00OO00O000O ["风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+O0OOOOOO0O00OOO00 #line:2357
		O0O0OO00OO00O000O ["评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"报告单位评分"+O0OOOOOO0O00OOO00 .astype (str )+";"#line:2358
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["产品类别"]=="有源")&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+O000OOO0O0O0000OO *O0O0OO00OO00O000O ["型号计数"]/O0O0OO00OO00O000O ["证号计数"]#line:2361
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["产品类别"]=="有源")&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"型号集中度评分"+(round (O000OOO0O0O0000OO *O0O0OO00OO00O000O ["型号计数"]/O0O0OO00OO00O000O ["证号计数"],2 )).astype (str )+";"#line:2362
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["产品类别"]!="有源")&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+O000OOO0O0O0000OO *O0O0OO00OO00O000O ["批号计数"]/O0O0OO00OO00O000O ["证号计数"]#line:2363
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["产品类别"]!="有源")&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"批号集中度评分"+(round (O000OOO0O0O0000OO *O0O0OO00OO00O000O ["批号计数"]/O0O0OO00OO00O000O ["证号计数"],2 )).astype (str )+";"#line:2364
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["高度关注关键字"]>=1 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+O0OO000O000OO0OO0 #line:2367
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["高度关注关键字"]>=1 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"●含有高度关注关键字评分"+str (O0OO000O000OO0OO0 )+"；"#line:2368
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["二级敏感词"]>=1 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+OO0OOOO0OO000000O #line:2371
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["二级敏感词"]>=1 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"含有二级敏感词评分"+str (OO0OOOO0OO000000O )+"；"#line:2372
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["减分项"]>=1 ),"风险评分-影响"]=O0O0OO00OO00O000O ["风险评分-影响"]+OO0O000OOOOO0OOO0 #line:2375
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["减分项"]>=1 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"减分项评分"+str (OO0O000OOOOO0OOO0 )+"；"#line:2376
		O000000000O000OO0 =Countall (O0O0OOOO0OOO0O0OO ).df_findrisk ("事件发生月份")#line:2379
		O000000000O000OO0 =O000000000O000OO0 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2380
		O000000000O000OO0 =O000000000O000OO0 [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2381
		O0O0OO00OO00O000O =pd .merge (O0O0OO00OO00O000O ,O000000000O000OO0 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2382
		O0O0OO00OO00O000O ["风险评分-月份"]=1 #line:2384
		O0O0OO00OO00O000O ["mfc"]=""#line:2385
		O0O0OO00OO00O000O .loc [((O0O0OO00OO00O000O ["证号计数"]>O0O0OO00OO00O000O ["均值"])&(O0O0OO00OO00O000O ["标准差"].astype (str )=="nan")),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+1 #line:2386
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>O0O0OO00OO00O000O ["均值"]),"mfc"]="月份计数超过历史均值"+O0O0OO00OO00O000O ["均值"].astype (str )+"；"#line:2387
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=(O0O0OO00OO00O000O ["均值"]+O0O0OO00OO00O000O ["标准差"]))&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+1 #line:2389
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=(O0O0OO00OO00O000O ["均值"]+O0O0OO00OO00O000O ["标准差"]))&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"mfc"]="月份计数超过3例超过历史均值一个标准差("+O0O0OO00OO00O000O ["标准差"].astype (str )+")；"#line:2390
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+2 #line:2392
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=3 ),"mfc"]="月份计数超过3例且超过历史95%CI上限("+O0O0OO00OO00O000O ["CI上限"].astype (str )+")；"#line:2393
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=5 ),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+1 #line:2395
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=5 ),"mfc"]="月份计数超过5例且超过历史95%CI上限("+O0O0OO00OO00O000O ["CI上限"].astype (str )+")；"#line:2396
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=7 ),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+1 #line:2398
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=7 ),"mfc"]="月份计数超过7例且超过历史95%CI上限("+O0O0OO00OO00O000O ["CI上限"].astype (str )+")；"#line:2399
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=9 ),"风险评分-月份"]=O0O0OO00OO00O000O ["风险评分-月份"]+1 #line:2401
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["证号计数"]>=9 ),"mfc"]="月份计数超过9例且超过历史95%CI上限("+O0O0OO00OO00O000O ["CI上限"].astype (str )+")；"#line:2402
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=3 )&(O0O0OO00OO00O000O ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2406
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["证号计数"]>=3 )&(O0O0OO00OO00O000O ["标准差"].astype (str )=="nan"),"mfc"]="无历史数据但数量超过3例；"#line:2407
		O0O0OO00OO00O000O ["评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"●●证号数量："+O0O0OO00OO00O000O ["证号计数"].astype (str )+";"+O0O0OO00OO00O000O ["mfc"]#line:2410
		del O0O0OO00OO00O000O ["mfc"]#line:2411
		O0O0OO00OO00O000O =O0O0OO00OO00O000O .rename (columns ={"均值":"月份均值","标准差":"月份标准差","CI上限":"月份CI上限"})#line:2412
		O000000000O000OO0 =Countall (O0O0OOOO0OOO0O0OO ).df_findrisk ("产品批号")#line:2416
		O000000000O000OO0 =O000000000O000OO0 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2417
		O000000000O000OO0 =O000000000O000OO0 [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2418
		O0O0OO00OO00O000O =pd .merge (O0O0OO00OO00O000O ,O000000000O000OO0 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2419
		O0O0OO00OO00O000O ["风险评分-批号"]=1 #line:2421
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["产品类别"]!="有源"),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"●●高峰批号数量："+O0O0OO00OO00O000O ["批号计数"].astype (str )+";"#line:2422
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>O0O0OO00OO00O000O ["均值"]),"风险评分-批号"]=O0O0OO00OO00O000O ["风险评分-批号"]+1 #line:2424
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>O0O0OO00OO00O000O ["均值"]),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"高峰批号计数超过历史均值"+O0O0OO00OO00O000O ["均值"].astype (str )+"；"#line:2425
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>(O0O0OO00OO00O000O ["均值"]+O0O0OO00OO00O000O ["标准差"]))&(O0O0OO00OO00O000O ["批号计数"]>=3 ),"风险评分-批号"]=O0O0OO00OO00O000O ["风险评分-批号"]+1 #line:2426
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>(O0O0OO00OO00O000O ["均值"]+O0O0OO00OO00O000O ["标准差"]))&(O0O0OO00OO00O000O ["批号计数"]>=3 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"高峰批号计数超过3例超过历史均值一个标准差("+O0O0OO00OO00O000O ["标准差"].astype (str )+")；"#line:2427
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["批号计数"]>=3 ),"风险评分-批号"]=O0O0OO00OO00O000O ["风险评分-批号"]+1 #line:2428
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>O0O0OO00OO00O000O ["CI上限"])&(O0O0OO00OO00O000O ["批号计数"]>=3 ),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"高峰批号计数超过3例且超过历史95%CI上限("+O0O0OO00OO00O000O ["CI上限"].astype (str )+")；"#line:2429
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>=3 )&(O0O0OO00OO00O000O ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2431
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["批号计数"]>=3 )&(O0O0OO00OO00O000O ["标准差"].astype (str )=="nan"),"评分说明"]=O0O0OO00OO00O000O ["评分说明"]+"无历史数据但数量超过3例；"#line:2432
		O0O0OO00OO00O000O =O0O0OO00OO00O000O .rename (columns ={"均值":"高峰批号均值","标准差":"高峰批号标准差","CI上限":"高峰批号CI上限"})#line:2433
		O0O0OO00OO00O000O ["风险评分-影响"]=round (O0O0OO00OO00O000O ["风险评分-影响"],2 )#line:2436
		O0O0OO00OO00O000O ["风险评分-月份"]=round (O0O0OO00OO00O000O ["风险评分-月份"],2 )#line:2437
		O0O0OO00OO00O000O ["风险评分-批号"]=round (O0O0OO00OO00O000O ["风险评分-批号"],2 )#line:2438
		O0O0OO00OO00O000O ["总体评分"]=O0O0OO00OO00O000O ["风险评分-影响"].copy ()#line:2440
		O0O0OO00OO00O000O ["关注建议"]=""#line:2441
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-影响"]>=3 ),"关注建议"]=O0O0OO00OO00O000O ["关注建议"]+"●建议关注(影响范围)；"#line:2442
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-月份"]>=3 ),"关注建议"]=O0O0OO00OO00O000O ["关注建议"]+"●建议关注(当月数量异常)；"#line:2443
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-批号"]>=3 ),"关注建议"]=O0O0OO00OO00O000O ["关注建议"]+"●建议关注(高峰批号数量异常)。"#line:2444
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-月份"]>=O0O0OO00OO00O000O ["风险评分-批号"]),"总体评分"]=O0O0OO00OO00O000O ["风险评分-影响"]*O0O0OO00OO00O000O ["风险评分-月份"]#line:2448
		O0O0OO00OO00O000O .loc [(O0O0OO00OO00O000O ["风险评分-月份"]<O0O0OO00OO00O000O ["风险评分-批号"]),"总体评分"]=O0O0OO00OO00O000O ["风险评分-影响"]*O0O0OO00OO00O000O ["风险评分-批号"]#line:2449
		O0O0OO00OO00O000O ["总体评分"]=round (O0O0OO00OO00O000O ["总体评分"],2 )#line:2451
		O0O0OO00OO00O000O ["评分说明"]=O0O0OO00OO00O000O ["关注建议"]+O0O0OO00OO00O000O ["评分说明"]#line:2452
		O0O0OO00OO00O000O =O0O0OO00OO00O000O .sort_values (by =["总体评分","风险评分-影响"],ascending =[False ,False ],na_position ="last").reset_index (drop =True )#line:2453
		O0O0OO00OO00O000O ["主要故障分类"]=""#line:2456
		for OO0O0OO0OO000O0O0 ,OO0O00OO00000O000 in O0O0OO00OO00O000O .iterrows ():#line:2457
			OO0O000O0O000OOOO =O0000OO00000OO0OO [(O0000OO00000OO0OO ["注册证编号/曾用注册证编号"]==OO0O00OO00000O000 ["注册证编号/曾用注册证编号"])].copy ()#line:2458
			if OO0O00OO00000O000 ["总体评分"]>=float (O00O00OO0O0O0O00O ):#line:2459
				if OO0O00OO00000O000 ["规整后品类"]!="N":#line:2460
					O0000O0O0000O0OOO =Countall (OO0O000O0O000OOOO ).df_psur ("特定品种",OO0O00OO00000O000 ["规整后品类"])#line:2461
				elif OO0O00OO00000O000 ["产品类别"]=="无源":#line:2462
					O0000O0O0000O0OOO =Countall (OO0O000O0O000OOOO ).df_psur ("通用无源")#line:2463
				elif OO0O00OO00000O000 ["产品类别"]=="有源":#line:2464
					O0000O0O0000O0OOO =Countall (OO0O000O0O000OOOO ).df_psur ("通用有源")#line:2465
				elif OO0O00OO00000O000 ["产品类别"]=="体外诊断试剂":#line:2466
					O0000O0O0000O0OOO =Countall (OO0O000O0O000OOOO ).df_psur ("体外诊断试剂")#line:2467
				OO0OO000O00O0O0O0 =O0000O0O0000O0OOO [["事件分类","总数量"]].copy ()#line:2469
				OOOO00OOO0OO0OO0O =""#line:2470
				for O0O0OOO0OO00O0OO0 ,O00O00OOO00OO0OOO in OO0OO000O00O0O0O0 .iterrows ():#line:2471
					OOOO00OOO0OO0OO0O =OOOO00OOO0OO0OO0O +str (O00O00OOO00OO0OOO ["事件分类"])+":"+str (O00O00OOO00OO0OOO ["总数量"])+";"#line:2472
				O0O0OO00OO00O000O .loc [OO0O0OO0OO000O0O0 ,"主要故障分类"]=OOOO00OOO0OO0OO0O #line:2473
			else :#line:2474
				break #line:2475
		O0O0OO00OO00O000O =O0O0OO00OO00O000O [["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","证号计数","严重伤害数","死亡数量","总体评分","风险评分-影响","风险评分-月份","风险评分-批号","主要故障分类","评分说明","单位个数","单位列表","批号个数","批号列表","型号个数","型号列表","规格个数","规格列表","待评价数","严重伤害待评价数","高度关注关键字","二级敏感词","月份均值","月份标准差","月份CI上限","高峰批号均值","高峰批号标准差","高峰批号CI上限","型号","型号计数","产品批号","批号计数"]]#line:2479
		O0O0OO00OO00O000O ["报表类型"]="dfx_zhenghao"#line:2480
		TABLE_tree_Level_2 (O0O0OO00OO00O000O ,1 ,O0000OO00000OO0OO ,O0O0OOOO0OOO0O0OO )#line:2481
		pass #line:2482
	OOOO0000OOOOOO0O0 =Toplevel ()#line:2485
	OOOO0000OOOOOO0O0 .title ('风险预警')#line:2486
	O0O0OOO0OOOO0OOO0 =OOOO0000OOOOOO0O0 .winfo_screenwidth ()#line:2487
	OO0O000OO00OO0OOO =OOOO0000OOOOOO0O0 .winfo_screenheight ()#line:2489
	O00O0O000OOOOOO0O =350 #line:2491
	O00O000O0O0O0O0O0 =35 #line:2492
	OOOO000O0O0O0O0OO =(O0O0OOO0OOOO0OOO0 -O00O0O000OOOOOO0O )/2 #line:2494
	O0O0O0OOO00000O0O =(OO0O000OO00OO0OOO -O00O000O0O0O0O0O0 )/2 #line:2495
	OOOO0000OOOOOO0O0 .geometry ("%dx%d+%d+%d"%(O00O0O000OOOOOO0O ,O00O000O0O0O0O0O0 ,OOOO000O0O0O0O0OO ,O0O0O0OOO00000O0O ))#line:2496
	O0OOO0O0OO0000OOO =Label (OOOO0000OOOOOO0O0 ,text ="预警日期：")#line:2498
	O0OOO0O0OO0000OOO .grid (row =1 ,column =0 ,sticky ="w")#line:2499
	OOOOOOO0O0OOOO0OO =Entry (OOOO0000OOOOOO0O0 ,width =30 )#line:2500
	OOOOOOO0O0OOOO0OO .insert (0 ,datetime .date .today ())#line:2501
	OOOOOOO0O0OOOO0OO .grid (row =1 ,column =1 ,sticky ="w")#line:2502
	O0000O00O00O000OO =Button (OOOO0000OOOOOO0O0 ,text ="确定",width =10 ,command =lambda :TABLE_tree_Level_2 (OO00OOO00OO000O0O (OOOOOOO0O0OOOO0OO .get (),OO0OO0O00O00O0OO0 ),1 ,OO0OO0O00O00O0OO0 ))#line:2506
	O0000O00O00O000OO .grid (row =1 ,column =3 ,sticky ="w")#line:2507
	pass #line:2509
def TOOLS_autocount (OOO0000O0O000OOOO ,OO00OOOO000OO00O0 ):#line:2511
    ""#line:2512
    OO0O0O0OO0OO0OO00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ).reset_index ()#line:2515
    O00O0000OOO0OO0OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ).reset_index ()#line:2518
    OO00O0O0000OO0O00 =O00O0000OOO0OO0OO [(O00O0000OOO0OO0OO ["是否属于二级以上医疗机构"]=="是")]#line:2519
    if OO00OOOO000OO00O0 =="药品":#line:2522
        OOO0000O0O000OOOO =OOO0000O0O000OOOO .reset_index (drop =True )#line:2523
        if "再次使用可疑药是否出现同样反应"not in OOO0000O0O000OOOO .columns :#line:2524
            showinfo (title ="错误信息",message ="导入的疑似不是药品报告表。")#line:2525
            return 0 #line:2526
        O0O00O0000OO00OOO =Countall (OOO0000O0O000OOOO ).df_org ("监测机构")#line:2528
        O0O00O0000OO00OOO =pd .merge (O0O00O0000OO00OOO ,OO0O0O0OO0OO0OO00 ,on ="监测机构",how ="left")#line:2529
        O0O00O0000OO00OOO =O0O00O0000OO00OOO [["监测机构序号","监测机构","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2530
        O0OO0O0OO0OOOO0OO =["药品数量指标","审核通过数","报告数量"]#line:2531
        O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ]=O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ].apply (lambda O00OOO0OOO0O00O00 :O00OOO0OOO0O00O00 .astype (int ))#line:2532
        O00OOO000O0OOOOO0 =Countall (OOO0000O0O000OOOO ).df_user ()#line:2534
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,O00O0000OOO0OO0OO ,on =["监测机构","单位名称"],how ="left")#line:2535
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,OO0O0O0OO0OO0OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2536
        O00OOO000O0OOOOO0 =O00OOO000O0OOOOO0 [["监测机构序号","监测机构","单位名称","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2538
        O0OO0O0OO0OOOO0OO =["药品数量指标","审核通过数","报告数量"]#line:2539
        O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ]=O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ].apply (lambda O00O0OO0OOOO0OOO0 :O00O0OO0OOOO0OOO0 .astype (int ))#line:2540
        OO000OO000000O0O0 =pd .merge (OO00O0O0000OO0O00 ,O00OOO000O0OOOOO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2542
        OO000OO000000O0O0 =OO000OO000000O0O0 [(OO000OO000000O0O0 ["审核通过数"]<1 )]#line:2543
        OO000OO000000O0O0 =OO000OO000000O0O0 [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2544
    if OO00OOOO000OO00O0 =="器械":#line:2546
        OOO0000O0O000OOOO =OOO0000O0O000OOOO .reset_index (drop =True )#line:2547
        if "产品编号"not in OOO0000O0O000OOOO .columns :#line:2548
            showinfo (title ="错误信息",message ="导入的疑似不是器械报告表。")#line:2549
            return 0 #line:2550
        O0O00O0000OO00OOO =Countall (OOO0000O0O000OOOO ).df_org ("监测机构")#line:2552
        O0O00O0000OO00OOO =pd .merge (O0O00O0000OO00OOO ,OO0O0O0OO0OO0OO00 ,on ="监测机构",how ="left")#line:2553
        O0O00O0000OO00OOO =O0O00O0000OO00OOO [["监测机构序号","监测机构","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2554
        O0OO0O0OO0OOOO0OO =["器械数量指标","审核通过数","报告数量"]#line:2555
        O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ]=O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ].apply (lambda OOO0OO00OO00OO00O :OOO0OO00OO00OO00O .astype (int ))#line:2556
        O00OOO000O0OOOOO0 =Countall (OOO0000O0O000OOOO ).df_user ()#line:2558
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,O00O0000OOO0OO0OO ,on =["监测机构","单位名称"],how ="left")#line:2559
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,OO0O0O0OO0OO0OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2560
        O00OOO000O0OOOOO0 =O00OOO000O0OOOOO0 [["监测机构序号","监测机构","单位名称","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2562
        O0OO0O0OO0OOOO0OO =["器械数量指标","审核通过数","报告数量"]#line:2563
        O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ]=O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ].apply (lambda OOO0O0OOOO00O0000 :OOO0O0OOOO00O0000 .astype (int ))#line:2564
        OO000OO000000O0O0 =pd .merge (OO00O0O0000OO0O00 ,O00OOO000O0OOOOO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2566
        OO000OO000000O0O0 =OO000OO000000O0O0 [(OO000OO000000O0O0 ["审核通过数"]<1 )]#line:2567
        OO000OO000000O0O0 =OO000OO000000O0O0 [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2568
    if OO00OOOO000OO00O0 =="化妆品":#line:2571
        OOO0000O0O000OOOO =OOO0000O0O000OOOO .reset_index (drop =True )#line:2572
        if "初步判断"not in OOO0000O0O000OOOO .columns :#line:2573
            showinfo (title ="错误信息",message ="导入的疑似不是化妆品报告表。")#line:2574
            return 0 #line:2575
        O0O00O0000OO00OOO =Countall (OOO0000O0O000OOOO ).df_org ("监测机构")#line:2577
        O0O00O0000OO00OOO =pd .merge (O0O00O0000OO00OOO ,OO0O0O0OO0OO0OO00 ,on ="监测机构",how ="left")#line:2578
        O0O00O0000OO00OOO =O0O00O0000OO00OOO [["监测机构序号","监测机构","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2579
        O0OO0O0OO0OOOO0OO =["化妆品数量指标","审核通过数","报告数量"]#line:2580
        O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ]=O0O00O0000OO00OOO [O0OO0O0OO0OOOO0OO ].apply (lambda OO00OO0OOO00OO00O :OO00OO0OOO00OO00O .astype (int ))#line:2581
        O00OOO000O0OOOOO0 =Countall (OOO0000O0O000OOOO ).df_user ()#line:2583
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,O00O0000OOO0OO0OO ,on =["监测机构","单位名称"],how ="left")#line:2584
        O00OOO000O0OOOOO0 =pd .merge (O00OOO000O0OOOOO0 ,OO0O0O0OO0OO0OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2585
        O00OOO000O0OOOOO0 =O00OOO000O0OOOOO0 [["监测机构序号","监测机构","单位名称","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2586
        O0OO0O0OO0OOOO0OO =["化妆品数量指标","审核通过数","报告数量"]#line:2587
        O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ]=O00OOO000O0OOOOO0 [O0OO0O0OO0OOOO0OO ].apply (lambda O0O0O0O0OO0OO0OO0 :O0O0O0O0OO0OO0OO0 .astype (int ))#line:2588
        OO000OO000000O0O0 =pd .merge (OO00O0O0000OO0O00 ,O00OOO000O0OOOOO0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2590
        OO000OO000000O0O0 =OO000OO000000O0O0 [(OO000OO000000O0O0 ["审核通过数"]<1 )]#line:2591
        OO000OO000000O0O0 =OO000OO000000O0O0 [["监测机构","单位名称","报告数量","审核通过数"]]#line:2592
    OOO00OO0O00000O00 =filedialog .asksaveasfilename (title =u"保存文件",initialfile =OO00OOOO000OO00O0 ,defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:2599
    OO0000OO00O0000OO =pd .ExcelWriter (OOO00OO0O00000O00 ,engine ="xlsxwriter")#line:2600
    O0O00O0000OO00OOO .to_excel (OO0000OO00O0000OO ,sheet_name ="监测机构")#line:2601
    O00OOO000O0OOOOO0 .to_excel (OO0000OO00O0000OO ,sheet_name ="上报单位")#line:2602
    OO000OO000000O0O0 .to_excel (OO0000OO00O0000OO ,sheet_name ="未上报的二级以上医疗机构")#line:2603
    OO0000OO00O0000OO .close ()#line:2604
    showinfo (title ="提示",message ="文件写入成功。")#line:2605
def TOOLS_web_view (O0O00O0000O0OOO00 ):#line:2607
    ""#line:2608
    import pybi as pbi #line:2609
    O0O00O00OO0O000O0 =pd .ExcelWriter ("temp_webview.xls")#line:2610
    O0O00O0000O0OOO00 .to_excel (O0O00O00OO0O000O0 ,sheet_name ="temp_webview")#line:2611
    O0O00O00OO0O000O0 .close ()#line:2612
    O0O00O0000O0OOO00 =pd .read_excel ("temp_webview.xls",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:2613
    O00OOOOO00O00OOO0 =pbi .set_source (O0O00O0000O0OOO00 )#line:2614
    with pbi .flowBox ():#line:2615
        for OO0O0OOOOO0OO00OO in O0O00O0000O0OOO00 .columns :#line:2616
            pbi .add_slicer (O00OOOOO00O00OOO0 [OO0O0OOOOO0OO00OO ])#line:2617
    pbi .add_table (O00OOOOO00O00OOO0 )#line:2618
    O0O0O0OOO0OOOO0OO ="temp_webview.html"#line:2619
    pbi .to_html (O0O0O0OOO0OOOO0OO )#line:2620
    webbrowser .open_new_tab (O0O0O0OOO0OOOO0OO )#line:2621
def TOOLS_Autotable_0 (OO0O00O00OO0OOOOO ,OO0OO0000OOOO0OOO ,*O00OO00OOO00OOOOO ):#line:2626
    ""#line:2627
    OOOOO0000O0OOO0OO =[O00OO00OOO00OOOOO [0 ],O00OO00OOO00OOOOO [1 ],O00OO00OOO00OOOOO [2 ]]#line:2629
    O0OO0O0OO00OOOO0O =list (set ([O00O000OOO0O0OOOO for O00O000OOO0O0OOOO in OOOOO0000O0OOO0OO if O00O000OOO0O0OOOO !='']))#line:2631
    O0OO0O0OO00OOOO0O .sort (key =OOOOO0000O0OOO0OO .index )#line:2632
    if len (O0OO0O0OO00OOOO0O )==0 :#line:2633
        showinfo (title ="提示信息",message ="分组项请选择至少一列。")#line:2634
        return 0 #line:2635
    OOO0OOOO0OOOOO00O =[O00OO00OOO00OOOOO [3 ],O00OO00OOO00OOOOO [4 ]]#line:2636
    if (O00OO00OOO00OOOOO [3 ]==""or O00OO00OOO00OOOOO [4 ]=="")and OO0OO0000OOOO0OOO in ["数据透视","分组统计"]:#line:2637
        if "报告编码"in OO0O00O00OO0OOOOO .columns :#line:2638
            OOO0OOOO0OOOOO00O [0 ]="报告编码"#line:2639
            OOO0OOOO0OOOOO00O [1 ]="nunique"#line:2640
            text .insert (END ,"值项未配置,将使用报告编码进行唯一值计数。")#line:2641
        else :#line:2642
            showinfo (title ="提示信息",message ="值项未配置。")#line:2643
            return 0 #line:2644
    if O00OO00OOO00OOOOO [4 ]=="计数":#line:2646
        OOO0OOOO0OOOOO00O [1 ]="count"#line:2647
    elif O00OO00OOO00OOOOO [4 ]=="求和":#line:2648
        OOO0OOOO0OOOOO00O [1 ]="sum"#line:2649
    elif O00OO00OOO00OOOOO [4 ]=="唯一值计数":#line:2650
        OOO0OOOO0OOOOO00O [1 ]="nunique"#line:2651
    if OO0OO0000OOOO0OOO =="分组统计":#line:2654
        TABLE_tree_Level_2 (TOOLS_deep_view (OO0O00O00OO0OOOOO ,O0OO0O0OO00OOOO0O ,OOO0OOOO0OOOOO00O ,0 ),1 ,OO0O00O00OO0OOOOO )#line:2655
    if OO0OO0000OOOO0OOO =="数据透视":#line:2657
        TABLE_tree_Level_2 (TOOLS_deep_view (OO0O00O00OO0OOOOO ,O0OO0O0OO00OOOO0O ,OOO0OOOO0OOOOO00O ,1 ),1 ,OO0O00O00OO0OOOOO )#line:2658
    if OO0OO0000OOOO0OOO =="描述性统计":#line:2660
        TABLE_tree_Level_2 (OO0O00O00OO0OOOOO [O0OO0O0OO00OOOO0O ].describe ().reset_index (),1 ,OO0O00O00OO0OOOOO )#line:2661
    if OO0OO0000OOOO0OOO =="追加外部表格信息":#line:2664
        O000OOOOOO0O0OOOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2667
        O0O0OO000OO00OOOO =[pd .read_excel (OO00OO000O00O00OO ,header =0 ,sheet_name =0 )for OO00OO000O00O00OO in O000OOOOOO0O0OOOO ]#line:2668
        OOOOO000OOOO0O00O =pd .concat (O0O0OO000OO00OOOO ,ignore_index =True ).drop_duplicates (O0OO0O0OO00OOOO0O )#line:2669
        O0O000O0000OOO0OO =pd .merge (OO0O00O00OO0OOOOO ,OOOOO000OOOO0O00O ,on =O0OO0O0OO00OOOO0O ,how ="left")#line:2670
        TABLE_tree_Level_2 (O0O000O0000OOO0OO ,1 ,O0O000O0000OOO0OO )#line:2671
    if OO0OO0000OOOO0OOO =="添加到外部表格":#line:2673
        O000OOOOOO0O0OOOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2676
        O0O0OO000OO00OOOO =[pd .read_excel (OO0OO0000OO000OO0 ,header =0 ,sheet_name =0 )for OO0OO0000OO000OO0 in O000OOOOOO0O0OOOO ]#line:2677
        OOOOO000OOOO0O00O =pd .concat (O0O0OO000OO00OOOO ,ignore_index =True ).drop_duplicates ()#line:2678
        O0O000O0000OOO0OO =pd .merge (OOOOO000OOOO0O00O ,OO0O00O00OO0OOOOO .drop_duplicates (O0OO0O0OO00OOOO0O ),on =O0OO0O0OO00OOOO0O ,how ="left")#line:2679
        TABLE_tree_Level_2 (O0O000O0000OOO0OO ,1 ,O0O000O0000OOO0OO )#line:2680
    if OO0OO0000OOOO0OOO =="饼图(XY)":#line:2683
        DRAW_make_one (OO0O00O00OO0OOOOO ,"饼图",O00OO00OOO00OOOOO [0 ],O00OO00OOO00OOOOO [1 ],"饼图")#line:2684
    if OO0OO0000OOOO0OOO =="柱状图(XY)":#line:2685
        DRAW_make_one (OO0O00O00OO0OOOOO ,"柱状图",O00OO00OOO00OOOOO [0 ],O00OO00OOO00OOOOO [1 ],"柱状图")#line:2686
    if OO0OO0000OOOO0OOO =="折线图(XY)":#line:2687
        DRAW_make_one (OO0O00O00OO0OOOOO ,"折线图",O00OO00OOO00OOOOO [0 ],O00OO00OOO00OOOOO [1 ],"折线图")#line:2688
    if OO0OO0000OOOO0OOO =="托帕斯图(XY)":#line:2689
        DRAW_make_one (OO0O00O00OO0OOOOO ,"托帕斯图",O00OO00OOO00OOOOO [0 ],O00OO00OOO00OOOOO [1 ],"托帕斯图")#line:2690
    if OO0OO0000OOOO0OOO =="堆叠柱状图（X-YZ）":#line:2691
        DRAW_make_mutibar (OO0O00O00OO0OOOOO ,OOOOO0000O0OOO0OO [1 ],OOOOO0000O0OOO0OO [2 ],OOOOO0000O0OOO0OO [0 ],OOOOO0000O0OOO0OO [1 ],OOOOO0000O0OOO0OO [2 ],"堆叠柱状图")#line:2692
def STAT_countx (OOO0OO0000OOOOO0O ):#line:2702
	""#line:2703
	return OOO0OO0000OOOOO0O .value_counts ().to_dict ()#line:2704
def STAT_countpx (OOOO0O000O00O00O0 ,OO000OO00O0000OOO ):#line:2706
	""#line:2707
	return len (OOOO0O000O00O00O0 [(OOOO0O000O00O00O0 ==OO000OO00O0000OOO )])#line:2708
def STAT_countnpx (OOOOO00OO00O00O0O ,O0O0000O0000OO000 ):#line:2710
	""#line:2711
	return len (OOOOO00OO00O00O0O [(OOOOO00OO00O00O0O not in O0O0000O0000OO000 )])#line:2712
def STAT_get_max (OO0OOOOOOO00O0O0O ):#line:2714
	""#line:2715
	return OO0OOOOOOO00O0O0O .value_counts ().max ()#line:2716
def STAT_get_mean (OO0O0O00000OOOOO0 ):#line:2718
	""#line:2719
	return round (OO0O0O00000OOOOO0 .value_counts ().mean (),2 )#line:2720
def STAT_get_std (OO000000OO00O00O0 ):#line:2722
	""#line:2723
	return round (OO000000OO00O00O0 .value_counts ().std (ddof =1 ),2 )#line:2724
def STAT_get_95ci (O0OO0000OO00O00OO ):#line:2726
	""#line:2727
	return round (np .percentile (O0OO0000OO00O00OO .value_counts (),97.5 ),2 )#line:2728
def STAT_get_mean_std_ci (O0OOOOO0OOO0O0000 ,O000O0OO00OO000OO ):#line:2730
	""#line:2731
	warnings .filterwarnings ("ignore")#line:2732
	OOO00OOO0O0O00O00 =TOOLS_strdict_to_pd (str (O0OOOOO0OOO0O0000 ))["content"].values /O000O0OO00OO000OO #line:2733
	OO00O00O00O0OO000 =round (OOO00OOO0O0O00O00 .mean (),2 )#line:2734
	OO0O0O0O000O0OOOO =round (OOO00OOO0O0O00O00 .std (ddof =1 ),2 )#line:2735
	O0OO00OO0OO0OO0OO =round (np .percentile (OOO00OOO0O0O00O00 ,97.5 ),2 )#line:2736
	return pd .Series ((OO00O00O00O0OO000 ,OO0O0O0O000O0OOOO ,O0OO00OO0OO0OO0OO ))#line:2737
def STAT_findx_value (O00000OOO00OOO0OO ,O0000OOOO00O000OO ):#line:2739
	""#line:2740
	warnings .filterwarnings ("ignore")#line:2741
	O0000O00O0OOOOOOO =TOOLS_strdict_to_pd (str (O00000OOO00OOO0OO ))#line:2742
	O0O00OOOOO00000OO =O0000O00O0OOOOOOO .where (O0000O00O0OOOOOOO ["index"]==str (O0000OOOO00O000OO ))#line:2744
	print (O0O00OOOOO00000OO )#line:2745
	return O0O00OOOOO00000OO #line:2746
def STAT_judge_x (O00O0OO0O00OOOO0O ,OOOO00OO00O0OOO0O ):#line:2748
	""#line:2749
	for OO0O0OO00000O00O0 in OOOO00OO00O0OOO0O :#line:2750
		if O00O0OO0O00OOOO0O .find (OO0O0OO00000O00O0 )>-1 :#line:2751
			return 1 #line:2752
def STAT_recent30 (O000OOO00O000OOO0 ,OO00OO0000O000O0O ):#line:2754
	""#line:2755
	import datetime #line:2756
	OOO00O0OOOO0O000O =O000OOO00O000OOO0 [(O000OOO00O000OOO0 ["报告日期"].dt .date >(datetime .date .today ()-datetime .timedelta (days =30 )))]#line:2760
	OO00O0OO0OOOOOOOO =OOO00O0OOOO0O000O .groupby (OO00OO0000O000O0O ).agg (最近30天报告数 =("报告编码","nunique"),最近30天报告严重伤害数 =("伤害",lambda OO000OO0OO0OO0OO0 :STAT_countpx (OO000OO0OO0OO0OO0 .values ,"严重伤害")),最近30天报告死亡数量 =("伤害",lambda OOOO00OO0O0OOOO0O :STAT_countpx (OOOO00OO0O0OOOO0O .values ,"死亡")),最近30天报告单位个数 =("单位名称","nunique"),).reset_index ()#line:2767
	OO00O0OO0OOOOOOOO =STAT_basic_risk (OO00O0OO0OOOOOOOO ,"最近30天报告数","最近30天报告严重伤害数","最近30天报告死亡数量","最近30天报告单位个数").fillna (0 )#line:2768
	OO00O0OO0OOOOOOOO =OO00O0OO0OOOOOOOO .rename (columns ={"风险评分":"最近30天风险评分"})#line:2770
	return OO00O0OO0OOOOOOOO #line:2771
def STAT_PPR_ROR_1 (OOO0000000O0O0O00 ,OO0O0O0OOO000OO00 ,OOO000OO0O0O0OOO0 ,O0OOOO0OOOOOOOO0O ,O0O0O0000OOOO0000 ):#line:2774
    ""#line:2775
    OO0OO00O0000O00OO =O0O0O0000OOOO0000 [(O0O0O0000OOOO0000 [OOO0000000O0O0O00 ]==OO0O0O0OOO000OO00 )]#line:2778
    OO0OO00O000OOOO00 =OO0OO00O0000O00OO .loc [OO0OO00O0000O00OO [OOO000OO0O0O0OOO0 ].str .contains (O0OOOO0OOOOOOOO0O ,na =False )]#line:2779
    O0O0OOOOO0000O0OO =O0O0O0000OOOO0000 [(O0O0O0000OOOO0000 [OOO0000000O0O0O00 ]!=OO0O0O0OOO000OO00 )]#line:2780
    O0O0OOOO0000OO00O =O0O0OOOOO0000O0OO .loc [O0O0OOOOO0000O0OO [OOO000OO0O0O0OOO0 ].str .contains (O0OOOO0OOOOOOOO0O ,na =False )]#line:2781
    O0OOO00000O0OO0OO =(len (OO0OO00O000OOOO00 ),(len (OO0OO00O0000O00OO )-len (OO0OO00O000OOOO00 )),len (O0O0OOOO0000OO00O ),(len (O0O0OOOOO0000O0OO )-len (O0O0OOOO0000OO00O )))#line:2782
    if len (OO0OO00O000OOOO00 )>0 :#line:2783
        O000O000OO000O0O0 =STAT_PPR_ROR_0 (len (OO0OO00O000OOOO00 ),(len (OO0OO00O0000O00OO )-len (OO0OO00O000OOOO00 )),len (O0O0OOOO0000OO00O ),(len (O0O0OOOOO0000O0OO )-len (O0O0OOOO0000OO00O )))#line:2784
    else :#line:2785
        O000O000OO000O0O0 =(0 ,0 ,0 ,0 ,0 )#line:2786
    OO00O00O00O0000OO =len (OO0OO00O0000O00OO )#line:2789
    if OO00O00O00O0000OO ==0 :#line:2790
        OO00O00O00O0000OO =0.5 #line:2791
    return (O0OOOO0OOOOOOOO0O ,len (OO0OO00O000OOOO00 ),round (len (OO0OO00O000OOOO00 )/OO00O00O00O0000OO *100 ,2 ),round (O000O000OO000O0O0 [0 ],2 ),round (O000O000OO000O0O0 [1 ],2 ),round (O000O000OO000O0O0 [2 ],2 ),round (O000O000OO000O0O0 [3 ],2 ),round (O000O000OO000O0O0 [4 ],2 ),str (O0OOO00000O0OO0OO ),)#line:2802
def STAT_basic_risk (O0OOO00O0O00O0O0O ,O00OO0000OO0OOO00 ,OOOO00OOO00000O00 ,O0000OO0O000O00O0 ,O0OOOO000O00OO0OO ):#line:2806
	""#line:2807
	O0OOO00O0O00O0O0O ["风险评分"]=0 #line:2808
	O0OOO00O0O00O0O0O .loc [((O0OOO00O0O00O0O0O [O00OO0000OO0OOO00 ]>=3 )&(O0OOO00O0O00O0O0O [OOOO00OOO00000O00 ]>=1 ))|(O0OOO00O0O00O0O0O [O00OO0000OO0OOO00 ]>=5 ),"风险评分"]=O0OOO00O0O00O0O0O ["风险评分"]+5 #line:2809
	O0OOO00O0O00O0O0O .loc [(O0OOO00O0O00O0O0O [OOOO00OOO00000O00 ]>=3 ),"风险评分"]=O0OOO00O0O00O0O0O ["风险评分"]+1 #line:2810
	O0OOO00O0O00O0O0O .loc [(O0OOO00O0O00O0O0O [O0000OO0O000O00O0 ]>=1 ),"风险评分"]=O0OOO00O0O00O0O0O ["风险评分"]+10 #line:2811
	O0OOO00O0O00O0O0O ["风险评分"]=O0OOO00O0O00O0O0O ["风险评分"]+O0OOO00O0O00O0O0O [O0OOOO000O00OO0OO ]/100 #line:2812
	return O0OOO00O0O00O0O0O #line:2813
def STAT_PPR_ROR_0 (O0OO0OO0OOOOO0000 ,O00000000O0OOO0OO ,O0000OOO00OO0O00O ,OOO00O0OO00OO000O ):#line:2816
    ""#line:2817
    if O0OO0OO0OOOOO0000 *O00000000O0OOO0OO *O0000OOO00OO0O00O *OOO00O0OO00OO000O ==0 :#line:2822
        O0OO0OO0OOOOO0000 =O0OO0OO0OOOOO0000 +1 #line:2823
        O00000000O0OOO0OO =O00000000O0OOO0OO +1 #line:2824
        O0000OOO00OO0O00O =O0000OOO00OO0O00O +1 #line:2825
        OOO00O0OO00OO000O =OOO00O0OO00OO000O +1 #line:2826
    OO000OO0OO0O00000 =(O0OO0OO0OOOOO0000 /(O0OO0OO0OOOOO0000 +O00000000O0OOO0OO ))/(O0000OOO00OO0O00O /(O0000OOO00OO0O00O +OOO00O0OO00OO000O ))#line:2827
    OO0OO00OO0O00OO0O =math .sqrt (1 /O0OO0OO0OOOOO0000 -1 /(O0OO0OO0OOOOO0000 +O00000000O0OOO0OO )+1 /O0000OOO00OO0O00O -1 /(O0000OOO00OO0O00O +OOO00O0OO00OO000O ))#line:2828
    O0O00OOO0OO00000O =(math .exp (math .log (OO000OO0OO0O00000 )-1.96 *OO0OO00OO0O00OO0O ),math .exp (math .log (OO000OO0OO0O00000 )+1.96 *OO0OO00OO0O00OO0O ),)#line:2832
    O00000000O000OO00 =(O0OO0OO0OOOOO0000 /O0000OOO00OO0O00O )/(O00000000O0OOO0OO /OOO00O0OO00OO000O )#line:2833
    OOOOOO00OOO0O0O00 =math .sqrt (1 /O0OO0OO0OOOOO0000 +1 /O00000000O0OOO0OO +1 /O0000OOO00OO0O00O +1 /OOO00O0OO00OO000O )#line:2834
    OO00O0000O000OOOO =(math .exp (math .log (O00000000O000OO00 )-1.96 *OOOOOO00OOO0O0O00 ),math .exp (math .log (O00000000O000OO00 )+1.96 *OOOOOO00OOO0O0O00 ),)#line:2838
    O0O00O0OO00O000OO =((O0OO0OO0OOOOO0000 *O00000000O0OOO0OO -O00000000O0OOO0OO *O0000OOO00OO0O00O )*(O0OO0OO0OOOOO0000 *O00000000O0OOO0OO -O00000000O0OOO0OO *O0000OOO00OO0O00O )*(O0OO0OO0OOOOO0000 +O00000000O0OOO0OO +O0000OOO00OO0O00O +OOO00O0OO00OO000O ))/((O0OO0OO0OOOOO0000 +O00000000O0OOO0OO )*(O0000OOO00OO0O00O +OOO00O0OO00OO000O )*(O0OO0OO0OOOOO0000 +O0000OOO00OO0O00O )*(O00000000O0OOO0OO +OOO00O0OO00OO000O ))#line:2841
    return O00000000O000OO00 ,OO00O0000O000OOOO [0 ],OO000OO0OO0O00000 ,O0O00OOO0OO00000O [0 ],O0O00O0OO00O000OO #line:2842
def STAT_find_keyword_risk (O0OO0O0OOOO00O0O0 ,OOO0O0OOO0OOOO000 ,O0OO000OO00O0OO0O ,O0O0OOOOO00000OO0 ,O0OO0O00O00OOOO0O ):#line:2844
		""#line:2845
		O00O0O00OOOO00O00 =O0OO0O0OOOO00O0O0 .groupby (OOO0O0OOO0OOOO000 ).agg (证号关键字总数量 =(O0OO000OO00O0OO0O ,"count"),包含元素个数 =(O0O0OOOOO00000OO0 ,"nunique"),包含元素 =(O0O0OOOOO00000OO0 ,STAT_countx ),).reset_index ()#line:2850
		OOO0O0O00O0OOO0O0 =OOO0O0OOO0OOOO000 .copy ()#line:2852
		OOO0O0O00O0OOO0O0 .append (O0O0OOOOO00000OO0 )#line:2853
		O00OOO0O000OOOOOO =O0OO0O0OOOO00O0O0 .groupby (OOO0O0O00O0OOO0O0 ).agg (计数 =(O0O0OOOOO00000OO0 ,"count"),严重伤害数 =("伤害",lambda O000OO0O0OO0O00O0 :STAT_countpx (O000OO0O0OO0O00O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OO0OO0OOOOOO00O :STAT_countpx (O0OO0OO0OOOOOO00O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:2860
		OOO000000O0OO00OO =OOO0O0O00O0OOO0O0 .copy ()#line:2863
		OOO000000O0OO00OO .remove ("关键字")#line:2864
		O00O0OO00000000O0 =O0OO0O0OOOO00O0O0 .groupby (OOO000000O0OO00OO ).agg (该元素总数 =(O0O0OOOOO00000OO0 ,"count"),).reset_index ()#line:2867
		O00OOO0O000OOOOOO ["证号总数"]=O0OO0O00O00OOOO0O #line:2869
		O0O0OO00O0OOO0O0O =pd .merge (O00OOO0O000OOOOOO ,O00O0O00OOOO00O00 ,on =OOO0O0OOO0OOOO000 ,how ="left")#line:2870
		if len (O0O0OO00O0OOO0O0O )>0 :#line:2875
			O0O0OO00O0OOO0O0O [['数量均值','数量标准差','数量CI']]=O0O0OO00O0OOO0O0O .包含元素 .apply (lambda OOOO0OOOOO00OOO0O :STAT_get_mean_std_ci (OOOO0OOOOO00OOO0O ,1 ))#line:2876
		return O0O0OO00O0OOO0O0O #line:2879
def STAT_find_risk (O0O0000O0O00O0O00 ,OO0OO0O0OO000OOO0 ,OO00O00OO000O00O0 ,OOOO0000000O00000 ):#line:2885
		""#line:2886
		O0OO0000000OO00O0 =O0O0000O0O00O0O00 .groupby (OO0OO0O0OO000OOO0 ).agg (证号总数量 =(OO00O00OO000O00O0 ,"count"),包含元素个数 =(OOOO0000000O00000 ,"nunique"),包含元素 =(OOOO0000000O00000 ,STAT_countx ),均值 =(OOOO0000000O00000 ,STAT_get_mean ),标准差 =(OOOO0000000O00000 ,STAT_get_std ),CI上限 =(OOOO0000000O00000 ,STAT_get_95ci ),).reset_index ()#line:2894
		O00OO00000000OOOO =OO0OO0O0OO000OOO0 .copy ()#line:2896
		O00OO00000000OOOO .append (OOOO0000000O00000 )#line:2897
		OOO0OOO0OOO0OOO00 =O0O0000O0O00O0O00 .groupby (O00OO00000000OOOO ).agg (计数 =(OOOO0000000O00000 ,"count"),严重伤害数 =("伤害",lambda OOOOO0O0O00OOO000 :STAT_countpx (OOOOO0O0O00OOO000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOOO0O0000O0O0O0 :STAT_countpx (OOOOO0O0000O0O0O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:2904
		O0OO0O0O0O0OOOOOO =pd .merge (OOO0OOO0OOO0OOO00 ,O0OO0000000OO00O0 ,on =OO0OO0O0OO000OOO0 ,how ="left")#line:2906
		O0OO0O0O0O0OOOOOO ["风险评分"]=0 #line:2908
		O0OO0O0O0O0OOOOOO ["报表类型"]="dfx_findrisk"+OOOO0000000O00000 #line:2909
		O0OO0O0O0O0OOOOOO .loc [((O0OO0O0O0O0OOOOOO ["计数"]>=3 )&(O0OO0O0O0O0OOOOOO ["严重伤害数"]>=1 )|(O0OO0O0O0O0OOOOOO ["计数"]>=5 )),"风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+5 #line:2910
		O0OO0O0O0O0OOOOOO .loc [(O0OO0O0O0O0OOOOOO ["计数"]>=(O0OO0O0O0O0OOOOOO ["均值"]+O0OO0O0O0O0OOOOOO ["标准差"])),"风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+1 #line:2911
		O0OO0O0O0O0OOOOOO .loc [(O0OO0O0O0O0OOOOOO ["计数"]>=O0OO0O0O0O0OOOOOO ["CI上限"]),"风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+1 #line:2912
		O0OO0O0O0O0OOOOOO .loc [(O0OO0O0O0O0OOOOOO ["严重伤害数"]>=3 )&(O0OO0O0O0O0OOOOOO ["风险评分"]>=7 ),"风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+1 #line:2913
		O0OO0O0O0O0OOOOOO .loc [(O0OO0O0O0O0OOOOOO ["死亡数量"]>=1 ),"风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+10 #line:2914
		O0OO0O0O0O0OOOOOO ["风险评分"]=O0OO0O0O0O0OOOOOO ["风险评分"]+O0OO0O0O0O0OOOOOO ["单位个数"]/100 #line:2915
		O0OO0O0O0O0OOOOOO =O0OO0O0O0O0OOOOOO .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2916
		return O0OO0O0O0O0OOOOOO #line:2918
def TABLE_tree_Level_2 (OO00OO0O00OO0O0OO ,OOOO0O00000OO00OO ,O000O00OOOO00OOO0 ,*O0OO0O0OO00OOO0OO ):#line:2925
    ""#line:2926
    try :#line:2928
        O0000OO0O000O000O =OO00OO0O00OO0O0OO .columns #line:2929
    except :#line:2930
        return 0 #line:2931
    if "报告编码"in OO00OO0O00OO0O0OO .columns :#line:2933
        OOOO0O00000OO00OO =0 #line:2934
    try :#line:2935
        OOOOO000OOOO00OO0 =len (np .unique (OO00OO0O00OO0O0OO ["注册证编号/曾用注册证编号"].values ))#line:2936
    except :#line:2937
        OOOOO000OOOO00OO0 =10 #line:2938
    OO00O0O0OO0O0OO00 =Toplevel ()#line:2941
    OO00O0O0OO0O0OO00 .title ("报表查看器")#line:2942
    O0OOOO0OOOOOO00O0 =OO00O0O0OO0O0OO00 .winfo_screenwidth ()#line:2943
    O0OO0O0OOOOO0000O =OO00O0O0OO0O0OO00 .winfo_screenheight ()#line:2945
    OO000OO0OO0OOOO00 =1310 #line:2947
    OOOO0O0O0OO00O000 =600 #line:2948
    O0OOOO00OO0O00O0O =(O0OOOO0OOOOOO00O0 -OO000OO0OO0OOOO00 )/2 #line:2950
    OOO0OO0OO0OO0O0OO =(O0OO0O0OOOOO0000O -OOOO0O0O0OO00O000 )/2 #line:2951
    OO00O0O0OO0O0OO00 .geometry ("%dx%d+%d+%d"%(OO000OO0OO0OOOO00 ,OOOO0O0O0OO00O000 ,O0OOOO00OO0O00O0O ,OOO0OO0OO0OO0O0OO ))#line:2952
    O0OOO00O0OOO0O00O =ttk .Frame (OO00O0O0OO0O0OO00 ,width =1310 ,height =20 )#line:2955
    O0OOO00O0OOO0O00O .pack (side =TOP )#line:2956
    O00OO000OOOOO0O00 =ttk .Frame (OO00O0O0OO0O0OO00 ,width =1310 ,height =20 )#line:2957
    O00OO000OOOOO0O00 .pack (side =BOTTOM )#line:2958
    OO0OOOO0OO0O00OO0 =ttk .Frame (OO00O0O0OO0O0OO00 ,width =1310 ,height =600 )#line:2959
    OO0OOOO0OO0O00OO0 .pack (fill ="both",expand ="false")#line:2960
    if OOOO0O00000OO00OO ==0 :#line:2964
        PROGRAM_Menubar (OO00O0O0OO0O0OO00 ,OO00OO0O00OO0O0OO ,OOOO0O00000OO00OO ,O000O00OOOO00OOO0 )#line:2965
    try :#line:2968
        O0OOOO00O00O00000 =StringVar ()#line:2969
        O0OOOO00O00O00000 .set ("产品类别")#line:2970
        def O0O0O0O0000O00O00 (*OO00O00OOO00O0000 ):#line:2971
            O0OOOO00O00O00000 .set (OOO0OO0O000O00OO0 .get ())#line:2972
        OOOO000000O000OO0 =StringVar ()#line:2973
        OOOO000000O000OO0 .set ("无源|诊断试剂")#line:2974
        OO0OO0OO0O00O0O0O =Label (O0OOO00O0OOO0O00O ,text ="")#line:2975
        OO0OO0OO0O00O0O0O .pack (side =LEFT )#line:2976
        OO0OO0OO0O00O0O0O =Label (O0OOO00O0OOO0O00O ,text ="位置：")#line:2977
        OO0OO0OO0O00O0O0O .pack (side =LEFT )#line:2978
        O0OOO000O00O0O0OO =StringVar ()#line:2979
        OOO0OO0O000O00OO0 =ttk .Combobox (O0OOO00O0OOO0O00O ,width =12 ,height =30 ,state ="readonly",textvariable =O0OOO000O00O0O0OO )#line:2982
        OOO0OO0O000O00OO0 ["values"]=OO00OO0O00OO0O0OO .columns .tolist ()#line:2983
        OOO0OO0O000O00OO0 .current (0 )#line:2984
        OOO0OO0O000O00OO0 .bind ("<<ComboboxSelected>>",O0O0O0O0000O00O00 )#line:2985
        OOO0OO0O000O00OO0 .pack (side =LEFT )#line:2986
        O000O00OOOOOO0O0O =Label (O0OOO00O0OOO0O00O ,text ="检索：")#line:2987
        O000O00OOOOOO0O0O .pack (side =LEFT )#line:2988
        OO0OO0OOOO0O0000O =Entry (O0OOO00O0OOO0O00O ,width =12 ,textvariable =OOOO000000O000OO0 ).pack (side =LEFT )#line:2989
        def OO00O0O0OO0O0O0O0 ():#line:2991
            pass #line:2992
        O00OOO000OO0O0OO0 =Button (O0OOO00O0OOO0O00O ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (OO00OO0O00OO0O0OO ),)#line:3006
        O00OOO000OO0O0OO0 .pack (side =LEFT )#line:3007
        OO00O0O0OOO0OOOO0 =Button (O0OOO00O0OOO0O00O ,text ="视图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyreadT (OO00OO0O00OO0O0OO ),1 ,O000O00OOOO00OOO0 ),)#line:3016
        if "详细描述T"not in OO00OO0O00OO0O0OO .columns :#line:3017
            OO00O0O0OOO0OOOO0 .pack (side =LEFT )#line:3018
        OO00O0O0OOO0OOOO0 =Button (O0OOO00O0OOO0O00O ,text ="网",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_web_view (OO00OO0O00OO0O0OO ),)#line:3028
        if "详细描述T"not in OO00OO0O00OO0O0OO .columns :#line:3029
            OO00O0O0OOO0OOOO0 .pack (side =LEFT )#line:3030
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="含",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .loc [OO00OO0O00OO0O0OO [O0OOOO00O00O00000 .get ()].astype (str ).str .contains (str (OOOO000000O000OO0 .get ()),na =False )],1 ,O000O00OOOO00OOO0 ,),)#line:3048
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3049
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="无",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .loc [~OO00OO0O00OO0O0OO [O0OOOO00O00O00000 .get ()].astype (str ).str .contains (str (OOOO000000O000OO0 .get ()),na =False )],1 ,O000O00OOOO00OOO0 ,),)#line:3066
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3067
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="大",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .loc [OO00OO0O00OO0O0OO [O0OOOO00O00O00000 .get ()].astype (float )>float (OOOO000000O000OO0 .get ())],1 ,O000O00OOOO00OOO0 ,),)#line:3082
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3083
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="小",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .loc [OO00OO0O00OO0O0OO [O0OOOO00O00O00000 .get ()].astype (float )<float (OOOO000000O000OO0 .get ())],1 ,O000O00OOOO00OOO0 ,),)#line:3098
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3099
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="等",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .loc [OO00OO0O00OO0O0OO [O0OOOO00O00O00000 .get ()].astype (float )==float (OOOO000000O000OO0 .get ())],1 ,O000O00OOOO00OOO0 ,),)#line:3114
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3115
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="式",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_findin (OO00OO0O00OO0O0OO ,O000O00OOOO00OOO0 ))#line:3124
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3125
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="前",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .head (int (OOOO000000O000OO0 .get ())),1 ,O000O00OOOO00OOO0 ,),)#line:3140
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3141
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="升",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .sort_values (by =(O0OOOO00O00O00000 .get ()),ascending =[True ],na_position ="last"),1 ,O000O00OOOO00OOO0 ,),)#line:3156
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3157
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="降",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO .sort_values (by =(O0OOOO00O00O00000 .get ()),ascending =[False ],na_position ="last"),1 ,O000O00OOOO00OOO0 ,),)#line:3172
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3173
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="SQL",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_sql (OO00OO0O00OO0O0OO ),)#line:3183
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3184
    except :#line:3187
        pass #line:3188
    if ini ["模式"]!="其他":#line:3191
        OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="近月",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO [(OO00OO0O00OO0O0OO ["最近30天报告单位个数"]>=1 )],1 ,O000O00OOOO00OOO0 ,),)#line:3204
        if "最近30天报告数"in OO00OO0O00OO0O0OO .columns :#line:3205
            OO000000OO000OO0O .pack (side =LEFT )#line:3206
        OOO0O0O000OO00O00 =Button (O0OOO00O0OOO0O00O ,text ="图表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (OO00OO0O00OO0O0OO ),)#line:3218
        if OOOO0O00000OO00OO !=0 :#line:3219
            OOO0O0O000OO00O00 .pack (side =LEFT )#line:3220
        def OO0000000OOOOOOO0 ():#line:3225
            pass #line:3226
        if OOOO0O00000OO00OO ==0 :#line:3229
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="精简",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyread2 (OO00OO0O00OO0O0OO ),1 ,O000O00OOOO00OOO0 ,),)#line:3243
            OO000000OO000OO0O .pack (side =LEFT )#line:3244
        if OOOO0O00000OO00OO ==0 :#line:3247
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="证号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_zhenghao (),1 ,O000O00OOOO00OOO0 ,),)#line:3261
            OO000000OO000OO0O .pack (side =LEFT )#line:3262
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OO00OO0O00OO0O0OO ).df_zhenghao ()))#line:3271
            OO000000OO000OO0O .pack (side =LEFT )#line:3272
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="批号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_pihao (),1 ,O000O00OOOO00OOO0 ,),)#line:3287
            OO000000OO000OO0O .pack (side =LEFT )#line:3288
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OO00OO0O00OO0O0OO ).df_pihao ()))#line:3297
            OO000000OO000OO0O .pack (side =LEFT )#line:3298
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="型号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_xinghao (),1 ,O000O00OOOO00OOO0 ,),)#line:3313
            OO000000OO000OO0O .pack (side =LEFT )#line:3314
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OO00OO0O00OO0O0OO ).df_xinghao ()))#line:3323
            OO000000OO000OO0O .pack (side =LEFT )#line:3324
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="规格",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_guige (),1 ,O000O00OOOO00OOO0 ,),)#line:3339
            OO000000OO000OO0O .pack (side =LEFT )#line:3340
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (OO00OO0O00OO0O0OO ).df_guige ()))#line:3349
            OO000000OO000OO0O .pack (side =LEFT )#line:3350
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="企业",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_chiyouren (),1 ,O000O00OOOO00OOO0 ,),)#line:3365
            OO000000OO000OO0O .pack (side =LEFT )#line:3366
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="县区",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_org ("监测机构"),1 ,O000O00OOOO00OOO0 ,),)#line:3382
            OO000000OO000OO0O .pack (side =LEFT )#line:3383
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="单位",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_user (),1 ,O000O00OOOO00OOO0 ,),)#line:3396
            OO000000OO000OO0O .pack (side =LEFT )#line:3397
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="年龄",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_age (),1 ,O000O00OOOO00OOO0 ,),)#line:3411
            OO000000OO000OO0O .pack (side =LEFT )#line:3412
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="时隔",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_deep_view (OO00OO0O00OO0O0OO ,["时隔"],["报告编码","nunique"],0 ),1 ,O000O00OOOO00OOO0 ,),)#line:3426
            OO000000OO000OO0O .pack (side =LEFT )#line:3427
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (OO00OO0O00OO0O0OO ).df_psur (),1 ,O000O00OOOO00OOO0 ,),)#line:3441
            if "UDI"not in OO00OO0O00OO0O0OO .columns :#line:3442
                OO000000OO000OO0O .pack (side =LEFT )#line:3443
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_get_guize2 (OO00OO0O00OO0O0OO ),1 ,O000O00OOOO00OOO0 ,),)#line:3456
            if "UDI"in OO00OO0O00OO0O0OO .columns :#line:3457
                OO000000OO000OO0O .pack (side =LEFT )#line:3458
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="发生时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_time (OO00OO0O00OO0O0OO ,"事件发生日期",0 ),)#line:3467
            OO000000OO000OO0O .pack (side =LEFT )#line:3468
            OO000000OO000OO0O =Button (O0OOO00O0OOO0O00O ,text ="报告时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_one (TOOLS_time (OO00OO0O00OO0O0OO ,"报告日期",1 ),"时间托帕斯图","time","报告总数","超级托帕斯图(严重伤害数)"),)#line:3478
            OO000000OO000OO0O .pack (side =LEFT )#line:3479
    try :#line:3485
        O000O00OOO0O0O000 =ttk .Label (O00OO000OOOOO0O00 ,text ="方法：")#line:3487
        O000O00OOO0O0O000 .pack (side =LEFT )#line:3488
        OO00O00O0O0000OOO =StringVar ()#line:3489
        OO000O000OOO0OOOO =ttk .Combobox (O00OO000OOOOO0O00 ,width =15 ,textvariable =OO00O00O0O0000OOO ,state ='readonly')#line:3490
        OO000O000OOO0OOOO ['values']=("分组统计","数据透视","描述性统计","饼图(XY)","柱状图(XY)","折线图(XY)","托帕斯图(XY)","堆叠柱状图（X-YZ）","追加外部表格信息","添加到外部表格")#line:3491
        OO000O000OOO0OOOO .pack (side =LEFT )#line:3495
        OO000O000OOO0OOOO .current (0 )#line:3496
        OO00OOO00O00000OO =ttk .Label (O00OO000OOOOO0O00 ,text ="分组列（X-Y-Z）:")#line:3497
        OO00OOO00O00000OO .pack (side =LEFT )#line:3498
        O0OOO0O0O000O0OOO =StringVar ()#line:3501
        OO0O0O00OOO0O0OO0 =ttk .Combobox (O00OO000OOOOO0O00 ,width =15 ,textvariable =O0OOO0O0O000O0OOO ,state ='readonly')#line:3502
        OO0O0O00OOO0O0OO0 ['values']=OO00OO0O00OO0O0OO .columns .tolist ()#line:3503
        OO0O0O00OOO0O0OO0 .pack (side =LEFT )#line:3504
        O00O0OOOOO000O00O =StringVar ()#line:3505
        O0OOO00O0O0OOO00O =ttk .Combobox (O00OO000OOOOO0O00 ,width =15 ,textvariable =O00O0OOOOO000O00O ,state ='readonly')#line:3506
        O0OOO00O0O0OOO00O ['values']=OO00OO0O00OO0O0OO .columns .tolist ()#line:3507
        O0OOO00O0O0OOO00O .pack (side =LEFT )#line:3508
        OO00O00O0000O0OOO =StringVar ()#line:3509
        O000OO0OOOO0O000O =ttk .Combobox (O00OO000OOOOO0O00 ,width =15 ,textvariable =OO00O00O0000O0OOO ,state ='readonly')#line:3510
        O000OO0OOOO0O000O ['values']=OO00OO0O00OO0O0OO .columns .tolist ()#line:3511
        O000OO0OOOO0O000O .pack (side =LEFT )#line:3512
        O0O00OOO0O0000OOO =StringVar ()#line:3513
        O0OOOO00O0O0O0O00 =StringVar ()#line:3514
        OO00OOO00O00000OO =ttk .Label (O00OO000OOOOO0O00 ,text ="计算列（V-M）:")#line:3515
        OO00OOO00O00000OO .pack (side =LEFT )#line:3516
        O0000O0OO00OOO0O0 =ttk .Combobox (O00OO000OOOOO0O00 ,width =10 ,textvariable =O0O00OOO0O0000OOO ,state ='readonly')#line:3518
        O0000O0OO00OOO0O0 ['values']=OO00OO0O00OO0O0OO .columns .tolist ()#line:3519
        O0000O0OO00OOO0O0 .pack (side =LEFT )#line:3520
        O00000OO000OOOO0O =ttk .Combobox (O00OO000OOOOO0O00 ,width =10 ,textvariable =O0OOOO00O0O0O0O00 ,state ='readonly')#line:3521
        O00000OO000OOOO0O ['values']=["计数","求和","唯一值计数"]#line:3522
        O00000OO000OOOO0O .pack (side =LEFT )#line:3523
        OOO0000O0O0OOOO0O =Button (O00OO000OOOOO0O00 ,text ="自助报表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_Autotable_0 (OO00OO0O00OO0O0OO ,OO000O000OOO0OOOO .get (),O0OOO0O0O000O0OOO .get (),O00O0OOOOO000O00O .get (),OO00O00O0000O0OOO .get (),O0O00OOO0O0000OOO .get (),O0OOOO00O0O0O0O00 .get (),OO00OO0O00OO0O0OO ))#line:3525
        OOO0000O0O0OOOO0O .pack (side =LEFT )#line:3526
        OOO0O0O000OO00O00 =Button (O00OO000OOOOO0O00 ,text ="去首行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO [1 :],1 ,O000O00OOOO00OOO0 ,))#line:3543
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3544
        OOO0O0O000OO00O00 =Button (O00OO000OOOOO0O00 ,text ="去尾行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (OO00OO0O00OO0O0OO [:-1 ],1 ,O000O00OOOO00OOO0 ,),)#line:3559
        OOO0O0O000OO00O00 .pack (side =LEFT )#line:3560
        OO000000OO000OO0O =Button (O00OO000OOOOO0O00 ,text ="行数:"+str (len (OO00OO0O00OO0O0OO )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:3570
        OO000000OO000OO0O .pack (side =LEFT )#line:3571
    except :#line:3574
        showinfo (title ="提示信息",message ="界面初始化失败。")#line:3575
    O0O00O0OO0000000O =OO00OO0O00OO0O0OO .values .tolist ()#line:3581
    O0O0OOO0O0OOOO0O0 =OO00OO0O00OO0O0OO .columns .values .tolist ()#line:3582
    O00OO0OO0OOOO000O =ttk .Treeview (OO0OOOO0OO0O00OO0 ,columns =O0O0OOO0O0OOOO0O0 ,show ="headings",height =45 )#line:3583
    for OOOOO0O0O00O00OOO in O0O0OOO0O0OOOO0O0 :#line:3586
        O00OO0OO0OOOO000O .heading (OOOOO0O0O00O00OOO ,text =OOOOO0O0O00O00OOO )#line:3587
    for OOO0O0O00O00O00O0 in O0O00O0OO0000000O :#line:3588
        O00OO0OO0OOOO000O .insert ("","end",values =OOO0O0O00O00O00O0 )#line:3589
    for OOOO00000OO0OOOOO in O0O0OOO0O0OOOO0O0 :#line:3591
        try :#line:3592
            O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =80 ,stretch =NO )#line:3593
            if "只剩"in OOOO00000OO0OOOOO :#line:3594
                O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =150 ,stretch =NO )#line:3595
        except :#line:3596
            pass #line:3597
    OOO000O000O0O0OO0 =["评分说明"]#line:3601
    O0000000O000O0OOO =["该单位喜好上报的品种统计","报告编码","产品名称","上报机构描述","持有人处理描述","该注册证编号/曾用注册证编号报告数量","通用名称","该批准文号报告数量","上市许可持有人名称",]#line:3614
    OOO0O0O000O0O000O =["注册证编号/曾用注册证编号","监测机构","报告月份","报告季度","单位列表","单位名称",]#line:3622
    OOO00O00OOO00OO0O =["管理类别",]#line:3626
    for OOOO00000OO0OOOOO in O0000000O000O0OOO :#line:3629
        try :#line:3630
            O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =200 ,stretch =NO )#line:3631
        except :#line:3632
            pass #line:3633
    for OOOO00000OO0OOOOO in OOO0O0O000O0O000O :#line:3636
        try :#line:3637
            O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =140 ,stretch =NO )#line:3638
        except :#line:3639
            pass #line:3640
    for OOOO00000OO0OOOOO in OOO00O00OOO00OO0O :#line:3641
        try :#line:3642
            O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =40 ,stretch =NO )#line:3643
        except :#line:3644
            pass #line:3645
    for OOOO00000OO0OOOOO in OOO000O000O0O0OO0 :#line:3646
        try :#line:3647
            O00OO0OO0OOOO000O .column (OOOO00000OO0OOOOO ,minwidth =0 ,width =800 ,stretch =NO )#line:3648
        except :#line:3649
            pass #line:3650
    try :#line:3652
        O00OO0OO0OOOO000O .column ("请选择需要查看的表格",minwidth =1 ,width =300 ,stretch =NO )#line:3655
    except :#line:3656
        pass #line:3657
    try :#line:3659
        O00OO0OO0OOOO000O .column ("详细描述T",minwidth =1 ,width =2300 ,stretch =NO )#line:3662
    except :#line:3663
        pass #line:3664
    O0OO0OOOO00O00OOO =Scrollbar (OO0OOOO0OO0O00OO0 ,orient ="vertical")#line:3666
    O0OO0OOOO00O00OOO .pack (side =RIGHT ,fill =Y )#line:3667
    O0OO0OOOO00O00OOO .config (command =O00OO0OO0OOOO000O .yview )#line:3668
    O00OO0OO0OOOO000O .config (yscrollcommand =O0OO0OOOO00O00OOO .set )#line:3669
    O0O0OO0OOOO0O00OO =Scrollbar (OO0OOOO0OO0O00OO0 ,orient ="horizontal")#line:3671
    O0O0OO0OOOO0O00OO .pack (side =BOTTOM ,fill =X )#line:3672
    O0O0OO0OOOO0O00OO .config (command =O00OO0OO0OOOO000O .xview )#line:3673
    O00OO0OO0OOOO000O .config (yscrollcommand =O0OO0OOOO00O00OOO .set )#line:3674
    def O0O0OOOO00000OO00 (OO000O0000O00O00O ,O00O0OOO0O00OO0OO ,OO0O00OO0OOO0000O ):#line:3677
        for OOOOOO0O0O0OOOO00 in O00OO0OO0OOOO000O .selection ():#line:3679
            O00O00O0OOOO00OO0 =O00OO0OO0OOOO000O .item (OOOOOO0O0O0OOOO00 ,"values")#line:3680
        O000OOO0O0000O0OO =dict (zip (O00O0OOO0O00OO0OO ,O00O00O0OOOO00OO0 ))#line:3681
        if "详细描述T"in O00O0OOO0O00OO0OO and "{"in O000OOO0O0000O0OO ["详细描述T"]:#line:3685
            O00O00000OO0OO00O =eval (O000OOO0O0000O0OO ["详细描述T"])#line:3686
            O00O00000OO0OO00O =pd .DataFrame .from_dict (O00O00000OO0OO00O ,orient ="index",columns =["content"]).reset_index ()#line:3687
            O00O00000OO0OO00O =O00O00000OO0OO00O .sort_values (by ="content",ascending =[False ],na_position ="last")#line:3688
            DRAW_make_one (O00O00000OO0OO00O ,O000OOO0O0000O0OO ["条目"],"index","content","饼图")#line:3689
            return 0 #line:3690
        if "dfx_deepview"in O000OOO0O0000O0OO ["报表类型"]:#line:3695
            OOO0O00OO0OOO0O0O =eval (O000OOO0O0000O0OO ["报表类型"][13 :])#line:3696
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O .copy ()#line:3697
            for OO0OOO00OOOO000OO in OOO0O00OO0OOO0O0O :#line:3698
                O000OO00OO00O00O0 =O000OO00OO00O00O0 [(O000OO00OO00O00O0 [OO0OOO00OOOO000OO ]==O00O00O0OOOO00OO0 [OOO0O00OO0OOO0O0O .index (OO0OOO00OOOO000OO )])].copy ()#line:3699
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_deepview"#line:3700
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3701
            return 0 #line:3702
        if "dfx_deepvie2"in O000OOO0O0000O0OO ["报表类型"]:#line:3705
            OOO0O00OO0OOO0O0O =eval (O000OOO0O0000O0OO ["报表类型"][13 :])#line:3706
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O .copy ()#line:3707
            for OO0OOO00OOOO000OO in OOO0O00OO0OOO0O0O :#line:3708
                O000OO00OO00O00O0 =O000OO00OO00O00O0 [O000OO00OO00O00O0 [OO0OOO00OOOO000OO ].str .contains (O00O00O0OOOO00OO0 [OOO0O00OO0OOO0O0O .index (OO0OOO00OOOO000OO )],na =False )].copy ()#line:3709
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_deepview"#line:3710
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3711
            return 0 #line:3712
        if "dfx_zhenghao"in O000OOO0O0000O0OO ["报表类型"]:#line:3716
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:3717
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_zhenghao"#line:3718
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3719
            return 0 #line:3720
        if ("dfx_pihao"in O000OOO0O0000O0OO ["报表类型"]or "dfx_findrisk"in O000OOO0O0000O0OO ["报表类型"]or "dfx_xinghao"in O000OOO0O0000O0OO ["报表类型"]or "dfx_guige"in O000OOO0O0000O0OO ["报表类型"])and OOOOO000OOOO00OO0 ==1 :#line:3724
            OO000O0O0O0O0O0O0 ="CLT"#line:3725
            if "pihao"in O000OOO0O0000O0OO ["报表类型"]or "产品批号"in O000OOO0O0000O0OO ["报表类型"]:#line:3726
                OO000O0O0O0O0O0O0 ="产品批号"#line:3727
            if "xinghao"in O000OOO0O0000O0OO ["报表类型"]or "型号"in O000OOO0O0000O0OO ["报表类型"]:#line:3728
                OO000O0O0O0O0O0O0 ="型号"#line:3729
            if "guige"in O000OOO0O0000O0OO ["报表类型"]or "规格"in O000OOO0O0000O0OO ["报表类型"]:#line:3730
                OO000O0O0O0O0O0O0 ="规格"#line:3731
            if "事件发生季度"in O000OOO0O0000O0OO ["报表类型"]:#line:3732
                OO000O0O0O0O0O0O0 ="事件发生季度"#line:3733
            if "事件发生月份"in O000OOO0O0000O0OO ["报表类型"]:#line:3734
                OO000O0O0O0O0O0O0 ="事件发生月份"#line:3735
            if "性别"in O000OOO0O0000O0OO ["报表类型"]:#line:3736
                OO000O0O0O0O0O0O0 ="性别"#line:3737
            if "年龄段"in O000OOO0O0000O0OO ["报表类型"]:#line:3738
                OO000O0O0O0O0O0O0 ="年龄段"#line:3739
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])&(OO0O00OO0OOO0000O [OO000O0O0O0O0O0O0 ]==O000OOO0O0000O0OO [OO000O0O0O0O0O0O0 ])].copy ()#line:3740
            O000OO00OO00O00O0 ["报表类型"]="ori_pihao"#line:3741
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3742
            return 0 #line:3743
        if ("findrisk"in O000OOO0O0000O0OO ["报表类型"]or "dfx_pihao"in O000OOO0O0000O0OO ["报表类型"]or "dfx_xinghao"in O000OOO0O0000O0OO ["报表类型"]or "dfx_guige"in O000OOO0O0000O0OO ["报表类型"])and OOOOO000OOOO00OO0 !=1 :#line:3747
            O000OO00OO00O00O0 =OO00OO0O00OO0O0OO [(OO00OO0O00OO0O0OO ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:3748
            O000OO00OO00O00O0 ["报表类型"]=O000OOO0O0000O0OO ["报表类型"]+"1"#line:3749
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,1 ,OO0O00OO0OOO0000O )#line:3750
            return 0 #line:3752
        if "dfx_org监测机构"in O000OOO0O0000O0OO ["报表类型"]:#line:3755
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["监测机构"]==O000OOO0O0000O0OO ["监测机构"])].copy ()#line:3756
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_org"#line:3757
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3758
            return 0 #line:3759
        if "dfx_org市级监测机构"in O000OOO0O0000O0OO ["报表类型"]:#line:3761
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["市级监测机构"]==O000OOO0O0000O0OO ["市级监测机构"])].copy ()#line:3762
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_org"#line:3763
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3764
            return 0 #line:3765
        if "dfx_user"in O000OOO0O0000O0OO ["报表类型"]:#line:3768
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["单位名称"]==O000OOO0O0000O0OO ["单位名称"])].copy ()#line:3769
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_user"#line:3770
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3771
            return 0 #line:3772
        if "dfx_chiyouren"in O000OOO0O0000O0OO ["报表类型"]:#line:3776
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["上市许可持有人名称"]==O000OOO0O0000O0OO ["上市许可持有人名称"])].copy ()#line:3777
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_chiyouren"#line:3778
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3779
            return 0 #line:3780
        if "dfx_chanpin"in O000OOO0O0000O0OO ["报表类型"]:#line:3782
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["产品名称"]==O000OOO0O0000O0OO ["产品名称"])].copy ()#line:3783
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_chanpin"#line:3784
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3785
            return 0 #line:3786
        if "dfx_findrisk事件发生季度1"in O000OOO0O0000O0OO ["报表类型"]:#line:3791
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])&(OO0O00OO0OOO0000O ["事件发生季度"]==O000OOO0O0000O0OO ["事件发生季度"])].copy ()#line:3792
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_findrisk事件发生季度"#line:3793
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3794
            return 0 #line:3795
        if "dfx_findrisk事件发生月份1"in O000OOO0O0000O0OO ["报表类型"]:#line:3798
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])&(OO0O00OO0OOO0000O ["事件发生月份"]==O000OOO0O0000O0OO ["事件发生月份"])].copy ()#line:3799
            O000OO00OO00O00O0 ["报表类型"]="ori_dfx_findrisk事件发生月份"#line:3800
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3801
            return 0 #line:3802
        if ("keyword_findrisk"in O000OOO0O0000O0OO ["报表类型"])and OOOOO000OOOO00OO0 ==1 :#line:3805
            OO000O0O0O0O0O0O0 ="CLT"#line:3806
            if "批号"in O000OOO0O0000O0OO ["报表类型"]:#line:3807
                OO000O0O0O0O0O0O0 ="产品批号"#line:3808
            if "事件发生季度"in O000OOO0O0000O0OO ["报表类型"]:#line:3809
                OO000O0O0O0O0O0O0 ="事件发生季度"#line:3810
            if "事件发生月份"in O000OOO0O0000O0OO ["报表类型"]:#line:3811
                OO000O0O0O0O0O0O0 ="事件发生月份"#line:3812
            if "性别"in O000OOO0O0000O0OO ["报表类型"]:#line:3813
                OO000O0O0O0O0O0O0 ="性别"#line:3814
            if "年龄段"in O000OOO0O0000O0OO ["报表类型"]:#line:3815
                OO000O0O0O0O0O0O0 ="年龄段"#line:3816
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O [(OO0O00OO0OOO0000O ["注册证编号/曾用注册证编号"]==O000OOO0O0000O0OO ["注册证编号/曾用注册证编号"])&(OO0O00OO0OOO0000O [OO000O0O0O0O0O0O0 ]==O000OOO0O0000O0OO [OO000O0O0O0O0O0O0 ])].copy ()#line:3817
            O000OO00OO00O00O0 ["关键字查找列"]=""#line:3818
            for O0O0000OO00OO00OO in TOOLS_get_list (O000OOO0O0000O0OO ["关键字查找列"]):#line:3819
                O000OO00OO00O00O0 ["关键字查找列"]=O000OO00OO00O00O0 ["关键字查找列"]+O000OO00OO00O00O0 [O0O0000OO00OO00OO ].astype ("str")#line:3820
            O000OO00OO00O00O0 =O000OO00OO00O00O0 [(O000OO00OO00O00O0 ["关键字查找列"].str .contains (O000OOO0O0000O0OO ["关键字组合"],na =False ))]#line:3821
            if str (O000OOO0O0000O0OO ["排除值"])!="nan":#line:3823
                O000OO00OO00O00O0 =O000OO00OO00O00O0 .loc [~O000OO00OO00O00O0 ["关键字查找列"].str .contains (O000OOO0O0000O0OO ["排除值"],na =False )]#line:3824
            O000OO00OO00O00O0 ["报表类型"]="ori_"+O000OOO0O0000O0OO ["报表类型"]#line:3826
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3827
            return 0 #line:3828
        if ("PSUR"in O000OOO0O0000O0OO ["报表类型"]):#line:3833
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O .copy ()#line:3834
            if ini ["模式"]=="器械":#line:3835
                O000OO00OO00O00O0 ["关键字查找列"]=O000OO00OO00O00O0 ["器械故障表现"].astype (str )+O000OO00OO00O00O0 ["伤害表现"].astype (str )+O000OO00OO00O00O0 ["使用过程"].astype (str )+O000OO00OO00O00O0 ["事件原因分析描述"].astype (str )+O000OO00OO00O00O0 ["初步处置情况"].astype (str )#line:3836
            else :#line:3837
                O000OO00OO00O00O0 ["关键字查找列"]=O000OO00OO00O00O0 ["器械故障表现"]#line:3838
            if "-其他关键字-"in str (O000OOO0O0000O0OO ["关键字标记"]):#line:3840
                O000OO00OO00O00O0 =O000OO00OO00O00O0 .loc [~O000OO00OO00O00O0 ["关键字查找列"].str .contains (O000OOO0O0000O0OO ["关键字标记"],na =False )].copy ()#line:3841
                TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3842
                return 0 #line:3843
            O000OO00OO00O00O0 =O000OO00OO00O00O0 [(O000OO00OO00O00O0 ["关键字查找列"].str .contains (O000OOO0O0000O0OO ["关键字标记"],na =False ))]#line:3846
            if str (O000OOO0O0000O0OO ["排除值"])!="没有排除值":#line:3847
                O000OO00OO00O00O0 =O000OO00OO00O00O0 .loc [~O000OO00OO00O00O0 ["关键字查找列"].str .contains (O000OOO0O0000O0OO ["排除值"],na =False )]#line:3848
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3852
            return 0 #line:3853
        if ("ROR"in O000OOO0O0000O0OO ["报表类型"]):#line:3856
            O000000OOOO0OOOO0 ={'nan':"-未定义-"}#line:3857
            OOO000000O00O0O00 =eval (O000OOO0O0000O0OO ["报表定位"],O000000OOOO0OOOO0 )#line:3858
            O000OO00OO00O00O0 =OO0O00OO0OOO0000O .copy ()#line:3859
            for OO000OO00O0OOO00O ,O00OO0OOO0O00OO00 in OOO000000O00O0O00 .items ():#line:3861
                if OO000OO00O0OOO00O =="合并列"and O00OO0OOO0O00OO00 !={}:#line:3863
                    for OOO000O0000O00OO0 ,OOO00OO000O0OOO00 in O00OO0OOO0O00OO00 .items ():#line:3864
                        if OOO00OO000O0OOO00 !="-未定义-":#line:3865
                            O0OOOOO0O0O0000O0 =TOOLS_get_list (OOO00OO000O0OOO00 )#line:3866
                            O000OO00OO00O00O0 [OOO000O0000O00OO0 ]=""#line:3867
                            for OOOO0OOO0OOOO00O0 in O0OOOOO0O0O0000O0 :#line:3868
                                O000OO00OO00O00O0 [OOO000O0000O00OO0 ]=O000OO00OO00O00O0 [OOO000O0000O00OO0 ]+O000OO00OO00O00O0 [OOOO0OOO0OOOO00O0 ].astype ("str")#line:3869
                if OO000OO00O0OOO00O =="等于"and O00OO0OOO0O00OO00 !={}:#line:3871
                    for OOO000O0000O00OO0 ,OOO00OO000O0OOO00 in O00OO0OOO0O00OO00 .items ():#line:3872
                        O000OO00OO00O00O0 =O000OO00OO00O00O0 [(O000OO00OO00O00O0 [OOO000O0000O00OO0 ]==OOO00OO000O0OOO00 )]#line:3873
                if OO000OO00O0OOO00O =="不等于"and O00OO0OOO0O00OO00 !={}:#line:3875
                    for OOO000O0000O00OO0 ,OOO00OO000O0OOO00 in O00OO0OOO0O00OO00 .items ():#line:3876
                        if OOO00OO000O0OOO00 !="-未定义-":#line:3877
                            O000OO00OO00O00O0 =O000OO00OO00O00O0 [(O000OO00OO00O00O0 [OOO000O0000O00OO0 ]!=OOO00OO000O0OOO00 )]#line:3878
                if OO000OO00O0OOO00O =="包含"and O00OO0OOO0O00OO00 !={}:#line:3880
                    for OOO000O0000O00OO0 ,OOO00OO000O0OOO00 in O00OO0OOO0O00OO00 .items ():#line:3881
                        if OOO00OO000O0OOO00 !="-未定义-":#line:3882
                            O000OO00OO00O00O0 =O000OO00OO00O00O0 .loc [O000OO00OO00O00O0 [OOO000O0000O00OO0 ].str .contains (OOO00OO000O0OOO00 ,na =False )]#line:3883
                if OO000OO00O0OOO00O =="不包含"and O00OO0OOO0O00OO00 !={}:#line:3885
                    for OOO000O0000O00OO0 ,OOO00OO000O0OOO00 in O00OO0OOO0O00OO00 .items ():#line:3886
                        if OOO00OO000O0OOO00 !="-未定义-":#line:3887
                            O000OO00OO00O00O0 =O000OO00OO00O00O0 .loc [~O000OO00OO00O00O0 [OOO000O0000O00OO0 ].str .contains (OOO00OO000O0OOO00 ,na =False )]#line:3888
            TABLE_tree_Level_2 (O000OO00OO00O00O0 ,0 ,O000OO00OO00O00O0 )#line:3890
            return 0 #line:3891
    try :#line:3895
        if O0OO0O0OO00OOO0OO [1 ]=="dfx_zhenghao":#line:3896
            O00000OO00O000OOO ="dfx_zhenghao"#line:3897
            OOO00OOO00O0O0O00 =""#line:3898
    except :#line:3899
            O00000OO00O000OOO =""#line:3900
            OOO00OOO00O0O0O00 ="近一年"#line:3901
    if (("总体评分"in OOO0OO0O000O00OO0 ["values"])and ("高峰批号均值"in OOO0OO0O000O00OO0 ["values"])and ("月份均值"in OOO0OO0O000O00OO0 ["values"]))or O00000OO00O000OOO =="dfx_zhenghao":#line:3902
            def O0O000O0O0O0O00OO (event =None ):#line:3905
                for O00OOOO000O00O000 in O00OO0OO0OOOO000O .selection ():#line:3906
                    O000OOOOO0OOOOOO0 =O00OO0OO0OOOO000O .item (O00OOOO000O00O000 ,"values")#line:3907
                OO0O00O0O00OO0OOO =dict (zip (O0O0OOO0O0OOOO0O0 ,O000OOOOO0OOOOOO0 ))#line:3908
                OOOOO00000OO0O000 =O000O00OOOO00OOO0 [(O000O00OOOO00OOO0 ["注册证编号/曾用注册证编号"]==OO0O00O0O00OO0OOO ["注册证编号/曾用注册证编号"])].copy ()#line:3909
                OOOOO00000OO0O000 ["报表类型"]=OO0O00O0O00OO0OOO ["报表类型"]+"1"#line:3910
                TABLE_tree_Level_2 (OOOOO00000OO0O000 ,1 ,O000O00OOOO00OOO0 )#line:3911
            def OO0000OOO0O000OOO (event =None ):#line:3912
                for O0OO00O000OOOO000 in O00OO0OO0OOOO000O .selection ():#line:3913
                    OO00O0OO0O00O00OO =O00OO0OO0OOOO000O .item (O0OO00O000OOOO000 ,"values")#line:3914
                OO000OO0000000O0O =dict (zip (O0O0OOO0O0OOOO0O0 ,OO00O0OO0O00O00OO ))#line:3915
                OOOO000OO0000O00O =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==OO000OO0000000O0O ["注册证编号/曾用注册证编号"])].copy ()#line:3916
                OOOO000OO0000O00O ["报表类型"]=OO000OO0000000O0O ["报表类型"]+"1"#line:3917
                TABLE_tree_Level_2 (OOOO000OO0000O00O ,1 ,O0OO0O0OO00OOO0OO [0 ])#line:3918
            def O0O000OO0O0O0O00O (O0O00O00O000O0O00 ):#line:3919
                for OO00O0000O0OOOO0O in O00OO0OO0OOOO000O .selection ():#line:3920
                    O0O0O0OOOO0000O00 =O00OO0OO0OOOO000O .item (OO00O0000O0OOOO0O ,"values")#line:3921
                OOOOOOO00000O00O0 =dict (zip (O0O0OOO0O0OOOO0O0 ,O0O0O0OOOO0000O00 ))#line:3922
                OOO0OO000OOOO0OO0 =O000O00OOOO00OOO0 [(O000O00OOOO00OOO0 ["注册证编号/曾用注册证编号"]==OOOOOOO00000O00O0 ["注册证编号/曾用注册证编号"])].copy ()#line:3925
                OOO0OO000OOOO0OO0 ["报表类型"]=OOOOOOO00000O00O0 ["报表类型"]+"1"#line:3926
                OOO000OO00O00000O =Countall (OOO0OO000OOOO0OO0 ).df_psur (O0O00O00O000O0O00 ,OOOOOOO00000O00O0 ["规整后品类"])[["关键字标记","总数量","严重比"]]#line:3927
                OOO000OO00O00000O =OOO000OO00O00000O .rename (columns ={"总数量":"最近30天总数量"})#line:3928
                OOO000OO00O00000O =OOO000OO00O00000O .rename (columns ={"严重比":"最近30天严重比"})#line:3929
                OOO0OO000OOOO0OO0 =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==OOOOOOO00000O00O0 ["注册证编号/曾用注册证编号"])].copy ()#line:3931
                OOO0OO000OOOO0OO0 ["报表类型"]=OOOOOOO00000O00O0 ["报表类型"]+"1"#line:3932
                O000OOOO0O0O0O00O =Countall (OOO0OO000OOOO0OO0 ).df_psur (O0O00O00O000O0O00 ,OOOOOOO00000O00O0 ["规整后品类"])#line:3933
                O00O00000OOO0000O =pd .merge (O000OOOO0O0O0O00O ,OOO000OO00O00000O ,on ="关键字标记",how ="left")#line:3935
                del O00O00000OOO0000O ["报表类型"]#line:3936
                O00O00000OOO0000O ["报表类型"]="PSUR"#line:3937
                TABLE_tree_Level_2 (O00O00000OOO0000O ,1 ,OOO0OO000OOOO0OO0 )#line:3939
            def OO0O0OO0OOOO00OO0 (O00O0O0O0OO0OO00O ):#line:3942
                for O0000000O00000O0O in O00OO0OO0OOOO000O .selection ():#line:3943
                    OO00OO0O0O000OOO0 =O00OO0OO0OOOO000O .item (O0000000O00000O0O ,"values")#line:3944
                OOOOOO00O0OO0O000 =dict (zip (O0O0OOO0O0OOOO0O0 ,OO00OO0O0O000OOO0 ))#line:3945
                OO000O000000O0O0O =O0OO0O0OO00OOO0OO [0 ]#line:3946
                if OOOOOO00O0OO0O000 ["规整后品类"]=="N":#line:3947
                    if O00O0O0O0OO0OO00O =="特定品种":#line:3948
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:3949
                        return 0 #line:3950
                    OO000O000000O0O0O =OO000O000000O0O0O .loc [OO000O000000O0O0O ["产品名称"].str .contains (OOOOOO00O0OO0O000 ["产品名称"],na =False )].copy ()#line:3951
                else :#line:3952
                    OO000O000000O0O0O =OO000O000000O0O0O .loc [OO000O000000O0O0O ["规整后品类"].str .contains (OOOOOO00O0OO0O000 ["规整后品类"],na =False )].copy ()#line:3953
                OO000O000000O0O0O =OO000O000000O0O0O .loc [OO000O000000O0O0O ["产品类别"].str .contains (OOOOOO00O0OO0O000 ["产品类别"],na =False )].copy ()#line:3954
                OO000O000000O0O0O ["报表类型"]=OOOOOO00O0OO0O000 ["报表类型"]+"1"#line:3956
                if O00O0O0O0OO0OO00O =="特定品种":#line:3957
                    TABLE_tree_Level_2 (Countall (OO000O000000O0O0O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OOOOOO00O0OO0O000 ["规整后品类"],OOOOOO00O0OO0O000 ["注册证编号/曾用注册证编号"]),1 ,OO000O000000O0O0O )#line:3958
                else :#line:3959
                    TABLE_tree_Level_2 (Countall (OO000O000000O0O0O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],O00O0O0O0OO0OO00O ,OOOOOO00O0OO0O000 ["注册证编号/曾用注册证编号"]),1 ,OO000O000000O0O0O )#line:3960
            def OOOOOO0O0O00O0O00 (event =None ):#line:3962
                for OOO000O0O0O0OOOOO in O00OO0OO0OOOO000O .selection ():#line:3963
                    OOO00OOO0OOO0OO00 =O00OO0OO0OOOO000O .item (OOO000O0O0O0OOOOO ,"values")#line:3964
                OOOO00O0O00O0000O =dict (zip (O0O0OOO0O0OOOO0O0 ,OOO00OOO0OOO0OO00 ))#line:3965
                OOO000O0O0O0000O0 =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==OOOO00O0O00O0000O ["注册证编号/曾用注册证编号"])].copy ()#line:3966
                OOO000O0O0O0000O0 ["报表类型"]=OOOO00O0O00O0000O ["报表类型"]+"1"#line:3967
                TABLE_tree_Level_2 (Countall (OOO000O0O0O0000O0 ).df_pihao (),1 ,OOO000O0O0O0000O0 ,)#line:3972
            def O0O0O0OO000000O00 (event =None ):#line:3974
                for O0O0OOO00OOOO00O0 in O00OO0OO0OOOO000O .selection ():#line:3975
                    O00O0O0O00O0O00O0 =O00OO0OO0OOOO000O .item (O0O0OOO00OOOO00O0 ,"values")#line:3976
                OO00OO0O000O0OO0O =dict (zip (O0O0OOO0O0OOOO0O0 ,O00O0O0O00O0O00O0 ))#line:3977
                OOO0OO000OOOOO000 =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==OO00OO0O000O0OO0O ["注册证编号/曾用注册证编号"])].copy ()#line:3978
                OOO0OO000OOOOO000 ["报表类型"]=OO00OO0O000O0OO0O ["报表类型"]+"1"#line:3979
                TABLE_tree_Level_2 (Countall (OOO0OO000OOOOO000 ).df_xinghao (),1 ,OOO0OO000OOOOO000 ,)#line:3984
            def O0OO0O0O0OO0OOO00 (event =None ):#line:3986
                for OO00OOO0OO0O0OOO0 in O00OO0OO0OOOO000O .selection ():#line:3987
                    O00O0O000OOO0OO00 =O00OO0OO0OOOO000O .item (OO00OOO0OO0O0OOO0 ,"values")#line:3988
                O0OO00OOO0O0OO00O =dict (zip (O0O0OOO0O0OOOO0O0 ,O00O0O000OOO0OO00 ))#line:3989
                O0OO0O0OOO00O0OO0 =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==O0OO00OOO0O0OO00O ["注册证编号/曾用注册证编号"])].copy ()#line:3990
                O0OO0O0OOO00O0OO0 ["报表类型"]=O0OO00OOO0O0OO00O ["报表类型"]+"1"#line:3991
                TABLE_tree_Level_2 (Countall (O0OO0O0OOO00O0OO0 ).df_user (),1 ,O0OO0O0OOO00O0OO0 ,)#line:3996
            def OOO0000OO00O00000 (event =None ):#line:3998
                for OO000OO00OOOO0OO0 in O00OO0OO0OOOO000O .selection ():#line:4000
                    O0000O0OOO0OO00OO =O00OO0OO0OOOO000O .item (OO000OO00OOOO0OO0 ,"values")#line:4001
                O000OOOOOOO0OOOOO =dict (zip (O0O0OOO0O0OOOO0O0 ,O0000O0OOO0OO00OO ))#line:4002
                OOO0O0OOOOOO0O00O =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==O000OOOOOOO0OOOOO ["注册证编号/曾用注册证编号"])].copy ()#line:4003
                OOO0O0OOOOOO0O00O ["报表类型"]=O000OOOOOOO0OOOOO ["报表类型"]+"1"#line:4004
                O00OOO0O0O00OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:4005
                if ini ["模式"]=="药品":#line:4006
                    O00OOO0O0O00OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:4007
                if ini ["模式"]=="器械":#line:4008
                    O00OOO0O0O00OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:4009
                if ini ["模式"]=="化妆品":#line:4010
                    O00OOO0O0O00OO00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:4011
                OO00O000O0000O000 =O00OOO0O0O00OO00O ["值"][3 ]+"|"+O00OOO0O0O00OO00O ["值"][4 ]#line:4012
                if ini ["模式"]=="器械":#line:4013
                    OOO0O0OOOOOO0O00O ["关键字查找列"]=OOO0O0OOOOOO0O00O ["器械故障表现"].astype (str )+OOO0O0OOOOOO0O00O ["伤害表现"].astype (str )+OOO0O0OOOOOO0O00O ["使用过程"].astype (str )+OOO0O0OOOOOO0O00O ["事件原因分析描述"].astype (str )+OOO0O0OOOOOO0O00O ["初步处置情况"].astype (str )#line:4014
                else :#line:4015
                    OOO0O0OOOOOO0O00O ["关键字查找列"]=OOO0O0OOOOOO0O00O ["器械故障表现"].astype (str )#line:4016
                OOO0O0OOOOOO0O00O =OOO0O0OOOOOO0O00O .loc [OOO0O0OOOOOO0O00O ["关键字查找列"].str .contains (OO00O000O0000O000 ,na =False )].copy ().reset_index (drop =True )#line:4017
                TABLE_tree_Level_2 (OOO0O0OOOOOO0O00O ,0 ,OOO0O0OOOOOO0O00O ,)#line:4023
            def OOO00O00000OO0O00 (event =None ):#line:4026
                for OO0O0O0O00OO0000O in O00OO0OO0OOOO000O .selection ():#line:4027
                    OOOO0O0O000000000 =O00OO0OO0OOOO000O .item (OO0O0O0O00OO0000O ,"values")#line:4028
                OOO0OO000O00O000O =dict (zip (O0O0OOO0O0OOOO0O0 ,OOOO0O0O000000000 ))#line:4029
                OOOO0O0OO0O00OO00 =O0OO0O0OO00OOO0OO [0 ][(O0OO0O0OO00OOO0OO [0 ]["注册证编号/曾用注册证编号"]==OOO0OO000O00O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4030
                OOOO0O0OO0O00OO00 ["报表类型"]=OOO0OO000O00O000O ["报表类型"]+"1"#line:4031
                TOOLS_time (OOOO0O0OO0O00OO00 ,"事件发生日期",0 )#line:4032
            def OOO0OOO00O0O000O0 (O0O00O000OOO0OOOO ,OO000O0O00O0O0OO0 ):#line:4034
                for O00O0OOOO0OO0000O in O00OO0OO0OOOO000O .selection ():#line:4036
                    O00O0O000OOOO00OO =O00OO0OO0OOOO000O .item (O00O0OOOO0OO0000O ,"values")#line:4037
                OOOO0OOOOO0O0O00O =dict (zip (O0O0OOO0O0OOOO0O0 ,O00O0O000OOOO00OO ))#line:4038
                O000O0O00O0O0000O =O0OO0O0OO00OOO0OO [0 ]#line:4039
                if OOOO0OOOOO0O0O00O ["规整后品类"]=="N":#line:4040
                    if O0O00O000OOO0OOOO =="特定品种":#line:4041
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4042
                        return 0 #line:4043
                O000O0O00O0O0000O =O000O0O00O0O0000O .loc [O000O0O00O0O0000O ["注册证编号/曾用注册证编号"].str .contains (OOOO0OOOOO0O0O00O ["注册证编号/曾用注册证编号"],na =False )].copy ()#line:4044
                O000O0O00O0O0000O ["报表类型"]=OOOO0OOOOO0O0O00O ["报表类型"]+"1"#line:4045
                if O0O00O000OOO0OOOO =="特定品种":#line:4046
                    TABLE_tree_Level_2 (Countall (O000O0O00O0O0000O ).df_find_all_keword_risk (OO000O0O00O0O0OO0 ,OOOO0OOOOO0O0O00O ["规整后品类"]),1 ,O000O0O00O0O0000O )#line:4047
                else :#line:4048
                    TABLE_tree_Level_2 (Countall (O000O0O00O0O0000O ).df_find_all_keword_risk (OO000O0O00O0O0OO0 ,O0O00O000OOO0OOOO ),1 ,O000O0O00O0O0000O )#line:4049
            OOOOO0O0O00O0000O =Menu (OO00O0O0OO0O0OO00 ,tearoff =False ,)#line:4053
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"故障表现分类（无源）",command =lambda :O0O000OO0O0O0O00O ("通用无源"))#line:4054
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"故障表现分类（有源）",command =lambda :O0O000OO0O0O0O00O ("通用有源"))#line:4055
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"故障表现分类（特定品种）",command =lambda :O0O000OO0O0O0O00O ("特定品种"))#line:4056
            OOOOO0O0O00O0000O .add_separator ()#line:4058
            if O00000OO00O000OOO =="":#line:4059
                OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"同类比较(ROR-无源)",command =lambda :OO0O0OO0OOOO00OO0 ("无源"))#line:4060
                OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"同类比较(ROR-有源)",command =lambda :OO0O0OO0OOOO00OO0 ("有源"))#line:4061
                OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"同类比较(ROR-特定品种)",command =lambda :OO0O0OO0OOOO00OO0 ("特定品种"))#line:4062
            OOOOO0O0O00O0000O .add_separator ()#line:4064
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(批号-无源)",command =lambda :OOO0OOO00O0O000O0 ("无源","产品批号"))#line:4065
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(批号-特定品种)",command =lambda :OOO0OOO00O0O000O0 ("特定品种","产品批号"))#line:4066
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(月份-无源)",command =lambda :OOO0OOO00O0O000O0 ("无源","事件发生月份"))#line:4067
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(月份-有源)",command =lambda :OOO0OOO00O0O000O0 ("有源","事件发生月份"))#line:4068
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(月份-特定品种)",command =lambda :OOO0OOO00O0O000O0 ("特定品种","事件发生月份"))#line:4069
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(季度-无源)",command =lambda :OOO0OOO00O0O000O0 ("无源","事件发生季度"))#line:4070
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(季度-有源)",command =lambda :OOO0OOO00O0O000O0 ("有源","事件发生季度"))#line:4071
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"关键字趋势(季度-特定品种)",command =lambda :OOO0OOO00O0O000O0 ("特定品种","事件发生季度"))#line:4072
            OOOOO0O0O00O0000O .add_separator ()#line:4074
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"各批号报送情况",command =OOOOOO0O0O00O0O00 )#line:4075
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"各型号报送情况",command =O0O0O0OO000000O00 )#line:4076
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"报告单位情况",command =O0OO0O0O0OO0OOO00 )#line:4077
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"事件发生时间曲线",command =OOO00O00000OO0O00 )#line:4078
            OOOOO0O0O00O0000O .add_separator ()#line:4079
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"原始数据",command =OO0000OOO0O000OOO )#line:4080
            if O00000OO00O000OOO =="":#line:4081
                OOOOO0O0O00O0000O .add_command (label ="近30天原始数据",command =O0O000O0O0O0O00OO )#line:4082
            OOOOO0O0O00O0000O .add_command (label =OOO00OOO00O0O0O00 +"高度关注(一级和二级)",command =OOO0000OO00O00000 )#line:4083
            def OOO00000OO000O0O0 (OOO000OO000OO0O0O ):#line:4085
                OOOOO0O0O00O0000O .post (OOO000OO000OO0O0O .x_root ,OOO000OO000OO0O0O .y_root )#line:4086
            OO00O0O0OO0O0OO00 .bind ("<Button-3>",OOO00000OO000O0O0 )#line:4087
    if OOOO0O00000OO00OO ==0 or "规整编码"in OO00OO0O00OO0O0OO .columns :#line:4090
        O00OO0OO0OOOO000O .bind ("<Double-1>",lambda OO0OO0OO00OOOO00O :OOO0OOO00OO0OOOOO (OO0OO0OO00OOOO00O ,OO00OO0O00OO0O0OO ))#line:4091
    if OOOO0O00000OO00OO ==1 and "规整编码"not in OO00OO0O00OO0O0OO .columns :#line:4092
        O00OO0OO0OOOO000O .bind ("<Double-1>",lambda OO0O0OOO0O000OO00 :O0O0OOOO00000OO00 (OO0O0OOO0O000OO00 ,O0O0OOO0O0OOOO0O0 ,O000O00OOOO00OOO0 ))#line:4093
    def O00OOO0OO0OO0OOOO (OO0O00OO000000OOO ,O00000000000O0OO0 ,O0O0000O00O0O0O00 ):#line:4096
        O0O000O00000000OO =[(OO0O00OO000000OOO .set (O0O0O00OO0O000OO0 ,O00000000000O0OO0 ),O0O0O00OO0O000OO0 )for O0O0O00OO0O000OO0 in OO0O00OO000000OOO .get_children ("")]#line:4097
        O0O000O00000000OO .sort (reverse =O0O0000O00O0O0O00 )#line:4098
        for OOO00OOO0O00O00O0 ,(OO000OOOO000O0000 ,O0O0000O0000O0OO0 )in enumerate (O0O000O00000000OO ):#line:4100
            OO0O00OO000000OOO .move (O0O0000O0000O0OO0 ,"",OOO00OOO0O00O00O0 )#line:4101
        OO0O00OO000000OOO .heading (O00000000000O0OO0 ,command =lambda :O00OOO0OO0OO0OOOO (OO0O00OO000000OOO ,O00000000000O0OO0 ,not O0O0000O00O0O0O00 ))#line:4104
    for O0O0O000000O000OO in O0O0OOO0O0OOOO0O0 :#line:4106
        O00OO0OO0OOOO000O .heading (O0O0O000000O000OO ,text =O0O0O000000O000OO ,command =lambda _col =O0O0O000000O000OO :O00OOO0OO0OO0OOOO (O00OO0OO0OOOO000O ,_col ,False ),)#line:4111
    def OOO0OOO00OO0OOOOO (OOOOOO00O0OO0OOOO ,O0OO000OO0O00O00O ):#line:4115
        if "规整编码"in O0OO000OO0O00O00O .columns :#line:4117
            O0OO000OO0O00O00O =O0OO000OO0O00O00O .rename (columns ={"规整编码":"报告编码"})#line:4118
        for OO0000O00OO00O0O0 in O00OO0OO0OOOO000O .selection ():#line:4120
            OO00000OOO00O0OO0 =O00OO0OO0OOOO000O .item (OO0000O00OO00O0O0 ,"values")#line:4121
            OOO00OO0OOOO00O0O =Toplevel ()#line:4124
            O00OOO0OOO00O0O00 =OOO00OO0OOOO00O0O .winfo_screenwidth ()#line:4126
            OO0O0OO000O0O0OO0 =OOO00OO0OOOO00O0O .winfo_screenheight ()#line:4128
            O000OO0OOOO000O00 =800 #line:4130
            O000O0O0O000O0O00 =600 #line:4131
            O000O00OO0OOO0O0O =(O00OOO0OOO00O0O00 -O000OO0OOOO000O00 )/2 #line:4133
            OO0000O00OOOO00O0 =(OO0O0OO000O0O0OO0 -O000O0O0O000O0O00 )/2 #line:4134
            OOO00OO0OOOO00O0O .geometry ("%dx%d+%d+%d"%(O000OO0OOOO000O00 ,O000O0O0O000O0O00 ,O000O00OO0OOO0O0O ,OO0000O00OOOO00O0 ))#line:4135
            OOOO0OOO0OO0O0OOO =ScrolledText (OOO00OO0OOOO00O0O ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:4139
            OOOO0OOO0OO0O0OOO .pack (padx =10 ,pady =10 )#line:4140
            def OOO0OO000OOO000OO (event =None ):#line:4141
                OOOO0OOO0OO0O0OOO .event_generate ('<<Copy>>')#line:4142
            def O0O000OOO00OO0O0O (O0O0O0O0O00O0OO00 ,OO0000OOO00OOOO0O ):#line:4143
                TOOLS_savetxt (O0O0O0O0O00O0OO00 ,OO0000OOO00OOOO0O ,1 )#line:4144
            O0O0O00O0O0O000O0 =Menu (OOOO0OOO0OO0O0OOO ,tearoff =False ,)#line:4145
            O0O0O00O0O0O000O0 .add_command (label ="复制",command =OOO0OO000OOO000OO )#line:4146
            O0O0O00O0O0O000O0 .add_command (label ="导出",command =lambda :PROGRAM_thread_it (O0O000OOO00OO0O0O ,OOOO0OOO0OO0O0OOO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =O0OO000OO0O00O00O .iloc [0 ,0 ],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:4147
            def O0OO0O0O0OO0O0OOO (OOOO00O00OO00000O ):#line:4149
                O0O0O00O0O0O000O0 .post (OOOO00O00OO00000O .x_root ,OOOO00O00OO00000O .y_root )#line:4150
            OOOO0OOO0OO0O0OOO .bind ("<Button-3>",O0OO0O0O0OO0O0OOO )#line:4151
            try :#line:4153
                OOO00OO0OOOO00O0O .title (str (OO00000OOO00O0OO0 [0 ]))#line:4154
                O0OO000OO0O00O00O ["报告编码"]=O0OO000OO0O00O00O ["报告编码"].astype ("str")#line:4155
                O0000OO00OO00OOO0 =O0OO000OO0O00O00O [(O0OO000OO0O00O00O ["报告编码"]==str (OO00000OOO00O0OO0 [0 ]))]#line:4156
            except :#line:4157
                pass #line:4158
            O0OOO0000O0OO00O0 =O0OO000OO0O00O00O .columns .values .tolist ()#line:4160
            for O0O0OO0O0OO0OOO00 in range (len (O0OOO0000O0OO00O0 )):#line:4161
                try :#line:4163
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="报告编码.1":#line:4164
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4165
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="产品名称":#line:4166
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4167
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="事件发生日期":#line:4168
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4169
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="是否开展了调查":#line:4170
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4171
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="市级监测机构":#line:4172
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4173
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="上报机构描述":#line:4174
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4175
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]=="持有人处理描述":#line:4176
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4177
                    if O0O0OO0O0OO0OOO00 >1 and O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 -1 ]=="持有人处理描述":#line:4178
                        OOOO0OOO0OO0O0OOO .insert (END ,"\n\n")#line:4179
                except :#line:4181
                    pass #line:4182
                try :#line:4183
                    if O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ]in ["单位名称","产品名称ori","上报机构描述","持有人处理描述","产品名称","注册证编号/曾用注册证编号","型号","规格","产品批号","上市许可持有人名称ori","上市许可持有人名称","伤害","伤害表现","器械故障表现","使用过程","事件原因分析描述","初步处置情况","调查情况","关联性评价","事件原因分析.1","具体控制措施"]:#line:4184
                        OOOO0OOO0OO0O0OOO .insert (END ,"●")#line:4185
                except :#line:4186
                    pass #line:4187
                OOOO0OOO0OO0O0OOO .insert (END ,O0OOO0000O0OO00O0 [O0O0OO0O0OO0OOO00 ])#line:4188
                OOOO0OOO0OO0O0OOO .insert (END ,"：")#line:4189
                try :#line:4190
                    OOOO0OOO0OO0O0OOO .insert (END ,O0000OO00OO00OOO0 .iloc [0 ,O0O0OO0O0OO0OOO00 ])#line:4191
                except :#line:4192
                    OOOO0OOO0OO0O0OOO .insert (END ,OO00000OOO00O0OO0 [O0O0OO0O0OO0OOO00 ])#line:4193
                OOOO0OOO0OO0O0OOO .insert (END ,"\n")#line:4194
            OOOO0OOO0OO0O0OOO .config (state =DISABLED )#line:4195
    O00OO0OO0OOOO000O .pack ()#line:4197
def TOOLS_get_guize2 (O0OOO000000OO0OOO ):#line:4200
	""#line:4201
	OO00O0OO00O0O0OOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4202
	OO0O00O00OOOOO0O0 =pd .read_excel (OO00O0OO00O0O0OOO ,header =0 ,sheet_name ="器械")#line:4203
	O0OO0O0O0O0O00OOO =OO0O00O00OOOOO0O0 [["适用范围列","适用范围"]].drop_duplicates ("适用范围")#line:4204
	text .insert (END ,O0OO0O0O0O0O00OOO )#line:4205
	text .see (END )#line:4206
	OOOO0O00OO0O00000 =Toplevel ()#line:4207
	OOOO0O00OO0O00000 .title ('切换通用规则')#line:4208
	OO0OO00OOOO000OO0 =OOOO0O00OO0O00000 .winfo_screenwidth ()#line:4209
	OO0O0O0OOOO0O00O0 =OOOO0O00OO0O00000 .winfo_screenheight ()#line:4211
	OOOOOOO0OOOO000O0 =450 #line:4213
	O00000OO0OOO0OO0O =100 #line:4214
	OO0OO0OO00OOOOO0O =(OO0OO00OOOO000OO0 -OOOOOOO0OOOO000O0 )/2 #line:4216
	O0OO000OOO0OOOOO0 =(OO0O0O0OOOO0O00O0 -O00000OO0OOO0OO0O )/2 #line:4217
	OOOO0O00OO0O00000 .geometry ("%dx%d+%d+%d"%(OOOOOOO0OOOO000O0 ,O00000OO0OOO0OO0O ,OO0OO0OO00OOOOO0O ,O0OO000OOO0OOOOO0 ))#line:4218
	O0OOO0OOOOO0OOOO0 =Label (OOOO0O00OO0O00000 ,text ="查找位置：器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况")#line:4219
	O0OOO0OOOOO0OOOO0 .pack ()#line:4220
	O00OOO0OO0OO00O00 =Label (OOOO0O00OO0O00000 ,text ="请选择您所需要的通用规则关键字：")#line:4221
	O00OOO0OO0OO00O00 .pack ()#line:4222
	def O0OO0O00O0O00OO00 (*O0000O00OO00O0O00 ):#line:4223
		OO00O0O0OOOOOO00O .set (OOOO00O0OO00O0OO0 .get ())#line:4224
	OO00O0O0OOOOOO00O =StringVar ()#line:4225
	OOOO00O0OO00O0OO0 =ttk .Combobox (OOOO0O00OO0O00000 ,width =14 ,height =30 ,state ="readonly",textvariable =OO00O0O0OOOOOO00O )#line:4226
	OOOO00O0OO00O0OO0 ["values"]=O0OO0O0O0O0O00OOO ["适用范围"].to_list ()#line:4227
	OOOO00O0OO00O0OO0 .current (0 )#line:4228
	OOOO00O0OO00O0OO0 .bind ("<<ComboboxSelected>>",O0OO0O00O0O00OO00 )#line:4229
	OOOO00O0OO00O0OO0 .pack ()#line:4230
	OO0O000OO0O0O000O =LabelFrame (OOOO0O00OO0O00000 )#line:4233
	O00OO0O00O000O00O =Button (OO0O000OO0O0O000O ,text ="确定",width =10 ,command =lambda :OOO0OOO00O0000OOO (OO0O00O00OOOOO0O0 ,OO00O0O0OOOOOO00O .get ()))#line:4234
	O00OO0O00O000O00O .pack (side =LEFT ,padx =1 ,pady =1 )#line:4235
	OO0O000OO0O0O000O .pack ()#line:4236
	def OOO0OOO00O0000OOO (O0O0OOO00O000O000 ,O0OO000O00O0OO0OO ):#line:4238
		O0O000O00OO000OO0 =O0O0OOO00O000O000 .loc [O0O0OOO00O000O000 ["适用范围"].str .contains (O0OO000O00O0OO0OO ,na =False )].copy ().reset_index (drop =True )#line:4239
		TABLE_tree_Level_2 (Countall (O0OOO000000OO0OOO ).df_psur ("特定品种作为通用关键字",O0O000O00OO000OO0 ),1 ,O0OOO000000OO0OOO )#line:4240
def TOOLS_findin (OO0O00OO0OO00000O ,OOO0OO0O0000OO00O ):#line:4241
	""#line:4242
	O000O0OOO0OO00O00 =Toplevel ()#line:4243
	O000O0OOO0OO00O00 .title ('高级查找')#line:4244
	O00000O0O0OOO0OOO =O000O0OOO0OO00O00 .winfo_screenwidth ()#line:4245
	O000OOOO0OO00OO0O =O000O0OOO0OO00O00 .winfo_screenheight ()#line:4247
	O0000O0OOO0O0OO0O =400 #line:4249
	OO000OO00OOOO0O00 =120 #line:4250
	O0OO0OOO0O0000O0O =(O00000O0O0OOO0OOO -O0000O0OOO0O0OO0O )/2 #line:4252
	O0O00O00000OO0O0O =(O000OOOO0OO00OO0O -OO000OO00OOOO0O00 )/2 #line:4253
	O000O0OOO0OO00O00 .geometry ("%dx%d+%d+%d"%(O0000O0OOO0O0OO0O ,OO000OO00OOOO0O00 ,O0OO0OOO0O0000O0O ,O0O00O00000OO0O0O ))#line:4254
	OOOO00O000OOO0OO0 =Label (O000O0OOO0OO00O00 ,text ="需要查找的关键字（用|隔开）：")#line:4255
	OOOO00O000OOO0OO0 .pack ()#line:4256
	OOOO00O00OOO0O00O =Label (O000O0OOO0OO00O00 ,text ="在哪些列查找（用|隔开）：")#line:4257
	OO0OOO00OOO0OO00O =Entry (O000O0OOO0OO00O00 ,width =80 )#line:4259
	OO0OOO00OOO0OO00O .insert (0 ,"破裂|断裂")#line:4260
	O0OOO000O0O000000 =Entry (O000O0OOO0OO00O00 ,width =80 )#line:4261
	O0OOO000O0O000000 .insert (0 ,"器械故障表现|伤害表现")#line:4262
	OO0OOO00OOO0OO00O .pack ()#line:4263
	OOOO00O00OOO0O00O .pack ()#line:4264
	O0OOO000O0O000000 .pack ()#line:4265
	O0OOO0O00OOOO00OO =LabelFrame (O000O0OOO0OO00O00 )#line:4266
	O0OOO0OO0O000OO0O =Button (O0OOO0O00OOOO00OO ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (TABLE_tree_Level_2 ,OOOO00O0OOOO000OO (OO0OOO00OOO0OO00O .get (),O0OOO000O0O000000 .get (),OO0O00OO0OO00000O ),1 ,OOO0OO0O0000OO00O ))#line:4267
	O0OOO0OO0O000OO0O .pack (side =LEFT ,padx =1 ,pady =1 )#line:4268
	O0OOO0O00OOOO00OO .pack ()#line:4269
	def OOOO00O0OOOO000OO (O0OO0O0O0O0O000O0 ,OOOOOO0000OO0OO0O ,O0O0000OO0O0OO0OO ):#line:4272
		O0O0000OO0O0OO0OO ["关键字查找列10"]="######"#line:4273
		for O0O0O0OOO0O0O000O in TOOLS_get_list (OOOOOO0000OO0OO0O ):#line:4274
			O0O0000OO0O0OO0OO ["关键字查找列10"]=O0O0000OO0O0OO0OO ["关键字查找列10"].astype (str )+O0O0000OO0O0OO0OO [O0O0O0OOO0O0O000O ].astype (str )#line:4275
		O0O0000OO0O0OO0OO =O0O0000OO0O0OO0OO .loc [O0O0000OO0O0OO0OO ["关键字查找列10"].str .contains (O0OO0O0O0O0O000O0 ,na =False )]#line:4276
		del O0O0000OO0O0OO0OO ["关键字查找列10"]#line:4277
		return O0O0000OO0O0OO0OO #line:4278
def PROGRAM_about ():#line:4280
    ""#line:4281
    O0OOOOOOOOOOOOOO0 =" 佛山市食品药品检验检测中心 \n(佛山市药品不良反应监测中心)\n蔡权周（QQ或微信411703730）\n仅供政府设立的不良反应监测机构使用。"#line:4282
    showinfo (title ="关于",message =O0OOOOOOOOOOOOOO0 )#line:4283
def PROGRAM_thread_it (O0O0O000O000OO0OO ,*O0OO0OOO0O000OOOO ):#line:4286
    ""#line:4287
    O0O00OO0O0O0O0000 =threading .Thread (target =O0O0O000O000OO0OO ,args =O0OO0OOO0O000OOOO )#line:4289
    O0O00OO0O0O0O0000 .setDaemon (True )#line:4291
    O0O00OO0O0O0O0000 .start ()#line:4293
def PROGRAM_Menubar (O000OO0O0O00000O0 ,O0O00OOO0O0OOOO00 ,OOO00OOO00000O000 ,O0O0O0OOOO0OO000O ):#line:4294
	""#line:4295
	if ini ["模式"]=="其他":#line:4296
		return 0 #line:4297
	OO0000OO0OOOOOOO0 =Menu (O000OO0O0O00000O0 )#line:4298
	O000OO0O0O00000O0 .config (menu =OO0000OO0OOOOOOO0 )#line:4300
	O0O0O0O00O0O00O00 =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4304
	OO0000OO0OOOOOOO0 .add_cascade (label ="信号检测",menu =O0O0O0O00O0O00O00 )#line:4305
	O0O0O0O00O0O00O00 .add_command (label ="数量比例失衡监测-证号内批号",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_findrisk ("产品批号"),1 ,O0O0O0OOOO0OO000O ))#line:4308
	O0O0O0O00O0O00O00 .add_command (label ="数量比例失衡监测-证号内季度",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_findrisk ("事件发生季度"),1 ,O0O0O0OOOO0OO000O ))#line:4310
	O0O0O0O00O0O00O00 .add_command (label ="数量比例失衡监测-证号内月份",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_findrisk ("事件发生月份"),1 ,O0O0O0OOOO0OO000O ))#line:4312
	O0O0O0O00O0O00O00 .add_command (label ="数量比例失衡监测-证号内性别",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_findrisk ("性别"),1 ,O0O0O0OOOO0OO000O ))#line:4314
	O0O0O0O00O0O00O00 .add_command (label ="数量比例失衡监测-证号内年龄段",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_findrisk ("年龄段"),1 ,O0O0O0OOOO0OO000O ))#line:4316
	O0O0O0O00O0O00O00 .add_separator ()#line:4318
	O0O0O0O00O0O00O00 .add_command (label ="关键字检测（同证号内不同批号比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_find_all_keword_risk ("产品批号"),1 ,O0O0O0OOOO0OO000O ))#line:4320
	O0O0O0O00O0O00O00 .add_command (label ="关键字检测（同证号内不同月份比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_find_all_keword_risk ("事件发生月份"),1 ,O0O0O0OOOO0OO000O ))#line:4322
	O0O0O0O00O0O00O00 .add_command (label ="关键字检测（同证号内不同季度比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_find_all_keword_risk ("事件发生季度"),1 ,O0O0O0OOOO0OO000O ))#line:4324
	O0O0O0O00O0O00O00 .add_command (label ="关键字检测（同证号内不同性别比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_find_all_keword_risk ("性别"),1 ,O0O0O0OOOO0OO000O ))#line:4326
	O0O0O0O00O0O00O00 .add_command (label ="关键字检测（同证号内不同年龄段比对）",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_find_all_keword_risk ("年龄段"),1 ,O0O0O0OOOO0OO000O ))#line:4328
	O0O0O0O00O0O00O00 .add_separator ()#line:4330
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同证号的批号间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","产品批号"]),1 ,O0O0O0OOOO0OO000O ))#line:4332
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同证号的月份间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生月份"]),1 ,O0O0O0OOOO0OO000O ))#line:4334
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同证号的季度间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生季度"]),1 ,O0O0O0OOOO0OO000O ))#line:4336
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同证号的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","年龄段"]),1 ,O0O0O0OOOO0OO000O ))#line:4338
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同证号的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","性别"]),1 ,O0O0O0OOOO0OO000O ))#line:4340
	O0O0O0O00O0O00O00 .add_separator ()#line:4342
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同品名的证号间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]),1 ,O0O0O0OOOO0OO000O ))#line:4344
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同品名的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","规整后品类","产品名称","年龄段"]),1 ,O0O0O0OOOO0OO000O ))#line:4346
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同品名的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","规整后品类","产品名称","性别"]),1 ,O0O0O0OOOO0OO000O ))#line:4348
	O0O0O0O00O0O00O00 .add_separator ()#line:4350
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同类别的名称间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","产品名称"]),1 ,O0O0O0OOOO0OO000O ))#line:4352
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同类别的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","年龄段"]),1 ,O0O0O0OOOO0OO000O ))#line:4354
	O0O0O0O00O0O00O00 .add_command (label ="关键字ROR-页面内同类别的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_ror (["产品类别","性别"]),1 ,O0O0O0OOOO0OO000O ))#line:4356
	O0O0O0O00O0O00O00 .add_separator ()#line:4367
	if ini ["模式"]=="药品":#line:4368
		O0O0O0O00O0O00O00 .add_command (label ="新的不良反应检测(证号)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0O0O0OOOO0OO000O ,"证号"))#line:4371
		O0O0O0O00O0O00O00 .add_command (label ="新的不良反应检测(品种)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0O0O0OOOO0OO000O ,"品种"))#line:4374
	OOO0OOO000O0OOOOO =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4377
	OO0000OO0OOOOOOO0 .add_cascade (label ="简报制作",menu =OOO0OOO000O0OOOOO )#line:4378
	OOO0OOO000O0OOOOO .add_command (label ="药品简报",command =lambda :TOOLS_autocount (O0O00OOO0O0OOOO00 ,"药品"))#line:4381
	OOO0OOO000O0OOOOO .add_command (label ="器械简报",command =lambda :TOOLS_autocount (O0O00OOO0O0OOOO00 ,"器械"))#line:4383
	OOO0OOO000O0OOOOO .add_command (label ="化妆品简报",command =lambda :TOOLS_autocount (O0O00OOO0O0OOOO00 ,"化妆品"))#line:4385
	OOO0000OOOOO0OOO0 =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4389
	OO0000OO0OOOOOOO0 .add_cascade (label ="品种评价",menu =OOO0000OOOOO0OOO0 )#line:4390
	OOO0000OOOOO0OOO0 .add_command (label ="报告年份",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"报告年份",-1 ))#line:4392
	OOO0000OOOOO0OOO0 .add_command (label ="发生年份",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"事件发生年份",-1 ))#line:4394
	OOO0000OOOOO0OOO0 .add_separator ()#line:4395
	OOO0000OOOOO0OOO0 .add_command (label ="怀疑/并用",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"怀疑/并用",1 ))#line:4397
	OOO0000OOOOO0OOO0 .add_command (label ="涉及企业",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"上市许可持有人名称",1 ))#line:4399
	OOO0000OOOOO0OOO0 .add_command (label ="产品名称",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"产品名称",1 ))#line:4401
	OOO0000OOOOO0OOO0 .add_command (label ="注册证号",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_zhenghao (),1 ,O0O0O0OOOO0OO000O ))#line:4403
	OOO0000OOOOO0OOO0 .add_separator ()#line:4404
	OOO0000OOOOO0OOO0 .add_command (label ="年龄段分布",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"年龄段",1 ))#line:4406
	OOO0000OOOOO0OOO0 .add_command (label ="性别分布",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"性别",1 ))#line:4408
	OOO0000OOOOO0OOO0 .add_command (label ="年龄性别分布",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_age (),1 ,O0O0O0OOOO0OO000O ,))#line:4410
	OOO0000OOOOO0OOO0 .add_separator ()#line:4411
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应发生时间",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"时隔",1 ))#line:4413
	OOO0000OOOOO0OOO0 .add_command (label ="报告类型-严重程度",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"报告类型-严重程度",1 ))#line:4416
	OOO0000OOOOO0OOO0 .add_command (label ="停药减药后反应是否减轻或消失",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"停药减药后反应是否减轻或消失",1 ))#line:4418
	OOO0000OOOOO0OOO0 .add_command (label ="再次使用可疑药是否出现同样反应",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"再次使用可疑药是否出现同样反应",1 ))#line:4420
	OOO0000OOOOO0OOO0 .add_command (label ="对原患疾病影响",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"对原患疾病影响",1 ))#line:4422
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应结果",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"不良反应结果",1 ))#line:4424
	OOO0000OOOOO0OOO0 .add_command (label ="报告单位关联性评价",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"关联性评价",1 ))#line:4426
	OOO0000OOOOO0OOO0 .add_separator ()#line:4427
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应转归情况",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"不良反应结果2",4 ))#line:4429
	OOO0000OOOOO0OOO0 .add_command (label ="关联性评价汇总",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"关联性评价汇总",5 ))#line:4431
	OOO0000OOOOO0OOO0 .add_separator ()#line:4435
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应-术语",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"器械故障表现",0 ))#line:4437
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应器官系统-术语",command =lambda :TABLE_tree_Level_2 (Countall (O0O00OOO0O0OOOO00 ).df_psur (),1 ,O0O0O0OOOO0OO000O ))#line:4439
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"不良反应-code",2 ))#line:4441
	OOO0000OOOOO0OOO0 .add_command (label ="不良反应器官系统-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"不良反应-code",3 ))#line:4443
	OOO0000OOOOO0OOO0 .add_separator ()#line:4445
	OOO0000OOOOO0OOO0 .add_command (label ="疾病名称-术语",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"相关疾病信息[疾病名称]-术语",0 ))#line:4447
	OOO0000OOOOO0OOO0 .add_command (label ="疾病名称-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"相关疾病信息[疾病名称]-code",2 ))#line:4449
	OOO0000OOOOO0OOO0 .add_command (label ="疾病器官系统-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"相关疾病信息[疾病名称]-code",3 ))#line:4451
	OOO0000OOOOO0OOO0 .add_separator ()#line:4452
	OOO0000OOOOO0OOO0 .add_command (label ="适应症-术语",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"治疗适应症-术语",0 ))#line:4454
	OOO0000OOOOO0OOO0 .add_command (label ="适应症-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"治疗适应症-code",2 ))#line:4456
	OOO0000OOOOO0OOO0 .add_command (label ="适应症器官系统-由code转化",command =lambda :STAT_pinzhong (O0O00OOO0O0OOOO00 ,"治疗适应症-code",3 ))#line:4458
	OOO0O0O0OOO0OOOOO =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4460
	OO0000OO0OOOOOOO0 .add_cascade (label ="基础研究",menu =OOO0O0O0OOO0OOOOO )#line:4461
	OOO0O0O0OOO0OOOOO .add_command (label ="基础信息批量操作（品名）",command =lambda :TOOLS_ror_mode1 (O0O00OOO0O0OOOO00 ,"产品名称"))#line:4463
	OOO0O0O0OOO0OOOOO .add_command (label ="器官系统ROR批量操作（品名）",command =lambda :TOOLS_ror_mode2 (O0O00OOO0O0OOOO00 ,"产品名称"))#line:4465
	OOO0O0O0OOO0OOOOO .add_command (label ="ADR-ROR批量操作（品名）",command =lambda :TOOLS_ror_mode3 (O0O00OOO0O0OOOO00 ,"产品名称"))#line:4467
	O000O000O0O000O00 =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4468
	OO0000OO0OOOOOOO0 .add_cascade (label ="风险预警",menu =O000O000O0O000O00 )#line:4469
	O000O000O0O000O00 .add_command (label ="预警（单日）",command =lambda :TOOLS_keti (O0O00OOO0O0OOOO00 ))#line:4471
	O000O000O0O000O00 .add_command (label ="事件分布（器械）",command =lambda :TOOLS_get_guize2 (O0O00OOO0O0OOOO00 ))#line:4474
	O000OO00OO0OOO0O0 =Menu (OO0000OO0OOOOOOO0 ,tearoff =0 )#line:4481
	OO0000OO0OOOOOOO0 .add_cascade (label ="实用工具",menu =O000OO00OO0OOO0O0 )#line:4482
	O000OO00OO0OOO0O0 .add_command (label ="数据规整（报告单位）",command =lambda :TOOL_guizheng (O0O00OOO0O0OOOO00 ,2 ,False ))#line:4486
	O000OO00OO0OOO0O0 .add_command (label ="数据规整（产品名称）",command =lambda :TOOL_guizheng (O0O00OOO0O0OOOO00 ,3 ,False ))#line:4488
	O000OO00OO0OOO0O0 .add_command (label ="数据规整（自定义）",command =lambda :TOOL_guizheng (O0O00OOO0O0OOOO00 ,0 ,False ))#line:4490
	O000OO00OO0OOO0O0 .add_separator ()#line:4492
	O000OO00OO0OOO0O0 .add_command (label ="原始导入",command =TOOLS_fileopen )#line:4494
	O000OO00OO0OOO0O0 .add_command (label ="脱敏保存",command =lambda :TOOLS_data_masking (O0O00OOO0O0OOOO00 ))#line:4496
	O000OO00OO0OOO0O0 .add_separator ()#line:4497
	O000OO00OO0OOO0O0 .add_command (label ="批量筛选（默认）",command =lambda :TOOLS_xuanze (O0O00OOO0O0OOOO00 ,1 ))#line:4499
	O000OO00OO0OOO0O0 .add_command (label ="批量筛选（自定义）",command =lambda :TOOLS_xuanze (O0O00OOO0O0OOOO00 ,0 ))#line:4501
	O000OO00OO0OOO0O0 .add_separator ()#line:4502
	O000OO00OO0OOO0O0 .add_command (label ="评价人员（广东化妆品）",command =lambda :TOOL_person (O0O00OOO0O0OOOO00 ))#line:4504
	O000OO00OO0OOO0O0 .add_separator ()#line:4505
	O000OO00OO0OOO0O0 .add_command (label ="意见反馈",command =lambda :PROGRAM_helper (["","  药械妆不良反应报表统计分析工作站","  开发者：蔡权周","  邮箱：411703730@qq.com","  微信号：sysucai","  手机号：18575757461"]))#line:4509
	O000OO00OO0OOO0O0 .add_command (label ="更改用户组",command =lambda :PROGRAM_thread_it (display_random_number ))#line:4511
def PROGRAM_helper (OO0O00O00O0O00OOO ):#line:4515
    ""#line:4516
    OOOO0OO00000OOO0O =Toplevel ()#line:4517
    OOOO0OO00000OOO0O .title ("信息查看")#line:4518
    OOOO0OO00000OOO0O .geometry ("700x500")#line:4519
    OO0O0OOOOO0O00000 =Scrollbar (OOOO0OO00000OOO0O )#line:4521
    O0OO00OO00OO0O0OO =Text (OOOO0OO00000OOO0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:4522
    OO0O0OOOOO0O00000 .pack (side =RIGHT ,fill =Y )#line:4523
    O0OO00OO00OO0O0OO .pack ()#line:4524
    OO0O0OOOOO0O00000 .config (command =O0OO00OO00OO0O0OO .yview )#line:4525
    O0OO00OO00OO0O0OO .config (yscrollcommand =OO0O0OOOOO0O00000 .set )#line:4526
    for OO0O0OO0O000OO0O0 in OO0O00O00O0O00OOO :#line:4528
        O0OO00OO00OO0O0OO .insert (END ,OO0O0OO0O000OO0O0 )#line:4529
        O0OO00OO00OO0O0OO .insert (END ,"\n")#line:4530
    def O0O0OOO0O0O00O0O0 (event =None ):#line:4533
        O0OO00OO00OO0O0OO .event_generate ('<<Copy>>')#line:4534
    OOO0000OO0OO0OOOO =Menu (O0OO00OO00OO0O0OO ,tearoff =False ,)#line:4537
    OOO0000OO0OO0OOOO .add_command (label ="复制",command =O0O0OOO0O0O00O0O0 )#line:4538
    def OOOOO0OOO0OOOOOO0 (OO0OOOO00O0O000OO ):#line:4539
         OOO0000OO0OO0OOOO .post (OO0OOOO00O0O000OO .x_root ,OO0OOOO00O0O000OO .y_root )#line:4540
    O0OO00OO00OO0O0OO .bind ("<Button-3>",OOOOO0OOO0OOOOOO0 )#line:4541
    O0OO00OO00OO0O0OO .config (state =DISABLED )#line:4543
def PROGRAM_change_schedule (OOO0O00O00000OO00 ,O00O000OOO0O0O00O ):#line:4545
    ""#line:4546
    canvas .coords (fill_rec ,(5 ,5 ,(OOO0O00O00000OO00 /O00O000OOO0O0O00O )*680 ,25 ))#line:4548
    root .update ()#line:4549
    x .set (str (round (OOO0O00O00000OO00 /O00O000OOO0O0O00O *100 ,2 ))+"%")#line:4550
    if round (OOO0O00O00000OO00 /O00O000OOO0O0O00O *100 ,2 )==100.00 :#line:4551
        x .set ("完成")#line:4552
def PROGRAM_showWelcome ():#line:4555
    ""#line:4556
    OO0O0O0OOO0O0O00O =roox .winfo_screenwidth ()#line:4557
    OO00OO0O00O00OOOO =roox .winfo_screenheight ()#line:4559
    roox .overrideredirect (True )#line:4561
    roox .attributes ("-alpha",1 )#line:4562
    OOO0OOO00O0O0OOOO =(OO0O0O0OOO0O0O00O -475 )/2 #line:4563
    OO0O0OOOO00O0O0O0 =(OO00OO0O00O00OOOO -200 )/2 #line:4564
    roox .geometry ("675x130+%d+%d"%(OOO0OOO00O0O0OOOO ,OO0O0OOOO00O0O0O0 ))#line:4566
    roox ["bg"]="green"#line:4567
    OOOOO0OO0O00OOOOO =Label (roox ,text =title_all2 ,fg ="white",bg ="green",font =("微软雅黑",20 ))#line:4570
    OOOOO0OO0O00OOOOO .place (x =0 ,y =15 ,width =675 ,height =90 )#line:4571
    O00O000OOO000000O =Label (roox ,text ="仅供监测机构使用 ",fg ="white",bg ="black",font =("微软雅黑",15 ))#line:4574
    O00O000OOO000000O .place (x =0 ,y =90 ,width =675 ,height =40 )#line:4575
def PROGRAM_closeWelcome ():#line:4578
    ""#line:4579
    for O00O00000OOO00OO0 in range (2 ):#line:4580
        root .attributes ("-alpha",0 )#line:4581
        time .sleep (1 )#line:4582
    root .attributes ("-alpha",1 )#line:4583
    roox .destroy ()#line:4584
class Countall ():#line:4599
	""#line:4600
	def __init__ (O000OOOO0OOOO0O0O ,OO000OO000O0OOOOO ):#line:4601
		""#line:4602
		O000OOOO0OOOO0O0O .df =OO000OO000O0OOOOO #line:4603
		O000OOOO0OOOO0O0O .mode =ini ["模式"]#line:4604
	def df_org (O000OOOO0000OOO0O ,OO00O00000OOO0OOO ):#line:4606
		""#line:4607
		OO0O0O00OOOO0OOOO =O000OOOO0000OOO0O .df .drop_duplicates (["报告编码"]).groupby ([OO00O00000OOO0OOO ]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOO0O0O0OOO0OOOO0 :STAT_countpx (OOO0O0O0OOO0OOOO0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO0OOO0O0O0O0O0O :STAT_countpx (OOO0OOO0O0O0O0O0O .values ,"死亡")),超时报告数 =("超时标记",lambda O0O00000O00OO00O0 :STAT_countpx (O0O00000O00OO00O0 .values ,1 )),有源 =("产品类别",lambda O000000OOOO0O00O0 :STAT_countpx (O000000OOOO0O00O0 .values ,"有源")),无源 =("产品类别",lambda O0O0OO0OOOO00O000 :STAT_countpx (O0O0OO0OOOO00O000 .values ,"无源")),体外诊断试剂 =("产品类别",lambda O000O0O0O0OOO0OO0 :STAT_countpx (O000O0O0O0OOO0OO0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda O0000O0O0O000000O :STAT_countpx (O0000O0O0O000000O .values ,"Ⅲ类")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4622
		O0000OOO00OOOOOO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量","单位个数"]#line:4624
		OO0O0O00OOOO0OOOO .loc ["合计"]=OO0O0O00OOOO0OOOO [O0000OOO00OOOOOO0 ].apply (lambda OOOO0O0000OO0OO00 :OOOO0O0000OO0OO00 .sum ())#line:4625
		OO0O0O00OOOO0OOOO [O0000OOO00OOOOOO0 ]=OO0O0O00OOOO0OOOO [O0000OOO00OOOOOO0 ].apply (lambda OO0OO0O000O000O0O :OO0OO0O000O000O0O .astype (int ))#line:4626
		OO0O0O00OOOO0OOOO .iloc [-1 ,0 ]="合计"#line:4627
		OO0O0O00OOOO0OOOO ["严重比"]=round ((OO0O0O00OOOO0OOOO ["严重伤害数"]+OO0O0O00OOOO0OOOO ["死亡数量"])/OO0O0O00OOOO0OOOO ["报告数量"]*100 ,2 )#line:4629
		OO0O0O00OOOO0OOOO ["Ⅲ类比"]=round ((OO0O0O00OOOO0OOOO ["三类数量"])/OO0O0O00OOOO0OOOO ["报告数量"]*100 ,2 )#line:4630
		OO0O0O00OOOO0OOOO ["超时比"]=round ((OO0O0O00OOOO0OOOO ["超时报告数"])/OO0O0O00OOOO0OOOO ["报告数量"]*100 ,2 )#line:4631
		OO0O0O00OOOO0OOOO ["报表类型"]="dfx_org"+OO00O00000OOO0OOO #line:4632
		if ini ["模式"]=="药品":#line:4635
			del OO0O0O00OOOO0OOOO ["有源"]#line:4637
			del OO0O0O00OOOO0OOOO ["无源"]#line:4638
			del OO0O0O00OOOO0OOOO ["体外诊断试剂"]#line:4639
			OO0O0O00OOOO0OOOO =OO0O0O00OOOO0OOOO .rename (columns ={"三类数量":"新的和严重的数量"})#line:4640
			OO0O0O00OOOO0OOOO =OO0O0O00OOOO0OOOO .rename (columns ={"Ⅲ类比":"新严比"})#line:4641
		return OO0O0O00OOOO0OOOO #line:4643
	def df_user (O0OO0O0O0O000OO0O ):#line:4647
		""#line:4648
		O0OO0O0O0O000OO0O .df ["医疗机构类别"]=O0OO0O0O0O000OO0O .df ["医疗机构类别"].fillna ("未填写")#line:4649
		OOO0000000O0OO0OO =O0OO0O0O0O000OO0O .df .drop_duplicates (["报告编码"]).groupby (["监测机构","单位名称","医疗机构类别"]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda O0O0OOOOOOOO0O0O0 :STAT_countpx (O0O0OOOOOOOO0O0O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO0000OO000O0OO0 :STAT_countpx (OOO0000OO000O0OO0 .values ,"死亡")),超时报告数 =("超时标记",lambda O0O000000OO00OOOO :STAT_countpx (O0O000000OO00OOOO .values ,1 )),有源 =("产品类别",lambda O00OOOOOO00O00OO0 :STAT_countpx (O00OOOOOO00O00OO0 .values ,"有源")),无源 =("产品类别",lambda O000O0OO0OO00OO0O :STAT_countpx (O000O0OO0OO00OO0O .values ,"无源")),体外诊断试剂 =("产品类别",lambda OO0OO0OO0O0O00OO0 :STAT_countpx (OO0OO0OO0O0O00OO0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda OO0OOO0OOOOOOOO00 :STAT_countpx (OO0OOO0OOOOOOOO00 .values ,"Ⅲ类")),产品数量 =("产品名称","nunique"),产品清单 =("产品名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4664
		OOOO0O0OOO00O0O00 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量"]#line:4667
		OOO0000000O0OO0OO .loc ["合计"]=OOO0000000O0OO0OO [OOOO0O0OOO00O0O00 ].apply (lambda O0OO0O0OO0O00OOO0 :O0OO0O0OO0O00OOO0 .sum ())#line:4668
		OOO0000000O0OO0OO [OOOO0O0OOO00O0O00 ]=OOO0000000O0OO0OO [OOOO0O0OOO00O0O00 ].apply (lambda O0O0OOOOO0000OOO0 :O0O0OOOOO0000OOO0 .astype (int ))#line:4669
		OOO0000000O0OO0OO .iloc [-1 ,0 ]="合计"#line:4670
		OOO0000000O0OO0OO ["严重比"]=round ((OOO0000000O0OO0OO ["严重伤害数"]+OOO0000000O0OO0OO ["死亡数量"])/OOO0000000O0OO0OO ["报告数量"]*100 ,2 )#line:4672
		OOO0000000O0OO0OO ["Ⅲ类比"]=round ((OOO0000000O0OO0OO ["三类数量"])/OOO0000000O0OO0OO ["报告数量"]*100 ,2 )#line:4673
		OOO0000000O0OO0OO ["超时比"]=round ((OOO0000000O0OO0OO ["超时报告数"])/OOO0000000O0OO0OO ["报告数量"]*100 ,2 )#line:4674
		OOO0000000O0OO0OO ["报表类型"]="dfx_user"#line:4675
		if ini ["模式"]=="药品":#line:4677
			del OOO0000000O0OO0OO ["有源"]#line:4679
			del OOO0000000O0OO0OO ["无源"]#line:4680
			del OOO0000000O0OO0OO ["体外诊断试剂"]#line:4681
			OOO0000000O0OO0OO =OOO0000000O0OO0OO .rename (columns ={"三类数量":"新的和严重的数量"})#line:4682
			OOO0000000O0OO0OO =OOO0000000O0OO0OO .rename (columns ={"Ⅲ类比":"新严比"})#line:4683
		return OOO0000000O0OO0OO #line:4685
	def df_zhenghao (OO000O00O00OO00OO ):#line:4690
		""#line:4691
		OOOO00OOO0O0O000O =OO000O00O00OO00OO .df .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("注册证编号/曾用注册证编号","count"),严重伤害数 =("伤害",lambda OOO00OOO0O0OOOO0O :STAT_countpx (OOO00OOO0O0OOOO0O .values ,"严重伤害")),死亡数量 =("伤害",lambda O00OOO0O00OO0OO0O :STAT_countpx (O00OOO0O00OO0OO0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),待评价数 =("持有人报告状态",lambda OO0OO00000O0OO00O :STAT_countpx (OO0OO00000O0OO00O .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O00O000O000OOO0OO :STAT_countpx (O00O000O000OOO0OO .values ,"严重伤害待评价")),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:4706
		OOOO00OOO0O0O000O =STAT_basic_risk (OOOO00OOO0O0O000O ,"证号计数","严重伤害数","死亡数量","单位个数")#line:4707
		OOOO00OOO0O0O000O =pd .merge (OOOO00OOO0O0O000O ,STAT_recent30 (OO000O00O00OO00OO .df ,["注册证编号/曾用注册证编号"]),on =["注册证编号/曾用注册证编号"],how ="left")#line:4709
		OOOO00OOO0O0O000O ["最近30天报告数"]=OOOO00OOO0O0O000O ["最近30天报告数"].fillna (0 ).astype (int )#line:4710
		OOOO00OOO0O0O000O ["最近30天报告严重伤害数"]=OOOO00OOO0O0O000O ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:4711
		OOOO00OOO0O0O000O ["最近30天报告死亡数量"]=OOOO00OOO0O0O000O ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:4712
		OOOO00OOO0O0O000O ["最近30天报告单位个数"]=OOOO00OOO0O0O000O ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:4713
		OOOO00OOO0O0O000O ["最近30天风险评分"]=OOOO00OOO0O0O000O ["最近30天风险评分"].fillna (0 ).astype (int )#line:4714
		OOOO00OOO0O0O000O ["报表类型"]="dfx_zhenghao"#line:4716
		if ini ["模式"]=="药品":#line:4718
			OOOO00OOO0O0O000O =OOOO00OOO0O0O000O .rename (columns ={"待评价数":"新的数量"})#line:4719
			OOOO00OOO0O0O000O =OOOO00OOO0O0O000O .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4720
		return OOOO00OOO0O0O000O #line:4722
	def df_pihao (O0O0O000OOO00000O ):#line:4724
		""#line:4725
		O0O00OOO0O0OOO0OO =O0O0O000OOO00000O .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("产品批号","count"),严重伤害数 =("伤害",lambda O0OO00O00O0OOO000 :STAT_countpx (O0OO00O00O0OOO000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O0O00OO00OO0OOO :STAT_countpx (O0O0O00OO00OO0OOO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),待评价数 =("持有人报告状态",lambda OOOOOO00O00O00O0O :STAT_countpx (OOOOOO00O00O00O0O .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OOOO00O0000OO0000 :STAT_countpx (OOOO00O0000OO0000 .values ,"严重伤害待评价")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:4738
		O0O00OOO0O0OOO0OO =STAT_basic_risk (O0O00OOO0O0OOO0OO ,"批号计数","严重伤害数","死亡数量","单位个数")#line:4741
		O0O00OOO0O0OOO0OO =pd .merge (O0O00OOO0O0OOO0OO ,STAT_recent30 (O0O0O000OOO00000O .df ,["注册证编号/曾用注册证编号","产品批号"]),on =["注册证编号/曾用注册证编号","产品批号"],how ="left")#line:4743
		O0O00OOO0O0OOO0OO ["最近30天报告数"]=O0O00OOO0O0OOO0OO ["最近30天报告数"].fillna (0 ).astype (int )#line:4744
		O0O00OOO0O0OOO0OO ["最近30天报告严重伤害数"]=O0O00OOO0O0OOO0OO ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:4745
		O0O00OOO0O0OOO0OO ["最近30天报告死亡数量"]=O0O00OOO0O0OOO0OO ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:4746
		O0O00OOO0O0OOO0OO ["最近30天报告单位个数"]=O0O00OOO0O0OOO0OO ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:4747
		O0O00OOO0O0OOO0OO ["最近30天风险评分"]=O0O00OOO0O0OOO0OO ["最近30天风险评分"].fillna (0 ).astype (int )#line:4748
		O0O00OOO0O0OOO0OO ["报表类型"]="dfx_pihao"#line:4750
		if ini ["模式"]=="药品":#line:4751
			O0O00OOO0O0OOO0OO =O0O00OOO0O0OOO0OO .rename (columns ={"待评价数":"新的数量"})#line:4752
			O0O00OOO0O0OOO0OO =O0O00OOO0O0OOO0OO .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4753
		return O0O00OOO0O0OOO0OO #line:4754
	def df_xinghao (O0OO00OO0O000O0O0 ):#line:4756
		""#line:4757
		O0O00OOO0O000OO0O =O0OO00OO0O000O0O0 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("型号","count"),严重伤害数 =("伤害",lambda O00O000000O0O0OO0 :STAT_countpx (O00O000000O0O0OO0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0000OO00000O0O0O :STAT_countpx (O0000OO00000O0O0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),待评价数 =("持有人报告状态",lambda O00O00OO000O000OO :STAT_countpx (O00O00OO000O000OO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0O00000000O0O0OO :STAT_countpx (O0O00000000O0O0OO .values ,"严重伤害待评价")),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:4770
		O0O00OOO0O000OO0O ["报表类型"]="dfx_xinghao"#line:4771
		if ini ["模式"]=="药品":#line:4772
			O0O00OOO0O000OO0O =O0O00OOO0O000OO0O .rename (columns ={"待评价数":"新的数量"})#line:4773
			O0O00OOO0O000OO0O =O0O00OOO0O000OO0O .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4774
		return O0O00OOO0O000OO0O #line:4776
	def df_guige (OO0O0O00O0O0000OO ):#line:4778
		""#line:4779
		O0O0OO0O0OO0OOOO0 =OO0O0O00O0O0000OO .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (规格计数 =("规格","count"),严重伤害数 =("伤害",lambda O00OOOOO00O0O0O0O :STAT_countpx (O00OOOOO00O0O0O0O .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OO0O000000O0O0O :STAT_countpx (O0OO0O000000O0O0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),待评价数 =("持有人报告状态",lambda OO00OO0OO0OO000O0 :STAT_countpx (OO00OO0OO0OO000O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OOOOO00O0000OOOOO :STAT_countpx (OOOOO00O0000OOOOO .values ,"严重伤害待评价")),).sort_values (by ="规格计数",ascending =[False ],na_position ="last").reset_index ()#line:4792
		O0O0OO0O0OO0OOOO0 ["报表类型"]="dfx_guige"#line:4793
		if ini ["模式"]=="药品":#line:4794
			O0O0OO0O0OO0OOOO0 =O0O0OO0O0OO0OOOO0 .rename (columns ={"待评价数":"新的数量"})#line:4795
			O0O0OO0O0OO0OOOO0 =O0O0OO0O0OO0OOOO0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:4796
		return O0O0OO0O0OO0OOOO0 #line:4798
	def df_findrisk (OOOOOOOO0000O00OO ,O0OOOOO0OO0O00000 ):#line:4800
		""#line:4801
		if O0OOOOO0OO0O00000 =="产品批号":#line:4802
			return STAT_find_risk (OOOOOOOO0000O00OO .df [(OOOOOOOO0000O00OO .df ["产品类别"]!="有源")],["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",O0OOOOO0OO0O00000 )#line:4803
		else :#line:4804
			return STAT_find_risk (OOOOOOOO0000O00OO .df ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",O0OOOOO0OO0O00000 )#line:4805
	def df_find_all_keword_risk (O00O0OOO00OO0O0OO ,O00O00O0OOO0OO0OO ,*O0OOOO0O000OOOO00 ):#line:4807
		""#line:4808
		O00O0000O0OO0O00O =O00O0OOO00OO0O0OO .df .copy ()#line:4810
		O00000O000O00OO0O =time .time ()#line:4811
		OO00OO0O00O00OO00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4812
		if "报告类型-新的"in O00O0000O0OO0O00O .columns :#line:4813
			O0O0O0O0OOOOOOOOO ="药品"#line:4814
		else :#line:4815
			O0O0O0O0OOOOOOOOO ="器械"#line:4816
		OOOO0OOOO00O00OO0 =pd .read_excel (OO00OO0O00O00OO00 ,header =0 ,sheet_name =O0O0O0O0OOOOOOOOO ).reset_index (drop =True )#line:4817
		try :#line:4820
			if len (O0OOOO0O000OOOO00 [0 ])>0 :#line:4821
				OOOO0OOOO00O00OO0 =OOOO0OOOO00O00OO0 .loc [OOOO0OOOO00O00OO0 ["适用范围"].str .contains (O0OOOO0O000OOOO00 [0 ],na =False )].copy ().reset_index (drop =True )#line:4822
		except :#line:4823
			pass #line:4824
		OOO00O000OO0OO00O =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]#line:4826
		OO00O00OO000O0O0O =OOO00O000OO0OO00O [-1 ]#line:4827
		O0000O000OO0OO0O0 =O00O0000O0OO0O00O .groupby (OOO00O000OO0OO00O ).agg (总数量 =(OO00O00OO000O0O0O ,"count"),严重伤害数 =("伤害",lambda O00OO0O0OOOO00OOO :STAT_countpx (O00OO0O0OOOO00OOO .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0O0O0O0000OO0O0 :STAT_countpx (OO0O0O0O0000OO0O0 .values ,"死亡")),)#line:4832
		OO00O00OO000O0O0O =OOO00O000OO0OO00O [-1 ]#line:4833
		O00O0O0OOO0OOO00O =OOO00O000OO0OO00O .copy ()#line:4835
		O00O0O0OOO0OOO00O .append (O00O00O0OOO0OO0OO )#line:4836
		O0O000O000OOO00O0 =O00O0000O0OO0O00O .groupby (O00O0O0OOO0OOO00O ).agg (该元素总数量 =(OO00O00OO000O0O0O ,"count"),).reset_index ()#line:4839
		O0000O000OO0OO0O0 =O0000O000OO0OO0O0 [(O0000O000OO0OO0O0 ["总数量"]>=3 )].reset_index ()#line:4842
		OOO0O00OOO0OO0000 =[]#line:4843
		OO0O000O0OOOOOO0O =0 #line:4847
		O0OOO000OO0O0O000 =int (len (O0000O000OO0OO0O0 ))#line:4848
		for O0O0O000OO0O00OO0 ,O00O000O0O0OO0OOO ,OO00O0O0000OOO0OO ,O0OO00O00OO00O0OO in zip (O0000O000OO0OO0O0 ["产品名称"].values ,O0000O000OO0OO0O0 ["产品类别"].values ,O0000O000OO0OO0O0 [OO00O00OO000O0O0O ].values ,O0000O000OO0OO0O0 ["总数量"].values ):#line:4849
			OO0O000O0OOOOOO0O +=1 #line:4850
			if (time .time ()-O00000O000O00OO0O )>3 :#line:4852
				root .attributes ("-topmost",True )#line:4853
				PROGRAM_change_schedule (OO0O000O0OOOOOO0O ,O0OOO000OO0O0O000 )#line:4854
				root .attributes ("-topmost",False )#line:4855
			OO0OO0000OOOOO000 =O00O0000O0OO0O00O [(O00O0000O0OO0O00O [OO00O00OO000O0O0O ]==OO00O0O0000OOO0OO )].copy ()#line:4856
			OOOO0OOOO00O00OO0 ["SELECT"]=OOOO0OOOO00O00OO0 .apply (lambda OOOO0000OOOO0O00O :(OOOO0000OOOO0O00O ["适用范围"]in O0O0O000OO0O00OO0 )or (OOOO0000OOOO0O00O ["适用范围"]in O00O000O0O0OO0OOO )or (OOOO0000OOOO0O00O ["适用范围"]=="通用"),axis =1 )#line:4857
			O0OO00OO00000O00O =OOOO0OOOO00O00OO0 [(OOOO0OOOO00O00OO0 ["SELECT"]==True )].reset_index ()#line:4858
			if len (O0OO00OO00000O00O )>0 :#line:4859
				for OOOOO00O0OOOOOOO0 ,O000OO00000OOOOO0 ,O0OO0OOOOO0O000O0 in zip (O0OO00OO00000O00O ["值"].values ,O0OO00OO00000O00O ["查找位置"].values ,O0OO00OO00000O00O ["排除值"].values ):#line:4861
					O0OOOOOO00O0OOO00 =OO0OO0000OOOOO000 .copy ()#line:4862
					O00000O00O0O00O00 =TOOLS_get_list (OOOOO00O0OOOOOOO0 )[0 ]#line:4863
					O0OOOOOO00O0OOO00 ["关键字查找列"]=""#line:4865
					for OO0OO00000OOOOOOO in TOOLS_get_list (O000OO00000OOOOO0 ):#line:4866
						O0OOOOOO00O0OOO00 ["关键字查找列"]=O0OOOOOO00O0OOO00 ["关键字查找列"]+O0OOOOOO00O0OOO00 [OO0OO00000OOOOOOO ].astype ("str")#line:4867
					O0OOOOOO00O0OOO00 .loc [O0OOOOOO00O0OOO00 ["关键字查找列"].str .contains (OOOOO00O0OOOOOOO0 ,na =False ),"关键字"]=O00000O00O0O00O00 #line:4869
					if str (O0OO0OOOOO0O000O0 )!="nan":#line:4872
						O0OOOOOO00O0OOO00 =O0OOOOOO00O0OOO00 .loc [~O0OOOOOO00O0OOO00 ["关键字查找列"].str .contains (O0OO0OOOOO0O000O0 ,na =False )].copy ()#line:4873
					if (len (O0OOOOOO00O0OOO00 ))<1 :#line:4875
						continue #line:4876
					O000OOO0OO0OOO000 =STAT_find_keyword_risk (O0OOOOOO00O0OOO00 ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","关键字"],"关键字",O00O00O0OOO0OO0OO ,int (O0OO00O00OO00O0OO ))#line:4878
					if len (O000OOO0OO0OOO000 )>0 :#line:4879
						O000OOO0OO0OOO000 ["关键字组合"]=OOOOO00O0OOOOOOO0 #line:4880
						O000OOO0OO0OOO000 ["排除值"]=O0OO0OOOOO0O000O0 #line:4881
						O000OOO0OO0OOO000 ["关键字查找列"]=O000OO00000OOOOO0 #line:4882
						OOO0O00OOO0OO0000 .append (O000OOO0OO0OOO000 )#line:4883
		O0O00OO0OOOO0OOO0 =pd .concat (OOO0O00OOO0OO0000 )#line:4887
		O0O00OO0OOOO0OOO0 =pd .merge (O0O00OO0OOOO0OOO0 ,O0O000O000OOO00O0 ,on =O00O0O0OOO0OOO00O ,how ="left")#line:4890
		O0O00OO0OOOO0OOO0 ["关键字数量比例"]=round (O0O00OO0OOOO0OOO0 ["计数"]/O0O00OO0OOOO0OOO0 ["该元素总数量"],2 )#line:4891
		O0O00OO0OOOO0OOO0 =O0O00OO0OOOO0OOO0 .reset_index (drop =True )#line:4893
		if len (O0O00OO0OOOO0OOO0 )>0 :#line:4894
			O0O00OO0OOOO0OOO0 ["风险评分"]=0 #line:4895
			O0O00OO0OOOO0OOO0 ["报表类型"]="keyword_findrisk"+O00O00O0OOO0OO0OO #line:4896
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["计数"]>=3 ),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+3 #line:4897
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["计数"]>=(O0O00OO0OOOO0OOO0 ["数量均值"]+O0O00OO0OOOO0OOO0 ["数量标准差"])),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+1 #line:4898
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["计数"]>=O0O00OO0OOOO0OOO0 ["数量CI"]),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+1 #line:4899
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["关键字数量比例"]>0.5 )&(O0O00OO0OOOO0OOO0 ["计数"]>=3 ),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+1 #line:4900
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["严重伤害数"]>=3 ),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+1 #line:4901
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["单位个数"]>=3 ),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+1 #line:4902
			O0O00OO0OOOO0OOO0 .loc [(O0O00OO0OOOO0OOO0 ["死亡数量"]>=1 ),"风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+10 #line:4903
			O0O00OO0OOOO0OOO0 ["风险评分"]=O0O00OO0OOOO0OOO0 ["风险评分"]+O0O00OO0OOOO0OOO0 ["单位个数"]/100 #line:4904
			O0O00OO0OOOO0OOO0 =O0O00OO0OOOO0OOO0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:4905
		print ("耗时：",(time .time ()-O00000O000O00OO0O ))#line:4911
		return O0O00OO0OOOO0OOO0 #line:4912
	def df_ror (OOOO0O0O0OOOOOO0O ,OO0O00O00OO0O000O ,*O0O0O0O0OO00OO00O ):#line:4915
		""#line:4916
		OOO00O0000OOOOO0O =OOOO0O0O0OOOOOO0O .df .copy ()#line:4918
		OO0O0OO00OOO0OOOO =time .time ()#line:4919
		OOO0O00000O0OO00O =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4920
		if "报告类型-新的"in OOO00O0000OOOOO0O .columns :#line:4921
			O0O0O000OOOOOOOOO ="药品"#line:4922
		else :#line:4924
			O0O0O000OOOOOOOOO ="器械"#line:4925
		O0O00OO00O0OO0000 =pd .read_excel (OOO0O00000O0OO00O ,header =0 ,sheet_name =O0O0O000OOOOOOOOO ).reset_index (drop =True )#line:4926
		if "css"in OOO00O0000OOOOO0O .columns :#line:4929
			OO000O0O0O0O00OOO =OOO00O0000OOOOO0O .copy ()#line:4930
			OO000O0O0O0O00OOO ["器械故障表现"]=OO000O0O0O0O00OOO ["器械故障表现"].fillna ("未填写")#line:4931
			OO000O0O0O0O00OOO ["器械故障表现"]=OO000O0O0O0O00OOO ["器械故障表现"].str .replace ("*","",regex =False )#line:4932
			OO00O00OOO00000O0 ="use("+str ("器械故障表现")+").file"#line:4933
			O00OOO000O0O0O00O =str (Counter (TOOLS_get_list0 (OO00O00OOO00000O0 ,OO000O0O0O0O00OOO ,1000 ))).replace ("Counter({","{")#line:4934
			O00OOO000O0O0O00O =O00OOO000O0O0O00O .replace ("})","}")#line:4935
			O00OOO000O0O0O00O =ast .literal_eval (O00OOO000O0O0O00O )#line:4936
			O0O00OO00O0OO0000 =pd .DataFrame .from_dict (O00OOO000O0O0O00O ,orient ="index",columns =["计数"]).reset_index ()#line:4937
			O0O00OO00O0OO0000 ["适用范围列"]="产品类别"#line:4938
			O0O00OO00O0OO0000 ["适用范围"]="无源"#line:4939
			O0O00OO00O0OO0000 ["查找位置"]="伤害表现"#line:4940
			O0O00OO00O0OO0000 ["值"]=O0O00OO00O0OO0000 ["index"]#line:4941
			O0O00OO00O0OO0000 ["排除值"]="-没有排除值-"#line:4942
			del O0O00OO00O0OO0000 ["index"]#line:4943
		O00OO0OOO00O000O0 =OO0O00O00OO0O000O [-2 ]#line:4946
		OO000OO0O0OO000OO =OO0O00O00OO0O000O [-1 ]#line:4947
		O0OO0000OO00O0OO0 =OO0O00O00OO0O000O [:-1 ]#line:4948
		try :#line:4951
			if len (O0O0O0O0OO00OO00O [0 ])>0 :#line:4952
				O00OO0OOO00O000O0 =OO0O00O00OO0O000O [-3 ]#line:4953
				O0O00OO00O0OO0000 =O0O00OO00O0OO0000 .loc [O0O00OO00O0OO0000 ["适用范围"].str .contains (O0O0O0O0OO00OO00O [0 ],na =False )].copy ().reset_index (drop =True )#line:4954
				O0O0OO0OOO00O0O00 =OOO00O0000OOOOO0O .groupby (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (该元素总数量 =(OO000OO0O0OO000OO ,"count"),该元素严重伤害数 =("伤害",lambda O00OO00OO00OO0OO0 :STAT_countpx (O00OO00OO00OO0OO0 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda OO0OOOOO000OO0000 :STAT_countpx (OO0OOOOO000OO0000 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:4961
				OO0OOO00000OOO0OO =OOO00O0000OOOOO0O .groupby (["产品类别","规整后品类"]).agg (所有元素总数量 =(O00OO0OOO00O000O0 ,"count"),所有元素严重伤害数 =("伤害",lambda O0O000O0OO00OOOOO :STAT_countpx (O0O000O0OO00OOOOO .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O0O000O0OO0O0OOO0 :STAT_countpx (O0O000O0OO0O0OOO0 .values ,"死亡")),)#line:4966
				if len (OO0OOO00000OOO0OO )>1 :#line:4967
					text .insert (END ,"注意，产品类别有两种，产品名称规整疑似不正确！")#line:4968
				O0O0OO0OOO00O0O00 =pd .merge (O0O0OO0OOO00O0O00 ,OO0OOO00000OOO0OO ,on =["产品类别","规整后品类"],how ="left").reset_index ()#line:4970
		except :#line:4972
			text .insert (END ,"\n目前结果为未进行名称规整的结果！\n")#line:4973
			O0O0OO0OOO00O0O00 =OOO00O0000OOOOO0O .groupby (OO0O00O00OO0O000O ).agg (该元素总数量 =(OO000OO0O0OO000OO ,"count"),该元素严重伤害数 =("伤害",lambda OO00OOO0OO0000O0O :STAT_countpx (OO00OOO0OO0000O0O .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O0O000OOO0OO00O00 :STAT_countpx (O0O000OOO0OO00O00 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:4980
			OO0OOO00000OOO0OO =OOO00O0000OOOOO0O .groupby (O0OO0000OO00O0OO0 ).agg (所有元素总数量 =(O00OO0OOO00O000O0 ,"count"),所有元素严重伤害数 =("伤害",lambda OOOOO0O0O0OO00O0O :STAT_countpx (OOOOO0O0O0OO00O0O .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda OO0OOO00OOOO0OOO0 :STAT_countpx (OO0OOO00OOOO0OOO0 .values ,"死亡")),)#line:4986
			O0O0OO0OOO00O0O00 =pd .merge (O0O0OO0OOO00O0O00 ,OO0OOO00000OOO0OO ,on =O0OO0000OO00O0OO0 ,how ="left").reset_index ()#line:4990
		OO0OOO00000OOO0OO =OO0OOO00000OOO0OO [(OO0OOO00000OOO0OO ["所有元素总数量"]>=3 )].reset_index ()#line:4992
		OO0O0OOOO0O0OOOOO =[]#line:4993
		if ("产品名称"not in OO0OOO00000OOO0OO .columns )and ("规整后品类"not in OO0OOO00000OOO0OO .columns ):#line:4995
			OO0OOO00000OOO0OO ["产品名称"]=OO0OOO00000OOO0OO ["产品类别"]#line:4996
		if "规整后品类"not in OO0OOO00000OOO0OO .columns :#line:5002
			OO0OOO00000OOO0OO ["规整后品类"]="不适用"#line:5003
		O00O0OOOO0O0O00OO =0 #line:5006
		O0OOO000OOO0O0OOO =int (len (OO0OOO00000OOO0OO ))#line:5007
		for OOOO00OOO0O0OOO00 ,O000OO0O0OO0OO000 ,OOO0O0O000OO00000 ,OO00OO0000000O0O0 in zip (OO0OOO00000OOO0OO ["规整后品类"],OO0OOO00000OOO0OO ["产品类别"],OO0OOO00000OOO0OO [O00OO0OOO00O000O0 ],OO0OOO00000OOO0OO ["所有元素总数量"]):#line:5008
			O00O0OOOO0O0O00OO +=1 #line:5009
			if (time .time ()-OO0O0OO00OOO0OOOO )>3 :#line:5010
				root .attributes ("-topmost",True )#line:5011
				PROGRAM_change_schedule (O00O0OOOO0O0O00OO ,O0OOO000OOO0O0OOO )#line:5012
				root .attributes ("-topmost",False )#line:5013
			OOO00OOOO0O0O0000 =OOO00O0000OOOOO0O [(OOO00O0000OOOOO0O [O00OO0OOO00O000O0 ]==OOO0O0O000OO00000 )].copy ()#line:5014
			O0O00OO00O0OO0000 ["SELECT"]=O0O00OO00O0OO0000 .apply (lambda O0OO0OOO0OOO0OOOO :((OOOO00OOO0O0OOO00 in O0OO0OOO0OOO0OOOO ["适用范围"])or (O0OO0OOO0OOO0OOOO ["适用范围"]in O000OO0O0OO0OO000 )),axis =1 )#line:5015
			O0O0OO00O00O000O0 =O0O00OO00O0OO0000 [(O0O00OO00O0OO0000 ["SELECT"]==True )].reset_index ()#line:5016
			if len (O0O0OO00O00O000O0 )>0 :#line:5017
				for OOOOO000OOOO0000O ,O00O0O0OOOOOOOO00 ,O00O00000000OO0OO in zip (O0O0OO00O00O000O0 ["值"].values ,O0O0OO00O00O000O0 ["查找位置"].values ,O0O0OO00O00O000O0 ["排除值"].values ):#line:5019
					O0O00OO000OO00O00 =OOO00OOOO0O0O0000 .copy ()#line:5020
					O0O00OOOOOOO00OOO =TOOLS_get_list (OOOOO000OOOO0000O )[0 ]#line:5021
					OO0O00OOO0O0O000O ="关键字查找列"#line:5022
					O0O00OO000OO00O00 [OO0O00OOO0O0O000O ]=""#line:5023
					for OOOOOOOO0000O0OO0 in TOOLS_get_list (O00O0O0OOOOOOOO00 ):#line:5024
						O0O00OO000OO00O00 [OO0O00OOO0O0O000O ]=O0O00OO000OO00O00 [OO0O00OOO0O0O000O ]+O0O00OO000OO00O00 [OOOOOOOO0000O0OO0 ].astype ("str")#line:5025
					O0O00OO000OO00O00 .loc [O0O00OO000OO00O00 [OO0O00OOO0O0O000O ].str .contains (OOOOO000OOOO0000O ,na =False ),"关键字"]=O0O00OOOOOOO00OOO #line:5027
					if str (O00O00000000OO0OO )!="nan":#line:5030
						O0O00OO000OO00O00 =O0O00OO000OO00O00 .loc [~O0O00OO000OO00O00 ["关键字查找列"].str .contains (O00O00000000OO0OO ,na =False )].copy ()#line:5031
					if (len (O0O00OO000OO00O00 ))<1 :#line:5034
						continue #line:5035
					for OO00OO0O00OO00000 in zip (O0O00OO000OO00O00 [OO000OO0O0OO000OO ].drop_duplicates ()):#line:5037
						try :#line:5040
							if OO00OO0O00OO00000 [0 ]!=O0O0O0O0OO00OO00O [1 ]:#line:5041
								continue #line:5042
						except :#line:5043
							pass #line:5044
						OO00O00O000OOOO0O ={"合并列":{OO0O00OOO0O0O000O :O00O0O0OOOOOOOO00 },"等于":{O00OO0OOO00O000O0 :OOO0O0O000OO00000 ,OO000OO0O0OO000OO :OO00OO0O00OO00000 [0 ]},"不等于":{},"包含":{OO0O00OOO0O0O000O :OOOOO000OOOO0000O },"不包含":{OO0O00OOO0O0O000O :O00O00000000OO0OO }}#line:5052
						O0OO0OOOO0O0O000O =STAT_PPR_ROR_1 (OO000OO0O0OO000OO ,str (OO00OO0O00OO00000 [0 ]),"关键字查找列",OOOOO000OOOO0000O ,O0O00OO000OO00O00 )+(OOOOO000OOOO0000O ,O00O00000000OO0OO ,O00O0O0OOOOOOOO00 ,OOO0O0O000OO00000 ,OO00OO0O00OO00000 [0 ],str (OO00O00O000OOOO0O ))#line:5054
						if O0OO0OOOO0O0O000O [1 ]>0 :#line:5056
							O00OOO0O0OO00O000 =pd .DataFrame (columns =["特定关键字","出现频次","占比","ROR值","ROR值的95%CI下限","PRR值","PRR值的95%CI下限","卡方值","四分表","关键字组合","排除值","关键字查找列",O00OO0OOO00O000O0 ,OO000OO0O0OO000OO ,"报表定位"])#line:5058
							O00OOO0O0OO00O000 .loc [0 ]=O0OO0OOOO0O0O000O #line:5059
							OO0O0OOOO0O0OOOOO .append (O00OOO0O0OO00O000 )#line:5060
		O0O000OO0O0OO0OOO =pd .concat (OO0O0OOOO0O0OOOOO )#line:5064
		O0O000OO0O0OO0OOO =pd .merge (O0O0OO0OOO00O0O00 ,O0O000OO0O0OO0OOO ,on =[O00OO0OOO00O000O0 ,OO000OO0O0OO000OO ],how ="right")#line:5068
		O0O000OO0O0OO0OOO =O0O000OO0O0OO0OOO .reset_index (drop =True )#line:5069
		del O0O000OO0O0OO0OOO ["index"]#line:5070
		if len (O0O000OO0O0OO0OOO )>0 :#line:5071
			O0O000OO0O0OO0OOO ["风险评分"]=0 #line:5072
			O0O000OO0O0OO0OOO ["报表类型"]="ROR"#line:5073
			O0O000OO0O0OO0OOO .loc [(O0O000OO0O0OO0OOO ["出现频次"]>=3 ),"风险评分"]=O0O000OO0O0OO0OOO ["风险评分"]+3 #line:5074
			O0O000OO0O0OO0OOO .loc [(O0O000OO0O0OO0OOO ["ROR值的95%CI下限"]>1 ),"风险评分"]=O0O000OO0O0OO0OOO ["风险评分"]+1 #line:5075
			O0O000OO0O0OO0OOO .loc [(O0O000OO0O0OO0OOO ["PRR值的95%CI下限"]>1 ),"风险评分"]=O0O000OO0O0OO0OOO ["风险评分"]+1 #line:5076
			O0O000OO0O0OO0OOO ["风险评分"]=O0O000OO0O0OO0OOO ["风险评分"]+O0O000OO0O0OO0OOO ["该元素单位个数"]/100 #line:5077
			O0O000OO0O0OO0OOO =O0O000OO0O0OO0OOO .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5078
		print ("耗时：",(time .time ()-OO0O0OO00OOO0OOOO ))#line:5084
		return O0O000OO0O0OO0OOO #line:5085
	def df_chiyouren (O000OO0OOO00000O0 ):#line:5091
		""#line:5092
		OOO00O0OOOO00O00O =O000OO0OOO00000O0 .df .copy ().reset_index (drop =True )#line:5093
		OOO00O0OOOO00O00O ["总报告数"]=data ["报告编码"].copy ()#line:5094
		OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"总待评价数量"]=data ["报告编码"]#line:5095
		OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["伤害"]=="严重伤害"),"严重伤害报告数"]=data ["报告编码"]#line:5096
		OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价")&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害"),"严重伤害待评价数量"]=data ["报告编码"]#line:5097
		OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价")&(OOO00O0OOOO00O00O ["伤害"]=="其他"),"其他待评价数量"]=data ["报告编码"]#line:5098
		OOOO00OOOO000O0O0 =OOO00O0OOOO00O00O .groupby (["上市许可持有人名称"]).aggregate ({"总报告数":"nunique","总待评价数量":"nunique","严重伤害报告数":"nunique","严重伤害待评价数量":"nunique","其他待评价数量":"nunique"})#line:5101
		OOOO00OOOO000O0O0 ["严重伤害待评价比例"]=round (OOOO00OOOO000O0O0 ["严重伤害待评价数量"]/OOOO00OOOO000O0O0 ["严重伤害报告数"]*100 ,2 )#line:5106
		OOOO00OOOO000O0O0 ["总待评价比例"]=round (OOOO00OOOO000O0O0 ["总待评价数量"]/OOOO00OOOO000O0O0 ["总报告数"]*100 ,2 )#line:5109
		OOOO00OOOO000O0O0 ["总报告数"]=OOOO00OOOO000O0O0 ["总报告数"].fillna (0 )#line:5110
		OOOO00OOOO000O0O0 ["总待评价比例"]=OOOO00OOOO000O0O0 ["总待评价比例"].fillna (0 )#line:5111
		OOOO00OOOO000O0O0 ["严重伤害报告数"]=OOOO00OOOO000O0O0 ["严重伤害报告数"].fillna (0 )#line:5112
		OOOO00OOOO000O0O0 ["严重伤害待评价比例"]=OOOO00OOOO000O0O0 ["严重伤害待评价比例"].fillna (0 )#line:5113
		OOOO00OOOO000O0O0 ["总报告数"]=OOOO00OOOO000O0O0 ["总报告数"].astype (int )#line:5114
		OOOO00OOOO000O0O0 ["总待评价比例"]=OOOO00OOOO000O0O0 ["总待评价比例"].astype (int )#line:5115
		OOOO00OOOO000O0O0 ["严重伤害报告数"]=OOOO00OOOO000O0O0 ["严重伤害报告数"].astype (int )#line:5116
		OOOO00OOOO000O0O0 ["严重伤害待评价比例"]=OOOO00OOOO000O0O0 ["严重伤害待评价比例"].astype (int )#line:5117
		OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .sort_values (by =["总报告数","总待评价比例"],ascending =[False ,False ],na_position ="last")#line:5120
		if "场所名称"in OOO00O0OOOO00O00O .columns :#line:5122
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["审核日期"]=="未填写"),"审核日期"]=3000 -12 -12 #line:5123
			OOO00O0OOOO00O00O ["报告时限"]=pd .Timestamp .today ()-pd .to_datetime (OOO00O0OOOO00O00O ["审核日期"])#line:5124
			OOO00O0OOOO00O00O ["报告时限2"]=45 -(pd .Timestamp .today ()-pd .to_datetime (OOO00O0OOOO00O00O ["审核日期"])).dt .days #line:5125
			OOO00O0OOOO00O00O ["报告时限"]=OOO00O0OOOO00O00O ["报告时限"].dt .days #line:5126
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限"]>45 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（严重）"]=1 #line:5127
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限"]>45 )&(OOO00O0OOOO00O00O ["伤害"]=="其他")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（其他）"]=1 #line:5128
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限"]>30 )&(OOO00O0OOOO00O00O ["伤害"]=="死亡")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"待评价且超出当前日期30天（死亡）"]=1 #line:5129
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]<=1 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["报告时限2"]>0 )&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩1天"]=1 #line:5131
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>1 )&(OOO00O0OOOO00O00O ["报告时限2"]<=3 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩1-3天"]=1 #line:5132
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>3 )&(OOO00O0OOOO00O00O ["报告时限2"]<=5 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩3-5天"]=1 #line:5133
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>5 )&(OOO00O0OOOO00O00O ["报告时限2"]<=10 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩5-10天"]=1 #line:5134
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>10 )&(OOO00O0OOOO00O00O ["报告时限2"]<=20 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩10-20天"]=1 #line:5135
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>20 )&(OOO00O0OOOO00O00O ["报告时限2"]<=30 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩20-30天"]=1 #line:5136
			OOO00O0OOOO00O00O .loc [(OOO00O0OOOO00O00O ["报告时限2"]>30 )&(OOO00O0OOOO00O00O ["报告时限2"]<=45 )&(OOO00O0OOOO00O00O ["伤害"]=="严重伤害")&(OOO00O0OOOO00O00O ["持有人报告状态"]=="待评价"),"严重待评价且只剩30-45天"]=1 #line:5137
			del OOO00O0OOOO00O00O ["报告时限2"]#line:5138
			OO0000O0OOOOOOOO0 =(OOO00O0OOOO00O00O .groupby (["上市许可持有人名称"]).aggregate ({"待评价且超出当前日期45天（严重）":"sum","待评价且超出当前日期45天（其他）":"sum","待评价且超出当前日期30天（死亡）":"sum","严重待评价且只剩1天":"sum","严重待评价且只剩1-3天":"sum","严重待评价且只剩3-5天":"sum","严重待评价且只剩5-10天":"sum","严重待评价且只剩10-20天":"sum","严重待评价且只剩20-30天":"sum","严重待评价且只剩30-45天":"sum"}).reset_index ())#line:5140
			OOOO00OOOO000O0O0 =pd .merge (OOOO00OOOO000O0O0 ,OO0000O0OOOOOOOO0 ,on =["上市许可持有人名称"],how ="outer",)#line:5141
			OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（严重）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（严重）"].fillna (0 )#line:5142
			OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（严重）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（严重）"].astype (int )#line:5143
			OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（其他）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（其他）"].fillna (0 )#line:5144
			OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（其他）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期45天（其他）"].astype (int )#line:5145
			OOOO00OOOO000O0O0 ["待评价且超出当前日期30天（死亡）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期30天（死亡）"].fillna (0 )#line:5146
			OOOO00OOOO000O0O0 ["待评价且超出当前日期30天（死亡）"]=OOOO00OOOO000O0O0 ["待评价且超出当前日期30天（死亡）"].astype (int )#line:5147
			OOOO00OOOO000O0O0 ["严重待评价且只剩1天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩1天"].fillna (0 )#line:5149
			OOOO00OOOO000O0O0 ["严重待评价且只剩1天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩1天"].astype (int )#line:5150
			OOOO00OOOO000O0O0 ["严重待评价且只剩1-3天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩1-3天"].fillna (0 )#line:5151
			OOOO00OOOO000O0O0 ["严重待评价且只剩1-3天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩1-3天"].astype (int )#line:5152
			OOOO00OOOO000O0O0 ["严重待评价且只剩3-5天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩3-5天"].fillna (0 )#line:5153
			OOOO00OOOO000O0O0 ["严重待评价且只剩3-5天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩3-5天"].astype (int )#line:5154
			OOOO00OOOO000O0O0 ["严重待评价且只剩5-10天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩5-10天"].fillna (0 )#line:5155
			OOOO00OOOO000O0O0 ["严重待评价且只剩5-10天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩5-10天"].astype (int )#line:5156
			OOOO00OOOO000O0O0 ["严重待评价且只剩10-20天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩10-20天"].fillna (0 )#line:5157
			OOOO00OOOO000O0O0 ["严重待评价且只剩10-20天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩10-20天"].astype (int )#line:5158
			OOOO00OOOO000O0O0 ["严重待评价且只剩20-30天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩20-30天"].fillna (0 )#line:5159
			OOOO00OOOO000O0O0 ["严重待评价且只剩20-30天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩20-30天"].astype (int )#line:5160
			OOOO00OOOO000O0O0 ["严重待评价且只剩30-45天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩30-45天"].fillna (0 )#line:5161
			OOOO00OOOO000O0O0 ["严重待评价且只剩30-45天"]=OOOO00OOOO000O0O0 ["严重待评价且只剩30-45天"].astype (int )#line:5162
		OOOO00OOOO000O0O0 ["总待评价数量"]=OOOO00OOOO000O0O0 ["总待评价数量"].fillna (0 )#line:5164
		OOOO00OOOO000O0O0 ["总待评价数量"]=OOOO00OOOO000O0O0 ["总待评价数量"].astype (int )#line:5165
		OOOO00OOOO000O0O0 ["严重伤害待评价数量"]=OOOO00OOOO000O0O0 ["严重伤害待评价数量"].fillna (0 )#line:5166
		OOOO00OOOO000O0O0 ["严重伤害待评价数量"]=OOOO00OOOO000O0O0 ["严重伤害待评价数量"].astype (int )#line:5167
		OOOO00OOOO000O0O0 ["其他待评价数量"]=OOOO00OOOO000O0O0 ["其他待评价数量"].fillna (0 )#line:5168
		OOOO00OOOO000O0O0 ["其他待评价数量"]=OOOO00OOOO000O0O0 ["其他待评价数量"].astype (int )#line:5169
		OOOO0OOOOOO000000 =["总报告数","总待评价数量","严重伤害报告数","严重伤害待评价数量","其他待评价数量"]#line:5172
		OOOO00OOOO000O0O0 .loc ["合计"]=OOOO00OOOO000O0O0 [OOOO0OOOOOO000000 ].apply (lambda O000O0000OOO0OOO0 :O000O0000OOO0OOO0 .sum ())#line:5173
		OOOO00OOOO000O0O0 [OOOO0OOOOOO000000 ]=OOOO00OOOO000O0O0 [OOOO0OOOOOO000000 ].apply (lambda OOO00000OOOOOOOOO :OOO00000OOOOOOOOO .astype (int ))#line:5174
		OOOO00OOOO000O0O0 .iloc [-1 ,0 ]="合计"#line:5175
		if "场所名称"in OOO00O0OOOO00O00O .columns :#line:5177
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .reset_index (drop =True )#line:5178
		else :#line:5179
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .reset_index ()#line:5180
		if ini ["模式"]=="药品":#line:5182
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .rename (columns ={"总待评价数量":"新的数量"})#line:5183
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .rename (columns ={"严重伤害待评价数量":"新的严重的数量"})#line:5184
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .rename (columns ={"严重伤害待评价比例":"新的严重的比例"})#line:5185
			OOOO00OOOO000O0O0 =OOOO00OOOO000O0O0 .rename (columns ={"总待评价比例":"新的比例"})#line:5186
			del OOOO00OOOO000O0O0 ["其他待评价数量"]#line:5188
		OOOO00OOOO000O0O0 ["报表类型"]="dfx_chiyouren"#line:5189
		return OOOO00OOOO000O0O0 #line:5190
	def df_age (OOO000OOO00OOO00O ):#line:5192
		""#line:5193
		OO00OOO00O00O0O0O =OOO000OOO00OOO00O .df .copy ()#line:5194
		OO00OOO00O00O0O0O =OO00OOO00O00O0O0O .drop_duplicates ("报告编码").copy ()#line:5195
		OOOO000O00OO0O000 =pd .pivot_table (OO00OOO00O00O0O0O .drop_duplicates ("报告编码"),values =["报告编码"],index ="年龄段",columns ="性别",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"}).reset_index ()#line:5196
		OOOO000O00OO0O000 .columns =OOOO000O00OO0O000 .columns .droplevel (0 )#line:5197
		OOOO000O00OO0O000 ["构成比(%)"]=round (100 *OOOO000O00OO0O000 ["All"]/len (OO00OOO00O00O0O0O ),2 )#line:5198
		OOOO000O00OO0O000 ["累计构成比(%)"]=OOOO000O00OO0O000 ["构成比(%)"].cumsum ()#line:5199
		OOOO000O00OO0O000 ["报表类型"]="年龄性别表"#line:5200
		return OOOO000O00OO0O000 #line:5201
	def df_psur (O0O0OO00000O0OOOO ,*OOOOOO000O00O0O00 ):#line:5203
		""#line:5204
		OOOOO000OO0O0OO0O =O0O0OO00000O0OOOO .df .copy ()#line:5205
		OO0OOOO00OO0OOO00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5206
		O00000OO0O0O0OOO0 =len (OOOOO000OO0O0OO0O .drop_duplicates ("报告编码"))#line:5207
		if "报告类型-新的"in OOOOO000OO0O0OO0O .columns :#line:5211
			O0OOOOO0000O00O0O ="药品"#line:5212
		elif "皮损形态"in OOOOO000OO0O0OO0O .columns :#line:5213
			O0OOOOO0000O00O0O ="化妆品"#line:5214
		else :#line:5215
			O0OOOOO0000O00O0O ="器械"#line:5216
		OOO0O0O0O00OOO0O0 =pd .read_excel (OO0OOOO00OO0OOO00 ,header =0 ,sheet_name =O0OOOOO0000O00O0O )#line:5219
		O0O0O00000O00000O =(OOO0O0O0O00OOO0O0 .loc [OOO0O0O0O00OOO0O0 ["适用范围"].str .contains ("通用监测关键字|无源|有源",na =False )].copy ().reset_index (drop =True ))#line:5222
		try :#line:5225
			if OOOOOO000O00O0O00 [0 ]in ["特定品种","通用无源","通用有源"]:#line:5226
				OOO00OO0000OO00O0 =""#line:5227
				if OOOOOO000O00O0O00 [0 ]=="特定品种":#line:5228
					OOO00OO0000OO00O0 =OOO0O0O0O00OOO0O0 .loc [OOO0O0O0O00OOO0O0 ["适用范围"].str .contains (OOOOOO000O00O0O00 [1 ],na =False )].copy ().reset_index (drop =True )#line:5229
				if OOOOOO000O00O0O00 [0 ]=="通用无源":#line:5231
					OOO00OO0000OO00O0 =OOO0O0O0O00OOO0O0 .loc [OOO0O0O0O00OOO0O0 ["适用范围"].str .contains ("通用监测关键字|无源",na =False )].copy ().reset_index (drop =True )#line:5232
				if OOOOOO000O00O0O00 [0 ]=="通用有源":#line:5233
					OOO00OO0000OO00O0 =OOO0O0O0O00OOO0O0 .loc [OOO0O0O0O00OOO0O0 ["适用范围"].str .contains ("通用监测关键字|有源",na =False )].copy ().reset_index (drop =True )#line:5234
				if OOOOOO000O00O0O00 [0 ]=="体外诊断试剂":#line:5235
					OOO00OO0000OO00O0 =OOO0O0O0O00OOO0O0 .loc [OOO0O0O0O00OOO0O0 ["适用范围"].str .contains ("体外诊断试剂",na =False )].copy ().reset_index (drop =True )#line:5236
				if len (OOO00OO0000OO00O0 )<1 :#line:5237
					showinfo (title ="提示",message ="未找到相应的自定义规则，任务结束。")#line:5238
					return 0 #line:5239
				else :#line:5240
					O0O0O00000O00000O =OOO00OO0000OO00O0 #line:5241
		except :#line:5243
			pass #line:5244
		try :#line:5248
			if O0OOOOO0000O00O0O =="器械"and OOOOOO000O00O0O00 [0 ]=="特定品种作为通用关键字":#line:5249
				O0O0O00000O00000O =OOOOOO000O00O0O00 [1 ]#line:5250
		except dddd :#line:5252
			pass #line:5253
		OO00000O0000OO00O =""#line:5256
		O000OO0OO0OOO0OOO ="-其他关键字-不含："#line:5257
		for O0O000OOOOO00OO0O ,O0O0O0OOOO0OO0OO0 in O0O0O00000O00000O .iterrows ():#line:5258
			O000OO0OO0OOO0OOO =O000OO0OO0OOO0OOO +"|"+str (O0O0O0OOOO0OO0OO0 ["值"])#line:5259
			OO0O0OOO0O000O0OO =O0O0O0OOOO0OO0OO0 #line:5260
		OO0O0OOO0O000O0OO [2 ]="通用监测关键字"#line:5261
		OO0O0OOO0O000O0OO [4 ]=O000OO0OO0OOO0OOO #line:5262
		O0O0O00000O00000O .loc [len (O0O0O00000O00000O )]=OO0O0OOO0O000O0OO #line:5263
		O0O0O00000O00000O =O0O0O00000O00000O .reset_index (drop =True )#line:5264
		if ini ["模式"]=="器械":#line:5268
			OOOOO000OO0O0OO0O ["关键字查找列"]=OOOOO000OO0O0OO0O ["器械故障表现"].astype (str )+OOOOO000OO0O0OO0O ["伤害表现"].astype (str )+OOOOO000OO0O0OO0O ["使用过程"].astype (str )+OOOOO000OO0O0OO0O ["事件原因分析描述"].astype (str )+OOOOO000OO0O0OO0O ["初步处置情况"].astype (str )#line:5269
		else :#line:5270
			OOOOO000OO0O0OO0O ["关键字查找列"]=OOOOO000OO0O0OO0O ["器械故障表现"]#line:5271
		text .insert (END ,"\n药品查找列默认为不良反应表现,药品规则默认为通用规则。\n器械默认查找列为器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况，器械默认规则为无源通用规则+有源通用规则。\n")#line:5272
		OO0O0O0O0000O000O =[]#line:5274
		for O0O000OOOOO00OO0O ,O0O0O0OOOO0OO0OO0 in O0O0O00000O00000O .iterrows ():#line:5276
			O000000O0O0OOOOO0 =O0O0O0OOOO0OO0OO0 ["值"]#line:5277
			if "-其他关键字-"not in O000000O0O0OOOOO0 :#line:5279
				OO0000OO00O00000O =OOOOO000OO0O0OO0O .loc [OOOOO000OO0O0OO0O ["关键字查找列"].str .contains (O000000O0O0OOOOO0 ,na =False )].copy ()#line:5282
				if str (O0O0O0OOOO0OO0OO0 ["排除值"])!="nan":#line:5283
					OO0000OO00O00000O =OO0000OO00O00000O .loc [~OO0000OO00O00000O ["关键字查找列"].str .contains (str (O0O0O0OOOO0OO0OO0 ["排除值"]),na =False )].copy ()#line:5285
			else :#line:5287
				OO0000OO00O00000O =OOOOO000OO0O0OO0O .loc [~OOOOO000OO0O0OO0O ["关键字查找列"].str .contains (O000000O0O0OOOOO0 ,na =False )].copy ()#line:5290
			OO0000OO00O00000O ["关键字标记"]=str (O000000O0O0OOOOO0 )#line:5291
			OO0000OO00O00000O ["关键字计数"]=1 #line:5292
			if len (OO0000OO00O00000O )>0 :#line:5298
				try :#line:5299
					OOO0OO0O0000O0000 =pd .pivot_table (OO0000OO00O00000O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害PSUR",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5309
				except :#line:5311
					OOO0OO0O0000O0000 =pd .pivot_table (OO0000OO00O00000O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5321
				OOO0OO0O0000O0000 =OOO0OO0O0000O0000 [:-1 ]#line:5322
				OOO0OO0O0000O0000 .columns =OOO0OO0O0000O0000 .columns .droplevel (0 )#line:5323
				OOO0OO0O0000O0000 =OOO0OO0O0000O0000 .reset_index ()#line:5324
				if len (OOO0OO0O0000O0000 )>0 :#line:5327
					O0000OO00O0OOO00O =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",OO0000OO00O00000O ,1000 ))).replace ("Counter({","{")#line:5328
					O0000OO00O0OOO00O =O0000OO00O0OOO00O .replace ("})","}")#line:5329
					O0000OO00O0OOO00O =ast .literal_eval (O0000OO00O0OOO00O )#line:5330
					OOO0OO0O0000O0000 .loc [0 ,"事件分类"]=str (TOOLS_get_list (OOO0OO0O0000O0000 .loc [0 ,"关键字标记"])[0 ])#line:5332
					OOO0OO0O0000O0000 .loc [0 ,"不良事件名称1"]=str ({OO0OOOO00O000O00O :OO0OOOOOO000OOOOO for OO0OOOO00O000O00O ,OO0OOOOOO000OOOOO in O0000OO00O0OOO00O .items ()if STAT_judge_x (str (OO0OOOO00O000O00O ),TOOLS_get_list (O000000O0O0OOOOO0 ))==1 })#line:5333
					OOO0OO0O0000O0000 .loc [0 ,"不良事件名称2"]=str ({O0O0OO000O00OO00O :O000OO0OO0O0O0O0O for O0O0OO000O00OO00O ,O000OO0OO0O0O0O0O in O0000OO00O0OOO00O .items ()if STAT_judge_x (str (O0O0OO000O00OO00O ),TOOLS_get_list (O000000O0O0OOOOO0 ))!=1 })#line:5334
					if ini ["模式"]=="药品":#line:5345
						for O000OO00O000OOOO0 in ["SOC","HLGT","HLT","PT"]:#line:5346
							OOO0OO0O0000O0000 [O000OO00O000OOOO0 ]=O0O0O0OOOO0OO0OO0 [O000OO00O000OOOO0 ]#line:5347
					if ini ["模式"]=="器械":#line:5348
						for O000OO00O000OOOO0 in ["国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]:#line:5349
							OOO0OO0O0000O0000 [O000OO00O000OOOO0 ]=O0O0O0OOOO0OO0OO0 [O000OO00O000OOOO0 ]#line:5350
					OO0O0O0O0000O000O .append (OOO0OO0O0000O0000 )#line:5353
		OO00000O0000OO00O =pd .concat (OO0O0O0O0000O000O )#line:5354
		OO00000O0000OO00O =OO00000O0000OO00O .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5359
		OO00000O0000OO00O =OO00000O0000OO00O .reset_index ()#line:5360
		OO00000O0000OO00O ["All占比"]=round (OO00000O0000OO00O ["All"]/O00000OO0O0O0OOO0 *100 ,2 )#line:5362
		OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5363
		try :#line:5364
			OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={"其他":"一般"})#line:5365
		except :#line:5366
			pass #line:5367
		try :#line:5369
			OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={" 一般":"一般"})#line:5370
		except :#line:5371
			pass #line:5372
		try :#line:5373
			OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={" 严重":"严重"})#line:5374
		except :#line:5375
			pass #line:5376
		try :#line:5377
			OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={"严重伤害":"严重"})#line:5378
		except :#line:5379
			pass #line:5380
		try :#line:5381
			OO00000O0000OO00O =OO00000O0000OO00O .rename (columns ={"死亡":"死亡(仅支持器械)"})#line:5382
		except :#line:5383
			pass #line:5384
		for O00O000OO0OOOO0OO in ["一般","新的一般","严重","新的严重"]:#line:5387
			if O00O000OO0OOOO0OO not in OO00000O0000OO00O .columns :#line:5388
				OO00000O0000OO00O [O00O000OO0OOOO0OO ]=0 #line:5389
		try :#line:5391
			OO00000O0000OO00O ["严重比"]=round ((OO00000O0000OO00O ["严重"].fillna (0 )+OO00000O0000OO00O ["死亡(仅支持器械)"].fillna (0 ))/OO00000O0000OO00O ["总数量"]*100 ,2 )#line:5392
		except :#line:5393
			OO00000O0000OO00O ["严重比"]=round ((OO00000O0000OO00O ["严重"].fillna (0 )+OO00000O0000OO00O ["新的严重"].fillna (0 ))/OO00000O0000OO00O ["总数量"]*100 ,2 )#line:5394
		OO00000O0000OO00O ["构成比"]=round ((OO00000O0000OO00O ["总数量"].fillna (0 ))/OO00000O0000OO00O ["总数量"].sum ()*100 ,2 )#line:5396
		if ini ["模式"]=="药品":#line:5398
			try :#line:5399
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)","SOC","HLGT","HLT","PT"]]#line:5400
			except :#line:5401
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","SOC","HLGT","HLT","PT"]]#line:5402
		elif ini ["模式"]=="器械":#line:5403
			try :#line:5404
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5405
			except :#line:5406
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5407
		else :#line:5409
			try :#line:5410
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2","死亡(仅支持器械)"]]#line:5411
			except :#line:5412
				OO00000O0000OO00O =OO00000O0000OO00O [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","构成比","严重比","事件分类","不良事件名称1","不良事件名称2"]]#line:5413
		for OO000O000OOOOOOO0 ,OOOOO00OOO0O00O0O in O0O0O00000O00000O .iterrows ():#line:5415
			OO00000O0000OO00O .loc [(OO00000O0000OO00O ["关键字标记"].astype (str )==str (OOOOO00OOO0O00O0O ["值"])),"排除值"]=OOOOO00OOO0O00O0O ["排除值"]#line:5416
		OO00000O0000OO00O ["排除值"]=OO00000O0000OO00O ["排除值"].fillna ("没有排除值")#line:5418
		for O000OOO0O0000OOOO in ["一般","新的一般","严重","新的严重","总数量","总数量占比","严重比"]:#line:5422
			OO00000O0000OO00O [O000OOO0O0000OOOO ]=OO00000O0000OO00O [O000OOO0O0000OOOO ].fillna (0 )#line:5423
		for O000OOO0O0000OOOO in ["一般","新的一般","严重","新的严重","总数量"]:#line:5425
			OO00000O0000OO00O [O000OOO0O0000OOOO ]=OO00000O0000OO00O [O000OOO0O0000OOOO ].astype (int )#line:5426
		OO00000O0000OO00O ["RPN"]="未定义"#line:5429
		OO00000O0000OO00O ["故障原因"]="未定义"#line:5430
		OO00000O0000OO00O ["可造成的伤害"]="未定义"#line:5431
		OO00000O0000OO00O ["应采取的措施"]="未定义"#line:5432
		OO00000O0000OO00O ["发生率"]="未定义"#line:5433
		OO00000O0000OO00O ["报表类型"]="PSUR"#line:5435
		return OO00000O0000OO00O #line:5436
def A0000_Main ():#line:5446
	print ("")#line:5447
if __name__ =='__main__':#line:5449
	root =Tk .Tk ()#line:5452
	root .title (title_all )#line:5453
	try :#line:5454
		root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:5455
	except :#line:5456
		pass #line:5457
	sw_root =root .winfo_screenwidth ()#line:5458
	sh_root =root .winfo_screenheight ()#line:5460
	ww_root =700 #line:5462
	wh_root =620 #line:5463
	x_root =(sw_root -ww_root )/2 #line:5465
	y_root =(sh_root -wh_root )/2 #line:5466
	root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:5467
	framecanvas =Frame (root )#line:5472
	canvas =Canvas (framecanvas ,width =680 ,height =30 )#line:5473
	canvas .pack ()#line:5474
	x =StringVar ()#line:5475
	out_rec =canvas .create_rectangle (5 ,5 ,680 ,25 ,outline ="silver",width =1 )#line:5476
	fill_rec =canvas .create_rectangle (5 ,5 ,5 ,25 ,outline ="",width =0 ,fill ="silver")#line:5477
	canvas .create_text (350 ,15 ,text ="总执行进度")#line:5478
	framecanvas .pack ()#line:5479
	try :#line:5486
		frame0 =ttk .Frame (root ,width =90 ,height =20 )#line:5487
		frame0 .pack (side =LEFT )#line:5488
		B_open_files1 =Button (frame0 ,text ="导入数据",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =TOOLS_allfileopen ,)#line:5499
		B_open_files1 .pack ()#line:5500
		B_open_files3 =Button (frame0 ,text ="数据查看",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ori ,0 ,ori ),)#line:5515
		B_open_files3 .pack ()#line:5516
	except KEY :#line:5519
		pass #line:5520
	text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF")#line:5524
	text .pack (padx =5 ,pady =5 )#line:5525
	text .insert (END ,"\n 本程序适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请点击实用工具-意见反馈。\n")#line:5528
	text .insert (END ,"\n\n")#line:5529
	setting_cfg =read_setting_cfg ()#line:5532
	generate_random_file ()#line:5533
	setting_cfg =open_setting_cfg ()#line:5534
	if setting_cfg ["settingdir"]==0 :#line:5535
		showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:5536
		filepathu =filedialog .askdirectory ()#line:5537
		path =get_directory_path (filepathu )#line:5538
		update_setting_cfg ("settingdir",path )#line:5539
	setting_cfg =open_setting_cfg ()#line:5540
	random_number =int (setting_cfg ["sidori"])#line:5541
	input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:5542
	day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:5543
	sid =random_number *2 +183576 #line:5544
	if input_number ==sid and day_end =="未过期":#line:5545
		usergroup ="用户组=1"#line:5546
		text .insert (END ,usergroup +"   有效期至：")#line:5547
		text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:5548
	else :#line:5549
		text .insert (END ,usergroup )#line:5550
	text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:5551
	peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:5552
	roox =Toplevel ()#line:5556
	tMain =threading .Thread (target =PROGRAM_showWelcome )#line:5557
	tMain .start ()#line:5558
	t1 =threading .Thread (target =PROGRAM_closeWelcome )#line:5559
	t1 .start ()#line:5560
	root .lift ()#line:5562
	root .attributes ("-topmost",True )#line:5563
	root .attributes ("-topmost",False )#line:5564
	root .mainloop ()#line:5568
	print ("done.")#line:5569
