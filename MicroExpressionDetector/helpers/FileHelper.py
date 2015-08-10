class FileHelper( object ):
    """description of class"""

    def __init__( 



    def readIn( asm, files ):
        m = 0
        for f in files:
            if m > 499:
                 return        
            with open( os.path.join(folder,f), "r" ) as infile:
                ptList = [ ]
                allLines = infile.readlines()
                pointLine = False
                cleanLines = [ x.strip() for x in allLines]
                for line in cleanLines:
                    if line is '{':
                        pointLine = True
                
                    elif line is '}':
                        pointLine = False
                        pass
                    elif pointLine:
                        ptList.append( map( float, line.split(' ') ) )
                    else:
                        pass

            asm.addShape( Shape( ptList ) )
            m += 1
            print m


