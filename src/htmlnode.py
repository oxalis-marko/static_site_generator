class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f" {key}=\"{value}\""
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):

    def __init__(self, tag , value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        if self.children == None:
            raise ValueError("Invalid HTML: no children")
        result = f"<{self.tag}>"
        for node in self.children:
            result += node.to_html()
        result += f"</{self.tag}>"
        return result