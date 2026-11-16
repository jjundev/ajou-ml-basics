# Discrete Dynamical Systems - Eigenvalues and Eigenvectors 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=7SfocUa8gis (약 26:15)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 3개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, I'm Luis Serrano and this is Serrano Academy and DeepLearning.AI. In today's video, we're going to learn about discrete dynamical systems and their relations with matrices, linear transformations, eigenvalues, and eigenvectors. If any of these words don't sound familiar, don't worry, we're going to learn everything from scratch.

And this is a sampler of a series of courses I have with DeepLearning.AI, which I'll tell you more later in the video. So let's get started with dynamical systems. My favorite dynamical system is a very simple one which models the weather.

And in this system, we have two possible things that can happen. In a given day, it can be sunny, or it can be rainy. And let's say the whole day is sunny and the whole day is rainy to really simplify this.

Now, as I go, I encourage you to imagine how this would be if we had 100 or 200 types of weather. The methods are the same, but the math obviously gets more complicated. Now, here is the thing.

Let's say today is sunny, then it's likely that tomorrow is going to be sunny, but it could also rain. And if today is rainy, then it's likely that tomorrow will be rainy, but it could also switch to sunny. So what are these probabilities?

Well, if today is sunny, the probability that tomorrow is sunny is 80%, which is high, and the remaining 20% is that it switches to rainy. And if it's rainy, the probability that tomorrow is rainy is 70%, and the remaining 30 is that it will turn into sunny.

So that's our dynamical system, and it's described by this matrix over here called the transition matrix, which has the four probabilities: that it goes from sunny to sunny, from sunny to rainy, from rainy to sunny, and from rainy to rainy. In this case, these are the numbers: .8, .3, .2, and .7.

Notice that in this matrix, every column adds to 1 because it's the probability that you go from today's state to all the possible states tomorrow. If you had a 100 by 100 matrix, then every column would still add to 1.

Now, here's a question: what is the probability, if we don't know what happened yesterday, that today is sunny or rainy? That's what happens in a random day if we don't know what happened previously. Well, it turns out that answering this question will give us a lot of information about this dynamical system relating to eigenvalues and similar things.

So let's estimate what this probability could be. Let's say that today was sunny, and today is day 0. That means the probability that today is sunny is 1, and the probability that is rainy is 0, because we stuck our head out of the window and looked at the weather and we realized it was sunny.

And what happens tomorrow, the first day? Well, remember that this was the transition matrix, the matrix of probabilities. And as we do operations here, we're going to do operations in the matrix, and they're going to be the same operations.

So, if today is sunny, the probability that tomorrow is sunny is 80%, and the probability tomorrow is raining is 20%. That's the same as multiplying that matrix by the vector of today, which is 1, 0, and then we get .8, .2.

If you don't know how to multiply matrix, let me tell you very quickly. How do you get this .8? Well, is the product of this .8 times 1, and then you go to the right in the rows in the first matrix and down in the columns in the second matrix, which is the vector, so you multiply .8 times 1 and you add it to .3 times 0, and you get .8.

And for the second number, then you do the same thing but with the second row, so you take .2 times 1 and add it to .7 times 0, so you get .2. But the interesting thing is that what happens there happens here.

So let's do one more day. Let's see what happens on the second day. Well, if it's sunny, then the probability that tomorrow is sunny is .8 and rainy is .2. And if it's rainy, the probabilities are .3 and .7.

So now what we need to do is multiply the numbers going down a path. So what's the probability that we get sunny, sunny, sunny? Then that's .8 times .8, which is .64.

The probability that we get sunny, sunny, rainy is .8 times .2, which is .16. The probability that we get sunny, rainy, sunny is .2 times .3, which is .06, quite small. And finally, the probability that we get sunny, rainy, rainy is .2 times .7, which is .14.

Now we have two sunnies and two rainies, so we're going to add the sunnies. We get .64 plus .06, which is .7. These are disjoint, so we'll have to add them.

And for rainy, we get .16 plus .14, which is .3. Verify that those two add to 1, we're still good. And that's going to be our vector of probabilities for the second day, which happens to be the same thing as multiplying the transition matrix times the vector of probabilities for the first day.

Now let's do day 3, and there's a lot of arrows here, so I'm just going to be a little lazy and only do the matrix multiplication, but I encourage you to work it out in this tree over here. For the third day, we multiply the transition matrix times the vector of probabilities of the second day to get .65, .35.

