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

app = Flask(__name__)


def get_db_connection():
    try:
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "madureseset",
        }
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Fungsi untuk menerapkan normalisasi NFC
def normalize_nfc(text):
    return unicodedata.normalize("NFC", text)


@app.route("/kamus", methods=["GET"])
def get_dictionary():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, `basic_lemma` AS total FROM `lemmata`")
    myresult = cursor.fetchall()
    cursor.close()
    # connection.close()
    df_kamus = pd.DataFrame(myresult, columns=["id", "madura"])
    cursor = connection.cursor()
    cursor.execute(
        "SELECT* FROM substitution_lemmata INNER JOIN sentences ON substitution_lemmata.sentence_id = sentences.id WHERE `language` = 'IND' and sentences.index = 1 GROUP BY substitution_lemmata.sentence_id"
    )
    myresult = cursor.fetchall()
    cursor.close()
    connection.close()
    df_kalimat = pd.DataFrame(myresult)
    tempArti = []
    for subslem, sentence in zip(df_kalimat[1], df_kalimat[10]):
        if subslem == "":
            tempArti.append(sentence)
        else:
            tempArti.append(subslem)
    df_kamus["indonesia"] = tempArti
    df_kamus[["madura", "indonesia"]] = df_kamus[["madura", "indonesia"]].applymap(
        normalize_nfc
    )

    mad_bersih_kamus = []
    for i in df_kamus["madura"]:
        if "(h)" in i or "(h).v." in i or "(h)n." in i:
            spl = i.split("(")
            # print(spl[0])
            mad_bersih_kamus.append(spl[0])
        else:
            mad_bersih_kamus.append(i)

    df_kamus["madura"] = mad_bersih_kamus

    # Mengonversi DataFrame ke JSON
    json_result = df_kamus.to_json(orient="records")
    return jsonify(kamus=json_result)


@app.route("/ambigu", methods=["GET"])
def get_ambigu():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, `basic_lemma` AS total FROM `lemmata`")
    myresult = cursor.fetchall()
    cursor.close()
    # connection.close()
    df = pd.DataFrame(myresult, columns=["id", "madura"])

    count_values = df["madura"].value_counts()
    # count_values

    # # Ambil madura yang terhitung lebih dari 1
    nilai_terhitung_lebih_dari_satu = count_values[count_values > 1].index.tolist()
    nilai_terhitung_lebih_dari_satu

    # # Filter dataframe untuk madura yang terhitung lebih dari 1
    df_ambigu = df[df["madura"].isin(nilai_terhitung_lebih_dari_satu)]

    cursor = connection.cursor()
    cursor.execute(
        "SELECT* FROM substitution_lemmata INNER JOIN sentences ON substitution_lemmata.sentence_id = sentences.id WHERE `language` = 'IND' and sentences.index = 1 GROUP BY substitution_lemmata.sentence_id"
    )
    myresult = cursor.fetchall()
    cursor.close()
    connection.close()

    df = pd.DataFrame(myresult)
    df_id_ambigu = df_ambigu["id"]
    # # # Filter dataframe untuk madura yang terhitung lebih dari 1
    df_terhitung_lebih_dari_satu = df[df[12].isin(df_id_ambigu)]

    tempArti = []
    for subslem, sentence in zip(
        df_terhitung_lebih_dari_satu[1], df_terhitung_lebih_dari_satu[10]
    ):
        if subslem == "":
            # print(subslem, sentence)
            tempArti.append(sentence)
        else:
            tempArti.append(subslem)
    df_ambigu["indonesia"] = tempArti
    df_ambigu[["madura", "indonesia"]] = df_ambigu[["madura", "indonesia"]].applymap(
        normalize_nfc
    )

    mad_bersih_ambigu = []
    for i in df_ambigu["madura"]:
        if "(h)" in i or "(h).v." in i or "(h)n." in i:
            spl = i.split("(")
            # print(spl[0])
            mad_bersih_ambigu.append(spl[0])
        else:
            mad_bersih_ambigu.append(i)

    df_ambigu["madura"] = mad_bersih_ambigu
    # Mengonversi DataFrame ke JSON
    json_result = df_ambigu.to_json(orient="records")
    return jsonify(ambigu=json_result)


@app.route("/subslemma", methods=["GET"])
def get_subslemma():
    connection = get_db_connection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM analisa_view WHERE language = 'MAD'")

    myresult = mycursor.fetchall()
    mycursor.close()
    # print(myresult)
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM analisa_view WHERE language = 'IND'")

    myresult_arti_subs = mycursor.fetchall()
    mycursor.close()

    df_subs_lemma = pd.DataFrame(myresult)
    df_subs_lemma = df_subs_lemma[[0, 7, 1]]
    df_subs_lemma = df_subs_lemma.rename(
        columns={0: "subs_lemma_id", 7: "sentence_id", 1: "sub_lemma"}
    )
    df_korpus = df_subs_lemma
    df_subs_lemma_arti = pd.DataFrame(myresult_arti_subs)
    df_subs_lemma_arti = df_subs_lemma_arti[[0, 7, 1]]
    df_subs_lemma_arti = df_subs_lemma_arti.rename(
        columns={0: "subs_lemma_id", 7: "sentence_id", 1: "sub_lemma"}
    )

    temp_arti_subs = []
    for id in df_subs_lemma["sentence_id"]:

        temp_ = df_subs_lemma_arti[df_subs_lemma_arti["sentence_id"] == id + 1][
            "sub_lemma"
        ].values
        if len(temp_) == 0:
            print(temp_)
            temp_arti_subs.append("")
        else:
            temp_arti_subs.append(temp_[0])
    df_korpus["arti"] = temp_arti_subs

    df_korpus["sub_lemma"] = df_korpus[
        [
            "sub_lemma",
        ]
    ].applymap(normalize_nfc)
    json_result = df_korpus.to_json(orient="records")
    return jsonify(subslemma=json_result)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
