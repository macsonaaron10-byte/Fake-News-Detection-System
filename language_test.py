from langdetect import detect

text = "Government launches new policy"

language = detect(text)

print(language)