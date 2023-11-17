import contextlib
import plistlib
import rumps
from infer import run_latex_ocr
from vision import run_vision_ocr
from AppKit import NSPasteboard, NSStringPboardType, NSPasteboardTypePNG, NSApplication, NSApplicationActivationPolicyProhibited, NSEvent
from Quartz import kCGEventFlagMaskCommand, kCGEventFlagMaskShift
from Foundation import NSNotificationCenter
import subprocess
import Quartz
from Quartz import kCGSessionEventTap, kCGHeadInsertEventTap, kCGEventTapOptionListenOnly
import Cocoa

APP_NAME = "Latex OCR"
CONFIG_FILE = f"{APP_NAME}.plist"

class OCRMenuBarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(OCRMenuBarApp, self).__init__(*args, **kwargs)
        self.use_latex_ocr = rumps.MenuItem("Use LaTeX OCR", self.toggle) # A flag to toggle between OCR methods
        self.menu = [self.use_latex_ocr]
        # self.quit_app = rumps.MenuItem(f"Quit {APP_NAME}", self.quit)
        self.load_config()
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyProhibited)

    @rumps.clicked("Run OCR")
    def run_ocr(self, sender):
        # Use screencapture CLI tool to capture a selected area and store it in the clipboard
        subprocess.run(["/usr/sbin/screencapture", "-i", "-c"])

        # Access the general pasteboard
        pasteboard = NSPasteboard.generalPasteboard()
        # Get the first item from the pasteboard
        pasteboard_item = pasteboard.pasteboardItems()[0] if pasteboard.pasteboardItems() else None
        if not pasteboard_item:
            # print("Error: No item in the pasteboard")
            return None

        # Get the data for the first available type from the pasteboard item
        data = pasteboard_item.dataForType_(NSPasteboardTypePNG) # pasteboard_item.types()[0])
        if not data:
            # print("Error: No image data found in the pasteboard")
            return None

        if not self.use_latex_ocr.state:
            text = run_vision_ocr(data)
        else:
            text = run_latex_ocr(data)  # `input_data` needs to be provided
        pasteboard.declareTypes_owner_([NSStringPboardType], None)  # Declare the type of data
        pasteboard.setString_forType_(text, NSStringPboardType)  # Set the string on the pasteboard

    def toggle(self, sender):
        """Toggle sender state."""
        sender.state = not sender.state
        # print("Set {} to {}".format(sender.title, sender.state))
        self.save_config()

    def load_config(self):
        self.config = {}
        with contextlib.suppress(FileNotFoundError):
            with self.open(CONFIG_FILE, "rb") as f:
                with contextlib.suppress(Exception):
                    # don't crash if config file is malformed
                    self.config = plistlib.load(f)
        if not self.config:
            self.config = {
                "use_latex_ocr": True,
            }
        
        self.use_latex_ocr.state = self.config.get("use_latex_ocr", True)
        self.save_config()

    def save_config(self):
        self.config["use_latex_ocr"] = self.use_latex_ocr.state
        with self.open(CONFIG_FILE, "wb+") as f:
            plistlib.dump(self.config, f)

    def quit(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        rumps.quit_application()

    def keyboardTapCallback(self, proxy, type_, event, refcon):
        # Get the event flags and key code from the CGEvent
        flags = Quartz.CGEventGetFlags(event)
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        desired_keycode = 19 # NSString.characterWithString_("2").characterAtIndex_(0)
        desired_flags = kCGEventFlagMaskCommand | kCGEventFlagMaskShift
        if keycode == desired_keycode and (flags & desired_flags) == desired_flags:
            self.run_ocr(None)

    def register_hotkey(self):
        tap = Quartz.CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionListenOnly,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp),
            self.keyboardTapCallback,
            None
        )

        runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)

        Quartz.CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(),
            runLoopSource,
            Quartz.kCFRunLoopDefaultMode
        )

        Quartz.CGEventTapEnable(tap, True)

    def check_accessibility_permissions():
        options = {Cocoa.kAXTrustedCheckOptionPrompt: True}
        trusted = Cocoa.AXIsProcessTrustedWithOptions(options)
        # if not trusted:
        #     print("The app does not have accessibility permissions. Please grant permissions in System Preferences.")
        return trusted

if __name__ == "__main__":
    app = OCRMenuBarApp(name=APP_NAME)
    app.register_hotkey()
    app.run()