import numpy as np
from itertools import product
import ase, ase.io
from io import StringIO

def shift_xyz_data(data, shift):
	res = []
	for elem,x,y,z in data:
		res.append( [elem] + list(np.round(np.array([x,y,z]) + np.array(shift), 6)))
	return res
	
def multiply_xyz_data(data, pbcell, multiplier, mulmul):
	new_data = []
	for i in  product(*[list(range(i)) for i in multiplier]):
		shifts = [v*np.array([float(n)]*3) for n,v in zip(i, pbcell.cell.cell_basis)]
		shift = sum(shifts)*mulmul	# little gap b/w images
		new_data += shift_xyz_data(data, shift)
	return new_data
	
def generate_xyz(data, comment='', pbcell = None, multiplier = [1,1,1], mulmul=1.0):
	if pbcell is not None:
		data = [ [e] + list(pbcell.wrap_in_cell_orhonorm([x,y,z], precission=3)) for e,x,y,z in data ]
		data = multiply_xyz_data(data[:], pbcell, multiplier, mulmul)

	comment = 'Lattice="{}" Comment="{}"'.format (  " ".join(map(str, np.array(pbcell.cell.cell_basis).ravel())), comment )
	#res = str(len(data)) + '\n' + comment + "\n"
	res = ""
	N = 0
	for row in data:
		if row[0] != 'XX':
			res += '\t'.join([str(x) for x in row]) + '\n';
			N +=1
			
	return str(N) + '\n' + comment + "\n" + res

def oneline_xyz(data):		
	return '; '.join( ['(' + ', '.join([str(x) for x in row]) + ')' for row in data])


'''	
def write_xyz(cells, regr, unique_lcs, filename, comment, marks):
	regr.mark_by_cells(cells, unique_lcs, marks)
	
	output = open(filename, 'w')
	output.write(generate_xyz(regr.generate_xyz_data(hide=[]), comment=comment))
'''

def shifted_xyz_mark(marks, idx, lctype, coords):
	m = marks[ (idx,lctype) ]
	if isinstance(m, str):
		return [ m ] + list(coords)
	else:
		return [ m[0] ] + list(coords + m[1])

"""
def xyz_for_lc_state(lc_state, cl, atoms, marks):

	incell_shifts = [cl.to_orthonorm_basis(c) for _,c in atoms]
	
	data = []
	for lc,shift in zip(lc_state, incell_shifts):
		cc_dict = lc.to_cart_config_dict(shift)
		data += [shifted_xyz_mark(marks, idx,lc.lctype,coords) for coords,idx in cc_dict.iteritems()]
		
	return data[:]
"""

def get_lc_xyz_data(lc, marks, shift=tuple([0., 0., 0.])):
	cc_dict = lc.to_cart_config_dict(shift)
	data = [ [marks[idx] ] + list(np.round(coords, 6) ) for coords,idx in cc_dict.items()]
	return data[:]

	


def gen_xyz_data(cells, regr, lc_marker, pbc_wrapper, with_lattice):
	data = []
	for cell_i,cell in enumerate(cells):
		if any(cell):		
			for lci,x in enumerate(cell):
				if (x):
					zero_coords = regr[cell_i].coords
					unwrapped_data = lc_marker(lci)
					data += [ [row[0]] + list( pbc_wrapper( zero_coords + row[1:] ) ) for row in unwrapped_data]
		else:
			if with_lattice:
				data.append( ['H'] + list(regr[cell_i].coords) ) 
	return data
	
def write_xyz_2(cells, regr, lc_marker, filename, comment, pbc_wrapper, with_lattice=True, background = []):
	output = open(filename, 'w')
	data = background + gen_xyz_data( cells, regr, lc_marker, pbc_wrapper, with_lattice)
	output.write( generate_xyz(data, comment=comment ))
	return data

def cells_as_xyz_data(regr, cells, rn_states):
	assert (cells is not None)
	xyz_data = []
	for i, (cell, vertex) in enumerate(zip(cells, regr.vertex_index)):
		state = rn_states[cell]
		c0 = vertex.coords
		print (i, len(cells))
		xyz = state.get_prop('xyz_mark', 1)
		xyz_data += shift_xyz_data(xyz, c0)
	return xyz_data
	
