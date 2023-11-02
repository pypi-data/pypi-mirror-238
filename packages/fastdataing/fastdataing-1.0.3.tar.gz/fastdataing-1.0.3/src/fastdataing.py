"""
Common fast data processing methods
"""
import os
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ezdxf
from tqdm import tqdm


def __version__():
	version = "1.0.3"
	return version

def smooth_MIS(x,y,factor=300):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factor: smooth factor, like, factor=300
	"""
	x_smooth = np.linspace(x.min(), x.max(), factor)
	y_smooth = make_interp_spline(x, y)(x_smooth)

	print("\n>>> smooth_MIS successfully !\n")
	return x_smooth,y_smooth


def smooth_SF(x,y,factors=[5,3]):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factors: smooth factors, like, factors=[5,3]
	"""
	y_smooth = savgol_filter(y, factors[0], factors[1], mode= 'nearest')
	x_smooth = x
	print("\n>>> smooth_SF successfully !\n")
	return x_smooth,y_smooth


def cal_solpes(x,y):
	"""
	calculating slope
	x: x axis data
	y: y axis data
	"""
	slopes = []

	for i in range(1, len(x)):
	    delta_x = x[i] - x[i - 1]
	    delta_y = y[i] - y[i - 1]
	    slope = abs(delta_y / delta_x)
	    slopes.append(slope)

	x_values = x[1:]
	return 	x_values,slopes


def average_xy(x,y,window_size=10):
	"""
	average data
	x: x axis data
	y: y axis data
	window_size: window size
	"""
	avg_x = []
	avg_y = []
	for i in range(0, len(x), window_size):
	    avg_x.append(sum(x[i:i + window_size]) / window_size)
	    avg_y.append(sum(y[i:i + window_size]) / window_size)
	return avg_x, avg_y


def get_files(directory, suffix):
	"""
	Read files with the same suffix in the folder and save them as a list
	directory: a directory for reading
	suffix: a suffix
	"""
	files = []
	for filename in os.listdir(directory):
		if filename.endswith(suffix):
			files.append(filename)
	print("\n>>> get files successfully !\n")
	return files

def add_fig(figsize=(10,8),size=22):
	"""
	add a canvas, return ax
	figsize=(10,8),
	size=22
	"""
	plt.rc('font', family='Times New Roman', size=size)
	plt.rcParams['xtick.direction'] = 'in'
	plt.rcParams['ytick.direction'] = 'in'
	fig = plt.figure(figsize=figsize)
	print("\n>>> add a fig successfully !\n")
	return fig

def add_ax(fig,subplot=(1,1,1)):
	"""
	add a ax
	fig: a  figure
	subplot=(1,1,1)
	"""
	if isinstance(subplot, int):
		subplot = (subplot,)
		subplot = tuple(int(ch) for ch in str(subplot[0]))
	ax = fig.add_subplot(subplot[0],subplot[1],subplot[2])
	return ax


def plot_fig(ax,x,y,label=False,linewidth=1,
	factors=False,color="r-",savefig="temp.png",
	xlabel=False,ylabel=False,fontweight="normal",alpha=1.0,loc="best",ncols=1,
	dpi=300,transparent=True,fontsize=26):
	"""
	plot fig
	x,y: x,y
	label: label="label", default label=False
	linewidth: linewidth=1,
	factors: factors=[199,3],
	color: color="r",
	savefig: savefig="temp.png",
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	alpha=1.0,
	ncols = 1
	dpi: dpi=300,
	transparent: transparent=True)
	"""
	if factors==False:
		if label == False:
			ax.plot(x,y,color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color,label=label,linewidth=linewidth,alpha=alpha)
	else:
		x,y = smooth_SF(x,y,factors=factors)
		if label == False:
			ax.plot(x,y,color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color,label=label,linewidth=linewidth,alpha=alpha)
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	if savefig and savefig != "temp.png":
		plt.savefig(savefig,dpi=dpi,transparent=transparent)
	else:
		pass
	print("\n>>> plot a fig successfully !\n")
	return ax



