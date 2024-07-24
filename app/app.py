# from flask import Flask, request, jsonify, render_template

# app = Flask(__name__)

# # Data contoh
# data = [
#     {"id": 1, "name": "Alice"},
#     {"id": 2, "name": "Bob"},
#     {"id": 3, "name": "Charlie"},
#     {"id": 4, "name": "David"},
#     {"id": 5, "name": "Eve"},
# ]


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/search")
# def search():
#     query = request.args.get("query", "").lower()
#     results = [item for item in data if query in item["name"].lower()]
#     return jsonify(results)


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from modulterjemahan import Translator
import Stem
import unicodedata
import pandas as pd
from rapidfuzz.distance import DamerauLevenshtein
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import mysql.connector
from mysql.connector import Error
import requests
import json

app = Flask(__name__)


def get_data(string):
    response = requests.get(f"http://127.0.0.1:5002/{string}")
    items = response.json()
    # Memuat JSON ke dalam dictionary
    data = json.loads(items[string])
    return pd.DataFrame(data)


# Load data once
data_kamus = get_data("kamus").values
data_ambigu = get_data("ambigu")
korpus_sub = get_data("subslemma")
korpus = set(korpus_sub["sub_lemma"].dropna().astype(str).values)
normalized_korpus = {unicodedata.normalize("NFC", word): word for word in korpus}
# korpus_sub = pd.read_csv("../korpusSubsLemma-NFC.csv")
# myresult = pd.read_csv("../korpusSubsLemma-NFC.csv")
# print("item cek: ", df_kamus)
# data_kamus = pd.read_excel("../kamus-NFC.xlsx").values
# print("kamus cek : ", data_kamus)
kamus = {}
for data in data_kamus:
    # kamus[data[1]] = [data[2], data[3], data[4], data[5], data[6]]
    kamus[data[1]] = [data[2]]
data = pd.read_csv(
    "https://raw.githubusercontent.com/ThoriqFathu/skripsi/main/data-desa.txt",
    sep=",",
    names=["id", "id_", "nama"],
)
V_Geo = data["nama"].str.upper().values
V_Preposition = ["è", "è", "ka", "ḍâ'", "neng", "ḍâri", "sampè"]
V_Loc = [
    "alamat",
    "dhisa",
    "koṭṭa",
    "kampong",
    "polo",
    "gheḍḍhung",
    "jhâlân",
    "gang",
    "masjid",
    "bâkap",
    "bèntèng",
    "pasar",
    "kecamadhân",
]


korpus_SLA = pd.read_excel("../klimat_wsd.xlsx")


# Cache for distance calculations
distance_cache = defaultdict(dict)
translate_cache = {}


def calculate_distance(normalized_char1, normalized_char2):
    if normalized_char2 in distance_cache[normalized_char1]:
        return distance_cache[normalized_char1][normalized_char2]
    dld = DamerauLevenshtein.distance(normalized_char1, normalized_char2)
    distance_cache[normalized_char1][normalized_char2] = dld
    return dld


def c_ngram(token, n):
    # token = kalimat.split()
    if n == 2:
        ngram = [f"{token[i]} {token[i+1]}" for i in range(len(token) - 1)]
    else:
        ngram = [f"{token[i]} {token[i+1]} {token[i+2]}" for i in range(len(token) - 2)]
    # print(ngram)
    return ngram


def rules_tri_bi(tokens, n, V_Preposition, V_Loc, V_Geo, dic):
    ngram = c_ngram(tokens, n)
    for i, elemen in enumerate(ngram):
        # print("elemen 0", elemen[0])
        if i > 0:
            if tokens[i - 1] in V_Preposition or tokens[i - 1] in V_Loc:
                if elemen == elemen.title():
                    # print('tilte', elemen)
                    for j in range(i, i + n):
                        # dic[tokens[j].lower()] = "loc"
                        dic[j][1] = "loc"

                elif elemen.upper() in V_Geo:
                    for j in range(i, i + n):
                        # dic[tokens[j].lower()] = "loc"
                        dic[j][1] = "loc"
                    # print('wilayah',elemen)
            else:
                if elemen == elemen.title():
                    for j in range(i, i + n):
                        # dic[tokens[j].lower()] = "loc"
                        dic[j][1] = "loc"
                    # print('tilte', elemen)
                elif elemen.upper() in V_Geo:
                    for j in range(i, i + n):
                        # dic[tokens[j].lower()] = "loc"
                        dic[j][1] = "loc"
                    # print('wilayah',elemen)
        else:
            if elemen == elemen.title():
                for j in range(i, i + n):
                    # dic[tokens[j].lower()] = "loc"
                    dic[j][1] = "loc"
                # print('tilte', elemen)
            elif elemen.upper() in V_Geo:
                for j in range(i, i + n):
                    # dic[tokens[j].lower()] = "loc"
                    dic[j][1] = "loc"
    # st.write(f"jumlah n ={n} : {dic}")
    return dic


def NER_location(tokens, V_Geo, V_Loc, V_Preposition):
    # data = pd.read_csv('data-desa.txt', sep=",", names=['id','id_', 'nama'])

    # print(kalimat)
    # st.write("token : ",tokens)
    # tokens = kalimat.split()

    # bigram = c_bigram(tokens)
    # trigram = c_trigram(tokens)
    dic = []
    for token in tokens:
        dic.append([token.lower(), None])
    # print(dic)
    # dic = rules_tri_bi(tokens, trigram, 3, V_Preposition, V_Loc, V_Geo, dic)
    # dic = rules_tri_bi(tokens, bigram, 2, V_Preposition, V_Loc, V_Geo, dic)
    for n in range(2, 4):
        dic = rules_tri_bi(tokens, n, V_Preposition, V_Loc, V_Geo, dic)
    # print("tribi = ",dic)
    for i, elemen in enumerate(tokens):
        # print("elemen 0", elemen[0])
        if i > 0:
            if tokens[i - 1] in V_Preposition or tokens[i - 1] in V_Loc:
                if elemen == elemen.title():
                    # print('tilte', elemen)

                    # dic[tokens[i].lower()] = "loc"
                    dic[i][1] = "loc"
                elif elemen.upper() in V_Geo:

                    # dic[tokens[i].lower()] = "loc"
                    dic[i][1] = "loc"
                    # print('wilayah',elemen)

    # print(dic)
    return dic


