# Singular Value Decomposition (SVD) and Image Compression 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=DG7YTlGnCEo (약 28:55)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 3개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, I'm Luis Serrano and this video is about singular value decomposition. In this video, I will tell you how some rotations and some stretchings are going to help us with some amazing applications such as image compression. Let's begin.

But before we start, some announcements. This video has some code attached and it's in my GitHub repo. I encourage you to take a look at it and play with the code. It's for the application at the very end.

The GitHub is LuisSerrano and the repo's called singular value decomposition. It's linked in the comments. And also I'd like to announce that I have a book. It's called Grokking Machine Learning and in the comments there's a link to find it and there's also a discount code.

Okay. So let's get started. First, let's get started with some transformations. Transformations in the plane or in space can be seen as a function that takes points to other points.

Some special cases are stretching and compressing. For example, we can stretch an image horizontally or we can also compress it. We can also stretch it vertically and we can also compress it. And finally, we can rotate this image by some angle.

Now that we know how to stretch, compress and rotate, let me give you a puzzle. Can you start with this circle on the left and turn it into the ellipse on the right only by applying rotations and horizontal and vertical stretchings and compressions? By the way, we're going to start calling stretches and compressions scalings from now on.

Feel free to pause the video for a minute and give it a try yourself. But notice something very important and is that you can only stretch and compress in the horizontal or in the vertical direction, not at any other angle.

And here's the way I do it. First, I stretch in the horizontal direction. Then I compress in the vertical direction. And finally, I rotate counterclockwise to get the desired ellipse. That wasn't so hard, right?

Now let's go for a harder puzzle. In this one, the circle is colored like this and you're supposed to turn it into the ellipse on the right, but respecting the colors. So let's try the same thing as before.

First, we stretch horizontally. Then we compress vertically. And finally, we rotate. And oh no, we didn't get the same thing.

We got the shape right, but not the coloring. This problem is harder because we actually have to map every point of the circle to a point in the ellipse. You can think of it as a colored circle or maybe a chain with colored beads that need to be in the right location when you finish the process.

So what can we do now? Well, don't panic. It's just a little harder, but we can do it. What we have to do is, before stretching, we rotate it to be in the right orientation.

Now, we can scale. We can stretch horizontally like before. Now we can compress vertically, and then we rotate again to be in the right orientation.

And voila, now we got it. The moral of the story is that doing a rotation, then a scaling, and then another rotation is the way we can mimic every linear transformation. But what do I mean by linear transformation?

A linear transformation is a matrix, and that's the point of this video: matrices. Every matrix defines a linear transformation on the plane as follows. Let's say this matrix A, which is 3 0 4 5.

It takes every point in the plane and moves it to a different point. For clarity, we have two planes: the one on the left and the one on the right. So, if at the left we have a point with coordinates p, q, then the matrix A sends it to the point with coordinates 3p + 0q for the first row entries, and 4p + 5q for the second row entries.

Let's do some examples. The point 1 0, which is this blue point in the left, gets sent to the point 3 4, which is this blue point in the right. And this is because 3 times 1 plus 0 times 0 is 3, and 4 times 1 plus 0 times 5 is 4.

Now, we can do the other ones. The point 0 1, the red one on the left, gets sent to the point 0 5, the red one on the right. Next is the point -1 0, the green on the left, which gets sent to -3 -4, the green on the right. And finally, the point 0 -1, the yellow on the left, gets sent to 0 -5, the yellow on the right.

And we can map a few more points, like these four, which get mapped to these four. As you can see, on the left we can draw a unit circle, which gets mapped in the right to this ellipse over here. And in general, every 2 by 2 matrix will define a linear transformation that sends the unit circle in the left to some ellipse centered at the origin on the right. And that ellipse defines the linear transformation.

Now, some matrices are special. For example, matrices that look like this: cos theta, sin theta, -sin theta, cos theta, for some angle theta. They represent a rotation by an angle theta.

