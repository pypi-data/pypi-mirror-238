from math import sqrt
from .cell import make_3d_cell, make_2d_cell, make_supercell, Cell


def make_fcc_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a, alpha=60, beta=60, gamma=60)
	atoms=[("Pt", [.0, .0, .0])]
	return (cell, atoms)

def make_fcc_orthogonal_cell(a):
	cell = make_3d_cell(a=a*sqrt(2), b=a*sqrt(2), c=a*sqrt(2), alpha=90, beta=90, gamma=90)	
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.0, .5, .5]), ("Pt", [.5, .0, .5]), ("Pt", [.5, .5, .0])]
	return (cell, atoms)
	
def make_fcc111_2layer_plane_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a*2, alpha=60, beta=60, gamma=60)
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.0, .0, .5])]
	return (cell, atoms)

	
def make_fcc111_orthogonal_cell(a):
	cell = make_3d_cell(a=a, b=a*sqrt(3), c=a*sqrt(6), alpha=90, beta=90, gamma=90)	
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.5, .5, .0]), ("Pt", [.0, 2./3., 1./3.]), ("Pt", [.5, 1./6., 1./3.]), ("Pt", [.0, 1./3., 2./3.]), ("Pt", [.5, 5./6., 2./3.])]
	return (cell, atoms)

def make_cubic_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a, alpha=90, beta=90, gamma=90)
	atoms=[("Pt", [.0, .0, .0])]	
	return (cell, atoms)
	
def make_bcc_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a, alpha=109.3, beta=109.3, gamma=109.3)
	atoms=[("Pt", [.0, .0, .0])]	
	return (cell, atoms)

def make_bcc_orthogonal_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a, alpha=90, beta=90, gamma=90)
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.5, .5, .5])]	
	return (cell, atoms)

def make_hcp_cell(a):
	cell = make_3d_cell(a=a, b=a, c=a*sqrt(6.)*2./3., alpha=90., beta=90., gamma=120.)
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [2./3., 1./3., .5])]	
	return (cell, atoms)

def make_hcp_orthogonal_cell(a):
	cell = make_3d_cell(a=a, b=sqrt(3.)*a, c=a*sqrt(6.)*2./3., alpha=90., beta=90., gamma=90.)	
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.5, 1./6., .5]), ("Pt", [.5, .5, .0]), ("Pt", [1., 2./3., .5])]
	return (cell, atoms)
	
#------------------- planes -------------------------

def make_triangular_Oxy_plane_cell(a):
	cell = Cell([[a,0.,0.], [0.5*a, 0.5*sqrt(3.)*a, 0.], [0.,0.,1.] ] )
	atoms=[("Pt", [.0, .0, .0])]
	return (cell, atoms)
	
def make_triangular_Oxy_plane_cell_neg(a):
	cell = Cell([[a,0.,0.], [-0.5*a, 0.5*sqrt(3.)*a, 0.], [0.,0.,1.] ] )
	atoms=[("Pt", [.0, .0, .0])]
	return (cell, atoms)

def make_triangular_plane_cell(a):
	return make_fcc_cell(a)
		
def make_triangular_orthogonal_plane_cell(a):
	cell = make_3d_cell(a=a, b=sqrt(3.)*a, c=a, alpha=90., beta=90., gamma=90. )
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.5, .5, .0])]
	return (cell, atoms)
	
def make_triangular_orthogonal_bridge_plane_cell(a):
	cell = make_3d_cell(a=a, b=sqrt(3.)*a, c=a, alpha=90., beta=90., gamma=90. )
	atoms=[("Pt", [.5, .0, .0]), ("Pt", [.25, .25, .0]), ("Pt", [.75, .25, .0]),
		("Pt", [.0, .5, .0]), ("Pt", [.25, .75, .0]), ("Pt", [.75, .75, .0]) ]
	return (cell, atoms)

def make_fcc110_plane_cell(a):
	cell = make_3d_cell(a=a, b=sqrt(2.)*a, c=a, alpha=90., beta=90., gamma=90. )
	atoms=[("Pt", [.0, .0, .0])]
	return (cell, atoms)

def make_fcc110_2layer_plane_cell(a):
	cell = make_3d_cell(a=a, b=sqrt(2.)*a, c=a, alpha=90., beta=90., gamma=90. )
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [.5, .5, .0])]
	return (cell, atoms)

def make_square_plane_cell(a):
	return make_cubic_cell(a)

def make_hexagonal_plane_cell(a):
	cell = make_3d_cell(a=sqrt(3.)*a, b=sqrt(3.)*a, c=a, alpha=90., beta=90., gamma=60.)		
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [1./3., 1./3., .0])]
	return (cell, atoms)


		
def make_hexagonal_orthogonal_plane_cell(a):
	cell = make_3d_cell(a=3.*a, b=sqrt(3.)*a, c=a, alpha=90., beta=90., gamma=90.)
	atoms=[("Pt", [.0, .0, .0]), ("Pt", [1./3., .0, .0]), ("Pt", [.5, .5, .0]), ("Pt", [5./6., .5, .0])]
	return (cell, atoms)


def make_cell_from_xyz(fn):
	f = open(fn,'r')
	atoms = []
	
	for i,l in enumerate(f):
		if i == 0:
			N = int(l)
		elif i == 1:
			pass # comment
		else:
			s = l.split()
			v,[x,y,z] = s[0], [float(x) for x in s[1:]]		
			atoms.append((v,[x,y,z]))

	minx = min([x for _,[x,_,_] in atoms])
	miny = min([y for _,[_,y,_] in atoms])
	minz = min([z for _,[_,_,z] in atoms])
	
	
	atoms = [(v,[x-minx,y-miny,z-minz]) for (v,[x,y,z]) in atoms[:]]

	maxx = max([x for _,[x,_,_] in atoms]) + 0.000001
	maxy = max([y for _,[_,y,_] in atoms]) + 0.000001
	maxz = max([z for _,[_,_,z] in atoms]) + 0.000001
	
	
	atoms = [(v,[x/maxx,y/maxy,z/maxz]) for (v,[x,y,z]) in atoms[:]]
	
	
	cell = make_3d_cell(a=maxx, b=maxy, c=maxz, alpha=90., beta=90., gamma=90.)
	
					
	return make_supercell(cell, atoms, [1,1,1]) 
	

