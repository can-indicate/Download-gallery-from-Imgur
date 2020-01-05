"""
My personal script to download galleries from Imgur.
To use, open a terminal in the directory that contains this file,
and enter the following:
 `python3 -m download_imgur <Imgur link>`
You may need to replace 'imgur' with 'i.imgur' in the link.
"""
import requests as req
import sys
__path__ = "./"


class ImgurLinks:
    """
    Collection of imgur links to images and videos.
    """

    def __init__(self) -> None:
        """
        Initializer.
        """
        self._ids = []
        self._filetypes = []
        self._files = []
        self._links = []

    def __len__(self) -> int:
        """
        Get the number of links.
        """
        return len(self._ids)

    def get_id(self, i: int) -> str:
        """
        get the id, given its index.
        """
        return self._ids[i]

    def get_link(self, i: int) -> str:
        """
        get the link, given its index.
        """
        return self._links[i]

    def append(self, imgur_id: str, filetype: str) -> None:
        """
        Add a new imgur link.
        """
        self._ids.append(imgur_id)
        self._filetypes.append(filetype)
        self._files.append(("%s.%s") % (imgur_id, filetype))
        self._links.append(
                ("https://i.imgur.com/%s.%s") % (imgur_id, filetype))

    def download(self) -> None:
        """
        Download and save a local copy of the image or video files.
        """
        n = len(self._links)
        for i in range(n):
            file = self._files[i]
            link = self._links[i]
            print("downloading file {} [{}/{}]".format(file, i + 1, n))
            r = req.get(link)
            f = open(file, mode='wb')
            for crap in r.iter_content(131072):
                f.write(crap)
            f.close()


def get_link() -> str:
    """
    Get an imgur link.
    """
    validlink = False
    while (not validlink):
        link = input("Please enter an imgur url: \n")
        validlink = ("imgur.com" in link)
        if (not validlink):
            print("Not valid link")
    return link


def get_imgur_links(link_to_page: str) -> ImgurLinks:
    """
    Get all links to images and videos in a page.

    Parameters:
     link_to_page[str]: The link to the imgur page.

    Returns:
     imgur_links[ImgurLinks]: Every link to an image or video file on this
     imgur page.
    """
    r = req.get(link_to_page)
    imgur_links = ImgurLinks()

    line, imgur_id = '', ''
    for c in r.text:
        if (c != '\n'):
            line += c
        else:
            if ("http://schema.org/" in line) and ("id" in line):
                line = line.strip()
                for character in line[9:]:
                    if character != '\"':
                        imgur_id += character
                    else:
                        break
                if "ImageObject" in line:
                    imgur_links.append(imgur_id, "jpg")
                elif "VideoObject" in line:
                    imgur_links.append(imgur_id, "gif")
            line, imgur_id = '', ''
    return imgur_links


if __name__ == "__main__":
    if len(sys.argv) >= 1 and "imgur.com" in sys.argv[1]:
        link_to_page = sys.argv[1]
    else: 
        link_to_page = get_link()
    imgur_links = get_imgur_links(link_to_page)
    while(1):
        print("ID\tLINK")
        for j in range(len(imgur_links)):
            print("%s\t%s" % (imgur_links.get_id(j), imgur_links.get_link(j)))
        print("\n")

        print("There are %d downloads in total." % (len(imgur_links)))
        yn = input("Continue? [y/n] ")

        if (yn == 'Y') or (yn == 'y'):
            print("")
            imgur_links.download()
            break
        else:
            break
