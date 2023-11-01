from setuptools import setup
setup(
    name="vsbutton",
    version="0.5",
    description="This Package is used to create Buttons like in Visual Studio 2023",
    long_description = """
The VSButton module is designed to create modern and stylish buttons that resemble those used in the Visual Studio main page. These buttons are not only visually appealing but also highly customizable. With this module, you can effortlessly integrate these buttons into your Tkinter-based graphical user interfaces (GUIs).

Key Features:

Customizable Appearance: You can create buttons with unique headings, descriptions, secondary descriptions, and icons. The module allows you to define the appearance of your buttons, including their color themes (light or dark), making them suitable for various styles and designs.

Hover Effects: The buttons come with built-in hover effects. When the mouse cursor hovers over a button, you can specify custom actions, such as changing the button's appearance or displaying additional information.

Clickable Actions: These buttons support click events. You can define actions or functions to execute when the buttons are clicked, enabling seamless integration with your application's functionality.
""",
    author="Rana Kabeer",
    packages=['vsbutton'],
    install_requires=[])
