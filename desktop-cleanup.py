import platform, os, heapq


def get_largest_files(startdir):
    """Finds the 10 largest files from the dirctory tree of
        the given directroy"""
    largest = []
    for (dirpath, dirnames, filenames) in os.walk(startdir):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)):
                if len(largest) < 10:
                    size = os.path.getsize(os.path.join(dirpath, f))
                    heapq.heappush(largest, [size, f, dirpath])
                    continue

                size = os.path.getsize(os.path.join(dirpath, f))
                if size > largest[0][0]:
                    heapq.heappushpop(largest, [size, f, dirpath])

    if len(largest) == 0:
        print ("Empty Directory")
        return
    largest.sort(reverse = True)
    for s in largest:
        s[0] = round(s[0] / 1024 ** 2, 2)	# Convert size to MB

    # Pretty Print the files
    spaces = []
    for i in range(3):
        spaces.append(max( len(str(s[i])) for s in largest ))
    if spaces[1] < 8:       # Spaces for heading 'Filename'
        spaces[1] = 8
    if spaces[2] < 16:		# Spaces for heading 'Parent Directory'
        spaces[2] = 16
    print ('The largest files are:')
    print('-' * spaces[1] + '    ' + '-' * (spaces[0] + 3) + '    ' + '-' * spaces[2])
    print('Filename'.ljust(spaces[1]) + '    ' + 'Size'.ljust(spaces[0] + 3) + '    ' + 'Parent Directory')
    print('-' * spaces[1] + '    ' + '-' * (spaces[0] + 3) + '    ' + '-' * spaces[2])
    for s in largest:
        print(s[1].ljust(spaces[1]) + '    ' + (str(s[0]) + ' MB').ljust(spaces[0] + 3) + '    ' + s[2])


def clean_desktop():
    """Sorts all the files on Desktop into folders in Documents
        folder based on their extensions, ignoring shortcuts"""
    print ('\nCleaning the Desktop and sorting the files into folders in Documents folder...')
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')			# Path to Desktop
    for file in os.listdir(desktop_path):
        filename, extension = os.path.splitext(file)
        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')			# Path to documents folder
        ext = extension[1:]
        if ext != 'lnk' or os.path.islink(os.path.join(desktop_path, file)):	# Ignoring links and shortcuts
            folderpath = os.path.join(documents_path, ext)
            if not os.path.isdir(folderpath):
                os.mkdir(folderpath)
            os.rename(os.path.join(desktop_path, file), os.path.join(folderpath, file))
    print ('Done')


if platform.system() == 'Linux':
    print ('Scanning the system for largest files...')
    get_largest_files('/home/')

elif platform.system() == 'Windows':
    print ('Scanning C drive for largest files...')
    get_largest_files('C:\\')

    if os.path.exists('D:\\'):
    	print ('\nScanning D drive for largest files...')
    	get_largest_files('D:\\')

    if os.path.exists('E:\\'):
        print ('\nScanning E drive for largest files...')
        get_largest_files('E:\\')


print ('\nScanning Downloads folder for largest files...')
get_largest_files(os.path.join(os.path.expanduser('~'), 'Downloads'))


clean_desktop()
