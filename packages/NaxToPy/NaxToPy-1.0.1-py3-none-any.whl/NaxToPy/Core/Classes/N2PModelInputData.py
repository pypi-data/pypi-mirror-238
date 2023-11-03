"""Module with de definition of N2PModelInputData"""
import array
import System


class _N2PField:
    """Class defined only for Typing"""
    def ToReal(self):
        """Converts the Field object of a Table of a N2PCard into a float"""
        pass
    def ToCharacter(self):
        """Converts the Field object of a Table of a N2PCard into a str"""
        pass
    def ToInteger(self):
        """Converts the Field object of a Table of a N2PCard into a int"""
        pass


class N2PInputData:
    """General class for the information in an input file of Nastran
    Attributes:
        DataType: str
        Lines: list[str, ...]
        """

    def __init__(self, inputdata):
        self.__inputdata = inputdata

    @property
    def DataType(self) -> str:
        return self.__inputdata.DataType.ToString()

    @property
    def Lines(self) -> list[str, ...]:
        return list(self.__inputdata.Lines)

    # @property
    # def FilePathId(self) -> str:
    #     return self.__inputdata.FilePathId

    # @property
    # def Children(self) -> list["N2PInputData"]:
    #     return list(self.__inputdata.Children)


class N2PCard(N2PInputData):
    """Class with the information of a bulk data card of an input file of Nastran.

    Functions:
        get_field(row:int, col:int)

    Attributes:
        DataType: str
        Lines: list[str, ...]
        Table: 2D-Array
        SuperElement: int
        CardType: str
    """

    def __init__(self, card):
        super().__init__(card)
        self.__card = card

    @property
    def Table(self) -> array.array:
        """2D Array with the information of each field of a card. This information is kept as an object.
        To actually obtain this information one of this methods should be used on a field:\n

            - ToCharacter()
            - ToReal()
            - ToInteger()

        WARNING: The user must know what type of data the filed is to use the correct method

        Example:
            id = .Table[0,1].ToInteger()
        """
        return self.__card.Table

    @property
    def SuperElement(self) -> int:
        return self.__card.SuperElement

    @property
    def CardType(self) -> str:
        return self.__card.CardType.ToString()

    def get_field(self, i: int, j: int) -> _N2PField:
        """It returns an object with the information of a field of a card. To actually obtain this information one of
        this methods should be used on a field:\n

            - ToCharacter()
            - ToReal()
            - ToInteger()

        WARNING: The user must know what type of data the filed is to use the correct method

        Example:
            id = .get_field(0, 1).ToInteger()
        """
        return self.__card.Table[i, j]


class N2PModelInputData:
    """Class with the complete data of a MEF input file (text file). \n
    Functions:
        get_cards_by_field
    Attributes:
        ListBulkDataCards: list[N2PCard, ...]
        DictionaryIDsFiles: dict
        TypeOfFile: str
    """

    def __init__(self, listbulkdatacards, inputfiledata):
        self.__listbulkdatacards = listbulkdatacards
        self.__inputfiledata = inputfiledata

    @property
    def ListBulkDataCards(self) -> list[N2PCard, ...]:
        """List with the N2PCard objects of the input FEM file. It has all bulk data cards of the model"""
        return self.__listbulkdatacards

    @property
    def DictionaryIDsFiles(self) -> dict:
        return dict(self.__inputfiledata.DictionaryIDsFiles)

    @property
    def TypeOfFile(self) -> str:
        return self.__inputfiledata.TypeOfFile.ToString()

    def get_cards_by_field(self, fields: list[str, ], row: int = 0, col: int = 0) -> list[N2PCard, ]:
        """Method that returns a list with the N2PCard objects of the input FEM file that meet the condition.
        In other words, that field is equal to the string in the position defined. If no row or column is defined, the
        string will compare with the position (0,0) of the card, that is the name of the card.
        Args:
            fields: str | list[str]
            row: int (optional)
            col: int (optional)
        Returns:
            list[N2PCard, ]
        """
        if isinstance(fields, str):
            fields = [fields]
        array_strings = System.Array[System.String]([field.strip() for field in fields])
        return [self.__listbulkdatacards[idcard] for idcard
                in self.__inputfiledata.GetCardIDsByField(array_strings, row, col)]


class CBAR(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCbar)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PBAR or PBARL entry. (Integer > 0 or blank*; Default = EID unless BAROR entry has nonzero entry in field 3.)    """
        return self.__cardinfo.PID

    @property
    def GA(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer > 0; GA ≠ GB)    """
        return self.__cardinfo.GA

    @property
    def GB(self) -> int:
        """ GB    """
        return self.__cardinfo.GB

    @property
    def X1(self) -> float:
        """ BOO       Basic                  Offset           Basic    """
        return self.__cardinfo.X1

    @property
    def X2(self) -> float:
        """ X2    """
        return self.__cardinfo.X2

    @property
    def X3(self) -> float:
        """ X3    """
        return self.__cardinfo.X3

    @property
    def G0(self) -> int:
        """ Alternate method to supply the orientation vector v using grid point G0.The direction of v is from GA to G0.v is then translated to End A. (Integer > 0; G0 ≠ GA or GB)    """
        return self.__cardinfo.G0

    @property
    def OFFT(self) -> str:
        """ BOO       Basic                  Offset           Basic    """
        return self.__cardinfo.OFFT

    @property
    def PA(self) -> int:
        """ Integers 1 through 6 anywhere in the field with no embedded blanks; Integer > 0.) Pin flags combined with offsets are not allowed for SOL 600.    """
        return self.__cardinfo.PA

    @property
    def PB(self) -> int:
        """ PB    """
        return self.__cardinfo.PB

    @property
    def W1A(self) -> float:
        """ BOO       Basic                  Offset           Basic    """
        return self.__cardinfo.W1A

    @property
    def W2A(self) -> float:
        """ W2A    """
        return self.__cardinfo.W2A

    @property
    def W3A(self) -> float:
        """ W3A    """
        return self.__cardinfo.W3A

    @property
    def W1B(self) -> float:
        """ W1B    """
        return self.__cardinfo.W1B

    @property
    def W2B(self) -> float:
        """ W2B    """
        return self.__cardinfo.W2B

    @property
    def W3B(self) -> float:
        """ W3B    """
        return self.__cardinfo.W3B



class CBEAM(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCbeam)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of PBEAM, PBCOMP or PBEAML entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def GA(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer > 0; GA ≠ GB)    """
        return self.__cardinfo.GA

    @property
    def GB(self) -> int:
        """ GB    """
        return self.__cardinfo.GB

    @property
    def X1(self) -> float:
        """ BOO       Basic                  Offset           Offset    """
        return self.__cardinfo.X1

    @property
    def X2(self) -> float:
        """ X2    """
        return self.__cardinfo.X2

    @property
    def X3(self) -> float:
        """ X3    """
        return self.__cardinfo.X3

    @property
    def G0(self) -> int:
        """ Alternate method to supply the orientation vector v using grid point G0.The direction of v is from GA to G0.v is then transferred to End A. (Integer > 0; G0 ≠ GA or GB)    """
        return self.__cardinfo.G0

    @property
    def OFFT(self) -> str:
        """ BOO       Basic                  Offset           Offset    """
        return self.__cardinfo.OFFT

    @property
    def BIT(self) -> float:
        """Built-in twist of the cross-sectional axes about the beam axis at end B relative to end A.For beam p-elements only. (Real; Default = 0.0)    """
        return self.__cardinfo.BIT

    @property
    def PA(self) -> int:
        """ Integers 1 through 6 anywhere in the field with no embedded blanks; Integer > 0.) Pin flags combined with offsets are not allowed for SOL 600.    """
        return self.__cardinfo.PA

    @property
    def PB(self) -> int:
        """ PB    """
        return self.__cardinfo.PB

    @property
    def W1A(self) -> float:
        """ BOO       Basic                  Offset           Basic    """
        return self.__cardinfo.W1A

    @property
    def W2A(self) -> float:
        """ W2A    """
        return self.__cardinfo.W2A

    @property
    def W3A(self) -> float:
        """ W3A    """
        return self.__cardinfo.W3A

    @property
    def W1B(self) -> float:
        """ W1B    """
        return self.__cardinfo.W1B

    @property
    def W2B(self) -> float:
        """ W2B    """
        return self.__cardinfo.W2B

    @property
    def W3B(self) -> float:
        """ W3B    """
        return self.__cardinfo.W3B

    @property
    def SA(self) -> int:
        """ SA and SB cannot be specified for beam p-elements. (Integers > 0 or blank)    """
        return self.__cardinfo.SA

    @property
    def SB(self) -> int:
        """ SB    """
        return self.__cardinfo.SB



class CBUSH(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCbush)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PBUSH entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def GA(self) -> int:
        """ If the distance between GA and GB is less than .0001, or if GB is blank, then CID must be specified.GB blank implies that B is grounded.    """
        return self.__cardinfo.GA

    @property
    def GB(self) -> int:
        """ GB    """
        return self.__cardinfo.GB

    @property
    def X1(self) -> float:
        """ Components of orientation vector v, from GA, in the displacement coordinate system at GA. (Real)    """
        return self.__cardinfo.X1

    @property
    def X2(self) -> float:
        """ X2    """
        return self.__cardinfo.X2

    @property
    def X3(self) -> float:
        """ X3    """
        return self.__cardinfo.X3

    @property
    def G0(self) -> int:
        """ cylindrical or spherical coordinate, GA falls on the z-axis used to define them, it is recommended that another CID be selectfced to define the element x-axis.    """
        return self.__cardinfo.G0

    @property
    def CID(self) -> int:
        """ cylindrical or spherical coordinate, GA falls on the z-axis used to define them, it is recommended that another CID be selectfced to define the element x-axis.    """
        return self.__cardinfo.CID

    @property
    def S(self) -> float:
        """ Location of spring damper. See Figure 8-19. (0.0 < Real < 1.0; Default = 0.5)    """
        return self.__cardinfo.S

    @property
    def OCID(self) -> int:
        """ If OCID = -1 or blank (default) then S is used and S1, S2, S3 are ignored. If OCID > 0, then S is ignored and S1, S2, S3 are used.    """
        return self.__cardinfo.OCID

    @property
    def S1(self) -> float:
        """ If OCID = -1 or blank (default) then S is used and S1, S2, S3 are ignored. If OCID > 0, then S is ignored and S1, S2, S3 are used.    """
        return self.__cardinfo.S1

    @property
    def S2(self) -> float:
        """ S2    """
        return self.__cardinfo.S2

    @property
    def S3(self) -> float:
        """ S3    """
        return self.__cardinfo.S3



class CELAS1(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCelas1)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PELAS entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Geometric grid point identification number. (Integer >= 0)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def C1(self) -> int:
        """ Component number. (0 < Integer < 6; blank or zero if scalar point.)    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> int:
        """ C2    """
        return self.__cardinfo.C2



class CELAS2(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCelas2)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def K(self) -> float:
        """ Stiffness of the scalar spring. (Real)    """
        return self.__cardinfo.K

    @property
    def G1(self) -> int:
        """ Geometric grid point identification number. (Integer >= 0)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def C1(self) -> int:
        """ Component number. (0 < Integer < 6; blank or zero if scalar point.)    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> int:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def GE(self) -> float:
        """ To obtain the damping coefficient GE, multiply the critical damping ratio C ⁄ C0 by 2.0.    """
        return self.__cardinfo.GE

    @property
    def S(self) -> float:
        """ Stress coefficient (Real).    """
        return self.__cardinfo.S