Notice that every day it's a little less likely that sunny and a little more likely that rainy because that first sunny day has less and less and less influence. Right? If it's sunny today, it has a lot of influence over if it's sunny tomorrow, but if it's sunny today, it doesn't have so much influence over if it's sunny in a month from now.

And we can continue doing this, and let's say in the nth day, for a lot of days, a thousand days or ten thousand days, then we are going to have this matrix times some vector. Now that's too many operations, so let's work out the math a little so that it's simpler.

Look at what I'm going to do with the matrices. I'm going to say that for the first day, it's the matrix raised to the power of 1 times 1, 0, which is the probability vector for day 0. Now for the second day, we're multiplying by that matrix one more time, so therefore we have that original matrix squared times 1, 0.

You see, instead of doing matrix times vector of the first day, I did matrix times matrix times vector of day 0. And I'm going to continue like that, so the third day is the matrix to the 3 times the vector of day 1, and so on, and we get the matrix to the n times the vector of day 1.

And I encourage you to actually do the math and notice that this regulates. If you keep calculating the next vector and the next vector, it starts regulating at .6, .4, starts converging to that.

And we'll see a good reason why later, but for now, let's just say we did this product so many times that we noticed that it stabilized at .6, .4. Which means that on a given day, the probability of sunny is .6 and the probability of rainy is .4.

Now for consistency, let's see what would have happened if today was rainy. I'm going to be a little faster in the math. We do the tree like we did before.

We get .3 and .7. That's for the first day, because for the 0th day, we had probability of sunny equals 0, probability of rainy equals 1. For the next day, we have 30% for sunny, 70% for rainy.

For the next day, we have .45, 45% and .55 for sunny and rainy. Notice that it's growing quickly. For the next day, the numbers are .525 and .475, and so on and so forth.

And if we do this many times, like tens or hundreds of thousands, we're going to notice that it again stabilizes at .6, .4, meaning that the probability of sunny is still .6 and rainy is still .4. And in general, if we don't know what happened on a given day, then the probability of sunny and rainy are p and 1 minus p for some number p, because we don't know what happened today.

And if we continue growing that tree for many, many, many layers, we're going to start noticing that it again stabilizes to .6, .4 for the probabilities of sunny and rainy. What does that mean?

That if we take this matrix and let's say raise it to a big power, to the n, then as n goes to infinity, this matrix actually stabilizes to .6, .6, .4, .4. And that is very special because if I were to multiply this matrix times any vector that has entries that add to 1, so p and 1 minus p, then you can check the math, it gets .6, .4.

So in summary, that's a discrete dynamical system, but I like to see things graphically because I like to see matrices not as arrays of numbers, but as linear transformations. Let me show you.

We're going to plot our points in a two-dimensional plane where the horizontal axis represents sunny and the vertical axis represents rainy, and we have a whole grid. So for the point 1, 0, that's 1 sunny, 0 rainy, then we have this point over here.

Now what happens if I multiply that by the matrix? Well, I get .8, .2, which is this point over here. Now if I do it again, I multiply the matrix, the transition matrix times .8, .2, then I get the vector .7, .3, which is over here.

Notice that we're getting a bit of a line. And if I continue doing that, I continue growing this line, and eventually it converges to the point .6, .4.

In other words, I just draw a line from the point 1, 0 all the way to .6, .4, and I start getting closer and closer and closer and closer to .6, .4, which is the point of equilibrium. Now what happens if I have a rainy day?

Then I start all the way there, up to the left, because I have the point 0, 1, that is 0 sunny, 1 rainy. And if I want to see where the next days appear, then I draw a line all the way to the point of equilibrium, .6, .4, and I start plotting the points.

And the first one is .3, .7, which is pretty much halfway there, right? It's actually halfway. The next point is going to be .45, .55, which is halfway to the point of equilibrium from the point that we started, and so on and so forth.

And in many, many, many days, in infinitely many days, we're going to get to that point of equilibrium, .6, .4, no matter where you start. So anywhere you start in that line is a random day with probability something to be sunny and 1 minus something to be rainy.

No matter what happens, if you continue the next day, the next day, the next day, it's going to walk along this line to reach the point of equilibrium at the limit. Now, just out of curiosity, what happens if I put a point that is not in that line? For example, this point, or this point over here. Will they go...

## Part 02 (10:00–20:00)

to the point of equilibrium? Well, not exactly. There's actually a line of equilibrium, which is this line from 0 0 to the point of equilibrium and goes on forever. 

