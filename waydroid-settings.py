#!/bin/python
import sys
import gi
import utils
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import WebKit2


class WaydroidSettings(Gtk.Application):
    def __init__(self, *args, **kargs):
        super().__init__(*args, application_id='cu.axel.waydroidsettings', **kargs)

        self.builder = Gtk.Builder.new_from_file('window.ui')
        self.window = None

        docs_web_view_box = self.builder.get_object('docs_web_view_box')
        self.docs_web_view = WebKit2.WebView()
        docs_web_view_box.pack_start(self.docs_web_view, True, True, 0)

        free_form_switch = self.builder.get_object('free_form_switch')
        print("PROP_FREE_FORM: " + utils.get_prop(utils.PROP_FREE_FORM))
        if utils.get_prop(utils.PROP_FREE_FORM) == 'true':
            free_form_switch.set_state(True)

        color_invert_switch = self.builder.get_object('color_invert_switch')        
        print("PROP_INVERT_COLORS: " + utils.get_prop(utils.PROP_INVERT_COLORS))
        if utils.get_prop(utils.PROP_INVERT_COLORS) == 'true':
            color_invert_switch.set_state(True)

        suspend_switch = self.builder.get_object('suspend_switch') 
        print("PROP_SUSPEND_INACTIVE: " + utils.get_prop(utils.PROP_SUSPEND_INACTIVE))
        if utils.get_prop(utils.PROP_SUSPEND_INACTIVE) == 'true':
            suspend_switch.set_state(True)

        w_width_entry = self.builder.get_object('w_width_entry')
        w_height_entry = self.builder.get_object('w_height_entry')
        wp_width_entry = self.builder.get_object('wp_width_entry')
        wp_height_entry = self.builder.get_object('wp_height_entry')

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
        dialog = Gtk.Dialog(title='Exclude apps', use_header_bar=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.get_content_area().pack_start(Gtk.Label(label='Space separated package names to exclude'), True, True,
                                             10)
        apps_entry = Gtk.Entry()
        dialog.get_content_area().pack_start(apps_entry, True, True, 10)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if len(app_list := apps_entry.get_text()) > 0:
                utils.set_prop(utils.PROP_BLACKLISTED_APPS, app_list)

        dialog.destroy()

    def show_force_w_dialog(self, button):
        pass

    def on_tab_switched(self, notebook, page, position):
        if position == 1:
            self.docs_web_view.load_uri(utils.DOCS_URL)
        elif position == 2:
            self.home_web_view.load_uri(utils.HOME_URL)


if __name__ == "__main__":
    app = WaydroidSettings()
    app.run(sys.argv)
