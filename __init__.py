import os
from cudatext import *

FN_CONFIG = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
SECTION = 'folding'

class Command:
    def __init__(self):
        self.indexes = dict()
        self.h_pfs = []
        self.lexers = ini_read(FN_CONFIG, SECTION, 'lexers', 'Python')

    def folding_panel_init(self):
        self.h_pf = ed.get_prop(PROP_HANDLE_PARENT)
        if self.h_pf not in self.h_pfs:
            self.n_sbf = dlg_proc(self.h_pf, DLG_CTL_ADD, 'statusbar')
            self.h_sbf = dlg_proc(self.h_pf, DLG_CTL_HANDLE, index=self.n_sbf)
            dlg_proc(self.h_pf, DLG_CTL_PROP_SET, index=self.n_sbf, prop={'align':ALIGN_TOP})
            self.ind = statusbar_proc(self.h_sbf, STATUSBAR_ADD_CELL)
            statusbar_proc(self.h_sbf, STATUSBAR_SET_PADDING, index=self.ind, value=4)
            statusbar_proc(self.h_sbf, STATUSBAR_SET_CELL_AUTOSTRETCH, index=self.ind, value=True)
            colors = app_proc(PROC_THEME_UI_DICT_GET, '')
            statusbar_proc(self.h_sbf, STATUSBAR_SET_CELL_COLOR_FONT, index=self.ind, value=colors['EdTextFont']['color'])
            statusbar_proc(self.h_sbf, STATUSBAR_SET_CELL_COLOR_BACK, index=self.ind, value=colors['EdTextBg']['color'])
            self.h_pfs.append(self.h_pf)
            self.indexes[self.h_sbf] = self.ind
        return self.indexes

    def folding_set(self, text = ''):
        h_sbf = self.folding_panel_init()
        for h_sbf_ in h_sbf:
            statusbar_proc(h_sbf_, STATUSBAR_SET_CELL_TEXT, index=h_sbf[h_sbf_], value=text)

    def get_fold_block(self, y):
        res = []
        for fold in ed.folding(FOLDING_GET_LIST):
            f0 = fold[0]
            f1 = fold[1]
            if f0 <= y <= f1 and ((f1 - f0) > 1):
                res.append(f0)
        return res

    def work(self):
        res = self.get_fold_block(ed.get_carets()[0][1])
        text_ = ''
        if res is not None:
            for res_ in res:
                text_ = text_ + ed.get_text_line(res_)[:-1].strip() + ' > '
            self.folding_set(text_[:-3])
        else:
            self.folding_set('')

    def on_caret_slow(self, ed_self):
        lexer = ed_self.get_prop(PROP_LEXER_FILE)
        if ','+lexer+',' in ','+self.lexers+',':
            self.work()

    def on_focus(self, ed_self):
        self.on_caret_slow(ed_self)

    def config(self):
        ini_write(FN_CONFIG, SECTION, 'lexers', self.lexers)
        file_open(FN_CONFIG)
        lines = [ed.get_text_line(i) for i in range(ed.get_line_count())]
        try:
            index = lines.index('['+SECTION+']')
            ed.set_caret(0, index)
        except:
            pass