def plot_scatter(ax,x,y,s=None,marker="o",color="r",linewidths=1.5,edgecolors='face',label=False,
	xlabel=False,ylabel=False,fontweight="normal",fontsize=26,alpha=1.0,loc="best",ncols=1):
	"""
	plot a scatter fig
	x,y: x,y
	s: markersize
	label: label="label", default label=False
	linewidth: linewidth=1,
	marker: marker="o"...
	color: color="r",
	edgecolors: 'face',
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	fontsize=26
	alpha=1.0,
	loc="best"
	ncols = 1
	"""
	if label == False:
		ax.scatter(x,y,s=s,marker="o",color=color,alpha=1,linewidths=1.5,edgecolors='face')
	else:
		ax.scatter(x,y,s=s,marker="o",color=color,label=label,alpha=1,linewidths=1.5,edgecolors='face')
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return

def plot_dotsline(ax,x,y,yerr=None, fmt='',markersize=12,markeredgecolor="r",
	elinewidth=1.5,capsize=5,barsabove=True, capthick=1,label=False,
	xlabel=False,ylabel=False,fontweight="normal",fontsize=26,alpha=1.0,loc="best",ncols=1):
	"""
	plot a scatter fig
	x,y: x,y
	yerr: None
	fmt: "ro--"
	markersize: markersize
	markeredgecolor: "r"
	elinewidth: elinewidth=1.5,
	capsize: capsize=5
	barsabove: True,
	capthick: 1,
	label: label="label", default label=False
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	fontsize=26
	alpha=1.0,
	loc="best"
	ncols = 1
	"""
	if label == False:
		s1 = ax.errorbar(x,y,yerr=yerr,capsize=capsize,capthick=capthick,alpha=.5,barsabove=barsabove,elinewidth=elinewidth,
				fmt=fmt,mec=markeredgecolor,markersize=markersize)
	else:
		s1 = ax.errorbar(x,y,yerr=yerr,capsize=capsize,capthick=capthick,alpha=.5,barsabove=barsabove,elinewidth=elinewidth,
				fmt=fmt,mec=markeredgecolor,markersize=markersize,label=label)
	
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return



class Figure(object):
	"""Figure class: picture processing"""
	def __init__(self,):
		super(Figure, self).__init__()

	def fig2ico(self,png_file,ico_file=False):
		"""
		convert png to ico file
		png_file: png file name
		ico_file: ico file name
		"""
		image = Image.open(png_file)
		if image.mode != "RGBA":
			image = image.convert("RGBA")
		sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
		if ico_file==False:
			ico_file = png_file.split(".")[0]+".ico"
		image.save(ico_file, format="ICO", sizes=sizes)
		print("\n>>> png2ico successfully !\n")

		return
		
	def fig2binary(self, fig_file, binary_file=False, threshold=128):
		"""
		convert fig to binary image
		fig_file: fig file name
		threshold: RGB threshold
		"""
		img = Image.open(fig_file)
		gray_image = img.convert("L")
		binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, "1")
		if binary_file==False:
			binary_file = "binary_"+fig_file
		binary_image.save(binary_file)
		print("\n>>> fig2binary successfully !\n")
		return binary_image

	def binary2dxf(self,binary_image_file,dxf_file=False):
		"""
		convert binary to dxf format
		binary_image_file: binary image file name
		dxf_file: dxf file name
		"""
		doc = ezdxf.new("R2010")
		msp = doc.modelspace()
		binary_image = Image.open(binary_image_file)
		width, height = binary_image.size
		for y in tqdm(range(height)):
			for x in range(width):
				pixel = binary_image.getpixel((x, y))
				if pixel == 0:
					msp.add_point((x, y))
		if dxf_file==False:
			dxf_file = "binary_"+binary_image_file
		doc.saveas(dxf_file)
		print("\n>>> binary2dxf successfully !\n")
		return



if __name__ == "__main__":
	print(__version__())

	# f = Figure()
	# f.fig2binary("toux.jpg","toux_1.jpg")
	# f.binary2dxf("toux_1.jpg","toux_1.dxf")
	# f.fig2ico("toux.jpg","toux.ico")