And those points are going to move towards the line, just like the other two points did. So basically, they move closer and closer and closer to that line, and they converge to a point in that line of equilibrium.

So that pretty much describes the dynamical system. But there are some questions. First of all, why does this happen? Why does it go in a line? And second of all, why halfway?

And to see why these things happen, we're going to study linear transformations because, as I said, I don't like to see matrices as arrays of numbers. I like to see them as beautiful transformations that transform the plane like that one into a plane like this one. 

And in general, this is for 2x2 matrices, but in general, if I have a 100x100 matrix, then that's just going to transform a 100-dimensional space into another 100-dimensional space in a really nice way. So this matrix, the transition matrix, 0.8, 0.3, 0.2, and 0.7, what does it do to the plane on the right? 

Well, let's look at some points. Let's pick four points forming a square, and it's the four points 0 0, 0 1, 1 0, and 1 1. Well, where does the point, for example, 0 0 go? 

Well, that always goes to 0 0 because 0 0 times the matrix is 0 0. So the origin goes to the origin. That always happens.

Now, where does 1 0 go? Well, it goes to 0.8, 0.2 over here because the matrix times 1 0 is 0.8, 0.2. 

The point 0 1 goes to 0.3, 0.7, as we saw before. And the point 1 1 goes to the point 0.9, 1.1.

So basically, this square over here, which we call a basis, becomes this little parallelogram over here, which is another basis. So a transformation is a change of basis. 

And why is it called a basis? Because this little map from the square to this parallelogram actually dictates how the whole linear transformation behaves because, as the square tessellates the plane, then this parallelogram also tessellates the plane. And so basically, the big square goes to this big parallelogram over here. 

So what does this mean? That means if I pick a random point over there, where would it go when you multiply by this matrix? Well, I can look at that thing as a big grid. Then I locate the point in this grid where it would correspond. 

And that is where the matrix takes that green point into this point over here. Now, that is nice, but it's not that nice. Why? 

Well, take a look at this. If I do the transformation once, I went from the square to that parallelogram. That's very pretty and very easy to understand.

However, if I were to do it again, I would have to recalculate everything. That maybe takes it to that other parallelogram. I don't really know what it does. 

And if I want to do it a thousand times, I kind of have to see where this goes a thousand times. I have to describe each one of them. That's not good. 

That's way too much work. I want to be lazy, and I want to do something that makes it very easy for me to say if this is what the transformation did, then this is what it's going to do twice and three times and four times and a thousand times.

So to describe this transformation nicely, we're going to look at eigenvalues and eigenvectors. Now, I'm not going to describe how to find them. You have to solve a little quadratic with the determinant and then solve a couple of linear equations. 

I have a link in the description that shows how to do it, and I also show how to do it in detail in the course with Deep Learning AI. And there are many places where you can find eigenvalues and eigenvectors quickly. My favorite one is Wolfram Alpha. 

So I plug this into Wolfram Alpha, and I get these as eigenvalues and eigenvectors. Let me summarize. The eigenvectors are 0.6, 0.4. What a coincidence. That's exactly the stability vector we had before.

And the other one is 1, -1, which also appears as the direction in which you move towards that line. So it's kind of nice. And the eigenvalues are 1 and 0.5. 

That 0.5 is because we were moving halfway to the point of equilibrium. So all is written here. But I don't want to get ahead of myself. We'll do it step by step. 

What do the eigenvectors and eigenvalues mean? It means the following. First, I'm going to tell you algebraically, which is not that pretty. Then I'm going to tell you geometrically, which is very pretty.

So the matrix times the eigenvector becomes the eigenvector times the eigenvalue. I'm going to be honest with you. First time I saw this type of equation, it said nothing to me. 

So if this says nothing to you yet, don't worry. When we look at it geometrically, it's going to be really nice. And also, that if you take the matrix times the second eigenvector, you get the second eigenvalue times the second eigenvector. 

Now, as we saw, this is the vector for the stable weather. So that means that if I take the weather today, and that was a 60% probability of sun and a 40% probability of rain, then the weather tomorrow is the exact same thing. 

So the stability condition of the dynamical system is actually encoded in this equation. But as I promised, let's look at these things in a nice geometric way. What does this mean?

Well, let's take a look at the first eigenvector, 0.6, 0.4. Where does that go? Well, that goes over here to itself because it's 1 times itself. So it's actually a vector that gets fixed. 

In other words, the arrow points in the exact same direction. That's really what matters, that it points in the same direction. This one actually is nicer because it has the same magnitude, but it doesn't have to normally.

