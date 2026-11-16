# Clustering: K-means and Hierarchical 전체 오디오 전사본

- **원본 영상**: https://www.youtube.com/watch?v=QXOkPvFM6NU (약 17:22)
- **채널**: Luis Serrano Academy
- **전사 방식**: gemini-3.5-flash (Vertex AI API), 원어 축어 전사
- **총 세그먼트**: 2개 파트 (각 약 10분)

---

## Part 01 (00:00–10:00)

Hello, I'm Luis Serrano, and this video is about clustering. We're going to learn two very important algorithms: K-means clustering and hierarchical clustering.

Clustering is a type of unsupervised learning, and it basically consists on grouping data. So if your data looks like it's all over the place, the algorithm will say, "Okay, you got a group here, you got a group here, a group here, etc." So let's take a look.

So let's start with an application. The application's going to be in marketing, in particular, in customer segmentation. And the situation is the following: we have an app and we want to market this app.

We've looked at our budget, and we can actually make three marketing strategies. So that's our goal, to make three marketing strategies. So the idea is to look at their potential customer base and to split it into three well-defined groups.

When we look at the customer base, we realize that we have two types of information. We have their age in years, and we have their engagement with a certain page in number of days per week. So one of the columns is demographic, age, and the other one is behavioral, which is engagement with the page.

And the engagement of the page can be a number from zero to seven since it's in days per week. So we look at the potential customer base, and this is it. There's eight people with their age and their engagement.

So by looking at this list of people, what groups can you come up with? Let's take a look. Feel free to pause the video and think about it for a minute.

So just by eyeballing, I can think that, for example, these two people are similar. They have similar ages and similar engagements. Maybe I could put those in the same group.

I don't know, maybe these two are similar as well. We can take a while and we can actually write them down and maybe come up with groups, but there's got to be something easier. Or at least something mechanical that computer can do automatically.

So one of the first things to do with data is to plot it. So let's let's plot it in some way. Let's plot it like this.

So in the horizontal axis, we put the age, and in the vertical axis, we put the engagement. And now it looks more clear, right? There are three groups.

Here is one, here is another one, and here is the other one. So that's our three marketing strategies.

The first one is for people around the age of 20 who are have a low engagement with the page, two, three, and four days a week. Then strategy two, for people that are around their late 30s and early 40s and high engagement with the page. And then the last one is for people that are around their 50s and very low engagement with the page.

And that is pretty much what clustering is. Basically, if our data looks like it's a bunch of points like this, then a clustering algorithm will say, "Hey, you know what? I don't know much about your data, but I can tell you that it's kind of split into these groups."

So what we learn in this video is how to do this clustering. How does the computer identify these groups? Because for a human, in this small case, it's easy, but for a computer, it's not.

And in particular, if you have many, many, many points and and many columns or many dimensions, it's not easy. So in this video, I'm going to show you two important methods. The first one is called K-means clustering, and the second one is called hierarchical clustering.

So let's start with K-means clustering. And the question is, how does the computer look at this, points all over the place, and figure out that they are forming these groups?

So when I try to imagine points in the plane, I just imagine places in a city and trying to put pizza parlors. So let's say that we are the owners of this pizza place, and we want to put three pizza parlors in this city. And what we want to do is we want to put them in such a way that we serve our clientele in the best possible way.

So we look at our clientele, and it looks like this. This is where they live. So what we want to do is locate three pizza parlors in the best possible places that will serve our clientele.

So if you take a look at it, you can come up with three places, right? It seems like we should have a red one that serves the red points, a blue one that serves the blue points, and a yellow one that serves the yellow points. However, for human, this is easy, but a computer has a harder time.

So what the computer's going to do is, like in most things in machine learning, start at a random spot and start getting better and better. So how does it start? Well, first, it locates three random points and puts three pizza parlors there.

And now what we're going to do is a series of slightly obvious logical statements that, when put together, will get us to a better place. So the first logical statement is, it seems like if we have the pizza parlors in these places, everyone should go to the closest one to them. That makes sense, right?

So we're going to plot all the people that go to the red, to the blue, and to the yellow pizza parlor. Basically, you go to the one that is the closest.

So here's another logical statement. If all the red people go to the red pizza parlor, it would make sense to put it in the center of all those houses, right? And the same thing with the blue and with the yellow. Basically, you move the pizza parlor to the center of the houses that it's serving.

So the yellow one will serve these houses over here, the blue one is serving these houses over here, and the red one is serving these houses over here. So we move each one of them to the center of the houses that they're serving.

