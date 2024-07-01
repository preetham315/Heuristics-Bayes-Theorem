## Raichu

### Problem Statement
The Board game consists of three pieces. Pichu, Pickachu and Raichu.

Pichu: Pichu’s possible moves are that it can move diagonally one square forward only if that square is empty. Pichu can also jump over another pichu but it has to be of opposite color. The piece that was jumped over will be removed from the board.

Pikachu: Pikachu’s possible moves are that it can move 1 or 2 squares forward or left or right only if it’s a empty square. A pikachu can also jump over a pichu or a pikachu as long as it is of opposite color and it can move 2 or 3 squares in this case . Also there are some constraints to this. First of all the squares between the pikachu’s start position and jumped piece should be empty and also all the squares between the jumped piece and ending position should also be empty.

Raichu: First of all Raichu is created when a pichu or pikachu reached the opposite side of the board. Raichu’s possible moves are that it can move any number of squares which are forward, backward,left,right, and also diagonal to an empty square as long as all the squares in between are empty. A raichu can also jump over a pichu, pikachu or raichu as long as they are of opposite color and can land on any number of squares as long as the squres between the jumped square and the landing square are empty.

In this game the winner is the one who captures all of the pieces of other player. We have to write a code that plays raichu well.

### State Space
The state space here is the set of all possible places pichu, pikachu and raichu will be on the board which includes black and white both. 

### Initial State
The initial state is the state of the board in which there are pichus and pikachus of white and black on both sides in equal numbers.

### Successor Function
We written successor function for pichu, Pickachu and also Raichu.

Since pichu can only move diagonally we have written a successor function which returns all the possible moves. Similarly in the case of pikachu since it can only move forward, left or right we have written a successor function with those constraints and returned all the possible moves. In the case of Raichu, as it can basically move in all directions we wrote a successor function which also considers some constraints like if the square is empty or not and also since it can  jump over pichu, pikachu and also raichu we considered those while building our successor function and then returned all the possible moves for raichu.

### Heuristic

We have come up with two heauristics for this problem. Both return the counts for where as in the first we are giving the weights for the respective move based on the moves of the pices. second one is simple count. for which we were getting 1.77 as the value at the end

# Goal State
The Goal state is a state in which a player captures all the pieces of the other player.

# Reference 

* [Ref-1](https://stackoverflow.com/questions/33644353/better-heuristic-function-for-a-game-ai-minimax)
* [Ref-2](https://github.com/njmarko/alpha-beta-pruning-minmax-checkers)

## Truth be Told

### Problem Statement: 
Many practical problems involve classifying textual objects — documents, emails, sentences, tweets, etc. —into two specific categories —spam vs nonspam, important vs unimportant, acceptable vs inappropriate, etc. Naive Bayes classifiers are often used for such problems. They often use a bag-of-words model, which means that each object is represented as just an unordered “bag” of words, with no information about the grammatical structure or order of words in the document. Using this clasifier we need to classify reviews into faked or legitimate, for 20 hotels in Chicago from the given data sets

### Approach: 

Initially we cleaned the text in the given data set using string translate, regex functions and sets. to get only the text and remove the charecters and any other unuseful information. Then from nltk we used the corpus english words to get the stop words. We've also tried to give teh stop words manually which didn't improve the accuracy that much. Then we tried doing the lemmatization to get the base root word with out loosing any information even this didn't improve the accuracy that much. But at this point we've considered the stop words from nltk and went further.

Once the text is clear then we moved to calculating the posterior probabilities for two classes truthful and deceptive. In this process first we calculated the prior probabilies for the classes that is deceptive/total length and likewise for truthful. So step 1 is done. Now we move to step 2: where we calculated the likehood probabilities for the words given classes using the dictionaries. For example P(poor/ truthful) is calculated based on occurences of poor in truth divided by number of words in truthful here to avaoid the case of no word poor we did smoothing by adding a positive value of 1 in numerator and denomenator. and finally mutiplied this with priors of respectives class. In the latest try updated the formula by considering the prior probability in the denominator as well which helped in increasing the accuaracy of the model.


Lastly we compare this values of posterior of truth with posterior of false based on this we will be appending the label to test data.

Finally got at accuracy of 81.50%

### References

* [REf-1](https://jaimin-ml2001.medium.com/stemming-lemmatization-stopwords-and-n-grams-in-nlp-96f8e8b6aa6f)
* [REf-2](https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/)
* [REf-3](https://medium.com/@rangavamsi5/na%C3%AFve-bayes-algorithm-implementation-from-scratch-in-python-7b2cc39268b9)
* [REf-4](https://leasetruk.medium.com/naive-bayes-classifier-with-examples-7b541f9ffedf)
* [REf-5](https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/)


