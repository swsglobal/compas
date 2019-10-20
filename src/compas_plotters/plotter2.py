from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt


__all__ = ['Plotter2']


class Plotter2(object):
    """"""
    def __init__(self, view=None, size=(8, 5), dpi=100, **kwargs):
        """Initialises a plotter object"""
        self._bgcolor = None
        self._view = None
        self._axes = None
        self._artists = []
        self.view = view
        self.size = size
        self.dpi = dpi
        self.bgcolor = kwargs.get('bgcolor', '#ffffff')

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        if not view:
            return
        if len(view) != 2:
            return
        xlim, ylim = view
        if len(xlim) != 2:
            return
        if len(ylim) != 2:
            return
        self._view = xlim, ylim

    @property
    def axes(self):
        """Returns the axes subplot matplotlib object.

        Returns
        -------
        Axes
            The matplotlib axes object.

        Notes
        -----
        For more info, see the documentation of the Axes class ([1]_) and the
        axis and tick API ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/axes_api.html
        .. [2] https://matplotlib.org/api/axis_api.html

        """
        if not self._axes:
            figure = plt.figure(facecolor=self.bgcolor,
                                figsize=self.size,
                                dpi=self.dpi)
            axes = figure.add_subplot('111', aspect='equal')
            axes.grid(b=False)
            axes.set_frame_on(False)
            if self.view:
                xmin, xmax = self.view[0]
                ymin, ymax = self.view[1]
                axes.set_xlim(xmin, xmax)
                axes.set_ylim(ymin, ymax)
            axes.set_xscale('linear')
            axes.set_yscale('linear')
            axes.set_xticks([])
            axes.set_yticks([])
            axes.autoscale()
            plt.tight_layout()
            self._axes = axes
        return self._axes

    @property
    def figure(self):
        """Returns the matplotlib figure instance.

        Returns
        -------
        Figure
            The matplotlib figure instance.

        Notes
        -----
        For more info, see the figure API ([1]_).

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/figure_api.html

        """
        return self.axes.get_figure()

    @property
    def canvas(self):
        """Returns the canvas of the figure instance.
        """
        return self.figure.canvas

    @property
    def bgcolor(self):
        """Returns the background color.

        Returns
        -------
        str
            The color as a string (hex colors).

        """
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
        """Sets the background color.

        Parameters
        ----------
        value : str, tuple
            The color specififcation for the figure background.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of normalized RGB components.

        """
        self._bgcolor = value
        self.figure.set_facecolor(value)

    @property
    def title(self):
        """Returns the title of the plot.

        Returns
        -------
        str
            The title of the plot.

        """
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value):
        """Sets the title of the plot.

        Parameters
        ----------
        value : str
            The title of the plot.

        """
        self.figure.canvas.set_window_title(value)

    @property
    def artists(self):
        return self._artists

    @artists.setter
    def artists(self, artists):
        self._artists = artists

    # ==========================================================================
    # Methods
    # ==========================================================================

    def add_artist(self, artist):
        artist.plotter = self
        self._artists.append(artist)

    def add_artists(self, artists):
        for artist in artists:
            self.add_artist(artist)

    def register_listener(self, listener):
        """Register a listener for pick events.

        Parameters
        ----------
        listener : callable
            The handler for pick events.

        Returns
        -------
        None

        Notes
        -----
        For more information, see the docs of ``mpl_connect`` ([1]_), and on event
        handling and picking ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        .. [2] https://matplotlib.org/users/event_handling.html

        Examples
        --------
        .. code-block:: python

            #

        """
        self.figure.canvas.mpl_connect('pick_event', listener)

    def draw(self, pause=None):
        for artist in self._artists:
            artist.draw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def redraw(self, pause=None):
        """Updates and pauses the plot.

        Parameters
        ----------
        pause : float
            Ammount of time to pause the plot in seconds.

        """
        for artist in self._artists:
            artist.redraw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def show(self):
        """Displays the plot.

        """
        plt.show()

    def save(self, filepath, **kwargs):
        """Saves the plot to a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Notes
        -----
        For an overview of all configuration options, see [1]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/pyplot_api.html#matplotlib.pyplot.savefig

        """
        plt.savefig(filepath, **kwargs)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
