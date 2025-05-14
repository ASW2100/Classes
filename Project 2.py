"""
Name: Andrew Wolk
UIN: 668250903
I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC's
Academic Integrity standards. Signed: Andrew Wolk
"""

import math
import random
import matplotlib.pyplot as plt

class Point:
    #Represents a point in 2D space.
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, other):
        #Calculates the Euclidean distance between two points.
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def midpoint(self, other):
        #Finds the midpoint between two points.
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def __str__(self):
        #Returns a string representation of the point.
        return f"({self.x}, {self.y})"

class Circle:
    #Represents a circle with a center (Point) and radius.
    def __init__(self, x, y, r):
        self.center = Point(x, y)  # Center is stored as a Point object
        self.radius = r  # Radius of the circle
    
    @property
    def area(self):
        #Calculates and returns the area of the circle.
        return math.pi * (self.radius ** 2)
    
    def __repr__(self):
        #Returns a string of the circle for testing.
        return f"This is a circle with center {self.center} and radius {self.radius}"

class Bubble(Circle):
    #Represents a bubble, which is a special case of a circle.
    def __add__(self, other):
        #Merges two bubbles into a new larger bubble based on their areas and midpoint.
        new_area = self.area + other.area
        new_radius = math.sqrt(new_area / math.pi)  # Compute new radius from total area
        new_center = self.center.midpoint(other.center)  # New center at the midpoint
        return Bubble(new_center.x, new_center.y, new_radius)
    
    @staticmethod
    def make_random_bubble():
        #Generates a random bubble with randomized position and size.
        x = random.uniform(-50, 50)  
        y = random.uniform(-50, 50)  
        r = random.uniform(5, 20)  
        return Bubble(x, y, r)

class BubbleCollection:
    #Manages a collection of bubbles, merging overlapping bubbles.
    def __init__(self):
        self.bub_list = []  # List to store Bubble objects
    
    def __iadd__(self, bubble):
        #Adds a bubble to the collection, merging it with overlapping bubbles.
        for existing_bubble in self.bub_list:
            if bubble.center.distance(existing_bubble.center) < (bubble.radius + existing_bubble.radius):
                # If bubbles overlap, merge them and recursively add the merged bubble
                merged_bubble = bubble + existing_bubble
                self.bub_list.remove(existing_bubble)  # Remove old bubble
                return self.__iadd__(merged_bubble)  # Recursively add merged bubble
        
        # If no overlap, add the bubble normally
        self.bub_list.append(bubble)
        return self
    
    def make_graph(self):
        #Generates and displays a graph of all bubbles using matplotlib.
        fig, ax = plt.subplots()
        ax.set_xlim(-60, 60) 
        ax.set_ylim(-60, 60)  
        ax.set_aspect('equal') 
        
        for bubble in self.bub_list:
            # Draw each bubble as a circle on the plot
            circle = plt.Circle((bubble.center.x, bubble.center.y), bubble.radius, fill=True, alpha=0.5)
            ax.add_patch(circle)
        
        plt.show()  # Show plot window
        plt.savefig("bubbles.png")  # Save plot as PNG file

if __name__ == "__main__":
    #Runs the program: creates a BubbleCollection, adds random bubbles, and plots them.
    collection = BubbleCollection()
    for _ in range(10):
        collection += Bubble.make_random_bubble()  # Generate and add random bubbles
    collection.make_graph()  # Visualize bubbles
