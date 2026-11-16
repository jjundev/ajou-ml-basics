# The covariance matrix 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=WBlnwvjfMtQ (약 13:56)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 2개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, my name is Luis Serrano and this video is about the covariance matrix. For a data set, the covariance matrix tells us a lot of information about it. So let's look at it. But first, let's start with other measures.

The first one is the center of mass. The center of mass is the point where you would balance this data set if every point was an equal weight. We also call it the mean or the average.

Then we also have the X variance, which tells us how much this data set is spread in the horizontal direction. And the Y variance, which tells us how much the data set is spread in the vertical direction. As you can see, this data set is a little more spread in the horizontal than in the vertical direction, so we expect this X variance to be higher than its Y variance. However, that doesn't tell us everything because the data set could be an oval or a circle or different things.

Something that will tell us a bit more about the shape of the data set is the covariance. In this case, it would tell us it's elongated and it points in this diagonal direction. So that tells us a lot about the shape of our data set, and then we can do things like fit a Gaussian to it, etc.

So we have something called the covariance matrix, which encompasses a lot of this information, and it's simply the matrix formed by the variance in the X direction, the variance in the Y direction that goes in the diagonal, and the covariance which goes in the places outside the diagonal. Now, this data set is two-dimensional, so the covariance matrix is 2 by 2, but if we had, for example, a 100-dimensional data set, then we would have a 100 by 100 covariance matrix.

Now, in some cases, we're going to have points that are weighted, so we don't have the entire point in the data set, but we have half of a point, or a third of a point, or a tenth of a point. We can still find the center of mass. This time it's going to be a little more up and to the right because the heavy points are up and to the right.

We still have an X variance, and we still have a Y variance, and we still have a covariance. So in this video, I'll teach you how to calculate it. This is useful in algorithms like Gaussian mixture models, for example, which uses portions of points, etc. And we can also find the shape of this data set.

So let's start with the average, and let's start with a very small data set, these four points. So what is the center of mass? Well, the center of mass, or average, or mean, is right here.

What are the coordinates? Well, first we look at the first coordinate, the X coordinate, and take the average of those four, so it's 1 plus 3 plus 3 plus 5 divided by 4. And then let's do the same thing with the second coordinate, the Y coordinate, and we get this point.

If we summarize it, we get the point 3, 2. So 3, 2 is the center of mass of this data set, and that's expected given the points.

Now, what we normally want to do in order to calculate the covariance matrix, which is much easier, is that we look at the point 0, 0 and we take the data set and move the center to the point 0, 0, recalculating every weight. So we subtract 3 from every X coordinate and 2 from every Y coordinate. So we end up with this new data set. We can look at it over here.

And now I'm going to teach you how to find the X variance, so a measure of how spread in the horizontal direction is this data set. For this, we only need to look at the first coordinate, which is the X coordinate, and we simply take the average of the squares of these variables. Why the squares? Because we want to check how far it is from the origin, so we don't want a positive 2 to negate a negative 2.

We want them both to add because the farther points are in the X direction, the more variance there is, and that's why we take the average of the squares. In this case, it's 1/4 of 2 squared plus 0 squared plus 0 squared plus minus 2 squared, which is 2.

Now, to find the Y variance, it's exactly the same thing. So now we take the second coordinate, so the Y coordinate, and we take the average of the squares, so 1/4 times minus 1 squared plus minus 1 squared plus 1 squared plus 1 squared. And that is equal to 1.

So let's look at some examples of data sets. This one over here is pretty centered, so we expect it to have a small X variance and a small Y variance. This one over here is pretty spread out but only in the horizontal direction, so we expect it to have a large X variance and a small Y variance.

This one over here is pretty centered in the horizontal direction but quite spread out in the vertical direction, so we expect it to have a small X variance but a large Y variance. And this one is spread out in both directions, so we expect it to have a large X variance and a large Y variance.

However, X variance and Y variance don't tell us the entire story. For example, let's take a look at these two data sets. Notice that if we calculate the X and Y variance, they have the exact same X and Y variance, which is 2 and 1.

However, they are very different. One is sort of belonging to one diagonal, the other one is belonging to the other diagonal. So how do we tell these apart? And the way we're going to tell these apart is with something called the covariance.

So how would you tell these two sets apart? Is there any equation, other than sum of squares, which we know it doesn't work, that you would use to tell them apart? Well, one way is to look at these two points.

In the left, they look like they form a diagonal that goes up and to the left, and on the right, it's the opposite diagonal. So what equation would work? Feel free to pause the video and think about it. And I'll tell you the answer: it's the product of the two coordinates.

Take a look at this: minus 2 times minus 1 is 2, and 2 times minus 1 is minus 2, that's at the left, whereas at the right, they are 2 times 1 equals 2 and minus 2 times minus 1 equals again 2. So on the left, the points in this backwards diagonal have the property that the product of the coordinates is negative, whereas the ones on the right, the product of the coordinates is positive.

So all we have to do is calculate the product of coordinates for all the other points, and the covariance is going to be the average of all the products of coordinates. So on the left, it's going to be the average of minus 2, 0, 0, and minus 2, which is minus 1. And on the right, it's going to be the average of 2, 0, 0, and 2, which is 1.

