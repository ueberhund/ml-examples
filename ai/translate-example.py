import boto3

#POC code to show how to detect a lanaguage and then translate between the detected lanaguage
#and other languages. In this case, a customer requested if we could translate between Simplified
#Chinese (zh) and Traditional Chinese (zh-TW). This example shows how to do that 

language_text = """羅素·納爾遜會長

只要你對主和祂的聖職能力運用信心，就會更有能力汲取主準備好的靈性寶藏。

謝謝各位提供這麼美妙的音樂。我們中場起立唱「感謝神賜我們先知」這首聖詩時，我有兩個很強烈的感想。一個是先知約瑟·斯密是這個福音期的先知。我對他的愛和敬佩與日俱增。第二個想法是我看著我的妻子、女兒、孫女和曾孫女，我感覺很希望你們每個人都是我的家人。

幾個月前，在聖殿一場恩道門結束後，我對妻子溫蒂說：「我希望姊妹們了解在聖殿中那些屬於她們的靈性寶藏。」姊妹們，我發現自己經常想到你們，包括兩個月前，我和溫蒂拜訪賓夕法尼亞州哈茂耐的時候"""

#Start out by detecting the dominant language
client = boto3.client("comprehend")
response = client.detect_dominant_language(Text=language_text)

dominant_language_code = response['Languages'][0]['LanguageCode']

#If this is Traditional Chinese (zh-TW), then we want to translate into Simplified Chinese (zh) and vice versa
language_code = ''
if dominant_language_code == 'zh-TW':
    language_code = 'zh'
else:
    language_code = 'zh-TW'

#Now that we have the dominant language, pass this into Translate to provide the translation
client = boto3.client('translate')

response = client.translate_text(Text=language_text,
  SourceLanguageCode=dominant_language_code, TargetLanguageCode=language_code)

#Print out the translated text
print(response['TranslatedText'])
