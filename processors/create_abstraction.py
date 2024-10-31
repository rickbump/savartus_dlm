
#from gensim.summarization import summarize
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#

extracted_text = "'Lemon Garlic Dump Chicken…It’s What’s For Dinner!\n\nI know it’s not the most pleasant-sounding name for a dinner entree, but don’t let the name fool you! Dump Chicken is not only delicious it’s deliciously EASY to make which makes it even more attractive for dinner! :-)\nYou may have\xa0heard of a thing called Dump CAKE…you know, where you “dump” a couple of ingredients (usually a cake mix and a can of fruit) into a 9×13 pan and bake? Well, Dump Chicken is just as easy as that PLUS you can make several different varieties and freeze them for future dinners! Can you tell I’m a big fan of this idea???\nWhen I saw the idea for “Dump Cooking” at The Lazy Gourmet\xa0I had a hard time choosing which recipe to try first…she has over twenty of them! Check them out!\nBut I decided on one of my favorite combinations – Lemon and Garlic.\xa0Another\xa0great thing about dump cooking is you probably already have all the necessary ingredients right in your\xa0pantry! No trip to the grocery store necessary. A major plus in my book!\n\nLemon & Garlic Chicken\nadapted from The Lazy Gourmet\n1 – 2 tsp minced garlic (I like more so I used 2)\n1/4 cup olive oil\n1 Tbls parsley flakes\n2 Tbls lemon juice (or the juice of one whole lemon)\n4-6 chicken breasts (or 8 to 10 chicken tenders)\nPlace all ingredients into a 1-gallon freezer bag. I used wide mouth half gallon\xa0mason jar to hold the bag upright while I filled it with the chicken and other ingredients.\n\n\n\n\n\xa0\nAfter sealing the bag, turn the bag over several times until everything is combined and the chicken is well coated. Freeze flat.\nHere is my Lemon Garlic Dump Chicken dinner all ready for the freezer……\n\n\xa0\nAnd here’s two “frozen dinners” all ready for freezer storage.\n\nTo cook you have a few different\xa0options: \nThaw chicken. Pour chicken and marinade into a baking dish, turn chicken to coat.\xa0Bake at 350 F for 35 minutes.\nOR\nThaw and grill in a cast iron skillet on the stove, or outside on the\xa0barbecue grill, until no longer pink inside.\nOR\nPlace the frozen chicken in the crockpot and cook on low for 6 to 8 hours (or high for 4-6 hours.)\nI could hardly wait to try my “winner, winner, chicken dinner”…so the next day I put one of my frozen dinners in the crockpot\xa0and made it up for dinner.\xa0Suffice it to say, it was divine.\xa0One of the best-tasting marinated chicken breasts I’ve had. Can’t wait to try all the rest of the dump chicken recipes! You should too!\n\xa0\n'"

tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")

#model="sshleifer/distilbart-cnn-12-6"
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")

# Load the summarization pipeline
summarizer = pipeline("summarization", model = model, tokenizer = tokenizer)


text_length = len(extracted_text)
abstraction_ratio = .2

# Summarize the text
summary = summarizer(extracted_text, max_length=text_length*abstraction_ratio, min_length=30, do_sample=False)

print("Abstracted Summary:\n", summary[0]['summary_text'])
