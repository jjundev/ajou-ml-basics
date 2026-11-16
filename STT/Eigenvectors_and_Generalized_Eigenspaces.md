# Eigenvectors and Generalized Eigenspaces 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=ajXb3N6QEqc (약 19:18)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 2개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, I'm Luis Serrano and this video is about eigenvalues, eigenvectors, eigenspaces, and their generalized counterparts.

Let's begin with a matrix, for example, this one with entries 2, 1, 0, and 3. And matrices transform vectors into others by the way of matrix multiplication. So to calculate the product of this matrix and the vector with entries x, y, we take each row of the matrix and combine it with the column vector like this. This is called the dot product.

And we obtain the vector with entries 2x + y and 3y. But this looks like some formulaic mumbo jumbo. Is there a nice picture attached? And luckily, the answer is yes.

So in this video, I'll show you this picture, and I will also show you some very important concepts. The first one is eigenvalues, eigenvectors, and eigenspaces. And the second one is generalized eigenvalues, generalized eigenvectors, and generalized eigenspaces. So let's begin.

A nice geometric way to see the matrix is as linear transformations, namely as a way to map the plane onto itself, where every point goes to some other point. Let's look at the transformation that corresponds to this matrix with entries 2, 1, 0, and 3.

Now, my second favorite way to see transformations, and I say second because the first one is coming up very soon, is to form a square and see where this square goes. Recall that in this transformation, the point with coordinates x, y goes to the point with coordinates 2x + y and 3y.

So one of the vertices of the square is the point 0, 0, which if you do the calculation, goes to the point 0, 0. This always happens because 2 times 0 plus 0 equals 0 and 3 times 0 equals 0.

We can do the other points and notice that the point with coordinates 1, 0 goes to the point with coordinates 2, 0. The point with coordinates 0, 1 goes to the point with coordinates 1, 3. And finally, the point with coordinates 1, 1 goes to the point with coordinates 3, 3.

And now we can conclude that this small square goes to this larger parallelogram. And the wonderful property of linear transformations is that the grid formed by the square goes to the grid formed by the parallelogram.

Therefore, for any point, say this one around here, the way to find where it goes is by looking at the corresponding point in the grid on the right. And we can easily move this point around, and as long as we respect the grid, we know exactly where the point goes.

And as this square and the parallelogram tessellate the entire plane, we call them bases. Therefore, what the matrix does is a change of basis. It changes from one basis to the other one, and then it describes the entire transformation.

The two basis vectors are these two that describe the square on the left and these two that describe the parallelogram on the right. And they are very important in linear algebra.

And here's my favorite way to represent a linear transformation. For this particular same matrix as before, let's not look at the unit square we looked at, but instead at this small parallelogram formed by these four points. And I'll tell you soon how we obtained the parallelogram.

The parallelogram is formed by the point 0, 0, which as usual goes to the point 0, 0, the point 1, 0, which goes to 2, 0, the point 1, 1, which now goes to 3, 3, and the point 2, 1, which goes to 5, 3. And just as before, this parallelogram, which is a basis, gets sent to the larger parallelogram, which is another basis.

So this is a change of basis, and that defines where every point in the plane goes based on the two grids defined by the two bases. Now, here is what's interesting. Why do I prefer these bases and not the ones before?

It's because in this case, the two parallelograms have parallel sides. Notice that the vector 1, 0 here in blue gets sent to 2, 0, which is twice itself. And the vector 1, 1 in red gets sent to the vector 3, 3, which is three times itself.

Thus, the entire linear transformation is defined by the two directions and the two stretches. This may sound simple, but it's very important in linear algebra, especially when you have a very large and complicated matrix.

Now, everything here has a name, and the stem is the word eigen, which is German for own. The two vectors forming the basis are called the eigenvectors. The basis is called an eigenbasis. And the two quantities by which we stretch the eigenvectors are called the eigenvalues.

Now, there is even more eigen stuff. Notice one thing: every point in the line formed by the blue eigenvector gets sent to another point in this line. The line gets stretched by 2, but it gets sent to itself because if we stretch a line, you get the same line.

The same thing happens with the line formed by the other eigenvector. It gets stretched by 3, but it gets sent to itself. And these two lines are called eigenspaces.

And those are the only two lines through the origin that get sent to themselves. Any other line through the origin also gets sent to a line through the origin, but not itself.

Of course, if the matrix is the identity or a multiple of it, then every line through the origin gets sent to itself. But for the other cases, that's not what happens, and so therefore, the other lines are not eigenspaces.

And now that we've seen the pretty pictures, let's come back to the formulas. When we multiply the matrix by the red eigenvector 1, 1, we get 3 times that eigenvector. And when we multiply it by the blue eigenvector 1, 0, we get twice that eigenvector.

And in general, if the matrix is called A and the eigenvectors are called v1 and v2, the eigenvalues are called lambda1 and lambda2, and the equations are: A v1 = lambda1 v1, A v2 = lambda2 v2, where these are the eigenvectors and these are the eigenvalues.

