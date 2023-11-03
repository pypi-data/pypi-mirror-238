"""Module with the class N2PProperty and all its derivated class"""

from abc import ABC
import math
from NaxToPy.Core.Errors.N2PLog import N2PLog

failuredict = {0: "UNKNOWN",
               1: "HILL",
               2: "HOFF",
               3: "TASI",
               4: "STRN",
               5: "HASH",
               6: "PUCK",
               7: "STRS"}


# Clase base para el resto de propiedades ------------------------------------------------------------------------------
class N2PProperty(ABC):
    """Main abstract class for properties. The rest of the properties derive from it"""

    def __init__(self, information, model_father):
        """
        Constructor of the class N2PProperty. As Abaqus don't have ids for the props
        """

        self.__info__ = information
        self.__model__ = model_father

    @property
    def ID(self) -> int:
        if self.__info__.ID is None or self.__info__.ID == 0:
            N2PLog.Error.E209(self.Name)
        return self.__info__.ID

    @property
    def PartID(self) -> int:
        if self.__info__.PartID is None:
            N2PLog.Error.E210(self.Name)
        return self.__info__.PartID

    @property
    def InternalID(self) -> int:
        return self.__info__.InternalID

    @property
    def Name(self) -> str:
        return self.__info__.Name

    @property
    def PropertyType(self) -> str:
        return self.__info__.PropertyType.ToString()



    # Special Method for Object Representation -------------------------------------------------------------------------
    def __repr__(self):
        if self.__model__.Solver == "Abaqus":
            reprs = f"N2PProperty(\'{self.Name}\', \'{self.PropertyType}\')"
        else:
            reprs = f"N2PProperty({self.ID}, \'{self.PropertyType}\')"
        return reprs
    # ------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Clase para definir propiedades de compuestos -------------------------------------------------------------------------