And now let's apply the first logical statement again. We have three pizza parlors, and everyone's going to go to the one that is closest to them. So some things change, right?

Because let's take a look at these three blue points. Well, now they're closer to the yellow pizza parlor. So these people move, and now they're going to go to the other, to the yellow pizza parlor.

What about these two red points over here? Well, now they're closer to the blue pizza parlor, so they're going to start going to the blue pizza parlor now.

So let's go back to the other logical statement, which is that the best location for a pizza parlor is the center of the houses that it serves. So we move every pizza parlor to the center of the houses that it serves.

And again, let's go back to the first logical statement, which is, every person goes to the closest pizza parlor. So if you look at these points over here, they are red, but now they're much closer to the blue pizza parlor, so they move to the blue pizza parlor now.

And you can see that we're getting better and better, right? Because now, when we apply the other statement, which is, every pizza parlor should be at the center of the houses that it serves, then now we move everything to the center of the houses where it serves, and we're done.

So that's pretty simple, right? And a computer can do it because a computer can find the center of a bunch of points by just averaging the coordinates, and can also determine if a point is closer to one center than to the other one because it simply just applies the Pythagorean theorem, or the distance formula, and can compare numbers. These are these are decisions that a computer can make very easily.

So we managed to think like a computer and not like a human, which is basically the main idea in machine learning. So this is the K-means clustering algorithm.

Now, you may be noticing that we took one decision that seemed to be taken by a human and not by a computer, right? We decided that there were three clusters. But as we said, that's hard for a computer to decide.

A human can see it, but a computer can't. So here's a question: how do we know how many clusters to pick? And for this, we have a few methods, but I'm going to show you what's called the elbow method.

So the elbow method basically says, try a bunch of numbers, and then be a little smart on how to pick the best one. So let's try with one cluster. We can do this algorithm with only one cluster, and we're probably going to get something like this: every house go to the same pizza parlor.

Then we can run it with two clusters. And you can start seeing that this algorithm actually depends on where the original points start. Sometimes it works, sometimes it doesn't, sometimes it gives you different answers. So let's say we try two clusters and we got this.

Then we try three clusters, and we got the solution that we got. Then we try with four clusters, and let's say we got this.

With five clusters, and we got this, and with six clusters, and we got this. So by eyeballing this, we can see that the best solution is with three clusters.

But again, we need to teach the computer how to find the three clusters. We need to think like a computer, so we can't rationalize things. We have to do things like measuring distances, comparing numbers, averaging coordinates, etc.

So with those tools, how do we find that three is the best? Well, what we need is a measure of how good is one clustering.

And maybe the following measure will make sense. Basically, what we're going to do is we're going to think of the diameter of a clustering. And the diameter is simply going to be the largest possible distance between two points of the same color.

That basically tells us how big each group is in a in a rough way. So let's look at the first one-cluster solution. The longest possible distance between two points of the same color is this one.

Those two red points are the farthest apart. So that distance is is in a way telling us how good is that clustering. Let's do it with two clusters.

So the longest distance, let's say, is this distance over here. That tells us how good the clustering is with two clusters. Now let's do it with three clusters, and let's say that the longest distance is this one over here.

Again, with four clusters, the longest distance is this one. With five clusters, the longest distance is this one, and with six clusters, is this one.

## Part 02 (10:00–17:22)

Now, I just eyeballed these distances, so if you think there's another one, you may be correct. But conceptually, what we're trying to do is to define the next method, which is the elbow method. So, what we're going to do is we take all these distances and we graph them in the following way.

On the horizontal axis, we're going to put the number of clusters: 1, 2, 3, 4, 5, and 6. And on the vertical axis, we're going to graph the diameter, so we get the following points. And now, what we do is we join these points.

And now, this is somewhere where a human can intervene. A human can look at this graph and say, "Okay, you know what? I want the elbow to be here." There are also some automatic methods to do this, but at some point in the machine learning algorithm, it's good to actually have a consistency check. This is because you may have an idea of how many clusters you want, or you may have an idea of how many clusters you would like to have, or a maximum or a minimum.

So anyway, in some way or another, we figure out that the number is three. Another thing that's important is that this elbow method is very easy for a human. If our data has many, many columns, we're looking at points in very high dimensions. However, the elbow method, the graph, is always going to be two-dimensional.

So that's it. That's how we decided that three clusters are the best. And that is the K-means clustering algorithm in a nutshell.

