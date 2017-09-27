import jellyfish
import re

def normalizeWord(word):
    return re.sub("[^\w]", "", word.lower()).strip()

def encPhone(english_word):
    english_word=normalizeWord(english_word)
    #print(english_word)
    encoded={'origin':english_word}
    encoded['metaphone']=jellyfish.metaphone(english_word)
    encoded['soundex']=jellyfish.soundex(english_word)
    encoded['nysiis']=jellyfish.nysiis(english_word)
    encoded['match_rating_codex']=jellyfish.match_rating_codex(english_word)
    return encoded

def encPhonePerWord(english_sentence):
    encoded={'origin':english_sentence}
    words=list(map(normalizeWord,english_sentence.split()))
    #print(words)
    encoded['metaphone']=" ".join(map(jellyfish.metaphone,words))
    encoded['soundex']=" ".join(map(jellyfish.soundex,words))
    encoded['nysiis']=" ".join(map(jellyfish.nysiis,words))
    encoded['match_rating_codex']=" ".join(map(jellyfish.match_rating_codex,words))
    return encoded

def encPhoneVariants(english_sth):
    return[encPhone(english_sth),encPhonePerWord(english_sth)]