And now, where does the second eigenvector go? Well, that's 1, -1. That goes to 0.5, -0.5. So it's not so nice. 

It doesn't get fixed, but it's still very nice because the direction is the same because the direction of this vector is the same direction of that vector over here. And that's what we're really careful for, the fact that it's the same direction. 

Now, there's a small thing, which is if you have a transition matrix like this one, where the columns add to 1, then one eigenvector is always going to be 1. And that means we have that stability condition. But in general, matrices have eigenvalues and eigenvectors, but they're not necessarily 1. 

So now, what does this say? It says that the basis corresponding of those two vectors, that's this parallelogram over there, goes to this parallelogram over here. Just like before, we have the square going to the parallelogram, except that now we have a parallelogram going to another parallelogram whose sides are parallel, and that's very important. 

So we basically picked a really nice basis that goes to a basis that's very similar, that has parallel sides, even though they could be in different places. And that's a way to describe this matrix. But let's take a look at the two directions. 

These directions actually stay put. And moreover, that parallelogram over there tessellates the entire plane, and so does this parallelogram over here. 

We already did that before with the square going to the parallelogram, but this is much better because, as you can see, what the transformation is doing is taking that big parallelogram over there and basically squishing it by a factor of 1/2 to get this one over here. So it's basically contracting. 

And that can be described if it happens many ways because applying the matrix once takes that basis over there and it squishes it by 1/2. If I were to apply the matrix again, it would squish it by 1/2 one more time. And if I keep applying it, it keeps squishing it and squishing it and squishing it.

So if I do it many, many, many times, this matrix to the power of n, where n is hundreds of thousands, well, it takes that parallelogram over there and turns it into this really, really, really skinny parallelogram that barely covers that red line. 

And then this is much better because it doesn't take me so much work to figure out what the matrix is doing tens or hundreds of thousands of times, which was a problem before. So let me summarize what this matrix does. 

Basically, we have that line of equilibrium, which is the line corresponding to the eigenvector with eigenvalue 1. That's the line with equation y = 0.4 / 0.6 * x. And for any points that are flying around, what this matrix does, if you apply it many, many times, is that it takes the point towards the line in an angle of 45 degrees. 

So it's not perpendicular to the green line. It's in an angle of 45 degrees. Why? Because that second eigenvector is the vector that points down 45 degrees.

So I like to describe dynamical system as these bunch of lines that all point in an angle of 45 degrees towards that equilibrium line. And if I have a bunch of points, then applying the matrix one time is simply going to bring them halfway to the green line. 

Why halfway? Because the second eigenvalue is 0.5. So something special about these matrices is that one eigenvalue is going to be 1, and the other ones are going to be less than 1. 

And therefore, this can happen. So that describes exactly what was happening with the original dynamical system with the sunny and the rainy days. So let's say we have our rainy point, which is 0 1. 

That's our rainy day. And the next day is going to have probabilities that are going to be described by that point taken halfway to the green line. So 0.3, 0.7. Tomorrow, the probabilities are 0.3, 0.7. 

And if I have the day 1 0, which corresponds to today being sunny, then the probabilities for tomorrow are whatever point I get if I take that point halfway towards the equilibrium line, which is 0.8, 0.2. And if I do this many, many, many times, no matter where I start, I end up closer and closer and closer to the equilibrium point, which is 0.6, 0.4.

So that is the description of a dynamical system looked at geometrically. And as you can see, eigenvalues and eigenvectors are very important. 

Now, let me do a bigger example. And for this one, we're only going to look at the matrices. We don't need to look at the diagram, and we actually don't need to look at the three-dimensional description, but I encourage you to imagine what's happening.

## Part 03 (20:00–26:15)

It's still the same thing where you have an equilibrium line and you bring everything towards that equilibrium line. So in a dynamical system we also have weather except we have three types: sunny, cloudy, and rainy. And the probabilities are the following: if today is sunny, then tomorrow can be sunny, cloudy, or rainy with probabilities .8, .15, and .05. It's more likely that it'll be sunny tomorrow.

If today is cloudy, then the probabilities are .45, .35, and .20. And if today is rainy, then the probabilities are .3, .4, and .3. Notice that in this matrix, the values are positive and the columns all add to 1 because they're probabilities. Another way to call this is a Markov matrix, by the way, because it describes how tomorrow will be based on today, and that's what it means to be a Markovian process.

