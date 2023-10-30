#!python -u

import sys
import argparse

def argv2str():
	return ' '.join([ (f'"{a}"' if ' ' in a else a)  for a in sys.argv])

def model_report():
	parser = argparse.ArgumentParser(description="Make HTML report for lattice model", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('--samples-dir','-d', dest='samples_dir', nargs='?', default='tmp',
						help='Directory with AC samples and "energies" file')
						
	args = parser.parse_args()
	
	samples_dir = args.samples_dir
	
	empty_cell_sample, ac_samples, lateral_samples = load_energies(samples_dir)
	
	
	html_table = ""
	
	for a in lateral_samples:
			e = a.lateral_energy
			print("Energy=", e, a.filename, a.info.get('mass_center_dist',None), a.info.get('size',None))
			png_fn = a.filename + ".png"
			ase.io.write(samples_dir + "/" + png_fn, [a])
			html_table += '<tr><td><img src="{}"</td><td>{}</td></tr>'.format(png_fn, e)

	with open(samples_dir + "/energies.html", 'w') as html_file:
		html_file.write("<html><body><table>{}</table></body></html>".format(html_table))