And diagonal matrix, namely those that only have elements sigma 1 and sigma 2 in the main diagonal and zeros everywhere else, represent scaling. So they represent horizontal stretching of the plane by a factor of sigma 1, and vertical stretching of the plane by a factor of sigma 2. Notice that in this case, the factor is bigger than 1, so we're doing a stretching.

If it's less than 1, we're doing a compression. And if it's 1, we're doing nothing. Also, if it's a negative value, then this is a stretching followed by a reflection over the axis, but we're not going to worry much about this now.

Now, what does this have to do with matrices? Well, here is the main moral of this video. In the same way that at the beginning in the puzzle, we used a rotation, a horizontal stretching, and a vertical stretching, and then a rotation to get from the circle to any ellipse that we want, point by point, then any matrix, any linear transformation, can be expressed as a rotation followed by a horizontal and a vertical stretching, followed by another rotation.

And in matrix form, this is equivalent to matrix multiplication. Here is the main equation for today. We can write this matrix as a product of these three: a rotation matrix, a scaling matrix, and another rotation matrix.

We write our matrix as A, our two rotation matrices as U and V, and our scaling matrix as Sigma. Notice that this V has a dagger standing for the adjoint or conjugate transpose. This won't matter too much in our video today because most matrices we'll use are square, but it's an important thing to notice, and it is for notational and dimensional convenience that we use V dagger instead of V.

Now, how do we find this? Well, there are mathematical ways, and they are not too different from finding eigenvalues and eigenvectors, but I will leave that mathematical reasoning for another video. And for now, I have two great ways to do it.

One is using WolframAlpha, which is one of my favorite tools, it's free online on the web. And the other one is using the NumPy package in Python. It has a very simple function called SVD.

So here is the decomposition that we just found, and let's interpret it as rotations and scalings. So, if you like floating-point numbers, you can use this one. If you like radicals and square roots, you can use this one. They're both the same thing.

So we're going to use the unit circle in the left for reference. First, let's look at the matrix in the right because when we multiply these matrices by a vector, the first one we multiply by the vector is the one at the right, so they read backwards. This matrix on the right happens to be a rotation of negative pi over 4, which is negative 45 degrees.

And you can work out that the cosine and the sine of negative 45 degrees actually gives us this matrix from the rotation matrix we introduced before. So, in the left, we're going to rotate our circle by negative 45 degrees like this, which is the same as 45 degrees clockwise.

Now, let's look at the next matrix. The next is a scaling matrix. So, this first entry scales everything horizontally by a factor of 3 square root 5, which is positive, so it stretches it like this. And the second factor scales everything vertically by a factor of root 5, which does this because root 5 is also bigger than 1, so it stretches.

And finally, the matrix on the left is also a rotation matrix. It's harder to find the angle, but if you take the ratio between the left coordinates, you get

## Part 02 (10:00–20:00)

The arc tan of 3, which is 71.72 degrees or 1.249 radians, and that's the rotation. So we proceed to rotate the plane by that angle counterclockwise. And voila, that's exactly how the original transformation looked like.

We can summarize everything in this graph. Our original transformation A turned the unit circle into this ellipse.

And that can be summarized into one rotation V dagger, then two scalings Sigma, one scaling is horizontal and the other one is vertical, and finally another rotation U. And that encompasses the equation in the middle: A equals U Sigma V dagger.

Now let me show you how this is used in dimensionality reduction or simplifying our matrices. Here is a slightly different matrix with entries 1.8, 1.2, 4.4, and 4.6. Notice how it still turns a unit circle on the left into an ellipse on the right, but this time the ellipse on the right is really skinny. It's almost like the points are forming a line.

That means that the matrix is close to being a degenerate transformation, a transformation that takes the whole plane on the right and crunches it into a line on the right. That means that the matrix is close to being singular, having determinant zero, meaning that it has a smaller rank than its size.

Now, that's a lot of linear algebra terms, but we'll get into some of them later. For now, let's look at this transformation through the lens of the singular value decomposition to see where we can capture that skinniness of the matrix.

