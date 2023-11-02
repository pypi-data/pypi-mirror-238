import sys
import os
import subprocess
import typing
import warnings
import shutil
import glob
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QErrorMessage,
    QDialog,
    QWidget,
    QMessageBox,
    QProgressBar,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from Bio import PDB, BiopythonWarning
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from mainwindow import Ui_MainWindow
from advanced_options_parse_pdb import Ui_DialogParseParam
from nerdss_install import Ui_NERDSSInstall
from pdb_movie_player import Ui_Form
from mplwidget import MPLWidget
from plot_copy_num import Ui_PlotCopyNum
from plot_complex import Ui_PlotComplex
import numpy as np
import pandas as pd

warnings.simplefilter("ignore", BiopythonWarning)

molecules = []
reactions = []

colors = [
    (1.0, 0.0, 0.0, 0.1),
    (0.0, 1.0, 0.0, 0.1),
    (0.0, 0.0, 1.0, 0.1),
    (1.0, 1.0, 0.0, 0.1),
    (1.0, 0.0, 1.0, 0.1),
    (0.0, 1.0, 1.0, 0.1),
    (0.5, 0.5, 0.5, 0.1),
]

colors2 = [
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
]

energyTable = {
    "CYS-CYS": 5.44,
    "CYS-MET": 4.99,
    "CYS-PHE": 5.80,
    "CYS-ILE": 5.50,
    "CYS-LEU": 5.83,
    "CYS-VAL": 4.96,
    "CYS-TRP": 4.95,
    "CYS-TYR": 4.16,
    "CYS-ALA": 3.57,
    "CYS-GLY": 3.16,
    "CYS-THR": 3.11,
    "CYS-SER": 2.86,
    "CYS-ASN": 2.59,
    "CYS-GLN": 2.85,
    "CYS-ASP": 2.41,
    "CYS-GLU": 2.27,
    "CYS-HIS": 3.60,
    "CYS-ARG": 2.57,
    "CYS-LYS": 1.95,
    "CYS-PRO": 3.07,
    "MET-MET": 5.46,
    "MET-PHE": 6.56,
    "MET-ILE": 6.02,
    "MET-LEU": 6.41,
    "MET-VAL": 5.32,
    "MET-TRP": 5.55,
    "MET-TYR": 4.91,
    "MET-ALA": 3.94,
    "MET-GLY": 3.39,
    "MET-THR": 3.51,
    "MET-SER": 3.03,
    "MET-ASN": 2.95,
    "MET-GLN": 3.30,
    "MET-ASP": 2.57,
    "MET-GLU": 2.89,
    "MET-HIS": 3.98,
    "MET-ARG": 3.12,
    "MET-LYS": 2.48,
    "MET-PRO": 3.56,
    "PHE-PHE": 7.26,
    "PHE-ILE": 6.84,
    "PHE-LEU": 7.28,
    "PHE-VAL": 6.29,
    "PHE-TRP": 6.16,
    "PHE-TYR": 5.66,
    "PHE-ALA": 4.81,
    "PHE-GLY": 4.13,
    "PHE-THR": 4.28,
    "PHE-SER": 4.02,
    "PHE-ASN": 3.75,
    "PHE-GLN": 4.10,
    "PHE-ASP": 3.48,
    "PHE-GLU": 3.56,
    "PHE-HIS": 4.77,
    "PHE-ARG": 3.98,
    "PHE-LYS": 3.36,
    "PHE-PRO": 4.25,
    "ILE-ILE": 6.54,
    "ILE-LEU": 7.04,
    "ILE-VAL": 6.05,
    "ILE-TRP": 5.78,
    "ILE-TYR": 5.25,
    "ILE-ALA": 4.58,
    "ILE-GLY": 3.78,
    "ILE-THR": 4.03,
    "ILE-SER": 3.52,
    "ILE-ASN": 3.24,
    "ILE-GLN": 3.67,
    "ILE-ASP": 3.17,
    "ILE-GLU": 3.27,
    "ILE-HIS": 4.14,
    "ILE-ARG": 3.63,
    "ILE-LYS": 3.01,
    "ILE-PRO": 3.76,
    "LEU-LEU": 7.37,
    "LEU-VAL": 6.48,
    "LEU-TRP": 6.14,
    "LEU-TYR": 5.67,
    "LEU-ALA": 4.91,
    "LEU-GLY": 4.16,
    "LEU-THR": 4.34,
    "LEU-SER": 3.92,
    "LEU-ASN": 3.74,
    "LEU-GLN": 4.04,
    "LEU-ASP": 3.40,
    "LEU-GLU": 3.59,
    "LEU-HIS": 4.54,
    "LEU-ARG": 4.03,
    "LEU-LYS": 3.37,
    "LEU-PRO": 4.20,
    "VAL-VAL": 5.52,
    "VAL-TRP": 5.18,
    "VAL-TYR": 4.62,
    "VAL-ALA": 4.04,
    "VAL-GLY": 3.38,
    "VAL-THR": 3.46,
    "VAL-SER": 3.05,
    "VAL-ASN": 2.83,
    "VAL-GLN": 3.07,
    "VAL-ASP": 2.48,
    "VAL-GLU": 2.67,
    "VAL-HIS": 3.58,
    "VAL-ARG": 3.07,
    "VAL-LYS": 2.49,
    "VAL-PRO": 3.32,
    "TRP-TRP": 5.06,
    "TRP-TYR": 4.66,
    "TRP-ALA": 3.82,
    "TRP-GLY": 3.42,
    "TRP-THR": 3.22,
    "TRP-SER": 2.99,
    "TRP-ASN": 3.07,
    "TRP-GLN": 3.11,
    "TRP-ASP": 2.84,
    "TRP-GLU": 2.99,
    "TRP-HIS": 3.98,
    "TRP-ARG": 3.41,
    "TRP-LYS": 2.69,
    "TRP-PRO": 3.73,
    "TYR-TYR": 4.17,
    "TYR-ALA": 3.36,
    "TYR-GLY": 3.01,
    "TYR-THR": 3.01,
    "TYR-SER": 2.78,
    "TYR-ASN": 2.76,
    "TYR-GLN": 2.97,
    "TYR-ASP": 2.76,
    "TYR-GLU": 2.79,
    "TYR-HIS": 3.52,
    "TYR-ARG": 3.16,
    "TYR-LYS": 2.60,
    "TYR-PRO": 3.19,
    "ALA-ALA": 2.72,
    "ALA-GLY": 2.31,
    "ALA-THR": 2.32,
    "ALA-SER": 2.01,
    "ALA-ASN": 1.84,
    "ALA-GLN": 1.89,
    "ALA-ASP": 1.70,
    "ALA-GLU": 1.51,
    "ALA-HIS": 2.41,
    "ALA-ARG": 1.83,
    "ALA-LYS": 1.31,
    "ALA-PRO": 2.03,
    "GLY-GLY": 2.24,
    "GLY-THR": 2.08,
    "GLY-SER": 1.82,
    "GLY-ASN": 1.74,
    "GLY-GLN": 1.66,
    "GLY-ASP": 1.59,
    "GLY-GLU": 1.22,
    "GLY-HIS": 2.15,
    "GLY-ARG": 1.72,
    "GLY-LYS": 1.15,
    "GLY-PRO": 1.87,
    "THR-THR": 2.12,
    "THR-SER": 1.96,
    "THR-ASN": 1.88,
    "THR-GLN": 1.90,
    "THR-ASP": 1.80,
    "THR-GLU": 1.74,
    "THR-HIS": 2.42,
    "THR-ARG": 1.90,
    "THR-LYS": 1.31,
    "THR-PRO": 1.90,
    "SER-SER": 1.67,
    "SER-ASN": 1.58,
    "SER-GLN": 1.49,
    "SER-ASP": 1.63,
    "SER-GLU": 1.48,
    "SER-HIS": 2.11,
    "SER-ARG": 1.62,
    "SER-LYS": 1.05,
    "SER-PRO": 1.57,
    "ASN-ASN": 1.68,
    "ASN-GLN": 1.71,
    "ASN-ASP": 1.68,
    "ASN-GLU": 1.51,
    "ASN-HIS": 2.08,
    "ASN-ARG": 1.64,
    "ASN-LYS": 1.21,
    "ASN-PRO": 1.53,
    "GLN-GLN": 1.54,
    "GLN-ASP": 1.46,
    "GLN-GLU": 1.42,
    "GLN-HIS": 1.98,
    "GLN-ARG": 1.80,
    "GLN-LYS": 1.29,
    "GLN-PRO": 1.73,
    "ASP-ASP": 1.21,
    "ASP-GLU": 1.02,
    "ASP-HIS": 2.32,
    "ASP-ARG": 2.29,
    "ASP-LYS": 1.68,
    "ASP-PRO": 1.33,
    "GLU-GLU": 0.91,
    "GLU-HIS": 2.15,
    "GLU-ARG": 2.27,
    "GLU-LYS": 1.80,
    "GLU-PRO": 1.26,
    "HIS-HIS": 3.05,
    "HIS-ARG": 2.16,
    "HIS-LYS": 1.35,
    "HIS-PRO": 2.25,
    "ARG-ARG": 1.55,
    "ARG-LYS": 0.59,
    "ARG-PRO": 1.70,
    "LYS-LYS": 0.12,
    "LYS-PRO": 0.97,
    "PRO-PRO": 1.75,
    "MET-CYS": 4.99,
    "PHE-CYS": 5.80,
    "ILE-CYS": 5.50,
    "LEU-CYS": 5.83,
    "VAL-CYS": 4.96,
    "TRP-CYS": 4.95,
    "TYR-CYS": 4.16,
    "ALA-CYS": 3.57,
    "GLY-CYS": 3.16,
    "THR-CYS": 3.11,
    "SER-CYS": 2.86,
    "ASN-CYS": 2.59,
    "GLN-CYS": 2.85,
    "ASP-CYS": 2.41,
    "GLU-CYS": 2.27,
    "HIS-CYS": 3.60,
    "ARG-CYS": 2.57,
    "LYS-CYS": 1.95,
    "PRO-CYS": 3.07,
    "PHE-MET": 6.56,
    "ILE-MET": 6.02,
    "LEU-MET": 6.41,
    "VAL-MET": 5.32,
    "TRP-MET": 5.55,
    "TYR-MET": 4.91,
    "ALA-MET": 3.94,
    "GLY-MET": 3.39,
    "THR-MET": 3.51,
    "SER-MET": 3.03,
    "ASN-MET": 2.95,
    "GLN-MET": 3.30,
    "ASP-MET": 2.57,
    "GLU-MET": 2.89,
    "HIS-MET": 3.98,
    "ARG-MET": 3.12,
    "LYS-MET": 2.48,
    "PRO-MET": 3.56,
    "ILE-PHE": 6.84,
    "LEU-PHE": 7.28,
    "VAL-PHE": 6.29,
    "TRP-PHE": 6.16,
    "TYR-PHE": 5.66,
    "ALA-PHE": 4.81,
    "GLY-PHE": 4.13,
    "THR-PHE": 4.28,
    "SER-PHE": 4.02,
    "ASN-PHE": 3.75,
    "GLN-PHE": 4.10,
    "ASP-PHE": 3.48,
    "GLU-PHE": 3.56,
    "HIS-PHE": 4.77,
    "ARG-PHE": 3.98,
    "LYS-PHE": 3.36,
    "PRO-PHE": 4.25,
    "LEU-ILE": 7.04,
    "VAL-ILE": 6.05,
    "TRP-ILE": 5.78,
    "TYR-ILE": 5.25,
    "ALA-ILE": 4.58,
    "GLY-ILE": 3.78,
    "THR-ILE": 4.03,
    "SER-ILE": 3.52,
    "ASN-ILE": 3.24,
    "GLN-ILE": 3.67,
    "ASP-ILE": 3.17,
    "GLU-ILE": 3.27,
    "HIS-ILE": 4.14,
    "ARG-ILE": 3.63,
    "LYS-ILE": 3.01,
    "PRO-ILE": 3.76,
    "VAL-LEU": 6.48,
    "TRP-LEU": 6.14,
    "TYR-LEU": 5.67,
    "ALA-LEU": 4.91,
    "GLY-LEU": 4.16,
    "THR-LEU": 4.34,
    "SER-LEU": 3.92,
    "ASN-LEU": 3.74,
    "GLN-LEU": 4.04,
    "ASP-LEU": 3.40,
    "GLU-LEU": 3.59,
    "HIS-LEU": 4.54,
    "ARG-LEU": 4.03,
    "LYS-LEU": 3.37,
    "PRO-LEU": 4.20,
    "TRP-VAL": 5.18,
    "TYR-VAL": 4.62,
    "ALA-VAL": 4.04,
    "GLY-VAL": 3.38,
    "THR-VAL": 3.46,
    "SER-VAL": 3.05,
    "ASN-VAL": 2.83,
    "GLN-VAL": 3.07,
    "ASP-VAL": 2.48,
    "GLU-VAL": 2.67,
    "HIS-VAL": 3.58,
    "ARG-VAL": 3.07,
    "LYS-VAL": 2.49,
    "PRO-VAL": 3.32,
    "TYR-TRP": 4.66,
    "ALA-TRP": 3.82,
    "GLY-TRP": 3.42,
    "THR-TRP": 3.22,
    "SER-TRP": 2.99,
    "ASN-TRP": 3.07,
    "GLN-TRP": 3.11,
    "ASP-TRP": 2.84,
    "GLU-TRP": 2.99,
    "HIS-TRP": 3.98,
    "ARG-TRP": 3.41,
    "LYS-TRP": 2.69,
    "PRO-TRP": 3.73,
    "ALA-TYR": 3.36,
    "GLY-TYR": 3.01,
    "THR-TYR": 3.01,
    "SER-TYR": 2.78,
    "ASN-TYR": 2.76,
    "GLN-TYR": 2.97,
    "ASP-TYR": 2.76,
    "GLU-TYR": 2.79,
    "HIS-TYR": 3.52,
    "ARG-TYR": 3.16,
    "LYS-TYR": 2.60,
    "PRO-TYR": 3.19,
    "GLY-ALA": 2.31,
    "THR-ALA": 2.32,
    "SER-ALA": 2.01,
    "ASN-ALA": 1.84,
    "GLN-ALA": 1.89,
    "ASP-ALA": 1.70,
    "GLU-ALA": 1.51,
    "HIS-ALA": 2.41,
    "ARG-ALA": 1.83,
    "LYS-ALA": 1.31,
    "PRO-ALA": 2.03,
    "THR-GLY": 2.08,
    "SER-GLY": 1.82,
    "ASN-GLY": 1.74,
    "GLN-GLY": 1.66,
    "ASP-GLY": 1.59,
    "GLU-GLY": 1.22,
    "HIS-GLY": 2.15,
    "ARG-GLY": 1.72,
    "LYS-GLY": 1.15,
    "PRO-GLY": 1.87,
    "SER-THR": 1.96,
    "ASN-THR": 1.88,
    "GLN-THR": 1.90,
    "ASP-THR": 1.80,
    "GLU-THR": 1.74,
    "HIS-THR": 2.42,
    "ARG-THR": 1.90,
    "LYS-THR": 1.31,
    "PRO-THR": 1.90,
    "ASN-SER": 1.58,
    "GLN-SER": 1.49,
    "ASP-SER": 1.63,
    "GLU-SER": 1.48,
    "HIS-SER": 2.11,
    "ARG-SER": 1.62,
    "LYS-SER": 1.05,
    "PRO-SER": 1.57,
    "GLN-ASN": 1.71,
    "ASP-ASN": 1.68,
    "GLU-ASN": 1.51,
    "HIS-ASN": 2.08,
    "ARG-ASN": 1.64,
    "LYS-ASN": 1.21,
    "PRO-ASN": 1.53,
    "ASP-GLN": 1.46,
    "GLU-GLN": 1.42,
    "HIS-GLN": 1.98,
    "ARG-GLN": 1.80,
    "LYS-GLN": 1.29,
    "PRO-GLN": 1.73,
    "GLU-ASP": 1.02,
    "HIS-ASP": 2.32,
    "ARG-ASP": 2.29,
    "LYS-ASP": 1.68,
    "PRO-ASP": 1.33,
    "HIS-GLU": 2.15,
    "ARG-GLU": 2.27,
    "LYS-GLU": 1.80,
    "PRO-GLU": 1.26,
    "ARG-HIS": 2.16,
    "LYS-HIS": 1.35,
    "PRO-HIS": 2.25,
    "LYS-ARG": 0.59,
    "PRO-ARG": 1.70,
    "PRO-LYS": 0.97,
}

