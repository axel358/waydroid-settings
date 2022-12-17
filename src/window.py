# window.py
#
# Copyright 2022 Axel358
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
import os
import glob
from .utils import Utils
import time

gi.require_version('Vte', '3.91')
gi.require_version('Adw', '1')
gi.require_version('WebKit2', '5.0')
from gi.repository import Gtk, Gdk, GLib, Vte, Adw, WebKit2


@Gtk.Template(resource_path='/cu/axel/waydroidsettings/window.ui')
class WaydroidsettingsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WaydroidsettingsWindow'

    terminal_box = Gtk.Template.Child()
    scripts_list = Gtk.Template.Child()
    web_box = Gtk.Template.Child()
    free_form_switch = Gtk.Template.Child()
    color_invert_switch = Gtk.Template.Child()
    suspend_switch = Gtk.Template.Child()
    nav_btns_switch = Gtk.Template.Child()
    soft_kb_switch = Gtk.Template.Child()
    settings_page = Gtk.Template.Child()
    session_bar = Gtk.Template.Child()
    container_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.terminal = Vte.Terminal()
        self.terminal_box.set_child(self.terminal)
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
        self.terminal.set_input_enabled(True)
        self.terminal.set_scroll_on_output(True)
        self.utils = Utils()
        web_view = WebKit2.WebView()
        self.web_box.set_child(web_view)
        web_view.load_uri('https://google.com')

        #Load values
        self.update_status()

        self.free_form_switch.connect('state-set', self.toggle_free_form)
        self.color_invert_switch.connect('state-set',
                                         self.toggle_color_inversion)
        self.suspend_switch.connect('state-set', self.toggle_suspend)
        self.nav_btns_switch.connect('state-set', self.toggle_navbar)
        self.soft_kb_switch.connect('state-set', self.toggle_keyboard)

        self.update_scripts_list()

    def update_scripts_list(self):
        scripts = glob.glob(
            self.utils.SCRIPTS_DIR + '/**/*.sh', recursive=True) + glob.glob(
                self.utils.SCRIPTS_DIR + '/**/*.py', recursive=True)

        for script in scripts:
            row = Adw.ActionRow()
            row.set_icon_name('scripts-symbolic')
            row.set_title(os.path.basename(script))
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            box.add_css_class('linked')
            run_button = Gtk.Button().new_from_icon_name('run-symbolic')
            run_button.connect('clicked', self.run_script, script)
            info_button = Gtk.Button().new_from_icon_name('info-symbolic')
            box.append(run_button)
            box.append(info_button)
            box.set_valign(Gtk.Align.CENTER)
            row.add_suffix(box)
            self.scripts_list.append(row)

    def run_script(self, button, script):
        if '.py' in script: interpreter = '/bin/python3'
        else: interpreter = '/bin/bash'
        self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, None,
                                  [interpreter, script], None,
                                  GLib.SpawnFlags.DEFAULT, None, None, -1,
                                  None, None)

    def toggle_free_form(self, switch, checked):
        if checked:
            self.utils.enable_freeform_override()
        else:
            self.utils.disable_freeform_override()

    def toggle_suspend(self, switch, checked):
        self.utils.set_prop(self.utils.PROP_SUSPEND_INACTIVE,
                            str(checked).lower())

    def toggle_navbar(self, switch, checked):
        if checked == True:
            self.utils.disable_navbar()
        else:
            self.utils.enable_navbar()

    def toggle_keyboard(self, switch, checked):
        if checked:
            self.utils.disable_kb()
        else:
            self.utils.enable_kb()

    def toggle_color_inversion(self, switch, checked):
        self.utils.set_prop(self.utils.PROP_INVERT_COLORS,
                            str(checked).lower())

    def update_status(self):
        self.updating = True
        if not self.utils.is_container_active():
            self.container_bar.set_revealed(True)
        else:
            self.container_bar.set_revealed(False)
            if self.utils.is_waydroid_running():
                self.session_bar.set_revealed(False)
                self.free_form_switch.set_active(
                    self.utils.search_base_prop(
                        'persist.waydroid.multi_windows=true'))
                self.color_invert_switch.set_active(
                    self.utils.get_prop(self.utils.PROP_INVERT_COLORS) ==
                    'true')
                self.suspend_switch.set_active(
                    self.utils.get_prop(self.utils.PROP_SUSPEND_INACTIVE) ==
                    'true')
                self.nav_btns_switch.set_active(
                    self.utils.search_base_prop('qemu.hw.mainkeys=1'))
                self.soft_kb_switch.set_active(self.utils.is_kb_disabled())
            else:
                self.session_bar.set_revealed(True)
        self.updating = False

    @Gtk.Template.Callback()
    def show_ff_dialog(self, button):
        dialog = Adw.MessageDialog.new(
            self, 'Excluded apps', 'Space separated package names to exclude')
        apps_entry = Gtk.Entry()
        dialog.set_extra_child(apps_entry)
        dialog.connect('response', self.on_ff_dialog_response)
        current_app_list = self.utils.get_prop(
            self.utils.PROP_BLACKLISTED_APPS)
        apps_entry.set_text(current_app_list)
        dialog.add_response("cancel", _("_Cancel"))
        dialog.add_response("ok", _("_Ok"))
        dialog.present()

    def on_ff_dialog_response(self, dialog, response):
        if response == 'ok':
            if len(app_list := apps_entry.get_text()) > 0:
                str_apps_list = '"' + str(apps_entry.get_text().rstrip()) + '"'
                self.utils.set_prop(self.utils.PROP_BLACKLISTED_APPS,
                                    str_apps_list)

    @Gtk.Template.Callback()
    def show_force_w_dialog(self, button):
        dialog = Adw.MessageDialog.new(
            self, 'Included apps', 'Space separated package names to exclude')
        apps_entry = Gtk.Entry()
        dialog.set_extra_child(apps_entry)
        current_app_list = self.utils.get_prop(self.utils.PROP_ACTIVE_APPS)
        apps_entry.set_text(current_app_list)
        dialog.add_response("cancel", _("_Cancel"))
        dialog.add_response("ok", _("_Ok"))
        dialog.connect('response', self.on_force_w_dialog_response)
        dialog.present()

    def on_force_w_dialog_response(self, dialog, response):
        if response == 'ok':
            if len(app_list := apps_entry.get_text()) > 0:
                str_apps_list = '"' + str(apps_entry.get_text().rstrip()) + '"'
                self.utils.set_prop(self.utils.PROP_ACTIVE_APPS, str_apps_list)

    def show_not_available_dialog(self):
        dialog = Adw.MessageDialog.new(
            self, 'Waydroid session not running',
            'Waydroid is either not installed or currently not running. Please start the session using the option at the bottom of the next screen. '
        )
        dialog.add_response("ok", _("_Ok"))
        dialog.present()

    def show_container_dialog(self):
        dialog = Adw.MessageDialog.new(
            self, 'Waydroid container not running',
            'Waydroid container service is currently not running or waydroid is not installed properly. Please start the service using the option at the bottom of the next screen. '
        )
        dialog.add_response("ok", _("_Ok"))
        dialog.present()

    @Gtk.Template.Callback()
    def show_resize_dialog(self, button):

        dialog = Adw.MessageDialog.new(
            self, 'Resize system image',
            'Current image size: ' + str(self.utils.get_image_size()))
        size_entry = Gtk.Entry()
        dialog.set_extra_child(size_entry)
        size_entry.set_text('')
        dialog.add_response("cancel", _("_Cancel"))
        dialog.add_response("ok", _("_Ok"))
        dialog.connect('response', self.on_show_resize_dialog_response)
        dialog.present()

    def on_show_resize_dialog_response(self, dialog, response):
        if response == 'ok':
            self.utils.resize_image(image_size_entry.get_text())

    @Gtk.Template.Callback()
    def show_wipe_dialog(self, button):
        dialog = Adw.MessageDialog.new(
            self, 'Wipe all data',
            'Wipe all Waydroid data? This cannot be undone')
        dialog.add_response("cancel", _("_Cancel"))
        dialog.add_response("ok", _("_Ok"))
        dialog.connect('response', self.on_wipe_dialog_response)
        dialog.present()

    def on_wipe_dialog_response(self, dialog, response):
        if response == 'ok':
            self.utils.wipe_data()

    @Gtk.Template.Callback()
    def select_apk(self, button):
        dialog = Gtk.FileChooserDialog(transient_for=self,
                                       title='Select apk',
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL, "_Install",
                           Gtk.ResponseType.ACCEPT)
        dialog.connect('response', self.on_select_apk_response)
        dialog.show()

    def on_select_apk_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.utils.install_apk(dialog.get_file().get_path())

        dialog.destroy()

    @Gtk.Template.Callback()
    def show_about(self, event):
        about_window = Adw.AboutWindow(
            transient_for=self,
            application_name='Waydroid Settings',
            application_icon='cu.axel.waydroidsettings',
            version='0.7.0',
            developer_name='Axel358 n Jon West',
            website='https://github.com/axel358/waydroid-settings',
            issue_url='https://github.com/axel358/waydroid-settings/issues',
            developers=['Axel358', 'Jon West'])
        about_window.present()

    @Gtk.Template.Callback()
    def on_click_start_container(self, button):
        self.utils.start_container_service()
        counter = 5
        while not (counter == 0):
            time.sleep(1)
            counter = counter - 1
            if self.utils.is_container_active():
                counter = 0
                self.update_status()

    @Gtk.Template.Callback()
    def on_click_start_session(self, button):
        self.utils.start_session()
        counter = 5
        while not (counter == 0):
            time.sleep(1)
            counter = counter - 1
            if self.utils.is_waydroid_running():
                counter = 0
                self.update_status()

    @Gtk.Template.Callback()
    def on_click_restart_session(self, button):
        self.utils.restart_session()
        self.update_status()

    @Gtk.Template.Callback()
    def on_click_stop_session(self, button):
        self.utils.stop_session()
        self.update_status()

    @Gtk.Template.Callback()
    def on_click_freeze_container(self, button):
        self.utils.freeze_container()
        self.update_status()

    @Gtk.Template.Callback()
    def on_click_unfreeze_container(self, button):
        utils.unfreeze_container()
        self.load_values()