def damerau_levenshtein_distance(str1, str2):
    # Matriks untuk menyimpan jarak Damerau-Levenshtein
    d = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    # Inisialisasi baris pertama dan kolom pertama
    for i in range(len(str1) + 1):
        d[i][0] = i
    for j in range(len(str2) + 1):
        d[0][j] = j

    # Mengisi matriks berdasarkan operasi penyisipan, penghapusan, penggantian, dan transposisi
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,  # Operasi penghapusan
                d[i][j - 1] + 1,  # Operasi penyisipan
                d[i - 1][j - 1] + cost,  # Operasi penggantian
            )

            # Operasi transposisi
            if (
                i > 1
                and j > 1
                and str1[i - 1] == str2[j - 2]
                and str1[i - 2] == str2[j - 1]
            ):
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)

    return d[len(str1)][len(str2)]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data_input = request.get_json()
    user_input = data_input.get("text", "")
    # print(user_input)
    # user_input = request.form["inputText"]
    obj = Translator()
    user_input = obj.norm_char(user_input)
    tokens = obj.ghalluIdentification(
        obj.ceIdentification(obj.tokenizing(obj.punc_removal(user_input)))
    )
    user_input_prep = " ".join(tokens)
    # print("cek input : ", user_input_prep)
    if user_input_prep in translate_cache:
        # print("cek logika : ", True)
        result, detils = translate_cache[user_input_prep]
    else:
        hasil_NER = NER_location(tokens, V_Geo, V_Loc, V_Preposition)
        # obj = Translator()
        result, detils = obj.translate(
            hasil_NER, user_input, kamus, data_ambigu, korpus_SLA, korpus_sub
        )
        translate_cache[user_input_prep] = (result, detils)
    # print("dic cache : ", translate_cache)
    # return render_template("index.html", hasil=result, user_input=user_input)
    ###############################################
    ambigu = False
    tag_detil_result = "<h5>Sentence</h5><p>"
    for restok in detils:
        if len(restok[1]) != 0 and restok[1][1] > 1:
            ambigu = True
        tag_detil_result += f"<span style='color: {restok[2]}'>{restok[0]}</span> "
    tag_detil_result += "</p>"

    tag_ambigu = ""
    if ambigu:
        tag_ambigu = "<h5>Ambiguous detail:</h5><div>"
        for til in detils:

            if len(til[1]) == 0:
                pass
            else:
                if til[1][1] > 1 and not til[3]:
                    tag_ambigu += f"<p style='color:green;'>{til[0]} => {til[1][0]}</p>"
                    for num, det in enumerate(til[1][2]):
                        tag_ambigu += f"<p>arti ke {num+1}: ({det[0]} , {det[1]})</p>"
        tag_ambigu += "</div>"
    return jsonify(
        hasil=result,
        user_input=user_input,
        detils=detils,
        tag_detil_result=tag_detil_result,
        tag_ambigu=tag_ambigu,
        status_ambigu=ambigu,
    )


@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()
    text = data.get("text", "")
    # myresult = pd.read_excel("../korpuskata-NFC.xlsx")
    # korpus = myresult["kata"].values
    # myresult = pd.read_csv("../korpusSubsLemma-NFC.csv")
    # korpus = myresult["sub_lemma"].values
    user_input = text.split()
    lis_cor = []
    lis_pos = []
    correct = ""
    status = True
    for token in user_input:
        dis = {}
        if token in korpus:
            correct += token
            lis_pos.append(True)
            # lis_cor.append([token, token, token])
        else:
            status = False

            normalized_char1 = unicodedata.normalize("NFC", token)
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(
                        calculate_distance, normalized_char1, normalized_char2
                    ): normalized_char2
                    for normalized_char2 in normalized_korpus
                }
                for future in futures:
                    normalized_char2 = futures[future]
                    try:
                        dld = future.result()
                        dis[normalized_char2] = dld
                    except Exception as e:
                        print(f"Error calculating distance: {e}")

            correctWord = min(dis, key=dis.get)
            correct += correctWord + " "
            sorted_dis = sorted(dis.items(), key=lambda item: item[1])
            lis_cor.append([sorted_dis[0][0], sorted_dis[1][0], sorted_dis[2][0]])
            lis_pos.append(False)
    import itertools

    def combine_arrays(arrays):
        return itertools.product(*arrays)

    sug = combine_arrays(lis_cor)

    results = []
    for z, combination in enumerate(sug):
        txt = ""
        pos_sug = 0
        for pos, is_correct in enumerate(lis_pos):
            if is_correct:
                txt += user_input[pos]
            else:
                txt += combination[pos_sug]
                pos_sug += 1
            if pos != len(lis_pos) - 1:
                txt += " "
        results.append({"id": z + 1, "correct": txt})
        # pos_det += 1
    return jsonify(data=results, correct=status)
    # blob = TextBlob(text)
    # corrected_text = str(blob.correct())
    # return jsonify({"corrected_text": text})
    # return jsonify({"corrected_text": corrected_text})


if __name__ == "__main__":
    app.run(debug=True)
