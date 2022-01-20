from html.parser import HTMLParser

class HTML_HeaderParser(HTMLParser):
    class HeaderNode:
        def __init__(self, parent, data):
            self.parent = parent
            self.data = data
            self.children = []

            if self.parent != None:
                self.parent.children.append(self)

        def get_parent(self):
            return self.parent

        def get_depth(self):
            if self.parent == None:
                return 0

            return self.parent.get_depth() + 1

        def apply_noret(self, func):
            if self.parent != None:
                func(self)

            for i in self.children:
                i.apply_noret(func)

    class HeaderTree:
        def __init__(self, root):
            self.root = root

        def get_root(self):
            return self.root

        def apply(self, func):
            self.root.apply_noret(func)

    def __init__(self, maxdepth=6):
        HTMLParser.__init__(self)

        self.headerlist = []
        self.tags = ["h1", "h2", "h3", "h4", "h5", "h6"][:maxdepth]
        self.curlevel = ""
    
    def handle_starttag(self, tag, attrs):
        if tag in self.tags:
            self.curlevel = tag

    def handle_endtag(self, tag):
        if tag in self.tags:
            self.curlevel = ""

    def handle_data(self, data):
        if self.curlevel:
            self.headerlist.append([int(self.curlevel[1]), data])

    def get_headertree(self):
        tree = self.HeaderTree(self.HeaderNode(None, None))
        cur = tree.get_root()

        for i in self.headerlist:
            if i[0] > cur.get_depth():
                cur = self.HeaderNode(cur, i[1])
            else:
                while i[0] <= cur.get_depth():
                    cur = cur.get_parent()
                cur = self.HeaderNode(cur, i[1])
        
        return tree


# for test and giving example
if __name__ == "__main__":
    a = HTML_HeaderParser()
    with open("html-sample/2.html", 'r') as f:
        a.feed(f.read())

    for i in a.headerlist:
        print(i)
    
    a.get_headertree().apply(lambda x: print("-" * x.get_depth(), x.data))