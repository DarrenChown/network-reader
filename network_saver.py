import pypsa
import os
from pathlib import Path
network = pypsa.Network()

# Gets File Path for Excel Files
def get_path(dataDict, parentFolder, childFolder, dataFile):
    folder = parentFolder / dataDict[childFolder]["Folder"]
    file_name = f"{dataDict[childFolder][dataFile]}"
    return folder / file_name

# Function to generate the next file name
def get_next_filename(folder, base_name, extension):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    contains = os.listdir(folder)
    existing_numbers = []
    for filename in contains:
        if filename.startswith(base_name) and filename.endswith(f'.{extension}'):
            try:
                number = int(filename[len(base_name):-len(f'.{extension}')])
                existing_numbers.append(number)
            except ValueError:
                pass
    next_number = max(existing_numbers, default=0) + 1
    return f"{base_name}{next_number}.{extension}"

def export_files(loadedNetwork, dataTree, folderName, dataType, fileType):
    if(fileType == 'csv'):
        newFile = get_next_filename(folderName / dataTree[dataType]['Folder'], dataTree[dataType]['File'], fileType)
        loadedNetwork.export_to_csv_folder(folderName / dataTree[dataType]['Folder'] / newFile)
        fullPath = folderName / newFile
        print(f"Result saved to: {fullPath}")
    elif(fileType == 'h5'):
        newNet = get_next_filename(str(folderName), dataType, fileType)
        fullPath = folderName / newNet
        loadedNetwork.export_to_hdf5(fullPath)
        print(f"Network saved to: {fullPath}")
    else:
        print("Invalid File Type")