And in particular, let's look at the scaling matrix Sigma. The horizontal scaling is large, it's a factor of 6.71, and that's why the ellipse is long. But the vertical scaling is only by a factor of 0.44, which is very small.

And this is the reason the ellipse is so skinny, is because we're compressing it vertically to almost a line. So the degeneracy of this transformation is really encoded in the 0.44 here.

So what if we said, "Hey, who are we kidding? This 0.44 is really small. Let's turn it into a zero and see what happens." So we turn it into a zero, which means that we're compressing this ellipse into a line.

And our transformation becomes a transformation that turns the entire plane, the entire circle and the entire plane, into a line. And as I mentioned before, this is called a degenerate transformation.

And so something very special happens. If we turn this 0.44 below into a zero, then our original matrix changes because our original matrix was the product of these three. So our new matrix is 1.5, 1.5, 4.5, and 4.5.

Notice how strange this matrix is. Its rows are the same. And this is an example of a degenerate matrix. Now, not all of them look like that, but they do have relations between the rows and relations between the columns.

And so, as we mentioned, this matrix has rank one. Morally, it just feels like it doesn't carry enough information, right? This matrix, the the the two columns are exactly the same, so we can just encode it into one of the columns and then say, "Well, they're both the same, so you don't need to record all these numbers," right?

So let's recap. Our original, almost degenerate matrix of rank two got sent into a matrix of rank one.

So notice how, doing a small modification, we managed to store a a very close matrix of rank two as a matrix of rank one. Now, if that's not clear and that may be confusing, let's look at a bigger example.

This is a rank-one matrix. Now, stare at this matrix for a moment and think of what's special about it. It's it's not random entries at all.

If you look at it for a while, you notice that the rows are all very similar. They all look like 1, 2, 3, 4.

It's just that the first row is 1 times 1, 2, 3, 4, and the second row is -1 times 1, 2, 3, 4, and the third one is 2 times 1, 2, 3, 4, and the fourth one is 10 times 1, 2, 3, 4. So they're all multiples of 1, 2, 3, 4.

So I don't need 16 entries to encode this matrix. I only need eight because I only need the green and the blue entries.

I can only say, "Well, these are all multiples of the green one, and the multiples are on the blue entries." So that's the same as saying that this matrix can be expressed as the product of these two vectors, and that's called an outer product.

Now, what is special here? Well, that the matrix on the left, I need 16 numbers to encode it, whereas the one on the right, I only need eight numbers.

Now, there's not a huge difference between 16 and 8, but imagine if this was a 1,000 by 1,000 matrix. On the left, you have 1 million entries, and on the right, you only have 2,000 because it's two vectors of 1,000. So I've saved a lot of space.

And that's what we mean by compressing. That's what we mean by dimensionality reduction. I have expressed a matrix that has unnecessarily more entries than it needs to as a product of two smaller things.

Now, obviously, I cannot do that with every matrix. Let's look at this matrix. This matrix, there's no way I can find two vectors that multiplied give you that matrix because that's very random.

That's an actually rank-four matrix, its determinant is not zero. I need all the 16 entries to explain this matrix. So I can't express it like this.

But what we do with singular value decomposition is that we approximate this matrix as a sum of rank-one matrices. So instead, I can say, "Well, this matrix is this rank-one matrix plus this one plus so on."

And how many do I need? Well, I actually need four. But let's just say I need many of them. And then I decide how far do I want to go.

If this is a sum that gets smaller and smaller and smaller, if I stop somewhere, I can say, "Well, okay, my matrix, I won't be able to express it as as a sum of one or maybe two rank-one matrices, but it's close enough." And that's what we do with singular value decompositions. We say, "My matrix is close enough to a a sum of a few rank-one matrices, so I'm going to call it that sum."

And let me show you how we do that expansion using singular value decomposition. So let's say we have our matrix A, and we express it as a product of a rotation matrix U, a diagonal matrix Sigma, and another rotation matrix V dagger.

