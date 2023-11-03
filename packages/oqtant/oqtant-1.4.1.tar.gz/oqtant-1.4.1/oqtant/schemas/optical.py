# classes and methods for abstractions of quasi-1D "painted" light Oqtant objects

# "ideal" optical potentials are those specified by the user using included objects
# "actual" optical potentials include implementation and hardware realities
# such as objects being projected as a sum of gaussians on a pre-defined position grid
# with dynamic weights recalculated on a periodic basis

import json
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas import job as job_schema

from oqtant.schemas.interpolation import interpolate_1d, interpolate_1d_list


def gaussian(
    xs: np.ndarray,
    amp: float = 1.0,
    center: float = 0.0,
    sigma: float = 1.0,
    offset: float = 0.0,
) -> list:
    """Function that evaluates a standard gaussian form over the given input points.

    Args:
        xs (np.ndarray): positions where the gaussian should be evaluated
        amp (float, optional): gaussian amplitude. Defaults to 1.0.
        center (float, optional): gaussian center. Defaults to 0.0.
        sigma (float, optional): gaussian width. Defaults to 1.0.
        offset (float, optional): gaussian dc offset. Defaults to 0.0.

    Returns:
        list: gaussian function evaluated over the input points
    """
    return amp * np.exp(-((xs - center) ** 2) / (2 * sigma**2)) + offset


class Projected:
    """A class that captures the features, and limitations, of optical objects
    implemented by the Oqtant hardware projection system.
    """

    RESOLUTION = 2.2  # 1/e^2 diameter of projection system, microns
    POSITION_STEP = 1.0  # grid step between projected spots, microns
    POSITION_MIN = -60.0  # minimum position of projected light, microns
    POSITION_MAX = 60  # maximum position of projected light, microns
    PROJECTED_SPOTS = np.arange(POSITION_MIN, POSITION_MAX + 1.0, POSITION_STEP)
    UPDATE_PERIOD = 0.1  # milliseconds between updates of projected light
    ENERGY_MIN = 0.0  # minimimum projected energy shift at any position, kHz
    ENERGY_MAX = 100  # maximum projected energy shift at any position, kHz

    @staticmethod
    def get_corrected_times(times: list[float]) -> list:
        """Calculates the effective times realized by the projection system, which only
        updates optical features periodically (e.g. every 100 us)

        Args:
            time (float): Time, in ms, that the caller wants to be corrected

        Returns:
            float: The corrected time
        """
        times_corrected = (
            np.floor((1000.0 * np.asarray(times)) / (1000.0 * Projected.UPDATE_PERIOD))
            * Projected.UPDATE_PERIOD
        )
        return list(times_corrected)

    @staticmethod
    def get_corrected_time(time: float) -> float:
        """Calculates the effective time realized by the projection system, which only
        updates optical features periodically (e.g. every 100 us)

        Args:
            time (float): Time, in ms, that the caller wants to be corrected

        Returns:
            float: The corrected time
        """
        return Projected.get_corrected_times(times=[time])[0]

    # gets corrected weights at each projected gaussian spot to reproduce the ideal
    # potential energy vs position as closely as is reasonable
    @staticmethod
    def get_projection_weights(
        get_ideal_potential: Callable[[float], list], time: float = 0
    ) -> list:
        """Calculates the corrected weights for each horizontal "spot" projected onto
        the atom ensemble to attempt to achieve the passed optical object's "ideal"
        potential energy profile.  Implements first-order corrections for anamolous
        contributions from nearby spots, inter-integer barrier centers, etc.

        Args:
            get_ideal_potential (Callable[[float], list]): Method for the optical object
                or any class that supports optical objects that calculates the user
                specified "ideal" or "requested" potential energy profile.
            time (float, optional): Time at which . Defaults to 0.

        Returns:
            list: Calculated (optical intensity) contribution for each projected spot
            (diffraction frequency) used by the projection system
        """

        positions_fine = np.arange(
            Projected.POSITION_MIN, Projected.POSITION_MAX + 0.1, 0.1
        )

        # calculate the ideal potential over the entire spatial region
        potential_ideal = np.asarray(
            get_ideal_potential(time=time, positions=positions_fine)
        )

        # calculate the optical field that would result from raw object data
        weights = np.asarray(
            get_ideal_potential(time=time, positions=Projected.PROJECTED_SPOTS)
        )
        potential_actual = np.zeros_like(positions_fine)
        for indx, spot in enumerate(Projected.PROJECTED_SPOTS):
            potential_actual += gaussian(
                xs=positions_fine,
                amp=weights[indx],
                center=spot,
                sigma=Projected.RESOLUTION / 4.0,
                offset=0.0,
            )

        # recompute weights with overall scaling to achieve correct peak height/energy
        # this removes first order variation in height with inter-grid object centers
        # and contributions from adjacent space/frequency spots
        maximum = max(potential_actual)
        scaling = max(potential_ideal) / maximum if maximum > 0.0 else 0.0
        return list(scaling * weights)

    @staticmethod
    def get_actual_potential(
        get_ideal_potential: Callable[[float], list],
        time: float = 0.0,
        positions: list = PROJECTED_SPOTS,
    ) -> list:
        """Calculates the 'actual' potential energy vs position for optical objects/fields
        as realized by the Oqtant projection system
        Includes effects, and first-order corrections for, finite time updates and finite
        optical resolution / optical objects being projected as sums of gaussians
        and energetic clipping of optical potentials at 100 kHz

        Args:
            get_ideal_potential (Callable[[float], list]): object method for requested/ideal potential
            time (float, optional): time to evaluate ideal potential.
                Defaults to 0.0.
            positions (list, optional): positions to evaluate the actual potential at.
                Defaults to PROJECTED_SPOTS.

        Returns:
            list: Expected actual potential energy at the requested positions.
        """
        time = Projected.get_corrected_time(time)  # include finite-update period
        weights = Projected.get_projection_weights(get_ideal_potential, time)
        potential = np.zeros_like(positions)
        for indx, spot in enumerate(Projected.PROJECTED_SPOTS):
            potential += gaussian(
                xs=positions,
                amp=weights[indx],
                center=spot,
                sigma=Projected.RESOLUTION / 4.0,
                offset=0.0,
            )
        return list(np.clip(potential, Projected.ENERGY_MIN, Projected.ENERGY_MAX))


