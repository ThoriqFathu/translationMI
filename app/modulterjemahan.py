import unicodedata
from mecs import Stem


class Translator:
    def __init__(self):
        self.lemma = None
        self.suffix = None
        self.prefix = None
        self.nasal = None
        self.dic = False

    def cf(self, data):  # proses merubah seluruh huruf besar menjadi huruf kecil//
        return data.lower()

    def punc_removal(self, data):
        allowedChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij\
                klmnopqrstuvwxyz0123456789âèḍṭṭ '-.,()"
        # allowedChar = "abcdefghijklmnopqrstuvwxyz0123456789âḍèâ '-.,"
        temp = ""
        for char in data:
            if char in allowedChar:
                if char == "." or char == ",":
                    temp += " "
                else:
                    temp += char
        return temp

    def norm_char(self, text):
        return unicodedata.normalize("NFC", text)

    def tokenizing(self, data):
        return data.split()

    def ceIdentification(self, token):
        affixes = ["na", "da", "sa", "ra", "nga", "eng", "ma", "dha"]
        targetIndices = []
        for i in range(len(token)):  # proses rule based term ce'
            if token[i] == "cè'":
                targetIndices.append(i + 1)

        for j in targetIndices:  # identifikasi imbuan pada term setelah term ce'''
            for affixTerm in affixes:
                if token[j].endswith(affixTerm):
                    if affixTerm == "dha":
                        token[j] = token[j].replace("ddha", "t")
                    else:
                        token[j] = token[j].replace(affixTerm, "")
                    break
        return token

    def ghalluIdentification(self, token):  # proses identifikasi term ghallu
        demonstrative = [
            "rèya",
            "jarèya",
            "arèya",
            "jariya",
            "jiya",
            "jajiya",
            "jeh",
            "rowa",
            "arowa",
            "juwa",
        ]
        se = ["sè"]
        targetIndices = []
        for i in range(len(token)):
            if token[i] == "ghallu" and token[i - 2] in se:
                targetIndices.append(i - 1)
            elif token[i] == "ghallu" and token[i - 2] in demonstrative:
                targetIndices.append(i - 1)
            elif token[i] == "ghallu" and token[i - 1].startswith(
                "ta"
            ):  # contoh term = tamera
                targetIndices.append(i - 1)
                token[i - 1] = token[i - 1][2 : (len(token[i - 1]))]

        # indekstarget = rajah, kene'
        for j in targetIndices:
            token[j], token[j + 1] = token[j + 1], token[j]
        # print("testing = ", token)
        return token

    def repetitive(self, term, dictionary):
        temp = term.split("-")
        # print("true")
        if (
            temp[0] == temp[1]
        ):  # term Ulang Sempurna. contoh term: mogha-mogha, #revisi pengecekan term ulang sempurna
            # if temp[1] not in dictionary:
            # if temp[1] in dictionary:
            #     self.dic = True
            return {"kd": temp[1], "prefix": "", "suffix": ""}
        else:
            if temp[0].startswith("e"):
                if temp[0].startswith("e") and temp[1].endswith(
                    "aghi"
                ):  # term Ulang Dwi Lingga Berimbuhan e- dan -aghi.contoh term: ekol-pokolaghi
                    self.prefix = "e"
                    self.suffix = "aghi"
                    # if temp[1][: temp[1].index("aghi")] in dictionary:
                    #     self.dic = True
                    return {
                        "kd": temp[1][: temp[1].index("aghi")],
                        "prefix": "di",
                        "suffix": "kan",
                    }
                else:
                    self.prefix = "e"
                    # if temp[1] in dictionary:
                    #     self.dic = True
                    return {
                        "kd": temp[1],
                        "prefix": "di",
                        "suffix": "",
                    }  # term Ulang Dwi Lingga Berimbuhan e-. contoh term: ero-soro
            elif temp[0].startswith(
                "a"
            ):  # term Ulang Dwi Lingga Tidak Berimbuhan a-. contoh term: areng-sareng
                if temp[0].startswith("a") and temp[1].endswith(
                    "an"
                ):  # term Ulang Dwi Lingga Berimbuhan a- dan -an.contoh term: aka'-berka'an
                    self.prefix = "a"
                    self.suffix = "an"
                    # if temp[1][: temp[1].index("an")] in dictionary:
                    #     self.dic = True
                    return {
                        "kd": temp[1][: temp[1].index("an")],
                        "prefix": "ber",
                        "suffix": "an",
                    }
                else:
                    # if temp[1] in dictionary:
                    #     self.dic = True
                    self.prefix = "a"
                    return {"kd": temp[1], "prefix": "ber", "suffix": ""}
            elif temp[1].endswith(
                "na"
            ):  # term Ulang Dwi Lingga Berimbuhan -na. contoh term: ca-kancana
                self.suffix = "na"
                # if temp[1][: temp[1].index("na")] in dictionary:
                #     self.dic = True
                return {
                    "kd": temp[1][: temp[1].index("na")],
                    "prefix": "",
                    "suffix": "nya",
                }
            elif temp[1].endswith("an"):
                self.suffix = "an"
                # if temp[1][: temp[1].index("an")] in dictionary:
                #     self.dic = True
                return {
                    "kd": temp[1][: temp[1].index("an")],
                    "prefix": "",
                    "suffix": "an",
                }  # term Ulang Dwi Lingga Berimbuhan -an. contoh term: ca-kancaan
            elif temp[1].endswith("ân"):
                self.suffix = "ân"
                # if temp[1][: temp[1].index("ân")] in dictionary:
                #     self.dic = True
                return {
                    "kd": temp[1][: temp[1].index("ân")],
                    "prefix": "",
                    "suffix": "an",
                }
            elif temp[1].endswith("a"):
                # if temp[1][: temp[1].index("a")] in dictionary:
                #     self.dic = True
                return {"kd": temp[1][: temp[1].index("a")], "prefix": "", "suffix": ""}
            elif temp[1].endswith(
                temp[0]
            ):  # term Ulang Dwi Lingga Tidak Berimbuhan. #contoh term: ku-buku,
                # if temp[1] in dictionary:
                #     self.dic = True
                return {"kd": temp[1], "prefix": "", "suffix": ""}
            # add thoriq
            else:
                return {"kd": term, "prefix": "", "suffix": ""}

    def affixInfix(self, term, dictionary):
        term = term.replace("ten", "t")
        self.prefix = "ten"
        # if term in dictionary:
        #     self.dic = True
        return {
            "kd": term,
            "prefix": "di",
        }  # contoh term: tenolong-->tolong-->ditolong, tenompang-->tompang-ditumpang (sisipan 'en')

    def affixPrefix(self, term, dictionary):
        # if term[1:] in dictionary:
        #     self.dic = True
        return {"kd": term[1:], "prefix": "ter"}

    def paPrefix(self, term, dictionary):
        self.suffix = "pa"
        # if term[2 : term.index("na")] in dictionary:
        #     self.dic = True
        return {"kd": term[2 : term.index("na")], "suffix": "annya"}

    def kaPrefix(self, term, dictionary):
        if term.startswith("ka") and term.endswith("ânna"):
            self.prefix = "ka"
            self.suffix = "ânna"
            # if term[2 : term.index("ânna")] in dictionary:
            #     self.dic = True
            return {
                "kd": term[2 : term.index("ânna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif term.startswith("ka") and term.endswith("anna"):
            self.prefix = "ka"
            self.suffix = "anna"
            # if term[2 : term.index("anna")] in dictionary:
            #     self.dic = True
            return {
                "kd": term[2 : term.index("anna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif term.startswith("ka") and term.endswith("an"):
            self.prefix = "ka"
            self.suffix = "an"
            # if term[2 : term.index("an")] in dictionary:
            #     self.dic = True
            return {"kd": term[2 : term.index("an")], "prefix": "ke", "suffix": "an"}
        elif term.startswith("ka") and term.endswith("ân"):
            self.prefix = "ka"
            self.suffix = "ân"
            # if term[2 : term.index("ân")] in dictionary:
            #     self.dic = True
            return {"kd": term[2 : term.index("ân")], "prefix": "ke", "suffix": "an"}
        # add thoriq
        else:
            return {"kd": term, "prefix": "", "suffix": ""}

    def nasalPrefix(self, term, dictionary):
        if term.startswith("nge"):
            term = term.replace("nge", "")
            self.nasal = "nge"
            # add thoriq
            # if term in dictionary.keys():
            #     self.dic = True
            return {"kd": term, "prefix": "me", "suffix": ""}
        elif term.startswith("ng"):
            temp = term + ""
            temp = temp.replace("ng", "")
            self.nasal = "ng"
            if temp in dictionary.keys():
                # self.dic = True
                if temp.endswith("è"):
                    return {"kd": temp, "prefix": "me", "suffix": "i"}
                else:
                    return {"kd": temp, "prefix": "me", "suffix": ""}
            else:
                temp2 = term + ""
                temp2 = term.replace("ng", "gh")
                if temp2 in dictionary.keys():
                    # self.dic = True
                    return {"kd": temp2, "prefix": "meng", "suffix": ""}
                else:
                    temp3 = term + ""
                    temp3 = term.replace("ng", "k")
                    if temp3 in dictionary.keys():
                        # self.dic = True
                        return {"kd": temp3, "prefix": "meng", "suffix": ""}
                    # add thoriq
                    else:
                        self.nasal = None
                        return {"kd": term, "prefix": "", "suffix": ""}

        elif term.startswith("ny"):
            temp = term + ""
            temp = temp.replace("ny", "c")
            self.nasal = "ny"
            if temp in dictionary.keys():
                # self.dic = True
                return {"kd": temp, "prefix": "men", "suffix": ""}
            else:
                temp2 = term + ""
                temp2 = term.replace("ny", "j")  # nyajhal --> jajhal
                if temp2 in dictionary.keys():
                    # self.dic = True
                    return {"kd": temp2, "prefix": "men", "suffix": ""}
                else:
                    temp3 = term + ""
                    temp3 = term.replace("ny", "s")  # nyabun --> sabun
                    if temp3 in dictionary.keys():
                        # self.dic = True
                        return {"kd": temp3, "prefix": "meny", "suffix": ""}
                    # add thoriq
                    else:
                        self.nasal = None
                        return {"kd": term, "prefix": "", "suffix": ""}
        elif term.startswith("m"):
            temp = list(term)
            temp[0] = "b"
            newTerm = "".join(temp)
            self.nasal = "m"
            if newTerm in dictionary.keys():
                # self.dic = True
                return {"kd": newTerm, "prefix": "mem", "suffix": ""}
            else:
                temp[0] = "p"
                newTerm = "".join(temp)
                # add thoriq
                # if newTerm in dictionary.keys():
                # self.dic = True
                return {"kd": newTerm, "prefix": "mem", "suffix": ""}
        elif term.startswith("n"):
            temp = list(term)
            temp[0] = "t"
            newTerm = "".join(temp)

            if newTerm in dictionary.keys():
                # self.dic = True
                self.nasal = "n"
                return {"kd": newTerm, "prefix": "men", "suffix": ""}
            # add thoriq
            else:
                return {"kd": term, "prefix": "", "suffix": ""}

    def affix(self, term, dictionary):
        if term.endswith("na"):
            if term.startswith("sa") and term.endswith("na"):
                temp = term + ""
                temp = temp[2:]
                temp = temp.replace("na", "")
                # print(temp)
                if temp in dictionary.keys():
                    # self.dic = True
                    self.prefix = "sa"
                    self.suffix = "na"
                    return {"kd": temp, "prefix": "se", "suffix": "nya"}
                else:
                    temp2 = term + ""
                    temp2 = term.replace("na", "")
                    if temp2 in dictionary.keys():
                        # self.dic = True
                        self.suffix = "na"
                        return {"kd": temp2, "prefix": "", "suffix": "nya"}
                    # add thoriq
                    else:
                        return {"kd": term, "prefix": "", "suffix": "nya"}

            elif term.endswith("ânna"):
                self.suffix = "ânna"
                # add thoriq
                # if term[: term.index("ânna")] in dictionary.keys():
                #     self.dic = True
                return {
                    "kd": term[: term.index("ânna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            elif term.endswith("anna"):
                self.suffix = "anna"
                if term[: term.index("anna")] in dictionary.keys():
                    self.dic = True
                return {
                    "kd": term[: term.index("anna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            else:
                # add thoriq
                temp = term.replace("na", "")
                if temp in dictionary:
                    self.suffix = "na"
                    # self.dic = True
                    return {"kd": temp, "prefix": "", "suffix": "nya"}
                else:
                    return {"kd": term, "prefix": "", "suffix": ""}
        elif term.endswith("aghi"):
            self.suffix = "aghi"
            if term.startswith("e") and term.endswith("aghi"):
                self.prefix = "e"
                # add thoriq
                # if term[1 : term.index("aghi")] in dictionary.keys():
                #     self.dic = True
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif term.startswith("è") and term.endswith("aghi"):
                self.prefix = "è"
                # if term[1 : term.index("aghi")] in dictionary.keys():
                #     self.dic = True
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif term.startswith("a") and term.endswith("aghi"):
                self.prefix = "a"
                # if term[1 : term.index("aghi")] in dictionary.keys():
                #     self.dic = True
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "meng",
                    "suffix": "kan",
                }
            else:
                # if term[: term.index("aghi")] in dictionary.keys():
                #     self.dic = True
                return {"kd": term[: term.index("aghi")], "prefix": "", "suffix": "kan"}
        elif term.startswith("ta"):
            self.prefix = "ta"
            # if term[2:] in dictionary.keys():
            #     self.dic = True
            return {"kd": term[2:], "prefix": "ter", "suffix": ""}
        elif term.startswith("ma"):
            self.prefix = "ma"
            # if term[2:] in dictionary.keys():
            #     self.dic = True
            return {"kd": term[2:], "prefix": "memper", "suffix": ""}
        elif term.startswith("ka"):
            self.prefix = "ka"
            # if term[2:] in dictionary.keys():
            #     self.dic = True
            if term.startswith("ka") and term.endswith("'"):
                return {"kd": term[2:], "prefix": "ber", "suffix": ""}
            else:
                return {"kd": term[2:], "prefix": "ter", "suffix": ""}
        elif term.startswith("sa"):
            if term.startswith("sa") and term.endswith("sa"):
                self.prefix = "sa"
                self.suffix = "sa"
                # if term[2 : term.index("sa")] in dictionary.keys():
                #     self.dic = True
                return {
                    "kd": term[2 : term.index("sa")],
                    "prefix": "se",
                    "suffix": "nya",
                }
            else:
                # add thoriq
                if term[2:] in dictionary:
                    # self.dic = True
                    self.prefix = "sa"
                    return {"kd": term[2:], "prefix": "se", "suffix": ""}
                else:
                    return {"kd": term, "prefix": "", "suffix": ""}

        elif term.startswith("pa"):
            self.prefix = "pa"
            # if term[2:] in dictionary:
            #     self.dic = True
            return {"kd": term[2:], "prefix": "pe", "suffix": ""}
        elif term.startswith("pe"):
            self.prefix = "pe"
            # if term[2:] in dictionary:
            #     self.dic = True
            return {"kd": term[2:], "prefix": "pe", "suffix": ""}
        elif term.endswith("è"):
            self.suffix = "è"
            # if term[: term.index("è")] in dictionary:
            #     self.dic = True
            return {"kd": term[: term.index("è")], "prefix": "", "suffix": "kan"}
        elif term.endswith("an"):
            if term.startswith("a") and term.endswith("an"):
                self.suffix = "an"
                self.prefix = "a"
                # if term[1 : term.index("an")] in dictionary:
                #     self.dic = True
                return {"kd": term[1 : term.index("an")], "prefix": "ber", "suffix": ""}
            elif term.startswith("pa") and term.endswith("an"):
                # if term[2 : term.index("an")] in dictionary:
                #     self.dic = True
                return {"kd": term[2 : term.index("an")], "prefix": "", "suffix": ""}
            elif term.startswith("sa") and term.endswith("an"):
                self.prefix = "sa"
                self.suffix = "an"
                # if term[2 : term.index("an")] in dictionary:
                #     self.dic = True
                return {
                    "kd": term[2 : term.index("an")],
                    "prefix": "se",
                    "suffix": "an",
                }
            else:
                self.suffix = "an"
                # if term[2 : term.index("an")] in dictionary:
                #     self.dic = True
                return {"kd": term[: term.index("an")], "prefix": "", "suffix": "an"}
        elif term.endswith("ân"):
            if term.endswith("ân"):
                self.suffix = "ân"
                # if term[: term.index("ân")] in dictionary:
                #     self.dic = True
                return {"kd": term[: term.index("ân")], "prefix": "", "suffix": "an"}
            elif term.startswith("a") and term.endswith("ân"):
                self.prefix = "a"
                # if term[1 : term.index("ân")] in dictionary:
                #     self.dic = True
                return {"kd": term[1 : term.index("ân")], "prefix": "ber", "suffix": ""}
            # elif term.startswith('ka') and term.endswith("'ân"):
            # return {'kd':term[2:term.index("ân")],'prefix':'','suffix':'an'}
            elif term.startswith("ka") and term.endswith("ân"):
                self.prefix = "ka"
                self.suffix = "ân"
                # if term[2 : term.index("ân")] in dictionary:
                #     self.dic = True
                return {
                    "kd": term[2 : term.index("ân")],
                    "prefix": "ke",
                    "suffix": "an",
                }
        elif term.endswith("ra"):
            self.suffix = "ra"
            # if term[: term.index("ra")] in dictionary:
            #     self.dic = True
            return {"kd": term[: term.index("ra")], "prefix": "", "suffix": "nya"}
        elif term.endswith("sa"):
            self.suffix = "sa"
            # if term[: term.index("sa")] in dictionary:
            #     self.dic = True
            return {"kd": term[: term.index("sa")], "prefix": "", "suffix": "nya"}
        elif term.endswith("èpon"):
            self.suffix = "èpon"
            # if term[: term.index("èpon")] in dictionary:
            #     self.dic = True
            return {"kd": term[: term.index("èpon")], "prefix": "", "suffix": "nya"}
        elif term.startswith("e"):
            if term.startswith("epa"):
                self.prefix = "epa"
                # if term[3:] in dictionary:
                #     self.dic = True
                return {"kd": term[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "e"
                # if term[1:] in dictionary:
                #     self.dic = True
                return {"kd": term[1:], "prefix": "di", "suffix": ""}
        elif term.startswith("è"):
            if term.startswith("èpa"):
                self.prefix = "èpa"
                # if term[3:] in dictionary:
                #     self.dic = True
                return {"kd": term[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "è"
                # if term[1:] in dictionary:
                #     self.dic = True
                return {"kd": term[1:], "prefix": "di", "suffix": ""}
        elif term.startswith("a"):
            self.prefix = "a"
            # if term[1:] in dictionary:
            #     self.dic = True
            return {"kd": term[1:], "prefix": "ber", "suffix": ""}

    def translate(
        self, hasil_NER, kalimat, dictionary, data_ambigu, korpus_SLA, korpus_subs
    ):
        # kalimat = self.ghalluIdentification(self.ceIdentification(kalimat))
        # token_kalimat = self.ghalluIdentification(
        #     self.ceIdentification(self.tokenizing(self.cf(token_kalimat)))
        # )
        # kalimat_ = self.ghalluIdentification(
        #     self.ceIdentification(self.tokenizing(self.cf(kalimat)))
        # )
        # print(kalimat_)
        # hasil = ""
        # st.write(token_kalimat)
        ngram_subs = self.generate_ngrams_subs(kalimat, korpus_subs)
        dic_hasil_subs_awal = self.isi_arti_token(kalimat, ngram_subs)
        dic_hasil_subs = dic_hasil_subs_awal.copy()

        # print(ngram_subs)
        print("==========Translate=========")
        detils = []
        corrects = []
        orange = []
        biru = []
        merah = []
        hijau = []
        # for term in token_kalimat:
        # for pos, term in enumerate(kalimat_):
        for pos in range(len(hasil_NER)):
            hasil = ""
            term = hasil_NER[pos][0]
            # print(term)
            list_detil = []
            self.dic = False
            if hasil_NER[pos][1] != "loc":
                # if term == ".":
                #     hasil = hasil[: len(hasil) - 1]  # catatan
                #     hasil += ". "
                # elif term == ",":
                #     hasil = hasil[: len(hasil) - 1]
                #     hasil += ", "
                # else:
                if term == "ghallu":
                    hasil += "terlalu "
                    list_detil = [term, 1, ["terlalu"]]
                    # print(True)
                elif term == "è":
                    hasil += "di "
                    list_detil = [term, 1, ["di"]]
                elif term == "ka":
                    hasil += "ke "
                    list_detil = [term, 1, ["ke"]]
                else:
                    if "-" in term:
                        temp = self.repetitive(term, dictionary)
                        self.lemma = temp["kd"]
                        makna_SLA, list_detil = self.modified_SLA(
                            temp["kd"], kalimat, dictionary, data_ambigu, korpus_SLA
                        )
                        hasil += (
                            temp["prefix"]
                            + makna_SLA
                            + "-"
                            + makna_SLA
                            + temp["suffix"]
                            + " "
                        )
                    else:
                        if term not in dictionary.keys():
                            # print(term)

                            if term.startswith("pa") and term.endswith("na"):
                                temp = self.paPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += makna_SLA + temp["suffix"] + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("ka") and term.endswith("ân"):
                                temp = self.kaPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ka") and term.endswith("an"):
                                temp = self.kaPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ka") and term.endswith("ânna"):
                                temp = self.kaPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ka") and term.endswith("anna"):
                                temp = self.kaPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ten"):
                                temp = self.affixInfix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("ny"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    if temp["prefix"] == "meny":
                                        # print("meny")
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += temp["prefix"] + makna_SLA[1:] + " "
                                    else:
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("nge"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ng"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    if temp["kd"].startswith("k"):
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += (
                                            temp["prefix"]
                                            + makna_SLA[1:]
                                            + temp["suffix"]
                                            + " "
                                        )
                                    else:
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += (
                                            temp["prefix"]
                                            + makna_SLA
                                            + temp["suffix"]
                                            + " "
                                        )
                                else:
                                    hasil += term + " "
                            elif term.endswith("na"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.endswith("aghi"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("ta"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("ma"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("ka"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("sa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                # st.warning(self.dic)
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("pa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("pe"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA + " "
                                else:
                                    hasil += term + " "
                            elif term.endswith("è"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                    # hasil += (
                                    #     temp["prefix"]
                                    #     + dictionary[temp["kd"]][0]
                                    #     + temp["suffix"]
                                    #     + " "
                                    # )
                                else:
                                    hasil += term + " "
                            elif term.endswith("an"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.endswith("ân"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.endswith("ra"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += makna_SLA + temp["suffix"] + " "
                                else:
                                    hasil += term + " "
                            elif term.endswith("sa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                # print(True)
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        dictionary[temp["kd"]][0] + temp["suffix"] + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.endswith("èpon"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += makna_SLA + temp["suffix"] + " "
                                else:
                                    hasil += term + " "
                            elif term.startswith("a"):
                                tokens_kalimat = self.tokenizing(kalimat)
                                # print(token_kalimat[-1])
                                if term == tokens_kalimat[-1]:
                                    temp = self.affixPrefix(term, dictionary)
                                    self.lemma = temp["kd"]
                                    if temp["kd"] in dictionary.keys():
                                        self.dic = True
                                    if self.dic == True:
                                        # print(True)
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += temp["prefix"] + makna_SLA + " "
                                    else:
                                        hasil += term + " "
                                else:
                                    temp = self.affix(term, dictionary)
                                    self.lemma = temp["kd"]
                                    if temp["kd"] in dictionary.keys():
                                        self.dic = True
                                    if self.dic == True:
                                        # print(True)
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += (
                                            temp["prefix"]
                                            + makna_SLA
                                            + temp["suffix"]
                                            + " "
                                        )
                                    else:
                                        hasil += term + " "
                            elif term.startswith("e"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print("awal e")
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                else:
                                    hasil += term + " "
                            elif term.startswith("è"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    # print(True)
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += (
                                        temp["prefix"]
                                        + makna_SLA
                                        + temp["suffix"]
                                        + " "
                                    )
                                    # hasil += (
                                    #     temp["prefix"]
                                    #     + dictionary[temp["kd"]][0]
                                    #     + temp["suffix"]
                                    #     + " "
                                    # )
                                else:
                                    hasil += term + " "
                            elif term.startswith("m"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if temp["kd"].startswith("b"):
                                    if self.dic == True:
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += temp["prefix"] + makna_SLA + " "
                                    else:
                                        hasil += term + " "
                                else:
                                    if self.dic == True:
                                        makna_SLA, list_detil = self.modified_SLA(
                                            temp["kd"],
                                            kalimat,
                                            dictionary,
                                            data_ambigu,
                                            korpus_SLA,
                                        )
                                        hasil += temp["prefix"] + makna_SLA[1:] + " "
                                    else:
                                        hasil += term + " "
                            elif term.startswith("n"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                if temp["kd"] in dictionary.keys():
                                    self.dic = True
                                if self.dic == True:
                                    makna_SLA, list_detil = self.modified_SLA(
                                        temp["kd"],
                                        kalimat,
                                        dictionary,
                                        data_ambigu,
                                        korpus_SLA,
                                    )
                                    hasil += temp["prefix"] + makna_SLA[1:] + " "
                                else:
                                    hasil += term + " "
                            else:
                                hasil += term + " "
                                self.lemma = term

                        else:
                            # hasil += dictionary[term][0] + " "
                            makna_SLA, list_detil = self.modified_SLA(
                                term, kalimat, dictionary, data_ambigu, korpus_SLA
                            )
                            hasil += makna_SLA + " "
                            self.dic = True
                            self.lemma = term
            else:
                hasil += term + " "

            # if self.dic == False:
            #     pass
            # if kalimat.index(term) == 0:
            #     hasil = hasil.capitalize()

            # indeks = len(hasil) - 1
            # while hasil[indeks] != "." and indeks >= 0:
            #     indeks -= 1
            # if indeks > 0:
            #     text_temp = hasil[: indeks + 2]
            #     last_word = hasil[indeks + 2 : len(hasil)].capitalize()

            #     hasil = text_temp + last_word
            ###############################################
            # if hasil_NER[pos][1] == "loc":
            #     list_detil = [term, 1, [term]]
            #     detils.append([term, list_detil, "orange"])
            # elif len(list_detil) == 0:

            #     detils.append([term, list_detil, "red"])
            # elif list_detil[1] == 1:
            #     detils.append([term, list_detil, "blue"])

            # else:
            #     detils.append([term, list_detil, "green"])
            corrects.append(self.dic)

            # tambahan fitur untuk penelitian
            if hasil_NER[pos][1] == "loc":
                dic_hasil_subs[pos] = term
                detils.append([term, list_detil, "orange", False])
                # print(pos)
            elif dic_hasil_subs_awal[pos] == False:
                if self.dic == True:
                    if list_detil[1] > 1:
                        detils.append([term, list_detil, "green", False])
                    else:
                        detils.append([term, list_detil, "blue", False])
                    dic_hasil_subs[pos] = hasil[: len(hasil) - 1]
                    # print("cek TRUE : ", term, hasil[: len(hasil) - 1])
                    # pass
                else:
                    dic_hasil_subs[pos] = term
                    detils.append([term, list_detil, "red", False])
                    # print("cek FALSE: ", term, list_detil)
            else:
                # pass
                if self.dic == True:
                    if (
                        pos > 0
                        and dic_hasil_subs[pos] == dic_hasil_subs[pos - 1]
                        and len(dic_hasil_subs[pos].split()) > 1
                    ):
                        # Jika nilai dari kunci saat ini sama dengan nilai dari kunci sebelumnya, abaikan
                        detils.append([term, list_detil, "blue", True])
                        # pass
                    elif (
                        len(kalimat.split()) > 1
                        and pos < (len(kalimat.split()) - 1)
                        and dic_hasil_subs[pos] == dic_hasil_subs[pos + 1]
                        and len(dic_hasil_subs[pos].split()) > 1
                    ):
                        detils.append([term, list_detil, "blue", True])
                        # pass
                    else:
                        if list_detil[1] > 1:
                            detils.append([term, list_detil, "green", False])
                        else:
                            detils.append([term, list_detil, "blue", False])

                        dic_hasil_subs[pos] = hasil[: len(hasil) - 1]
                        # print(list_detil)
                else:
                    detils.append([term, list_detil, "blue", True])
        # for cek_subs in detils:
        #     print(f"cek subs : {cek_subs}")
        print(dic_hasil_subs_awal)
        print(dic_hasil_subs)
        hasil_kalimat = self.generate_arti(
            dic_hasil_subs_awal,
            dic_hasil_subs,
            kalimat,
            dictionary,
            data_ambigu,
            korpus_SLA,
        )
        # print(corrects)
        return hasil_kalimat, detils

    def generate_ngrams_subs(self, kalimat_input, df_korpus):
        # Memisahkan kalimat menjadi kata-kata
        kata_kata = kalimat_input.split()
        n = len(kata_kata)

        # Menghasilkan n-gram dari n sampai 1
        ngrams = []
        for i in range(n, 0, -1):
            temp_gram = []
            for j in range(0, n - i + 1):
                ngram = " ".join(kata_kata[j : j + i])
                if ngram in df_korpus["sub_lemma"].values:
                    arti_ = df_korpus[df_korpus["sub_lemma"] == ngram]["arti"].values[0]
                    # print(ngram)
                    # print(arti_)
                    temp_gram.append([ngram, arti_])
                else:
                    temp_gram.append([ngram, False])
            ngrams.append(temp_gram)
            # print(temp_gram)
        # print(len(ngrams))
        # print((ngrams))

        return ngrams

    # Fungsi untuk menandai kata pada kalimat
    def isi_arti_token(self, kalimat, array):
        kata_kata = kalimat.split()
        dic_token = {}
        for Itoken_ in range(len(kata_kata)):
            dic_token[Itoken_] = False
        print("dic_token : ", dic_token)
        hasil = []

        for posisi_kata, kata in enumerate(kata_kata):
            ditemukan = False
            # Mengecek frasa terlebih dahulu
            for sublist in array:
                for item in sublist:
                    if isinstance(item[1], str) and kata in item[0]:
                        # print(item[0])
                        # print(item[1])
                        # Memastikan bahwa kata merupakan bagian dari frasa dengan arti
                        frasa = item[0].split()
                        if kata in frasa:
                            hasil.append((kata, True))
                            # print(posisi_kata)
                            if dic_token[posisi_kata] == False:
                                if (
                                    posisi_kata < (len(kata_kata) - 1)
                                    and kata_kata[posisi_kata]
                                    != kata_kata[posisi_kata + 1]
                                    or posisi_kata > 0
                                    and kata_kata[posisi_kata]
                                    != kata_kata[posisi_kata - 1]
                                ):
                                    dic_token[posisi_kata] = item[1]
                                # print("kata :", kata)
                            ditemukan = True
                            break
                if ditemukan:
                    break
            # Jika tidak ditemukan dalam frasa, cek secara individu
            if not ditemukan:
                for sublist in array:
                    for item in sublist:
                        if isinstance(item[1], bool) and kata == item[0]:
                            hasil.append((kata, item[1]))
                            ditemukan = True
                            if dic_token[posisi_kata] == False:
                                dic_token[posisi_kata] = item[1]
                            break
                    if ditemukan:
                        break
            if not ditemukan:
                hasil.append((kata, False))
        return dic_token

    def generate_arti(
        self,
        dic_hasil_subs_awal,
        dic_hasil_subs_akhir,
        kalimat,
        dictionary,
        data_ambigu,
        korpus_SLA,
    ):
        kata_kalimat = kalimat.split()
        # Menggabungkan nilai-nilai dictionary menjadi satu kalimat
        keys = sorted(dic_hasil_subs_akhir.keys())
        result = []

        for i in range(len(keys)):
            if (
                i > 0
                and dic_hasil_subs_akhir[keys[i]] == dic_hasil_subs_akhir[keys[i - 1]]
                and len(dic_hasil_subs_akhir[keys[i]].split()) > 1
            ):
                # Jika nilai dari kunci saat ini sama dengan nilai dari kunci sebelumnya, abaikan
                continue
            elif (
                len(kata_kalimat) > 1
                and i == 0
                and dic_hasil_subs_akhir[keys[i]] == dic_hasil_subs_akhir[keys[i + 1]]
                and len(dic_hasil_subs_akhir[keys[i]].split()) > 1
            ):
                result.append(dic_hasil_subs_akhir[keys[i]])

            else:
                if dic_hasil_subs_awal[keys[i]] == False:
                    result.append(dic_hasil_subs_akhir[keys[i]])
                else:
                    # terapkan SLA
                    kata = kata_kalimat[keys[i]]
                    # result_SLA, list_detil = self.modified_SLA(
                    #     kata, kalimat, dictionary, data_ambigu, korpus_SLA
                    # )
                    # if list_detil[1] > 1:
                    #     result.append(result_SLA)
                    # else:
                    #     result.append(dic_hasil_subs_akhir[keys[i]])
                    result.append(dic_hasil_subs_akhir[keys[i]])

            # print(result)

        # Menggabungkan hasil menjadi satu kalimat
        hasil = " ".join(result)
        return hasil

    def modified_SLA(
        self, token, kalimat, dictionary, data_ambigu, korpus_SLA
    ):  # ganti nama function
        # data_ambigu = pd.read_excel("data-ambigu.xlsx")
        # st.write(token)
        # list_detil = []

        arti = 1  # default
        list_overlap = [dictionary[token][0]]
        # st.write("dic === ",dictionary[token])
        # data_ambigu = pd.read_csv("data-ambigu.csv")
        # data_ambigu = pd.read_csv(
        #     "https://raw.githubusercontent.com/ThoriqFathu/skripsi/main/data-ambigu.csv"
        # )
        if data_ambigu["madura"].isin([token]).any():
            indeks_boolean = data_ambigu["madura"] == token

            # Mengambil nilai dari semua kolom berdasarkan indeks boolean
            nilai_ditemukan = data_ambigu[indeks_boolean].values
            # st.write("nilai ditemukan = ", nilai_ditemukan)
            arti = len(nilai_ditemukan)
            hasil, list_overlap = self.SLA(
                kalimat, nilai_ditemukan, dictionary[token][0], korpus_SLA
            )
        else:
            hasil = dictionary[token][0]
        # list_detil.append()
        list_detil = [token, arti, list_overlap]
        # print([token, arti, list_overlap])
        return hasil, list_detil

    def compute_overlap(self, text1, text2):

        text1 = unicodedata.normalize("NFC", text1)
        text2 = unicodedata.normalize("NFC", text2)
        print("text1 :", text1)
        print("text2 :", text2)
        set1 = set(text1.split())
        set2 = set(text2.split())
        # st.write(f"stem has 1: {text1}")
        # st.write(f"stem has 2: {text2}")
        return len(set1.intersection(set2))

    def SLA(self, kalimat, data_ambigu, makna_awal, korpus_SLA):
        # korpus_SLA = pd.read_excel("klimat_wsd.xlsx")
        # korpus_SLA = pd.read_csv("klimat_wsd.csv")
        # korpus_SLA = pd.read_csv(
        #     "https://raw.githubusercontent.com/ThoriqFathu/skripsi/main/klimat_wsd.csv"
        # )
        kalimat = unicodedata.normalize("NFD", kalimat)
        kalimat_token = self.tokenizing(self.cf(kalimat))
        prep_kalimat = ""
        max_kalimat = len(kalimat_token)
        for pos_tok, tok in enumerate(kalimat_token):
            # Create stemmer
            stm = Stem.Stemmer()

            # stem
            term = tok
            stm.stemming(term)
            if pos_tok == max_kalimat - 1:
                if stm.lemma == None:
                    prep_kalimat += term
                else:
                    prep_kalimat += stm.lemma
            else:
                if stm.lemma == None:
                    prep_kalimat += term + " "
                else:
                    prep_kalimat += stm.lemma + " "
        makna_terbaik = makna_awal
        maks_overlap = 0
        list_overlap = []
        list_korpus = []
        # st.write(f"stem has: {prep_kalimat}")
        for id_ in data_ambigu:
            temp_list_korpus = []
            overlap = 0
            if korpus_SLA["id"].isin([id_[0]]).any():
                indeks_boolean = korpus_SLA["id"] == id_[0]

                # Mengambil nilai dari semua kolom berdasarkan indeks boolean
                nilai_ditemukan = korpus_SLA[indeks_boolean]["kalimat"].values
                for contoh_kalimat in nilai_ditemukan:
                    contoh_kalimat = unicodedata.normalize("NFD", contoh_kalimat)
                    contoh_kalimat_token = self.tokenizing(self.cf(contoh_kalimat))
                    prep_contoh_kalimat = ""
                    max_contoh_kalimat = len(contoh_kalimat_token)
                    for pos_tok_contoh, tok_contoh in enumerate(contoh_kalimat_token):
                        # Create stemmer
                        stm = Stem.Stemmer()
                        # stem
                        term = tok_contoh
                        stm.stemming(term)
                        if pos_tok_contoh == max_contoh_kalimat - 1:
                            prep_contoh_kalimat += stm.lemma
                        else:
                            prep_contoh_kalimat += stm.lemma + " "
                    overlap += self.compute_overlap(prep_kalimat, prep_contoh_kalimat)
                    temp_list_korpus.append(prep_contoh_kalimat)
                # print(overlap)
                if overlap > maks_overlap:
                    maks_overlap = overlap
                    makna_terbaik = id_[2]
                list_overlap.append([id_[2], overlap])
                list_korpus.append(temp_list_korpus)
            else:
                list_overlap.append([id_[2], overlap])
                # st.write(id_)

        ###################### TAMBAH BOBOT IDF ###################
        var_x = list_overlap[0][1]
        makna_sama_bool = all(sub_array[1] == var_x for sub_array in list_overlap)
        if makna_sama_bool:
            # print(list_korpus)
            makna_terbaik = list_overlap[0][0]
            max_sum = 0
            for ind_id in range(len(list_korpus)):
                idf_ = [
                    self.calculate_idf(tok_idf, list_korpus[ind_id])
                    for tok_idf in prep_kalimat.split()
                ]
                sum_idf = sum(idf_)
                if sum_idf > max_sum:
                    makna_terbaik = list_overlap[ind_id][0]
                    max_sum = sum_idf
        #         print(f"idf {list_overlap[ind_id][0]} :", idf_)
        #         print("sum_idf :", sum_idf)
        #     print(f"Makana terbaik : {makna_terbaik}")
        #     print(f"Maks IDF : {max_sum}")
        # print(list_overlap)
        return makna_terbaik, list_overlap

    def calculate_idf(self, word, corpus):
        import math

        # Jumlah total dokumen dalam korpus
        n = len(corpus)

        # Jumlah dokumen yang mengandung kata
        n_t = sum(1 for document in corpus if word in document.split())
        # print(f"{word} :{n}/{n_t}")
        # Menghitung nilai IDF
        idf = math.log(n / n_t) if n_t != 0 else 0

        return idf
