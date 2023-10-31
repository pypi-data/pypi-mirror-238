class ColorFormat:
    def __repr__(self) -> str:
        return str(self.rgba())
    
    def rgb(self) -> tuple[float, float, float]:
        raise NotImplementedError
    
    def rgba(self) -> tuple[float, float, float, float]:
        raise NotImplementedError
    
    def decimal_rgb(self) -> tuple[float, float, float]:
        raise NotImplementedError
    
    def decimal_rgba(self) -> tuple[float, float, float, float]:
        raise NotImplementedError
    
    def hex(self) -> str:
        raise NotImplementedError
    

class RGB(ColorFormat):
    def __init__(self, r: float | int, g: float | int, b: float | int, alpha: float = 1.) -> None:
        """
        RGB color format. Helps to create Color objects
        :param r: value from 0 to 255
        :param g: value from 0 to 255
        :param b: value from 0 to 255
        :param alpha: value from 0 to 1
        """
        super(ColorFormat, self).__init__()
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha
        
    def rgb(self) -> tuple[float | int, float | int, float | int]:
        return self.r, self.g, self.b
    
    def rgba(self) -> tuple[float | int, float | int, float | int, float]:
        return self.r, self.g, self.b, self.alpha
    
    def decimal_rgb(self) -> tuple[float, float, float]:
        return self.r/255, self.g/255, self.b/255
    
    def decimal_rgba(self) -> tuple[float, float, float, float]:
        return self.r/255, self.g/255, self.b/255, self.alpha
    
    def hex(self) -> str:
        return "#" + "%02x%02x%02x" % self.rgb()
    