class N2PComp(N2PProperty):
    """
    Class for defining compound properties. It derives from N2PProperty.
    """

    def __init__(self, information, model_father):
        """
        Constructor of the class N2PComp. It has base in N2PProperty
        """
        super().__init__(information, model_father)
        self.__info__ = information
        self.__model__ = model_father

    @property
    def NumPiles(self) -> int:
        return self.__info__.NumPiles

    @property
    def IsSymetric(self) -> bool:
        return self.__info__.IsSymetric

    @property
    def NSM(self) -> float:
        return self.__info__.NSM

    @property
    def AllowShear(self) -> float:
        return self.__info__.AllowShear

    @property
    def FailTh(self) -> str:
        return self.__info__.FailTh.ToString()

    @property
    def DampCoef(self) -> float:
        return self.__info__.DampCoef

    @property
    def MatID(self) -> tuple[int]:
        return tuple(self.__info__.Mat)

    @property
    def Thickness(self) -> tuple[float]:
        return tuple(self.__info__.Thickness)

    @property
    def Theta(self) -> tuple[float]:
        return tuple(self.__info__.Theta)

    @property
    def SOut(self) -> tuple[bool]:
        return tuple(self.__info__.SOut)

    @property
    def Plies(self) -> list[tuple]:
        """
        It returns a list of tuple. A tuple for a ply. Plies have four data: (MatID, Thickness, Theta, SOut)
        """
        return [(self.MatID[i], self.Thickness[i], self.Theta[i]) for i in range(self.NumPiles)]

    @property
    def QMatrix(self) -> list:
        q11_t = 0
        q12_t = 0
        q22_t = 0
        q16_t = 0
        q26_t = 0
        q66_t = 0

        t_thick = sum(self.Thickness)

        for i in range(self.NumPiles):
            c = math.cos(math.radians(self.Theta[i]))
            s = math.sin(math.radians(self.Theta[i]))

            thick = self.Thickness[i]
            rel_thick = thick/t_thick

            mat = self.__model__._N2PModelContent__material_dict[self.MatID[i]]

            s11 = 1 / mat.YoungX
            s22 = 1 / mat.YoungY
            s12 = (-1) * mat.PoissonXY / mat.YoungX
            s66 = 1 / mat.ShearXY

            # Calculate the terms of the reduced stiffness matrix Q in the laminae coordinate system
            q11 = s22 / (s11 * s22 - s12 ** 2)
            q12 = (-1) * s12 / (s11 * s22 - s12 ** 2)
            q22 = s11 / (s11 * s22 - s12 ** 2)
            q66 = 1 / s66

            # Calculate the terms of the reduced stiffness matrix Q' in the laminate coordinate system
            q11_t += (q11 * c ** 4 + 2 * (q12 + 2 * q66) * s ** 2 * c ** 2 + q22 * s ** 4) * rel_thick
            q12_t += ((q11 + q22 - 4 * q66) * s ** 2 * c ** 2 + q12 * (s ** 4 + c ** 4)) * rel_thick
            q22_t += (q11 * s ** 4 + 2 * (q12 + 2 * q66) * s ** 2 * c ** 2 + q22 * c ** 4) * rel_thick
            q16_t += ((q11 - q12 - 2 * q66) * s * c ** 3 + (q12 - q22 + 2 * q66) * s ** 3 * c) * rel_thick
            q26_t += ((q11 - q12 - 2 * q66) * s ** 3 * c + (q12 - q22 + 2 * q66) * s * c ** 3) * rel_thick
            q66_t += ((q11 + q22 - 2 * q12 - 2 * q66) * s ** 2 * c ** 2 + q66 * (s ** 4 + c ** 4)) * rel_thick

        Q = [[q11_t, q12_t, q16_t],
             [q12_t, q22_t, q26_t],
             [q16_t, q26_t, q66_t]]

        return Q

    @property
    def ABDMatrix(self) -> tuple[list, list, list]:

        # Nótese que las unidades de las matrices de rigidez ABD deben ser consistentes: A [N/m], B [N] y D [N·m].

        a11 = 0
        a12 = 0
        a22 = 0
        a16 = 0
        a26 = 0
        a66 = 0

        b11 = 0
        b12 = 0
        b22 = 0
        b16 = 0
        b26 = 0
        b66 = 0

        d11 = 0
        d12 = 0
        d22 = 0
        d16 = 0
        d26 = 0
        d66 = 0

        t_thick = sum(self.Thickness)
        low_reference = - sum(self.Thickness) / 2

        for i in range(self.NumPiles):

            c = math.cos(math.radians(self.Theta[i]))
            s = math.sin(math.radians(self.Theta[i]))
            
            thick = self.Thickness[i]

            centroid = low_reference + thick/2

            mat = self.__model__._N2PModelContent__material_dict[self.MatID[i]]

            s11 = 1 / mat.YoungX
            s22 = 1 / mat.YoungY
            s12 = (-1) * mat.PoissonXY / mat.YoungX
            s66 = 1 / mat.ShearXY

            # Calculate the terms of the reduced stiffness matrix Q in the laminae coordinate system
            q11 = s22 / (s11 * s22 - s12 ** 2)
            q12 = (-1) * s12 / (s11 * s22 - s12 ** 2)
            q22 = s11 / (s11 * s22 - s12 ** 2)
            q66 = 1 / s66

            # Calculate the terms of the reduced stiffness matrix Q' in the laminate coordinate system
            q11_t = q11 * c ** 4 + 2 * (q12 + 2 * q66) * s ** 2 * c ** 2 + q22 * s ** 4
            q12_t = (q11 + q22 - 4 * q66) * s ** 2 * c ** 2 + q12 * (s ** 4 + c ** 4)
            q22_t = q11 * s ** 4 + 2 * (q12 + 2 * q66) * s ** 2 * c ** 2 + q22 * c ** 4
            q16_t = (q11 - q12 - 2 * q66) * s * c ** 3 + (q12 - q22 + 2 * q66) * s ** 3 * c
            q26_t = (q11 - q12 - 2 * q66) * s ** 3 * c + (q12 - q22 + 2 * q66) * s * c ** 3
            q66_t = (q11 + q22 - 2 * q12 - 2 * q66) * s ** 2 * c ** 2 + q66 * (s ** 4 + c ** 4)

            # Calculate the terms of the extensional stiffness matrix A in the laminate coordinate system
            a11 += q11_t * thick
            a12 += q12_t * thick
            a22 += q22_t * thick
            a16 += q16_t * thick
            a26 += q26_t * thick
            a66 += q66_t * thick

            b11 += q11_t * centroid * thick
            b12 += q12_t * centroid * thick
            b22 += q22_t * centroid * thick
            b16 += q16_t * centroid * thick
            b26 += q26_t * centroid * thick
            b66 += q66_t * centroid * thick

            d11 += q11_t * ((centroid)**2 * thick + (thick**3)/12)
            d12 += q12_t * ((centroid)**2 * thick + (thick**3)/12)
            d22 += q22_t * ((centroid)**2 * thick + (thick**3)/12)
            d16 += q16_t * ((centroid)**2 * thick + (thick**3)/12)
            d26 += q26_t * ((centroid)**2 * thick + (thick**3)/12)
            d66 += q66_t * ((centroid)**2 * thick + (thick**3)/12)

            low_reference += thick

        A = [[a11, a12, a16],
             [a12, a22, a26],
             [a16, a26, a66]]  # extensional_matrix
        
        B = [[b11, b12, b16],
             [b12, b22, b26],
             [b16, b26, b66]]  # bending_matrix
        
        D = [[d11, d12, d16],
             [d12, d22, d26],
             [d16, d26, d66]]  # copluing_matrix

        return A, B, D
