# Lecture07 Warm-Up: Gaussian Mixture Models (Luis Serrano) 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=q71Niz856KE (약 17분 27초)
- **출처**: Lecture07_Density_Estimation_Part1.pdf 3쪽 Warm-Up 지정 영상
- **전사 방식**: Gemini 2.5 Flash (Vertex AI API), 영어 원문 축어 전사
- **총 세그먼트**: 2개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, my name is Luis Serrano, and this video is about Gaussian Mixture Models. Gaussian Mixture Models are very useful clustering models. Clustering has many applications, including audio classification, where they are used for telling sounds apart.

For example, telling different instruments apart in a song, or telling your voice apart from background noise when you talk to your voice assistant. Another application is document classification, so if you have a large collection of documents, you can use it to separate different documents by topic. Say the sports ones from the science ones, and the politics ones, etcetera.

Another very useful application is image segmentation, for example, when self-driving cars see an image that they want to separate into pedestrians, road, road signs, other cars, etcetera.

In short, the clustering problem is the following: we have a data set of points, and with luck, they may seem like they are clustered into groups like this, very well defined. And we proceed to cluster them. So in this case, we see that we have the green cluster, the blue cluster, and the red cluster.

There are some very useful clustering algorithms such as K-means clustering and hierarchical clustering, and I explained them in detail in this video in my channel. You can find the link down in the comments.

In that other video, you can learn how to cluster data sets like this one. However, sometimes data sets are more complicated, like this one. In this data set, it looks like there are two clusters: this circle over here, and this line or elongated oval around here.

And these clusters seem to intersect with each other, which makes the problem very difficult for traditional clustering algorithms. Therefore, we need something different. Notice one thing, that in the previous clustering algorithms, each point belongs to exactly one cluster, either you are yellow or you are blue.

However, we can think of points belonging to both clusters at the same time. So we're moving from hard assignments to soft assignments, so from hard clustering to soft clustering. In hard clustering, every point belongs to a particular cluster and only that one. In soft clustering, however, a point can be 10% from one cluster, 25% from another one, etcetera.

So in this case, we have some points which are mostly blue, some which are mostly yellow, and some that belong to both clusters. And the algorithm we'll learn today is a very powerful and very popular soft clustering algorithm which will do this, and it's called the Gaussian Mixture Model.

And why is it called Gaussian Mixture Model? Well, because it is based on the Gaussian or normal distribution. This one over here is a Gaussian distribution in two variables, and this one is another one. They both look like bumps underneath a really large blanket.

But since we're drawing everything in the plane, we will draw them in the following way: from the top. So what we'll do is we draw the shadow. These purple curves here are the levels of the bump. So whenever I draw these concentric oval underneath, simply imagine a small mountain whose base is on the screen and whose top is facing you.

Now, these Gaussian distributions are defined in any number of dimensions, and so is our data. But for the purpose of clarity, in this video, I'll mostly be using two-dimensional data in a plane, so the Gaussians will look three-dimensional like this one on the plane, and as I said, we only look at their shadow or their projection.

So now we're ready to get into the Gaussian Mixture Model clustering algorithm, and this one has two major steps. The first one is to color points according to Gaussians. How do we do this? Well, this works the following way. Let's say we have two Gaussians, the yellow one and the blue one. Every point in the plane can be colored with two colors, yellow and blue, according to these two Gaussians. Before we get into details, let's draw some points over here.

Notice that the leftmost point mostly lives in the yellow mountain, so we'll color it yellow, or mostly yellow. As we move towards the right, we notice that the points are more half and half. This point here is half blue, half yellow, as it lives in between. And as we move towards the right, we go more and more blue. We get to this point in the right, which mostly lives in the blue mountain, so this one is colored almost all of it blue.

And we can do this for every point in the plane. The points that are close to the yellow mountain get mostly yellow, the points that are close to the blue mountain get mostly blue, and the points in between get some combination, some proportion between yellow and blue. But how do we do this more exactly? Well, we do it the following way.

And for illustration purposes, I'm going to do it in only one dimension, but you can imagine this as seeing it from the side, so you actually see the mountain from the side. So, let's say that now we have lines instead of planes, so Gaussian distributions in one dimension. We have the yellow one, called f(x), and the blue one, called g(x).

And now let's say we have three points in the line, and for each one, we're going to look at their distances to the yellow and the blue curve and take that ratio. So for the first point, we have the yellow distance is much larger than the blue distance, so this point is, let's say, 75% yellow, 25% blue, for example. The point in the middle is 50/50 because it's at that point where the blue and the yellow heights are the same. So this one is exactly half yellow, half blue. And the last point is mostly blue because there's very small distance in the yellow curve and a very large distance to the blue one. So therefore, this one is, say, 95% blue and 5% yellow.

