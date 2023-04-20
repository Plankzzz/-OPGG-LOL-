import requests
import re
import pandas as pd

def OPGGChampionRank():

    duizhao = {'上单':'top', '打野':'jungle', '中单':'mid', '下路':'adc', '辅助':'support'}

    position = input("位置（上单、打野、中单、下路、辅助）：")
    while position not in duizhao.keys():
        position = input("输入错误，请重新选择位置（上单、打野、中单、下路、辅助）：")

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    url = 'https://www.op.gg/champions?region=kr&tier=platinum_plus&position=' + duizhao[position]
    response = requests.get(url = url, headers = headers)
    result = response.text

    p_name = '<td class="css-cym2o0 e1oulx2j6">.*?<strong>(.*?)</strong></a></td>'
    p_tier = '<td class="css-ew1afn e1oulx2j3">.*?</span>(.*?)</td>'
    p_rate = '<td class="css-1wvfkid exo2f211">(.*?)<!-- -->%</td>'

    name = re.findall(p_name,result)
    tier = re.findall(p_tier,result)
    rate = re.findall(p_rate,result)
    winrate = []
    pick = []
    ban = []

    tier = map(int,tier)
    for i in range(int(len(rate)/3)):
        winrate.append(float(rate[3*i]))
        pick.append(float(rate[3*i+1]))
        ban.append(float(rate[3*i+2]))

    data = {'名称': name, '层级':tier, '胜率%':winrate, '登场率%':pick, '禁用率%':ban}
    data = pd.DataFrame(data)
    print(data)
    filename = position +'梯度.xlsx'
    data.to_excel(filename, index = False)

if __name__ == "__main__":
    OPGGChampionRank()
