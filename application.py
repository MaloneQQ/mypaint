import gtk, os
import drawwindow, brushsettingswindow, brushselectionwindow
import colorselectionwindow, functionwindow
import brush

class Application: # singleton
    def __init__(self):
        self.confpath = os.getenv('HOME') + '/.mypaint/'
        if not os.path.isdir(self.confpath): os.mkdir(self.confpath)
        self.brushpath = self.confpath + 'brushes/'
        if not os.path.isdir(self.brushpath): os.mkdir(self.brushpath)

        self.brush = brush.Brush()
        self.brushes = []
        self.selected_brush = None
        self.brush_selected_callbacks = [self.brush_selected_cb]
        self.contexts = []
        for i in range(10):
            c = brush.Brush()
            c.name = 'context%02d' % i
            self.contexts.append(c)
        self.selected_context = None

        # load brushes
        loadnames = []
        filename = self.confpath + 'brush_order.conf'
        if os.path.isfile(filename):
            for line in open(filename).readlines():
                # FIXME: security problem?
                loadnames.append(line.strip())
        for filename in os.listdir(self.brushpath):
            if filename.endswith('.myb'):
                loadnames.append(filename[:-4])
        for name in loadnames:
            filename = self.brushpath + name + '.myb'
            if not os.path.isfile(filename):
                print 'ignoring non-existing brush:', filename
                continue
            # load brushes from disk
            b = brush.Brush()
            b.load(self.brushpath, name)
            if name.startswith('context'):
                i = int(name[-2:])
                assert i >= 0 and i < 10 # 10 for now...
                self.contexts[i] = b
            else:
                self.brushes.append(b)

        self.image_windows = []

        self.new_image_window()

        self.brushsettings_window = brushsettingswindow.Window(self)
        self.brushsettings_window.show_all()

        self.function_window = functionwindow.Window(self)
        self.function_window.show_all()

        self.brushselection_window = brushselectionwindow.Window(self)
        self.brushselection_window.show_all()

        self.colorselectionwindow = colorselectionwindow.Window(self)
        self.colorselectionwindow.show_all()

        gtk.accel_map_load(self.confpath + 'accelmap.conf')

    def brush_selected_cb(self, brush):
        "actually set the new brush"
        assert brush is not self.brush
        if brush in self.brushes:
            self.selected_brush = brush
        else:
            #print 'Warning, you have selected a brush not in the list.'
            # TODO: maybe find out parent and set this as selected_brush
            self.selected_brush = None
        if brush is not None:
            self.brush.copy_settings_from(brush)

    def select_brush(self, brush):
        for callback in self.brush_selected_callbacks:
            callback(brush)

    def quit(self):
        print 'save'
        gtk.accel_map_save(self.confpath + 'accelmap.conf')
        gtk.main_quit()
        
    def new_image_window(self):
        w = drawwindow.Window(self)
        w.show_all()
        self.image_windows.append(w)
        return w


