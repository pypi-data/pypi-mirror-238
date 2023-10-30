from .sitestate import SPMI_db, register_property, StateProp


class LatticeTask():
	"""Class for description of a lattice model


	"""
	def __init__(self, site_state_types, unit_cell, states, edges_dict, IM, INF_E, precission, max_dimensions):
		"""
		Constructor of LatticeTask
			
		Parameters:
			:site_state_types: list of types of possible states of lattice sites as :class:`SiteStateType` objects. Usually correspond to considered adsorption complexes, including an empty site.
			
			:unit_cell: unit cell of the lattice as :class:`Cell` object
		
			:states: list of possible states of lattice sites as :class:`CellState` objects. Usually correspond to various orientations of adsorption complexes from ``site_state_types`` 
			
		"""
		self.site_state_types = site_state_types
		self.unit_cell = unit_cell
		self.states = states
		self.edges_dict = edges_dict
		self.IM = IM
		self.INF_E = INF_E
		self.precission = precission
		self.max_dimensions = max_dimensions
	
	def __repr__(self):
		return "{} {} {} {} {}".format(self.site_state_types, self.states, self.unit_cell, len(self.edges_dict), self.IM.shape)
		
	def get_site_state_type(self, name):
		for s in self.site_state_types:
			if s.props['name'].value == name:
				return s
		assert False, "Unknown site state type name: {}".format(name)

	def find_state_index(self, prop_name, prop_value):
		return [i for i,s in enumerate(self.states) if s.get_prop(prop_name) == prop_value][0]

	def set_property(self, property_name, values, default_value=0):
		'''
		Sets a property for all adsoprtion complexes
		
		Parameters:
			:property_name: name of the property
			:values: dictionary with AC names as keys and new property values as values
			:default_value: value to be set for ACs not included in :values:, default value - :0:.
		
		Returns:
			None
		'''
		
		for k in values:
			self.get_site_state_type(k) # assert for correct AC names
		
		if property_name not in SPMI_db:
			register_property(property_name)
			print ("Register new AC property", property_name)
		
		for s in self.site_state_types:
			ac_name = s.props['name'].value
			s.props[property_name] = StateProp(property_name, values.get(ac_name, default_value))

	def get_property(self, property_name, ac_name=None):
		'''
		Returns current value of the property of the specified adsorption complex
		
		Parameters:
			:property_name: name of property
			:ac_name: name of adsorption complex
		Returns:
			Current value of the property of the specified adsorption complex
		'''
		if ac_name is None:
			return {(s.props['name'].value, s.props[property_name].value) for s in self.site_state_types}
			
		return self.get_site_state_type(ac_name).props[property_name].value

	
	def set_ads_energy(self, ac_name, energy):
		'''
		Sets adsorption energy for adsorption complex by it's name
		
		Parameters:
			:ac_name: name of adsorption complex
			:energy: new adsorption energy of the adsorption complex
		
		Returns:
			None
		'''
		self.get_site_state_type(ac_name).props['ads_energy'].value = energy

	def get_ads_energy(self, ac_name):
		'''
		Returns current energy of adsorption of the specified adsorption complex
		
		Parameters:
			:ac_name: name of adsorption complex
		
		Returns:
			Сurrent energy of adsorption of the specified adsorption complex
		'''
		return self.get_site_state_type(ac_name).props['ads_energy'].value

	@property
	def zero_coverage_state_index(self):
		"""Get index of the state with zero coverage, that is empty state"""
		return self.find_state_index('coverage', 0)

	@property
	def states_count(self):
		"""Get number of possible cell states"""
		return len(self.states)
		
	@property
	def edges_count(self):
		"""Get number of different edges in the lattice, that are considered in the model"""
		return len(self.edges_dict)
	
	@property
	def edges_array(self):
		"""Get edges considered in the model as a two-dimensional array of size *(edges_count, 3)* """
		return np.array([e.coords for e in self.edges_dict])

	@property
	def interactions_array(self):
		"""
		Get paiwise interactions of the model as a three-dimensional array of size *(states_count, edges_count, states_count)*. 
		
		Returns:
			:result [i,j,k]: interaction energy between states i-th and k-th separated by j-th edge
		"""
		return self.IM.asarray()


	def __str__(self):
		return "LT: {} states, {} edges, state types: {}".format(self.states_count, self.edges_count, [str(s) for s in self.site_state_types])
	
	
