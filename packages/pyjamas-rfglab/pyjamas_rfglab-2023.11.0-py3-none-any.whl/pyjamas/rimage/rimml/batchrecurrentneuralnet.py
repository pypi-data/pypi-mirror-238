"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Optional

import numpy
from PyQt6 import QtGui, QtCore

from pyjamas.pjsthreads import ThreadSignals
from pyjamas.rimage.rimml.batchml import BatchML
from pyjamas.rimage.rimml.rimrecurrentneuralnet import rimrecurrentneuralnet
from pyjamas.rimage.rimutils import rimutils
from pyjamas.rutils import RUtils


class BatchRecurrentNeuralNet(BatchML):
    def __init__(self, n_frames: int, classifier: Optional[rimrecurrentneuralnet] = None):
        super().__init__(n_frames, classifier)
        self.prob_arrays = [numpy.empty((1, 0)) for i in range(self.n_frames)]
        self.object_arrays = [numpy.empty((1, 0)) for i in range(self.n_frames)]
        self.object_ids = [numpy.empty((1, 0)) for i in range(self.n_frames)]

    def fit(self, stop_signal: Optional[ThreadSignals] = None) -> bool:
        if self.image_classifier is None:
            return False

        if stop_signal is not None:
            stop_signal.emit('Launching classifier training ...')

        self.image_classifier.fit()

        if stop_signal is not None:
            stop_signal.emit('Classifier training completed.')
        return True

    def predict(self, slices: numpy.ndarray, indices: numpy.ndarray, progress_signal: Optional[ThreadSignals] = None,
                annotations: Optional[numpy.ndarray] = None, ids: Optional[list] = None, max_id: Optional[int] = 0,
                track: bool = False) \
            -> bool:

        # Make sure that the slices are in a 1D numpy array.
        indices = numpy.atleast_1d(indices)
        num_slices = len(indices)

        # For every slice ...
        for i, index in enumerate(indices):
            if slices.ndim > 2:
                theimage = slices[index].copy()
            elif slices.ndim == 2 and index == 0:
                theimage = slices.copy()

            if annotations is not None:
                if not track:
                    if index == 0:  # No previous mask to input
                        themask = numpy.zeros(theimage.shape)
                    elif i == 0:  # Use the polyline annotations made by the user
                        thepolyline = annotations[index - 1].copy()
                        try:
                            themask = rimutils.mask_from_polylines(theimage.shape, thepolyline)
                        except IndexError:
                            themask = numpy.zeros(theimage.shape)
                    else:  # Use the previous classifier output
                        thepolygons = []
                        for apoly in self.object_arrays[index - 1]:
                            thispolygon = QtGui.QPolygonF()
                            for thepoint in apoly:
                                thispolygon.append(QtCore.QPointF(thepoint[0], thepoint[1]))
                            thepolygons.append(thispolygon)
                        try:
                            themask = rimutils.mask_from_polylines(theimage.shape, thepolygons)
                        except IndexError:
                            themask = numpy.zeros(theimage.shape)
                    if numpy.sum(themask) == 0:
                        themask = numpy.ones(theimage.shape)
                    self.object_arrays[index], self.prob_arrays[index] = self.image_classifier.predict(theimage,
                                                                                                       themask)
                    self.object_ids[index] = None  # No reason to believe segmentations are tracked from previous frame

                else:
                    print(f"Slice index {index}, slice number {i}")
                    if index == 0:  # No previous mask to input
                        thepolygons = []
                    elif i == 0:  # Use polyline annotation made by user
                        thepolygons = annotations[index - 1]
                        self.object_ids[index - 1] = ids[index - 1]
                    else:  # Use the previous classifier output
                        thepolygons = []
                        for apoly in self.object_arrays[index - 1]:
                            thispolygon = QtGui.QPolygonF()
                            for thepoint in apoly:
                                thispolygon.append(QtCore.QPointF(thepoint[0], thepoint[1]))
                            thepolygons.append(thispolygon)

                    self.object_ids[index] = []
                    self.object_arrays[index] = []
                    self.prob_arrays[index] = []
                    for obj_num, this_object in enumerate(thepolygons):
                        print(obj_num)
                        try:
                            this_mask = rimutils.mask_from_polylines(imsize=theimage.shape,
                                                                     polylines=[this_object],
                                                                     brushsz=0)
                        except IndexError:  # Polyline not big enough to make a mask from, use empty mask instead
                            this_mask = numpy.ones(theimage.shape, dtype=int)

                        this_object_array, this_prob_array = self.image_classifier.predict(theimage, this_mask)
                        if len(this_object_array) >= 1:  # Object detected
                            for new_obj_num, this_new_object in enumerate(this_object_array):
                                self.object_arrays[index].append(this_new_object)
                                self.prob_arrays[index].append(this_prob_array[new_obj_num])
                                if new_obj_num == 0 and ids is not None:  # Give same ID as prev cell
                                    self.object_ids[index].append(self.object_ids[index - 1][obj_num])
                                else:
                                    self.object_ids[index].append(max_id + 1)
                                    max_id += 1

            else:
                self.object_arrays[index], self.prob_arrays[index] = self.image_classifier.predict(theimage, slice_num=index)
                self.object_ids[index] = None

            if progress_signal is not None:
                progress_signal.emit(int((100 * (i + 1)) / num_slices))

        return True

    def reset_objects(self, n_frames: int) -> bool:
        self.n_frames = n_frames
        self.object_arrays = [numpy.empty((1, 0)) for i in range(self.n_frames)]
        self.prob_arrays = [numpy.empty((1, 0)) for i in range(self.n_frames)]
        self.object_ids = [numpy.empty((1, 0)) for i in range(self.n_frames)]

        return True
