# Principal Component Analysis (PCA) 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=g-Hb26agBFg (약 26:33)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 3개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, I'm Luis Serrano and in this video we're going to learn principal component analysis or PCA. Principal component analysis or PCA is one of the most important dimensionality reduction techniques out there.

What is dimensionality reduction? Well, let's say you have a huge table of data, so big that it's hard to process, and you would like to make it into a smaller one while still keeping as much of the information as possible. So dimensionality reduction techniques, what they do is they reduce the number of columns.

And so today we're going to learn PCA in a few steps. First we're going to learn what projections are, then we're going to learn variance, covariance, covariance matrix, then we're going to learn what eigenvalues and eigenvectors are, and finally we're going to go to PCA. So let's begin.

So let's start with a simple problem. Let's say we have a bunch of friends standing like this, and we want to take a picture of them. So the question is where do we take the picture from, what angle?

So it could be this one, it could be this one, or this one. Well, it seems like this would be one of the best angles to take the picture, right? And that's really what dimensionality reduction is. It's taking a picture of your data.

And trying to keep as much information as possible in this picture. So when your data looks like this, then a picture of the data could be, for example, projecting it over this line, then you get these points over here. Another one could be projecting it over this line.

Now the question is, intuitively, which of the two projections seems better? Let's compare them, put them side-by-side. Well, it seems to me that the one on the right is better because the points are more spaced out and you can actually tell them apart.

If you only had this picture, you could actually make out the data a little better than with the one on the left. So what we're going to learn in this video is how to obtain the projection in the right, how to get that sort of ideal line to project our data and keep it as sparse as possible.

So first a little parenthesis. Why does this matter? Why do we do this? So let me give you an example of some housing data.

Let's say we have a housing data set with a bunch of columns, with the following information: size, number of rooms, number of bathrooms, the schools that are around the area, and the crime rate. So if I gave you this data set and I told you there's too many columns, there's five and I want less, what would you think? Feel free to pause the video and think.

How can we sort of reduce this and keep the information? Well, just from eyeballing it, I can see a difference here, right? The first three features are related to size, so maybe we can lump them together into something called a size feature. And the second two are related to the neighborhood, so let's lump them together into something called a location feature.

So that's what dimensionality reduction is, right? We went from five columns to two, and we're capturing the information because it seems to me that a bigger house may also have a higher number of rooms and a higher number of bathrooms, so we may not need the three pieces of information, we may need maybe a sum of the three or maybe a weighted sum, and the same thing for the second, for the location feature.

So how to do this ideally? That's what PCA does. So let's look at an example, not from going from five columns to two, but let's go from two columns to one.

So we have number of rooms and size, and we're going to try to lump those into one feature. So we have a graph here where on the horizontal axis we have number of rooms and on the vertical axis we have size. And notice that our suspicion was correct: the bigger the house, the more rooms it has.

There is some variation, but for the most part. And so where would we project this data? How do we take a picture of these houses so that they look as spaced out as possible?

Well, it seems like this line would work, right? And a little aside, we're not doing linear regression. We're not trying to fit the closest line to the data. We're trying to fit the one that makes the best projection, so it's slightly different. And definitely with a different purpose.

But if we do this, then we project each house to the line by drawing the perpendicular and sending it there. So we do this, and then our data set changes a little bit. It's not exactly the same one, it's not faithful to the data, but it's much, much simpler because now it's not two-dimensional, it's one-dimensional because now we can see it like this, and now we only have one axis, which is the size feature.

So now all of a sudden, our data set became more simple. It went from being a two-dimensional data set, so a table of two columns, to a one-dimensional data set, so a table with only one column. Now every house only has one number attached to it, not two.

So from two dimensions to one dimension, namely size and number of rooms to the size feature. Now, we did it from two dimensions to one dimension because it's graphically nice to see, but you can imagine that from five dimensions to two dimensions, it would be going from something like these features to the size and the location feature. So it's hard to picture five dimensions in our head, but imagine what we just did from two to one, imagine it doing from five to two.

So if you've seen statistics before, the next couple of minutes may look like a review, but I still find it interesting because I like to see things in a more geometric way. So what is the mean of a set of numbers? Well, let's say that I have three weights that are exactly the same, and I want to balance them.

