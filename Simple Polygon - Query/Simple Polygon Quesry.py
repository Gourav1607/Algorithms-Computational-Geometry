#!/usr/bin/env python
# coding: utf-8

# Simple Polygon - Query
# Gourav Siddhad

#################################################################

print('Importing Libraries', end='')

import matplotlib.pyplot as plt
from fractions import Fraction
import cv2
from random import randint
import numpy as np

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


def drawpoly(N):
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
                scords[i+1][0], scords[i+1][1]), color=(0, 0, 0), thickness=1)
        else:
            cvimage = cv2.line(cvimage, (scords[i][0], scords[i][1]), (
                scords[0][0], scords[0][1]), color=(0, 0, 0), thickness=1)

    cv2.imwrite('CP01_{:02d}_01.png'.format(N), cvimage)
    images.append(np.array(cvimage))

    return images, cvimage, scords

#################################################################


def shootray(images, cvimage, scords):
    totalcross = 0
    Q = [randint(0, SIZE-1), randint(0, SIZE-1)]
    # Q = tuple(np.mean(scords, axis=0, dtype='int32'))
    print('Query Point Q : ', Q, end='\n\n')

    cvimage = cv2.line(cvimage, (Q[0], Q[1]),
                       (Q[0], Q[1]), color=(0, 0, 255), thickness=1)
    cvimage = cv2.circle(cvimage, (Q[0], Q[1]), 5, (0, 0, 255), 1)
    images.append(np.array(cvimage))

    for i in range(Q[0], SIZE-1, 1):
        point = np.array([i, Q[1]])
        imvalue = cvimage[point[0], point[1], :]
        if imvalue[0] == 0 and imvalue[1] == 0 and imvalue[2] == 0:
            totalcross += 1
            i += 1
        cvimage = cv2.line(cvimage, (point[0], point[1]), (point[0], point[1]), color=(
            0, 0, 255), thickness=1)

    cv2.imwrite('CP02_{:02d}_03.png'.format(N), cvimage)
    images.append(np.array(cvimage))

    print('Total Crossings : ', totalcross)

    pcolor = cvimage[Q[0], Q[1]]
    if pcolor[0] == 0 and pcolor[1] == 0 and pcolor[2] == 0:
        print('Q on Polygon')
        text = 'On'
    elif totalcross % 2 == 0:
        print('Q outside Polygon')
        text = '{:1d} Out'.format(totalcross)
    else:
        print('Q inside Polygon')
        text = '{:1d} In'.format(totalcross)

    cv2.putText(cvimage, text, tuple(
        [Q[0], Q[1]-5]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, 1)
    cv2.imwrite('CP02_{:02d}_04.png'.format(N), cvimage)
    images.append(np.array(cvimage))

    if totalcross % 2 != 0:
        vert0 = scords[0]
        vert1 = scords[1]
        cvimage = cv2.line(cvimage, (Q[0], Q[1]),
                           vert0, color=(0, 255, 0), thickness=2)
        cvimage = cv2.line(cvimage, (Q[0], Q[1]),
                           vert1, color=(0, 255, 0), thickness=2)
        cvimage = cv2.line(cvimage, vert1, vert0,
                           color=(0, 255, 0), thickness=2)

        seedpoint = tuple(
            np.mean([list(Q), list(vert0), list(vert1)], axis=0, dtype='int32'))
        print(seedpoint)
        cv2.floodFill(cvimage, None, seedPoint=seedpoint, newVal=(
            0, 255, 0), loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))

        cv2.imwrite('CP02_{:02d}_05.png'.format(N), cvimage)
        images.append(np.array(cvimage))

        vert0, vert1, Q = np.array(vert0), np.array(vert1), np.array(Q)
        area = abs(0.5*np.cross(abs(vert0-Q), abs(vert1-Q)))
        print('Area of Triangle : {:} Unit Square'.format(area), end='\n\n')

    return images, cvimage, totalcross

#################################################################


for N in range(5, 26, 5):
    images, cvimage, scords = drawpoly(N)
    images, cvimage, totalcross = shootray(images, cvimage, scords)

    fig, ax = plt.subplots(1, 4, figsize=(15, 15))
    ax[0].imshow(cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB))
    ax[0].set_title('Polygon - {:02d}'.format(N))
    ax[1].imshow(cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB))
    ax[1].set_title('Query Q - {:02d}'.format(N))
    ax[2].imshow(cv2.cvtColor(images[3], cv2.COLOR_BGR2RGB))
    ax[2].set_title('Ray Shoot - {:02d}'.format(N))
    if len(images) == 5:
        ax[3].imshow(cv2.cvtColor(images[4], cv2.COLOR_BGR2RGB))
        ax[3].set_title('Triangle - {:02d}'.format(N))
    else:
        ax[3].imshow(cv2.cvtColor(
            np.zeros((800, 800, 3), dtype='uint8'), cv2.COLOR_BGR2RGB))
        ax[3].set_title('NA')
    plt.tight_layout()
    plt.savefig('CP02_{:02d}.png'.format(N), dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.show()

#################################################################

N = int(input('Enter Number of Co-ordinates (N>2): '))
if N <= 2:
    print('Drawing Polygon with N<=2 is not possible')
    exit(0)

images, cvimage, scords = drawpoly(N)
images, cvimage, totalcross = shootray(images, cvimage, scords)

fig, ax = plt.subplots(1, 4, figsize=(15, 15))
ax[0].imshow(cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB))
ax[0].set_title('Polygon - {:02d}'.format(N))
ax[1].imshow(cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB))
ax[1].set_title('Query Q - {:02d}'.format(N))
ax[2].imshow(cv2.cvtColor(images[3], cv2.COLOR_BGR2RGB))
ax[2].set_title('Ray Shoot - {:02d}'.format(N))
if len(images) == 5:
    ax[3].imshow(cv2.cvtColor(images[4], cv2.COLOR_BGR2RGB))
    ax[3].set_title('Triangle - {:02d}'.format(N))
else:
    ax[3].imshow(cv2.cvtColor(
        np.zeros((800, 800, 3), dtype='uint8'), cv2.COLOR_BGR2RGB))
    ax[3].set_title('NA')
plt.tight_layout()
plt.savefig('CP02_{:02d}.png'.format(N), dpi=300,
            bbox_inches='tight', pad_inches=0.1)
plt.show()
