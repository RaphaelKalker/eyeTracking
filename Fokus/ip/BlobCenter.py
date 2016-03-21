import logging
import math
import numpy as np

class BlobCenter():
    def __init__(self, center, radius, confidence):
        self.center = center
        self.radius = radius
        self.confidence = confidence
