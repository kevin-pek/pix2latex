from Cocoa import NSObject
from Quartz import Carbon

class HotkeyHandler(NSObject):
    def handle_hotkey_event(self, event):
        pass

def register_hotkey(self, keycode, modifiers):
    eventHandler = HotkeyHandler.alloc().init()
    eventSpec = Carbon.CarbonEvents.EventHotKeyID(1, keycode, modifiers)
    eventType = Carbon.CarbonEvents.kEventHotKeyPressed

    eventHotKeyRef = Carbon.CarbonEvents.InstallEventHandler(
        Carbon.CarbonEvents.GetApplicationEventTarget(), 
        eventHandler.handleHotkeyEvent_, 
        1, 
        [eventType], 
        eventSpec, 
        None
    )

    Carbon.CarbonEvents.RegisterEventHotKey(
        keycode, 
        modifiers, 
        eventSpec, 
        Carbon.CarbonEvents.GetApplicationEventTarget(), 
        0, 
        Carbon.Ptr(eventHotKeyRef)
    )