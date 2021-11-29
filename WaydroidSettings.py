import sys
import gi
import Utils
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class WaydroidSettings(Gtk.Application):
    def __init__(self, *args, **kargs):
        super().__init__(*args, application_id='cu.axel.waydroidsettings', **kargs)

        self.builder = Gtk.Builder.new_from_file('MainWindow.glade')
        self.window = None
        self.free_form_switch = self.builder.get_object('free_form_switch')

        if Utils.get_prop('persist.waydroid.multiwindows') == 'true':
            self.free_form_switch.set_state(True)

        self.builder.connect_signals(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self.window:
            self.window = self.builder.get_object('main_window')
            self.window.set_application(self)

        self.window.show_all()

    def toggle_free_form(self, switch, checked):
        if checked:
            Utils.set_prop('persist.waydroid.multiwindows', 'true')
        else:
            Utils.set_prop('persist.waydroid.multiwindows', 'false')


if __name__ == "__main__":
    app = WaydroidSettings()
    app.run(sys.argv)
