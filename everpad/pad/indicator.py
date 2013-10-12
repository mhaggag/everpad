import sys
sys.path.insert(0, '../..')
from PySide.QtCore import Slot, QTranslator, QLocale, Signal, QSettings, QT_TRANSLATE_NOOP
from PySide.QtGui import QApplication, QSystemTrayIcon, QMenu, QCursor
from PySide.QtNetwork import QNetworkProxyFactory
from everpad.basetypes import Note, NONE_ID, NONE_VAL
from everpad.tools import get_provider, get_pad, get_auth_token, print_version
from everpad.pad.editor import Editor
from everpad.pad.management import Management
from everpad.pad.list import List
from everpad.const import (
    STATUS_SYNC, SYNC_STATES, SYNC_STATE_START,
    SYNC_STATE_FINISH, API_VERSION,
)
from everpad.specific import get_launcher, get_tray_icon
from functools import partial
from datetime import datetime
import signal
import dbus
import dbus.service
import dbus.mainloop.glib
import argparse
import fcntl
import os
import getpass


class Indicator(QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        QSystemTrayIcon.__init__(self, *args, **kwargs)
        self.app = QApplication.instance()
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.menu.aboutToShow.connect(self.update)
        self.opened_notes = {}
        self.activated.connect(self._activated)

    def _activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.menu.popup(QCursor().pos())

    def _add_note(self, struct):
        note = Note.from_tuple(struct)
        title = note.title[:40].replace('&', '&&')
        self.menu.addAction(title, Slot()(
            partial(self.open, note=note)
        ))

    @Slot()
    def update(self):
        self.menu.clear()
        try:
            version = self.app.provider.get_api_version()
        except (  # dbus raise some magic
            dbus.exceptions.UnknownMethodException,
            dbus.exceptions.DBusException,
        ):
            version = -1
        if version != API_VERSION:
            action = self.menu.addAction(
                self.tr('API version missmatch, please restart'),
            )
            action.setEnabled(False)
            if version < API_VERSION:
                handler = self.app.provider.kill
            else:
                handler = partial(os.execlp, 'everpad', '--replace')
            self.menu.addAction(
                self.tr('Restart everpad'), handler,
            )
            return
        if get_auth_token():
            pin_notes = self.app.provider.find_notes(
                '', dbus.Array([], signature='i'),
                dbus.Array([], signature='i'), 0,
                20, Note.ORDER_UPDATED_DESC, 1,
            )
            notes = self.app.provider.find_notes(
                '', dbus.Array([], signature='i'),
                dbus.Array([], signature='i'), 0,
                20 - len(pin_notes), Note.ORDER_UPDATED_DESC, 0,
            )
            if len(notes) + len(pin_notes) or self.app.provider.is_first_synced():
                self.menu.addAction(self.tr('All Notes'), self.show_all_notes)
                self.menu.addSeparator()
                if len(pin_notes):
                    for struct in pin_notes:
                        self._add_note(struct)
                    self.menu.addSeparator()
                for struct in notes:
                    self._add_note(struct)
                self.menu.addSeparator()
                self.menu.addAction(self.tr('Create Note'), self.create)
                first_sync = False
            else:
                first_sync = True
            if self.app.provider.get_status() == STATUS_SYNC:
                action = self.menu.addAction(
                    self.tr('Wait, first sync in progress') if first_sync
                    else self.tr('Sync in progress')
                )
                action.setEnabled(False)
            else:
                if first_sync:
                    label = self.tr('Please perform first sync')
                else:
                    last_sync = self.app.provider.get_last_sync()
                    delta_sync = (
                        datetime.now() - datetime.strptime(last_sync, '%H:%M')
                    ).seconds // 60
                    if delta_sync == 0:
                        label = self.tr('Last Sync: Just now')
                    elif delta_sync == 1:
                        label = self.tr('Last Sync: 1 min ago')
                    else:
                        label = self.tr('Last Sync: %s mins ago') % delta_sync
                self.menu.addAction(label, Slot()(self.app.provider.sync))
        self.menu.addAction(self.tr('Settings and Management'), self.show_management)
        self.menu.addSeparator()
        self.menu.addAction(self.tr('Exit'), self.exit)

    def open(self, note, search_term=''):
        old_note_window = self.opened_notes.get(note.id, None)
        if old_note_window and not getattr(old_note_window, 'closed', True):
            editor = self.opened_notes[note.id]
            editor.activateWindow()
        else:
            editor = Editor(note)
            editor.show()
            self.opened_notes[note.id] = editor
        if search_term:
            editor.findbar.set_search_term(search_term)
            editor.findbar.show()
        return editor

    @Slot()
    def create(self, attach=None, notebook_id=NONE_ID):
        note_struct = Note(  # maybe replace NONE's to somthing better
            id=NONE_ID,
            title=self.tr('New note'),
            content=self.tr("New note content"),
            tags=dbus.Array([], signature='i'),
            notebook=notebook_id,
            created=NONE_VAL,
            updated=NONE_VAL,
            conflict_parent=NONE_VAL,
            conflict_items=dbus.Array([], signature='i'),
            place='',
        ).struct
        note = Note.from_tuple(
            self.app.provider.create_note(note_struct),
        )
        editor = self.open(note)
        if attach:
            editor.resource_edit.add_attach(attach)

    @Slot()
    def show_all_notes(self):
        if not hasattr(self, 'list') or getattr(self.list, 'closed', True):
            self.list = List()
            self.list.show()
        else:
            self.list.activateWindow()

    @Slot()
    def show_management(self):
        if not hasattr(self, 'management') or getattr(self.management, 'closed', True):
            self.management = Management()
            self.management.show()
        else:
            self.management.activateWindow()

    @Slot()
    def exit(self):
        self.app.quit()


class PadApp(QApplication):
    data_changed = Signal()

    def __init__(self, *args, **kwargs):
        QApplication.__init__(self, *args, **kwargs)
        self.settings = QSettings('everpad', 'everpad-pad')
        self.translator = QTranslator()
        if not self.translator.load('../../i18n/%s' % QLocale.system().name()):
            self.translator.load('/usr/share/everpad/i18n/%s' % QLocale.system().name())
        # This application string can be localized to 'RTL' to switch the application layout
        # direction. See for example i18n/ar_EG.ts
        QT_TRANSLATE_NOOP('QApplication', 'QT_LAYOUT_DIRECTION')
        self.installTranslator(self.translator)
        QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.indicator = Indicator()
        self.update_icon()
        self.indicator.show()

    def update_icon(self):
        is_black = int(self.settings.value('black-icon', 0))
        self.icon = get_tray_icon(is_black)
        self.indicator.setIcon(self.icon)

    def send_notify(self, text):
        self.indicator.showMessage('Everpad', text,
            QSystemTrayIcon.Information)

    def on_sync_state_changed(self, state):
        if int(self.settings.value('launcher-progress', 1)):
            self.launcher.update({
                'progress': float(state + 1) / len(SYNC_STATES),
                'progress-visible': state not in (SYNC_STATE_START, SYNC_STATE_FINISH),
            })

    def on_data_changed(self):
        """Note, notebook or tag changed"""
        self.data_changed.emit()


class EverpadService(dbus.service.Object):
    def __init__(self, *args, **kwargs):
        self.app = QApplication.instance()
        dbus.service.Object.__init__(self, *args, **kwargs)

    @dbus.service.method("com.everpad.App", in_signature='i', out_signature='')
    def open(self, id):
        self.open_with_search_term(id, '')

    @dbus.service.method("com.everpad.App", in_signature='is', out_signature='')
    def open_with_search_term(self, id, search_term):
        note = Note.from_tuple(self.app.provider.get_note(id))
        self.app.indicator.open(note, search_term)

    @dbus.service.method("com.everpad.App", in_signature='', out_signature='')
    def create(self):
        self.app.indicator.create()

    @dbus.service.method("com.everpad.App", in_signature='s', out_signature='')
    def create_wit_attach(self, name):
        self.app.indicator.create(name)

    @dbus.service.method("com.everpad.App", in_signature='', out_signature='')
    def settings(self):
        self.app.indicator.show_management()

    @dbus.service.method("com.everpad.App", in_signature='', out_signature='')
    def all_notes(self):
        self.app.indicator.show_all_notes()

    @dbus.service.method("com.everpad.App", in_signature='', out_signature='')
    def kill(self):
        self.app.quit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    parser = argparse.ArgumentParser()
    parser.add_argument('attach', type=str, nargs='?', help='attach file to new note')
    parser.add_argument('--open', type=int, help='open note')
    parser.add_argument('--create', action='store_true', help='create new note')
    parser.add_argument('--all-notes', action='store_true', help='show all notes window')
    parser.add_argument('--settings', action='store_true', help='settings and management')
    parser.add_argument('--replace', action='store_true', help='replace already runned')
    parser.add_argument('--version', '-v', action='store_true', help='show version')
    args = parser.parse_args(sys.argv[1:])
    if args.version:
        print_version()
    if args.replace:
        try:
            pad = get_pad()
            pad.kill()
        except dbus.exceptions.DBusException:
            pass
    fp = open('/tmp/everpad-%s.lock' % getpass.getuser(), 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        app = PadApp(sys.argv)
        app.setApplicationName('everpad')
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        app.provider = get_provider(session_bus)
        app.provider.connect_to_signal(
            'sync_state_changed',
            app.on_sync_state_changed,
            dbus_interface="com.everpad.provider",
        )
        app.provider.connect_to_signal(
            'data_changed',
            app.on_data_changed,
            dbus_interface="com.everpad.provider",
        )
        app.launcher = get_launcher('application://everpad.desktop', session_bus, '/')
        bus = dbus.service.BusName("com.everpad.App", session_bus)
        service = EverpadService(session_bus, '/EverpadService')
        if args.open:
            app.indicator.open(args.open)
        if args.create:
            app.indicator.create()
        if args.settings:
            app.indicator.show_management()
        if args.attach:
            app.indicator.create(args.attach)
        if args.all_notes:
            app.indicator.show_all_notes()
        app.exec_()
    except IOError:
        pad = get_pad()
        if args.open:
            pad.open(args.open)
        if args.create:
            pad.create()
        if args.settings:
            pad.settings()
        if args.attach:
            pad.create_wit_attach(args.attach)
        if args.all_notes:
            pad.all_notes()
        sys.exit(0)

if __name__ == '__main__':
    main()
