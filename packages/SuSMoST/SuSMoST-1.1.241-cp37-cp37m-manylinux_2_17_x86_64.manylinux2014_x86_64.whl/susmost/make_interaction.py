import numpy as np

def nearest_int(cc1, cc2,int_en = 0.0, int_r = 0.5, h = 0.5, INF_E = 1e6, dop_int=0.0, empty_name = "Empty"):
	"""
	Calculates the energy of interaction between nearest neighbors. If name of the molecule is 'Empty', then there is no any interactions with it.

	Parameters:
		:cc1,cc2:	Coordinates of first and second molecules.
		:int_en:		Simple interaction energy between elements of the molecule. Default is 0.0.
		:int_r:		The radius of the interaction. If the distance R between the molecules is h <= R <= int_r, then there is interaction. Default is 0.5.
		:h:			Radius of a solid sphere. If the distance between the elements of the molecules is smaller or equal, then an infinitely strong repulsion arises. Default is 0.5.
		:INF_E:		The value of an infinitely strong repulsion. Default is 1e6.
		:dop_int:	Complex interaction energy between elements of the molecule. Has the form dop_int = {('mol_1_name','mol_2_name'):energy1,...} Default is 0.0.
		:empty_name: Name of the element with properties of empty element. Default is "Empty".
	Returns:
		Energy of interaction between molecules.
	"""
	if cc1.lctype == empty_name or cc2.lctype == empty_name:
		return None

	interactions = 0.0
	for c1 in cc1.coords:					# coordinates of each atom in cc1
		for c2 in cc2.coords:				# coordinates of each atom in cc2
			r = np.linalg.norm(c1 - c2)		# distance

			if r < h*1.9999:
				interactions += INF_E				# forbidden_distance

			if (h*1.9999 < r < int_r*2.0001):
				if not type(dop_int) is dict:
					interactions += int_en			#interaction_energy
				else:
					molecules = sorted([cc1.lctype, cc2.lctype])
					interactions += dop_int.get((molecules[0],molecules[1]),0.0)
	return interactions