So how do we balance them? How do we find the perfect point of balance for these three weights? And let's just assume that that bar has no weight.

So what I'm going to do is I'm going to imagine that there's a wall here at the left, and I'm going to measure the distance from every point to the wall. So the one is at distance one, then the other one's two, and then the other one is six. And I'm going to take the average of these points.

So the mean is 1 + 2 + 6 divided by 3, and that's the point of equilibrium. If I were to put a balance here at three, then the points would balance. But now there are a lot more things I can say about a set, for example, what if I have these three points and these three points?

How do I tell those apart? Well, not using the mean because they have the same mean. Notice that they balance on the same point. But if you can see, the points in the top are a lot closer to each other, and the ones in the bottom are a lot more spread out.

So how do I measure that? What I'm going to do is I'm going to take the distance from each point to the center. So the point in the left is at distance one from the center, the point at the right is at distance one from the center, and the point in the middle is at distance zero from the center because it's actually the center.

It's the point where the points balance. And the same thing in the bottom, except these are five, five, and zero. So the variance is you're going to add these numbers, but actually it's going to square them.

And the reason we square them is because actually when you take a distance that goes towards the left, you're subtracting coordinates, and then so you're going to get negative numbers. So you square everything so you get everything positive. And so for the top, you get 1 squared + 0 squared + 1 squared divided by 3, which is 2/3.

And for the bottom one, we get 5 squared + 0 squared + 5 squared divided by 3, which is 50 over 3, so it's much bigger. So this is basically a measure of how spread out is a set. So now we have what is the variance of the original set?

Well, from the center, the point on the left is at distance two, the next point is at distance one, and the point on the right is at distance three. So the variance is 2 squared + 1 squared + 3 squared divided by 3, the average of these squares, and so that is 14 divided by 3. So you can see that it makes sense, 14 divided by 3, because they're kind of spread out.

Now the question is, what is the variance for a two-dimensional data set? So when the set is in the plane, what do we mean by spread out? Well, two things we can do is ask how spread out it is in the horizontal direction and how spread out it is in the vertical direction.

So basically, we forget about the height and we send everything to the horizontal or x-axis, and then calculate the variance of those points, which is the x-variance. And then do the same thing, but by forgetting the x-coordinates, sending everything to the vertical axis, and now with those points, we calculate the y-variance. And then we have two numbers, the x-variance and the y-variance, and they should tell us well how spread out is a set.

However, there are some technicalities. Let's look at this set and let's look at this set. What are the x and y variances of those two?

Well, let's calculate the x-variance, and let's say these distances are two. So it's going to be 2 squared + 0 squared + 2 squared divided by 3, which is 8 divided by 3. And what's the y-variance? Well, it's if these distances are one, then it's 1 squared + 0 squared + 1 squared divided by 3, which is 2/3.

So those two sets have the same x-variance and the same y-variance, but they're fundamentally very different. So how do we tell those two apart? Can we have a third metric that tells us that these two are different? And the answer is yes, and that's going to be covariance.

So the question the covariance answers is how do we tell these three points apart from these three points? So let's think, can you think of a number or a metric that tells those two sets apart? Feel free to pause the video and think about it. And I'll tell you the one that I think, it's the product of coordinates.

So what if you look at the two numbers and multiply them, the two and the one, the minus two and the one, etc.? Well, let's see. For the point in the middle, 0 times 0 is obviously zero.

For the top right and the bottom left corner, it's actually plus two because 2 times 1 is 2, but minus 2 times minus 1 is also 2. And for the other two points, it's minus two because 2 times minus 1 is the same as minus 2 times 1, which is minus 2. So...

## Part 02 (10:00–20:00)

So, this product of coordinates is positive for these two points, and negative for these two points, and it's zero for the one in the middle. But that, that's okay. It still, it still helps us tell the points apart. So, basically covariance is that, is the sum of products of coordinates.

See, before it was the sum of squares of one of the coordinates, now it's the sum of products of coordinates. So, let's calculate the covariance of this set. We see that the products are -2, 0, and -2. And for this set, where the products are 2, 0, and 2.