class CELAS3(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCelas3)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PELAS entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def S1(self) -> int:
        """ Scalar point identification numbers. (Integer >= 0)    """
        return self.__cardinfo.S1

    @property
    def S2(self) -> int:
        """ S2    """
        return self.__cardinfo.S2



class CELAS4(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCelas4)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def K(self) -> float:
        """ Stiffness of the scalar spring. (Real)    """
        return self.__cardinfo.K

    @property
    def S1(self) -> int:
        """ Scalar point identification numbers. (Integer >= 0; S1 ≠ S2)    """
        return self.__cardinfo.S1

    @property
    def S2(self) -> int:
        """ S2    """
        return self.__cardinfo.S2



class CFAST(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCfast)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (0 < Integer < 100,000,000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PFAST entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def TYPE(self) -> str:
        """ four CQUAD8 elements with midside nodes and no nodes in common between each CQUAD8 as that would total to 32 unique grids for the patch.)    """
        return self.__cardinfo.TYPE

    @property
    def IDA(self) -> int:
        """ Property id (for PROP option) or Element id (for ELEM option) defining patches A and B. IDA ≠ IDB (Integer > 0)    """
        return self.__cardinfo.IDA

    @property
    def IDB(self) -> int:
        """ IDB    """
        return self.__cardinfo.IDB

    @property
    def GS(self) -> int:
        """ Diagnostic printouts, checkout runs and control of search and projection parameters are requested on the SWLDPRM Bulk Data entry.    """
        return self.__cardinfo.GS

    @property
    def GA(self) -> int:
        """ Diagnostic printouts, checkout runs and control of search and projection parameters are requested on the SWLDPRM Bulk Data entry.    """
        return self.__cardinfo.GA

    @property
    def GB(self) -> int:
        """ GB    """
        return self.__cardinfo.GB

    @property
    def XS(self) -> float:
        """ Diagnostic printouts, checkout runs and control of search and projection parameters are requested on the SWLDPRM Bulk Data entry.    """
        return self.__cardinfo.XS

    @property
    def YS(self) -> float:
        """ YS    """
        return self.__cardinfo.YS

    @property
    def ZS(self) -> float:
        """ ZS    """
        return self.__cardinfo.ZS



class CHEXANAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardChexaNas)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (0 < Integer < 100000000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def G11(self) -> int:
        """ G11    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> int:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> int:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> int:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> int:
        """ G15    """
        return self.__cardinfo.G15

    @property
    def G16(self) -> int:
        """ G16    """
        return self.__cardinfo.G16

    @property
    def G17(self) -> int:
        """ G17    """
        return self.__cardinfo.G17

    @property
    def G18(self) -> int:
        """ G18    """
        return self.__cardinfo.G18

    @property
    def G19(self) -> int:
        """ G19    """
        return self.__cardinfo.G19

    @property
    def G20(self) -> int:
        """ G20    """
        return self.__cardinfo.G20



class CHEXAOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardChexaOpt)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (0 < Integer < 100000000)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def G11(self) -> int:
        """ G11    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> int:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> int:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> int:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> int:
        """ G15    """
        return self.__cardinfo.G15

    @property
    def G16(self) -> int:
        """ G16    """
        return self.__cardinfo.G16

    @property
    def G17(self) -> int:
        """ G17    """
        return self.__cardinfo.G17

    @property
    def G18(self) -> int:
        """ G18    """
        return self.__cardinfo.G18

    @property
    def G19(self) -> int:
        """ G19    """
        return self.__cardinfo.G19

    @property
    def G20(self) -> int:
        """ G20    """
        return self.__cardinfo.G20

    @property
    def CORDM(self) -> str:
        """ Flag indicating that the following field(s) reference data to determine the material coordinate system.    """
        return self.__cardinfo.CORDM

    @property
    def CID(self) -> int:
        """ Material coordinate system identification number. Default = 0 (Integer ≥ -1)    """
        return self.__cardinfo.CID

    @property
    def THETA(self) -> float:
        """ towards the elemental Y-axis. Default = blank (Real)    """
        return self.__cardinfo.THETA

    @property
    def PHI(self) -> float:
        """ Note: For positive PHI, the new X-axis is rotated towards the elemental Z-axis. Default = blank (Real)    """
        return self.__cardinfo.PHI



class CONM2(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardConm2)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def G(self) -> int:
        """ CardGrid point identification number. (Integer > 0)    """
        return self.__cardinfo.G

    @property
    def CID(self) -> int:
        """ Coordinate system identification number.For CID of -1; see X1, X2, X3 low. (Integer > -1; Default = 0)    """
        return self.__cardinfo.CID

    @property
    def M(self) -> float:
        """ Mass value. (Real)    """
        return self.__cardinfo.M

    @property
    def X1(self) -> float:
        """ case X1, X2, X3 are the coordinates, not offsets, of the center of gravity of the mass in the basic coordinate system. (Real)    """
        return self.__cardinfo.X1

    @property
    def X2(self) -> float:
        """ X2    """
        return self.__cardinfo.X2

    @property
    def X3(self) -> float:
        """ X3    """
        return self.__cardinfo.X3

    @property
    def I11(self) -> float:
        """ system is implied. (For I11, I22, and I33; Real > 0.0; for I21, I31, and I32; Real)    """
        return self.__cardinfo.I11

    @property
    def I21(self) -> float:
        """ I21    """
        return self.__cardinfo.I21

    @property
    def I22(self) -> float:
        """ I22    """
        return self.__cardinfo.I22

    @property
    def I31(self) -> float:
        """ I31    """
        return self.__cardinfo.I31

    @property
    def I32(self) -> float:
        """ I32    """
        return self.__cardinfo.I32

    @property
    def I33(self) -> float:
        """ I33    """
        return self.__cardinfo.I33



class CORD1C(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord1c)    """
        return self.__cardinfo.CharName

    @property
    def CIDA(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CIDA

    @property
    def CIDB(self) -> int:
        """ CIDB    """
        return self.__cardinfo.CIDB

    @property
    def G1A(self) -> int:
        """ CardGrid point identification numbers. (Integer > 0; G1A ≠ G2A ≠ G3AG1B ≠ G2B ≠ G3B;)    """
        return self.__cardinfo.G1A

    @property
    def G2A(self) -> int:
        """ G2A    """
        return self.__cardinfo.G2A

    @property
    def G3A(self) -> int:
        """ G3A    """
        return self.__cardinfo.G3A

    @property
    def G1B(self) -> int:
        """ G1B    """
        return self.__cardinfo.G1B

    @property
    def G2B(self) -> int:
        """ G2B    """
        return self.__cardinfo.G2B

    @property
    def G3B(self) -> int:
        """ G3B    """
        return self.__cardinfo.G3B



class CORD1R(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord1r)    """
        return self.__cardinfo.CharName

    @property
    def CIDA(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CIDA

    @property
    def CIDB(self) -> int:
        """ CIDB    """
        return self.__cardinfo.CIDB

    @property
    def G1A(self) -> int:
        """ CardGrid point identification numbers. (Integer > 0; G1A ≠ G2A ≠ G3AG1B ≠ G2B ≠ G3B;)    """
        return self.__cardinfo.G1A

    @property
    def G2A(self) -> int:
        """ G2A    """
        return self.__cardinfo.G2A

    @property
    def G3A(self) -> int:
        """ G3A    """
        return self.__cardinfo.G3A

    @property
    def G1B(self) -> int:
        """ G1B    """
        return self.__cardinfo.G1B

    @property
    def G2B(self) -> int:
        """ G2B    """
        return self.__cardinfo.G2B

    @property
    def G3B(self) -> int:
        """ G3B    """
        return self.__cardinfo.G3B



class CORD1S(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord1s)    """
        return self.__cardinfo.CharName

    @property
    def CIDA(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CIDA

    @property
    def CIDB(self) -> int:
        """ CIDB    """
        return self.__cardinfo.CIDB

    @property
    def G1A(self) -> int:
        """ CardGrid point identification numbers. (Integer > 0; G1A ≠ G2A ≠ G3AG1B ≠ G2B ≠ G3B;)    """
        return self.__cardinfo.G1A

    @property
    def G2A(self) -> int:
        """ G2A    """
        return self.__cardinfo.G2A

    @property
    def G3A(self) -> int:
        """ G3A    """
        return self.__cardinfo.G3A

    @property
    def G1B(self) -> int:
        """ G1B    """
        return self.__cardinfo.G1B

    @property
    def G2B(self) -> int:
        """ G2B    """
        return self.__cardinfo.G2B

    @property
    def G3B(self) -> int:
        """ G3B    """
        return self.__cardinfo.G3B



class CORD2C(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord2c)    """
        return self.__cardinfo.CharName

    @property
    def CID(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CID

    @property
    def RID(self) -> int:
        """ system.)    """
        return self.__cardinfo.RID

    @property
    def A1(self) -> float:
        """ Coordinates of three points in coordinate system defined in field 3. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def B1(self) -> float:
        """ B1    """
        return self.__cardinfo.B1

    @property
    def B2(self) -> float:
        """ B2    """
        return self.__cardinfo.B2

    @property
    def B3(self) -> float:
        """ B3    """
        return self.__cardinfo.B3

    @property
    def C1(self) -> float:
        """ C1    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> float:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def C3(self) -> float:
        """ C3    """
        return self.__cardinfo.C3



class CORD2R(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord2r)    """
        return self.__cardinfo.CharName

    @property
    def CID(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CID

    @property
    def RID(self) -> int:
        """ system.)    """
        return self.__cardinfo.RID

    @property
    def A1(self) -> float:
        """ Coordinates of three points in coordinate system defined in field 3. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def B1(self) -> float:
        """ B1    """
        return self.__cardinfo.B1

    @property
    def B2(self) -> float:
        """ B2    """
        return self.__cardinfo.B2

    @property
    def B3(self) -> float:
        """ B3    """
        return self.__cardinfo.B3

    @property
    def C1(self) -> float:
        """ C1    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> float:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def C3(self) -> float:
        """ C3    """
        return self.__cardinfo.C3



class CORD2S(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCord2s)    """
        return self.__cardinfo.CharName

    @property
    def CID(self) -> int:
        """ Coordinate system identification number. (Integer > 0)    """
        return self.__cardinfo.CID

    @property
    def RID(self) -> int:
        """ system.)    """
        return self.__cardinfo.RID

    @property
    def A1(self) -> float:
        """ Coordinates of three points in coordinate system defined in field 3. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def B1(self) -> float:
        """ B1    """
        return self.__cardinfo.B1

    @property
    def B2(self) -> float:
        """ B2    """
        return self.__cardinfo.B2

    @property
    def B3(self) -> float:
        """ B3    """
        return self.__cardinfo.B3

    @property
    def C1(self) -> float:
        """ C1    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> float:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def C3(self) -> float:
        """ C3    """
        return self.__cardinfo.C3



class CPENTANAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCpentaNas)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected grid points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def G11(self) -> int:
        """ G11    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> int:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> int:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> int:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> int:
        """ G15    """
        return self.__cardinfo.G15



class CPENTAOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCpentaOpt)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected grid points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def G11(self) -> int:
        """ G11    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> int:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> int:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> int:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> int:
        """ G15    """
        return self.__cardinfo.G15

    @property
    def CORDM(self) -> str:
        """ Flag indicating that the following field(s) reference data to determine the material coordinate system.    """
        return self.__cardinfo.CORDM

    @property
    def CID(self) -> int:
        """ Material coordinate system identification number. Default = 0 (Integer ≥ -1)    """
        return self.__cardinfo.CID

    @property
    def THETA(self) -> float:
        """ towards the elemental Y-axis. Default = blank (Real)    """
        return self.__cardinfo.THETA

    @property
    def PHI(self) -> float:
        """ Note: For positive PHI, the new X-axis is rotated towards the elemental Z-axis. Default = blank (Real)    """
        return self.__cardinfo.PHI



class CPYRA(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCpyra)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Unique element identification number. No default (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """A PSOLID property entry identification number. Default = EID (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. Default = blank(Integer ≥ 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def G11(self) -> int:
        """ G11    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> int:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> int:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def CORDM(self) -> str:
        """ Flag indicating that the following field reference data to determine the material coordinate system.    """
        return self.__cardinfo.CORDM

    @property
    def CID(self) -> int:
        """ Material coordinate system identification number. Default = 0 (Integer ≥ -1)    """
        return self.__cardinfo.CID



class CQUAD4(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCquad4, CardCquad4*, *CardCquad4, ...)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSHELL, PCOMP, or PLPLANE entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integers > 0, all unique.)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def THETA(self) -> float:
        """ Material property orientation angle in degrees. THETA is ignored for hyperelastic elements.See Figure 8-46. (Real; Default = 0.0)    """
        return self.__cardinfo.THETA

    @property
    def MCID(self) -> int:
        """ (Integer >= 0; If blank, then THETA = 0.0 is assumed.)    """
        return self.__cardinfo.MCID

    @property
    def ZOFFS(self) -> float:
        """ Offset from the surface of grid points to the element reference plane. ZOFFS is ignored for hyperelastic elements.See Remark 6. (Real)    """
        return self.__cardinfo.ZOFFS

    @property
    def TFLAG(self) -> int:
        """ An integer flag, signifying the meaning of the Ti values. (Integer 0, 1, or blank)    """
        return self.__cardinfo.TFLAG

    @property
    def T1(self) -> float:
        """ set equal to the value of T on the PSHELL entry.    """
        return self.__cardinfo.T1

    @property
    def T2(self) -> float:
        """ T2    """
        return self.__cardinfo.T2

    @property
    def T3(self) -> float:
        """ T3    """
        return self.__cardinfo.T3

    @property
    def T4(self) -> float:
        """ T4    """
        return self.__cardinfo.T4



class CQUAD8(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCquad8, CardCquad8*, *CardCquad8, ...)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSHELL, PCOMP, or PLPLANE entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected corner grid points.Required data for all four grid points. (Unique Integers > 0)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """Identification numbers of connected edge grid points. Optional data for any or all four grid points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def T1(self) -> float:
        """ set equal to the value of T on the PSHELL entry.    """
        return self.__cardinfo.T1

    @property
    def T2(self) -> float:
        """ T2    """
        return self.__cardinfo.T2

    @property
    def T3(self) -> float:
        """ T3    """
        return self.__cardinfo.T3

    @property
    def T4(self) -> float:
        """ T4    """
        return self.__cardinfo.T4

    @property
    def THETA(self) -> float:
        """ Material property orientation angle in degrees. THETA is ignored for hyperelastic elements.See Figure 8-46. (Real; Default = 0.0)    """
        return self.__cardinfo.THETA

    @property
    def MCID(self) -> int:
        """ (Integer >= 0; If blank, then THETA = 0.0 is assumed.)    """
        return self.__cardinfo.MCID

    @property
    def ZOFFS(self) -> float:
        """ Offset from the surface of grid points to the element reference plane. ZOFFS is ignored for hyperelastic elements.See Remark 6. (Real)    """
        return self.__cardinfo.ZOFFS

    @property
    def TFLAG(self) -> int:
        """ An integer flag, signifying the meaning of the Ti values. (Integer 0, 1, or blank)    """
        return self.__cardinfo.TFLAG



class CROD(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCrod)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PROD entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer > 0 ; G1 ≠ G2)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2



class CSHEAR(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCshear)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSHEAR entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected grid points. (Integer >= 0 ; G1 ≠ G2 ≠ G3 ≠ G4)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4



class CTETRANAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCtetraNas)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected grid points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10



class CTETRAOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCtetraOpt)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSOLID or PLSOLID entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected grid points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ G4    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def G7(self) -> int:
        """ G7    """
        return self.__cardinfo.G7

    @property
    def G8(self) -> int:
        """ G8    """
        return self.__cardinfo.G8

    @property
    def G9(self) -> int:
        """ G9    """
        return self.__cardinfo.G9

    @property
    def G10(self) -> int:
        """ G10    """
        return self.__cardinfo.G10

    @property
    def CORDM(self) -> str:
        """ Flag indicating that the following field references the material coordinate system.    """
        return self.__cardinfo.CORDM

    @property
    def CID(self) -> int:
        """ Material coordinate system identification number. Default = 0 (Integer ≥ -1)    """
        return self.__cardinfo.CID



class CTRIA3(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCtria3, CardCtria3*, *CardCtria3, ...)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSHELL, PCOMP, or PLPLANE entry. (Integer > 0; Default = EID)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integers > 0, all unique.)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def THETA(self) -> float:
        """ Material property orientation angle in degrees. THETA is ignored for hyperelastic elements. (Real; Default = 0.0)    """
        return self.__cardinfo.THETA

    @property
    def MCID(self) -> int:
        """ (Integer >= 0; If blank, then THETA = 0.0 is assumed.)    """
        return self.__cardinfo.MCID

    @property
    def ZOFFS(self) -> float:
        """ Offset from the surface of grid points to the element reference plane. ZOFFS is ignored for hyperelastic elements.See Remark 3. (Real)    """
        return self.__cardinfo.ZOFFS

    @property
    def TFLAG(self) -> int:
        """ An integer flag, signifying the meaning of the Ti values. (Integer 0, 1, or blank)    """
        return self.__cardinfo.TFLAG

    @property
    def T1(self) -> float:
        """ Ti are ignored for hyperelastic elements.    """
        return self.__cardinfo.T1

    @property
    def T2(self) -> float:
        """ T2    """
        return self.__cardinfo.T2

    @property
    def T3(self) -> float:
        """ T3    """
        return self.__cardinfo.T3



class CTRIA6(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCtria6, CardCtria6*, *CardCtria6, ...)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def PID(self) -> int:
        """ Property identification number of a PSHELL, PCOMP, or PLPLANE entry. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def G1(self) -> int:
        """ Identification numbers of connected corner grid points. (Unique Integers > 0)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2

    @property
    def G3(self) -> int:
        """ G3    """
        return self.__cardinfo.G3

    @property
    def G4(self) -> int:
        """ Identification number of connected edge grid points. Optional data for any or all three points. (Integer >= 0 or blank)    """
        return self.__cardinfo.G4

    @property
    def G5(self) -> int:
        """ G5    """
        return self.__cardinfo.G5

    @property
    def G6(self) -> int:
        """ G6    """
        return self.__cardinfo.G6

    @property
    def THETA(self) -> float:
        """ Material property orientation angle in degrees. THETA is ignored for hyperelastic elements. (Real; Default = 0.0)    """
        return self.__cardinfo.THETA

    @property
    def MCID(self) -> int:
        """ (Integer >= 0; If blank, then THETA = 0.0 is assumed.)    """
        return self.__cardinfo.MCID

    @property
    def ZOFFS(self) -> float:
        """ Offset from the surface of grid points to the element reference plane. ZOFFS is ignored for hyperelastic elements.See Remark 3. (Real)    """
        return self.__cardinfo.ZOFFS

    @property
    def T1(self) -> float:
        """ Ti are ignored for hyperelastic elements.    """
        return self.__cardinfo.T1

    @property
    def T2(self) -> float:
        """ T2    """
        return self.__cardinfo.T2

    @property
    def T3(self) -> float:
        """ T3    """
        return self.__cardinfo.T3

    @property
    def TFLAG(self) -> int:
        """ An integer flag, signifying the meaning of the Ti values. (Integer 0, 1, or blank)    """
        return self.__cardinfo.TFLAG



class CWELD(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardCweld)    """
        return self.__cardinfo.CharName

    @property
    def EWID(self) -> int:
        """ See Figure 8-72 through Figure 8-76.    """
        return self.__cardinfo.EWID

    @property
    def PWID(self) -> int:
        """ Property identification number of a PWELD entry. (Integer > 0)    """
        return self.__cardinfo.PWID

    @property
    def GS(self) -> int:
        """ SWLDPRM Bulk Data entry.It is recommended to start with the default settings.    """
        return self.__cardinfo.GS

    @property
    def TYPE(self) -> str:
        """ For the other formats, GA and GB are not required. Two shell normals in the direction GA-GB are generated at GA and GB, respectively.    """
        return self.__cardinfo.TYPE

    @property
    def GA(self) -> int:
        """ Vertex grid identification number of shell A and B, respectively. (Integer > 0)    """
        return self.__cardinfo.GA

    @property
    def GB(self) -> int:
        """ GB    """
        return self.__cardinfo.GB

    @property
    def PIDA(self) -> int:
        """ Property identification numbers of PSHELL entries defining surface A and B respectively. (Integer > 0)    """
        return self.__cardinfo.PIDA

    @property
    def PIDB(self) -> int:
        """ PIDB    """
        return self.__cardinfo.PIDB

    @property
    def XS(self) -> float:
        """ not specified, then XS, YS, and ZS must be specified.    """
        return self.__cardinfo.XS

    @property
    def YS(self) -> float:
        """ YS    """
        return self.__cardinfo.YS

    @property
    def ZS(self) -> float:
        """ ZS    """
        return self.__cardinfo.ZS

    @property
    def SHIDA(self) -> int:
        """ Shell element identification numbers of elements on patch A and B, respectively. (Integer > 0)    """
        return self.__cardinfo.SHIDA

    @property
    def SHIDB(self) -> int:
        """ SHIDB    """
        return self.__cardinfo.SHIDB

    @property
    def SPTYP(self) -> str:
        """ T               Connects the shell vertex grid GS with a triangular surface patch A (T3 to T6) if surface patch B is not specified.    """
        return self.__cardinfo.SPTYP

    @property
    def GA1(self) -> int:
        """ and quadrilateral elements apply for the order of GAi and GBi, see Figure 8-75. Missing midside nodes are allowed.    """
        return self.__cardinfo.GA1

    @property
    def GA2(self) -> int:
        """ GA2    """
        return self.__cardinfo.GA2

    @property
    def GA3(self) -> int:
        """ GA3    """
        return self.__cardinfo.GA3

    @property
    def GA4(self) -> int:
        """ GA4    """
        return self.__cardinfo.GA4

    @property
    def GA5(self) -> int:
        """ GA5    """
        return self.__cardinfo.GA5

    @property
    def GA6(self) -> int:
        """ GA6    """
        return self.__cardinfo.GA6

    @property
    def GA7(self) -> int:
        """ GA7    """
        return self.__cardinfo.GA7

    @property
    def GA8(self) -> int:
        """ GA8    """
        return self.__cardinfo.GA8

    @property
    def GB1(self) -> int:
        """ and quadrilateral elements apply for the order of GAi and GBi, see Figure 8-75. Missing midside nodes are allowed.    """
        return self.__cardinfo.GB1

    @property
    def GB2(self) -> int:
        """ GB2    """
        return self.__cardinfo.GB2

    @property
    def GB3(self) -> int:
        """ GB3    """
        return self.__cardinfo.GB3

    @property
    def GB4(self) -> int:
        """ GB4    """
        return self.__cardinfo.GB4

    @property
    def GB5(self) -> int:
        """ GB5    """
        return self.__cardinfo.GB5

    @property
    def GB6(self) -> int:
        """ GB6    """
        return self.__cardinfo.GB6

    @property
    def GB7(self) -> int:
        """ GB7    """
        return self.__cardinfo.GB7

    @property
    def GB8(self) -> int:
        """ GB8    """
        return self.__cardinfo.GB8



class GRID(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (GRID, GRID*, *GRID, ...)    """
        return self.__cardinfo.CharName

    @property
    def ID(self) -> int:
        """ CardCardGrid point identification number. (0 < Integer < 100000000)     """
        return self.__cardinfo.ID

    @property
    def CP(self) -> int:
        """ Identification number of coordinate system in which the location of the grid point is defined. (Integer >= 0 or blank*)    """
        return self.__cardinfo.CP

    @property
    def X1(self) -> float:
        """ Location of the grid point in coordinate system CP. (Real; Default = 0.0)    """
        return self.__cardinfo.X1

    @property
    def X2(self) -> float:
        """ Location of the grid point in coordinate system CP. (Real; Default = 0.0)    """
        return self.__cardinfo.X2

    @property
    def X3(self) -> float:
        """ Location of the grid point in coordinate system CP. (Real; Default = 0.0)    """
        return self.__cardinfo.X3

    @property
    def CD(self) -> int:
        """ and solution vectors are defined at the grid point. (Integer >= -1 or blank)*    """
        return self.__cardinfo.CD

    @property
    def PS(self) -> int:
        """ (Any of the Integers 1 through 6 with no embedded blanks, or blank*.)    """
        return self.__cardinfo.PS

    @property
    def SEID(self) -> int:
        """Superelement identification number. (Integer >= 0; Default = 0)    """
        return self.__cardinfo.SEID



class MAT10NAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat10Nas)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def BULK(self) -> float:
        """ Bulk modulus. (Real > 0.0)    """
        return self.__cardinfo.BULK

    @property
    def RHO(self) -> float:
        """ Mass density. (Real > 0.0)    """
        return self.__cardinfo.RHO

    @property
    def C(self) -> float:
        """ Speed of sound. (Real > 0.0)    """
        return self.__cardinfo.C

    @property
    def GE(self) -> float:
        """ Fluid element damping coefficient. (Real)    """
        return self.__cardinfo.GE



class MAT10OPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat10Opt)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Unique material identification. No default (Integer > 0 or <String>)    """
        return self.__cardinfo.MID

    @property
    def BULK(self) -> float:
        """ Bulk modulus. No default (Real > 0.0)    """
        return self.__cardinfo.BULK

    @property
    def RHO(self) -> float:
        """ Mass density. Automatically computes the mass. No default (Real > 0.0)    """
        return self.__cardinfo.RHO

    @property
    def C(self) -> float:
        """ Speed of sound. No default (Real > 0.0)    """
        return self.__cardinfo.C

    @property
    def GE(self) -> float:
        """ Fluid element damping coefficient. No default (Real)    """
        return self.__cardinfo.GE

    @property
    def ALPHA(self) -> float:
        """ of interest for the analysis. No default (Real)    """
        return self.__cardinfo.ALPHA



class MAT1NAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat1Nas)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def E(self) -> float:
        """ Young’s modulus. (Real > 0.0 or blank)    """
        return self.__cardinfo.E

    @property
    def G(self) -> float:
        """ Shear modulus. (Real > 0.0 or blank)    """
        return self.__cardinfo.G

    @property
    def NU(self) -> float:
        """ Poisson’s ratio. (-1.0 < Real < 0.5 or blank)    """
        return self.__cardinfo.NU

    @property
    def RHO(self) -> float:
        """ The mass density RHO will be used to compute mass for all structural elements automatically.    """
        return self.__cardinfo.RHO

    @property
    def A(self) -> float:
        """ Thermal expansion coefficient. (Real)    """
        return self.__cardinfo.A

    @property
    def TREF(self) -> float:
        """ be used for this purpose, but TREF must be blank.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ residual structure will be updated as prescribed under the TEMPERATURE Case Control command.    """
        return self.__cardinfo.GE

    @property
    def ST(self) -> float:
        """ and have no effect on the computational procedures.See “Beam Element (CBEAM)” in Chapter 3 of the MSC.Nastran Reference Guide. (Real > 0.0 or blank)    """
        return self.__cardinfo.ST

    @property
    def SC(self) -> float:
        """ SC    """
        return self.__cardinfo.SC

    @property
    def SS(self) -> float:
        """ SS    """
        return self.__cardinfo.SS

    @property
    def MCSID(self) -> int:
        """ Material coordinate system identification number. Used only for PARAM,CURV processing.See “Parameters” on page 631. (Integer > 0 or blank)    """
        return self.__cardinfo.MCSID



class MAT1OPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat1Opt)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def E(self) -> float:
        """ Young’s modulus. (Real > 0.0 or blank)    """
        return self.__cardinfo.E

    @property
    def G(self) -> float:
        """ Shear modulus. (Real > 0.0 or blank)    """
        return self.__cardinfo.G

    @property
    def NU(self) -> float:
        """ Poisson’s ratio. If < 0.0, a warning is issued. (-1.0 < Real < 0.5 or blank)    """
        return self.__cardinfo.NU

    @property
    def RHO(self) -> float:
        """ Mass density. Used to automatically compute mass for all structural elements. No default (Real)    """
        return self.__cardinfo.RHO

    @property
    def A(self) -> float:
        """ Thermal expansion coefficient. No default (Real)    """
        return self.__cardinfo.A

    @property
    def TREF(self) -> float:
        """ Reference temperature for thermal loading. Default = 0.0 (Real)    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ Structural element damping coefficient. No default (Real)    """
        return self.__cardinfo.GE

    @property
    def ST(self) -> float:
        """ Stress limits in tension, compression and shear. Used for composite ply failure calculations. No default (Real)    """
        return self.__cardinfo.ST

    @property
    def SC(self) -> float:
        """ SC    """
        return self.__cardinfo.SC

    @property
    def SS(self) -> float:
        """ SS    """
        return self.__cardinfo.SS

    @property
    def MODULI(self) -> str:
        """ Continuation line flag for moduli temporal property.    """
        return self.__cardinfo.MODULI

    @property
    def MTIME(self) -> str:
        """ This material property is considered as the Long-term relaxed material input for viscoelasticity on the MATVE entry.    """
        return self.__cardinfo.MTIME