updatedEnergyTable = {key: -value + 2.27 for key, value in energyTable.items()}


class LongTaskThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(LongTaskThread, self).__init__(parent)
        self.filename = None
        self.cutoff = 3.5
        self.thresholdResidue = 3
        self.stretchFactor = 1.0
        self.geometric_center = None

    def set_filename(self, filename):
        self.filename = filename

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff

    def set_threshold_residue(self, threshold_residue):
        self.thresholdResidue = threshold_residue

    def set_stretch_factor(self, stretch_factor):
        self.stretchFactor = stretch_factor

    def set_geometric_center(self, geometric_center):
        self.geometric_center = geometric_center

    def run(self):
        self.cg()
        self.finished_signal.emit()

    def cg(self):
        chains = []
        residues = []
        atoms = []
        interfaces = []
        with open(self.filename, "r") as fileName:
            currentChain = ""
            atomIndex = -1
            residueGlobalIndex = -1
            residueLocalIndex = -1
            chainIndex = -1
            for line in fileName:
                # parse one line from the pdb file
                typeName = line[0:4].strip()

                if typeName == "ATOM":
                    index = int(line[6:11])
                    atomType = line[12:16].strip()
                    residueType = line[17:20].strip().upper()
                    chainName = line[21]

                    # check if it is a new chain
                    if chainName != currentChain:
                        chainIndex += 1
                        chain = Chain(chainName, chainIndex)
                        currentChain = chainName
                        chains.append(chain)

                    residueIndex = int(line[22:26])

                    # check if it is a new residue
                    if residueIndex != residueLocalIndex:
                        residueGlobalIndex += 1
                        residueLocalIndex = residueIndex
                        residue = Residue(residueGlobalIndex)
                        residue.chain = chainIndex
                        residues.append(residue)
                        chains[-1].residues.append(residueGlobalIndex)

                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coord = Coord(x, y, z)
                    atomIndex += 1
                    atom = Atom(
                        atomIndex,
                        atomType,
                        residueType,
                        chainName,
                        chainIndex,
                        residueGlobalIndex,
                        coord,
                    )
                    atoms.append(atom)
                    residues[-1].atoms.append(atomIndex)
                    if atomType == "CA":
                        residues[-1].CA = atomIndex
                    if atomType == "C1'":
                        residues[-1].isDNA = True
                        residues[-1].CA = atomIndex

        # calculate the center of mass of each chain
        for chain in chains:
            x = 0
            y = 0
            z = 0
            count = 0
            for residueIndex in chain.residues:
                residue = residues[residueIndex]
                for atomIndex in residue.atoms:
                    chain.atoms.append(atomIndex)
                    atom = atoms[atomIndex]
                    x += atom.coord.x
                    y += atom.coord.y
                    z += atom.coord.z
                    count += 1
            x /= count
            y /= count
            z /= count
            chain.COM = Coord(x, y, z)

        # calculate the interface
        interfaceIndex = -1
        for chain1 in chains:
            for chain2 in chains:
                if chain1.index < chain2.index:
                    ca1 = []
                    ca2 = []
                    energy = []
                    residuesPair = ()
                    residues1 = ()
                    residues2 = ()
                    # loop all the atoms pair between chain1 and chain2
                    for a1 in chain1.atoms:
                        for a2 in chain2.atoms:
                            atom1 = atoms[a1]
                            atom2 = atoms[a2]
                            dsquare = atom1.coord.distanceSquare(atom2.coord)
                            if dsquare <= self.cutoff * self.cutoff:
                                ca1.append(a1)
                                ca2.append(a2)
                                residuesPairName = (
                                    atom1.chainName
                                    + str(atom1.resideIndex)
                                    + atom1.residueType
                                    + atom2.chainName
                                    + str(atom2.resideIndex)
                                    + atom2.residueType
                                )
                                if residuesPairName not in residuesPair:
                                    residuesPair += (residuesPairName,)
                                    bond = atom1.residueType + "-" + atom2.residueType
                                    if bond in updatedEnergyTable:
                                        energy.append(updatedEnergyTable[bond])
                                residues1 += (atom1.resideIndex,)
                                residues2 += (atom2.resideIndex,)
                    if (
                        len(ca1) > 0
                        and len(residues1) >= self.thresholdResidue
                        and len(residues2) >= self.thresholdResidue
                    ):
                        x, y, z = 0, 0, 0
                        for a in ca1:
                            CAIndex = residues[atoms[a].resideIndex].CA
                            x += atoms[CAIndex].coord.x
                            y += atoms[CAIndex].coord.y
                            z += atoms[CAIndex].coord.z
                        x /= len(ca1)
                        y /= len(ca1)
                        z /= len(ca1)
                        interfaceIndex += 1
                        interface = Interface(interfaceIndex, chain2.index)
                        interface.name = chain1.name + chain2.name
                        interface.chain = chain1.index
                        interface.coord = Coord(x, y, z)
                        interface.energy = sum(energy)
                        interface.atomsNum = len(ca1)
                        interface.residuesNum = len(residuesPair)
                        interface.size = len(residues1)
                        interfaces.append(interface)
                        chain1.interfaces.append(interfaceIndex)

                        x, y, z = 0, 0, 0
                        for a in ca2:
                            CAIndex = residues[atoms[a].resideIndex].CA
                            x += atoms[CAIndex].coord.x
                            y += atoms[CAIndex].coord.y
                            z += atoms[CAIndex].coord.z
                        x /= len(ca2)
                        y /= len(ca2)
                        z /= len(ca2)
                        interfaceIndex += 1
                        interface = Interface(interfaceIndex, chain1.index)
                        interface.name = chain2.name + chain1.name
                        interface.chain = chain2.index
                        interface.coord = Coord(x, y, z)
                        interface.energy = sum(energy)
                        interface.atomsNum = len(ca2)
                        interface.residuesNum = len(residuesPair)
                        interface.size = len(residues2)
                        interfaces.append(interface)
                        chain2.interfaces.append(interfaceIndex)

        # Move the interfaces to center of mass of the chain based on the stretch factor
        for chain in chains:
            for interfaceIndex in chain.interfaces:
                interface = interfaces[interfaceIndex]
                interface.coord.x = (
                    interface.coord.x - chain.COM.x
                ) * self.stretchFactor + chain.COM.x
                interface.coord.y = (
                    interface.coord.y - chain.COM.y
                ) * self.stretchFactor + chain.COM.y
                interface.coord.z = (
                    interface.coord.z - chain.COM.z
                ) * self.stretchFactor + chain.COM.z

        # write the pdb file with the interfaces added
        # Open a PDB file for writing
        with open("coarse_grained_structure.pdb", "w") as pdb_file:
            atom_serial = 1  # Initialize atom serial number
            residue_serial = 1  # Initialize residue serial number
            conect_records = []  # List to store CONECT records

            for chain in chains:
                com_serial = atom_serial  # Store the atom serial number for the COM

                # Write COM to PDB file
                pdb_file.write(
                    f"ATOM  {atom_serial:5d} COM  COM {chain.name}{residue_serial:4d}    {chain.COM.x:8.3f}{chain.COM.y:8.3f}{chain.COM.z:8.3f}\n"
                )
                atom_serial += 1

                for interfaceIndex in chain.interfaces:
                    interface = interfaces[interfaceIndex]

                    # Write interface to PDB file
                    pdb_file.write(
                        f"ATOM  {atom_serial:5d} INT  {interface.name.ljust(3)} {chain.name}{residue_serial:4d}    {interface.coord.x:8.3f}{interface.coord.y:8.3f}{interface.coord.z:8.3f}\n"
                    )

                    # Add bond between COM and interface
                    conect_records.append(f"CONECT{com_serial:5d}{atom_serial:5d}\n")

                    atom_serial += 1
                residue_serial += 1

            # Write all the CONECT records to the PDB file
            for conect in conect_records:
                pdb_file.write(conect)
        print("coarse_grained_structure.pdb has been generated.")

        # Build the NERDSS molecule
        for chain in chains:
            molecules.append(Molecule(chain.name))
            molecules[-1].COM = chain.COM
            for interfaceIndex in chain.interfaces:
                interface = interfaces[interfaceIndex]
                molecules[-1].interfaces.append(Intf(interface.name, interface.coord))

        # Update the visual coord
        for molecule in molecules:
            for interface in molecule.interfaces:
                interface.positionsVisual = interface.positions
            molecule.COMVisual = molecule.COM

        # Shift the COM of molecule to [0,0,0]
        for molecule in molecules:
            for interface in molecule.interfaces:
                interface.positions -= [molecule.COM.x, molecule.COM.y, molecule.COM.z]
                interface.positions = [p / 10.0 for p in interface.positions]
            molecule.COM = Coord(0, 0, 0)

        # Calculate the radius of the molecule
        for molecule in molecules:
            for interface in molecule.interfaces:
                molecule.radius = max(
                    molecule.radius, np.linalg.norm(interface.positions)
                )

        # Calculate the translational diffusion coefficient and rotational diffusion coefficient
        for molecule in molecules:
            molecule.D = 226.95 / molecule.radius
            molecule.Dr = 170.22 / (molecule.radius**3)

        # Build the NERDSS reaction
        builtReactions = ()
        for chain in chains:
            mol1 = chain.name
            interfaceName1 = None
            mol2 = None
            interfaceName2 = None
            for i in chain.interfaces:
                interface = interfaces[i]
                interfaceName1 = interface.name
                partnerInterface = None
                for partnerChain in chains:
                    if partnerChain.index == interface.partner:
                        mol2 = partnerChain.name
                        for j in partnerChain.interfaces:
                            partnerInterface = interfaces[j]
                            if partnerInterface.partner == chain.index:
                                interfaceName2 = partnerInterface.name
                                break
                        break
                reactionName = None
                if mol1 < mol2:
                    reactionName = (
                        mol1
                        + "("
                        + interfaceName1
                        + ")"
                        + "-"
                        + mol2
                        + "("
                        + interfaceName2
                        + ")"
                    )
                elif mol1 > mol2:
                    reactionName = (
                        mol2
                        + "("
                        + interfaceName2
                        + ")"
                        + "-"
                        + mol1
                        + "("
                        + interfaceName1
                        + ")"
                    )
                else:
                    if interfaceName1 < interfaceName2:
                        reactionName = (
                            mol1
                            + "("
                            + interfaceName1
                            + ")"
                            + "-"
                            + mol2
                            + "("
                            + interfaceName2
                            + ")"
                        )
                    else:
                        reactionName = (
                            mol2
                            + "("
                            + interfaceName2
                            + ")"
                            + "-"
                            + mol1
                            + "("
                            + interfaceName1
                            + ")"
                        )
                if reactionName not in builtReactions:
                    builtReactions += (reactionName,)
                    reaction = Reaction(
                        reactionName,
                        [
                            mol1 + "(" + interfaceName1 + ")",
                            mol2 + "(" + interfaceName2 + ")",
                        ],
                        mol1
                        + "("
                        + interfaceName1
                        + "!1)"
                        + "."
                        + mol2
                        + "("
                        + interfaceName2
                        + "!1)",
                    )
                    reaction.angles = self.calculateAngles(
                        np.array([chain.COM.x, chain.COM.y, chain.COM.z]),
                        np.array(
                            [
                                chains[interface.partner].COM.x,
                                chains[interface.partner].COM.y,
                                chains[interface.partner].COM.z,
                            ]
                        ),
                        np.array(
                            [interface.coord.x, interface.coord.y, interface.coord.z]
                        ),
                        np.array(
                            [
                                partnerInterface.coord.x,
                                partnerInterface.coord.y,
                                partnerInterface.coord.z,
                            ]
                        ),
                        np.array([0, 0, 1]),
                        np.array([0, 0, 1]),
                    )
                    reaction.norm1 = [0, 0, 1]
                    reaction.norm2 = [0, 0, 1]
                    reaction.sigma = np.linalg.norm(
                        np.array(
                            [interface.coord.x, interface.coord.y, interface.coord.z]
                        )
                        - np.array(
                            [
                                partnerInterface.coord.x,
                                partnerInterface.coord.y,
                                partnerInterface.coord.z,
                            ]
                        )
                    )
                    reaction.sigma = reaction.sigma / 10.0
                    reaction.energy = interface.energy
                    reaction.size = [interface.size, partnerInterface.size]
                    reactions.append(reaction)

    def calculateAngles(self, c1, c2, p1, p2, n1, n2):
        """
        Determine the angles of the reaction (theta1, theta2, phi1, phi2, omega) given the coordinates of the two Center of Mass (c1 and c2) and two reaction sites (p1 and p2), and two norm vectors (n1 and n2).

        Parameters
        ----------
        c1 : numpy.array
            Center of Mass vector for the first molecule.
        c2 : numpy.array
            Center of Mass vector for the second molecule.
        p1 : numpy.array
            Reaction site vector for the first molecule.
        p2 : numpy.array
            Reaction site vector for the second molecule.
        n1 : numpy.array
            Norm vector for the first molecule.
        n2 : numpy.array
            Norm vector for the second molecule.

        Returns
        -------
        tuple
            The tuple (theta1, theta2, phi1, phi2, omega), where theta1, theta2, phi1, phi2, omega are the angles in radians.
        """
        v1 = p1 - c1
        v2 = p2 - c2
        sigma1 = p1 - p2
        sigma2 = -sigma1

        theta1 = np.arccos(
            np.dot(v1, sigma1) / (np.linalg.norm(v1) * np.linalg.norm(sigma1))
        )
        theta2 = np.arccos(
            np.dot(v2, sigma2) / (np.linalg.norm(v2) * np.linalg.norm(sigma2))
        )

        t1 = np.cross(v1, sigma1)
        t2 = np.cross(v1, n1)
        norm_t1 = t1 / np.linalg.norm(t1)
        norm_t2 = t2 / np.linalg.norm(t2)
        phi1 = np.arccos(np.dot(norm_t1, norm_t2))

        # the sign of phi1 is determined by the direction of t2 relative to the right-hand rule of cross product of v1 and t1
        if np.dot(np.cross(v1, t1), t2) > 0:
            phi1 = -phi1

        t1 = np.cross(v2, sigma2)
        t2 = np.cross(v2, n2)
        norm_t1 = t1 / np.linalg.norm(t1)
        norm_t2 = t2 / np.linalg.norm(t2)
        phi2 = np.arccos(np.dot(norm_t1, norm_t2))

        # the sign of phi2 is determined by the direction of t2 relative to the right-hand rule of cross product of v2 and t1
        if np.dot(np.cross(v2, t1), t2) > 0:
            phi2 = -phi2

        if not np.isclose(np.linalg.norm(np.cross(v1, sigma1)), 0) and not np.isclose(
            np.linalg.norm(np.cross(v2, sigma2)), 0
        ):
            t1 = np.cross(sigma1, v1)
            t2 = np.cross(sigma1, v2)
        else:
            t1 = np.cross(sigma1, n1)
            t2 = np.cross(sigma1, n2)

        omega = np.arccos(np.dot(t1, t2) / (np.linalg.norm(t1) * np.linalg.norm(t2)))

        # the sign of omega is determined by the direction of t2 relative to the right-hand rule of cross product of sigma1 and t1
        if np.dot(np.cross(sigma1, t1), t2) > 0:
            omega = -omega

        return theta1, theta2, phi1, phi2, omega


