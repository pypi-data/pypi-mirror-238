import tkinter as tk

from .. import services


# -------------------
## holds base class for all manual dialog boxes
class DlgBase:  # pylint: disable=too-few-public-methods
    ## constant: width of the dialog box
    width = 850
    ## constant: height of the dialog box
    height = 650
    ## constant: holds font to use for btns and most text and entry widgets
    common_font = ('Aerial', 12)
    ## constant: width of the first column
    col0_width = 10
    ## concstant: width of col 1 and 2
    col12_width = 27

    # -------------------
    ## constructor
    def __init__(self):
        ## main TK window
        self._parent = None

        ## dialog box object
        self._dlg = None
        ## dialog frame
        self._frame = None

        # tester info
        ## the testers name if found in cfg
        self._tester_name = 'unknown'
        ## the tester initials text box
        self._txt_tester_initials = None
        ## the tester name lbl
        self._lbl_tester_name = None

        ## the Next button
        self._btn_next = None

        ## the Message label
        self._lbl_message = None

        ## callback to do additional actions when the initials widget is changed
        self._initials_key_pressed_callback = None

    # -------------------
    ## common first portion of the dlg initialization
    #
    # @param row        the row to use
    # @param title      the dlg title to use
    # @param fn_ensure_initials  the callback function to use when the initials are set/changed
    # @return None
    def _dlg_common_first(self, row, title, fn_ensure_initials):
        services.logger.user(f'display dlg: {title}')
        self._create_dlg(title)

        # disable buttons if initials is empty
        self._initials_key_pressed_callback = fn_ensure_initials

        self._create_tester_info(row)

    # -------------------
    ## common last portion of the dlg initialization
    #
    # @param row        the row to use
    # @param msg        the initial message for the msg textbox
    # @param fn_handle_click     the callback function to use when a click occurs
    # @param fn_ensure_initials  the callback function to use when the initials are set/changed
    # @return None
    def _dlg_common_last(self, row, msg, fn_handle_click, fn_ensure_initials):
        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_next_btn(row, 0, lambda: fn_handle_click('next'))
        self._create_abort_btn(row, 1, lambda: fn_handle_click('abort'))

        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_message_box(row, msg)

        fn_ensure_initials()
        self._set_dlg_location()

    # -------------------
    ## create the TopLevel dialog box
    #
    # @param title   the name of the dlg box
    # @return None
    def _create_dlg(self, title):
        self._dlg = tk.Toplevel(self._parent)

        # temporarily make iconify it (make it invisible)
        self._dlg.withdraw()

        self._dlg.title(title)

        self._dlg.resizable(width=tk.FALSE, height=tk.FALSE)  # remove the max window button
        self._dlg.protocol('WM_DELETE_WINDOW', self._disable_event)

        self._dlg.config(bg='white')
        self._create_frame()

    # -------------------
    ## set the dlg location based on the last position saved, if any.
    # otherwise center the dlg in the current screen
    #
    # @return None
    def _set_dlg_location(self):
        # dlgbox is created, but all content may not be updated yet
        self._parent.update_idletasks()
        self._dlg.update_idletasks()

        # show the window
        self._dlg.deiconify()

        # use last position if non-0, otherwise center it
        if services.status.last_position_saved():
            self._dlg.geometry(f'+{services.status.last_position_x}+{services.status.last_position_y}')
            self._dlg.update_idletasks()
        else:
            # center the window
            self._parent.eval(f'tk::PlaceWindow {str(self._dlg)} center')
            self._dlg.update_idletasks()
            services.status.save_last_position(self._dlg.winfo_x(), self._dlg.winfo_y())

        self._dlg.bind('<Configure>', self._on_move)

    # -------------------
    ## callback when the dlg is moved
    #
    # @param event   the tkinter config event that occurred
    # @return None
    def _on_move(self, event):
        services.status.save_last_position(event.x, event.y)

    # -------------------
    ## used to ignore click events
    #
    # @return None
    def _disable_event(self):
        pass

    # -------------------
    ## create the Frame that holds the grid of buttons, text, etc.
    #
    # @return None
    def _create_frame(self):
        self._frame = tk.Frame(self._dlg, bg='white')
        self._frame.pack(padx=1, pady=5)

    # -------------------
    ## create the tester information: initials and name.
    # the name is retried from the cfg file based on the given initials.
    # there can be 2 or 3 initials only
    #
    # @param row   the row to place these widgets in
    # @return None
    def _create_tester_info(self, row):
        self._create_tester_initials(row, 0)
        self._create_tester_name(row, 1)

    # -------------------
    ## create the tester intials Entry box
    #
    # @param row   the row to place the widget in
    # @param col   the column to place the widget in
    # @return None
    def _create_tester_initials(self, row, col):
        self._txt_tester_initials = tk.Entry(self._frame,
                                             font=self.common_font,
                                             width=self.col0_width,
                                             fg='black', bg='white',
                                             highlightbackground='black', highlightthickness=1
                                             )
        services.logger.user(f'tester initials: "{services.status.last_tester_initials}"')
        self._txt_tester_initials.insert(0, services.status.last_tester_initials)
        self._txt_tester_initials.focus()
        self._txt_tester_initials.bind('<KeyRelease>', self._initials_key_pressed)
        self._txt_tester_initials.grid(row=row, column=col, sticky='W')

    # -------------------
    ## indicates if the tester initials has 2 or 3 characters
    #
    # @return True if 2 or 3 chars, False otherwise
    def _tester_initials_is_wrong(self):
        num = len(services.status.last_tester_initials)
        return num < 2 or num > 3

    # -------------------
    ## create tester name label. Filled based on tester initials and content of cfg file
    #
    # @param row  the row to place it in
    # @param col  the column to place it in
    # @return None
    def _create_tester_name(self, row, col):
        self._get_tester_name()
        self._lbl_tester_name = tk.Label(self._frame,
                                         text=self._tester_name,
                                         font=self.common_font,
                                         width=self.col12_width,
                                         height=1,
                                         bg='white',
                                         highlightbackground='black', highlightthickness=1)
        self._lbl_tester_name.grid(row=row, column=col, sticky='W', columnspan=2)

    # -------------------
    ## handle an entry in the tester intial box
    #
    # @param unused   ignored; the key that was pressed
    # @return None
    # noinspection PyUnusedLocal
    def _initials_key_pressed(self, unused):  # pylint: disable=unused-argument
        services.status.last_tester_initials = self._txt_tester_initials.get().upper().strip()
        self._get_tester_name()
        self._lbl_tester_name.config(text=self._tester_name,
                                     fg='black', bg='white',
                                     width=self.col12_width)

        if self._initials_key_pressed_callback:
            self._initials_key_pressed_callback()  # pylint: disable=not-callable

    # -------------------
    ## translate tester initials into tester name
    #
    # @return None
    def _get_tester_name(self):
        if services.status.last_tester_initials in services.cfg.testers:
            self._tester_name = services.cfg.testers[services.status.last_tester_initials]
        else:
            self._tester_name = 'unknown'
        services.logger.user(f'tester name: "{self._tester_name}"')

    # -------------------
    ## create empty row
    #
    # @param row  the row to place it in
    # @return None
    def _create_empty_row(self, row):
        lbl = tk.Label(self._frame, text='', width=0,
                       highlightbackground='white', highlightthickness=1)
        lbl.grid(row=row, column=0, sticky='W')

    # -------------------
    ## btn that indicates the tester wants to abort the test
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @param fn_handle_click  the callback for handling a click
    # @return None
    def _create_abort_btn(self, row, col, fn_handle_click):
        btn = tk.Button(self._frame, text='Abort', command=fn_handle_click,
                        font=self.common_font,
                        bg='red', fg='white', width=self.col0_width)
        btn.grid(row=row, column=col, sticky='W')

    # -------------------
    ## Create the Next btn. The tester presses
    # it to go to the next protocol step.
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @param fn_handle_click  the callback for handling a click
    # @return None
    def _create_next_btn(self, row, col, fn_handle_click):
        # initially disabled
        self._btn_next = tk.Button(self._frame, text='Next', command=fn_handle_click,
                                   font=self.common_font,
                                   state='disabled',
                                   bg='blue', fg='white', width=self.col0_width)
        self._btn_next.grid(row=row, column=col, sticky='W')

    # -------------------
    ## enable the Next btn
    #
    # @return None
    def _next_enable(self):
        self._btn_next['state'] = 'normal'

    # -------------------
    ## disable the Next btn
    #
    # @return None
    def _next_disable(self):
        self._btn_next['state'] = 'disabled'

    # -------------------
    ## create message box label. Filled with messages to the tester
    #
    # @param row  the row to place it in
    # @param msg  the message to display
    # @return None
    def _create_message_box(self, row, msg):
        self._lbl_message = tk.Label(self._frame,
                                     text=msg,
                                     font=('Aerial', 9),
                                     wraplength=self.width)
        self._set_message('black', 'Press Can\'t do or perform the action and press Done')
        self._lbl_message.grid(row=row, column=0, sticky='W', columnspan=3)

    # -------------------
    ## set the text of the message box
    #
    ## @param color  the color to print the text in
    ## @param text   the text to display
    # @return None
    def _set_message(self, color, text):
        self._lbl_message.config(text=text,
                                 fg=color, bg='white',
                                 width=52,
                                 highlightbackground='black', highlightthickness=2)
