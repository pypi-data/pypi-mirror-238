#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import glob
from sys import argv
import pathlib
isST=True
from setuptools import setup, Extension, find_packages
from os import listdir
from os.path import isfile, join
import platform
systemName=platform.system()
import sys
is_64bits = sys.maxsize > 2**32

from setuptools.command.build_ext import build_ext as build_ext_orig


version='0.48'
libName="mazalib"

file_dir_path = os.path.dirname(os.path.realpath(__file__))

def package_files(directory):
    return [os.path.join(p,f) for p,d,files in os.walk(directory) for f in files]

with open("README.md", "r") as fh:
	long_description = fh.read()
short_description = "Cross-platform 2d/3d image segmentation C++ library"

language="c++"
extra_compile_args=['-O3', '-w', '-std=c++11']
# extra_link_args=['-std=c++11','_GLIBCXX_USE_CXX11_ABI=0']
# extraFlags=['-fpermissive','-std=c++11']
installRequiresList=['numpy']
entry_points_Command={'main_library': ['kriging = mazalib:kriging',
                                       'mrf = mazalib:mrf',
                                       'rgs = mazalib:rgs',
                                       'hessian = mazalib:hessian',
                                       'windowedHessian = mazalib:windowedHessian',
                                       'nlm = mazalib:nlm',
                                       'unsharp = mazalib:unsharp',
									   'cac = mazalib:cac']}
license='GPLv3'
author='Mathieu Gravey, Roman V. Vasilyev, Timofey Sizonenko, Kirill M. Gerke, Marina V. Karsanina, Andrey A. Ananev'
author_email='mathieu.gravey@unil.ch'

classifiers=[
			'Development Status :: 3 - Alpha',
			'Intended Audience :: Science/Research',
			'Intended Audience :: Education',
			'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
			'Programming Language :: C++',
			'Programming Language :: Python :: 3 :: Only'
			# 'Operating System :: OS Independent',
		]

packages=find_packages('src',include=['mazalib*']) + ['segmentation', 'eigen3']

eigen_path=os.path.join(file_dir_path,"src","eigen3","")
eigen_package_files=package_files(eigen_path)

if(systemName=='Linux' or systemName=='Windows' or systemName=='Darawin'):

	os.environ["CXX"]='g++'
	os.environ["CC"]='gcc'

	import numpy as np

	mazalib_module = Extension(libName, 
							sources=['./src/mazalib/mazalib.cpp'] + package_files('./src/segmentation/src/'),
							language=language, 
							extra_compile_args=extra_compile_args,
							include_dirs=["./src/segmentation/include/", "./src/eigen3/", np.get_include()])
	setup(
		name=libName,
		version=version,
		description=short_description,
		long_description=long_description,
		author=author,
		author_email=author_email,
		license=license,
		packages=packages,
    	package_dir={'': 'src'},
    	package_data={'segmentation': ['./src/*.cpp', './include/*.h'],
					  'eigen3': eigen_package_files},
		classifiers=classifiers,
		# ext_package = libName,
		ext_modules=[mazalib_module],
		setup_requires=installRequiresList,
		install_requires=installRequiresList,
		entry_points=entry_points_Command
	)

if(systemName=='Darwin'):
	pass

# if(systemName=='Windows'):
# 	import numpy
# 	if is_64bits:
# 		setup(name=libName,
# 			version=version,
# 			description=short_description,
# 			long_description=long_description,
# 			author='Mathieu Gravey, Roman V. Vasilyev, Timofey Sizonenko, Kirill M. Gerke, Marina V. Karsanina',
# 			author_email='mathieu.gravey@unil.ch',
# 			license='GPLv3',
# 			packages=[libName],
# 			classifiers=[
# 				'Development Status :: 3 - Alpha',
# 				'Intended Audience :: Science/Research',
# 				'Intended Audience :: Education',
# 				#'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
# 				'Programming Language :: C++',
# 				'Programming Language :: Python :: 3 :: Only'
# 			],
# 			ext_package = libName,
# 			ext_modules=[Extension(libName, sources=['./pythonInterface.cpp']+glob.glob('../non_local_means/src/*.cpp')+glob.glob('../lib/*.cpp'),
# 			language="c++", 
# 			extra_compile_args=["-std=c++14",'-O3']+extraFlags,
# 			extra_link_args=["-std=c++14"]+extraFlags,
# 			include_dirs=['../lib','../non_local_means/include','../eigen3'],
# 			libraries = [],
# 			library_dirs = []
# 			)],
# 			include_dirs=numpy.get_include(),
# 			install_requires=installRequiresList,
# 			entry_points=entry_points_Command
# 			#data_files=[('lib\\site-packages\\g2s',["./libzmq-v141-x64-4_3_2/libzmq-v141-mt-4_3_2.dll","./libzmq-v141-x64-4_3_2/libsodium.dll"])]
# 		)
# 	else:
# 		setup(name=libName,
# 			version=version,
# 			description='TBA',
# 			long_description=long_description,
# 			**{'long_description_content_type':'text/markdown'} if isST else {},
# 			author='Mathieu Gravey, Roman V. Vasilyev, Timofey Sizonenko, Kirill M. Gerke, Marina V. Karsanina',
# 			author_email='mathieu.gravey@unil.ch',
# 			url='TBA',
# 			license='TBA',
# 			packages=[libName],
# 			classifiers=[
# 				'Development Status :: 3 - Alpha',
# 				'Intended Audience :: Science/Research',
# 				'Intended Audience :: Education',
# 				#'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
# 				'Programming Language :: C++',
# 				'Programming Language :: Python :: 3 :: Only'
# 			],
# 			ext_package = libName,
# 			ext_modules=[Extension(libName, sources=['./pythonInterface.cpp']+glob.glob('../non_local_means/src/*.cpp')+glob.glob('../lib/*.cpp'),
# 			language="c++", 
# 			extra_compile_args=["-std=c++14",'-O3']+extraFlags,
# 			extra_link_args=["-std=c++14"]+extraFlags,
# 			include_dirs=['../lib','../non_local_means/include','../eigen3'],
# 			libraries = [],
# 			library_dirs = []
# 			)],
# 			include_dirs=numpy.get_include(),
# 			install_requires=installRequiresList,
# 			entry_points=entry_points_Command
# 			#data_files=[('lib\\site-packages\\g2s',["./libzmq-v141-4_3_2/libzmq-v141-mt-4_3_2.dll","./libzmq-v141-4_3_2/libsodium.dll"])]
# 		)