class Molecule:
    def __init__(self, name):
        self.name = name
        self.COM = None
        self.COMVisual = None
        self.interfaces = []
        self.viewWidget = None
        self.radius = 0.0
        self.D = 0.0
        self.Dr = 0.0


class Intf:
    def __init__(self, name, positions):
        self.name = name
        self.positions = positions
        self.positionsVisual = None
        self.states = []


class State:
    def __init__(self, name):
        self.name = name


class Reaction:
    def __init__(self, name, reactants, products):
        self.name = name
        self.reactants = reactants
        self.products = products
        self.reverse = True
        self.onRate = 10.0
        self.offRate = 1.0
        self.angles = []
        self.norm1 = []
        self.norm2 = []
        self.sigma = 0.0
        self.energy = 0.0
        self.size = 0


class Chain:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.residues = []
        self.COM = None
        self.interfaces = []
        self.atoms = []


class Residue:
    def __init__(self, index):
        self.index = index
        self.atoms = []
        self.chain = -1
        self.CA = -1
        self.isDNA = False


class Coord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distanceSquare(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        dsquare = dx * dx + dy * dy + dz * dz
        return dsquare

    # define the - between Coord and list, return list
    def __sub__(self, other):
        return [self.x - other[0], self.y - other[1], self.z - other[2]]


class Atom:
    def __init__(
        self, index, atomType, residueType, chainName, chainIndex, residueIndex, coord
    ):
        self.index = index
        self.atomType = atomType
        self.residueType = residueType
        self.chainName = chainName
        self.chainIndex = chainIndex
        self.resideIndex = residueIndex
        self.coord = coord


class Interface:
    def __init__(self, index, partner):
        self.index = index
        self.partner = partner
        self.coord = None
        self.name = None
        self.chain = -1
        self.energy = 0.0
        self.atomsNum = 0
        self.residuesNum = 0
        self.size = 0


class AdvancedOptionsParsePDB(QDialog, Ui_DialogParseParam):
    def __init__(self, parent=None):
        super(AdvancedOptionsParsePDB, self).__init__(parent)
        self.setupUi(self)
        self.cutoff = 3.5
        self.thresholdResidue = 3
        self.stretchFactor = 1.0
        self.pushButtonApply.clicked.connect(self.apply)
        self.pushButtonCancel.clicked.connect(self.cancel)

    def apply(self):
        self.cutoff = float(self.lineEditCutoff.text())
        self.thresholdResidue = int(self.lineEditThreshold.text())
        self.stretchFactor = float(self.lineEditStretch.text())
        self.close()

    def cancel(self):
        self.close()


class PDBMoviePlayer(QDialog, Ui_Form):
    def __init__(self, parent=None, path: str = ""):
        super(PDBMoviePlayer, self).__init__(parent)
        self.setupUi(self)
        self.path = path
        if not self.path:
            self.path = QFileDialog.getExistingDirectory(
                self, "Select Simulation Folder"
            )
        self.timeStep = 0.1
        inp_files = glob.glob(self.path + "/*.inp")
        with open(inp_files[0], "r") as inp_file:
            for line in inp_file:
                line = line.strip()
                if line.startswith("timeStep"):
                    self.timeStep = float(line.split("=")[1]) * 1e-6
                if line.startswith("pdbWrite"):
                    self.timeStep *= int(line.split("=")[1])
        self.path = os.path.join(self.path, "PDB")
        self.pushButtonPlay.clicked.connect(self.play)
        self.pushButtonPause.clicked.connect(self.pause)
        self.pushButtonQuit.clicked.connect(self.quit)
        self.pdb_files = sorted(glob.glob(os.path.join(self.path, "*.pdb")))
        self.glview = gl.GLViewWidget(self.openGLWidgetMovie)
        self.glview.setCameraPosition(distance=2500)
        self.openGLLayout = QVBoxLayout(self.openGLWidgetMovie)
        self.openGLLayout.addWidget(self.glview)
        self.openGLWidgetMovie.setLayout(self.openGLLayout)

        self.scatter = gl.GLScatterPlotItem()
        self.glview.addItem(self.scatter)

        self.current_frame = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def play(self):
        self.timer.start(10)

    def update_frame(self):
        if self.current_frame < len(self.pdb_files):
            self.visualize_pdb(self.pdb_files[self.current_frame])
            self.labelMovie.setText(f"Time: {self.current_frame * self.timeStep:.5f}s")
            self.current_frame += 1
        else:
            self.timer.stop()
            self.current_frame = 0

    def visualize_pdb(self, pdb_file):
        for item in self.glview.items[:]:
            if isinstance(item, gl.GLScatterPlotItem):
                self.glview.removeItem(item)

        parser = PDB.PDBParser()
        structure = parser.get_structure("structure", pdb_file)

        def add_scatter_data(coords_chunk, color_data_chunk):
            color_data_chunk = np.array(color_data_chunk, dtype=np.float32)
            scatter = gl.GLScatterPlotItem(
                pos=coords_chunk, color=color_data_chunk, size=2
            )
            self.glview.addItem(scatter)

        coords = []
        color_data = []

        for idx, chain in enumerate(structure.get_chains()):
            chain_color = colors[0]
            for atom in chain.get_atoms():
                coords.append(atom.coord)
                color_data.append(chain_color)
                if len(coords) >= 500:
                    add_scatter_data(coords, color_data)
                    coords = []
                    color_data = []

        if coords:
            add_scatter_data(coords, color_data)

    def pause(self):
        self.timer.stop()

    def quit(self):
        self.close()


class PlotCopyNum(QDialog, Ui_PlotCopyNum):
    def __init__(self, parent=None, path: str = ""):
        super(PlotCopyNum, self).__init__(parent)
        self.setupUi(self)
        self.path = path
        if not self.path:
            self.path = QFileDialog.getExistingDirectory(
                self, "Select Simulation Folder"
            )
        self.path = os.path.join(self.path, "copy_numbers_time.dat")

        self.pushButtonPlotSpecies.clicked.connect(self.plot_species)
        self.pushButtonSaveSpecies.clicked.connect(self.save_species)

        self.data = pd.read_csv(self.path, delimiter=",")
        self.listWidgetSpecies.clear()
        self.listWidgetSpecies.addItems(self.data.columns[1:])

    def plot_species(self):
        if self.data is None:
            return
        selected_species = [
            item.text() for item in self.listWidgetSpecies.selectedItems()
        ]
        if not selected_species:
            return
        self.widget.ax.clear()
        if self.radioButtonPlotSep.isChecked():
            for species in selected_species:
                self.widget.ax.plot(
                    self.data["Time (s)"], self.data[species], label=species
                )
        elif self.radioButtonPlotSum.isChecked():
            self.widget.ax.plot(
                self.data["Time (s)"],
                self.data[selected_species].sum(axis=1),
                label="Total",
            )
        self.widget.ax.set_xlabel("Time (s)")
        self.widget.ax.set_ylabel("Copy Number")
        self.widget.ax.legend()
        self.widget.canvas.draw()

    def save_species(self):
        if self.data is None:
            return
        selected_species = [
            item.text() for item in self.listWidgetSpecies.selectedItems()
        ]
        if not selected_species:
            return
        save_path = QFileDialog.getSaveFileName(
            self, "Save Copy Number", "", "CSV (*.csv)"
        )
        if save_path[0]:
            if self.radioButtonPlotSep.isChecked():
                self.data[["Time (s)"] + selected_species].to_csv(
                    save_path[0], index=False
                )
            elif self.radioButtonPlotSum.isChecked():
                # Compute the sum of the selected species
                summed_data = self.data[selected_species].sum(axis=1)
                # Create a new DataFrame with 'Time (s)' and the computed sum
                df_to_save = pd.DataFrame(
                    {"Time (s)": self.data["Time (s)"], "Sum": summed_data}
                )
                df_to_save.to_csv(save_path[0], index=False)


class PlotComplex(QDialog, Ui_PlotComplex):
    def __init__(self, parent=None, path: str = ""):
        super(PlotComplex, self).__init__(parent)
        self.setupUi(self)
        self.path = path
        if not self.path:
            self.path = QFileDialog.getExistingDirectory(
                self, "Select Simulation Folder"
            )
        self.path = os.path.join(self.path, "histogram_complexes_time.dat")
        with open(self.path, "r") as f:
            lines = f.readlines()

        self.species = set()
        for line in lines:
            line = line.strip()

            if line.startswith("Time (s):") and self.species:
                break

            if not line.startswith("Time (s):"):
                parts = line.split("\t")[1].split(".")
                for part in parts:
                    name = part.split(":")[0].strip()
                    if name != "":
                        self.species.add(name)

        self.listWidgetComplex.clear()
        self.species = list(sorted(self.species))
        self.species_num = [0 for _ in range(len(self.species))]
        self.listWidgetComplex.addItems(
            [
                f"{self.species[i]}: {self.species_num[i]}"
                for i in range(len(self.species))
            ]
        )

        self.pushButtonPlotComplex.clicked.connect(self.plot_complex)
        self.pushButtonPlotComplexStoi.clicked.connect(self.plot_complex_stoi)
        self.pushButtonSaveComplex.clicked.connect(self.save_complex)

        self.time = None
        self.counts = None

    def plot_complex(self):
        time = []
        counts = []
        current_time = None
        count_for_time = 0
        components = []
        for i in range(len(self.species)):
            if self.species_num[i] > 0:
                components.append(f"{self.species[i]}: {self.species_num[i]}")
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Time (s):"):
                    if current_time is not None:
                        time.append(current_time)
                        counts.append(count_for_time)
                    current_time = float(line.split(":")[1].strip())
                    count_for_time = 0
                else:
                    count, comp = line.split("\t")
                    comp_list = comp.strip().split(". ")[:]
                    comp_list[-1] = comp_list[-1][:-1]
                    comp_list = sorted(comp_list)
                    if comp_list == components:
                        count_for_time += int(count)
            if current_time is not None:
                time.append(current_time)
                counts.append(count_for_time)

        self.widget.ax.clear()
        self.widget.ax.plot(time, counts)
        self.widget.ax.set_xlabel("Time (s)")
        self.widget.ax.set_ylabel("Count")
        self.widget.canvas.draw()
        self.time = time
        self.counts = counts

    def plot_complex_stoi(self):
        # pop out a dialog to get the stoi, provide a box for each species
        stoi_dialog = QDialog(self)
        stoi_dialog.setWindowTitle("Stoichiometry")
        stoi_dialog.setModal(True)
        stoi_dialog.resize(300, 200)

        layout = QVBoxLayout(stoi_dialog)
        stoi_dialog.setLayout(layout)

        # A dictionary to store QLineEdit widgets for each species
        line_edits = []

        for species in self.species:
            layout.addWidget(QLabel(species))
            le = QLineEdit()
            layout.addWidget(le)
            # Associate the species name with its QLineEdit
            line_edits.append(le)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttonBox)

        # Connect the button signals
        buttonBox.accepted.connect(stoi_dialog.accept)
        buttonBox.rejected.connect(stoi_dialog.reject)

        # If the dialog was accepted (OK pressed), retrieve the stoichiometries
        if stoi_dialog.exec_() == QDialog.Accepted:
            for i in range(len(line_edits)):
                self.species_num[i] = int(line_edits[i].text())

        self.listWidgetComplex.clear()
        self.listWidgetComplex.addItems(
            [
                f"{self.species[i]}: {self.species_num[i]}"
                for i in range(len(self.species))
            ]
        )

    def save_complex(self):
        save_path = QFileDialog.getSaveFileName(
            self, "Save Complex Count", "", "CSV (*.csv)"
        )
        if save_path[0]:
            df_to_save = pd.DataFrame({"Time (s)": self.time, "Count": self.counts})
            df_to_save.to_csv(save_path[0], index=False)