And I'm going to label the columns of U as U1, U2, U3, U4, the diagonal elements of Sigma as Sigma1, Sigma2, Sigma3, Sigma4, and the rows of V dagger as V1, V2, V3, V4.

And now, we're going to carry out the matrix multiplication, and it actually expands like this. The first term is Sigma1 times the outer product of U1 and V1, and the rest are similar terms.

That's actually what happens if you actually carry out the matrix multiplication, you get that. And each one of these is a rank-one matrix. Now, their sum is obviously a higher rank matrix. But now, the key is on the red numbers.

And those numbers are the singular values. So let's say that the first one is a large number, and that the second one is a medium number, and the third one is small, and the fourth one is tiny. So we've been able to order them from large to small.

And let's say that the third and the fourth are tiny enough that we don't need to worry about them, so we can forget about them. And we've been able to express our matrix A as a sum of two rank-one matrices, and that is a lot simpler than a rank-four matrix.

So we've been able to find a matrix that is very similar to A, but that has a smaller rank, and that we can compress, we can encode using fewer entries.

And that's the idea. Obviously, here we went from 16 entries to 4 plus 4 plus 4 plus 4, which is actually 16. But imagine if this matrix was a 1,000 by 1,000. We've been able to express it as 4,000 entries, which is much better.

Now, as a quick example, let's work out the decomposition of the original matrix we were looking at. You can do this with WolframAlpha again or with Python, and we've worked it out in the repo that I show you in this video.

It's this one over here. And when we look at the components, the largest singular value component, which is 21.2, is this outer product, which gives us this rank-one matrix. And notice that this matrix is very close to the original. It's actually the closest rank-one matrix.

## Part 03 (20:00–28:55)

matrix that we can find to the original matrix.

Now, if we're not content, we can keep going and find the component with the second singular value. And if we add these two things, we get this one. Now, notice that now we're awfully close to our original matrix. This is the closest rank-two matrix that we can find to the original matrix.

And we can keep going. Let's take the third component. So, it still has a small eigenvalue, and the sum of these three is this.

And notice that now we are awfully close to our original matrix, right, with a rank-three matrix. This is, again, the closest rank-three matrix to the original matrix.

But if we're not fully content, we can go all the way. The last eigenvalue is tiny because it's just made up of tiny corrections that will get us the original matrix. After four iterations, we always get the original matrix because the original matrix has rank four.

Now, I've noticed that I've used the word rank a lot without really explaining it. So, let me give you an idea of what rank is.

And we're going to keep the example of a 4x4 matrix, but you can imagine this in any size. So, rank-one matrices are the most predictable ones. They may have a lot of entries, but the entries satisfy a lot of relations, and we capture this with this equation.

We can write the matrix as a product of a tall, skinny vector of width one and a short, long vector of height one. So, there's a lot of structure to the coefficients and a lot of correlations between them.

Now, a matrix of rank two we cannot express like this, but we can express it like this, as a product of a matrix of width two and a matrix of height two.

So, it's still got a lot of structure, it still has a lot of correlations, it's still predictable, but less predictable than the matrix of rank one. It's just a little more complex.

A matrix of rank three is not expressible like this, but we can express it like this, a product of a matrix of width three and a matrix of height three.

And finally, a matrix of rank four is the most complex of all. In this case, it's a full-rank matrix because you cannot get any higher than rank four with this matrix. Normally, the highest rank you can get is whatever is smaller between the number of rows and the number of columns in the matrix.

And so, for this rank-four matrix, for this full-rank matrix, there's simply no linear relations that we can exploit like this. So, as you can see, the higher the rank, the higher the unpredictability among the entries, and the lower the rank, the higher the relations between them that we can exploit.

And so, the goal of dimensionality reduction is to say, "Okay, we have a very big matrix, and it may have high rank, so it may be hard to express it as a product of two small matrices, but we can find a matrix that is very close to it and that has a much lower rank, so I can express it as the product of two small matrices and, thus, store it much easier." Now, notice that all our matrices were square.

