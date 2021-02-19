# Simple Polygon - Query

On 2D space, taking the (x, y) coordinates for N random points as input, draw the simple polygon on the screen. Let us call it as P.

Now take a random query point Q, Test and report whether that query point is inside on or outside the polygon P.
If the query point Q is inside P, then consider any triangle taking any one line segment (say RS) of P and Q as the third point of the triangle QRS.

Highlight that triangle QRS by filling it with a different color and calculate the area of that triangle.

<hr style="border:2px solid gray"> </hr>

**Solution Description**

- Input: N - Number of Vertices for the polygon.
- Create Simple Polygon using approach from Coding Project 01
- Generate query point Q randomly.
- Check if Q already lie on some line, if yes, then Q is on the polygon else continue with further steps.
- Initialize a counter to 0.
- Draw a ray from the point in right direction ad check for each point.
- If the current point of ray from Q lie on any line segment of Polygon, then increment the counter.
- Repeat until the ray reaches the end.
- If the counter is even, then Q is outside of Polygon.
- If the counter is odd, then Q is inside the Polygon.
- If Q is inside, then random edge is taken and two vectors are created.
- Half of cross product of these vectors will result in area of the triangle.
- Flood fill is used to color the triangle in green, using the center of triangle as the seed value.

**NOTE : Point is on line is confirmed if it is Black on Image.**