So, the covariance for the set on the left is -2 + 0 + -2, which is -4 over 3, divided by 3, the average of those. And the one on the right is 2 + 0 + 2 divided by 3, which is 4 over 3. So, the points on the left have a negative covariance, and the points on the right have a positive covariance.

If you heard the term correlation, that's also very related to this. The points on the left are negatively correlated, and the ones on the right are positively correlated. This is because in the ones on the left, as the x direction grows, the y direction decreases, whereas in the ones on the right, as the x direction grows, the y direction grows as well.

So, let's look at another set and try to calculate the covariance. This is our set. What do you think the covariance of this one is going to be? Well, let me tell you.

Let's calculate all the products. They are -2, 0, and 2, according to these numbers over here. And then the covariance is just the sum of all those things. But you can see that they all cancel out.

So, the sum of all those things divided by 9, the average, is actually 0. And it made sense, because this set is not positively correlated or negatively correlated. It doesn't look like a diagonal in either one of the directions. It looks like a sort of thing in the middle.

So, by looking at the type of set, we can sort of tell the covariance. If we have a set like this, or like this, or like this, what do you think the covariances are? So, the first one looks like an inverted diagonal, so it's got negative covariance.

The second one looks like it's just sort of well-centered, so it has probably covariance of 0, or a very small covariance. And the third one has a positive covariance because it looks like a sort of forwards diagonal. So, this covariance is going to help us a lot with PCA.

So, now we're ready to start thinking about PCA. Let's say we have a dataset like this one. How do we find the perfect projection? Well, first, let's put it in some coordinate axis.

And the first thing we're going to do is center it. So, centering it means we're going to take the average of the coordinates, both in the x and in the y direction, find that center of mass, think of the point where this set would balance, and move that to zero. So, we're going to move it so that the dataset is centered at zero.

And now, we are going to create a 2x2 matrix. And the 2x2 matrix is going to be very simple. It's just going to be formed by the two variances and the covariance of this dataset.

So, on the top-left corner, we're going to put the x variance, so the variance on the horizontal axis. In this coordinate, we're going to put the y variance, so the variance in the vertical direction. And then in the other two spots, we're going to put the covariance. We're going to put it there twice.

And in the literature, this matrix is normally called sigma, but we're just going to call it the covariance matrix. And so, let me just make up some numbers. This dataset looks like it could have this covariance matrix: 9, 4, 4, 3.

This is because 9 is the x variance, because the dataset looks like it's pretty spread in the x direction. It's not so much spread in the y direction, so the variance y is maybe something like 3. And it looks like it has positive covariance because it looks like a forwards diagonal. So, let's just say that the covariance is 4.

So, now we're going to do a little aside on linear transformations, because that matrix, we're going to think about it now as a linear transformation. Don't get scared with the term. Linear transformation is really just a function or a map from, say, the plane to the plane.

This could also be in higher dimensions, but here it's just going to be in two. So, it sends any point in the plane on the left to a point in the plane on the right, in the following way, using the numbers of the matrix.

So, a point of coordinates x, y gets sent to the point 9x + 4y and 4x + 3y. So, two coordinates go to two coordinates. And the numbers are taken from the matrix.

This 9 and this 4 get encoded here at this 9x + 4y, and this 4 and this 3 get encoded in this 4x + 3y. If you feel more comfortable thinking of points as two rows instead of two columns, the way I did it, feel free to think of that so that you can think of matrix multiplication. But if you want to just simplify, think about it this way.

So, let's see what this transformation does. Let's see what it does to several points. Where does the point 0, 0 go? Well, what is 9 * 0 + 4 * 0?

Well, that's just 0. And 4 * 0 + 3 * 0, that's 0. So, this goes to the point 0, 0. So, let's draw the point on the left, the point 0, 0, and that goes to the point 0, 0. So, very simple.

Let's do another slightly more complicated point. Where do you think the point 1, 0 goes? At any moment, feel free to pause the video and think about it yourself.

1, 0 goes to 9, 4, because if you plug in the numbers 1 and 0 for x and y, you get 9 and 4 for 9x + 4y, because you get 9 * 1 + 4 * 0, and then 4 * 1 + 3 * 0. So, that goes to the point 9, 4. So, we're going to send the point 1, 0 on the left to the point 9, 4 on the right. And these are not drawn to scale, but I'm trying to capture the entire movement here.

