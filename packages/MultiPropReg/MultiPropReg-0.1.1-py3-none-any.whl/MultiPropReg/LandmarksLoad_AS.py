'''
This funciton reads a '.ldm' file. '.ldm' is a file type defined by AnatomySketch to store
Landmarks data.
Input: filename of '.ldm' file.
Output: A list and each element is [LdmName, LdmID, LdmColor, LdmPosition]
    LdmName: string, name of Landmarks.
    LdmID: int, ID of Landmarks.
    LdmColor: int[3], RGB color of Landmarks.
    LdmPosition: float[3]. xyz position of Landmarks.
'''
def LoadLandmarks(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    Output = list()
    ncrntLine = 0
    # 0 Check file header 
    if data[ncrntLine] != '#Anatomy Sketch Landmark File\n':
        return -1
    ncrntLine += 1
    # 1 Number of reference points
    if data[ncrntLine] != '#NUMBER OF DATA:\n':
        return -1
    ncrntLine += 1
    NumOfLandMData = int(data[ncrntLine])
    ncrntLine += 1
    # 2 DATALIST
    if data[ncrntLine] != '#DATA LIST DEFINITION:\n':
        return -1
    ncrntLine += 1
    for ncrntLandMData in range(NumOfLandMData):
        # // 2.1 DATA LIST NUMBER
        if data[ncrntLine] != '#DATA LIST NUMBER ' + str(ncrntLandMData) + ' DEFINITION:\n':
            return -1
        ncrntLine += 1
        # 2.2 data_list_index
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'data_list_index\n':
            return -1
        if int(sublist[0]) != ncrntLandMData:
            return -1
        # 2.3 data_name
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'data_name\n':
            return -1
        # 2.4 number_of_landmarks
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'number_of_landmarks\n':
            return -1
        NumOfLandM = int(sublist[0])
        for ncrntLandM in range(NumOfLandM):
            if data[ncrntLine] != '#LANDMARK LIST NUMBER ' + str(ncrntLandM) + ' DEFINITION:\n':
                return -1
            ncrntLine += 1
            # 2.4.1 landmark_index
            sublist = data[ncrntLine].split(' # ')
            ncrntLine += 1
            if sublist[1] != 'landmark_index\n':
                return -1
            if int(sublist[0]) != ncrntLandM:
                return -1
            # 2.4.2 landmark_name
            sublist = data[ncrntLine].split(' # ')
            ncrntLine += 1
            if sublist[1] != 'landmark_name\n':
                return -1
            LdmName = sublist[0]
            # 2.4.4 landmark_ID
            sublist = data[ncrntLine].split(' # ')
            ncrntLine += 1
            if sublist[1] != 'landmark_ID\n':
                return -1
            LdmID = int(sublist[0])
            # 2.4.5 Color
            sublist = data[ncrntLine].split(' # ')
            ncrntLine += 1
            if sublist[1] != 'r_color g_color b_color\n':
                return -1
            subsublist = sublist[0].split(' ')
            LdmColor = [int(subsublist[0]), int(subsublist[1]), int(subsublist[2])]
            # 2.5.6 Position
            if data[ncrntLine] != '#POINT_POS\n':
                return -1
            ncrntLine += 1
            sublist = data[ncrntLine].split(' ')
            ncrntLine += 1
            if len(sublist) != 3:
                return -1
            LdmPosition = [float(sublist[0]), float(sublist[1]), float(sublist[2])]
            if data[ncrntLine] != '#END_POINT_POS\n':
                return -1
            ncrntLine += 1
            crntLandM = [LdmName, LdmID, LdmColor, LdmPosition]
            Output.append(crntLandM)
    return Output