So if you can imagine doing that for every point, we're coloring every point in the line. And if we can imagine doing this in two dimensions or in more dimensions, you're still coloring points in the plane based on the heights at each one of the mountains on top of that point.

And that was step one, which is how to color points based on the Gaussian. Now we're going to do step two, which is the last step, and it's the opposite: given some points, how to find the Gaussian. And we do it in the following way.

Let's say that these are our points. So the idea is to find the Gaussian that lifts them the most. If our points are like this, then the Gaussian would be this one. And in flatland, which is how we're looking at it from the top, they look like this.

So this is how we find the Gaussian. Let's say that these are our points. And I explain this in a lot more detail and with actual numbers and formulas in this video over here. It's called the covariance matrix video. You can find the link right here or in the description.

But here I'm going to give you the gist. So, the first thing we have to do is find the center of mass of these points. So imagine that these points were weights. Where would you put your finger to balance all these weights? Well, you would put it somewhere over here, in the mean, or the average, which is called mu. The way you calculate it is you take the x-coordinates and the average of all those, and that's the x-coordinate of the mean. And then you take the y-coordinates and take the average of them, and the that is the y-coordinate of your mean.

So that gives us good information about the data set, but we need some more. We need to know the x-variance, which is the horizontal spread. How how spread are these points in the horizontal direction? Are they all close or are they far apart? This is a number. Similarly, we have the y-variance, so tells us that tells us the spread in the vertical direction.

And that still doesn't tell us everything about the data set because we don't know if it looks like a rectangle or a or a line or an oval or a circle or in what direction it points. So for that, we have something called the covariance. So the covariance tells us a bit more about where the data is pointing.

And given the x-variance, the y-variance, and the covariance, we actually know a lot about how our data set looks like, and that helps us find the perfect Gaussian. How? Well, using sigma, the covariance matrix. Now, this data is in two dimensions, and so the covariance matrix is going to be a 2x2 matrix. But if your data is 100-dimensional, we're going to have a 100x100 matrix. So this is general. The covariance matrix looks like this: in the diagonal elements, we're going to have the variances, so the x-variance and the y-variance. And in the off-diagonal, we're going to have the corresponding covariances, so we're going to have covariance of x, y in particular. It's a symmetric matrix and it has some wonderful properties. And the way we find the Gaussian is simply by plugging it into this formula. So don't worry so much about this formula, just know that mu goes into this formula, sigma goes into this formula, and x, which is the point. So at every x, you plug it into this formula, and you get a number. That number is the height of the mountain at that point. So if you plug this formula, it's going to for every point, it's going to look like a bump, like that bump over an infinite blanket, which is the Gaussian distribution. This formula may look a little foreign, but this one may look more familiar if you have seen Gaussian or normal distributions in one dimension. This is the one-dimensional version.

However, we're still missing one thing. Here our points are all complete, but we may have a data set like this, where some points appear as a fraction. So you can see that some points in the bottom are half points, and this point at the left is a quarter point. So you may have 10% of a point or 97% of a point, any proportion. And for those data sets, you can still find a Gaussian that fits them well. You can still find the center of mass. This time the center of mass is not going to be in the same place as before because there are some heavy points in the top right that pull it. So it's going to be over here. We still have an x-variance, maybe it's going to be different. We still have a y-variance, and we still have a covariance. So given this,

## Part 02 (10:00–17:27)

we can build a covariance matrix and we can plug things in the formula and get a Gaussian. So the moral of the story is, if we have a bunch of points or a bunch of proportions of points, percentages of points, we can always fit the perfect Gaussian, so the perfect mountain that lifts these points the most and puts every other point in the in the bottom.

And so we're going to use this step in our algorithm.

So now that we've done the two steps, we are ready to build a Gaussian mixture model, and here it goes. We will do this to separate this data set into two clusters, as we saw at the beginning, which are the circle over here and the line where some points belong mostly to the circle, some belong mostly to the line, and some to both.

And the algorithm is the following. I wrote it over here in the corner. It simply consists of repeating step one and two many times.

So let me show you. First, we start with some random Gaussians. So let's start with one over here and one over here. So we have random mean, random covariance, random variances, and we draw the yellow and the blue Gaussian.

Next step is we're going to enter a loop. How long will this loop go? We'll figure it out later. For now, let's just run it many times and see what happens.