def cells_as_Atoms(regr, cells, rn_states):
	assert (cells is not None)
	
	atoms = []
	for state in rn_states:
		xyz_mark = state.get_prop('xyz_mark', 1)
		elements = [e for e,_,_,_ in xyz_mark]
		positions = [[x,y,z] for _,x,y,z in xyz_mark]
		a = ase.Atoms(positions = positions, symbols=elements)
		atoms.append(a)
	
	res = ase.Atoms()
	for i, (cell, vertex) in enumerate(zip(cells, regr.vertex_index)):
		c0 = vertex.coords
		a = atoms[cell].copy()
		a.translate(c0)
		res.extend(a)
	return res

def save_lattice_as_xyz(fn, lattice, comment='', multiplier = [1,1,1], mulmul=0.0):
	"""
		Dump current state of the lattice as XYZ file.
		
		Parameters:
			:fn: filename to append current state
			:m: Lattice object to be dumped
			:comment: comment section of the XYZ file
			:multiplier: three-element list of multipliers for dumping multiple images as a supercell
			:mulmul: gap size between copies in a supercell
	"""
	regr, cells, states = lattice.regr, lattice.cells, lattice.lattice_task.states
	
	assert cells is not None
	atoms = cells_as_Atoms(regr, cells, states)
	atoms.cell = lattice.regr.pbcell.cell.cell_basis
	atoms.cell += np.eye(3) * mulmul
	atoms.cell = np.round(atoms.cell, 6)
	
	s = StringIO()
	atoms.info['comment']='"{}"'.format(comment)
	ase.io.write(s, [atoms], 'extxyz', parallel=False)
	
	with open(fn,'a') as f:
		f.write(s.getvalue())
	
	return s.getvalue()
	
def property_image(regr, cells, states, prop_name, ppa, beta=None):
	coords = []
	values = []
	for cell, vertex in zip(cells, regr.vertex_index):
		state = states[cell]
		v = state.get_prop(prop_name, beta)
		c = vertex.coords[:2]
		coords += [c]
		values += [v]
	
	coords = np.array(coords)
	

	
	cell_vectors = np.array(regr.pbcell.cell.cell_basis)
	print('cell_vectors', cell_vectors)
	cell_vertices = []
	#for p_int, p_float in [ (k,np.sum(cell_vectors * k, axis=0)) for k in product([0., 1.], repeat=3)]:
	for k in product([0., 1.], repeat=3):
		p_float = cell_vectors.T.dot(k)
		print('p_float', p_float)
		cell_vertices += [p_float]
	cell_vertices = np.array(cell_vertices)

	#print 'cell_vertices', cell_vertices.shape, '\n:', cell_vertices
	#print 'cell_vertices.max(axis=0)', cell_vertices.max(axis=0)
	#print 'cell_vertices.max(axis=1)', cell_vertices.max(axis=1)
	maxx, maxy, _ = cell_vertices.max(axis=0)
	minx, miny, _ = cell_vertices.min(axis=0)
	print('maxx', maxx)
	print('maxy', maxy)
	
	coords -= [minx, miny]
	coords *= float(ppa)
	
	img = np.zeros(( int( (maxx-minx) * ppa), int( (maxy - miny) * ppa) ))
	
	for c,v in zip(coords, values):
		img[int(c[0]), int(c[1]) ] = v


	return img
	


def save_gnuplot_image(a, fn='plot', dat_fn=None, png_fn=None):
	if dat_fn is None:
		dat_fn = fn + '.dat'
		
	if png_fn is None:
		png_fn = fn + '.png'
	
	with open(dat_fn,'w') as f:
		f.write('set size ratio -1; set xrange [0:{}]; set yrange [0:{}] \n'.format(*a.shape))
		#f.write("set palette gray negative\n")
		f.write("set palette gray positive\n")
		f.write("set terminal png size 1600,1200\n")
		f.write("set output '{}'\n".format(png_fn))
		f.write("plot '-' u 2:1:3 matrix with image\n")
		for r in a:
			f.write(' '.join(map(str, r )) + '\n')
		f.write('e\ne\n')
		# gnuplot -p -e "plot 'plot.dat' u 2:1:3 matrix with image"
		# gnuplot plot.dat
	


