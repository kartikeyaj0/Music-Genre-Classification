import glob
import math
import os
import numpy as np
import scipy
import sklearn.linear_model as lm
from sklearn.metrics import confusion_matrix
from matplotlib import pylab
from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
def read_ceps(genre_list, base_dir = '/media/kj/New Volume/opihi.cs.uvic.ca/sound/genres/ceps/training'):
	X = []
	y = []
	for label, genre in enumerate(genre_list):
		genre_dir = os.path.join(base_dir, genre, "*.ceps.npy")
		file_list = glob.glob(genre_dir)
		
		for fn in file_list:
			ceps_features = scipy.load(fn)
			num_ceps = len(ceps_features)
			X.append(np.mean(ceps_features[int(num_ceps*0.1):int(num_ceps*0.9)], axis=0))
			y.append(label)
	return np.array(X), np.array(y)

genre_list = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "rock"]
train_dataset,train_labels = read_ceps(genre_list)
test_dataset, test_labels = read_ceps(genre_list, '/media/kj/New Volume/opihi.cs.uvic.ca/sound/genres/ceps/testing')

def randomize(dataset, labels):
	permutation = np.random.permutation(labels.shape[0])
	shuffled_dataset = dataset[permutation,:]
	shuffled_labels = labels[permutation]
	return shuffled_dataset, shuffled_labels

# To randomize
train_dataset, train_labels = randomize(train_dataset, train_labels)
test_dataset, test_labels = randomize(test_dataset, test_labels)
count1 = 0
count2 = 0
for a in train_dataset:
	count1 = count1 + 1
	for b in a:
		count2 = count2 + 1
		if math.isnan(b):
			print 'swell', count1,count2
clff = OneVsRestClassifier(LinearSVC(random_state=0)).fit(train_dataset, train_labels)
z1 = clff.predict(test_dataset)
a = 0.0
b = 0.0
for x in (z1==test_labels):
    if(x):
        a = a + 1
    b = b + 1
print(a/b)

cm = confusion_matrix(test_labels, z1)
print(cm)

def plot_confusion_matrix(cm, genre_list):
	pylab.clf()
	cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	print('Normalized confusion matrix')
	print(cm_normalized)
	pylab.matshow(cm_normalized, fignum=False, cmap='Blues',
	vmin=0, vmax=1)
	ax = pylab.axes()
	ax.set_xticks(range(len(genre_list)))
	ax.set_xticklabels(genre_list)
	ax.xaxis.set_ticks_position("bottom")
	ax.set_yticks(range(len(genre_list)))
	ax.set_yticklabels(genre_list)
	# pylab.title(title)
	pylab.colorbar()
	pylab.grid(False)
	pylab.xlabel('Predicted class')
	pylab.ylabel('True class')
	pylab.grid(False)
	pylab.show()


plot_confusion_matrix(cm, genre_list)