So, I'm going to be a little quicker here. I'm going to take a random vector. Let's say that today is cloudy, and that's our state vector, we're going to call it x0, and we're going to see what happens tomorrow, which is x1. If we multiply this, we get .45, .35, .2, which is actually the second column of the matrix.

And let me do this operation a few times. So that's one day ahead, and if I want two days ahead, I multiply the matrix by that vector, so I get these numbers over here. And if I do it again, for the three days ahead, I get these numbers over here, and I'm going to go a little fast. If I do it four times, I get this.

If I do it five times, I get this, and if I do it six, and seven, and eight, and nine, and I promise I'm almost done. I think 10 will be enough because by now, it's sort of stabilizing, right? It feels like we're getting the same values. The values are actually .6666 forever, .2222 forever, and .1111 forever.

And so the eigenvalue is again 1. And so this is our eigenvector, this is our stability vector, and this is our eigenvalue, and therefore, the probabilities that it's going to be sunny on a random day is going to be this number, 6 over 9, then 2 over 9 for cloudy, and 1 over 9 for rainy. And that's going to describe our dynamical system. That's going to be our transition matrix P and our equilibrium vector, we're going to call it x infinity, which is the one that's going to give us the long-run probabilities.

So if you put that matrix in Wolfram Alpha, you will get these eigenvectors and these eigenvalues. Notice that one of them is 1, and the others are smaller than 1 but still positive. And that first eigenvector is 6, 2, 1, which is a lengthening of the one we had, which is .6666, .222, .111, that doesn't matter, it's still pointing in the same direction. Because an eigenvector describes the direction.

So that 6, 2, 1 is basically that equilibrium line, and the other two eigenvectors and eigenvalues tell you how quickly and in what direction do all the other points converge to that equilibrium line. Now, to visualize this system, I've written some code, and you can see the link in the description, where you can see the dynamical system here. This blue line is this equilibrium line, this yellow point here is the steady state, which is, as we calculated, .6666, .2222, .1111, that's the main eigenvector, the one with eigenvalue 1.

The other two eigenvectors are this purple one over here, which as you can see, has an eigenvalue of 0.42, which is between 0 and 1. That is the scaling that moves any point towards the line in the direction of that purple eigenvector. And the other eigenvector is this green eigenvector with eigenvalue 0.03. That means that a point will go 97% along the way towards the blue line, so that one crunches the space pretty quickly.

And so there they are, the three eigenvectors. And also, I have drawn some points. The point 1, 0, 0, you can see the trajectory and how it moves towards the equilibrium state very quickly. And this other state vector, 0, 0, 1, which also gets moved pretty quickly towards this steady state, the yellow steady state, which is .6666, .2222, .1111.

So I invite you to take a look at the code. As I said, the link is down in the comments, and play with this, and notice how the discrete dynamical system is completely described by the three eigenvectors and the three eigenvalues. So that's it. I hope you enjoyed learning about discrete dynamical systems and their related eigenvalues and eigenvectors.

As I mentioned, this is a sampler of the Mathematics for Machine Learning and Data Science Specialization that I have built with DeepLearning.AI. And this specialization wasn't just me. It was done with a fantastic team of content creators and designers. In particular, this discrete dynamical systems topic was masterminded by Magdalena Bouza, one of the great content creators there, and also by Obed and Anshuman, who was the leader of the project.

There's a lot more people in this team, but I really want to mention these three because of their importance in this particular topic. So definitely check out this course. Let me tell you a bit more about the three courses that comprise this specialization. It has three courses: Linear Algebra, Calculus, and Probability, and all are geared towards what kind of math you need for machine learning.

So this video is a sampler of Linear Algebra, and in my channel, in the links that I have in the description, I have samplers for Calculus and for Probability & Statistics. I encourage you to check them out. The Linear Algebra course has things like vectors, matrices, linear transformations, determinant, rank, eigenvalues, eigenvectors, but my style is that I don't like to see things as numbers and formulas. I always like to see the geometric part of things: how things move, how things get transformed, where are the lines, where are the planes, etc., etc., etc., etc.

The next course is Calculus, where you learn derivatives, optimization, gradient descent, visualizations, basically everything needed to minimize loss functions and do similar things for machine learning. And the last course is Probability & Statistics, where you learn things like Bayesian probability, probability distributions, and then statistical things like maximum likelihood, hypothesis testing. All these are very useful things in the toolkit of any data scientist. So I really encourage you to check out the course. The link is in the description below.

So that's it. Thank you very much, and see you in the next video.
