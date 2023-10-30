from math import exp
from .savexyz import shift_xyz_data
from .zmatrix import ZItem
from copy import deepcopy
import numpy as np


class StatePropMetaInfo:
	def __init__(self, pname, merge_func = None, join_func = None, 
					cmp_mode = 'indiff', cmp_func = None):
		self.pname = pname
		self.merge_func = merge_func
		self.join_func = join_func
		self.cmp_mode = cmp_mode
		self.cmp_func = cmp_func
		
	def is_mergable(self):
		return self.merge_func is not None

	def compare(self, v1, v2):
		if self.cmp_mode == '==':
			return v1 == v2
		elif self.cmp_mode == 'cmp_func':
			return self.cmp_func(v1, v2)
		elif self.cmp_mode == 'indiff': # indifferent
			return True
		else:
			assert False, self.cmp_mode

	def __repr__(self):
		return "SPMI " + self.pname + ' ' + str(self.__dict__)
		
	def __eq__(self, other):
		# print 'SPMI __cmp__ ', len(self.__dict__)  , len(other.__dict__)
		for k in self.__dict__:
			if self.__dict__[k] != other.__dict__[k]:
				print('SPMI __cmp__ ', k, self.__dict__[k], other.__dict__[k])
				return False
		return len(self.__dict__) == len(other.__dict__)

class StateProp:
	def __init__(self, name, value):
		self.value = value
		self.meta = SPMI_db[name]

	def equal(self, other):
		assert self.meta == other.meta, (self.meta, other.meta, default_props_meta)
		return self.meta.compare(self.value, other.value)

	def __getstate__(self):
		return (self.meta.pname, self.value)

	def __setstate__(self, state):
		pname,self.value = state
		self.meta = SPMI_db[pname]

	def __repr__(self):
		return str(self.meta.pname) + '=' + str(self.value)


def merge_weighted_avg(values, energies, beta):
	Z = sum([exp(-E*beta) for E in energies])
	return sum([exp(-E*beta)*v for v,E in zip(values, energies)])/Z
	
def merge_most_stable(values, energies, beta):
	i = np.argmin(energies)
	return values[i]

def join_sum(values, energies, shifts):
	return sum(values)

def join_avg(values, energies, shifts):
	return sum(values)/len(values)
	
def join_cover(values, energies, shifts):
	points = set()
	for x,y,z in shifts:
		p = round(x,3),round(y,3)
		points.add(p)
	return sum(values)/len(points)


def func_concat(values, sortkeys, separator):
	if len(values) == 1:
		return values[0]
	values_sorted = [str(v) for v,s in sorted(zip(values,sortkeys), key=lambda v_s:v_s[1] )]
	return "[" + separator.join(values_sorted) + "]"

def join_xyz_shifted(values, energies, shifts):
	return sum([shift_xyz_data(v,s) for v, s in zip(values, shifts)], [])


SPMI_db = {
	'name':	StatePropMetaInfo('name',
		merge_func = lambda values, energies, beta : func_concat(values, energies, "+"),
		join_func = lambda values, energies, shifts : func_concat(values,[tuple(s) for s in shifts], ":")
	),
	
	'xyz_mark':	StatePropMetaInfo('xyz_mark',
		merge_func = merge_most_stable,
		join_func = join_xyz_shifted
	),
	
	'ads_energy':	StatePropMetaInfo('ads_energy',
		merge_func = merge_weighted_avg,
		join_func = join_sum,
		cmp_mode = '==',
		cmp_func = lambda x,y : abs(x-y)/(abs(x) + abs(y)) < 1E-6
	),
	
	'coverage':	StatePropMetaInfo('coverage',
		merge_func = merge_weighted_avg,
		join_func = join_cover,
		cmp_mode = '==',
		cmp_func = lambda x,y : abs(x-y)/(abs(x) + abs(y)) < 1E-6
	),

	'idx':	StatePropMetaInfo('idx',
		merge_func = lambda values, energies, beta : func_concat(values, energies, "+"),
		join_func = lambda values, energies, shifts : func_concat(values,[tuple(s) for s in shifts], ":")
	)
}

def register_properties(*names):
	'''
		Register several state properties
		
		Parameters:
			:names: list of property names
	'''
	for n in names:
		register_property(n)

def register_property(name, cmp_func="==", merge_func=None, join_func=None):
	'''
		Register new state property
		
		Parameters:
			:name: name of the property
	'''
	assert name not in SPMI_db, name

	if cmp_func in ['==', 'indiff']:
		cmp_mode = cmp_func
		cmp_func = None
	elif cmp_func is not None:
		cmp_mode = 'cmp_func'
	else:
		assert False, cmp_func
	
	if merge_func is None:
		merge_func = merge_weighted_avg
	elif merge_func == 'no-merge':
		merge_func = None
	
	if join_func is None:
		join_func = join_sum

	spmi = StatePropMetaInfo(name, merge_func, join_func, cmp_mode, cmp_func)
	SPMI_db[name] = spmi

class SiteStateType:
	"""
		Descriptor of a lattice site state.
	"""
	def __init__(self, name, configuration=None, ads_energy=None, xyz_mark=None, **kwargs):
		"""
			Parameters:
				:name: name of the state
				:configuration: geometry of the state. `Internal coordinates <https://en.wikipedia.org/wiki/Z-matrix_(chemistry)>` of lattice sites spanned by the state. See functions ``make_dimer_zmatrix()``, make_trimer_zmatrix()`` etc
				:ads_energy: energy of the state, can be consdidered as chemical potential of the surface or adsorption energy.
				:xyz_mark: list of chemical element symbols, one element for each site of the ``configuration``. Used for visualization purposes only. For example for trajectory generation by ``mc.run()`` function.
				:**kwargs: other properties of the state. All states of the model must have the same set of properties. New properties must be registered with function ``register_property()``. Property ``coverage``is registered by default.
				
		"""
		
		self.props = dict()
		if configuration is not None and isinstance(configuration[0], ZItem):
			self.zmatrix = configuration

		self.xyz_mark = xyz_mark
		
		self.props['name'] = StateProp('name', name)
		#self.props['xyz_mark'] = None # will be filled in LatticeConfig
		self.props['ads_energy'] = StateProp('ads_energy', ads_energy)
		
		for pname in kwargs:
			self.props[pname] = StateProp(pname, kwargs[pname])
	
	@property
	def name(self):
		return self.props['name'].value

	@property
	def ads_energy(self):
		return self.props['ads_energy'].value
	
	@ads_energy.setter
	def ads_energy(self, value):
		self.props['ads_energy'].value = value

	def __repr__(self):
		return "SST {}".format(self.props['name'])

