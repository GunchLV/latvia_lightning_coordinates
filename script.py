import numpy as np
from PIL import Image
from urllib.request import urlopen
import ssl
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd

context = ssl._create_unverified_context()
viss_kopa = pd.DataFrame()

def koordinatu_tabula(cipars):
    datums = str(date.today() - timedelta(days=cipars)).replace('-','')
    url = 'https://images.lightningmaps.org/blitzortung/europe/index.php?map=baltic_big&date=' + datums
    im = Image.open(urlopen(url, context=context)).convert('RGB')
    uzRGB = np.array(im)
    tikai_LV = uzRGB[280:620, 200:740]  # izgriežam Latviju
    tikai_LV_pic = Image.fromarray(tikai_LV)  # no array uz bildi
    RGBim = tikai_LV_pic.convert('RGB') # no bildes uz RGB
    HSVim = RGBim.convert('HSV') # no bildes uz HSV
    RGB = np.array(RGBim)
    HSV = np.array(HSVim)
    H = HSV[:,:,0]
    l,h = 80,230
    ZilieZalie = np.where((H>l) & (H<h))
    RGB[ZilieZalie] = [255, 255, 255]
    result = Image.fromarray(RGB)
    RGBim2 = result.convert('RGB')
    HSVim2 = result.convert('HSV')
    RGB2 = np.array(RGBim2)
    HSV2 = np.array(HSVim2)
    S = HSV2[:,:,1]
    h2 = 55
    pelekie = np.where(S<h2)
    ne_pelekie = np.where(S>=h2)
    RGB2[pelekie] = [0, 0, 0]
    RGB2[ne_pelekie] = [255, 255, 255]
    RGB2[161:164, 231:234] = [0, 0, 0] # aizkrāsojam Rīgas sarkano punktu
    result2 = Image.fromarray(RGB2)
    B = RGB2[:,:,0] # jauns arrays pēc pēdējās apstrādes
    baltie = np.where(B>0) # visi, kur nav melnas krāsas
    baltie_zip = list(zip(baltie[1], baltie[0]))  # šeit ir sapakotas pixeļu koordinātas
    df_v2 = pd.DataFrame(baltie_zip, columns=['x', 'y'])
    df_v2['lat'] = 58.19268-(df_v2['y']*0.00764)
    df_v2['long'] = 20.8662+(df_v2['x']*0.01389)
    df_v2['lat/long']=round(df_v2['lat'], 2).astype(str)+round(df_v2['long'], 2).astype(str)
    df_v2['datums']=str(url[-8:-4]+'-'+url[-4:-2]+'-'+url[-2:])
    return df_v2
