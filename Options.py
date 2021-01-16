class Options:
    record = False
    recordFName = "Data.txt"

    play = False
    playFName = "Data.txt"


    def ParseCMD(self, argv):
        for i in range(len(argv)):
            if (argv[i] == "--record"):
                self.record = True

                if (i + 1 < len(argv) and argv[i + 1][0] != '-'):
                    self.recordFName = argv[i + 1]
            
            elif (argv[i] == "--play"):
                self.play = True

                if (i + 1 < len(argv) and argv[i + 1][0] != '-'):
                    self.playFName = argv[i + 1]