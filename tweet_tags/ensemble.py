from __future__ import division
import numpy as np
from scipy.sparse import vstack
 
# found here https://gist.github.com/tristanwietsma/5486024/

class Ensemble1:
 
    def __init__(self, training_set):
        #(these are x , y pairs, where x is a matrix)
        # y is a vector
        self.training_set = training_set
        self.N = self.training_set[0].shape[0]
        self.weights = np.ones(self.N)/self.N
        self.RULES = []
        self.ALPHA = []
        self.train_x = training_set[0]
        self.train_y = training_set[1]
 
    def set_rule(self, clf, test=False):
        errors = []

        for i in range(len(self.train_y)):
            pred = clf.predict(self.train_x[i])
            errors.append(pred[0]!=self.train_y[i])

        errors = np.array(errors)
        e = sum(errors*self.weights)
        print e

        if e > 0.5:
            print 'This is not a weak learner. Build something better!!'
            return -1;

        if test: return e
        alpha = 0.5 * np.log((1-e)/e)
        print 'e=%.2f a=%.2f'%(e, alpha)
        w = np.zeros(self.N)
        for i in range(self.N):
            if errors[i] == 1: w[i] = self.weights[i] * np.exp(alpha)
            else: w[i] = self.weights[i] * np.exp(-alpha)
        self.weights = w / w.sum()

        self.RULES.append(clf)
        self.ALPHA.append(alpha)
 
    def evaluate(self,test= None):
        # test is xy pairs

        if(test == None):
            test = self.train_x
            true_y_list = self.train_y

        NR = len(self.RULES)
        print NR
        for i in range(test.shape[0]):
            x = test[i]
            true_y = true_y_list[i]

            hx = [self.ALPHA[t]*self.RULES[t].predict(x)[0] for t in range(NR)]

            print 'Element ', i,'of the test set'
            print 'True vs Predicted:- ',true_y,' ', np.sign(sum(hx))

    def predict(self,points):

        pred = []
        for point in points:
            hypothesis = 0.0
            for t in range(len(self.RULES)):
                weak_prediction = self.RULES[t].predict(point)
                hypothesis += self.ALPHA[t]*weak_prediction[0]

            pred.append(np.sign(hypothesis))

        return pred

class AdaBoost:

    def __init__(self, training_set,iterations):
        #(these are x , y pairs, where x is a matrix)
        # y is a vector
        self.training_set = training_set
        self.N = self.training_set[0].shape[0]
        self.weights = np.ones(self.N)/self.N
        self.RULES = []
        self.ALPHA = []
        self.train_x = training_set[0]
        self.train_y = training_set[1]
        self.iterations = iterations

    def make_strong_learner(self, clf):
        print self.iterations
        for t in range(self.iterations):
            print t
            for c in clf:
                c.fit(self.train_x, self.train_y)

            (h_weak,e,errors) = self.find_best_classifier(clf)
            if e == 0:
                break
            alpha = 0.5 * np.log((1-e)/e)
            print 'e=%.2f a=%.2f'%(e, alpha)

            w = np.zeros(self.N)
            
            for i in range(self.N):
                if errors[i] == 1: w[i] = self.weights[i] * np.exp(alpha)
                else: w[i] = self.weights[i] * np.exp(-alpha)
            
            self.weights = w / w.sum()
            self.RULES.append(h_weak)
            self.ALPHA.append(alpha)
            self.update_training_set()

        print 'worked'

    def find_best_classifier(self, clf):
        best_class = clf[0]
        best_error_rate ,errors_best_class = self.error_rate(clf[0])
        for c in clf:
            error_rate_clf, errors = self.error_rate(c)

            if( error_rate_clf < best_error_rate):
                best_class = c
                errors_best_class = errors 
                best_error_rate = error_rate_clf

        return (best_class, best_error_rate, errors_best_class)



    def find_worst_classifier(self, clf):
        min_diff = 1;
        worst_class = None
        errors_worst_class = None
        for c in clf:
            error_rate_clf, errors = self.error_rate(c)

            if( abs(error_rate_clf - 0.5) < min_diff):
                min_diff= abs(error_rate_clf - 0.5)
                worst_class = c
                errors_worst_class = errors 

        return (worst_class,min_diff,errors_worst_class)


    def error_rate(self,clf):
        errors =[]

        for i in range(len(self.train_y)):
            pred = clf.predict(self.train_x[i])
            errors.append(pred[0]!=self.train_y[i])

        errors = np.array(errors)
        
        return sum(errors*self.weights), errors



    def update_training_set(self):
        m = self.N
        weighted_training_set = None
        counts = np.random.multinomial(m,self.weights)
        weighted_training_set_y = []
        
        for i in range(len(counts)):
            count = counts[i]
            duplicated = self.duplicate_sparse_column(self.train_x[i], count)
            
            if weighted_training_set == None:
                weighted_training_set = duplicated
            elif count != 0:
                weighted_training_set = vstack([weighted_training_set, duplicated])

            weighted_training_set_y += [self.train_y[i]]*count


        self.training_set = (weighted_training_set.tocsc(), weighted_training_set_y)
        self.train_x = self.training_set[0]
        self.train_y = self.training_set[1]

        print type(self.train_x)
        print type(self.train_y)



    def duplicate_sparse_column(self, column, count):
        ret = None
        for i in range(count):
            if ret == None: 
                ret = column
            else: 
                ret = vstack([ret, column])
        return ret

    def predict(self,points):

        pred = []
        for point in points:
            hypothesis = 0.0
            for t in range(len(self.RULES)):
                weak_prediction = self.RULES[t].predict(point)
                hypothesis += self.ALPHA[t]*weak_prediction[0]

            pred.append(np.sign(hypothesis))

        return pred

        
# if __name__ == '__main__':
 
#     examples = []
#     examples.append(((1,  2  ), 1))
#     examples.append(((1,  4  ), 1))
#     examples.append(((2.5,5.5), 1))
#     examples.append(((3.5,6.5), 1))
#     examples.append(((4,  5.4), 1))
#     examples.append(((2,  1  ),-1))
#     examples.append(((2,  4  ),-1))
#     examples.append(((3.5,3.5),-1))
#     examples.append(((5,  2  ),-1))
#     examples.append(((5,  5.5),-1))

#     for i in examples:
#         print i[0]
 
#     m = AdaBoost(examples)
#     m.set_rule(lambda x: 2*(x[0] < 1.5)-1)
#     m.set_rule(lambda x: 2*(x[0] < 4.5)-1)
#     m.set_rule(lambda x: 2*(x[1] > 5)-1)
#     m.evaluate()