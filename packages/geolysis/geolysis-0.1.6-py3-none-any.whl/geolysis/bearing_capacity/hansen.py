from dataclasses import dataclass

from geolysis.bearing_capacity import FootingShape, FootingSize, FoundationSize
from geolysis.utils import PI, exp, tan


class HansenFactors:
    def __init__(
        self,
        soil_friction_angle: float,
        cohesion: float,
        beta: float,
        total_vertical_load: float,
        foundation_size: FoundationSize,
        footing_shape: FootingShape,
    ) -> None:
        self.soil_friction_angle = soil_friction_angle
        self.cohesion = cohesion
        self.beta = beta
        self.total_vertical_load = total_vertical_load
        self.foundation_size = foundation_size
        self.footing_shape = footing_shape

    @property
    def nc(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = (N_q - 1) \cot \phi

        """
        x_1 = 1 / tan(self.soil_friction_angle)
        x_2 = self.nq - 1.0

        return x_1 * x_2

    @property
    def nq(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 \left(45 + \frac{\phi}{2} \right)
                  \left(e^{\pi \tan \phi}\right)

        """
        x_1 = tan(45 + self.soil_friction_angle / 2) ** 2
        x_2 = exp(PI * tan(self.soil_friction_angle))

        return x_1 * x_2

    @property
    def ngamma(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_q`.

        .. math::

            N_\gamma = 1.8(N_q - 1) \tan \phi
        """
        return 1.8 * (self.nq - 1.0) * tan(self.soil_friction_angle)

    @property
    def d2w(self) -> float:
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_c`.

        .. math::

            d_c = 1 + 0.35 \left(\frac{D_f}{B}\right)

        """
        return 1 + 0.35 * self.d2w

    @property
    def dq(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 0.35 \left(\frac{D_f}{B}\right)

        """
        return self.dc

    @property
    def dgamma(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0

        """
        return 1.0

    @property
    def _w2l(self) -> float:
        return self.foundation_size.w2l

    @property
    def sc(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_c`.

        - for strip footing |rarr| :math:`s_c = 1`
        - for rectangular footing |rarr| :math:`s_c = 1 + 0.2 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_c = 1.3`
        - for circular footing |rarr| :math:`s_c = 1.3`

        """
        _sc: float

        if self.footing_shape is FootingShape.STRIP:
            _sc = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sc = 1.3

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sc = 1 + 0.2 * self._w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sc

    @property
    def sq(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_q`.

        - for strip footing |rarr| :math:`s_q = 1`
        - for rectangular footing |rarr| :math:`s_q = 1 + 0.2 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_q = 1.2`
        - for circular footing |rarr| :math:`s_q = 1.2`

        """
        _sq: float

        if self.footing_shape is FootingShape.STRIP:
            _sq = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sq = 1.2

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sq = 1 + 0.2 * self._w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sq

    @property
    def sgamma(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_\gamma`.

        - for strip footing |rarr| :math:`s_\gamma = 1`
        - for rectangular footing |rarr| :math:`s_\gamma = 1 - 0.4 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_\gamma = 0.8`
        - for circular footing |rarr| :math:`s_\gamma = 0.6`

        """
        _sgamma: float

        if self.footing_shape is FootingShape.STRIP:
            _sgamma = 1.0

        elif self.footing_shape is FootingShape.SQUARE:
            _sgamma = 0.8

        elif self.footing_shape is FootingShape.CIRCULAR:
            _sgamma = 0.6

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sgamma = 1 - 0.4 * self._w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sgamma

    @property
    def ic(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_c`.

        .. math::

            i_c = 1 - \left(\dfrac{\beta}{2cBL}\right)

        """
        x_1 = (
            2
            * self.cohesion
            * self.foundation_size.width
            * self.foundation_size.length
        )
        return 1 - self.beta / x_1

    @property
    def iq(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_q`.

        .. math::

            i_q = 1 - 1.5 \cdot \dfrac{\beta}{V}

        """
        return 1 - (1.5 * self.beta) / self.total_vertical_load

    @property
    def igamma(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = \left(1 - 1.5 \cdot \dfrac{\beta}{V} \right)^2

        """

        return self.iq**2


class HansenBearingCapacity:
    r"""Ultimate bearing capacity according to ``Hansen``.

    :param cohesion: Cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param soil_unit_weight: Unit weight of soil :math:`(kN/m^3)`
    :type soil_unit_weight: float
    :param foundation_size: Size of foundation
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :param beta: Inclination of the load on the foundation with respect to the
        vertical (degrees)
    :type beta: float
    :param total_vertical_load: Total vertical load on foundation
    :type total_vertical_load: float
    :param footing_shape: Shape of the footing
    :type footing_shape: float
    """

    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        soil_friction_angle: float,
        beta: float,
        total_vertical_load: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.footing_shape = footing_shape
        self.total_vertical_load = total_vertical_load

        self.hansen_factors = HansenFactors(
            soil_friction_angle,
            cohesion,
            beta,
            total_vertical_load,
            foundation_size,
            footing_shape,
        )

    def ultimate(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Hansen``.

        .. math::

            q_u = c \cdot N_c \cdot s_c \cdot d_c \cdot i_c \,
                  + q \cdot N_q \cdot s_q \cdot d_q \cdot i_q \,
                  + 0.5 \cdot \gamma \cdot B \cdot N_\gamma
                  \cdot s_\gamma \cdot d_\gamma \cdot i_\gamma

        """
        x_1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x_2 = self.soil_unit_weight * self.foundation_size.depth
        x_3 = self.nq * self.sq * self.dq * self.iq
        x_4 = self.soil_unit_weight * self.foundation_size.width
        x_5 = self.ngamma * self.sgamma * self.dgamma * self.igamma

        return x_1 + (x_2 * x_3) + (0.5 * x_4 * x_5)

    @property
    def nc(self) -> float:
        return self.hansen_factors.nc

    @property
    def nq(self) -> float:
        return self.hansen_factors.nq

    @property
    def ngamma(self) -> float:
        return self.hansen_factors.ngamma

    @property
    def dc(self) -> float:
        return self.hansen_factors.dc

    @property
    def dq(self) -> float:
        return self.hansen_factors.dq

    @property
    def dgamma(self) -> float:
        return self.hansen_factors.dgamma

    @property
    def sc(self) -> float:
        return self.hansen_factors.sc

    @property
    def sq(self) -> float:
        return self.hansen_factors.sq

    @property
    def sgamma(self) -> float:
        return self.hansen_factors.sgamma

    @property
    def ic(self) -> float:
        return self.hansen_factors.ic

    @property
    def iq(self) -> float:
        return self.hansen_factors.iq

    @property
    def igamma(self) -> float:
        return self.hansen_factors.igamma