So that is what's going to tell them apart, and that is covariance. Just out of curiosity, let's calculate the covariance of this data set. What do you think it's going to be?

So this data set is kind of centered, it doesn't skew in any of the two diagonals, so we would expect it to be something small or zero. Let's see. The product of coordinates are these, and they're always zero, so the average of four zeros is zero. So this set has covariance zero.

So in general, if you have a data set that is like this, like the backwards diagonal, well, you would say that it has a negative covariance. If it's something like this that doesn't skew in any diagonal, it probably has a zero covariance, or at least a very small number. And these ones like this that go in the positive diagonal have positive covariance.

If you're thinking correlation, covariance and correlation are very similar. They're not the exact same formula, but very similar. So you would say that if there's a variable in the X-axis and a variable in the Y-axis, then on the graph on the left, they're negatively correlated, on the graph in the middle, they're not correlated, or independent perhaps, and in the graph on the right, they are positively correlated because as X increases, Y also increases.

So let's look at the actual formulas for these quantities that we learned. So if our data set is this, we're going to call the points x_i, y_i for i equals 1 to n because we have n points in our data set. So the mean, or the center of mass, is two numbers, mu_x and mu_y, and each one is just the average of the x_i and the average of the y_i.

Now, the X variance, well, all we have to do is subtract to every x the mu_x, which is the average of the X coordinates, and take the average of those squares. Same thing for the Y variance, to everything we subtract mu_y, which is the mean in the Y direction, in the vertical direction, and then take the square of everything, and then take the average.

And the covariance is simply the average of the products of x_i minus mu_x and y_i minus mu_y. Finally, the covariance matrix is the one that in the main diagonal has all the variances, and outside of the main diagonal, it has the covariances.

Now, that is almost the whole story, but let's remember that we talked at the beginning about data sets where the points appear as fractions, so not the whole point appears, but maybe 10% of it, or half of it, or 80%, etc. For those, we can still calculate the average and the covariance matrix. And we do it in the exact same way, except now we weight the points.

So let's look at it in the example that we saw at the beginning. So for these four points, the mean, or the average, or the center of mass, is calculated this way. And notice that I took the average in a different way, I didn't divide by 4, but I divided by 1 plus 1 plus 1 plus 1, so it's one unit for each one of the points, and you'll see why.

But now let's say we have a weighted data set. So instead of the bottom left point, we have a third of that point. So what happens now with...

## Part 02 (10:00–13:56)

The center of mass, well, now it's not going to be where it used to be, now it's going to be a little more to the right and up. How do we calculate it? Well, we just add a 1/3 in the corresponding weight and in the bottom in the corresponding unit. So we get 3.4, 2.2, so that's our new average.

The next thing we do is we're going to center this data set, so we are going to subtract to every x coordinate 3.4 and to every y coordinate 2.2. This is so that we're centering it in the point 0 0, and that's going to make it much easier for us to calculate the variance, x variance, y variance, and the covariance.

So let's start by calculating the x variance. So normally we would do this sum, the sum of squares of x coordinates divided by 4, which is the number of points, so the average. However, the point at the bottom left is only there 1/3.

It's not fully there, so we have to multiply its corresponding term by 1/3 squared. The reason the square is because in the formula of the variance you are adding a bunch of squares. So we calculate this and we get 0.88 for the new x variance.

Same thing for the y variance. To its corresponding term in the average of squares of y coordinates, we multiply by 1/3 squared and we get 0.72. Notice that both the x variance and the y variance are smaller than the previous one.

For the covariance, same thing. We are taking the average of the product of the coordinates, but to the corresponding term of that point we multiply by 1/3 squared, so we get 0.64 as our covariance.

And if you like formulas, here they are. Here are our points x1 y1, x2 y2, all the way to xn yn, and each point comes with a corresponding weight. That is a number between 0 and 1 that tells us how much of the point is in the data set, so if it is, for example, 30%, then alpha 1 is 0.3.

Now, for the mean we calculate it just like before, except except instead of dividing by n, we divide by the sum of alpha i. And each xi and yi gets weighted by alpha i, so it's just a weighted average.

X variance, same thing, but it's now weighted by the squares, so we divide by the sum of alpha i squared and each term gets multiplied by alpha i squared. Same thing for the y variance and same thing for the covariance.

And now we have our covariance matrix and this is pretty much it. This tells us a lot about the data set if the data set is weighted by some percentages.

So thank you very much for your attention. I'd like to remind you that I have a book called Grokking Machine Learning and in this book I explain supervised learning, most of the algorithms and several techniques for applying machine learning to many real life problems with code in Python. You can take a look at it in this web page which is also linked in the comments and you can use a discount code called serranoYT for a 40% discount in the price.

So thank you very much for your attention. If you liked this video, please subscribe for more content or hit like or share it amongst your friends. And I love when you comment, so please give me a comment, tell me about what you liked, what you didn't.

And also if you have any ideas for future videos, feel free to put them in the comments. Many videos have come out as an idea that someone suggested in the comments. You can also tweet at me, my handle is @luislikesmath.

And if you'd like to see a repository of all this information, all these videos, the book, blog posts, etc., please take a look at this web page, it's serrano.academy. So that's all for today. Thank you very much and see you in the next video.
