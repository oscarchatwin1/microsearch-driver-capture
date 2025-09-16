import json
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.metrics import dp

from storage import StorageManager
from syncer import SyncManager
from dropdown_manager import DropdownManager
from dropdown_widget import DropdownWidget

class NewEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.dropdown_manager = DropdownManager()
        self.mysql_config = None
        self.setup_ui()
        self.load_dropdown_data()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Scrollable form
        scroll = ScrollView()
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=dp(10))
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Form fields
        self.fields = {}
        
        # Description
        form_layout.add_widget(Label(text='Description*:', size_hint_y=None, height=dp(40)))
        self.fields['description'] = self.create_field_widget('description')
        form_layout.add_widget(self.fields['description'])
        
        # Size (kg)
        form_layout.add_widget(Label(text='Size (kg):', size_hint_y=None, height=dp(40)))
        self.fields['size_kg'] = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['size_kg'])
        
        # Use By Date
        form_layout.add_widget(Label(text='Use By Date:', size_hint_y=None, height=dp(40)))
        self.fields['use_by_date'] = TextInput(multiline=False, hint_text='YYYY-MM-DD', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['use_by_date'])
        
        # Pack Code
        form_layout.add_widget(Label(text='Pack Code:', size_hint_y=None, height=dp(40)))
        self.fields['pack_code'] = self.create_field_widget('pack_code')
        form_layout.add_widget(self.fields['pack_code'])
        
        # Bird Temp
        form_layout.add_widget(Label(text='Bird Temp (°C):', size_hint_y=None, height=dp(40)))
        self.fields['bird_temp_c'] = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['bird_temp_c'])
        
        # Customer
        form_layout.add_widget(Label(text='Customer:', size_hint_y=None, height=dp(40)))
        self.fields['customer'] = self.create_field_widget('customer')
        form_layout.add_widget(self.fields['customer'])
        
        # Retailer
        form_layout.add_widget(Label(text='Retailer*:', size_hint_y=None, height=dp(40)))
        self.fields['retailer'] = self.create_field_widget('retailer')
        form_layout.add_widget(self.fields['retailer'])
        
        # Supplier
        form_layout.add_widget(Label(text='Supplier:', size_hint_y=None, height=dp(40)))
        self.fields['supplier'] = self.create_field_widget('supplier')
        form_layout.add_widget(self.fields['supplier'])
        
        # Code
        form_layout.add_widget(Label(text='Code:', size_hint_y=None, height=dp(40)))
        self.fields['code'] = self.create_field_widget('code')
        form_layout.add_widget(self.fields['code'])
        
        # Sample Number
        form_layout.add_widget(Label(text='Sample Number:', size_hint_y=None, height=dp(40)))
        self.fields['sample_number'] = TextInput(multiline=False, input_filter='int', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['sample_number'])
        
        # Price
        form_layout.add_widget(Label(text='Price (£):', size_hint_y=None, height=dp(40)))
        self.fields['price_gbp'] = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['price_gbp'])
        
        # Van Temp
        form_layout.add_widget(Label(text='Van Temp (°C):', size_hint_y=None, height=dp(40)))
        self.fields['van_temp_c'] = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=dp(40))
        form_layout.add_widget(self.fields['van_temp_c'])
        
        scroll.add_widget(form_layout)
        layout.add_widget(scroll)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        save_btn = Button(text='Save', size_hint_x=0.2)
        save_btn.bind(on_press=self.save_sample)
        button_layout.add_widget(save_btn)
        
        save_new_btn = Button(text='Save & New', size_hint_x=0.2)
        save_new_btn.bind(on_press=self.save_and_new)
        button_layout.add_widget(save_new_btn)
        
        refresh_btn = Button(text='Refresh', size_hint_x=0.2)
        refresh_btn.bind(on_press=self.refresh_dropdowns)
        button_layout.add_widget(refresh_btn)
        
        back_btn = Button(text='Back', size_hint_x=0.2)
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def create_field_widget(self, field_name: str):
        """Create appropriate widget for field (dropdown or text input)"""
        if self.dropdown_manager.is_dropdown_field(field_name):
            # Create dropdown widget
            options = self.dropdown_manager.get_dropdown_options(field_name, self.mysql_config)
            placeholder = self.dropdown_manager.get_placeholder(field_name)
            allow_custom = self.dropdown_manager.allows_custom_input(field_name)
            
            widget = DropdownWidget(
                options=options,
                placeholder=placeholder,
                allow_custom=allow_custom,
                size_hint_y=None,
                height=dp(40)
            )
            
            # Set default values for supplier and code
            if field_name == 'supplier':
                widget.set_text('Flixton')
            elif field_name == 'code':
                widget.set_text('GB S011')
            
            return widget
        else:
            # Create regular text input
            widget = TextInput(multiline=False, size_hint_y=None, height=dp(40))
            
            # Set default values
            if field_name == 'supplier':
                widget.text = 'Flixton'
            elif field_name == 'code':
                widget.text = 'GB S011'
            
            return widget
    
    def load_dropdown_data(self):
        """Load dropdown data from configuration and database"""
        try:
            # Load MySQL config
            import json
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.mysql_config = config.get('mysql')
            
            # Refresh dropdown options
            if self.mysql_config:
                self.dropdown_manager.refresh_all_options(self.mysql_config)
                
        except Exception as e:
            print(f"Error loading dropdown data: {e}")
    
    def refresh_dropdown_data(self):
        """Refresh dropdown data from database"""
        if self.mysql_config:
            self.dropdown_manager.sync_dropdown_data(self.mysql_config)
            # Update existing dropdown widgets
            for field_name, widget in self.fields.items():
                if isinstance(widget, DropdownWidget):
                    options = self.dropdown_manager.get_dropdown_options(field_name, self.mysql_config)
                    widget.set_options(options)
    
    def refresh_dropdowns(self, instance):
        """Refresh dropdown data when user clicks refresh button"""
        self.refresh_dropdown_data()
        self.show_popup("Refresh", "Dropdown data refreshed from database")
    
    def save_sample(self, instance):
        self._save_sample(clear_form=False)
    
    def save_and_new(self, instance):
        self._save_sample(clear_form=True)
    
    def _save_sample(self, clear_form=False):
        # Get form data
        sample_data = {}
        for key, field in self.fields.items():
            # Handle both TextInput and DropdownWidget
            if hasattr(field, 'get_text'):
                value = field.get_text().strip()
            else:
                value = field.text.strip()
            if value:
                sample_data[key] = value
        
        # Add device and driver IDs from config
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                sample_data['device_id'] = config.get('device_id', 'DEVICE_001')
                sample_data['driver_id'] = config.get('driver_id', 'DRIVER_001')
        except:
            sample_data['device_id'] = 'DEVICE_001'
            sample_data['driver_id'] = 'DRIVER_001'
        
        # Save sample
        success, message = self.storage.create_sample(sample_data)
        
        if success:
            if clear_form:
                self.clear_form()
            self.show_popup("Success", message)
        else:
            self.show_popup("Error", message)
    
    def clear_form(self):
        for field_name, field in self.fields.items():
            if hasattr(field, 'set_text'):
                # DropdownWidget
                if field_name == 'supplier':
                    field.set_text('Flixton')
                elif field_name == 'code':
                    field.set_text('GB S011')
                else:
                    field.set_text('')
            else:
                # TextInput
                if field_name == 'supplier':
                    field.text = 'Flixton'
                elif field_name == 'code':
                    field.text = 'GB S011'
                else:
                    field.text = ''
    
    def go_back(self, instance):
        self.manager.current = 'menu'
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class QueueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Tabbed panel for different status views
        self.tab_panel = TabbedPanel(do_default_tab=False)
        
        # Pending tab
        pending_tab = TabbedPanelItem(text='Pending')
        pending_tab.content = self.create_sample_list('pending')
        self.tab_panel.add_widget(pending_tab)
        
        # Synced tab
        synced_tab = TabbedPanelItem(text='Synced')
        synced_tab.content = self.create_sample_list('synced')
        self.tab_panel.add_widget(synced_tab)
        
        # Error tab
        error_tab = TabbedPanelItem(text='Error')
        error_tab.content = self.create_sample_list('error')
        self.tab_panel.add_widget(error_tab)
        
        layout.add_widget(self.tab_panel)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=None, height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def create_sample_list(self, status):
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        layout.bind(minimum_height=layout.setter('height'))
        
        samples = self.storage.get_samples(status_filter=status)
        
        if not samples:
            layout.add_widget(Label(text=f'No {status} samples', size_hint_y=None, height=dp(40)))
        else:
            for sample in samples:
                sample_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(5))
                
                # Sample info
                info_text = f"{sample['description'][:20]}... | {sample['retailer']} | #{sample['sample_number']}"
                info_label = Label(text=info_text, text_size=(dp(200), None), halign='left', valign='middle')
                sample_layout.add_widget(info_label)
                
                # Created time
                created_time = sample['created_at_local'][:16] if sample['created_at_local'] else 'Unknown'
                time_label = Label(text=created_time, size_hint_x=0.3, text_size=(dp(100), None), halign='center', valign='middle')
                sample_layout.add_widget(time_label)
                
                # Action button
                if status == 'pending':
                    edit_btn = Button(text='Edit', size_hint_x=0.2)
                    edit_btn.bind(on_press=lambda x, s=sample: self.edit_sample(s))
                    sample_layout.add_widget(edit_btn)
                    
                    delete_btn = Button(text='Delete', size_hint_x=0.2)
                    delete_btn.bind(on_press=lambda x, s=sample: self.delete_sample(s))
                    sample_layout.add_widget(delete_btn)
                elif status == 'error':
                    error_btn = Button(text='View Error', size_hint_x=0.3)
                    error_btn.bind(on_press=lambda x, s=sample: self.show_error(s))
                    sample_layout.add_widget(error_btn)
                
                layout.add_widget(sample_layout)
        
        scroll.add_widget(layout)
        return scroll
    
    def edit_sample(self, sample):
        # Switch to new entry screen with pre-filled data
        new_entry_screen = self.manager.get_screen('new_entry')
        for key, field in new_entry_screen.fields.items():
            if key in sample and sample[key] is not None:
                field.text = str(sample[key])
        
        self.manager.current = 'new_entry'
    
    def delete_sample(self, sample):
        success, message = self.storage.delete_sample(sample['id'])
        self.show_popup("Delete", message)
        if success:
            self.refresh_lists()
    
    def show_error(self, sample):
        error_msg = sample.get('error_msg', 'Unknown error')
        self.show_popup("Sync Error", error_msg)
    
    def refresh_lists(self):
        # Refresh all tab contents
        for tab in self.tab_panel.tab_list:
            tab.content = self.create_sample_list(tab.text.lower())
    
    def go_back(self, instance):
        self.manager.current = 'menu'
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
    
    def on_enter(self):
        # Refresh lists when entering screen
        self.refresh_lists()

class SyncScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.syncer = SyncManager()
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Status information
        status_layout = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=dp(10))
        
        self.connection_label = Label(text='Connection: Checking...', size_hint_y=None, height=dp(40))
        status_layout.add_widget(self.connection_label)
        
        self.sync_status_label = Label(text='Sync Status: Unknown', size_hint_y=None, height=dp(40))
        status_layout.add_widget(self.sync_status_label)
        
        self.counts_label = Label(text='Sample Counts: Loading...', size_hint_y=None, height=dp(60))
        status_layout.add_widget(self.counts_label)
        
        layout.add_widget(status_layout)
        
        # Sync button
        self.sync_btn = Button(text='Sync Now', size_hint_y=None, height=dp(60))
        self.sync_btn.bind(on_press=self.sync_now)
        layout.add_widget(self.sync_btn)
        
        # Test connection button
        test_btn = Button(text='Test MySQL Connection', size_hint_y=None, height=dp(50))
        test_btn.bind(on_press=self.test_connection)
        layout.add_widget(test_btn)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=None, height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def update_status(self):
        status = self.syncer.get_sync_status()
        
        # Update connection info
        connection_text = "Connection: "
        if status['current_ssid']:
            connection_text += f"WiFi: {status['current_ssid']}"
        elif status['ethernet_connected']:
            connection_text += "Ethernet"
        else:
            connection_text += "Not available"
        
        self.connection_label.text = connection_text
        
        # Update sync status
        if status['is_sync_allowed']:
            self.sync_status_label.text = f"Sync Status: Allowed ({status['connection_info']})"
            self.sync_btn.disabled = False
            self.sync_btn.text = 'Sync Now'
        else:
            self.sync_status_label.text = f"Sync Status: Not allowed ({status['connection_info']})"
            self.sync_btn.disabled = True
            self.sync_btn.text = 'Sync Disabled'
        
        counts = status['sample_counts']
        self.counts_label.text = f"Pending: {counts['pending']} | Synced: {counts['synced']} | Errors: {counts['error']}"
    
    def sync_now(self, instance):
        success, message = self.syncer.sync_now()
        self.show_popup("Sync Result", message)
        self.update_status()
    
    def test_connection(self, instance):
        success, message = self.syncer.test_mysql_connection()
        self.show_popup("Connection Test", message)
    
    def go_back(self, instance):
        self.manager.current = 'menu'
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
    
    def on_enter(self):
        # Update status when entering screen
        self.update_status()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Title
        title = Label(text='Microsearch Driver Capture', font_size=dp(24), size_hint_y=None, height=dp(60))
        layout.add_widget(title)
        
        # Menu buttons
        new_entry_btn = Button(text='New Entry', size_hint_y=None, height=dp(60))
        new_entry_btn.bind(on_press=self.go_to_new_entry)
        layout.add_widget(new_entry_btn)
        
        queue_btn = Button(text='Today/Queue', size_hint_y=None, height=dp(60))
        queue_btn.bind(on_press=self.go_to_queue)
        layout.add_widget(queue_btn)
        
        sync_btn = Button(text='Sync', size_hint_y=None, height=dp(60))
        sync_btn.bind(on_press=self.go_to_sync)
        layout.add_widget(sync_btn)
        
        self.add_widget(layout)
    
    def go_to_new_entry(self, instance):
        self.manager.current = 'new_entry'
    
    def go_to_queue(self, instance):
        self.manager.current = 'queue'
    
    def go_to_sync(self, instance):
        self.manager.current = 'sync'

class MicrosearchApp(App):
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(NewEntryScreen(name='new_entry'))
        sm.add_widget(QueueScreen(name='queue'))
        sm.add_widget(SyncScreen(name='sync'))
        
        return sm

if __name__ == '__main__':
    MicrosearchApp().run()
