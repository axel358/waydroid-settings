#!/usr/bin/env python3
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
from gi.repository import Gtk, Vte, WebKit2, GLib, Gdk


class WaydroidSettings(Gtk.Application):
    DATA_DIR = '/usr/share/waydroid-settings/'
    APP_ID = 'cu.axel.WaydroidSettings'

    def __init__(self, *args, **kargs):
        super().__init__(*args, application_id=self.APP_ID, **kargs)

        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.append_search_path(self.DATA_DIR + 'icons')

        self.builder = Gtk.Builder.new_from_file(self.DATA_DIR + 'window.ui')
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

        scripts_box = self.builder.get_object('scripts_box')
        scroll_view = Gtk.ScrolledWindow()
        self.terminal = Vte.Terminal()
        self.terminal.set_input_enabled(True)
        self.terminal.set_scroll_on_output(True)
        bg_color = Gdk.RGBA()
        bg_color.red = 1.0
        bg_color.blue = 1.0
        bg_color.green = 1.0
        bg_color.alpha = 1.0
        self.terminal.set_color_background(bg_color)
        fg_color = Gdk.RGBA()
        fg_color.red = 0.0
        fg_color.blue = 0.0
        fg_color.green = 0.0
        fg_color.alpha = 1.0
        self.terminal.set_color_foreground(fg_color)
        scroll_view.add(self.terminal)
        terminal_box = self.builder.get_object('terminal_box')
        self.terminal.set_margin_bottom(12)
        self.terminal.set_margin_top(12)
        self.terminal.set_margin_end(12)
        self.terminal.set_margin_start(12)
        terminal_box.pack_end(scroll_view, True, True, 0)

        self.builder.connect_signals(self)
        self.load_values()

    def load_values(self):

        self.refreshing = True
        self.free_form_switch.set_active(utils.search_base_prop('persist.waydroid.multi_windows=true'))
        self.color_invert_switch.set_active(utils.get_prop(utils.PROP_INVERT_COLORS) == 'true')
        self.suspend_switch.set_active(utils.get_prop(utils.PROP_SUSPEND_INACTIVE) == 'true')
        self.nav_btns_switch.set_active(utils.search_base_prop('qemu.hw.mainkeys=1'))
        self.soft_kb_switch.set_active(utils.is_kb_disabled())

        container_banner = self.builder.get_object('container_banner')
        session_banner = self.builder.get_object('session_banner')
        container_banner.set_revealed(False)
        session_banner.set_revealed(False)

        if not utils.is_container_active():
            container_banner.set_revealed(True)
        elif not utils.is_waydroid_running():
            session_banner.set_revealed(True)
        else:
            pass

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

    def on_toggle_freeze_container(self, switch, checked):
        if checked:
            utils.freeze_container()
        else:
            utils.unfreeze_container()

        self.load_values()

    def do_activate(self):
        if not self.window:
            self.window = self.builder.get_object('main_window')
            self.window.set_application(self)

        self.window.show_all()

    def toggle_free_form(self, switch, checked):
        if not self.refreshing:
            if checked:
                utils.enable_freeform_override()
            else:
                utils.disable_freeform_override()

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


    def show_resize_dialog(self, button):
        dialog_builder = Gtk.Builder().new_from_file(self.DATA_DIR + 'resize_dialog.ui')
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

    def select_apk(self, button):
        dialog = Gtk.FileChooserDialog(title = 'Select apk', parent = self.window, action = Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL, "_Save", Gtk.ResponseType.ACCEPT)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            utils.install_apk(dialog.get_filename())
        dialog.destroy()

    def update_scripts_list(self):
        for child in self.scripts_list_box.get_children():
            self.scripts_list_box.remove(child)

        script_list = glob.glob(utils.SCRIPTS_DIR+'/**/*.sh', recursive=True) + glob.glob(utils.SCRIPTS_DIR+'/**/*.py', recursive=True)

        for script in script_list:
            script_row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            script_icon_image = Gtk.Image().new_from_icon_name(
                'scripts-python-symbolic' if '.py' in script else 'scripts-symbolic', Gtk.IconSize.BUTTON)
            script_name_label = Gtk.Label(label=os.path.basename(script))
            run_help_button = Gtk.Button().new_from_icon_name(
                'info-symbolic', Gtk.IconSize.BUTTON)
            run_help_button.connect('clicked', self.run_help, script)
            run_script_button = Gtk.Button().new_from_icon_name(
                'run-symbolic', Gtk.IconSize.BUTTON)
            run_script_button.connect('clicked', self.run_script, script)

            script_row.pack_start(script_icon_image, False, False, 0)
            script_row.pack_start(script_name_label, False, False, 6)
            box = Gtk.Box()
            box.get_style_context().add_class('linked');
            box.pack_start(run_script_button, False, False, 0)
            box.pack_start(run_help_button, False, False, 0)
            script_row.pack_end(box, False, False, 0)

            self.scripts_list_box.add(script_row)

        self.scripts_list_box.show_all()

    def run_script(self, button, script):
        interpreter = '/bin/python3' if '.py' in script else '/bin/bash'
        self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, None, [interpreter, script], None, GLib.SpawnFlags.DEFAULT, None,None,-1, None, None)

    def run_help(self, button, script):
        if '.py' in script: interpreter = '/bin/python3'
        else: interpreter = '/bin/bash'
        help_arg = '-h'
        self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, None, [interpreter, script, help_arg], None, GLib.SpawnFlags.DEFAULT, None,None,-1, None, None)

    def on_tab_switched(self, notebook, page, position):
        if position == 3:
            self.docs_web_view.load_uri(utils.DOCS_URL)
        elif position == 1:
            self.update_scripts_list()

    def show_about_dialog(self, button):
        dialog = Gtk.AboutDialog()
        dialog.props.program_name = 'Waydroid Settings'
        dialog.props.version = "0.3.0"
        dialog.props.authors = ['Axel358', 'Jon West']
        dialog.props.copyright = 'GPL-3'
        dialog.props.logo_icon_name = self.APP_ID
        dialog.props.comments = 'Control Waydroid settings'
        dialog.props.website = utils.HOME_URL
        dialog.set_transient_for(self.window)
        dialog.show()


if __name__ == "__main__":
    app = WaydroidSettings()
    app.run(sys.argv)
