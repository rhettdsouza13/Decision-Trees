# Decision-Trees
This is the basic implementation of ID3 (decision tree classification) with pruning, from the ground up.

To train the decision tree:
```python
ID3(examples, default)
#This returns the node object of the root of the tree.
```
To evaluate a particular example with a built tree:
```python
evaluate(tree_root, example)
#This returns the class label evaluated.
```
To test an entire set of examples:
```python
test(tree_root,examples)
#This returns the accuracy on the set of examples.
```
To prune a trained tree:
```python
prune(tree_root, validation_set)
#This will make changes to the tree itself. Doesn't return anything.
```

Feel free to make use of the unit tests which are in unit_tests.py to play around and understand the implementation and the algorithm better.
Also, feel free to use your own dataset. However, make sure to represent missing values as '?', and represent your target label with a column (dictionary key) as 'Class'.


Experimentation was performend on the house_votes dataset (available in house_votes_84.csv).
The testing accuracy was plotted for cases with pruning and without pruning, for various sizes of the training set.

![alt_text](https://github.com/rhettdsouza13/Decision-Trees/blob/master/plots/Figure_1.png)
