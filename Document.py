import re


class Document:
    documentText = ""
    path = ""
    previewLength = 100

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, "r")
        self.documentText = self.file.read()

    def preview(self):
        print(self.documentText[0:self.previewLength - 1])

    def search(self, searchTerm: str):
        indexArray = [_.start() for _ in re.finditer(searchTerm, self.documentText)]

        count = 1
        for instance in indexArray:

            termIndex = instance
            prevStart = 0
            prevEnd = termIndex + len(searchTerm) - 1 + self.previewLength

            # sets index to start of preview if search term is further in document than preview length
            if termIndex > self.previewLength - 1:
                prevStart = termIndex - self.previewLength

            print("Result: "+str(count))
            print(self.documentText[prevStart:prevEnd]+"\n")

            count+=1
