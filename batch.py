#!python
import argparse
import subprocess
import os
import shutil


def main(args):
    # Define folder locations.
    localFolder = os.path.join(args.baseFolder, args.pictureFolder)
    targetFolder = os.path.join(args.baseFolder, args.outFolder)

    # Define screen size into tuple.
    size = (args.hori, args.vert)

    # Sync with remote.
    remoteFileList = parseDUlist(args.pictureFolder)
    removeMissingFiles(remoteFileList, localFolder)
    downloadFiles(args.pictureFolder, args.baseFolder)

    # Process images.
    processAllImages(localFolder, targetFolder, size)

    # Show images.
    displayImages(targetFolder)


# Parse arguments.
def parseCliArgs():
    parser = argparse.ArgumentParser(description="Download and "
                                                 "process frame images.")
    parser.add_argument('pictureFolder', type=str,
                        help="Location on dropbox of the photo folder")
    parser.add_argument('--baseFolder', '-b', type=str,
                        default=os.environ["HOME"],
                        help="Base folder to work out of.")
    parser.add_argument('--outFolder', '-o', type=str,
                        default='ProcessedPhotos',
                        help="Out photo directory for processed photos.")
    parser.add_argument('--vert', '-v', type=int, default=1080,
                        help='Vertical height of display screen.')
    parser.add_argument('--hori', '-h', type=int, default=1920,
                        help='Horizontal width of display screen.')
    return parser.parse_args()


def displayImages(targetFolder):
    subprocess.run(['fbi', '--noverbose', '--random', '--autozoom',
                    '--timeout', '10', targetFolder + '*.jpeg'], shell=True)


def processAllImages(localFolder, targetFolder, size):
    localFileList = os.listdir(localFolder)

    for localName in localFileList:
        localFile = os.path.join(localFolder, localName)

        targetName = renameFile(localFile)
        targetFile = os.path.join(targetFolder, targetName)

        if not os.path.isfile(targetFile):
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
    return originalName.replace(' ', '_')


def downloadFiles(pictureFolder, baseFolder):
    subprocess.run(['dropbox_uploader.sh', '-s',
                    'download', pictureFolder, baseFolder])


def removeMissingFiles(remoteFileList, localFolder):
    localFileList = os.listdir(localFolder)
    missingFiles = (localFile for localFile in localFileList
                    if localFile in remoteFileList)
    for missingFile in missingFiles:
        print('Removing ' + missingFile)
        os.remove(os.path.join(localFolder, missingFile))


def parseDUlist(pictureFolder):
    result = subprocess.run(['dropbox_uploader.sh', 'list', pictureFolder],
                            capture_output=True)
    lineList = result.stdout.split('\n')
    return (line.split(' ')[2] for line in lineList if line.find('[F]'))


if __name__ == "__main__":
    args = parseCliArgs()
    main(args)
