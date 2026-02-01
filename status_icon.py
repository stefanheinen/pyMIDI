from logging import info

from AppKit import NSApp, NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSControlStateValueOn, NSControlStateValueOff, NSImage
import objc

import launchAgent


class StatusIconEvent():
    def __init__(self, event: str, parameters: list = []):
        self.event = event
        self.parameters = parameters

    def __str__(self):
        return f"{self.event}: {self.parameters}"


class App:
    def __init__(self, status_queue):
        self.status_queue = status_queue

        # Status bar item
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.button().setTitle_("􁓺")

        self._updateMenu(launchAgent.get_activated_status(), {})

    def _updateMenu(self, autostart_status, devices_states):
        menu = self._createMenu(autostart_status, devices_states)
        self.status_item.setMenu_(menu)

    def updateDeviceMenu(self, devices_states):
        self._updateMenu(launchAgent.get_activated_status(), devices_states)

    def _createMenu(self, autostart_status: bool, devices_states):
        # Main menu
        menu = NSMenu()

        # Autostart menu item
        if autostart_status:
            state = NSControlStateValueOn
        else:
            state = NSControlStateValueOff
        self.toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Autostart", "toggleAutostart:", ""
        )
        self.toggle_item.setTarget_(self)
        self.toggle_item.setState_(state)
        menu.addItem_(self.toggle_item)

        menu.addItem_(NSMenuItem.separatorItem())

        for mi in self._createDeviceMenu(devices_states):
            menu.addItem_(mi)

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "quitApp:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)

        return menu

    def _createDeviceMenu(self, devices_states):
        device_menus = []

        for state in devices_states:
            dropdown_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(f"{state[1]}: {state[2]}", None, "")

            if state[3] == "ready":
                image = NSImage.imageWithSystemSymbolName_accessibilityDescription_("cable.connector.horizontal", None)
                dropdown_item.setImage_(image)
            elif state[3] == "connected":
                image = NSImage.imageWithSystemSymbolName_accessibilityDescription_("progress.indicator", None)
                dropdown_item.setImage_(image)

            # Submenu
            submenu = NSMenu()
            for eventToAppMap in state[4]:
                item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(eventToAppMap[0], "selectOption:", "")
                item.setTarget_(self)  # target must be an object that has selectOption_ method
                item.setRepresentedObject_(state[0])

                if eventToAppMap[1]:
                    image = NSImage.imageWithSystemSymbolName_accessibilityDescription_("arrowshape.forward.circle",
                                                                                        None)
                    item.setImage_(image)
                submenu.addItem_(item)

            # Parent menu item
            dropdown_item.setSubmenu_(submenu)
            device_menus.append(dropdown_item)
        return device_menus

    def toggleAutostart_(self, sender):
        if sender.state() == NSControlStateValueOn:
            sender.setState_(NSControlStateValueOff)
            launchAgent.deactivate()
            info("Autostart disabled")
        else:
            sender.setState_(NSControlStateValueOn)
            launchAgent.activate()
            info("Autostart enabled")

    # This method is called when a submenu item is clicked
    @objc.python_method
    def selectOption_(self, sender):
        device_id = sender.representedObject()
        self.status_queue.put(StatusIconEvent("DEVICEMAPSELECT", [device_id, sender.title()]))

    # This method will be called when Quit is clicked
    def quitApp_(self, sender):
        def exitCallback():
            NSApp.terminate_(self)

        self.status_queue.put(StatusIconEvent("EXIT", [exitCallback]))

