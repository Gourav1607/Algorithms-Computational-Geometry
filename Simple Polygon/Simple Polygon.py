#!/usr/bin/env python
# coding: utf-8

# Simple Polygon
# Gourav Siddhad

#################################################################

print('Importing Libraries', end='')

import numpy as np
from random import randint
import cv2
import matplotlib.pyplot as plt

print(' - Done')

#################################################################


def simplePolygon(refX, refY, cords):
    slopes = []
    refCord = [refX, refY]

    for point in cords:
        x, y = point
        relX, relY = x-refX, y-refY
        slopes.append(np.arctan2(relX, relY))

    zipped_lists = zip(slopes, cords)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    slopes, scords = [list(tuple) for tuple in tuples]

    return scords, slopes

#################################################################


SIZE = 800


def drawncolorpoly(N):
    images = []
    print('For N = {:02d}'.format(N))

    cords = [(randint(0, SIZE-1), randint(0, SIZE-1)) for _ in range(N)]
    print('Input Co-ordinates : ', cords)

    refX, refY = np.mean(cords, axis=0, dtype='int32')
    print('Reference Points : ', refX, refY)

    scords, slopes = simplePolygon(refX, refY, cords)
    print('Simple Co-ordinates : ', scords)
    print('Slopes : ', slopes)

    cvimage = np.zeros(shape=[SIZE, SIZE, 3], dtype=np.uint8)
    cvimage += 255

    for i, vtx in enumerate(scords):
        if i < len(scords)-1:
            cvimage = cv2.line(cvimage, (scords[i][0], scords[i][1]), (
                scords[i+1][0], scords[i+1][1]), color=(0, 0, 0), thickness=2)
        else:
            cvimage = cv2.line(cvimage, (scords[i][0], scords[i][1]), (
                scords[0][0], scords[0][1]), color=(0, 0, 0), thickness=2)

    cv2.imwrite('CP01_{:02d}_01.png'.format(N), cvimage)
    images.append(np.array(cvimage))

    cv2.floodFill(cvimage, None, seedPoint=(refX, refY), newVal=(
        0, 255, 0), loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))
    cv2.floodFill(cvimage, None, seedPoint=(0, 0), newVal=(
        0, 0, 255), loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))

    cv2.imwrite('CP01_{:02d}_02.png'.format(N), cvimage)
    images.append(np.array(cvimage))

    fig, ax = plt.subplots(1, 2, figsize=(10, 10))
    ax[0].imshow(images[0])
    ax[0].set_title('Polygon - {:02d}'.format(N))
    ax[1].imshow(images[1])
    ax[1].set_title('Colored - {:02d}'.format(N))
    plt.tight_layout()
    plt.savefig('CP01_{:02d}.png'.format(N), dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.show()

    print()

#################################################################


for N in range(5, 26, 5):
    drawncolorpoly(N)

#################################################################

N = int(input('Enter Number of Co-ordinates (N>2): '))
if N <= 2:
    print('Drawing Polygon with N<=2 is not possible')
    exit(0)

drawncolorpoly(N)