Okay, so now let's go to our second method, which is hierarchical clustering. And we're going to do a similar problem, except now with this dataset. We're going to find the clustering into—let's see how many groups we can find.

So, another way to do it is the following. Let's think about this. Let's think of the two closest points. It would make sense to say that these two points that are the closest will belong to the same group. Maybe yes, maybe no, but it's a sensible thing to ask, right?

So, let's go on that statement. Let's say these are the two closest points. So, these two are going to be part of the same group.

And now, what are the next two closest points? Let's say it's these two, so these two belong in a group. And we're going to keep going in this direction.

The two closest points are these ones, so these two belong to the same group. The two closest points are these ones, so now what do we do? Well, we just join the two groups, so now it becomes a group of three.

The two closest points are these two, so they join like this. The two closest points after that are these two, so we join the two groups—the group of two and the group of three into a group of five.

And then the next pair of points that are the closest are these two, so we're going to join them. But let's say that's just too big, so we have maybe a measure of how much is too far. So, we stop here.

And that's it. That's hierarchical clustering. It's pretty simple, right?

Now again, there seems to be a human decision here, right? Why did we decide on that being the distance? Or, for example, why did we decide on two being the number of clusters? So, we can make this decision.

But let's actually look at an educated way to make this decision. So, let's answer this question: how do we decide the distance or the number of clusters?

So, a way to do it is by building something called a dendrogram. What we're going to do is the following. We're going to put our points in a row over here, one up to eight. And then, in the vertical axis, we're going to graph the distance.

And I'm going to show you how. Let's pick the closest two points, which are four and five. So, we join four and five, and we join them over here.

And this is not up to scale, but the height of that little curved line between four and five, let's say it's the distance between four and five. So, we join these two, and then we go to the next two, which is one and two. And so, we're going to join one and two here, and we're going to join them in the dendrogram in the right.

And again, assume that that height of that little curved line is the distance between one and two. Now, we join the next pair, which is six and seven, so we join six and seven, and again, the height is the distance. We keep going: six and eight.

So now, we're going to join six and eight. How do we join them? Well, we join them like this: the group of six-seven and the group of eight.

And the next group is going to be three and four-five, so they get joined like this. And now, the next group is going to be two and three, so we join the group corresponding to two and the group corresponding to three in the dendrogram. And notice that the dendrogram goes up because these distances increase. So, every time we make a new join, it's higher than the previous ones.

The next ones that we join are three and six, so we end up joining these two trees like that. And so, that's it. We have a lot of information about this set in this dendrogram.

And now, how do we decide where to cut? Well, let's say we cut over here at a certain distance. And that gives us two clusters, which are this one (one, two, three, four, and five) and this one, which is six, seven, and eight.

So, notice that we made the decision on cutting based on how much of a distance is too far away, or how many clusters do we want to obtain. Let's say that we want to obtain four clusters, so we cut at this distance over here, which gives us four clusters: the cluster formed by one and two, the one formed by three by itself, the one formed by four and five, and the one formed by six, seven, and eight.

So again, these decisions are taken by a human, but think about it again. Let's say we have billions of points. And let's say that they live in a thousand-dimensional space. It doesn't matter; the dendrogram is still a two-dimensional figure, and we can easily make decisions on it.

So again, a combination of a computer algorithm and some smart human decisions, it would give us the best clustering. And that's it. That's hierarchical clustering in a nutshell.

Clustering has some very interesting applications, and let me mention some of them. In things like genetics or evolutionary biology, the genome carries a lot of information about a species, and if you manage to cluster them, you get to understand a lot about species and how they evolved into what they are right now.

Other things like recommender systems use a lot of clustering. For example, the way you may have got this video recommended was using several methods that include clustering users, grouping them into similar users. So, maybe somebody very similar to you watched this video, and that's why you got it recommended.

And that brings us to social networks, which is another place where clustering is used a lot. In a very similar example than the one we did, social networks use these methods to group users into certain similar groups based on demographics, based on behavior, and then be able to target information to them that they want to see, or suggest you friends that are similar to you, etc.

So, that's all for now. Thank you very much for your attention. As usual, if you would like to see some more of this content, please subscribe or hit like. Feel free to share it with your friends, and feel free to throw in a comment and tell me what you think of the video, or if you have any suggestions for other videos you'd like to see. And my Twitter handle is @luislikesmath if you'd like to tweet at me. So, thanks again, and see you in the next video.
