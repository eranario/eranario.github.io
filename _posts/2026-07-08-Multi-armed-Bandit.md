---
title: "Evaluation vs instruction: learnings around action values"
layout: single
categories:
  - Notes
mathjax: true
---

Author: Earl Ranario

<!--more-->

**Note**: information is derived from Sutton's and Barto's Reinforcement Learning (An Introduction second edition)

## Motivation of learning

This is my first set of notes so I would like to remind myself that AI models are in the path of superintelligence, something very new. But, I think we should try to at least, first achieve individual human ability to accomplish tasks and imitate it.

This is a very fresh thought I have and coming from someone who is not entirely bright on the subject matter of artificial general intelligence. But, I do have experience with applying machine learning models to out-of-distribution domains. And I noticed, they tend to fail most of the time unless instructed with refined data points (i.e. ground-truth labeled data). Even with that constraint, there is a limitation of data points to evaluate with. So, we are stuck in between trying to instruct our models and evaluate its performance to what would be considered "gold standard". And this standard is heavily biased on specific domains of interest such as driving, agriculture or medicine. I do believe AI foundation models are capable to do what was considered impossible, but at some point, we may become data bounded in the future if we don't focus on current limitations of these models.

With that in mind, I am quite curious if we can create a generalizable model that is "adaptable" in real time. Just like humans, we are not experts at everything. We all have our strengths and weaknesses and pursue something that is typically achievable within our constraints of the world. This claim motivates me to find out if:

1. A model is able to complete actions to achieve a goal through adaptation by human demonstration and
2. Can be kept within a hardware constrained setting with small number of parameters
3. And can we keep models interpretable while mapping outputs to understanding

This law of scaling of current AI models states that larger models will always perform better - maybe can hold more memory (this blog post explains it nicely: https://lilianweng.github.io/posts/2026-06-24-scaling-laws/)? This concept of memory and parameter size is not needed for this motivation as I hope to restrain myself from relying on expensive hardware and large models. Generalizability does not mean *"lets build a big model to hold as much information as possible"*. But rather, *"lets build an adaptable system that can achieve what is intended"*. And afterwards, there is always hope of combining these models to interact with each other, similar to current research with agentic systems.

As I continue to learn, I am sure these thoughts will eventually change and my claims will become more refined.

## The idea of evaluation is similar to how we learn
Sutton distinguishes that "evaluative feedback depends entirely on the action taken, whereas instructive feedback is independent of the action taken.". He further clarifies that instruction is most similar to a supervised type of learning. Evaluative feedback indicates how good the action taken was, but not whether it was the best or the worst action possible.

We focus on a particular non-associative setting inspired by the k-armed bandit problem. This setting that we will discuss follows a stationary probability distribution of outcomes. This means that during an episode, the possible outcomes of a scenario will not change. We do not know the exact action values but, since we made the dataset, we do know the distribution it should follow. In real world scenarios, this prior knowledge of a specific task to solve may be unknown and the agent still tries to learn this distribution.

There are many methods mentioned in Sutton's book to solve this stationary problem but we will stick to a simple sample-average for estimating action values. 

$$
Q(a) \leftarrow Q(a) + \frac{1}{N(a)}\left[R - Q(a)\right]
$$

Where:
  - $Q(a)$ - current estimate $a$
  - $N(a)$ - number of times action $a$ has been taken
  - $R$ - reward received after taking action $a$

## Dataset creation
This static dataset contains multiple 2x2 grids of colors red, green, blue and white. Each samples comes in pairs: a before and after translation. The goal here is for an agent to determine the action-values of each translation action which is either flip (across a vertical) and a rotate (90 degree rotation). Why a grid? I've always been attracted to the ARC competition. Though this is a very simple dataset with two possible actions, it's a good stepping stone to understand the chapter more.

The dataset is split to highly favor rotational actions (around 80/20). If I am understanding this correctly, the action values after this simulation should follow a similar distribution favoring rotation over flipping.

![dataset_example](/assets/multi_armed_bandit/dataset_view.png)

## Experiments with the reward value
The reward function provided in the book for its k-bandit algorithm used an "artificial" reward function. It essentially was just noise included the expected action values. The first reward function I considered was an accuracy metric. 

 ```python
def get_reward(x, y, strict_reward):
    # will show after
    else:
        correct_matches = sum(1 for x, y in zip(x, y) if x == y)
        accuracy = correct_matches / len(x)
    return accuracy
  ```

Of the available grid sections, how many equal the ground-truth (expected) translation? Here is a graph showing the action values over time for 100 grid samples:

![non_strict_reward](/assets/multi_armed_bandit/q_history_non-strict.png)

Notice that the values hover around 0.9 (rotate) and 0.7 (flip). This setup does recognize, possibly, the rotation is the more desirable action in this setting. But not significant compared to I expect (around an 80/20 split). It must be that the reward function is not punishing the agent enough so it is not converging to the expected distribution of action values. Again, I only notice this because I created the dataset and this could be a challenge in future experiments: finding the correct reward function?

So, I implemented a stricter reward function where reward is 0 if it does not equal the translate grid otherwise the reward if 1. With this approach, I got the following grid:

![strict_reward](/assets/multi_armed_bandit/q_history_strict.png)

Great! This time, I got something closer to what I expected. Again, not perfect but having a clear understanding on what the reward should be greatly impacts the following action values. Here is what I used:

```python
def get_reward(x, y, strict_reward):
    if strict_reward:
        accuracy = 1.0 if np.array_equal(x, y) else 0.0
    else:
        correct_matches = sum(1 for x, y in zip(x, y) if x == y)
        accuracy = correct_matches / len(x)
    return accuracy
```

## Making a more complex dataset

I decided to include more possible actions such as: rotate 90, rotate 180, rotate 270, flip horizontal, flip vertical, and flip diagonal. Each action is distributed in the dataset respectively: 45%, 20%, 15%, 10%, 5% and 5%. Here is sample of the dataset:

![dataset_difficult](/assets/multi_armed_bandit/dataset_view_difficult.png)

I ran the same experiment and found that the action values never really converge to the true distribution but order is still maintained. Meaning, for a stationary setting, relative values for each action is retained correctly.

![results_difficult](/assets/multi_armed_bandit/q_history_difficult.png)

## Conclusion

In conclusion, having a strict reward allows the values to converge closer to the true distribution of actions. This must mean that if there were more variance in the reward function, it would take more exploration needed for it to converge correctly. For most cases, it is usually non-stationary cases when exploration and exploitation would matter more. Future notes will include these cases and more complex problems.
