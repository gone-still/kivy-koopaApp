from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

# Let's get ready to motherfucking roll:
from kivy.graphics.texture import Texture
import cv2
import numpy as np

# Set background color for the window:
Window.clearcolor = (1, 1, 1, 1)  # RGBA
# Set window size:
# Window.size = (360, 600)

# Nasty globals:
colorBaseValue = 15  # Color starting value
baseHue = 0  # Base hue value
colorIncrement = colorBaseValue  # The color increment
imageHue = baseHue  # Image hue

inputImageName = "koopa01.png"  # image name


def generateTexture(inputImage):
    # [ADD] Flip the array upside-down:
    inputImage = np.flipud(inputImage)

    # numpy array dimensions:
    (imageHeight, imageWidth, imageChannels) = inputImage.shape

    # Extract numpy data:
    data = inputImage.tobytes()

    # Create Kivy texture
    texture = Texture.create(size=(imageWidth, imageHeight), colorfmt="rgb")
    texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")

    print("Converted image...")

    return texture


def processImage(inputImage):
    print("processImage>> Processing Image...")

    # BGR -> HSV Conversion:
    hsvImg = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    # Split the channels, get H component:
    (hueImg, satImg, valueImg) = cv2.split(hsvImg)
    # Get image dimensions:
    (imageHeight, imageWidth) = hueImg.shape

    print("processImage>> Iterating Image...")

    # Get the global colorIncrementer:
    global colorIncrement
    # Get the imageHue:
    global imageHue
    # Increase hue value:
    imageHue = imageHue + colorIncrement

    print("imageHue1: " + str(imageHue) + " colorIncrement: " + str(colorIncrement))

    # Clip imageHue value:
    if imageHue >= 179:
        imageHue = 0

    print("imageHue2: " + str(imageHue) + " colorIncrement: " + str(colorIncrement))

    # Process image:
    for j in range(0, imageHeight):
        for i in range(0, imageWidth):
            currentHuePixel = hueImg[j, i]
            if currentHuePixel == 60:
                hueImg[j, i] = imageHue

    # Merge H (modified), S, V:
    print("processImage>> Merging Image...")
    newImage = cv2.merge([hueImg, satImg, valueImg])

    # [ADD] HSV -> RGB (RGB for kivy):
    newImage = cv2.cvtColor(newImage, cv2.COLOR_HSV2RGB)
    print("processImage>> Image Processed")

    # Show Image
    # [ADD] cv2.imshow("Processed Image", newImage)

    return newImage


def resetImage(*args):
    print("resetImage>> Clearing Image...")

    # Get the image:
    global image
    # Clear the source:
    image.source = ''
    # Re-assign the image source:
    global layout
    layout.children[1].source = inputImageName

    # Reset color variables:
    global imageHue
    imageHue = baseHue
    global colorIncrement
    colorIncrement = colorBaseValue

    print("resetImage>> Image Reset.")


def clickProcess(*args):
    # Read the image via opencv:
    inputImage = cv2.imread(inputImageName)

    # Check if image was loaded:
    if inputImage.size != 0:
        print("clickProcess>> Image Loaded")

        # cv2.namedWindow("test", cv2.WINDOW_NORMAL)
        # cv2.imshow("test", inputImage)

        # Process Image:
        inputImage = processImage(inputImage)

        # Convert numpy array to kivy texture and
        # update widget contents:
        global image
        image.texture = generateTexture(inputImage)

    else:
        print("clickProcess>> Image was not loaded")


class MainApp(App):

    def build(self):

        # Set the layout with extra parameters: # spacing = 10 , padding = 40
        global layout
        layout = GridLayout(cols=1, padding=100)  # col_force_default=False, col_default_width=900

        # Set the image:
        global image
        image = Image(source=inputImageName, allow_stretch=True)  # allow_stretch=True, keep_ratio=True
        # image.stretch = True
        image.width = 200

        # Create the relative layout::
        r1 = RelativeLayout()

        # Set button parameters:
        btnWidth = 200
        btnHeight = 50

        # Create button1:
        btn1 = Button(text="Reset", size_hint=(None, None), width=btnWidth, height=btnHeight,
                      pos_hint={"center_x": 0.5, "center_y": 0.6}) # Adjust til it properly fits into the screen
        btn1.bind(on_press=resetImage)
        # Add to relative layout:
        r1.add_widget(btn1)

        # Create button2:
        btn2 = Button(text="Process", size_hint=(None, None), width=btnWidth, height=btnHeight,
                      pos_hint={"center_x": 0.5, "center_y": 0.2}) # Adjust til it properly fits into the screen
        btn2.bind(on_press=clickProcess)
        # Add to relative layout:
        r1.add_widget(btn2)

        # Add the items to layout:
        layout.add_widget(image, 1)  # Image
        layout.add_widget(r1, 0)  # Relative layout with buttons

        return layout


MainApp().run()
