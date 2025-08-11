# Understanding Class Imbalance in Machine Learning

## What is Class Imbalance?

Class imbalance is a common problem in classification tasks where the number of observations per class is not equally distributed. In other words, one class (the *majority class*) has a lot more examples in the training data than the other classes (the *minority classes*).

This is very common in real-world scenarios like:
- Fraud detection (most transactions are not fraudulent)
- Medical diagnosis (most patients don't have the rare disease)
- Customer conversion (most visitors to a website don't make a purchase)

---

## An Example: The Shopping Dataset

Our shopping project is a perfect example. The goal is to predict whether a user will make a purchase (`Revenue` = TRUE).

- **Majority Class:** Users who **do not** make a purchase (`Revenue` = FALSE).
- **Minority Class:** Users who **do** make a purchase (`Revenue` = TRUE).

In a typical e-commerce dataset, the number of non-purchasers might vastly outnumber purchasers by a ratio of 10-to-1 or even more.

---

## How Does it Affect Models?

When a model is trained on an imbalanced dataset, it can become a "lazy" learner. Since it can achieve high accuracy by simply predicting the majority class every time, it often fails to learn the patterns that identify the minority class.

This leads to a misleading situation:
- **High Accuracy:** A model that always predicts "No Purchase" might be 85-90% accurate.
- **Useless Predictions:** This model is useless for our goal of finding potential buyers.

This is why **accuracy** is a poor metric for imbalanced datasets. We use **Sensitivity** and **Specificity** instead:
- **Sensitivity (True Positive Rate):** How well the model identifies the minority class (e.g., purchasers).
- **Specificity (True Negative Rate):** How well the model identifies the majority class (e.g., non-purchasers).

A good model needs to perform well on *both* metrics, not just one.

---

## Impact on k-Nearest Neighbors (k-NN)

The k-NN algorithm is particularly sensitive to class imbalance, especially as you change the number of neighbors (`k`).

k-NN works by taking a "vote" from the `k` data points closest to the new observation.

- **When `k` is small (e.g., k=1):** The model is very "local." It only looks at the single closest neighbor. It has a chance of correctly identifying a minority class member if it's in a small pocket of other minority members.
- **When `k` is large (e.g., k=11):** The model polls a larger group of neighbors. In an imbalanced dataset, the neighbors are overwhelmingly likely to be from the majority class. The majority class will almost always win the vote.

As you observed:
- Increasing `k` **improves specificity** (the model gets even better at predicting the already-common negative case).
- Increasing `k` **destroys sensitivity** (the model loses its ability to find the rare positive cases, as they are always outvoted).

---

## Common Solutions

Dealing with class imbalance is a major field of study in machine learning. Thankfully, there are several common techniques to address it:

1.  **Resampling Techniques:**
    *   **Oversampling:** Create copies of the minority class examples to balance the dataset.
    *   **Undersampling:** Remove some of the majority class examples to balance the dataset.
2.  **Algorithmic Approaches:** Use more advanced algorithms that can handle imbalance internally (e.g., by putting a higher penalty on misclassifying the minority class).
3.  **Collect More Data:** If possible, collecting more data, especially for the minority class, is often the best solution.

---

## A Closer Look at Resampling Techniques

Let's dive a little deeper into the most common approach: **Resampling**. The goal is to create a new, balanced version of your training dataset before training the model.

### Undersampling

This technique reduces the number of examples in the majority class.

*   **How it works:** If you have 8,500 "No Purchase" examples and 1,500 "Purchase" examples, you would randomly remove 7,000 of the "No Purchase" examples. You'd be left with a balanced 1,500 vs. 1,500 dataset to train your model on.
*   **Pros:** Can significantly speed up model training time because the dataset becomes much smaller.
*   **Cons:** You might be throwing away valuable information. Some of those majority class examples you removed could have been important for defining the boundary between the two classes.

### Oversampling

This technique increases the number of examples in the minority class.

*   **How it works (The Naive Way):** Simply duplicate random examples from the minority class. If you have 1,500 "Purchase" examples, you would randomly copy them until you have 8,500, matching the "No Purchase" class.
*   **Pros:** No information is lost from the majority class.
*   **Cons:** The model can become **overfitted**. It learns to be very good at predicting the specific minority examples it has seen before, but it may not generalize well to new, unseen minority examples because it hasn't learned broader patterns.

#### A Smarter Oversampling: SMOTE

A more advanced and popular method is **SMOTE** (Synthetic Minority Over-sampling Technique).

*   **How it works:** Instead of just making exact copies, SMOTE cleverly creates *new, synthetic* data points. It looks at a minority class example, finds its nearest neighbors that are also in the minority class, and then creates a new data point somewhere along the line connecting them.
*   **Why it's better:** This gives the model more varied minority examples to learn from, leading to better generalization and reducing the risk of overfitting compared to simple oversampling.