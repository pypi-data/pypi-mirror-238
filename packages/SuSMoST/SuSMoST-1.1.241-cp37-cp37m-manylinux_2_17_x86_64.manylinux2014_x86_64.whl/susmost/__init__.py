from .zmatrix import make_single_point_zmatrix, make_dimer_zmatrix
from .make_struct import make_square_plane_cell, make_hexagonal_plane_cell, \
							make_triangular_plane_cell, make_triangular_orthogonal_plane_cell, \
							make_triangular_Oxy_plane_cell_neg, make_triangular_Oxy_plane_cell
from .make_interaction import nearest_int
from .latconf import normal_lattice_task, joined_cells_lattice_task
from .sitestate import SiteStateType, register_property, register_properties
from .acutils import make_ac_samples, load_lattice_task
from .latticetask import LatticeTask
from .trg import solve_TRG
from .transferm import solve_TM
from .tensors import make_tensor
from .meanfield import solve_MF, solve_QC

import susmost.latconf
latconf.LatticeConfig.__module__ = 'susmost.latconf'
latconf.CellState.__module__ = 'susmost.latconf'
latconf.MergedCellState.__module__ = 'susmost.latconf'
latconf.JoinedCellState.__module__ = 'susmost.latconf'

import susmost.edge
edge.Edge.__module__ = 'susmost.edge'
import susmost.cell
cell.Cell.__module__ = 'susmost.cell'
import susmost.IndexedOrderedDict
IndexedOrderedDict.IndexedOrderedDict.__module__ = 'susmost.IndexedOrderedDict'
import susmost.InteractionMatrix
InteractionMatrix.IMdict.__module__ = 'susmost.InteractionMatrix'
import susmost.pbc
pbc.PBCell.__module__ = 'susmost.pbc'

# https://stackoverflow.com/a/56984285/14736976
from pkg_resources import get_distribution, DistributionNotFound
try:
	__version__ = get_distribution(__name__).version
except DistributionNotFound:
	# package is not installed
	pass

import hashlib
def phash(x):
	'''
	Persistent hash
	
	Parameters:
		:x: any object with defined ``repr(x)``
	Returns:
		``hashlib.md5(repr(x).encode('utf-8')).hexdigest()``
	'''
	return hashlib.md5(repr(x).encode('utf-8')).hexdigest()



__all__ = ['make_ac_samples', 'load_lattice_task', 'normal_lattice_task', 'joined_cells_lattice_task',
	'nearest_int', 'make_single_point_zmatrix', 'make_dimer_zmatrix',
	 'make_square_plane_cell', 'LatticeTask', 'make_hexagonal_plane_cell',
	'make_triangular_plane_cell', 'make_triangular_orthogonal_plane_cell',
	'make_triangular_Oxy_plane_cell', 'make_triangular_Oxy_plane_cell_neg',
	'make_triangular_Oxy_plane_cell_neg', 'SiteStateType',
	'register_property', 'phash', 'make_tensor', 'solve_TRG', 'solve_TM',  'solve_MF', 'solve_QC' ]

