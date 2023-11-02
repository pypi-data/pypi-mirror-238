import tkinter as tk

from .dlg_base import DlgBase
from .. import services


# -------------------
## holds Dialog Box for a Manual Action Step
class DlgManualAction(DlgBase):
    # -------------------
    ## constructor
    def __init__(self):
        super().__init__()

        ## the return state, holds abort, done, or cantdo
        self._return_value = 'initial'
        ## the reason text if state is cantdo, otherwise ''
        self._reason = ''

        # widgets
        ## the Done btn
        self._btn_done = None
        ## the Can't do btn
        self._btn_cantdo = None
        ## the Reason Text widget
        self._txt_reason = None

    # -------------------
    ## show dialog for a manual action
    #
    # @param parent   the tk root window
    # @param title    the dlg title
    # @param action   the action for the tester to perform
    # @return the final state of the dlg (done, cantdo, abort), the reason if state is cantdo, otherwise ''
    def step_manual_action(self, parent, title, action):
        self._parent = parent
        self._show_dlg_manual_action(title, action)
        self._parent.wait_window(self._dlg)
        return self._return_value, self._reason

    # -------------------
    ## show the dlg for performing a manual action
    #
    # @param title   the dlg title
    # @param action  the action for the tester to perform
    # @return None
    def _show_dlg_manual_action(self, title, action):
        row = 0
        self._dlg_common_first(row, title, self._ensure_initials)

        row += 1
        self._create_action_desc(row, action)
        services.logger.user(f'action: {action}')

        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_done_btn(row)

        row += 1
        self._create_cantdo_btn(row, 0)
        self._create_reason(row, 1)

        msg = 'Press Can\'t do or perform the action and press Done'
        self._dlg_common_last(row,
                              msg,
                              self._handle_click,
                              self._ensure_initials)

    # -------------------
    ## the action for the tester to perform
    #
    # @param row          the row to place it in
    # @param action_desc  the tester action needed for the current protocol step
    # @return None
    def _create_action_desc(self, row, action_desc):
        lbl = tk.Label(self._frame,
                       text=action_desc,
                       font=self.common_font,
                       wraplength=self.width,
                       bg='white',
                       highlightbackground='black', highlightthickness=2)
        lbl.grid(row=row, column=0, sticky='W', columnspan=3)

    # -------------------
    ## btn indicates action was done
    #
    # @param row     the row to place it in
    # @return None
    def _create_done_btn(self, row):
        self._btn_done = tk.Button(self._frame, text='Done', command=lambda: self._handle_click('done'),
                                   font=self.common_font,
                                   bg='lightgreen', fg='black', width=self.col0_width,
                                   highlightbackground='white', highlightthickness=4)
        self._btn_done.grid(row=row, column=0, sticky='W')

    # -------------------
    ## disable the Done button
    #
    # @return None
    def _done_disable(self):
        self._btn_done['state'] = 'disabled'

    # -------------------
    ## enable the Done button
    #
    # @return None
    def _done_enable(self):
        self._btn_done['state'] = 'normal'

    # -------------------
    ## place a highlight around the Done btn
    #
    # @return None
    def _done_highlight(self):
        self._btn_done['fg'] = 'black'
        self._btn_done['highlightbackground'] = 'black'
        self._btn_done['highlightthickness'] = 4

    # -------------------
    ## unhighlight the Done btn
    #
    # @return None
    def _done_unhighlight(self):
        self._btn_done['fg'] = 'darkgrey'
        self._btn_done['highlightbackground'] = 'white'
        self._btn_done['highlightthickness'] = 4

    # -------------------
    ## btn that indicates the tester can't do the requested action
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_cantdo_btn(self, row, col):
        self._btn_cantdo = tk.Button(self._frame, text='Can\'t Do', command=lambda: self._handle_click('cantdo'),
                                     font=self.common_font,
                                     bg='gold', fg='black', width=self.col0_width,
                                     highlightbackground='white', highlightthickness=4)
        self._btn_cantdo.grid(row=row, column=col, sticky='W')

    # -------------------
    ## disable the Can't Do button
    #
    # @return None
    def _cantdo_disable(self):
        self._btn_cantdo['state'] = 'disabled'

    # -------------------
    ## enable the Can't Do button
    #
    # @return None
    def _cantdo_enable(self):
        self._btn_cantdo['state'] = 'normal'

    # -------------------
    ## highlight the Can't Do btn
    #
    # @return None
    def _cando_highlight(self):
        self._btn_cantdo['fg'] = 'black'
        self._btn_cantdo['highlightbackground'] = 'black'
        self._btn_cantdo['highlightthickness'] = 4

    # -------------------
    ## unhighlight the Can't Do button
    #
    # @return None
    def _cantdo_unhighlight(self):
        self._btn_cantdo['fg'] = 'darkgrey'
        self._btn_cantdo['highlightbackground'] = 'white'
        self._btn_cantdo['highlightthickness'] = 4

    # -------------------
    ## Create the Reason text area. The tester fills
    # it in if they can not perform the requested action
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_reason(self, row, col):
        self._txt_reason = tk.Text(self._frame,
                                   font=self.common_font,
                                   state='disabled',
                                   width=self.col12_width,
                                   height=5,  # lines
                                   fg='black', bg='white')
        self._txt_reason.grid(row=row, column=col, sticky='W')

    # -------------------
    ## disable the Reason text box
    #
    # @return None
    def _reason_disable(self):
        self._txt_reason['state'] = 'disabled'
        self._txt_reason['fg'] = 'lightgrey'

    # -------------------
    ## enable the Reason text box
    # note: don't clear out reason text in case the tester wants to extend it
    #
    # @return None
    def _reason_enable(self):
        self._txt_reason['state'] = 'normal'
        self._txt_reason['fg'] = 'black'

    # -------------------
    ## handle a dlg box click
    #
    # @param option  the btn the tester clicked
    # @return None
    def _handle_click(self, option):
        if option == 'done':
            services.logger.user('click Done')
            self._reason_disable()
            self._cantdo_unhighlight()
            self._done_highlight()
            self._next_enable()
            self._return_value = 'done'
            # tester must press Next to move on
            self._set_message('green', 'Done selected. Press Next')

        elif option == 'cantdo':
            services.logger.user('click Can\t Do')
            self._reason_enable()
            self._cando_highlight()
            self._done_unhighlight()
            self._next_enable()
            self._return_value = 'cantdo'
            # tester must press Next to move on
            self._set_message('green', 'Can\'t Do selected. Enter a reason and then press Next')

        elif option == 'next':
            # get the reason text
            self._reason = self._txt_reason.get('1.0', 'end')
            self._reason = self._reason.strip()
            services.logger.user(f'reason: {self._reason}')
            services.logger.user('click Next')

            if self._return_value == 'done':
                # if the action was successfully done, then no reason text needed
                self._reason = ''

            if self._return_value == 'cantdo' and self._reason == '':
                self._set_message('red', 'Enter a reason for the failure')
            else:
                self._dlg.destroy()

        elif option == 'abort':
            services.logger.user(f'reason: {self._reason}')
            services.logger.user('click Abort')
            self._return_value = 'abort'
            self._dlg.destroy()

    # -------------------
    ## disable buttons (except abort) if initials box is empty
    #
    # @return None
    def _ensure_initials(self):
        if self._tester_initials_is_wrong():
            self._reason_disable()
            self._done_disable()
            self._cantdo_disable()
            self._next_disable()
            self._set_message('red', 'Enter your initials (2 or 3 characters)')
        else:
            self._reason_enable()
            self._done_enable()
            self._cantdo_enable()
            self._next_enable()
            self._set_message('green', 'Press Can\'t do or perform the action and press Done')
