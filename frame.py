#!/usr/bin/python3
import argparse
import subprocess
import os
import shutil
from glob import glob


def main(args):
    # Define folder locations.
    if not os.path.isdir(args.baseDir):
        os.mkdir(args.baseDir)

    localFolder = os.path.join(args.baseDir, os.path.split(args.pictureDir)[1])
    targetFolder = os.path.join(args.baseDir, args.outDir)
    if not os.path.isdir(targetFolder):
        os.mkdir(targetFolder)

    # Define screen size into tuple.
    size = (args.hori, args.vert)

    # Sync with remote.
    remoteFileList = parseDUlist(args.pictureDir, args.configFile)
    downloadFiles(args.pictureDir, args.baseDir, args.configFile)
    removeMissingFiles(remoteFileList, localFolder)

    # Process images.
    processAllImages(localFolder, targetFolder, size)
    removeMissingFiles(os.listdir(localFolder), targetFolder, renameFile)

    # Show images.
    displayImages(targetFolder, args.timeout, args.randomize)


# Parse arguments.
def parseCliArgs():
    parser = argparse.ArgumentParser(description="Download and "
                                                 "process frame images.")
    parser.add_argument('pictureDir', type=str,
                        help="Location on dropbox of the photo directory")
    parser.add_argument('--baseDir', '-b', type=str,
                        default=os.path.join(os.environ["HOME"],
                                             'framepy_working'),
                        help="Base directory to work out of")
    parser.add_argument('--outDir', '-o', type=str,
                        default='ProcessedPhotos',
                        help="Out photo directory for processed photos")
    parser.add_argument('--vert', '-v', type=int, default=1080,
                        help='Vertical height of display screen.')
    parser.add_argument('--hori', '-z', type=int, default=1920,
                        help='Horizontal width of display screen')
    parser.add_argument('--timeout', '-t', type=str, default='20',
                        help='Timeout before switching photos')
    parser.add_argument('--randomize', '-r', action='store_true',
                        help='Randomize image output')
    parser.add_argument('--configFile', '-f',
                        default=os.path.join(os.environ["HOME"],
                                             '.dropbox_uploader'),
                        help='Dropbox_uploader.sh config file.')
    return parser.parse_args()


def displayImages(targetFolder, timeout, randomize):
    fbiCall = ['fbi', '--noverbose', '--autozoom',
               '--timeout', timeout]
    if randomize:
        fbiCall.append('--random')

    fbiArgs = glob(os.path.join(targetFolder, '*.jpeg'))
    subprocess.run(fbiCall + fbiArgs)


def processAllImages(localFolder, targetFolder, size):
    localFileList = os.listdir(localFolder)

    for localName in localFileList:
        localFile = os.path.join(localFolder, localName)

        targetName = renameFile(localName)
        targetFile = os.path.join(targetFolder, targetName)

        if not os.path.isfile(targetFile) and '.jpeg' in targetName:
            shutil.copy(localFile, targetFile)
            processImage(targetFile, size)


def processImage(file, size):
    # Auto-rotate file.
    subprocess.run(['exiftran', '-ai', file])
    # Resize and reformat image.
    sizeStr = str(size[0]) + 'x' + str(size[1])
    subprocess.run(['mogrify', '-verbose', '-format', 'jpeg',
                    '-resize', sizeStr, file])


def renameFile(originalName):
    return originalName.replace(' ', '_')\
                       .replace('.jpg', '.jpeg')\
                       .replace('.JPG', '.jpeg')\
                       .replace('.JPEG', '.jpeg')


def downloadFiles(pictureFolder, baseFolder, duConfigPath):
    subprocess.run(['dropbox_uploader.sh', '-f', duConfigPath, 
                    '-s', 'download', pictureFolder, baseFolder])


def removeMissingFiles(srcFileList, destDir, renameFcn=None):
    if os.path.isdir(destDir):
        destFileList = os.listdir(destDir)

        # Rename the source file list to match the target if a
        # renaming function was used, to ensure matching.
        if renameFcn is not None:
            srcFileList = [renameFcn(file) for file in srcFileList]

        missingFiles = [destFile for destFile in destFileList
                        if destFile not in srcFileList]

        for missingFile in missingFiles:
            print('Removing ' + missingFile)
            os.remove(os.path.join(destDir, missingFile))


def parseDUlist(pictureFolder, duConfigPath):
    result = subprocess.run(['dropbox_uploader.sh', '-f', duConfigPath,
                             'list', pictureFolder],
                            capture_output=True, encoding='utf8')
    lineList = result.stdout.split('\n')
    return [' '.join(line.split(' ')[3:]).strip() for line in lineList
            if line.find('[F]') == 1]


if __name__ == "__main__":
    args = parseCliArgs()
    main(args)
