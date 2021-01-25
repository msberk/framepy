#!/usr/bin/python3
import argparse
import subprocess
import os
import shutil
from glob import glob


def main(args):
    # Define folder locations.
    localFolder = os.path.join(args.baseDir, os.path.split(args.pictureDir)[1])
    targetFolder = os.path.join(args.baseDir, args.outDir)
    if not os.path.isdir(targetFolder):
        os.mkdir(targetFolder)

    # Define screen size into tuple.
    size = (args.hori, args.vert)

    # Sync with remote.
    remoteFileList = parseDUlist(args.pictureDir)
    removeMissingFiles(remoteFileList, localFolder)
    downloadFiles(args.pictureDir, args.baseDir)

    # Process images.
    processAllImages(localFolder, targetFolder, size)
    removeMissingFiles(os.listdir(localFolder), targetFolder, renameFile)

    # Show images.
    displayImages(targetFolder)


# Parse arguments.
def parseCliArgs():
    parser = argparse.ArgumentParser(description="Download and "
                                                 "process frame images.")
    parser.add_argument('pictureDir', type=str,
                        help="Location on dropbox of the photo directory")
    parser.add_argument('--baseDir', '-b', type=str,
                        default=os.environ["HOME"],
                        help="Base directory to work out of.")
    parser.add_argument('--outDir', '-o', type=str,
                        default='ProcessedPhotos',
                        help="Out photo directory for processed photos.")
    parser.add_argument('--vert', '-v', type=int, default=1080,
                        help='Vertical height of display screen.')
    parser.add_argument('--hori', '-z', type=int, default=1920,
                        help='Horizontal width of display screen.')
    return parser.parse_args()


def displayImages(targetFolder):
    fbiCall = ['fbi', '--noverbose', '--random', '--autozoom',
               '--timeout', '10']
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


def downloadFiles(pictureFolder, baseFolder):
    subprocess.run(['dropbox_uploader.sh', '-s',
                    'download', pictureFolder, baseFolder])


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


def parseDUlist(pictureFolder):
    result = subprocess.run(['dropbox_uploader.sh', 'list', pictureFolder],
                            capture_output=True, encoding='utf8')
    lineList = result.stdout.split('\n')
    return [' '.join(line.split(' ')[3:]).strip() for line in lineList
            if line.find('[F]') == 1]


if __name__ == "__main__":
    args = parseCliArgs()
    main(args)