class MAT2NAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat2Nas)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ larger than 99999999 are used, PARAM, NOCOMPS,-1 must be specified to obtain stress output.    """
        return self.__cardinfo.MID

    @property
    def G11(self) -> float:
        """ The material property matrix. (Real)    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> float:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> float:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G22(self) -> float:
        """ G22    """
        return self.__cardinfo.G22

    @property
    def G23(self) -> float:
        """ G23    """
        return self.__cardinfo.G23

    @property
    def G33(self) -> float:
        """ G33    """
        return self.__cardinfo.G33

    @property
    def RHO(self) -> float:
        """ Mass density. (Real)    """
        return self.__cardinfo.RHO

    @property
    def A1(self) -> float:
        """ Thermal expansion coefficient vector. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def TREF(self) -> float:
        """ be used for this purpose, but TREF must be blank.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ If PARAM,W4 is not specified, GE is ignored in transient analysis. See “Parameters” on page 631.    """
        return self.__cardinfo.GE

    @property
    def ST(self) -> float:
        """ and have no effect on the computational procedures.See “Beam Element (CBEAM)” in Chapter 3 of the MSC.Nastran Reference Guide. (Real or blank)    """
        return self.__cardinfo.ST

    @property
    def SC(self) -> float:
        """ SC    """
        return self.__cardinfo.SC

    @property
    def SS(self) -> float:
        """ SS    """
        return self.__cardinfo.SS

    @property
    def MCSID(self) -> int:
        """ Material coordinate system identification number. Used only for PARAM,CURV processing.See “Parameters” on page 631. (Integer >= 0 or blank)    """
        return self.__cardinfo.MCSID



class MAT2OPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat2Opt)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def G11(self) -> float:
        """ The material property matrix. No default. (Real)    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> float:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> float:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G22(self) -> float:
        """ G22    """
        return self.__cardinfo.G22

    @property
    def G23(self) -> float:
        """ G23    """
        return self.__cardinfo.G23

    @property
    def G33(self) -> float:
        """ G33    """
        return self.__cardinfo.G33

    @property
    def RHO(self) -> float:
        """ Mass density. Used to automatically compute mass for all structural elements. No default (Real)    """
        return self.__cardinfo.RHO

    @property
    def A1(self) -> float:
        """ Thermal expansion coefficient vector. No default (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def TREF(self) -> float:
        """ Default = blank(Real or blank)    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ Structural element damping coefficient. No default (Real)    """
        return self.__cardinfo.GE

    @property
    def ST(self) -> float:
        """ Stress limits in tension, compression and shear. Used for composite ply failure calculations. No default (Real)    """
        return self.__cardinfo.ST

    @property
    def SC(self) -> float:
        """ SC    """
        return self.__cardinfo.SC

    @property
    def SS(self) -> float:
        """ SS    """
        return self.__cardinfo.SS



class MAT3(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat3)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def EX(self) -> float:
        """ Young’s moduli in the x, , and z directions, respectively. (Real > 0.0)    """
        return self.__cardinfo.EX

    @property
    def ETH(self) -> float:
        """ ETH    """
        return self.__cardinfo.ETH

    @property
    def EZ(self) -> float:
        """ EZ    """
        return self.__cardinfo.EZ

    @property
    def NUXTH(self) -> float:
        """ Poisson’s ratios (coupled strain ratios in the x , z , and zx directions, respectively). (Real)    """
        return self.__cardinfo.NUXTH

    @property
    def NUTHZ(self) -> float:
        """ NUTHZ    """
        return self.__cardinfo.NUTHZ

    @property
    def NUZX(self) -> float:
        """ NUZX    """
        return self.__cardinfo.NUZX

    @property
    def RHO(self) -> float:
        """ Mass density. (Real)    """
        return self.__cardinfo.RHO

    @property
    def GZX(self) -> float:
        """ Shear modulus. (Real > 0.0)    """
        return self.__cardinfo.GZX

    @property
    def AX(self) -> float:
        """ Thermal expansion coefficients. (Real)    """
        return self.__cardinfo.AX

    @property
    def ATH(self) -> float:
        """ ATH    """
        return self.__cardinfo.ATH

    @property
    def AZ(self) -> float:
        """ AZ    """
        return self.__cardinfo.AZ

    @property
    def TREF(self) -> float:
        """ be used for this purpose, but TREF must be blank.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ If PARAM,W4 is not specified, GE is ignored in transient analysis. See “Parameters” on page 631.    """
        return self.__cardinfo.GE



class MAT4(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat4)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def K(self) -> float:
        """ Thermal conductivity. (Blank or Real > 0.0)    """
        return self.__cardinfo.K

    @property
    def CP(self) -> float:
        """ Heat capacity per unit mass at constant pressure (specific heat). (Blank or Real > 0.0)    """
        return self.__cardinfo.CP

    @property
    def p(self) -> float:
        """ Density. (Real > 0.0; Default = 1.0)    """
        return self.__cardinfo.p

    @property
    def H(self) -> float:
        """ Free convection heat transfer coefficient. (Real or blank)    """
        return self.__cardinfo.H

    @property
    def u(self) -> float:
        """ Dynamic viscosity. See Remark 2. (Real > 0.0 or blank)    """
        return self.__cardinfo.u

    @property
    def HGEN(self) -> float:
        """ Heat generation capability used with QVOL entries. (Real > 0.0; Default = 1.0)    """
        return self.__cardinfo.HGEN

    @property
    def REFENTH(self) -> float:
        """ Reference enthalpy. (Real or blank)    """
        return self.__cardinfo.REFENTH

    @property
    def TCH(self) -> float:
        """ Lower temperature limit at which phase change region is to occur. (Real or blank)    """
        return self.__cardinfo.TCH

    @property
    def TDELTA(self) -> float:
        """ Total temperature change range within which a phase change is to occur. (Real > 0.0 or blank)    """
        return self.__cardinfo.TDELTA

    @property
    def QLAT(self) -> float:
        """ Latent heat of fusion per unit mass associated with the phase change. (Real > 0.0 or blank)    """
        return self.__cardinfo.QLAT



class MAT5(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat5)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def KXX(self) -> float:
        """ Thermal conductivity. (Real)    """
        return self.__cardinfo.KXX

    @property
    def KXY(self) -> float:
        """ KXY    """
        return self.__cardinfo.KXY

    @property
    def KXZ(self) -> float:
        """ KXZ    """
        return self.__cardinfo.KXZ

    @property
    def KYY(self) -> float:
        """ KYY    """
        return self.__cardinfo.KYY

    @property
    def KYZ(self) -> float:
        """ KYZ    """
        return self.__cardinfo.KYZ

    @property
    def KZZ(self) -> float:
        """ KZZ    """
        return self.__cardinfo.KZZ

    @property
    def CP(self) -> float:
        """ Heat capacity per unit mass. (Real > 0.0 or blank)    """
        return self.__cardinfo.CP

    @property
    def RHO(self) -> float:
        """ Density. (Real>0.0; Default=1.0)    """
        return self.__cardinfo.RHO

    @property
    def HGEN(self) -> float:
        """ Heat generation capability used with QVOL entries. (Real > 0.0; Default = 1.0)    """
        return self.__cardinfo.HGEN



class MAT8(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat8)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. Referenced on a PSHELL or PCOMP entry only. (0 < Integer< 100,000,000)    """
        return self.__cardinfo.MID

    @property
    def E1(self) -> float:
        """ Modulus of elasticity in longitudinal direction, also defined as the fiber direction or 1-direction. (Real ≠ 0.0)    """
        return self.__cardinfo.E1

    @property
    def E2(self) -> float:
        """ Modulus of elasticity in lateral direction, also defined as the matrix direction or 2-direction. (Real ≠ 0.0)    """
        return self.__cardinfo.E2

    @property
    def NU12(self) -> float:
        """ by the relation υ12E2 = υ21E1. (Real)    """
        return self.__cardinfo.NU12

    @property
    def G12(self) -> float:
        """ In-plane shear modulus. (Real > 0.0; Default = 0.0)    """
        return self.__cardinfo.G12

    @property
    def G1Z(self) -> float:
        """ Transverse shear modulus for shear in 1-Z plane. (Real > 0.0; Default implies infinite shear modulus.)    """
        return self.__cardinfo.G1Z

    @property
    def G2Z(self) -> float:
        """ Transverse shear modulus for shear in 2-Z plane. (Real > 0.0; Default implies infinite shear modulus.)    """
        return self.__cardinfo.G2Z

    @property
    def RHO(self) -> float:
        """ Mass density. (Real)    """
        return self.__cardinfo.RHO

    @property
    def A1(self) -> float:
        """ Thermal expansion coefficient in i-direction. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def TREF(self) -> float:
        """ TREF and GE are ignored if this entry is referenced by a PCOMP entry.    """
        return self.__cardinfo.TREF

    @property
    def Xt(self) -> float:
        """ the FT field on the PCOMP entry. (Real > 0.0; Default value for Xc is Xt.)    """
        return self.__cardinfo.Xt

    @property
    def Xc(self) -> float:
        """ Xc    """
        return self.__cardinfo.Xc

    @property
    def Yt(self) -> float:
        """ Default value for Yc is Yt.)    """
        return self.__cardinfo.Yt

    @property
    def Yc(self) -> float:
        """ Yc    """
        return self.__cardinfo.Yc

    @property
    def S(self) -> float:
        """ Allowable stress or strain for in-plane shear. See the FT field on the PCOMP entry. (Real > 0.0)    """
        return self.__cardinfo.S

    @property
    def GE(self) -> float:
        """ be used for this purpose, but TREF must then be blank.    """
        return self.__cardinfo.GE

    @property
    def F12(self) -> float:
        """ different from 0.0. See the FT field on the PCOMP entry. (Real)    """
        return self.__cardinfo.F12

    @property
    def STRN(self) -> float:
        """ [Real = 1.0 for strain allowables; blank(Default) for stress allowables.]    """
        return self.__cardinfo.STRN



class MAT9NAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat9Nas)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def G11(self) -> float:
        """ Elements of the 6 x 6 symmetric material property matrix in the material coordinate system. (Real)    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> float:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> float:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> float:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> float:
        """ G15    """
        return self.__cardinfo.G15

    @property
    def G16(self) -> float:
        """ G16    """
        return self.__cardinfo.G16

    @property
    def G22(self) -> float:
        """ G22    """
        return self.__cardinfo.G22

    @property
    def G23(self) -> float:
        """ G23    """
        return self.__cardinfo.G23

    @property
    def G24(self) -> float:
        """ G24    """
        return self.__cardinfo.G24

    @property
    def G25(self) -> float:
        """ G25    """
        return self.__cardinfo.G25

    @property
    def G26(self) -> float:
        """ G26    """
        return self.__cardinfo.G26

    @property
    def G33(self) -> float:
        """ G33    """
        return self.__cardinfo.G33

    @property
    def G34(self) -> float:
        """ G34    """
        return self.__cardinfo.G34

    @property
    def G35(self) -> float:
        """ G35    """
        return self.__cardinfo.G35

    @property
    def G36(self) -> float:
        """ G36    """
        return self.__cardinfo.G36

    @property
    def G44(self) -> float:
        """ G44    """
        return self.__cardinfo.G44

    @property
    def G45(self) -> float:
        """ G45    """
        return self.__cardinfo.G45

    @property
    def G46(self) -> float:
        """ G46    """
        return self.__cardinfo.G46

    @property
    def G55(self) -> float:
        """ G55    """
        return self.__cardinfo.G55

    @property
    def G56(self) -> float:
        """ G56    """
        return self.__cardinfo.G56

    @property
    def G66(self) -> float:
        """ G66    """
        return self.__cardinfo.G66

    @property
    def RHO(self) -> float:
        """ Mass density. (Real)    """
        return self.__cardinfo.RHO

    @property
    def A1(self) -> float:
        """ Thermal expansion coefficient. (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def A4(self) -> float:
        """ A4    """
        return self.__cardinfo.A4

    @property
    def A5(self) -> float:
        """ A5    """
        return self.__cardinfo.A5

    @property
    def A6(self) -> float:
        """ A6    """
        return self.__cardinfo.A6

    @property
    def TREF(self) -> float:
        """ TEMPERATURE(INITIAL) may be used for this purpose, but TREF must then be blank.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ If PARAM,W4 is not specified, GE is ignored in transient analysis. See “Parameters” on page 631.    """
        return self.__cardinfo.GE



class MAT9OPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardMat9Opt)    """
        return self.__cardinfo.CharName

    @property
    def MID(self) -> int:
        """ Unique material identification. No default (Integer > 0 or <String>)    """
        return self.__cardinfo.MID

    @property
    def G11(self) -> float:
        """ The material property matrix. No default (Real)    """
        return self.__cardinfo.G11

    @property
    def G12(self) -> float:
        """ G12    """
        return self.__cardinfo.G12

    @property
    def G13(self) -> float:
        """ G13    """
        return self.__cardinfo.G13

    @property
    def G14(self) -> float:
        """ G14    """
        return self.__cardinfo.G14

    @property
    def G15(self) -> float:
        """ G15    """
        return self.__cardinfo.G15

    @property
    def G16(self) -> float:
        """ G16    """
        return self.__cardinfo.G16

    @property
    def G22(self) -> float:
        """ G22    """
        return self.__cardinfo.G22

    @property
    def G23(self) -> float:
        """ G23    """
        return self.__cardinfo.G23

    @property
    def G24(self) -> float:
        """ G24    """
        return self.__cardinfo.G24

    @property
    def G25(self) -> float:
        """ G25    """
        return self.__cardinfo.G25

    @property
    def G26(self) -> float:
        """ G26    """
        return self.__cardinfo.G26

    @property
    def G33(self) -> float:
        """ G33    """
        return self.__cardinfo.G33

    @property
    def G34(self) -> float:
        """ G34    """
        return self.__cardinfo.G34

    @property
    def G35(self) -> float:
        """ G35    """
        return self.__cardinfo.G35

    @property
    def G36(self) -> float:
        """ G36    """
        return self.__cardinfo.G36

    @property
    def G44(self) -> float:
        """ G44    """
        return self.__cardinfo.G44

    @property
    def G45(self) -> float:
        """ G45    """
        return self.__cardinfo.G45

    @property
    def G46(self) -> float:
        """ G46    """
        return self.__cardinfo.G46

    @property
    def G55(self) -> float:
        """ G55    """
        return self.__cardinfo.G55

    @property
    def G56(self) -> float:
        """ G56    """
        return self.__cardinfo.G56

    @property
    def G66(self) -> float:
        """ G66    """
        return self.__cardinfo.G66

    @property
    def RHO(self) -> float:
        """ Mass density. Used to automatically compute mass for all structural elements. No default (Real)    """
        return self.__cardinfo.RHO

    @property
    def A1(self) -> float:
        """ Thermal expansion coefficient vector. No default (Real)    """
        return self.__cardinfo.A1

    @property
    def A2(self) -> float:
        """ A2    """
        return self.__cardinfo.A2

    @property
    def A3(self) -> float:
        """ A3    """
        return self.__cardinfo.A3

    @property
    def A4(self) -> float:
        """ A4    """
        return self.__cardinfo.A4

    @property
    def A5(self) -> float:
        """ A5    """
        return self.__cardinfo.A5

    @property
    def A6(self) -> float:
        """ A6    """
        return self.__cardinfo.A6

    @property
    def TREF(self) -> float:
        """ Reference temperature for the calculation of thermal loads. Default = blank(Real or blank)    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ Structural element damping coefficient. No default (Real)    """
        return self.__cardinfo.GE

    @property
    def MODULI(self) -> str:
        """ Continuation line flag for moduli temporal property.    """
        return self.__cardinfo.MODULI

    @property
    def MTIME(self) -> str:
        """ This material property is considered as the Long-term relaxed material input for viscoelasticity on the MATVE entry.    """
        return self.__cardinfo.MTIME



