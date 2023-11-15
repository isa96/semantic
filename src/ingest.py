# TODO: Upsampling low representation class with product name variation from LLM services.
import json 
import openai
from collections import Counter

# Configure API Key
OPENAI_KEY = json.load(open("./secret/openai-cred.json", "r"))["OPENAI_KEY"]
openai.api_key = OPENAI_KEY

# Load Corpus
data_corpus = json.load(open('corpus/reguler.json', 'r'))

if __name__ == "__main__":
    frequency_label = Counter(list(map(lambda x: x['Jenis Produk'], data_corpus)))
    frequency_label = dict(frequency_label)
    for key in frequency_label:
        print(f"[*] {key} \t\t: {frequency_label[key]}")
        """
        >>> [*] Bahan tambahan pangan               : 220
        >>> [*] Ikan dan produk perikanan, ...      : 97
        >>> [*] Daging dan produk olahan daging     : 169
        >>> [*] Susu dan analognya                  : 116
        >>> [*] Pangan olahan untuk keperluan ...   : 35
        >>> [*] Buah dan sayur dengan pengolahan..  : 108
        >>> [*] Makanan ringan siap santap          : 70
        >>> [*] Kembang gula/permen dan cokelat     : 71
        >>> [*] Lemak, minyak, dan emulsi minyak    : 69
        >>> [*] Produk bakeri                       : 111
        >>> [*] Serealia dan produk serealia ...    : 123
        >>> [*] Telur olahan dan produk ...         : 24
        >>> [*] Gula dan pemanis termasuk madu      : 55
        >>> [*] Es untuk dimakan (edible ice) ...   : 20
        >>> [*] Garam, rempah, sup, saus, salad, ...: 102
        """