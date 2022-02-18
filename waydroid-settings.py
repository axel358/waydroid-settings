#!/bin/python
import sys
import gi
import utils
import glob
import os
import subprocess
import time
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, WebKit2, GLib


class WaydroidSettings(Gtk.Application):
    def __init__(self, *args, **kargs):
        super().__init__(*args, application_id='cu.axel.waydroidsettings', **kargs)

        self.builder = Gtk.Builder.new_from_file('window.ui')
        self.window = None
        self.refreshing = False

        docs_web_view_box = self.builder.get_object('docs_web_view_box')
        self.docs_web_view = WebKit2.WebView()
        docs_web_view_box.pack_start(self.docs_web_view, True, True, 0)

        self.scripts_list_box = self.builder.get_object('scripts_list_box')
        self.free_form_switch = self.builder.get_object('free_form_switch')
        self.color_invert_switch = self.builder.get_object('color_invert_switch')
        self.suspend_switch = self.builder.get_object('suspend_switch')
        self.nav_btns_switch = self.builder.get_object('nav_btns_switch')
        self.soft_kb_switch = self.builder.get_object('soft_kb_switch')
        
        self.free_form_switch.connect('state-set', self.toggle_free_form)
        self.nav_btns_switch.connect('state-set', self.toggle_navbar)
        self.soft_kb_switch.connect('state-set', self.toggle_keyboard)

        w_width_entry = self.builder.get_object('w_width_entry')
        w_height_entry = self.builder.get_object('w_height_entry')
        wp_width_entry = self.builder.get_object('wp_width_entry')
        wp_height_entry = self.builder.get_object('wp_height_entry')

        scripts_box = self.builder.get_object('scripts_box')
        scroll_view = Gtk.ScrolledWindow()
        self.terminal = Vte.Terminal()
        self.terminal.set_input_enabled(True)
        self.terminal.set_scroll_on_output(True)
        scroll_view.add(self.terminal)

        scripts_box.pack_end(scroll_view, True, True, 10)

        self.builder.connect_signals(self)
        self.show_password_dialog()
        self.load_values()

    def load_values(self):

        self.refreshing = True
        self.free_form_switch.set_active(utils.get_prop(utils.PROP_FREE_FORM) == 'true' )
        self.color_invert_switch.set_active(utils.get_prop(utils.PROP_INVERT_COLORS) == 'true')
        self.suspend_switch.set_active(utils.get_prop(utils.PROP_SUSPEND_INACTIVE) == 'true')
        self.nav_btns_switch.set_active(utils.search_base_prop('qemu.hw.mainkeys=1'))
        self.soft_kb_switch.set_active(utils.is_kb_disabled())

        settings_box = self.builder.get_object('settings_box')
        if not utils.is_container_active():
            self.show_container_dialog()

            hbox = Gtk.Box(spacing=6)
            settings_box.add(hbox)
            hbox.set_margin_top(2.5)
            hbox.set_margin_bottom(2.5)

            button = Gtk.Button.new_with_label("Start Container Service")
            button.id = "get_waydroid_container_service_button"
            button.connect("clicked", self.on_click_start_container)
            hbox.pack_start(button, True, True, 10)

        if not utils.is_waydroid_running():
            self.show_not_available_dialog()

            hbox = Gtk.Box(spacing=6)
            settings_box.add(hbox)
            hbox.set_margin_top(2.5)
            hbox.set_margin_bottom(2.5)

            button = Gtk.Button.new_with_label("Start Session")
            button.connect("clicked", self.on_click_start_session)
            hbox.pack_start(button, True, True, 10)
        else:
            hbox = Gtk.Box(spacing=6)
            settings_box.add(hbox)
            hbox.set_margin_top(2.5)
            hbox.set_margin_bottom(2.5)

            button = Gtk.Button.new_with_label("Retart Container and Session")
            button.id = "restart_waydroid_container_and_session_button"
            button.connect("clicked", self.on_click_restart_session)
            hbox.pack_start(button, True, True, 10)

            hbox2 = Gtk.Box(spacing=6)
            settings_box.add(hbox2)
            hbox2.set_margin_top(2.5)
            hbox2.set_margin_bottom(2.5)

            button2 = Gtk.Button.new_with_label("Stop Session")
            button2.id = "stop_waydroid_session_button"
            button2.connect("clicked", self.on_click_stop_session)
            hbox2.pack_start(button2, True, True, 10)

            hbox3 = Gtk.Box(spacing=6)
            settings_box.add(hbox3)
            hbox3.set_margin_top(2.5)
            hbox3.set_margin_bottom(2.5)

            button3 = Gtk.Button.new_with_label("Freeze Container")
            button3.id = "freeze_waydroid_container_button"
            button3.connect("clicked", self.on_click_freeze_container)
            hbox3.pack_start(button3, True, True, 10)

            hbox4 = Gtk.Box(spacing=6)
            settings_box.add(hbox4)
            hbox4.set_margin_top(2.5)
            hbox4.set_margin_bottom(2.5)

            button4 = Gtk.Button.new_with_label("Unfreeze Container")
            button4.id = "unfreeze_waydroid_container_button"
            button4.connect("clicked", self.on_click_unfreeze_container)
            hbox4.pack_start(button4, True, True, 10)

        self.refreshing = False

    def on_click_start_container(self, button):
        utils.start_container_service()
        counter = 5
        while not (counter == 0):
            time.sleep(1)
            counter = counter - 1
            if utils.is_container_active():
                button.destroy()
                counter = 0
                self.load_values()

    def on_click_start_session(self, button):
        utils.start_session()
        counter = 5
        while not (counter == 0):
            time.sleep(1)
            counter = counter - 1
            if utils.is_waydroid_running():
                button.destroy()
                counter = 0
                self.load_values()

    def on_click_restart_session(self, button):
        utils.restart_session()
        self.load_values()

    def on_click_stop_session(self, button):
        utils.stop_session()
        self.load_values()

    def on_click_freeze_container(self, button):
        utils.freeze_container()
        self.load_values()

    def on_click_unfreeze_container(self, button):
        utils.unfreeze_container()
        self.load_values()

    def do_activate(self):
        if not self.window:
            self.window = self.builder.get_object('main_window')
            self.window.set_application(self)

        self.window.show_all()

    def toggle_free_form(self, switch, checked):
        if not self.refreshing:
            utils.set_prop(utils.PROP_FREE_FORM, str(checked).lower())

    def toggle_suspend(self, switch, checked):
        if not self.refreshing:
            utils.set_prop(utils.PROP_SUSPEND_INACTIVE, str(checked).lower())

    def toggle_navbar(self, switch, checked):
        if not self.refreshing:
            if checked == True:
                utils.disable_navbar()
            else:
                utils.enable_navbar()
    
    def toggle_keyboard(self, switch, checked):
        if not self.refreshing:
            if checked:
                utils.disable_kb()
            else:
                utils.enable_kb()
    
    def toggle_color_inversion(self, switch, checked):
        if not self.refreshing:
            utils.set_prop(utils.PROP_INVERT_COLORS, str(checked).lower())

    def show_ff_dialog(self, button):
        dialog = Gtk.Dialog(title='Excluded apps', use_header_bar=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.get_content_area().pack_start(Gtk.Label(label='Space separated package names to exclude'), True, True,
                                             10)
        apps_entry = Gtk.Entry()
        apps_entry.set_margin_start(5)
        apps_entry.set_margin_end(5)
        dialog.get_content_area().pack_start(apps_entry, True, True, 10)
        current_app_list = utils.get_prop(utils.PROP_BLACKLISTED_APPS)
        apps_entry.set_text(current_app_list)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(app_list:= apps_entry.get_text()) > 0:
                str_apps_list = '"'+str(apps_entry.get_text().rstrip())+'"'
                utils.set_prop(utils.PROP_BLACKLISTED_APPS, str_apps_list)

        dialog.destroy()

    def show_force_w_dialog(self, button):
        dialog = Gtk.Dialog(title='Included apps', use_header_bar=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.get_content_area().pack_start(Gtk.Label(label='Space separated package names to exclude'), True, True,
                                             10)
        apps_entry = Gtk.Entry()
        apps_entry.set_margin_start(5)
        apps_entry.set_margin_end(5)
        dialog.get_content_area().pack_start(apps_entry, True, True, 10)
        current_app_list = utils.get_prop(utils.PROP_ACTIVE_APPS)
        apps_entry.set_text(current_app_list)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(app_list:= apps_entry.get_text()) > 0:
                str_apps_list = '"'+str(apps_entry.get_text().rstrip())+'"'
                utils.set_prop(utils.PROP_ACTIVE_APPS, str_apps_list)

        dialog.destroy()
    
    
    def show_password_dialog(self):
        dialog = Gtk.Dialog(title='Root Permission Required', use_header_bar=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.get_content_area().pack_start(Gtk.Label(label='Please enter root password'), True, True,
                                             10)
        pass_entry = Gtk.Entry()
        pass_entry.set_visibility(False)
        pass_entry.set_margin_start(5)
        pass_entry.set_margin_end(5)
                
        dialog.get_content_area().pack_start(pass_entry, True, True, 10)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(password := pass_entry.get_text().strip()) > 0:
                if utils.is_correct_pass(password):
                    dialog.destroy()
                else:
                    self.show_wrong_password_dialog()
                    dialog.destroy()
                    self.show_password_dialog()

    def show_wrong_password_dialog(self):
        dialog = Gtk.MessageDialog(transient_for=self.window)
        dialog.props.message_type=Gtk.MessageType.INFO
        dialog.props.title = 'Authorization Issue'
        dialog.props.text = 'The password you entered was not correct. Please try again'
        dialog.add_buttons('OK', Gtk.ResponseType.OK)
        dialog.run()
        dialog.destroy()
        # ~ self.show_password_dialog()
    
    def show_not_available_dialog(self):
        dialog = Gtk.MessageDialog(transient_for=self.window)
        dialog.props.message_type=Gtk.MessageType.INFO
        dialog.props.title = 'Waydroid session not running'
        dialog.props.text = 'Waydroid is either not installed or currently not running. Please start the session using the option at the bottom of the next screen. '
        dialog.add_buttons('OK', Gtk.ResponseType.OK)
        dialog.run()
        dialog.destroy()

    def show_container_dialog(self):
        dialog = Gtk.MessageDialog(transient_for=self.window)
        dialog.props.message_type=Gtk.MessageType.INFO
        dialog.props.title = 'Waydroid container not running'
        dialog.props.text = 'Waydroid container service is currently not running or waydroid is not installed properly. Please start the service using the option at the bottom of the next screen. '
        dialog.add_buttons('OK', Gtk.ResponseType.OK)
        dialog.run()
        dialog.destroy()

    def show_resize_dialog(self, button):
        dialog_builder = Gtk.Builder().new_from_file('resize_dialog.ui')
        dialog_box = dialog_builder.get_object('resize_dialog_box')
        dialog = Gtk.Dialog(title='Resize system image', use_header_bar=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        image_size_label = dialog_builder.get_object('image_size_label')
        image_size_label.set_text(image_size_label.get_text()+' '+str(utils.get_image_size()))
        image_size_entry = dialog_builder.get_object('image_size_entry')
        dialog.get_content_area().add(dialog_box)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            utils.resize_image(image_size_entry.get_text())

        dialog.destroy()
        
    def show_wipe_dialog(self, button):
        dialog = Gtk.MessageDialog(transient_for=self.window)
        dialog.props.message_type=Gtk.MessageType.INFO
        dialog.props.title = 'Wipe all data'
        dialog.props.text = 'Wipe all Waydroid data? This cannot be undone'
        dialog.add_buttons('OK', Gtk.ResponseType.OK, 'CANCEL', Gtk.ResponseType.CANCEL)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            utils.wipe_data()
        dialog.destroy()

    def update_scripts_list(self):
        for child in self.scripts_list_box.get_children():
            self.scripts_list_box.remove(child)

        script_list = glob.glob(utils.SCRIPTS_DIR+'/**/*.sh', recursive=True) + glob.glob(utils.SCRIPTS_DIR+'/**/*.py', recursive=True)

        for script in script_list:
            row = Gtk.ListBoxRow()
            script_row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            script_icon_image = Gtk.Image().new_from_icon_name(
                'text-x-script', Gtk.IconSize.BUTTON)
            script_name_label = Gtk.Label(label=os.path.basename(script))
            run_help_button = Gtk.Button().new_from_icon_name(
                'help-about', Gtk.IconSize.BUTTON)
            run_help_button.connect('clicked', self.run_help, script)
            run_script_button = Gtk.Button().new_from_icon_name(
                'media-playback-start', Gtk.IconSize.BUTTON)
            run_script_button.connect('clicked', self.run_script, script)

            script_row.pack_start(script_icon_image, False, False, 10)
            script_row.pack_start(script_name_label, False, False, 5)
            script_row.pack_end(run_help_button, False, False, 10)
            script_row.pack_end(run_script_button, False, False, 10)

            row.add(script_row)
            self.scripts_list_box.add(row)

        self.scripts_list_box.show_all()

    def run_script(self, button, script):
        if '.py' in script: interpreter = '/bin/python3'
        else: interpreter = '/bin/bash'
        self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, None, [interpreter, script], None, GLib.SpawnFlags.DEFAULT, None,None,-1, None, None)

    def run_help(self, button, script):
        if '.py' in script: interpreter = '/bin/python3'
        else: interpreter = '/bin/bash'
        help_arg = '-h'
        self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, None, [interpreter, script, help_arg], None, GLib.SpawnFlags.DEFAULT, None,None,-1, None, None)

    def on_tab_switched(self, notebook, page, position):
        if position == 1:
            self.docs_web_view.load_uri(utils.DOCS_URL)
        elif position == 2:
            self.update_scripts_list()

    def show_about_dialog(self, button):
        dialog = Gtk.AboutDialog()
        dialog.props.program_name = 'Waydroid Settings'
        dialog.props.version = "0.1.0"
        dialog.props.authors = ['Axel358', 'Jon West']
        dialog.props.copyright = 'GPL-3'
        dialog.props.logo_icon_name = 'waydroid-settings'
        dialog.props.comments = 'Control Waydroid settings'
        dialog.props.website = utils.HOME_URL
        dialog.set_transient_for(self.window)
        dialog.show()


if __name__ == "__main__":
    app = WaydroidSettings()
    app.run(sys.argv)