class PBAR(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Identification number of a MATHP entry. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def A(self) -> float:
        """ Area of bar cross section. (Real; Default = 0.0)    """
        return self.__cardinfo.A

    @property
    def I1(self) -> float:
        """Area moments of inertia.See Figure 8-177. (Real; I1 > 0.0, I2 > 0.0, I1* I2 > ; Default = 0.0)    """
        return self.__cardinfo.I1

    @property
    def I2(self) -> float:
        """ I2    """
        return self.__cardinfo.I2

    @property
    def J(self) -> float:
        """ Torsional constant. See Figure 8-177. (Real; Default = for SOL 600 and 0.0 for all other solution sequences)    """
        return self.__cardinfo.J

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit length. (Real)    """
        return self.__cardinfo.NSM

    @property
    def C1(self) -> float:
        """ Stress recovery coefficients. (Real; Default = 0.0)    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> float:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def D1(self) -> float:
        """ D1    """
        return self.__cardinfo.D1

    @property
    def D2(self) -> float:
        """ D2    """
        return self.__cardinfo.D2

    @property
    def E1(self) -> float:
        """ E1    """
        return self.__cardinfo.E1

    @property
    def E2(self) -> float:
        """ E2    """
        return self.__cardinfo.E2

    @property
    def F1(self) -> float:
        """ F1    """
        return self.__cardinfo.F1

    @property
    def F2(self) -> float:
        """ F2    """
        return self.__cardinfo.F2

    @property
    def K1(self) -> float:
        """ Area factor for shear. See Remark 5. (Real or blank)    """
        return self.__cardinfo.K1

    @property
    def K2(self) -> float:
        """ K2    """
        return self.__cardinfo.K2

    @property
    def I12(self) -> float:
        """Area moments of inertia.See Figure 8-177. (Real; I1 > 0.0, I2 > 0.0, I1* I2 > ; Default = 0.0)    """
        return self.__cardinfo.I12



class PBARL(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PMASS)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Material identification number (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def GROUP(self) -> str:
        """Default = “MSCBML0")    """
        return self.__cardinfo.GROUP

    @property
    def TYPE(self) -> str:
        """ “HAT1”, “DBOX” for GROUP=“MSCBML0")    """
        return self.__cardinfo.TYPE

    @property
    def DIM(self) -> float:
        """ DIM    """
        return self.__cardinfo.DIM

    @property
    def NSM(self) -> float:
        """ NSM    """
        return self.__cardinfo.NSM



class PBEAM(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PSOLID_NASTRAN)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> str:
        """ Property identification number. (Integer > 0 or string)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Material identification number. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def A_A(self) -> float:
        """ Area of the beam cross section at end A. (Real > 0.0)    """
        return self.__cardinfo.A_A

    @property
    def I1_A(self) -> float:
        """ Area moment of inertia at end A for bending in plane 1 about the neutral axis.See Remark 10. (Real > 0.0)    """
        return self.__cardinfo.I1_A

    @property
    def I2_A(self) -> float:
        """ Area moment of inertia at end A for bending in plane 2 about the neutral axis.See Remark 10. (Real > 0.0)    """
        return self.__cardinfo.I2_A

    @property
    def I12_A(self) -> float:
        """Area product of inertia at end A. See Remark 10. (Real, but I1*I2 - I12^2 > 0.00)    """
        return self.__cardinfo.I12_A

    @property
    def J_A(self) -> float:
        """ Torsional stiffness parameter at end A. See Remark 10. (Real >= 0.0 but > 0.0 if warping is present)    """
        return self.__cardinfo.J_A

    @property
    def NSM_A(self) -> float:
        """ Nonstructural mass per unit length at end A. (Real)    """
        return self.__cardinfo.NSM_A

    @property
    def C1_A(self) -> float:
        """ recovery. (Real)    """
        return self.__cardinfo.C1_A

    @property
    def C2_A(self) -> float:
        """ C2_A    """
        return self.__cardinfo.C2_A

    @property
    def D1_A(self) -> float:
        """ D1_A    """
        return self.__cardinfo.D1_A

    @property
    def D2_A(self) -> float:
        """ D2_A    """
        return self.__cardinfo.D2_A

    @property
    def E1_A(self) -> float:
        """ E1_A    """
        return self.__cardinfo.E1_A

    @property
    def E2_A(self) -> float:
        """ E2_A    """
        return self.__cardinfo.E2_A

    @property
    def F1_A(self) -> float:
        """ F1_A    """
        return self.__cardinfo.F1_A

    @property
    def F2_A(self) -> float:
        """ F2_A    """
        return self.__cardinfo.F2_A

    @property
    def SO(self) -> str:
        """ “NO” No stresses or forces are recovered.    """
        return self.__cardinfo.SO

    @property
    def X_XB(self) -> float:
        """Figure 8-184 in Remark 10. (Real, 0.0 < x/xb ≤ 1.0)    """
        return self.__cardinfo.X_XB

    @property
    def A(self) -> float:
        """present.)    """
        return self.__cardinfo.A

    @property
    def I1(self) -> float:
        """ I1    """
        return self.__cardinfo.I1

    @property
    def I2(self) -> float:
        """ I2    """
        return self.__cardinfo.I2

    @property
    def I12(self) -> float:
        """ I12    """
        return self.__cardinfo.I12

    @property
    def J(self) -> float:
        """ J    """
        return self.__cardinfo.J

    @property
    def NSM(self) -> float:
        """ NSM    """
        return self.__cardinfo.NSM

    @property
    def C1(self) -> float:
        """ recovery. (Real)    """
        return self.__cardinfo.C1

    @property
    def C2(self) -> float:
        """ C2    """
        return self.__cardinfo.C2

    @property
    def D1(self) -> float:
        """ D1    """
        return self.__cardinfo.D1

    @property
    def D2(self) -> float:
        """ D2    """
        return self.__cardinfo.D2

    @property
    def E1(self) -> float:
        """ E1    """
        return self.__cardinfo.E1

    @property
    def E2(self) -> float:
        """ E2    """
        return self.__cardinfo.E2

    @property
    def F1(self) -> float:
        """ F1    """
        return self.__cardinfo.F1

    @property
    def F2(self) -> float:
        """ F2    """
        return self.__cardinfo.F2

    @property
    def K1(self) -> float:
        """ plane 2. See Remark 12. (Real)    """
        return self.__cardinfo.K1

    @property
    def K2(self) -> float:
        """ K2    """
        return self.__cardinfo.K2

    @property
    def S1(self) -> float:
        """ plane 2. Ignored for beam p-elements. (Real)    """
        return self.__cardinfo.S1

    @property
    def S2(self) -> float:
        """ S2    """
        return self.__cardinfo.S2

    @property
    def NSI_A(self) -> float:
        """ end A and end B.See Figure 8-184. (Real)    """
        return self.__cardinfo.NSI_A

    @property
    def NSI_B(self) -> float:
        """ NSI_B    """
        return self.__cardinfo.NSI_B

    @property
    def CW_A(self) -> float:
        """ for beam p-elements.See Remark 11. (Real)    """
        return self.__cardinfo.CW_A

    @property
    def CW_B(self) -> float:
        """ CW_B    """
        return self.__cardinfo.CW_B

    @property
    def M1_A(self) -> float:
        """ Figure 8-184. (Real)    """
        return self.__cardinfo.M1_A

    @property
    def M2_A(self) -> float:
        """ M2_A    """
        return self.__cardinfo.M2_A

    @property
    def M1_B(self) -> float:
        """ M1_B    """
        return self.__cardinfo.M1_B

    @property
    def M2_B(self) -> float:
        """ M2_B    """
        return self.__cardinfo.M2_B

    @property
    def N1_A(self) -> float:
        """ (y, z) coordinates of neutral axis for end A and end B (Real)    """
        return self.__cardinfo.N1_A

    @property
    def N2_A(self) -> float:
        """ N2_A    """
        return self.__cardinfo.N2_A

    @property
    def N1_B(self) -> float:
        """ N1_B    """
        return self.__cardinfo.N1_B

    @property
    def N2_B(self) -> float:
        """ N2_B    """
        return self.__cardinfo.N2_B



class PBEAML(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PMASS)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Material identification number (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def GROUP(self) -> str:
        """ Cross-section group. (Character; Default = “MSCBML0")    """
        return self.__cardinfo.GROUP

    @property
    def TYPE(self) -> str:
        """“DBOX” for GROUP = “MSCBML0")    """
        return self.__cardinfo.TYPE

    @property
    def DIM(self) -> float:
        """(Real > 0.0 for GROUP = “MSCBML0")    """
        return self.__cardinfo.DIM

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit length. (Default = 0.0)    """
        return self.__cardinfo.NSM

    @property
    def SO(self) -> str:
        """NO: No stresses or forces are recovered.    """
        return self.__cardinfo.SO

    @property
    def X_XB(self) -> float:
        """Default = 1.0)    """
        return self.__cardinfo.X_XB



class PBUSHNAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def K(self) -> str:
        """coordinate system. (Character)    """
        return self.__cardinfo.K

    @property
    def K1(self) -> float:
        """ (Real; Default = 0.0)    """
        return self.__cardinfo.K1

    @property
    def K2(self) -> float:
        """ K2    """
        return self.__cardinfo.K2

    @property
    def K3(self) -> float:
        """ K3    """
        return self.__cardinfo.K3

    @property
    def K4(self) -> float:
        """ K4    """
        return self.__cardinfo.K4

    @property
    def K5(self) -> float:
        """ K5    """
        return self.__cardinfo.K5

    @property
    def K6(self) -> float:
        """ K6    """
        return self.__cardinfo.K6

    @property
    def B(self) -> str:
        """(Character)    """
        return self.__cardinfo.B

    @property
    def B1(self) -> float:
        """ Bi: Nominal damping coefficients in direction 1 through 6 in units of force per unit velocity.See Remarks 2., 3., and 9. (Real; Default = 0.0)    """
        return self.__cardinfo.B1

    @property
    def B2(self) -> float:
        """ B2    """
        return self.__cardinfo.B2

    @property
    def B3(self) -> float:
        """ B3    """
        return self.__cardinfo.B3

    @property
    def B4(self) -> float:
        """ B4    """
        return self.__cardinfo.B4

    @property
    def B5(self) -> float:
        """ B5    """
        return self.__cardinfo.B5

    @property
    def B6(self) -> float:
        """ B6    """
        return self.__cardinfo.B6

    @property
    def GE(self) -> str:
        """constants.See Remark 7. (Character)    """
        return self.__cardinfo.GE

    @property
    def GE1(self) -> float:
        """ (Real; Default = 0.0)    """
        return self.__cardinfo.GE1

    @property
    def GE2(self) -> float:
        """ GE2    """
        return self.__cardinfo.GE2

    @property
    def GE3(self) -> float:
        """ GE3    """
        return self.__cardinfo.GE3

    @property
    def GE4(self) -> float:
        """ GE4    """
        return self.__cardinfo.GE4

    @property
    def GE5(self) -> float:
        """ GE5    """
        return self.__cardinfo.GE5

    @property
    def GE6(self) -> float:
        """ GE6    """
        return self.__cardinfo.GE6

    @property
    def RCV(self) -> str:
        """(Character)    """
        return self.__cardinfo.RCV

    @property
    def SA(self) -> float:
        """ (Real; Default = 0.0)    """
        return self.__cardinfo.SA

    @property
    def ST(self) -> float:
        """ ST    """
        return self.__cardinfo.ST

    @property
    def EA(self) -> float:
        """ EA    """
        return self.__cardinfo.EA

    @property
    def ET(self) -> float:
        """ ET    """
        return self.__cardinfo.ET

    @property
    def Mflag(self) -> str:
        """inertia properties(Iij )are desired CONM2 should be used.    """
        return self.__cardinfo.Mflag

    @property
    def M(self) -> float:
        """Lumped mass of the CBUSH. (Real≥0.0; Default=0.0)    """
        return self.__cardinfo.M



class PBUSHOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def K(self) -> str:
        """coordinate system. (Character)    """
        return self.__cardinfo.K

    @property
    def K1(self) -> float:
        """ (Real; Default = 0.0)    """
        return self.__cardinfo.K1

    @property
    def K2(self) -> float:
        """ K2    """
        return self.__cardinfo.K2

    @property
    def K3(self) -> float:
        """ K3    """
        return self.__cardinfo.K3

    @property
    def K4(self) -> float:
        """ K4    """
        return self.__cardinfo.K4

    @property
    def K5(self) -> float:
        """ K5    """
        return self.__cardinfo.K5

    @property
    def K6(self) -> float:
        """ K6    """
        return self.__cardinfo.K6

    @property
    def KMAG(self) -> str:
        """No default (Character)    """
        return self.__cardinfo.KMAG

    @property
    def KMAG1(self) -> float:
        """Default = 0.0 (Real)    """
        return self.__cardinfo.KMAG1

    @property
    def KMAG3(self) -> float:
        """ KMAG3    """
        return self.__cardinfo.KMAG3

    @property
    def KMAG4(self) -> float:
        """ KMAG4    """
        return self.__cardinfo.KMAG4

    @property
    def KMAG5(self) -> float:
        """ KMAG5    """
        return self.__cardinfo.KMAG5

    @property
    def KMAG6(self) -> float:
        """ KMAG6    """
        return self.__cardinfo.KMAG6

    @property
    def B(self) -> str:
        """(Character)    """
        return self.__cardinfo.B

    @property
    def B1(self) -> float:
        """ Bi: Nominal damping coefficients in direction 1 through 6 in units of force per unit velocity.See Remarks 2., 3., and 9. (Real; Default = 0.0)    """
        return self.__cardinfo.B1

    @property
    def B2(self) -> float:
        """ B2    """
        return self.__cardinfo.B2

    @property
    def B3(self) -> float:
        """ B3    """
        return self.__cardinfo.B3

    @property
    def B4(self) -> float:
        """ B4    """
        return self.__cardinfo.B4

    @property
    def B5(self) -> float:
        """ B5    """
        return self.__cardinfo.B5

    @property
    def B6(self) -> float:
        """ B6    """
        return self.__cardinfo.B6

    @property
    def GE(self) -> str:
        """constants.See Remark 7. (Character)    """
        return self.__cardinfo.GE

    @property
    def GE1(self) -> float:
        """ (Real; Default = 0.0)    """
        return self.__cardinfo.GE1

    @property
    def GE2(self) -> float:
        """ GE2    """
        return self.__cardinfo.GE2

    @property
    def GE3(self) -> float:
        """ GE3    """
        return self.__cardinfo.GE3

    @property
    def GE4(self) -> float:
        """ GE4    """
        return self.__cardinfo.GE4

    @property
    def GE5(self) -> float:
        """ GE5    """
        return self.__cardinfo.GE5

    @property
    def GE6(self) -> float:
        """ GE6    """
        return self.__cardinfo.GE6

    @property
    def ANGLE(self) -> str:
        """Flag indicating that the next 1 to 6 fields are Loss angles defined in degrees. 9    """
        return self.__cardinfo.ANGLE

    @property
    def ANGLE1(self) -> float:
        """ Nominal angle values in directions 1 through 6 in degrees.     """
        return self.__cardinfo.ANGLE1

    @property
    def ANGLE2(self) -> float:
        """ ANGLE2    """
        return self.__cardinfo.ANGLE2

    @property
    def ANGLE3(self) -> float:
        """ ANGLE3    """
        return self.__cardinfo.ANGLE3

    @property
    def ANGLE4(self) -> float:
        """ ANGLE4    """
        return self.__cardinfo.ANGLE4

    @property
    def ANGLE5(self) -> float:
        """ ANGLE5    """
        return self.__cardinfo.ANGLE5

    @property
    def ANGLE6(self) -> float:
        """ ANGLE6    """
        return self.__cardinfo.ANGLE6

    @property
    def M(self) -> str:
        """ Flag indicating that the next 1 to 6 fields are directional masses.    """
        return self.__cardinfo.M

    @property
    def M1(self) -> float:
        """ Default = blank(Real)    """
        return self.__cardinfo.M1

    @property
    def M2(self) -> float:
        """ M2    """
        return self.__cardinfo.M2

    @property
    def M3(self) -> float:
        """ M3    """
        return self.__cardinfo.M3

    @property
    def M4(self) -> float:
        """ M4    """
        return self.__cardinfo.M4

    @property
    def M5(self) -> float:
        """ M5    """
        return self.__cardinfo.M5

    @property
    def M6(self) -> float:
        """ M6    """
        return self.__cardinfo.M6



class PCOMPNAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPcompNas)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (0 < Integer < 10000000)    """
        return self.__cardinfo.PID

    @property
    def Z0(self) -> float:
        """ connection entry.    """
        return self.__cardinfo.Z0

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit area. (Real)    """
        return self.__cardinfo.NSM

    @property
    def SB(self) -> float:
        """ Allowable shear stress of the bonding material (allowable interlaminar shear stress). Required if FT is also specified. (Real > 0.0)    """
        return self.__cardinfo.SB

    @property
    def FT(self) -> str:
        """ c. Xt, Xc, Yt, Yc, and S on all referenced MAT8 Bulk Data entries if stress allowables are used, or Xt, Xc, Yt, S, and STRN = 1.0 if strain allowables are used.    """
        return self.__cardinfo.FT

    @property
    def TREF(self) -> float:
        """ INTEGRAL,TREF is not applicable.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ To obtain the damping coefficient GE, multiply the critical damping ratio C ⁄ C0 by 2.0.    """
        return self.__cardinfo.GE

    @property
    def LAM(self) -> str:
        """ results and prints results for the equivalent homogeneous element.    """
        return self.__cardinfo.LAM

    @property
    def MIDi(self) -> list[int]:
        """ results and prints results for the equivalent homogeneous element.    """
        return list(self.__cardinfo.MIDi)

    @property
    def Ti(self) -> list[float]:
        """ results and prints results for the equivalent homogeneous element.    """
        return list(self.__cardinfo.Ti)

    @property
    def THETAi(self) -> list[float]:
        """ results and prints results for the equivalent homogeneous element.    """
        return list(self.__cardinfo.THETAi)

    @property
    def SOUTi(self) -> list[str]:
        """ results and prints results for the equivalent homogeneous element.    """
        return list(self.__cardinfo.SOUTi)



class PCOMPOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPcompOpt)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (0 < Integer < 10000000)    """
        return self.__cardinfo.PID

    @property
    def Z0(self) -> float:
        """ connection entry.    """
        return self.__cardinfo.Z0

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit area. (Real)    """
        return self.__cardinfo.NSM

    @property
    def SB(self) -> float:
        """ Allowable shear stress of the bonding material (allowable interlaminar shear stress). Required if FT is also specified. (Real > 0.0)    """
        return self.__cardinfo.SB

    @property
    def FT(self) -> str:
        """ c. Xt, Xc, Yt, Yc, and S on all referenced MAT8 Bulk Data entries if stress allowables are used, or Xt, Xc, Yt, S, and STRN = 1.0 if strain allowables are used.    """
        return self.__cardinfo.FT

    @property
    def TREF(self) -> float:
        """ INTEGRAL,TREF is not applicable.    """
        return self.__cardinfo.TREF

    @property
    def GE(self) -> float:
        """ To obtain the damping coefficient GE, multiply the critical damping ratio C ⁄ C0 by 2.0.    """
        return self.__cardinfo.GE

    @property
    def LAM(self) -> str:
        """ results and prints results for the equivalent homogeneous element.    """
        return self.__cardinfo.LAM

    @property
    def MIDi(self) -> list[int]:
        """ Temperature-dependent ply properties only available in SOL 106. See PARAM,COMPMATT for details.    """
        return list(self.__cardinfo.MIDi)

    @property
    def Ti(self) -> list[float]:
        """ The default for MID2, ..., MIDn is the last defined MIDi. In the example above, MID1 is the default for MID2, MID3, and MID4.The same logic applies to Ti.    """
        return list(self.__cardinfo.Ti)

    @property
    def THETAi(self) -> list[float]:
        """ The default for MID2, ..., MIDn is the last defined MIDi. In the example above, MID1 is the default for MID2, MID3, and MID4.The same logic applies to Ti.    """
        return list(self.__cardinfo.THETAi)

    @property
    def SOUTi(self) -> list[str]:
        """ connection entry.    """
        return list(self.__cardinfo.SOUTi)

    @property
    def DS(self) -> float:
        """ (Real = 1.0 or blank)    """
        return self.__cardinfo.DS

    @property
    def NRPT(self) -> int:
        """ Number of repeat laminates 20. Default = blank(Integer > 0 or blank)    """
        return self.__cardinfo.NRPT

    @property
    def EXPLICIT(self) -> str:
        """ Flag indicating that parameters for Explicit Analysis are to follow.    """
        return self.__cardinfo.EXPLICIT

    @property
    def ISOPE(self) -> str:
        """ blank    """
        return self.__cardinfo.ISOPE

    @property
    def HGID(self) -> int:
        """ Identification number of the hourglass control (HOURGLS) entry. Default = Blank(Integer > 0)    """
        return self.__cardinfo.HGID

    @property
    def NIP(self) -> int:
        """ Number of Gauss points through thickness. Default = 3 (1 ≤ Integer ≤ 10)    """
        return self.__cardinfo.NIP



class PELAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID1(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID1

    @property
    def K1(self) -> float:
        """ Elastic property value. (Real)    """
        return self.__cardinfo.K1

    @property
    def GE1(self) -> float:
        """ Damping coefficient, . See Remarks 5. and 6. (Real)    """
        return self.__cardinfo.GE1

    @property
    def S1(self) -> float:
        """ Stress coefficient. (Real)    """
        return self.__cardinfo.S1

    @property
    def PID2(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID2

    @property
    def K2(self) -> float:
        """ Elastic property value. (Real)    """
        return self.__cardinfo.K2

    @property
    def GE2(self) -> float:
        """ Damping coefficient, . See Remarks 5. and 6. (Real)    """
        return self.__cardinfo.GE2

    @property
    def S2(self) -> float:
        """ Stress coefficient. (Real)    """
        return self.__cardinfo.S2



class PFAST(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PFAST)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def D(self) -> float:
        """ D    """
        return self.__cardinfo.D

    @property
    def MCID(self) -> int:
        """ MCID    """
        return self.__cardinfo.MCID

    @property
    def MFLAG(self) -> int:
        """ MCID    """
        return self.__cardinfo.MFLAG

    @property
    def KT1(self) -> float:
        """ KT1    """
        return self.__cardinfo.KT1

    @property
    def KT2(self) -> float:
        """ KT2    """
        return self.__cardinfo.KT2

    @property
    def KT3(self) -> float:
        """ KT3    """
        return self.__cardinfo.KT3

    @property
    def KR1(self) -> float:
        """ KR1    """
        return self.__cardinfo.KR1

    @property
    def KR2(self) -> float:
        """ KR2    """
        return self.__cardinfo.KR2

    @property
    def KR3(self) -> float:
        """ KR3    """
        return self.__cardinfo.KR3

    @property
    def MASS(self) -> float:
        """ MASS    """
        return self.__cardinfo.MASS

    @property
    def GE(self) -> float:
        """ MASS    """
        return self.__cardinfo.GE



class PLOTEL(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPlotel)    """
        return self.__cardinfo.CharName

    @property
    def EID(self) -> int:
        """ Element identification number. (Integer > 0)    """
        return self.__cardinfo.EID

    @property
    def G1(self) -> int:
        """ CardGrid point identification numbers of connection points. (Integer > 0 ; G1 ≠ G2)    """
        return self.__cardinfo.G1

    @property
    def G2(self) -> int:
        """ G2    """
        return self.__cardinfo.G2



class PLPLANE(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPlplane)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Identification number of a MATHP entry. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def CID(self) -> int:
        """ output in the basic coordinate system.    """
        return self.__cardinfo.CID

    @property
    def STR(self) -> str:
        """ Location of stress and strain output. (Character: “GAUS” or “GRID”, Default = “GRID”)    """
        return self.__cardinfo.STR



class PMASS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPmass)    """
        return self.__cardinfo.CharName

    @property
    def PID1(self) -> int:
        """ PIDi Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID1

    @property
    def M1(self) -> float:
        """ Mi Value of scalar mass. (Real)    """
        return self.__cardinfo.M1

    @property
    def PID2(self) -> int:
        """ PID2    """
        return self.__cardinfo.PID2

    @property
    def M2(self) -> float:
        """ M2    """
        return self.__cardinfo.M2

    @property
    def PID3(self) -> int:
        """ PID3    """
        return self.__cardinfo.PID3

    @property
    def M3(self) -> float:
        """ M3    """
        return self.__cardinfo.M3

    @property
    def PID4(self) -> int:
        """ PID4    """
        return self.__cardinfo.PID4

    @property
    def M4(self) -> float:
        """ M4    """
        return self.__cardinfo.M4



