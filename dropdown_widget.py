from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from typing import List, Callable, Optional

class DropdownWidget(BoxLayout):
    """Custom dropdown widget that combines text input with dropdown functionality"""
    
    def __init__(self, options: List[str] = None, placeholder: str = "", allow_custom: bool = True, **kwargs):
        super().__init__(**kwargs)
        
        self.options = options or []
        self.placeholder = placeholder
        self.allow_custom = allow_custom
        self.on_text_change = None
        self.popup = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components"""
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(5)
        
        # Text input
        self.text_input = TextInput(
            multiline=False,
            hint_text=self.placeholder,
            size_hint_x=0.8
        )
        self.text_input.bind(text=self.on_text_input_change)
        self.add_widget(self.text_input)
        
        # Dropdown button
        self.dropdown_btn = Button(
            text='▼',
            size_hint_x=0.2,
            size_hint_y=1
        )
        self.dropdown_btn.bind(on_press=self.show_dropdown)
        self.add_widget(self.dropdown_btn)
    
    def on_text_input_change(self, instance, text):
        """Handle text input changes"""
        if self.on_text_change:
            self.on_text_change(text)
    
    def show_dropdown(self, instance):
        """Show dropdown popup with options"""
        if not self.options:
            return
        
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Title
        title_label = Label(
            text=f"Select {self.placeholder.replace('...', '').title()}",
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='center'
        )
        content.add_widget(title_label)
        
        # Scrollable options
        scroll = ScrollView()
        options_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        options_layout.bind(minimum_height=options_layout.setter('height'))
        
        for option in self.options:
            btn = Button(
                text=option,
                size_hint_y=None,
                height=dp(40),
                text_size=(None, None),
                halign='left'
            )
            btn.bind(on_press=lambda x, opt=option: self.select_option(opt))
            options_layout.add_widget(btn)
        
        scroll.add_widget(options_layout)
        content.add_widget(scroll)
        
        # Custom input option
        if self.allow_custom:
            custom_label = Label(
                text="Or enter custom value:",
                size_hint_y=None,
                height=dp(30),
                text_size=(None, None),
                halign='center'
            )
            content.add_widget(custom_label)
            
            custom_input = TextInput(
                multiline=False,
                hint_text="Custom value...",
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(custom_input)
            
            # Custom input button
            custom_btn = Button(
                text="Use Custom Value",
                size_hint_y=None,
                height=dp(40)
            )
            custom_btn.bind(on_press=lambda x: self.select_custom(custom_input.text))
            content.add_widget(custom_btn)
        
        # Close button
        close_btn = Button(
            text="Close",
            size_hint_y=None,
            height=dp(40)
        )
        close_btn.bind(on_press=self.close_dropdown)
        content.add_widget(close_btn)
        
        # Create and show popup
        self.popup = Popup(
            title="Select Option",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=False
        )
        self.popup.open()
    
    def select_option(self, option: str):
        """Select an option from dropdown"""
        self.text_input.text = option
        self.close_dropdown()
    
    def select_custom(self, custom_value: str):
        """Select custom value"""
        if custom_value.strip():
            self.text_input.text = custom_value.strip()
        self.close_dropdown()
    
    def close_dropdown(self, instance=None):
        """Close dropdown popup"""
        if self.popup:
            self.popup.dismiss()
            self.popup = None
    
    def set_options(self, options: List[str]):
        """Update dropdown options"""
        self.options = options
    
    def set_text(self, text: str):
        """Set text input value"""
        self.text_input.text = text
    
    def get_text(self) -> str:
        """Get text input value"""
        return self.text_input.text
    
    def set_placeholder(self, placeholder: str):
        """Set placeholder text"""
        self.placeholder = placeholder
        self.text_input.hint_text = placeholder
    
    def bind_text_change(self, callback: Callable):
        """Bind text change callback"""
        self.on_text_change = callback