class Snapshot(job_schema.Landscape):
    """A class that represents a painted optical landscape / potential at a single
    point in (manipulation stage) time.
    """

    @classmethod
    def new(
        cls,
        time: float = 0,
        positions: list = [-10, 10],
        potentials: list = [0, 0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        """Creates a new Snapshot object instance
        Args:
            time (float): Time associated with this snapshot
            positions (list): position list for the snapshot
            potentials (list): potential energies corresponding to the list of positions
            interpolation (job_schema.InterpolationType): how to connect the object's
                (positions, potentials) data in space.
        Returns:
            Snapshot: the created Snapshot object
        """
        return cls(
            time_ms=time,
            positions_um=positions,
            potentials_khz=potentials,
            spatial_interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, landscape: job_schema.Landscape):
        return cls(**landscape.model_dump())

    def get_ideal_potential(
        self, time: float = 0, positions: list = Projected.PROJECTED_SPOTS
    ) -> list:
        """Samples the potential energy of this snapshot at the specified positions
        Args:
            positions (list): List of positions (in microns).
        Returns:
            list: Value of potential energy (in kHz) at the specified positions.
        """
        potentials = interpolate_1d_list(
            self.positions_um,
            self.potentials_khz,
            positions,
            self.spatial_interpolation,
        )
        return potentials

    def get_potential(self, positions: list) -> list:
        """Calculates the optical potential associated with this Snapshot object, taking
        into account the actual implementation of the Oqtant projection system.

        Args:
            positions (list): positions, in microns, where the potential should be evaluated

        Returns:
            list: Potential energies, in kHz, at the requested positions
        """
        return Projected.get_actual_potential(
            self.get_ideal_potential, positions=positions
        )

    def show_potential(
        self,
        xlimits: list = [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1],
        ylimits: list = [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1],
        include_ideal: bool = False,
    ):
        """Plots the potential energy as a function of position for this snapshot.

        Args:
            xlimits (list, optional): Plot limits for x axis.
                Defaults to [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1].
            ylimits (list, optional): Plot limits for y axis.
                Defaults to [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1].
            include_ideal (bool, optional): Option to include target potential in plot.
                Defaults to False.
        """

        positions = np.arange(
            Projected.POSITION_MIN, Projected.POSITION_MAX + 0.1, 0.1, dtype=float
        )

        fig, ax = plt.subplots()
        color = next(ax._get_lines.prop_cycler)["color"]
        (ln,) = plt.plot(
            positions, self.get_potential(positions=positions), color=color
        )
        if include_ideal:
            (ln2,) = plt.plot(
                positions,
                self.get_ideal_potential(positions=positions),
                "--",
                color=color,
            )
            plt.plot(self.positions_um, self.potentials_khz, ".", color=color)
            lns = [ln, ln2]
            labs = ["actual", "ideal"]
            ax.legend(lns, labs, loc=0)
        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Snapshot potential energy profile")
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        plt.show()


# (potentially) dynamic landscape made up of snapshots
class Landscape(job_schema.OpticalLandscape):
    """Class that represents a dynamic painted-potential optical landscape constructed
    from individual (instantaneous time) Snapshots
    """

    @classmethod
    def new(
        cls,
        snapshots: list[Snapshot] = [
            Snapshot.new(time=0),
            Snapshot.new(time=2),
        ],
    ):
        optical_landscapes = []
        for snapshot in snapshots:
            optical_landscapes.append(
                job_schema.Landscape(
                    time_ms=snapshot.time_ms,
                    positions_um=snapshot.positions_um,
                    potentials_khz=snapshot.potentials_khz,
                    spatial_interpolation=snapshot.spatial_interpolation,
                )
            )
        return cls(landscapes=optical_landscapes)

    @classmethod
    def from_input(cls, landscape: job_schema.OpticalLandscape):
        """
        Create an instance of the class using the provided `landscape` object.

        Parameters:
            - landscape (job_schema.OpticalLandscape): The landscape object to create the instance from.

        Returns:
            - cls: An instance of the class created using the `landscape` object.
        """
        return cls(**json.loads(landscape.model_dump_json()))

    # extract Snapshot abstract objects from backend data structure
    @property
    def snapshots(self) -> list[Snapshot]:
        """
        Returns: A list of Snapshot objects.
        """
        return [Snapshot(**landscape.model_dump()) for landscape in self.landscapes]

    def get_ideal_potential(
        self, time: float, positions: list = Projected.PROJECTED_SPOTS
    ) -> list:
        """Calculates ideal object potential energy at the specified time and positions.
        Args:
            time (float):
                Time (in ms) at which the potential energy is calculated.
            positions (list, optional):
                Positions at which the potential energy is calculated.
                Defaults to np.linspace(-100, 100, 201).
        Returns:
            list: Potential energies (in kHz) at specified time and positions.
        """
        potential = [0] * len(positions)
        snaps = self.snapshots
        if len(snaps) < 2:
            return potential
        snap_times = [snap.time_ms for snap in snaps]
        if time >= min(snap_times) and time <= max(snap_times):
            pre = next(snap for snap in snaps if snap.time_ms <= time)
            nex = next(snap for snap in snaps if snap.time_ms >= time)
            potential = [
                interpolate_1d(
                    [pre.time_ms, nex.time_ms], [p1, p2], time, self.interpolation
                )
                for p1, p2 in zip(
                    pre.get_ideal_potential(positions=positions),
                    nex.get_ideal_potential(positions=positions),
                )
            ]
        return potential

    def get_potential(
        self, time: float, positions: list = Projected.PROJECTED_SPOTS
    ) -> list:
        """Calculates the optical potential associated with this Landscape object, taking
        into account the actual implementation of the Oqtant projection system, at the
        given time.

        Args:
            time (float): time, in ms, at which to sample the potential energy
            positions (list): positions, in microns, where the potential should be evaluated

        Returns:
            list: Potential energies, in kHz, at the requested positions and time
        """
        return Projected.get_actual_potential(
            self.get_ideal_potential, time=time, positions=positions
        )

    def show_potential(
        self,
        times: list = [0.0],
        xlimits: list = [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1],
        ylimits: list = [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1],
        include_ideal: bool = False,
    ):
        """Plots the potential energy as a function of position for this Landscape at this given times.

        Args:
            times (list): times, in ms, at which to evaluate and plot the potential
            xlimits (list, optional): Plot limits for x axis.
                Defaults to [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1].
            ylimits (list, optional): Plot limits for y axis.
                Defaults to [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1].
            include_ideal (bool, optional): Option to include target potential in plot.
                Defaults to False.
        """

        positions = np.arange(
            Projected.POSITION_MIN, Projected.POSITION_MAX + 0.1, 0.1, dtype=float
        )

        fig, ax = plt.subplots()
        lns = []
        labs = []
        for time in times:
            potentials = self.get_potential(time, positions)
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(positions, potentials, color=color)
            lns.append(ln)
            labs.append("t = " + str(time) + " ms")
            if include_ideal:
                potentials_ideal = self.get_ideal_potential(
                    time=time, positions=positions
                )
                (ln,) = plt.plot(positions, potentials_ideal, "--", color=color)
                lns.append(ln)
                labs.append("t = " + str(time) + " ms (ideal)")

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Landscape potential energy profile")
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        ax.legend(lns, labs, loc=0)
        plt.show()


class Barrier(job_schema.Barrier):
    """Class that represents a painted optical barrier."""

    @classmethod
    def new(
        cls,
        position: float = 0,
        height: float = 0,
        width: float = 1,
        birth: float = 0,
        lifetime: float = 0,
        shape: job_schema.ShapeType = job_schema.ShapeType.GAUSSIAN,
        interpolation: job_schema.InterpolationType = job_schema.InterpolationType.LINEAR,
    ):
        if lifetime == 0:
            data = {
                "times_ms": [birth],
                "positions_um": [position],
                "heights_khz": [height],
                "widths_um": [width],
                "shape": shape,
                "interpolation": interpolation,
            }
        else:
            data = {
                "times_ms": [birth, birth + lifetime],
                "positions_um": [position] * 2,
                "heights_khz": [height] * 2,
                "widths_um": [width] * 2,
                "shape": shape,
                "interpolation": interpolation,
            }

        return cls(**data)

    @classmethod
    def from_input(cls, barrier: job_schema.Barrier):
        return cls(**barrier.model_dump())

    @property
    def lifetime(self) -> float:
        """Extract the Barrier lifetime.

        Returns:
            float: Amount of time (in ms) that Barrier object will exist.
        """
        return self.death - self.birth

    @property
    def birth(self) -> float:
        """Extract the (manipulation stage) time that the Barrier will be created.

        Returns:
            float: Time (in ms) at which the Barrier will start being projected.
        """
        return min(self.times_ms)

    @property
    def death(self) -> float:
        """Extract the (manipulation stage) time that the Barrier will cease to exist.

        Returns:
            float: Time (in ms) at which the Barrier will stop being projected.
        """
        return max(self.times_ms)

    def evolve(self, duration: float, position=None, height=None, width=None):
        """Evolve the position, height, and/or width of a Barrier over a duration.
        Used to script a Barrier's behavior.

        Args:
            duration (float): Time (in ms) over which evolution should take place.
            position (float, optional): Position, in microns, to evolve to.
                                        Defaults to None (position remains unchanged).
            height (float, optional): Height, in kHz, to evolve to.
                                        Defaults to None (height remains unchanged).
            width (float, optional): Width, in microns, to evolve to.
                                        Defaults to None (width remains unchanged).
        """
        if position is None:
            position = self.positions_um[-1]
        if height is None:
            height = self.heights_khz[-1]
        if width is None:
            width = self.widths_um[-1]
        self.positions_um.append(position)
        self.heights_khz.append(height)
        self.widths_um.append(width)
        self.times_ms.append(self.times_ms[-1] + duration)

    def is_active(self, time: float) -> bool:
        """Queries if the barrier is active (exists) at the specified time
        Args:
            time (float): Time (in ms) at which the query is evaluated.
        Returns:
            bool: True if the barrier exists at the specified time.
        """
        return time >= self.times_ms[0] and time <= self.times_ms[-1]

    def get_positions(self, times: list) -> list:
        """Calculate barrier position at the specified (manipulation stage) times.

        Args:
            times (float): Times (in ms) at which positions are calculated.
        Returns:
            list: Barrier positions (in microns) at desired times.
        """
        return interpolate_1d_list(
            self.times_ms,
            self.positions_um,
            Projected.get_corrected_times(times=times),
            self.interpolation,
        )

    def get_position(self, time: list) -> list:
        """Calculate barrier position at the specified time.

        Args:
            time (float): Time (in ms) at which position is calculated.
        Returns:
            list: Barrier center position (in microns) at the specified time.
        """
        return self.get_positions(times=[time])[0]

    def get_heights(self, times: list) -> list:
        """Get barrier heights at the specified list of times

        Args:
            times (float): Times (ms) at which the heights are calculated.
        Returns:
            list: Barrier heights (kHz) at specified times.
        """
        return interpolate_1d_list(
            self.times_ms,
            self.heights_khz,
            Projected.get_corrected_times(times=times),
            self.interpolation,
        )

    def get_height(self, time: float) -> list:
        """Get barrier height at the specified time

        Args:
            time (float): Times (ms) at which the height is calculated.
        Returns:
            list: Barrier heights (kHz) at desired times.
        """
        return self.get_heights(times=[time])[0]

    def get_widths(self, times: list) -> list:
        """Get barrier widths at the specified list of times

        Args:
            times (float): Times (ms) at which the widths are calculated.
        Returns:
            list: Barrier widths (in microns) at the specified times.
        """
        return interpolate_1d_list(
            self.times_ms,
            self.widths_um,
            Projected.get_corrected_times(times=times),
            self.interpolation,
        )

    def get_width(self, time: float) -> list:
        """Get barrier width at the specified time

        Args:
            time (float): Times (ms) at which the heights are calculated.
        Returns:
            list: Barrier (half) width (um) at the specified time.
        """
        return self.get_widths(times=[time])[0]

    def get_ideal_potential(
        self, time: float = 0.0, positions: list = Projected.PROJECTED_SPOTS
    ) -> list:
        """Ideal barrier potential energy at given positions and the specified time
            without taking into account finite projection system resolution or
            update timing of projected light

        Args:
            time_ms (float): Time (in ms) at which the potential is calculated
            positions_um (list, optional):
                Positions (um) at which the potential energies are evaluated.
                Defaults to range(-50, 51, 1).

        Returns:
            list: Potential energies (in kHz) at the input positions
        """
        h = self.get_height(time)
        p = self.get_position(time)
        w = self.get_width(time)
        potential = [0] * len(positions)
        if h <= 0 or w <= 0 or not self.is_active(time):
            return potential
        if self.shape == "SQUARE":  # width = half width
            potential = [0 if (x < p - w or x > p + w) else h for x in positions]
        elif self.shape == "LORENTZIAN":  # width == HWHM (half-width half-max)
            potential = [h / (1 + ((x - p) / w) ** 2) for x in positions]
        elif self.shape == "GAUSSIAN":  # width = sigma (Gaussian width)
            potential = [h * np.exp(-((x - p) ** 2) / (2 * w**2)) for x in positions]
        return potential

    def get_potential(
        self, time: float, positions: list = Projected.PROJECTED_SPOTS
    ) -> list:
        """Calculates the optical potential associated with this Barrier object, taking
        into account the actual implementation of the Oqtant projection system.

        Args:
            time (float): time, in ms, at which the potential should be evaluated
            positions (list): positions, in microns, where the potential should be evaluated

        Returns:
            list: Potential energies, in kHz, at the requested positions and time
        """
        return Projected.get_actual_potential(
            self.get_ideal_potential, time=time, positions=positions
        )

    def show_dynamics(self):
        """Plots the position, width, and height of the barrier over time."""
        tstart = min(self.times_ms)
        tstop = max(self.times_ms)
        times = np.linspace(
            tstart,
            tstop,
            num=int((tstop - tstart) / Projected.UPDATE_PERIOD),
            endpoint=True,
        )
        fig, ax1 = plt.subplots()

        # plot position and width vs time
        style = "steps-pre"
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("position or width (microns)")
        ax1.set_xlim([-1, self.times_ms[-1] + 1])
        ax1.set_ylim([Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1])
        (ln1,) = plt.plot(
            times, self.get_positions(times), color=color, drawstyle=style
        )
        plt.plot(
            self.times_ms,
            self.get_positions(self.times_ms),
            ".",
            color=color,
        )
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln2,) = plt.plot(times, self.get_widths(times), color=color, drawstyle=style)
        plt.plot(self.times_ms, self.get_widths(self.times_ms), ".", color=color)

        # plot height on the same time axis
        ax2 = ax1.twinx()
        ax2.set_ylabel("height (kHz)")
        ax2.set_ylim([0, 100])
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln3,) = plt.plot(times, self.get_heights(times), color=color, drawstyle=style)
        plt.plot(self.times_ms, self.get_heights(self.times_ms), ".", color=color)

        # shared setup
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.legend([ln1, ln2, ln3], ["position", "width", "height"], loc="upper left")
        plt.title("Barrier dynamics")
        fig.tight_layout()
        plt.show()

    def show_potential(
        self,
        times: list = [0.0],
        xlimits: list = [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1],
        ylimits: list = [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1],
        include_ideal: bool = False,
    ):
        """Plots the potential energy as a function of position for this snapshot.

        Args:
            xlimits (list, optional): Plot limits for x axis.
                Defaults to [Projected.POSITION_MIN - 1, Projected.POSITION_MAX + 1].
            ylimits (list, optional): Plot limits for y axis.
                Defaults to [Projected.ENERGY_MIN - 1, Projected.ENERGY_MAX + 1].
            include_ideal (bool, optional): Option to include target potential in plot.
                Defaults to False.
        """

        positions = np.arange(np.floor(min(xlimits)), np.ceil(max(xlimits)) + 1, 0.1)

        fig, ax1 = plt.subplots()
        ax = plt.gca()
        lns = []
        labs = []
        for time in times:
            color = next(ax._get_lines.prop_cycler)["color"]
            potential = self.get_potential(time=time, positions=positions)
            (ln,) = plt.plot(positions, potential, color=color)
            lns.append(ln)
            labs.append("t = " + str(time) + " ms")
            if include_ideal:
                potentials_ideal = self.get_ideal_potential(
                    time=time, positions=positions
                )
                (ln,) = plt.plot(positions, potentials_ideal, "--", color=color)
                lns.append(ln)
                labs.append("t = " + str(time) + "ms (ideal)")

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        ax1.legend(lns, labs, loc=0)
        plt.show()
