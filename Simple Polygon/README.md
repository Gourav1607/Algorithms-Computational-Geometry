# Simple Polygon

On 2D space, taking the (x, y) coordinates for N random points as input, draw the polygonal chains first and save the visualization as an image file.

Then draw the simple polygon on the screen and fill different regions (interior and exterior) with different fillcolors to identify.

Save the visualization as an image file.

<hr style="border:2px solid gray"> </hr>

**Solution Description**

- Input: N - Number of Vertices for the polygon.
- Randomly initialize N co-ordinates (Range 0-800).
- Draw a white RGB image of SIZE × SIZE × 3 (SIZE = 800).
- Take Center Point of all Vertices as Reference (refX, refY ).
- Calculate slope of each point from this point.
- Sort the Vertices based on their slope (Increasing Order).
- Connect these sorted vertices in this order.
- Connect the last vertex to the first Vertex.
- Flood Fill the polygon using Center as Seed.
- Flood Fill the outer area using (0, 0) as Seed.