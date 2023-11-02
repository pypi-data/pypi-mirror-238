#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Matplotlib imports
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt


# Other imports
import numpy
import string
from pathvalidate import sanitize_filepath
from pathlib import Path
from dataclasses import dataclass
import MPSPlots
from MPSPlots.render2D.axis import Axis
from MPSPlots.tools.utils import int_to_roman
from MPSPlots.render2D.artist import AxAnnotation


@dataclass
class SceneProperties:
    unit_size: tuple = (10, 3)
    tight_layout: bool = True
    transparent_background: bool = False
    title: str = ""

    ax_inherit_list = [
        'font_size',
        'x_scale_factor',
        'y_scale_factor',
        'line_width',
        'line_style',
        'legend_font_size',
        'tick_size',
        'x_tick_position',
        'y_tick_position',
        'x_limits',
        'y_limits',
        'x_label',
        'y_label',
        'water_mark',
        'equal',
        'equal_limits',
        'show_legend',
        'show_grid',
        'show_ticks',
        'show_colorbar',
    ]

    def __post_init__(self):
        self._mpl_axis_list = []
        self._axis_generated = False

    def __setattr__(self, name, value):
        if name in self.ax_inherit_list:
            for ax in self:
                setattr(ax, name, value)
        else:
            super(SceneProperties, self).__setattr__(name, value)

    def colorbar_n_ticks(self, value: int):
        for ax in self:
            ax.colorbar.n_ticks = value

    def colorbar_label_size(self, value: int):
        for ax in self:
            ax.colorbar.label_size = value

    @property
    def shape(self) -> numpy.ndarray:
        return numpy.array([self.number_of_column, self.number_of_row])

    @property
    def maximum_column_value(self) -> int:
        column_values = [ax.col for ax in self]
        return numpy.array(column_values).max()

    @property
    def maximum_row_value(self) -> int:
        row_values = [ax.row for ax in self]
        return numpy.array(row_values).max()

    @property
    def number_of_column(self) -> int:
        """
        Return the number of column for axis in the figure

        :returns:   number of column
        :rtype:     int
        """
        return self.maximum_column_value + 1

    @property
    def number_of_row(self) -> int:
        """
        Return the number of row for axis in the figure

        :returns:   number of row
        :rtype:     int
        """
        return self.maximum_row_value + 1

    def close(self) -> None:
        plt.close(self._mpl_figure)

    def save_figure(self, save_directory: str, **kwargs):
        save_directory = Path(save_directory)

        save_directory = sanitize_filepath(save_directory)

        plt.savefig(
            fname=save_directory,
            transparent=self.transparent_background,
            **kwargs
        )

    def show(self, save_directory: str = None, **kwargs):
        self._render_()

        if save_directory is not None:
            self.save_figure(save_directory=save_directory, **kwargs)

        plt.show()

        return self

    def _render_(self):
        """
        Renders the object.
        """
        if not self._axis_generated:
            self._generate_axis_()

        for ax in self._mpl_axis_list:
            ax._render_()

        if self.tight_layout:
            plt.tight_layout()

        return self

    def __getitem__(self, idx: int) -> Axis:
        """
        Returns ax from the SceneList

        :param      idx:  The index
        :type       idx:  int

        :returns:   axis corresponding to idx
        :rtype:     Axis
        """
        return self._mpl_axis_list[idx]

    def generate_mpl_figure(self) -> None:
        figure_size = self.shape * numpy.array(self.unit_size)
        self._mpl_figure = plt.figure(figsize=figure_size)
        self._mpl_figure.suptitle(self.title)

    def annotate_axis(self, numerotation_type: str = 'alphabet', **kwargs) -> None:
        """
        Annotate each axis in the figure with a numbering system

        :param      numerotation_type:  The numerotation type
        :type       numerotation_type:  str
        :param      kwargs:             The keywords arguments to be sent to each ax.add_ax_annotation
        :type       kwargs:             dictionary

        :returns:   { description_of_the_return_value }
        :rtype:     None
        """

        if numerotation_type.lower() == 'alphabet':
            numerotation = string.ascii_lowercase
        elif numerotation_type.lower() == 'roman':
            numerotation = [int_to_roman(idx) for idx in range(1, 26)]
        elif numerotation_type.lower() == 'numbering':
            numerotation = [int_to_roman(idx) for idx in range(1, 26)]

        def is_AxAnnotation(artist) -> bool:
            if isinstance(artist, AxAnnotation):
                return False
            return True

        for ax in self:
            ax._artist_list = list(filter(is_AxAnnotation, ax._artist_list))

        for letter, ax in zip(numerotation, self):
            ax.add_ax_annotation(
                text=f'({letter})',
                **kwargs
            )


@dataclass
class SceneList(SceneProperties):
    ax_orientation: str = 'vertical'

    @property
    def next_row_number(self) -> int:
        if self.ax_orientation == 'horizontal':
            row_number = 0
        elif self.ax_orientation == 'vertical':
            row_number = len(self._mpl_axis_list)

        return row_number

    @property
    def next_column_number(self) -> int:
        if self.ax_orientation == 'horizontal':
            column_number = len(self._mpl_axis_list)
        elif self.ax_orientation == 'vertical':
            column_number = 0

        return column_number

    def append_ax(self, **ax_kwargs: dict) -> None:
        """
        Appends axis to the list.

        :param      ax:   The axis to append to scene
        :type       ax:   Axis

        :returns:   No returns
        :rtype:     None
        """
        axis = Axis(
            col=self.next_column_number,
            row=self.next_row_number,
            **ax_kwargs
        )

        self._mpl_axis_list.append(axis)

        return axis

    def _generate_axis_(self):
        self.generate_mpl_figure()

        grid = gridspec.GridSpec(
            ncols=self.number_of_column,
            nrows=self.number_of_row,
            figure=self._mpl_figure
        )

        for axis in self._mpl_axis_list:
            subplot = self._mpl_figure.add_subplot(
                grid[axis.row, axis.col],
                projection=axis.projection
            )

            axis._ax = subplot

        self.axis_generated = True

        return self


@dataclass
class SceneMatrix(SceneProperties):
    def set_axis_row(self, value) -> None:
        for ax in self._mpl_axis_list:
            ax.row = value

    def set_axis_col(self, value) -> None:
        for ax in self._mpl_axis_list:
            ax.col = value

    def set_style(self, **style_dict):
        for ax in self:
            ax.set_style(**style_dict)

        return self

    @property
    def axis_matrix(self):
        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)
        for ax in self._mpl_axis_list:
            ax_matrix[ax.row, ax.col] = ax

        return ax_matrix

    def append_ax(self, row: int, column: int, **ax_kwargs: dict) -> None:
        """
        Appends axis to the list.

        :param      ax:   The axis to append to scene
        :type       ax:   Axis

        :returns:   No returns
        :rtype:     None
        """
        axis = Axis(
            col=column,
            row=row,
            **ax_kwargs
        )

        self._mpl_axis_list.append(axis)

        return axis

    def _generate_axis_(self):
        self.generate_mpl_figure()

        grid = gridspec.GridSpec(
            ncols=self.number_of_column,
            nrows=self.number_of_row,
            figure=self._mpl_figure
        )

        ax_matrix = numpy.full(
            shape=(self.number_of_row, self.number_of_column),
            fill_value=None
        )

        for axis in self._mpl_axis_list:
            subplot = self._mpl_figure.add_subplot(grid[axis.row, axis.col], projection=axis.projection)
            ax_matrix[axis.row, axis.col] = subplot
            axis._ax = subplot

        self.axis_generated = True

        return self


# -
