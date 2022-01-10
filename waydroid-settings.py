#!/bin/python
import sys
import gi
import utils
import glob
import os
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, WebKit2, GLib


class WaydroidSettings(Gtk.Application):
    def __init__(self, *args, **kargs):
        super().__init__(*args, application_id='cu.axel.waydroidsettings', **kargs)

        self.builder = Gtk.Builder.new_from_file('window.ui')
        self.window = None

        docs_web_view_box = self.builder.get_object('docs_web_view_box')
        self.docs_web_view = WebKit2.WebView()
        docs_web_view_box.pack_start(self.docs_web_view, True, True, 0)

        self.scripts_list_box = self.builder.get_object('scripts_list_box')

        free_form_switch = self.builder.get_object('free_form_switch')
        print("PROP_FREE_FORM: " + utils.get_prop(utils.PROP_FREE_FORM))
        if utils.get_prop(utils.PROP_FREE_FORM) == 'true':
            free_form_switch.set_state(True)

        color_invert_switch = self.builder.get_object('color_invert_switch')
        print("PROP_INVERT_COLORS: " + utils.get_prop(utils.PROP_INVERT_COLORS))
        if utils.get_prop(utils.PROP_INVERT_COLORS) == 'true':
            color_invert_switch.set_state(True)

        suspend_switch = self.builder.get_object('suspend_switch')
        print("PROP_SUSPEND_INACTIVE: " +
              utils.get_prop(utils.PROP_SUSPEND_INACTIVE))
        if utils.get_prop(utils.PROP_SUSPEND_INACTIVE) == 'true':
            suspend_switch.set_state(True)

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

    def do_activate(self):
        if not self.window:
            self.window = self.builder.get_object('main_window')
            self.window.set_application(self)

        self.window.show_all()

    def toggle_free_form(self, switch, checked):
        if checked:
            utils.set_prop(utils.PROP_FREE_FORM, 'true')
        else:
            utils.set_prop(utils.PROP_FREE_FORM, 'false')

    def toggle_suspend(self, switch, checked):
        if checked:
            utils.set_prop(utils.PROP_SUSPEND_INACTIVE, 'true')
        else:
            utils.set_prop(utils.PROP_SUSPEND_INACTIVE, 'false')

    def toggle_color_inversion(self, switch, checked):
        if checked:
            utils.set_prop(utils.PROP_INVERT_COLORS, 'true')
        else:
            utils.set_prop(utils.PROP_INVERT_COLORS, 'false')

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
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(app_list:= apps_entry.get_text()) > 0:
                utils.set_prop(utils.PROP_BLACKLISTED_APPS, app_list)

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
        print(current_app_list)
        apps_entry.set_text(current_app_list)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(app_list:= apps_entry.get_text()) > 0:
                str_apps_list = '"'+str(apps_entry.get_text().rstrip())+'"'
                utils.set_prop(utils.PROP_ACTIVE_APPS, str_apps_list)

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
                'gtk-dialog-question', Gtk.IconSize.BUTTON)
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