First, we go to step one, which is color points according to the Gaussian. So we learn how to color every point in the plane based on how close it is to these two Gaussians. Remember, we did it based on the heights.

So when we do that, we notice that these two points over here are much closer to the yellow Gaussian, so they belong to that yellow one. It looks like they're fully yellow, but think of them as a high percentage yellow and a very small percentage blue. These points over here, the same thing, they're mostly blue, and for all the other points, they're some combination of yellow and blue.

Now, these are sort of rough because I colored them eyeballing, but if you want to be exact, I encourage you to code this or to actually take a number example and and calculate it by hand, but this is mostly for illustration purposes.

So we've colored every single point in our data set according to these two Gaussians. So now what we do is we forget the Gaussians and we go to step two, and from the colors, we create new Gaussians.

So let's create two new Gaussians that fit the yellow portions and the blue portions. So let's only look at the yellow portions and let's fit a Gaussian. Again, this is something I eyeballed. So we have this Gaussian for the yellow points. Let's keep it in mind for a second.

And now let's look at the blue points or the blue portions, and we fit a Gaussian to those as well.

So now we forget about the colors, we have two Gaussians, and now with these two Gaussians, we are going to go back to step one and recolor our points.

So you see what's happening? First, we color points, then we move to the Gaussian, build Gaussians, then we forget about the Gaussians and we color points again. Then we forget about the colors and draw Gaussians again and go back and forth. This is just a back and forth process.

So, using these two Gaussians, we color points again. So these two are mostly yellow, these ones are mostly blue, and these ones are some sort of in between, some proportion of of blue and yellow.

Again, we go back to step two. We forget about the Gaussians, and using the colors, we are going to create two new Gaussians. So here are the ones for yellow, and here are the one for blue.

And now, with the new Gaussians, we're going to color the points. So we go back to step one.

And again, we color these points are mostly blue, these ones are mostly yellow, and these ones are some sort of mixture.

And now we go back to step two. But notice that now the algorithm sort of stays the same, it terminates, or at least it converges. It changes very little because it reached some sort of equilibrium.

Right? If we were to run it again, we get the same Gaussians or very similar Gaussians, and we get this run it again, we get the same colors or or very similar. So we have reached a ending point.

So we can say that this loop goes until the algorithm starts converging. Okay? So our algorithm says, while you're not converging, keep doing this.

And that's it. That's the entire algorithm for building a Gaussian mixture model.

Notice that we got the clusters that we're expecting. Now, this algorithm, like many others, is not exact. There was a bit of luck with our initial conditions and our data set, so we may not always reach the desired answer.

There are many heuristics that can help us. One is to run it several times and pick the best solutions we obtain. Another is to put good conditions on the original Gaussians, restrictions on the mean, variance, and covariances for them to be sort of random enough, but also good enough candidates.

So there are many ways to make this algorithm better. So here's a little summary of what we did. We started with our data set and we picked two random Gaussians.

Now, we use these two Gaussians to color every point in our data set as a combination of yellow and blue based on their position with respect to each one of the two Gaussians. Now, we forget about those two Gaussians because we'll find two new ones based on the colors that we've obtained.

So based on this color, we get two new better Gaussians. And now, we use these two Gaussians to recolor the entire data set. So forget about the colors and recolor them based on these two new Gaussians.

Now we forget about those two Gaussians again, and using the colors, we fit two new better Gaussians. And notice how these are much better than the previous ones. And finally, we use these two Gaussians to recolor our data set.

So notice that at each step, we're always doing step one and step two, which is color points, recalculate Gaussians, color points, recalculate Gaussians, and every time we're getting a little better and better until we get to a point where the Gaussians don't move very much, and that's where we're finished.

And that is all, folks. Thank you very much for your attention. I'd like to remind you that I have a book called Grokking Machine Learning that I invite you to take a look at.

In this book, I talk about the supervised learning algorithms in detail in a very conceptual way, using examples, et cetera, and there's also a lot of code in Python.

If you'd like to find it, go to this website over here, which is also in the description, and if you use the discount code SerranoYT, you can get a 40% discount on the book.

And if you enjoyed this video, please subscribe for more content. Please hit like, share amongst your friends, and feel free to comment. I love reading your comments, in particular, if you have ideas for any future videos you'd like to see, let me know in the comments.

Many times, I make a video that is comes out as a suggestion of something. So feel free. If you'd like to tweet at me, this is my Twitter handle, Luis Likes Math. And if you'd like to see all this information put together, I have this web page called Serrano.academy where you can find about the book, blog posts, videos, podcast interviews, et cetera.

So I invite you to take a look. Thank you very much for your attention, and see you in the next video.