class InstallNERDSS(QDialog, Ui_NERDSSInstall):
    def __init__(self, parent=None):
        super(InstallNERDSS, self).__init__(parent)
        self.setupUi(self)
        self.installPath = None
        self.pushButtonInstall.clicked.connect(self.install)
        self.pushButtonCancel.clicked.connect(self.cancel)
        self.pushButtonInstallPath.clicked.connect(self.set_install_path)

    def execute_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(
                self, "Error", f"Error running command: {e.cmd}\nError: {e}"
            )
            return False

    def install(self):
        # Change to the install directory
        print(f"NERDSS install path: {self.installPath}")
        os.chdir(self.installPath)

        # Clone the NERDSS repository
        if not self.execute_command(
            f"git clone https://github.com/mjohn218/NERDSS.git {self.installPath}/NERDSS"
        ):
            return

        # Install the Dependencies
        print(f"Platform: {sys.platform}")
        if sys.platform.startswith("linux"):
            if not self.execute_command(
                "sudo apt-get update && sudo apt-get install -y build-essential libgsl-dev"
            ):
                return
        elif sys.platform == "darwin":  # macOS
            if not self.execute_command(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            ):
                return
            print("homebrew installed.")
            if not self.execute_command("brew update && brew install gcc gsl"):
                return
            print("gcc and gsl installed.")

        # Build NERDSS
        os.chdir(f"{self.installPath}/NERDSS")
        if not self.execute_command("make serial"):
            return
        print("NERDSS built.")

        QMessageBox.information(
            self, "Success", "NERDSS has been installed successfully!"
        )
        self.close()

    def cancel(self):
        self.close()

    def set_install_path(self):
        self.installPath = QFileDialog.getExistingDirectory(
            self, "Select NERDSS install Folder"
        )
        self.lineEditInstallPath.setText(self.installPath)


class SimulationApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()

        self.glview = gl.GLViewWidget(self.openGLWidgetStructure)
        self.glview.setCameraPosition(distance=150)
        self.openGLLayout = QVBoxLayout(self.openGLWidgetStructure)
        self.openGLLayout.addWidget(self.glview)
        self.openGLWidgetStructure.setLayout(self.openGLLayout)

        self.scatter = gl.GLScatterPlotItem()
        self.glview.addItem(self.scatter)
        self.cutoff = 3.5
        self.thresholdResidue = 3
        self.stretchFactor = 1.0
        self.geometric_center = None

        self.progressBar.setValue(0)

    def setup_connections(self):
        self.pushButtonBrowseFile.clicked.connect(self.open_file_dialog)
        self.pushButtonParse.clicked.connect(self.parse_file)
        self.pushButtonAdvance.clicked.connect(self.open_advance_parameters)
        self.pushButtonGenerateNerdssInput.clicked.connect(self.save_nerdss_inputs)
        self.pushButtonInstallNERDSS.clicked.connect(self.install_nerdss)
        self.pushButtonSelectNERDSS.clicked.connect(self.select_nerdss)
        self.pushButtonSelectInputs.clicked.connect(self.select_inputs)
        self.pushButtonVisualizeTraj.clicked.connect(self.visualize_traj)
        self.pushButtonPlotCopyNum.clicked.connect(self.plot_copy_num)
        self.pushButtonPlotComplex.clicked.connect(self.plot_complex)
        self.commandLinkButtonRunSimulation.clicked.connect(self.run_simulation)

    def run_simulation(self):
        os.chdir(self.lineEditInputsFolder.text())
        # copy nerdss to the inputs folder
        shutil.copy(self.lineEditNERDSSExe.text(), self.lineEditInputsFolder.text())
        # run nerdss
        cmd = "./nerdss -f *.inp > output.log"
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # start a QTimer to periodically check the progress and update the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_progress(process))
        self.timer.start(30000)

    def update_progress(self, process):
        progress_percentage = self.calculate_progress_percentage()
        self.progressBar.setValue(progress_percentage)

        return_code = process.poll()
        if return_code is not None:
            self.timer.stop()
            if return_code == 0:
                QMessageBox.information(
                    self, "Success", "Simulation has been completed successfully!"
                )
            else:
                QMessageBox.critical(self, "Error", "Simulation has failed!")

    def calculate_progress_percentage(self):
        current_time = 0.0
        try:
            # find the last second line of the copy_numbers_time.dat file using the tail -n 2 command
            cmd = "tail -n 2 copy_numbers_time.dat"
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            output = output.decode("utf-8")
            lines = output.split("\n")
            last_line = lines[-2]
            current_time = float(last_line.split(",")[0])
        except Exception as e:
            pass

        total_time = 0.0
        try:
            # find the nItr and timeStep from the *.inp file
            nItr = 0
            timeStep = 0.0
            inp_files = glob.glob(self.lineEditInputsFolder.text() + "/*.inp")
            with open(inp_files[0], "r") as inp_file:
                for line in inp_file:
                    line = line.strip()
                    if line.startswith("nItr"):
                        nItr = int(line.split("=")[1])
                    if line.startswith("timeStep"):
                        timeStep = float(line.split("=")[1]) * 1e-6
            total_time = nItr * timeStep
        except Exception as e:
            raise e

        if total_time == 0.0:
            return 0
        else:
            return int(current_time / total_time * 100)

    def open_file_dialog(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open file", "", "PDB files (*.pdb);;All files (*)"
        )
        self.lineEditFilePath.setText(filename[0])

    def select_nerdss(self):
        filename = QFileDialog.getOpenFileName(
            self, "Select NERDSS", "", "NERDSS executable (*)"
        )
        self.lineEditNERDSSExe.setText(filename[0])

    def parse_file(self):
        try:
            parser = PDB.PDBParser()
            structure = parser.get_structure("structure", self.lineEditFilePath.text())

            # Computer the geometric center of the structure
            sum_coords = [0.0, 0.0, 0.0]
            atom_count = 0
            for atom in structure.get_atoms():
                sum_coords[0] += atom.coord[0]
                sum_coords[1] += atom.coord[1]
                sum_coords[2] += atom.coord[2]
                atom_count += 1

            self.geometric_center = [coord / atom_count for coord in sum_coords]

            # Shift coordinates and assign colors based on chains
            coords = []
            color_data = []

            for item in self.glview.items[:]:
                if isinstance(item, gl.GLScatterPlotItem):
                    self.glview.removeItem(item)

            def add_scatter_data(coords_chunk, color_data_chunk):
                color_data_chunk = np.array(color_data_chunk, dtype=np.float32)
                scatter = gl.GLScatterPlotItem(pos=coords_chunk, color=color_data_chunk)
                self.glview.addItem(scatter)

            for idx, chain in enumerate(structure.get_chains()):
                chain_color = colors[idx % len(colors)]
                for atom in chain.get_atoms():
                    shifted_coord = atom.coord - self.geometric_center
                    coords.append(shifted_coord)
                    color_data.append(chain_color)
                    if len(coords) >= 500:
                        add_scatter_data(coords, color_data)
                        coords = []
                        color_data = []

            if coords:
                add_scatter_data(coords, color_data)
        except Exception as e:
            errorDialog = QErrorMessage(self)
            errorDialog.showMessage("Error: " + str(e))

        try:
            self.longTaskThread = LongTaskThread()
            self.longTaskThread.set_filename(self.lineEditFilePath.text())
            self.longTaskThread.set_cutoff(self.cutoff)
            self.longTaskThread.set_threshold_residue(self.thresholdResidue)
            self.longTaskThread.set_stretch_factor(self.stretchFactor)
            self.longTaskThread.set_geometric_center(self.geometric_center)
            self.longTaskThread.finished_signal.connect(self.parse_finished)
            self.longTaskThread.start()

            # show a message to the user
            self.msgBox = QMessageBox(self)
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Parsing the pdb file, please wait...")
            self.msgBox.setWindowTitle("Parsing...")
            self.msgBox.setStandardButtons(QMessageBox.NoButton)
            self.msgBox.show()
        except Exception as e:
            errorDialog = QErrorMessage(self)
            errorDialog.showMessage("Error: " + str(e))

    def parse_finished(self):
        # Visualize the molecule in the GUI, put it on top of the pdb structure
        # Represent the COM and interfaces as spheres
        # Connect the COM and interfaces with lines
        # for item in self.glview.items[:]:
        #     if isinstance(item, gl.GLScatterPlotItem):
        #         self.glview.removeItem(item)
        for idx, molecule in enumerate(molecules):
            molecule_color = colors2[idx % len(colors2)]
            coords = []
            color_data = []
            com = molecule.COMVisual - self.geometric_center
            coords.append(com)
            color_data.append(molecule_color)
            for intf in molecule.interfaces:
                intf_coord = intf.positionsVisual - self.geometric_center
                coords.append(intf_coord)
                color_data.append(molecule_color)
            color_data = np.array(color_data, dtype=np.float32)
            scatter = gl.GLScatterPlotItem(pos=coords, color=color_data)
            self.glview.addItem(scatter)
            for intf in molecule.interfaces:
                intf_coord = intf.positionsVisual - self.geometric_center
                line = gl.GLLinePlotItem(
                    pos=np.array([com, intf_coord]), color=molecule_color
                )
                self.glview.addItem(line)
        self.msgBox.accept()

    def open_advance_parameters(self):
        self.dialogParsePDBParam = AdvancedOptionsParsePDB(self)
        self.dialogParsePDBParam.exec_()
        self.cutoff = self.dialogParsePDBParam.cutoff
        self.thresholdResidue = self.dialogParsePDBParam.thresholdResidue
        self.stretchFactor = self.dialogParsePDBParam.stretchFactor
        print(
            f"cutoff: {self.cutoff}, thresholdResidue: {self.thresholdResidue}, stretchFactor: {self.stretchFactor}"
        )

    def select_inputs(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.lineEditInputsFolder.setText(folder)

    def save_nerdss_inputs(self):
        # Pop up a dialog to ask for the folder to save the input files
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        # Save the molecule file
        for mol in molecules:
            with open(os.path.join(folder, mol.name + ".mol"), "w") as mol_file:
                mol_file.write(f"Name = {mol.name}\n")
                mol_file.write("checkOverlap = true\n\n")
                mol_file.write(f"D = [{mol.D:.2f}, {mol.D:.2f}, {mol.D:.2f}]\n\n")
                mol_file.write(f"Dr = [{mol.Dr:.2f}, {mol.Dr:.2f}, {mol.Dr:.2f}]\n\n")
                mol_file.write("COM\t0.0000\t0.0000\t0.0000\n")
                for intf in mol.interfaces:
                    mol_file.write(
                        f"{intf.name}\t{intf.positions[0]:.4f}\t{intf.positions[1]:.4f}\t{intf.positions[2]:.4f}\n"
                    )
                mol_file.write("\n")
                mol_file.write(f"bonds = {len(mol.interfaces)}\n")
                for intf in mol.interfaces:
                    mol_file.write(f"com {intf.name}\n")

        # Save the parameter file
        with open(os.path.join(folder, "parms.inp"), "w") as parm_file:
            parm_file.write("start parameters\n")
            parm_file.write("\tnItr = 1000000\n")
            parm_file.write("\ttimeStep = 0.1\n")
            parm_file.write("\ttimeWrite = 100\n")
            parm_file.write("\ttrajWrite = 100000\n")
            parm_file.write("\tpdbWrite = 1000\n")
            parm_file.write("\trestartWrite = 1000\n")
            parm_file.write("\tscaleMaxDisplace = 100.0\n")
            parm_file.write("\toverlapSepLimit = 1.0\n")
            parm_file.write("end parameters\n\n")
            parm_file.write("start boundaries\n")
            parm_file.write("\tWaterBox = [500.0, 500.0, 500.0]\n")
            parm_file.write("end boundaries\n\n")
            parm_file.write("start molecules\n")
            for mol in molecules:
                parm_file.write(f"\t{mol.name} : 100\n")
            parm_file.write("end molecules\n\n")
            parm_file.write("start reactions\n")
            for rect in reactions:
                parm_file.write(
                    f"\t{rect.reactants[0]} + {rect.reactants[1]} <-> {rect.products}\n"
                )
                parm_file.write("\t\tonRate3Dka = 10.0\n")
                parm_file.write("\t\toffRatekb = 1.0\n")
                parm_file.write(f"\t\tsigma = {rect.sigma:.4f}\n")
                parm_file.write(
                    f"\t\tnorm1 = [{rect.norm1[0]:.4f}, {rect.norm1[1]:.4f}, {rect.norm1[2]:.4f}]\n"
                )
                parm_file.write(
                    f"\t\tnorm2 = [{rect.norm2[0]:.4f}, {rect.norm2[1]:.4f}, {rect.norm2[2]:.4f}]\n"
                )
                parm_file.write(
                    f"\t\tassocAngles = [{rect.angles[0]:.4f}, {rect.angles[1]:.4f}, {rect.angles[2]:.4f}, {rect.angles[3]:.4f}, {rect.angles[4]:.4f}]\n"
                )
                parm_file.write(f"\t\texcludeVolumeBound = False\n")
                parm_file.write(
                    f"\t\t#Contact Energy = {rect.energy:.4f}\tInterfaces' size (residues) = {rect.size[0]}, {rect.size[1]}\n\n"
                )
            parm_file.write("end reactions\n")

        # Pop up a message to tell the user the input files have been saved
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(
            f"The input files for NERDSS simulation have been saved to {folder}."
        )
        msgBox.setWindowTitle("Saved")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.show()

    def install_nerdss(self):
        self.dialogInstallNERDSS = InstallNERDSS(self)
        self.dialogInstallNERDSS.exec_()

    def visualize_traj(self):
        self.dialogPDBMoviePlayer = PDBMoviePlayer(
            self, self.lineEditInputsFolder.text()
        )
        self.dialogPDBMoviePlayer.exec_()

    def plot_copy_num(self):
        self.dialogPlotCopyNum = PlotCopyNum(self, self.lineEditInputsFolder.text())
        self.dialogPlotCopyNum.exec_()

    def plot_complex(self):
        self.dialogPlotComplex = PlotComplex(self, self.lineEditInputsFolder.text())
        self.dialogPlotComplex.exec_()


def nerdss():
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    nerdss()
