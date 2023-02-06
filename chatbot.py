from tkinter import *
import tkinter as tk
import numpy as np
import nltk #natural lang tool kit
import string
import random


root=Tk()

def tot():
        
        txt2.delete('1.0', END)
        f=open('dataset.txt', 'r', errors = 'ignore') #opens the corpus
        raw_doc=f.read()
        raw_doc=raw_doc.lower()  #Converts text into lowercase
        nltk.download('punkt')   #Using the Punkt Tokenizer
        nltk.download('wordnet') #Using the WordNet Dictionary
        sent_tokens = nltk.sent_tokenize(raw_doc)  #Converts Doc. to list of Sentences
        word_tokens = nltk.word_tokenize(raw_doc)  #Converts Doc. to list of words

        lemmer = nltk.stem.WordNetLemmatizer()
        #Lemmatization is the process of grouping together the different inflected forms of a word so they can be analyzed as a single item.
        #WordNet is a semantically-oriented dictionary of English included in NLTK

        def LemTokens ( tokens ) :
            return [lemmer.lemmatize (token) for token in tokens]
            
        remove_punct_dict = dict( (ord(punct), None) for punct in string.punctuation) #Python ord() function returns the Unicode code from a given character.
        def LemNormalize(text) :
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting Function
        GREET_INPUTS = ("hello","hi","greetings","sup","what's up","hey")
        GREET_RESPONSES = ["hi","hey","*nods*","hi there","hello","I am glad! You are talking to me"]

        def greet(sentence):
          for word in sentence.split():
            if word.lower() in GREET_INPUTS:
              return random.choice(GREET_RESPONSES)

#Response Generation
        from sklearn.feature_extraction.text import TfidfVectorizer 
        from sklearn.metrics.pairwise import cosine_similarity


        def responses(user_response):
          robo1_response=''
          TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
          Tfidf = TfidfVec.fit_transform(sent_tokens)
          vals = cosine_similarity(Tfidf[-1],Tfidf)
          idx = vals.argsort()[0][-2]
          flat = vals.flatten()  #function is used as a 1Dimensional iterator over N-dimensional arrays
          flat.sort()
          req_tfidf = flat[-2] 
          if(req_tfidf==0):
            robo1_response = robo1_response+"I am sorry! I don't understand you"
            return robo1_response
          else:
            robo1_response = robo1_response + sent_tokens[idx]
            return robo1_response


        flag = True
        print("BOT: My name is Stark. Let's have a conversation! Also, if you want to exit anytime, just type Bye!")
        while(flag==True):
          user_response = txt1.get("1.0",'end-1c')
          user_response = user_response.lower()
          if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you'):
              flag = False
              print("BOT: You are welcome..")
            else:
              if(greet(user_response)!=None):
                print("BOT: "+greet(user_response))
                txt2.insert("1.0", greet(user_response))
                flag = False
              else:
                sent_tokens.append(user_response)
                word_tokens = word_tokens + nltk.word_tokenize(user_response)
                final_words = list(set(word_tokens))
                print("BOT: ",end="")
                Bot = responses(user_response)
                txt2.insert("1.0", Bot)
                #print(Bot)
                #print(responses(user_response))
                sent_tokens.remove(user_response)
                flag = False
          else:
            flag = False
            print("BOT: Goodbye! Take care ｡^‿^｡ ")
        

root.geometry("600x600+0+0") 
root.title("ChatBot")
root.configure(background='#074480')
bg_color = '#074480'
title=Label(root, text="Welcome to our ChatBot",bd=12,fg="gold",bg=bg_color,font=("times new roman",30,"bold"),pady=1).pack(fill=X)

F1=LabelFrame(root,text="Question:",bd=2,relief=GROOVE,fg="gold",font=("times new roman",16,"bold"),bg=bg_color)
F1.place(x=0,y=110,relwidth=1,height=380)
txt1=Text(F1,width=50, height=2,font=("times new roman",16,"bold"),bd=5,relief=SUNKEN)
txt1.grid(row=0,column=0,padx=10,pady=10)

F2=LabelFrame(root,text="Answer:",bd=2,relief=GROOVE,fg="gold",font=("times new roman",16,"bold"),bg=bg_color)
F2.place(x=0,y=200,relwidth=1,height=380)
txt2=Text(F2,width=50,height=13,font=("times new roman",16,"bold"),bd=5,relief=SUNKEN)
txt2.grid(row=0,column=2,padx=10,pady=10)
         
F3=LabelFrame(root,text="Result",bd=2,relief=GROOVE,fg="gold",font=("times new roman",16,"bold"),bg=bg_color)
F3.place(x=0,y=500,relwidth=1,relheight=1)
TT1=Button(F3,text="Submit",font=("times new roman",16,"bold"),bg="white",fg="grey",command=tot).place(x=245,y=10)


root.mainloop()

