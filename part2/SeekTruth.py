
import sys
import math
import string
import nltk
import re
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

def pre_processing(input):
    stopwords = nltk.corpus.stopwords.words('english')
    #table = str.maketrans(dict.fromkeys(string.punctuation))
    #input = input.translate(table)
    input = re.sub('[^a-zA-Z\s]+', '', input)
    input = re.sub(' +', ' ', input)
    input = input.lower()
    input = input.split()
    input=[word for word in input if not word in stopwords] 
    input = [wordnet_lemmatizer.lemmatize(word) for word in input]           
    input = ' '.join(input)
    return input


def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(pre_processing(parsed[1]) if len(parsed)>1 else "")
        #print ("objects:", objects)
        #print("\n---------------")
        #print("labels:",labels)

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

def prior_prob(data):
    prior_dict={}
    prior_prob_dict= {}
    for i in data["labels"]:
        if i in prior_dict:
            prior_dict[i] +=1
        else:
            prior_dict[i] =1
    total_feedback= len(data["labels"])
    for i in prior_dict:
        prior_prob_dict[i] = prior_dict[i]/total_feedback

    return prior_prob_dict

def total_words(data):
    words={}
    for i in data["objects"]:
        if i in words:
            words[i]+=1
        else:
            words[i]=1
    #{k: v for k, v in sorted(words.items(), key=lambda item: item[1])}
    #print(words)
    return words

def wordOccurance_labels (data):
    decptive_dict= {}
    truthful_dict ={}
    truthful_words=0
    decptive_words=0
    for i in range(len(data["labels"])):
        
        if data["labels"][i]=="deceptive":
        
            for j in data["objects"][i].split():
                if j in decptive_dict:
                    decptive_dict[j]+=1
                else:
                    decptive_dict[j]=1
        else:
            for s in data["objects"][i].split():
                if s in truthful_dict:
                    truthful_dict[s] +=1
                else:
                    truthful_dict[s] =1
    for i in decptive_dict:
        decptive_words += decptive_dict[i]
    for i in truthful_dict:
        truthful_words += truthful_dict[i]
    #print (decptive_dict)
    

    return decptive_dict,truthful_dict,decptive_words, truthful_words 

def prior_2(decptive_dict,truthful_dict,deceptive_words,truthful_words):
    total_single_words= deceptive_words+truthful_words
    total_respective_dict = {}
    for i in decptive_dict:
        respective_word = decptive_dict[i]
        if i in truthful_dict:
            respective_word= respective_word+ truthful_dict[i]
        total_respective_dict[i]= respective_word/total_single_words
        
    for i in truthful_dict:
        if i not in total_respective_dict:
            respective_word = truthful_dict[i]
            total_respective_dict[i]= respective_word/total_single_words
    return total_respective_dict





#
def classifier(train_data, test_data):
    
    prior_probobilities= prior_prob(train_data)
    words_training= total_words(train_data)
    decp_dict, truth_dict, decptive_words,truthful_words= wordOccurance_labels(train_data)
    #print("asdas",decp_dict,truth_dict)
    total_respective_dict = prior_2(decp_dict,truth_dict,decptive_words,truthful_words)


    for i in range(len(test_data["objects"])):
        posterior_truth_prob= 1
        posterior_decptive_prob=1
        for j in test_data["objects"][i].split():
            if j in truth_dict and truth_dict[j] >0:
                posterior_truth_prob += (((truth_dict[j]+1)/(truthful_words+1))*prior_probobilities["truthful"])/ total_respective_dict[j]
            else:
                posterior_truth_prob += (1/(truthful_words+1))*prior_probobilities["truthful"]
            if j in decp_dict and decp_dict[j]>0:
                posterior_decptive_prob += (((decp_dict[j]+1)/(decptive_words+1))*prior_probobilities["deceptive"])/ total_respective_dict[j]
            else:
                posterior_decptive_prob += (1/(decptive_words+1))*prior_probobilities["deceptive"]
        if posterior_truth_prob> posterior_decptive_prob:
            test_data["labels"].append("truthful")
        else:
            test_data["labels"].append("deceptive")

    return test_data["labels"]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    #train_data["objects"] = pre_processing(train_data["objects"])
    test_data = load_file(test_file)
    #test_data["objects"] = pre_processing(test_data["objects"])
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"],"labels":[], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