class PROD(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Material identification number    """
        return self.__cardinfo.MID

    @property
    def A(self) -> float:
        """ Area of bar cross section. (Real; Default = 0.0)    """
        return self.__cardinfo.A

    @property
    def J(self) -> float:
        """ Torsional constant. See Figure 8-177. (Real; Default = for SOL 600 and 0.0 for all other solution sequences)    """
        return self.__cardinfo.J

    @property
    def C(self) -> float:
        """ Coefficient to determine torsional stress. (Real; Default = 0.0)    """
        return self.__cardinfo.C

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit length. (Real)    """
        return self.__cardinfo.NSM



class PSHEAR(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Material identification number    """
        return self.__cardinfo.MID

    @property
    def T(self) -> float:
        """ Thickness of shear panel. (Real 0.0)    """
        return self.__cardinfo.T

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit length. (Real)    """
        return self.__cardinfo.NSM

    @property
    def F1(self) -> float:
        """ F1    """
        return self.__cardinfo.F1

    @property
    def F2(self) -> float:
        """ F2    """
        return self.__cardinfo.F2



class PSHELLNAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPshellNas)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID1(self) -> int:
        """ Material identification number for the membrane. (Integer >= 0 or blank)    """
        return self.__cardinfo.MID1

    @property
    def T(self) -> float:
        """ CQUAD8, and CTRIA6 entries. (Real or blank)    """
        return self.__cardinfo.T

    @property
    def MID2(self) -> int:
        """ Material identification number for bending. (Integer >= -1 or blank)    """
        return self.__cardinfo.MID2

    @property
    def INERTIA(self) -> float:
        """ homogeneous shell, T3 ⁄ 12. The default value is for a homogeneous shell. (Real > 0.0; Default = 1.0)    """
        return self.__cardinfo.INERTIA

    @property
    def MID3(self) -> int:
        """ Material identification number for transverse shear. (Integer > 0 or blank; unless MID2 > 0, must be blank.)    """
        return self.__cardinfo.MID3

    @property
    def TST(self) -> float:
        """ homogeneous shell. (Real > 0.0; Default = .833333)    """
        return self.__cardinfo.TST

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit area. (Real)    """
        return self.__cardinfo.NSM

    @property
    def Z1(self) -> float:
        """ grid points, if they are input on connection entries.    """
        return self.__cardinfo.Z1

    @property
    def Z2(self) -> float:
        """ Z2    """
        return self.__cardinfo.Z2

    @property
    def MID4(self) -> int:
        """ For the CQUADR and CTRIAR elements, the MID4 field should be left blankbecause their formulation does not include membrane-bending coupling.    """
        return self.__cardinfo.MID4



class PSHELLOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPshellOpt)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID1(self) -> int:
        """ Material identification number for the membrane. (Integer >= 0 or blank)    """
        return self.__cardinfo.MID1

    @property
    def T(self) -> float:
        """ CQUAD8, and CTRIA6 entries. (Real or blank)    """
        return self.__cardinfo.T

    @property
    def MID2(self) -> int:
        """ Material identification number for bending. (Integer >= -1 or blank)    """
        return self.__cardinfo.MID2

    @property
    def INERTIA(self) -> float:
        """ homogeneous shell, T3 ⁄ 12. The default value is for a homogeneous shell. (Real > 0.0; Default = 1.0)    """
        return self.__cardinfo.INERTIA

    @property
    def MID3(self) -> int:
        """ Material identification number for transverse shear. (Integer > 0 or blank; unless MID2 > 0, must be blank.)    """
        return self.__cardinfo.MID3

    @property
    def TST(self) -> float:
        """ homogeneous shell. (Real > 0.0; Default = .833333)    """
        return self.__cardinfo.TST

    @property
    def NSM(self) -> float:
        """ Nonstructural mass per unit area. (Real)    """
        return self.__cardinfo.NSM

    @property
    def Z1(self) -> float:
        """ grid points, if they are input on connection entries.    """
        return self.__cardinfo.Z1

    @property
    def Z2(self) -> float:
        """ Z2    """
        return self.__cardinfo.Z2

    @property
    def MID4(self) -> int:
        """ For the CQUADR and CTRIAR elements, the MID4 field should be left blankbecause their formulation does not include membrane-bending coupling.    """
        return self.__cardinfo.MID4

    @property
    def T0(self) -> float:
        """ Real = 0.0 or blank for MAT2, MAT8)    """
        return self.__cardinfo.T0

    @property
    def ZOFFS(self) -> float:
        """ Offset from the plane defined by element grid points to the shell reference plane. Real or Character Input(Top/Bottom)    """
        return self.__cardinfo.ZOFFS

    @property
    def EXPLICIT(self) -> str:
        """ Flag indicating that parameters for Explicit Analysis are to follow.    """
        return self.__cardinfo.EXPLICIT

    @property
    def ISOPE(self) -> int:
        """ Default = BWC for four-noded CQUAD4 elements in explicit analysis.    """
        return self.__cardinfo.ISOPE

    @property
    def HGID(self) -> int:
        """ Identification number of an hourglass control (HOURGLS) entry. Default = Blank(Integer > 0 or blank)    """
        return self.__cardinfo.HGID

    @property
    def NIP(self) -> int:
        """ Number of through thickness Gauss points. Default = 3 (1 ≤ Integer ≤ 10)    """
        return self.__cardinfo.NIP



class PSOLIDNAS(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (CardPsolidNas)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Identification number of a MAT1, MAT4, MAT5, MAT9, or MAT10 entry. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def CORDM(self) -> int:
        """ Identification number of a MAT1, MAT4, MAT5, MAT9, or MAT10 entry. (Integer > 0)    """
        return self.__cardinfo.CORDM

    @property
    def FCTN(self) -> str:
        """ Fluid element flag. (Character: “PFLUID” indicates a fluid element, “SMECH” indicates a structural element; Default = “SMECH.”)    """
        return self.__cardinfo.FCTN



class PSOLIDOPT(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PSOLID_NASTRAN)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> str:
        """ Property identification number. (Integer > 0 or string)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Identification number of a MAT1, MAT4, MAT5, MAT9, or MAT10 entry. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def CORDM(self) -> int:
        """ Identification number of a MAT1, MAT4, MAT5, MAT9, or MAT10 entry. (Integer > 0)    """
        return self.__cardinfo.CORDM


    @property
    def FCTN(self) -> str:
        """ Fluid element flag. (Character: “PFLUID” indicates a fluid element, “SMECH” indicates a structural element; Default = “SMECH.”)    """
        return self.__cardinfo.FCTN

    @property
    def EXPLICIT(self) -> str:
        """	Flag indicating that parameters for Explicit Analysis are to follow.    """
        return self.__cardinfo.EXPLICIT

    @property
    def ISOPE(self) -> str:
        """         AVE for four-noded CTETRA elements in explicit analysis.    """
        return self.__cardinfo.ISOPE

    @property
    def HGID(self) -> int:
        """ Identification number of the hourglass control (HOURGLS) Bulk Data Entry. No default    """
        return self.__cardinfo.HGID

    @property
    def HGHOR(self) -> str:
        """ Specifies the element formulation for ten-noded CTETRA elements in explicit analysis.    """
        return self.__cardinfo.HGHOR



class PWELD(N2PCard):

    def __init__(self, cardinfo):
        super().__init__(cardinfo)
        self.__cardinfo = cardinfo

    @property
    def CharName(self) -> str:
        """ Card code (PLPLANE)    """
        return self.__cardinfo.CharName

    @property
    def PID(self) -> int:
        """ Property identification number. (Integer > 0)    """
        return self.__cardinfo.PID

    @property
    def MID(self) -> int:
        """ Identification number of a MATHP entry. (Integer > 0)    """
        return self.__cardinfo.MID

    @property
    def D(self) -> float:
        """ Diameter of the connector    """
        return self.__cardinfo.D

    @property
    def MSET(self) -> str:
        """ are generated.    """
        return self.__cardinfo.MSET

    @property
    def TYPE(self) -> str:
        """ = “SPOT” spot weld connector    """
        return self.__cardinfo.TYPE

    @property
    def LDMIN(self) -> float:
        """ calculation, see Remark 4.    """
        return self.__cardinfo.LDMIN

    @property
    def LDMAX(self) -> float:
        """ calculation, see Remark 4.    """
        return self.__cardinfo.LDMAX