Now, here is something that you may have already figured out, but it deserves a special mention. The eigenvectors and eigenvalues define the entire transformation very nicely. For example, consider this point over here, and let's see where the transformation sends it.

Let's look at this parallelogram over here, which is also an eigenbasis, even though it's not the original one, which was the small unit parallelogram. The blue vector gets sent to twice itself, and the red vector gets sent to three times itself.

Therefore, the green point gets sent to this point over here, completing the parallelogram. And this is why the eigenbasis is so useful, because a linear transformation defined by a matrix can be complicated, but this expresses it as simply two stretchings in two particular directions.

Now, you may be wondering how to find these eigenvectors. The entire procedure is purely algebraic, and it involves factoring a polynomial that comes out of the determinant, called the characteristic polynomial, and then solving a system of linear equations.

This is worthy of another video, but for now, I will show you my favorite way of finding them, which is using wolframalpha.com. You simply type "eigenvalues of" the matrix, and you get everything there.

So here it shows us that you have the eigenvector 1, 1, which is this one, the eigenvector 1, 0, which is this one, and the eigenvalues are 3, which corresponds to the scaling by 3, and 2, which corresponds to the scaling by 2. And thus, the matrix that changes this basis into this one is expressed as a change of basis.

Now, the million-dollar question: can all these linear transformations be expressed in the way we did before with an eigenbasis and a change of basis? Well, not all the time. Unfortunately, there are some special cases that are not so nice, and we'll get them out of the way.

In particular, not every transformation sends the plane to the plane. Some of them crunch it into something smaller, and they are called singular transformations.

One singular transformation is the one that sends everything to 0. Technically, everything here is an eigenvector with eigenvalue 0, but that transformation is not that interesting.

Another singular transformation is the one that sends the entire plane to a single line, such as this one. In this case, we only have one eigenvector with non-zero eigenvalue, which is this one, and then there's some other eigenvector which gets sent to 0, and so that one has 0 eigenvalues.

Now, among the other transformations, namely the non-singular ones, which actually do send the plane to the entire plane, there are three fundamental things that could happen.

The first one is when the plane gets stretched in some direction, such as this one over here, for example, we get stretched in the horizontal direction. The second one is when the plane gets rotated, for example, here we have a rotation of 90 degrees.

And the third one is when the plane gets sheared, which is this strange transformation in which you pretty much grab the plane as a piece of paper and simultaneously push the top and the bottom in different directions. And every non-singular linear transformation is some combination of these three. So let's study the eigenvectors of these three transformations.

For the stretches, which are the ones we've already seen, the eigenvectors are precisely those that line up with the directions in which we are stretching. For example, in here, we are stretching the horizontal axis by 2 and the vertical axis by a half, and those are the two vectors that remain parallel to themselves, so this one has two eigenvectors. And remember, these stretches can be in any diagonal direction.

For the rotation, it's a bit different. Notice that there is...

## Part 02 (10:00–19:18)

No vector here that gets sent to a parallel vector because everything gets rotated. Does that mean this matrix has no eigenvectors? Well, it does, only that these are imaginary numbers. So we won't deal with them right now.

This is material for another future video. But for now, just know that they do have eigenvectors even if they are complex numbers. And the final one is a strange one, the shear.

Notice that for this particular one, the blue horizontal vector gets sent to itself and thus is an eigenvector. However, no other vector gets sent to a parallel vector since every other vector that is not the horizontal one gets rotated. This means that the matrix only has one eigenvector.

What do we do? Well, there is another hidden eigenvector-ish, which we call a generalized eigenvector. And that's what I'll talk about for the rest of the video.

These shear matrices are so strange that they actually have a name, defective matrices. I think defective matrices is a bit harsh name for them because they do deserve some shame since they make life a little more difficult. However, if we look at things from the right angle, they don't make life that difficult. So that's what we're going to see next.

So now let's look at a defective matrix, for example, this one with entries 3, -1, 1, 1. If we look at WolframAlpha, it gives us an eigenvector 1 1 with corresponding eigenvalue 2, which means it gets stretched by 2, and a strange generalized eigenvector 1 0 with, again, generalized eigenvalue 2. Does that mean that this gets stretched by 2? Well, not exactly, but almost.

To understand this, let's look at the eigenbasis. So the four points in this parallelogram are these, and recall that the matrix sends the vector x y to 3x - y, x + y. So 0 0, as usual, goes to 0 0, 1 0 to 3 1, 1 1 to 2 2, and 2 1 to 5 3.

So this is where the resulting basis goes. But now let's look at the eigenvectors. The eigenvector is 1 1, which gets sent to twice itself, as usual, and so that means that this is a stretch by 2 in the direction of the eigenvector.

Now, the generalized eigenvector is 1 0, which would love to send it to twice itself, but that's not the case. It gets sent to 3 1. But that's not that far.

What do we need to get from 2 0 to 3 1? Well, we need exactly the first eigenvector. So that's what happens.