Next point would be 0, 1, which is over here, and you can do the math, that goes to 4, 3. So, it goes over here. The next point is -1, 0, which is here, and it goes to -9, -4, which is over here. And finally, the point 0, -1, which is over here, goes to the point -4, -3, which is here.

And hopefully, you can see a pattern here, right? As a matter of fact, if you take this circle, the unit sphere, where do you think it goes? Well, it goes to this ellipse over here.

Now, it almost seems like what we did was stretching the plane in a sort of diagonal direction. Actually, we did two stretchings, but one is very small. But that's really what a linear transformation does, most of them.

So, let's think about this. There is some vector here, the red vector, that actually goes to this one. So, what happens is we sort of stretch the plane in that direction.

The direction is, we can calculate it in a minute, but it's 2, 1. So, it's two units to the right and one unit up. That's just the direction, that's not the vector. And the magnitude is 11.

We'll see why it's 11. But basically, the plane got stretched by a factor of 11 in that direction. And then there's another vector, which has the direction -1, 2, and that one gets sent to itself. So, it's actually stretched by a factor of 1.

Sometimes you will have different numbers, but basically think of it as two stretchings, and they happen to be perpendicular in this particular case. So, let's see. The directions are 2, 1 and -1, 2.

These are the eigenvectors, which give us direction. And the eigenvalues, which are these factors of stretching, are 11 and 1. So, those are, as I said, called eigenvalues, and they give us the magnitude.

So, again, we can think of a linear transformation, given the eigenvectors and the eigenvalues, as in the direction 2, 1, so two units to the right and one up, we stretch by 11. In the direction -1, 2, which is one unit to the left, that's -1, and two units up, we stretch by a factor of 1, so we don't do much. And so, the transformation basically does this.

So, notice that these two vectors are very special because an average vector, so anything that goes like in this direction, for example, I'm just drawing a random vector, goes to some other thing. But the red vector goes to something that points in the same direction, and the green vector goes to something that points in the same direction.

So, those two are the eigenvectors, the two vectors that actually go to something that points in the same direction. And basically what you're trying to say is that the linear transformation, which is this matrix, for most vectors, it does some crazy thing, but for two particular vectors, applying it to the vector v is the same as multiplying that vector v by a number, right?

So, it's scaling, and it's sending in the same direction. So, these are the eigenvectors, the red and the green vector, and this value is the eigenvalue.

So, there are many ways to calculate eigenvalues and eigenvectors. My favorite was just type the matrix into Wolfram Alpha, and it just tells me everything.

There's an algebraic way that I won't get into much detail, but basically you take your matrix, you take the characteristic polynomial, which is subtract x minus the things in the diagonal, and then do minus for everything that's off the diagonal, take the determinant of this, which is this formula over here, and express it as a quadratic, and factor this quadratic into two things, and then you magically get (x - 11)(x - 1).

I'm going a little fast here because it's something that if you really are interested, you can read further. Then the eigenvalues are going to be the two roots of this polynomial, so 11 and 1. That's how we find the eigenvalues.

And how do we find the eigenvectors? Well, now that we have the eigenvalues, then we have transformation times a vector [u, v]—and I'm reusing the letter v...

## Part 03 (20:00–26:33)

But that doesn't matter, now we just have two coordinates is equal to 11 times that vector, and the matrix times another vector is 1 times that vector. So, if we solve these as two linear equations for u and v, we get the eigenvector 2, 1 and the eigenvector -1, 2. If you find this interesting and you want to see some amazing animations with amazing explanations, go to this channel, 3Blue1Brown. He has a whole series on linear algebra, and his treatment of eigenvectors and eigenvalues is actually fantastic.

So, that may have been a little bit too much math, but think about this as the moral just says that if you have a linear transformation, it is stretching the plane in two directions. And those directions are given by the eigenvectors, and the amount of stretching is given by the eigenvalues.

Okay, so now we're ready to do PCA. First, we start with a dataset, and we center it. Now, we calculate the covariance matrix, which, as we saw, the x-variance is 9, the y-variance is 3, and the covariance is 4.

