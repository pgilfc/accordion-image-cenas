from PIL import Image

IMAGE_MODE = "1" # PIL: 1-bit pixels, black and white, stored with one pixel per byte


class IMG:
    def __init__(self, data: str, height: int, width: int, img_path: str, img_name: str):
        self.data = data
        self.height = height
        self.width = width
        self.img_path = img_path
        self.img_name = img_name

    @staticmethod
    def _hex_to_byte(hex_data: str) -> bytes:
        return bytes.fromhex(hex_data)
    
    @staticmethod
    def _sliding_window(data: str, window: int):
        for i in range(0, len(data) - window + 1):
            yield i, i+window, data[i:i+window]

    @staticmethod
    def _build_image(byte_data: bytes, height: int, width: int) -> Image.Image:
        return Image.frombytes(IMAGE_MODE, (width, height), byte_data)
    
    def _infere_window(self) -> int:
        """
        This is required because:
        https://stackoverflow.com/questions/75633075/why-do-image-size-differ-when-vertical-vs-horizontal/75633329#75633329
        """
        width = self.width
        while width%8 != 0:
            width += 1
        return self.height*(width//8)
        

    def _store_image(self, img: Image.Image, y: int, x: int, init: int, end: int)-> None:
        img.save(f"{self.img_path}/{self.img_name}_p{x}x{y}_window_{init}_{end}.bmp")
        
        
    def create_images(self):
        print(self.img_name, "hex_len", len(self.data))
        window = self._infere_window()
        if len(self.data)//2 < window:
            print("cant parse img:", self.img_name)
            return
        for init, end, windowed_message in self._sliding_window(self.data, window*2):
            byte_data: bytes = self._hex_to_byte(windowed_message)
            print(self.img_name, "byte_len", len(byte_data), init, end)
            img1 = self._build_image(byte_data, self.height, self.width)
            self._store_image(img1, self.height, self.width, init, end)
        