What happens if we have a rectangular matrix, say, this 4x6 matrix? Well, that still works. This method is fascinating because it still works for any shape of a matrix.

The way it works is U is still going to be 4x4. Sigma is not going to be 4x4, but it's going to look like a 4x4 with two rows of zeros, so we pad it with zeros to make it 6x4.

And V dagger is going to be a 6x6 matrix. And this product actually checks out.

Now, notice that these vectors, v5 and v6, they never get touched in this product because they will correspond to these two rows over here. But that's okay.

It's still useful to have the entire matrix. So, we can use this method in matrices of any shape we want, and that's super important.

Now, finally, let me show you a really cool application to image compression. We're going to compress this image of a heart.

And this is all done in this GitHub repo, so you can sing along with the code. My GitHub is LuisSerrano, and the repo is called Singular Value Decomposition.

So, first, we're going to add values to the pixels. So, I'm going to add a one for the black ones and a zero for the white ones. This is normally done the opposite way in graphics, but I like this one because it's better for visuals.

So, basically, we're going to compress this matrix of ones and zeros over here. So, we're going to find the singular value decomposition using our favorite tool, whether it's WolframAlpha or NumPy.

We're going to get this decomposition. And you may get a different one.

They they are the same up to certain transformations, so this is okay if you get a slightly different one. But we're going to work with this one.

And depending on the tools you use, they may give you matrices of slightly different sizes, but that only means that you may have to pad some zeros here and there. But, in general, the answers are consistent.

So, we're going to compress this matrix. And how do we get the components? Well, we're going to be doing outer products. So, let's take the outer product of the first column of U, the first row of V dagger, and we're going to multiply it by the scalar, which is the top-left entry of Sigma.

So, that gives us this image over here. Notice that it looks like a fuzzy version of the heart, and it's also a rank-one matrix if you look at it.

It's a very simple matrix, but it sort of captures the heart a little bit. And its intensity is the singular value, which is 4.74.

Now, let's go to the next component. The next component is the outer product of this green column on the left, this blue column on the right, and we multiply it by this factor of 1.41.

So, as you can see, it's a slightly lighter matrix because it's multiplied by a smaller number. It has less intensity.

And we keep going, finding each component. And since each singular value is smaller, each matrix is lighter than the next one. And some of them are zero, and we start getting to zero singular values.

And this poor column over here, this poor row over here, never actually gets used in the product, but that's fine. So, these are our components.

And now, all we have to do is add some of them, starting from the left. So, if we add the first one, well, we get this image. If we add the first two, then we get this image, which is a little a little more sharp.

Then, if we add these three, we get this image, which is just a little sharper. And if we add this one, we get a perfect heart. And we can stop there because the last ones have singular value zero.

And this all means is that this matrix over here has rank four because it was expressed as four terms over here. So, we can always decide how far we want to go.

If we don't have a lot of storage, we can use the first or the second image. And if we have more, we can keep using more of these components. But, in general, the singular value decomposition allows us to pick how sharp we want our image, and the price is, obviously, that the sharper we want the image, the more storage we're going to need.

And that is it for singular value decomposition. If you liked this technique, I highly recommend other videos that I have on similar dimensionality reduction topics.

There's one on matrix factorization and one on principal component analysis. The links are in the description.

And that's all, folks. Thank you so much for your attention. I'd like to remind you that I have a book called Grokking Machine Learning, where I explain the algorithms of supervised learning and some interesting machine learning techniques with simple real-life examples and lots of Python code.

You can get it from manning.com, and with the special discount code "serranoyt", you can get a 40% discount. So, if you liked this video, please subscribe for more content, or hit like, or share among your friends.

Or feel free to add a comment to tell me what you thought. I I love reading your comments.

Also, if you have ideas on what you'd like to see next, let me know in a comment. You can also tweet at me.

My Twitter handle is @luislikesmath. And in this page, serrano.academy, you can find all this information: the videos, the book, and any news. Thank you very much. That's all for now, and see you in the next video.