So, this matrix has eigenvectors, which give us direction, eigenvalues, which give us magnitude. The first one is direction 2, 1 and magnitude 11, which is this one over here. The second one is direction -1, 2 and magnitude 1, which is this one over here.

And notice that the two eigenvectors and eigenvalues tell us a lot about our dataset, right? Because it sort of tells us in what direction is spread and by how much. Also, notice that the red and the green vectors are perpendicular. That's not out of luck.

That's something that happens when we have a symmetric matrix. Symmetric means that, in this case, this 4 and this 4 are the same. Because, in general, symmetric means if you reflect the matrix over the main diagonal, you get the same matrix. So, the entries on top of the diagonal are the same as the ones below the diagonal, the corresponding one.

And when the matrix is symmetric, then the eigenvectors are orthogonal or perpendicular, even in higher dimensions. Another thing that is pretty lucky is that the transformation is actually two stretchings. This also doesn't happen all the time. Some transformations are rotations or different things, and that's because sometimes the eigenvalues are imaginary numbers or complex numbers.

In this case, they are real, which is also something that happens when the matrix is symmetric. So, because covariance matrices are always symmetric, because that's how we build them, we put the entry on top and on the bottom, that 4, we repeated it. So, in this particular case of covariance matrices, they always have very nice eigenvalues and eigenvectors that are perpendicular.

So, what we're going to do is we have summarized our dataset as the red vector and the green vector. And what we're going to do is we're going to say, "Okay, which one is more important?" Which one do you think is more important?

Well, the one with the largest eigenvalue, right? One of them matters 11 times the other one.

So, let's say the 11th one wins, and the other one gets the boot. So, we delete everything that's green and only care about what's red. And what does that mean? Well, that means we're going to consider this entire line, and we're going to project everything into this line.

And that is the projection. That is the picture of the dataset. And let's see what we did. What we did is we turned our two-dimensional dataset into this one-dimensional dataset. And because we picked projecting over the eigenvector with the highest eigenvalue, that means we projected over the axis that carries the most amount of information.

Okay, so now we are finally ready for the big picture of PCA. Are you ready? We start with a large table of data with lots of rows and lots of columns. In this case, we're going to say five columns, but you're going to see how this works in general.

So, this gets plotted in a five-dimensional plot. I can't draw in five dimensions, but this is my best sort of imaginary representation of how things would work in five dimensions with five axes.

So now, from this data, we get a 5x5 covariance matrix. In the main diagonal entries, we see all the variances with respect to each of the dimensions. And in the off-diagonal entries, we get the covariance for each pair of dimensions taken at a time. And notice that this is symmetric because we put the same entry on the top right as the bottom left.

So now that we have a matrix, we calculate a bunch of eigenstuff. We calculate five eigenvectors with their corresponding eigenvalues. Then, we order them from small to big.

And now, it's up to us to pick how many of the big ones we want. That depends on the eigenvalue or on how many dimensions we want to get to. But let's say we pick the top two and erase the bottom three.

So now, what do we do? We go back to our five-dimensional plot and plot those two eigenvectors with the length being the corresponding eigenvalue. So, we get these two, the red and the green.

Now, this creates a smaller dimensional space. In this case, it creates a plane, a plane we can see. So now, what we do is we project everything with respect to this plane, so we sort of take the shadow or like take a picture that prints in this plane. And we get a two-dimensional plot.

And this two-dimensional plot is a pretty faithful representation of our five-dimensional plot because we did it the smartest possible way by picking the directions in which the data is spread the most. And therefore, from this two-dimensional plot, we get a smaller table with two columns that actually captures the data as well as possible. So, that's it. That's the dimensionality reduction, and that's the big picture of PCA.

And that's it for this video. Thank you very much for your attention. As usual, if you liked this, please subscribe for more videos coming up. Please hit like and share with your friends, and write a comment. I love to read your comments, and it's always very useful for me to see suggestions of what topics you would like to see, etc.

And if you would like to tweet at me, this is my Twitter handle, @LuisLikesMath. So, thank you very much, and I'll see you in the next video.