# ----------------------------------------------------------------------------------------------------------------------


# Clase para definir propiedades de tipo placa -------------------------------------------------------------------------
class N2PShell(N2PProperty):
    """
    Class for defining shell properties. It derives from N2PProperty.
    """

    def __init__(self, information, model_father):
        """
        Constructor of the class N2PShell. It has base in N2PProperty
        """
        super().__init__(information, model_father)
        self.__info__ = information
        self.__model__ = model_father

    @property
    def MatMemID(self) -> int:
        return self.__info__.MatMemID

    @property
    def MatBenID(self) -> int:
        return self.__info__.MatBenID

    @property
    def MatSheID(self) -> int:
        return self.__info__.MatSheID

    @property
    def Thickness(self) -> float:
        return self.__info__.Thickness

    @property
    def BenMR(self) -> float:
        return self.__info__.BenMR

    @property
    def TrShThickness(self) -> float:
        return self.__info__.TrShThickness

    @property
    def NSM(self) -> float:
        return self.__info__.NSM

    @property
    def FiberDist(self) -> tuple[float, float]:
        """Fiber distances for stress calculations. The positive direction is determined by the right-hand rule, and the
        order in which the grid points are listed on the connection entry"""
        return tuple(self.__info__.FiberDist)
# ----------------------------------------------------------------------------------------------------------------------


# Clase para definir propiedades de tipo solido -------------------------------------------------------------------------
class N2PSolid(N2PProperty):
    """
    Class for defining solid properties. It derives from N2PProperty.
    """

    def __init__(self, information, model_father):
        """
        Constructor of the class N2PSolid. It has base in N2PProperty
        """
        super().__init__(information, model_father)
        self.__info__ = information
        self.__model__ = model_father

    @property
    def MatID(self) -> int:
        return self.__info__.MatID

    @property
    def Cordm(self) -> int:
        return self.__info__.Cordm

    @property
    def IntNet(self) -> str:
        return self.__info__.IntNet.strip()

    @property
    def LocStrssOut(self) -> str:
        return self.__info__.LocStrssOut.strip()

    @property
    def IntSch(self) -> str:
        return self.__info__.IntSch.strip()

    @property
    def Fluid(self) -> str:
        return self.__info__.Fluid
