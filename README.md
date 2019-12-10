# Traveling Salesman Problem (TSP)

This is a problem how to find the shortest path between the given points and return to your start point.

This problem becomes to demanding on proccesing power for pure "brute force" method.

In this project I tried to reduce the path to minimum, while time needed to calculate the path remains reasonable.

__________________________________________________
50.000 points got processed in 33min on ryzen5 1600+ procesor, while it took 1h 11min on my intel i3 2330m procesor (this include time for generating points).

There are two start sort algorithms. One is randomly based and gives quite good results, but doesn't reproduse same results for the same set of points (good for large arrays of points, but bad for smaller arrays of points).

The code DOES NOT sort the points into the perfect position for the shortest path, but I think it is in the 20% error limits (more testing needed).
Also more costumatiosation needed around start position (first and last point in the list behaves a bit differently in some algorithms).

programing language: python
