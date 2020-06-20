""" A simple script to translate .bp files to .npy (python uncompressed) files.
!_list=!ls *.bp
for file in _list:
   a=unpack_ndarray_file(file)
   print(file,a.shape)
   stem=file[:-3]
   np.save(stem,a)
   all=stem+'.*'
   !ls -l $all