The generalized eigenvector doesn't get sent to itself times 2. It gets sent to itself times 2 plus the first eigenvector, which means that this corresponds to a stretch by 2 in the direction of the generalized eigenvector followed by a shear in the direction of the first eigenvector. So the transformation corresponds to a stretch and a shear, and that's what a generalized eigenvector does.

And this is where the bases go. Now, mathematically, here's what happens. When we multiply the matrix by the red eigenvector, we get twice that red eigenvector, as usual.

And when we multiply the matrix by the blue generalized eigenvector, we get twice itself plus the first eigenvector. So there's the stretch, and there's the shear. And this is where the bases goes, and the math goes like this.

Av1 is lambda v1, that's the eigenvector, and Av2 equals lambda v2 plus v1, that's the generalized eigenvector. So again, v1 is the eigenvector, v2 is the generalized eigenvector. They both correspond to a stretch by lambda, and then v1 corresponds to a shear in the direction of v1.

Notice one special thing, and is that they both have the same eigenvalue, and this is always the case. The generalized eigenvector always has the same eigenvalue as the eigenvector it corresponds to. The reason is quite subtle.

Long story short, if they had a different eigenvalue, then we can find a second genuine eigenvector that actually gets sent to a multiple of itself. The details of this are long enough and probably for a separate video, but in the meantime, I encourage you to explore that by yourself.

And now, what happens to the eigenspaces? In other words, what is a generalized eigenspace? Well, to understand this, let's look again using parallel lines.

Here is the line corresponding to the red eigenvector, which, as we know, is an eigenspace because it gets sent to itself. Now, here's the line corresponding to the blue generalized eigenvector, which is not an eigenspace because it's not going to be sent to itself, it's going to be rotated. So we're going to find something that gets sent to itself, and that's going to be our generalized eigenspace.

And for that, let's look at the parallel lines to these two. Now, the first equation, Av1 is lambda 1 v1, tells us that there's a stretch in the direction of the red eigenvector, which means that the blue lines are going to be spaced away twice as far as the original blue line.

The second equation tells us that there's a stretch in the direction of the blue generalized eigenvector, which means that these red lines get sent twice as far away from the origin from the original red line. And the basis becomes this one so far, but we're still not done because we still have this v1 over here, which gives us a shear in the direction of the first eigenvector.

So this shear, to understand it well, we're going to look at some dots here, and the shear is precisely this transformation. Now, this transformation leaves the original red line by itself, but it seems like it doesn't keep anything else and send it to itself.

Well, it's kind of cheating, but the generalized eigenspace is the entire plane. The entire plane gets sent to itself. Let me be a bit more clear.

So the first eigenspace is this one, the one that got sent to itself. Now, for the rest, consider the entire plane is formed by all these blue lines, and so this plane gets stretched in the way that if you take your hands and pull this sheet of paper towards the side, you stretch it, and then it also gets sheared because it gets sent to this basis.

And when you shear the plane, you still get the same thing. These blue lines remain the same after you do the shear. So the eigenspace is the entire plane.

That's the generalized eigenspace. The entire plane gets sent to itself, so now we have an eigenspace and a generalized eigenspace. Now, as I had said, it looks like cheating, but if you have higher-dimensional things, it's okay.

Imagine that we have a 3x3 matrix, for example, that now sends the entire three-dimensional space to itself. So if we had, for example, an eigenvector like this and a generalized eigenvector like this, then the eigenspace is this line that gets sent to itself, and the generalized eigenspace is a plane that goes through both of them that actually gets sent to itself, and it goes through the origin.

And now, this is not trivial because we do have a plane inside the three-dimensional space that gets sent to itself. And this goes on as you keep increasing the dimensions. You may have a three-dimensional generalized eigenspace that gets sent to itself, and so on and so on.

So in, in general, what happens is that generalized eigenspace is the space of the smallest dimension that the transformation sends to itself. So if it happens to be a line, that's fantastic, but in defective matrix cases, you're going to have a line and then a plane and then a space, and so on. And this is it.

That's what generalized eigenspaces are. So this video wouldn't have been possible without my math genius friends who helped me understand this topic. They are Martha Yip, who is a professor at the University of Kentucky, and Alejandro Morales, who is a professor at the University of Massachusetts.

And if you like my explanations, I encourage you to take a look at my book, Grokking Machine Learning, in which I talk about machine learning in very simple terms, using pictures and examples and lots of code and real datasets. Here is a 40% discount code for you to use if you'd like to buy it. You can check the link and the code underneath in the comments.

And that's it. So if you like this video, I invite you to subscribe to the channel for more content, and also please hit like and share it and comment on it. I love reading the comments, in particular if you have topics you'd like to see, feel free to suggest them over there.

You can also tweet at me. My Twitter handle is @luislikesmath, and you can also view all these videos and other information in my page, Serrano.Academy. So that's all, folks. Thank you for your attention, and see you in the next video.
