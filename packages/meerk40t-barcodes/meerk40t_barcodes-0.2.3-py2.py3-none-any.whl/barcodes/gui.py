import wx

from .bcode_logic import PROVIDED_BARCODES, update_barcode, update_qr

_ = wx.GetTranslation


class BarcodeDialog(wx.Dialog):

    # from meerk40t.gui.wxutils import TextCtrl

    def __init__(self, context, *args, **kwds):
        self.context = context
        _ = context._
        self.command = ""
        self.PROVIDED_BARCODES = PROVIDED_BARCODES()
        # begin wxGlade: RefAlign.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(_("Create a barcode"))
        mainsizer = wx.BoxSizer(wx.VERTICAL)

        input_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Text to use:")), wx.HORIZONTAL
        )
        self.text_code = wx.TextCtrl(self, wx.ID_ANY)
        self.text_code.SetToolTip(
            _("The barcode/qrcode will be based on this content.")
        )
        label = wx.StaticText(self, wx.ID_ANY, label=_("Code:"))
        input_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        input_sizer.Add(self.text_code, 1, wx.EXPAND, 0)

        xy_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Coordinates:")), wx.HORIZONTAL
        )
        x_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("X:")), wx.HORIZONTAL
        )
        y_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Y:")), wx.HORIZONTAL
        )
        self.text_xpos = wx.TextCtrl(self, wx.ID_ANY, "0cm")
        self.text_xpos.SetToolTip(
            _("Where will the barcode will be located (top left corner).")
        )
        self.text_xpos.SetMaxSize(wx.Size(100, -1))

        x_sizer.Add(self.text_xpos, 1, wx.EXPAND, 0)

        self.text_ypos = wx.TextCtrl(self, wx.ID_ANY, "0cm")
        self.text_ypos.SetToolTip(
            _("Where will the barcode will be located (top left corner).")
        )
        self.text_ypos.SetMaxSize(wx.Size(100, -1))

        y_sizer.Add(self.text_ypos, 1, wx.EXPAND, 0)
        xy_sizer.Add(x_sizer, 1, wx.EXPAND, 0)
        xy_sizer.Add(y_sizer, 1, wx.EXPAND, 0)

        self.option_qr = wx.RadioButton(self, wx.ID_ANY, _("QR-Code"))
        self.option_bar = wx.RadioButton(self, wx.ID_ANY, _("Barcode"))

        codes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        qr_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("QR-Code:")), wx.VERTICAL
        )
        qrnotebook = wx.Notebook(self, wx.ID_ANY)

        # --------------- Option Panel

        qrmain_panel = wx.Panel(qrnotebook, wx.ID_ANY)
        qrnotebook.AddPage(qrmain_panel, _("Options"))
        qroptions_sizer = wx.BoxSizer(wx.VERTICAL)
        qrmain_panel.SetSizer(qroptions_sizer)
        qrdim_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #      --boxsize  (-x)      Boxsize (default 10)
        #  --border   (-b)      Border around qr-code (default 4)
        #  --version  (-v)      size (1..40)
        #  --errcorr  (-e)      error correction, one of L (7%), M (15%), Q (25%), H (30%)
        label = wx.StaticText(qrmain_panel, wx.ID_ANY, label=_("Width/Height:"))
        label.SetMinSize(wx.Size(80, -1))
        self.text_qrdim = wx.TextCtrl(qrmain_panel, wx.ID_ANY, "4cm")
        self.text_qrdim.SetToolTip(_("How wide/high will the resulting qr-code be?"))
        self.text_qrdim.SetMaxSize(wx.Size(100, -1))
        qrdim_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrdim_sizer.Add(self.text_qrdim, 1, wx.EXPAND, 0)

        qrres_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(qrmain_panel, wx.ID_ANY, label=_("Resolution:"))
        label.SetMinSize(wx.Size(80, -1))
        self.text_qrres = wx.TextCtrl(qrmain_panel, wx.ID_ANY, value="1")
        self.text_qrres.SetToolTip(
            _("How big will the qr-code become (1..40, default 1)?")
        )
        self.text_qrres.SetMaxSize(wx.Size(50, -1))
        qrres_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrres_sizer.Add(self.text_qrres, 1, wx.EXPAND, 0)

        # qrborder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # label = wx.StaticText(self, wx.ID_ANY, label=_("Border:"))
        # label.SetMinSize(wx.Size(80, -1))
        # self.text_qrborder = wx.TextCtrl(self, wx.ID_ANY, value="4")
        # self.text_qrborder.SetToolTip(_("How wide is the border around the qr-code (default 4)?"))
        # self.text_qrborder.SetMaxSize(wx.Size(50, -1))
        # qrborder_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # qrborder_sizer.Add(self.text_qrborder, 1, wx.EXPAND, 0)

        qrbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(qrmain_panel, wx.ID_ANY, label=_("Boxsize:"))
        label.SetMinSize(wx.Size(80, -1))
        self.text_qrbox = wx.TextCtrl(qrmain_panel, wx.ID_ANY, value="10")
        self.text_qrbox.SetToolTip(
            _("How big is the boxsize of the pixels (default 10)?")
        )
        self.text_qrbox.SetMaxSize(wx.Size(50, -1))
        qrbox_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrbox_sizer.Add(self.text_qrbox, 1, wx.EXPAND, 0)

        qrerrcorr_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(qrmain_panel, wx.ID_ANY, label=_("Error:"))
        label.SetMinSize(wx.Size(80, -1))
        errchoices = ["L (7%)", "M (15%)", "Q (25%)", "H (30%)"]
        self.combo_errcorr = wx.ComboBox(
            qrmain_panel,
            wx.ID_ANY,
            choices=errchoices,
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )
        self.combo_errcorr.SetToolTip(
            _("Establish the error correction used for the QR Code")
        )
        self.combo_errcorr.SetSelection(1)  # (M)
        qrerrcorr_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrerrcorr_sizer.Add(self.combo_errcorr, 1, wx.EXPAND, 0)

        qroptions_sizer.Add(qrdim_sizer, 0, wx.EXPAND, 0)
        qroptions_sizer.Add(qrres_sizer, 0, wx.EXPAND, 0)
        # qroptions_sizer.Add(qrborder_sizer, 0, wx.EXPAND, 0)
        qroptions_sizer.Add(qrbox_sizer, 0, wx.EXPAND, 0)
        qroptions_sizer.Add(qrerrcorr_sizer, 0, wx.EXPAND, 0)

        # --------------- WIFI PANEL

        qrwifi_panel = wx.Panel(qrnotebook, wx.ID_ANY)
        qrnotebook.AddPage(qrwifi_panel, _("WiFi"))
        qrwifi_sizer = wx.BoxSizer(wx.VERTICAL)
        qrwifi_panel.SetSizer(qrwifi_sizer)
        qrwifi_ssid_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_wifi_ssid = wx.TextCtrl(qrwifi_panel, wx.ID_ANY)
        ssid_label = wx.StaticText(qrwifi_panel, wx.ID_ANY, _("SSID:"))
        ssid_label.SetMinSize(wx.Size(45, -1))
        qrwifi_ssid_sizer.Add(ssid_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrwifi_ssid_sizer.Add(self.text_wifi_ssid, 1, wx.EXPAND, 0)

        qrwifi_passwd_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.text_wifi_password = wx.TextCtrl(qrwifi_panel, wx.ID_ANY)
        pass_label = wx.StaticText(qrwifi_panel, wx.ID_ANY, _("Key:"))
        pass_label.SetMinSize(wx.Size(45, -1))
        qrwifi_passwd_sizer.Add(pass_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrwifi_passwd_sizer.Add(self.text_wifi_password, 1, wx.EXPAND, 0)

        qrwifi_wpa_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.combo_wifi_wpa = wx.ComboBox(
            qrwifi_panel,
            wx.ID_ANY,
            choices=(_("WPA/WPA2/WPA3"), _("WEP"), _("None")),
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )
        self.combo_wifi_wpa.SetToolTip(
            _("What kind of encryption does the network use?")
        )
        self.combo_wifi_wpa.SetSelection(0)  # WPA
        wpa_label = wx.StaticText(qrwifi_panel, wx.ID_ANY, _("Encryption:"))
        qrwifi_wpa_sizer.Add(wpa_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrwifi_wpa_sizer.Add(self.combo_wifi_wpa, 0, wx.EXPAND, 0)

        qrwifi_hidden_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.check_hidden = wx.CheckBox(qrwifi_panel, wx.ID_ANY, _("Hidden"))
        self.check_hidden.SetToolTip(_("Is the network hidden?"))
        self.check_hidden.SetValue(False)
        qrwifi_hidden_sizer.Add(self.check_hidden, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        qrwifi_sizer.Add(qrwifi_ssid_sizer, 0, wx.EXPAND, 0)
        qrwifi_sizer.Add(qrwifi_passwd_sizer, 0, wx.EXPAND, 0)
        qrwifi_sizer.Add(qrwifi_wpa_sizer, 0, wx.EXPAND, 0)
        qrwifi_sizer.Add(qrwifi_hidden_sizer, 0, wx.EXPAND, 0)
        self.button_wifi = wx.Button(qrwifi_panel, wx.ID_ANY, _("Generate Pattern"))
        qrwifi_sizer.Add(self.button_wifi, 0, 0, 0)
        self.button_wifi.Bind(wx.EVT_BUTTON, self.on_wifi)

        # --------------- WIFI PANEL

        qrvcard_panel = wx.Panel(qrnotebook, wx.ID_ANY)
        qrnotebook.AddPage(qrvcard_panel, _("VCard"))
        qrvcard_sizer = wx.BoxSizer(wx.VERTICAL)
        qrvcard_panel.SetSizer(qrvcard_sizer)
        qrvcard_name = wx.BoxSizer(wx.HORIZONTAL)
        self.text_vcard_name = wx.TextCtrl(qrvcard_panel, wx.ID_ANY)
        self.text_vcard_name.SetToolTip(_("Provide your name as lastname,firstname"))
        vcard_name_label = wx.StaticText(qrvcard_panel, wx.ID_ANY, _("Name:"))
        vcard_name_label.SetMinSize(wx.Size(45, -1))
        qrvcard_name.Add(vcard_name_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrvcard_name.Add(self.text_vcard_name, 1, wx.EXPAND, 0)

        qrvcard_address = wx.BoxSizer(wx.HORIZONTAL)
        self.text_vcard_address = wx.TextCtrl(qrvcard_panel, wx.ID_ANY)
        self.text_vcard_address.SetToolTip(
            _(
                "Provide your address as:\n"
                + "PO box, room number, house number, city, prefecture, zip code and country"
            )
        )
        vcard_address_label = wx.StaticText(qrvcard_panel, wx.ID_ANY, _("Address:"))
        vcard_address_label.SetMinSize(wx.Size(45, -1))
        qrvcard_address.Add(vcard_address_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrvcard_address.Add(self.text_vcard_address, 1, wx.EXPAND, 0)

        qrvcard_tel = wx.BoxSizer(wx.HORIZONTAL)
        self.text_vcard_tel = wx.TextCtrl(qrvcard_panel, wx.ID_ANY)
        self.text_vcard_tel.SetToolTip(_("Provide your phone-number"))
        vcard_tel_label = wx.StaticText(qrvcard_panel, wx.ID_ANY, _("Phone:"))
        vcard_tel_label.SetMinSize(wx.Size(45, -1))
        qrvcard_tel.Add(vcard_tel_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrvcard_tel.Add(self.text_vcard_tel, 1, wx.EXPAND, 0)

        qrvcard_email = wx.BoxSizer(wx.HORIZONTAL)
        self.text_vcard_email = wx.TextCtrl(qrvcard_panel, wx.ID_ANY)
        self.text_vcard_email.SetToolTip(_("Provide your email-Address"))
        vcard_email_label = wx.StaticText(qrvcard_panel, wx.ID_ANY, _("email:"))
        vcard_email_label.SetMinSize(wx.Size(45, -1))
        qrvcard_email.Add(vcard_email_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrvcard_email.Add(self.text_vcard_email, 1, wx.EXPAND, 0)

        qrvcard_url = wx.BoxSizer(wx.HORIZONTAL)
        self.text_vcard_url = wx.TextCtrl(qrvcard_panel, wx.ID_ANY)
        self.text_vcard_url.SetToolTip(_("Provide a valid URL"))
        vcard_url_label = wx.StaticText(qrvcard_panel, wx.ID_ANY, _("URL:"))
        vcard_url_label.SetMinSize(wx.Size(45, -1))
        qrvcard_url.Add(vcard_url_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        qrvcard_url.Add(self.text_vcard_url, 1, wx.EXPAND, 0)

        qrvcard_sizer.Add(qrvcard_name, 0, wx.EXPAND, 0)
        qrvcard_sizer.Add(qrvcard_address, 0, wx.EXPAND, 0)
        qrvcard_sizer.Add(qrvcard_tel, 0, wx.EXPAND, 0)
        qrvcard_sizer.Add(qrvcard_email, 0, wx.EXPAND, 0)
        qrvcard_sizer.Add(qrvcard_url, 0, wx.EXPAND, 0)
        self.button_vcard = wx.Button(qrvcard_panel, wx.ID_ANY, _("Generate Pattern"))
        qrvcard_sizer.Add(self.button_vcard, 0, 0, 0)
        self.button_vcard.Bind(wx.EVT_BUTTON, self.on_vcard)

        # --------------- Barcode Section

        bar_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Barcode:")), wx.VERTICAL
        )
        baroptions_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Options:")), wx.VERTICAL
        )

        bartype_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, label=_("Type:"))
        label.SetMinSize(wx.Size(80, -1))
        self.combo_barcode = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=self.PROVIDED_BARCODES,
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )
        self.combo_barcode.SetToolTip(_("What kind of barcode do you want to create?"))
        self.combo_barcode.SetSelection(4)  # ean13
        bartype_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        bartype_sizer.Add(self.combo_barcode, 1, wx.EXPAND, 0)

        bardimx_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, label=_("Width:"))
        label.SetMinSize(wx.Size(80, -1))
        self.text_bardimx = wx.TextCtrl(self, wx.ID_ANY, "auto")
        self.text_bardimx.SetToolTip(_("How wide will the resulting barcode be?"))
        self.text_bardimx.SetMaxSize(wx.Size(100, -1))
        bardimx_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        bardimx_sizer.Add(self.text_bardimx, 1, wx.EXPAND, 0)

        bardimy_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, label=_("Height:"))
        label.SetMinSize(wx.Size(80, -1))
        self.text_bardimy = wx.TextCtrl(self, wx.ID_ANY, "auto")
        self.text_bardimy.SetToolTip(_("How high will the resulting barcode be?"))
        self.text_bardimy.SetMaxSize(wx.Size(100, -1))
        bardimy_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        bardimy_sizer.Add(self.text_bardimy, 1, wx.EXPAND, 0)

        barcheck1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, label=_("No text:"))
        label.SetMinSize(wx.Size(80, -1))
        self.check_suppress = wx.CheckBox(self, wx.ID_ANY, "")
        self.check_suppress.SetToolTip(_("Suppress the text under the barcode?"))
        self.check_suppress.SetMinSize(self.text_bardimx.GetSize())
        barcheck1_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        barcheck1_sizer.Add(self.check_suppress, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        baroptions_sizer.Add(bartype_sizer, 0, wx.EXPAND, 0)
        baroptions_sizer.Add(bardimx_sizer, 0, wx.EXPAND, 0)
        baroptions_sizer.Add(bardimy_sizer, 0, wx.EXPAND, 0)
        baroptions_sizer.Add(barcheck1_sizer, 0, wx.EXPAND, 0)

        qr_sizer.Add(self.option_qr, 0, wx.EXPAND, 1)
        qr_sizer.Add(qrnotebook, 1, wx.EXPAND, 0)
        bar_sizer.Add(self.option_bar, 0, wx.EXPAND, 1)
        bar_sizer.Add(baroptions_sizer, 1, wx.EXPAND, 0)

        codes_sizer.Add(qr_sizer, 1, wx.EXPAND, 0)
        codes_sizer.Add(bar_sizer, 1, wx.EXPAND, 0)
        sizer_buttons = wx.StdDialogButtonSizer()

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetToolTip(_("Create a barcode/qrcode"))
        self.button_OK.SetDefault()
        sizer_buttons.AddButton(self.button_OK)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        self.button_CANCEL.SetToolTip(_("Close without creating anything"))
        sizer_buttons.AddButton(self.button_CANCEL)

        sizer_buttons.Realize()
        mainsizer.Add(input_sizer, 0, wx.EXPAND, 0)
        mainsizer.Add(xy_sizer, 0, wx.EXPAND, 0)
        mainsizer.Add(codes_sizer, 0, wx.EXPAND, 0)
        mainsizer.Add(sizer_buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_xpos)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_ypos)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_code)

        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_qrdim)
        # self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_qrborder)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_qrbox)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_qrres)

        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_bardimx)
        self.Bind(wx.EVT_TEXT, self.enable_buttons, self.text_bardimy)

        self.Bind(wx.EVT_RADIOBUTTON, self.enable_controls, self.option_bar)
        self.Bind(wx.EVT_RADIOBUTTON, self.enable_controls, self.option_qr)

        self.Bind(wx.EVT_BUTTON, self.on_okay, self.button_OK)
        # Force disable/enable of elements
        self.option_qr.SetValue(True)
        self.enable_buttons(None)
        self.enable_controls(None)

    def enable_controls(self, event):
        qr = self.option_qr.GetValue()
        bar = not qr

        self.text_qrdim.Enable(qr)
        # self.text_qrborder.Enable(qr)
        self.text_qrbox.Enable(qr)
        self.text_qrres.Enable(qr)
        self.combo_errcorr.Enable(qr)

        self.combo_barcode.Enable(bar)
        self.text_bardimx.Enable(bar)
        self.text_bardimy.Enable(bar)
        self.check_suppress.Enable(bar)

    def enable_buttons(self, event):
        active = True
        if len(self.text_code.GetValue()) == 0:
            active = False
        try:
            if len(self.text_xpos.GetValue()) == 0:
                active = False
            else:
                __ = self.context.elements.length_x(self.text_xpos.GetValue())
        except ValueError:
            active = False
        try:
            if len(self.text_ypos.GetValue()) == 0:
                active = False
            else:
                __ = self.context.elements.length_y(self.text_ypos.GetValue())
        except ValueError:
            active = False
        if self.option_qr.GetValue():
            try:
                __ = self.context.elements.length(self.text_qrdim.GetValue())
                __ = int(self.text_qrbox.GetValue())
                # __ = int(self.text_qrborder.GetValue())
                __ = int(self.text_qrres.GetValue())
            except ValueError:
                active = False
        else:
            # Barcode
            try:
                if self.text_bardimx.GetValue() != "auto":
                    __ = self.context.elements.length_x(self.text_bardimx.GetValue())
                if self.text_bardimy.GetValue() != "auto":
                    __ = self.context.elements.length_y(self.text_bardimy.GetValue())
            except ValueError:
                active = False

        self.button_OK.Enable(active)

    def on_okay(self, event):
        def unquote(source):
            return source.replace('"', "'")

        result = ""
        code = self.text_code.GetValue()
        xpos = self.text_xpos.GetValue()
        ypos = self.text_ypos.GetValue()
        if self.option_qr.GetValue():
            dim = self.text_qrdim.GetValue()
            # border = self.text_qrborder.GetValue()
            box = self.text_qrbox.GetValue()
            res = self.text_qrres.GetValue()
            ecval = self.combo_errcorr.GetSelection()
            corrcode = ("M", "L", "Q", "H")
            errc = corrcode[ecval]
            result = f'qrcode {xpos} {ypos} {dim} "{unquote(code)}" '
            result += f"--boxsize {box} --version {res} --errcorr {errc}"
            # result += f" --border {border}"
        else:
            # Barcode
            dimx = self.text_bardimx.GetValue()
            dimy = self.text_bardimy.GetValue()
            btype = self.PROVIDED_BARCODES[self.combo_barcode.GetSelection()]
            if self.check_suppress.GetValue():
                suppress = " --notext"
            else:
                suppress = ""
            result = f'barcode {xpos} {ypos} {dimx} {dimy} {btype} "{unqote(code)}"'
            result += f"{suppress}"
        self.command = result
        event.Skip()

    def on_wifi(self, event):
        hidden = bool(self.check_hidden.GetValue())  # False, True, None
        ssid = self.text_wifi_ssid.GetValue()
        password = self.text_wifi_password.GetValue()
        security = max(0, self.combo_wifi_wpa.GetSelection())
        # 0=WPA, 1=WEP, 2 = None
        result = "WIFI:"
        if ssid:
            result += f"S:{ssid};"
        if password:
            result += f"P:{password};"
        if security == 0:
            result += "T:WPA;"
        if security == 1:
            result += "T:WEP;"
        if hidden is None:
            result += ";"
        elif hidden:
            result += "H:TRUE;"
        else:
            result += "H:FALSE;"
        while not result.endswith(";;"):
            result += ";"
        self.option_qr.SetValue(True)
        self.text_code.SetValue(result)

    def on_vcard(self, event):
        """
        Tag	i-mode compatible bar code recognition function	Description	Example
        ADR	        The physical delivery address. The fields divided by commas (,) denote
                    PO box, room number, house number, city, prefecture, zip code and country, in order.
                    ADR:,,123 Main St.,Springfield,IL,12345,USA;
        BDAY	    8 digits for date of birth: year (4 digits), month (2 digits) and day (2 digits), in order.
                    BDAY:19700310;
        EMAIL	    The address for electronic mail communication.
                    EMAIL:johndoe@hotmail.com;
        N	        A structured representation of the name of the person. When a field is divided
                    by a comma (,), the first half is treated as the last name and the second half
                    is treated as the first name.
                    N:Doe,John;
        NICKNAME    Familiar name for the object represented by this MeCard.
                    NICKNAME:Johnny;
        NOTE	    Specifies supplemental information to be set as memo in the phonebook.
                    NOTE:I am proficient in Tiger-Crane Style,\nand I am more than proficient in the exquisite art of the Samurai sword.;
        SOUND	    Designates a text string to be set as the kana name in the phonebook.
                    When a field is divided by a comma (,), the first half is treated as the last name
                    and the second half is treated as the first name.
        TEL	        The canonical number string for a telephone number for telephony communication.
                    TEL:(123) 555-5832;
        TEL-AV	    The canonical string for a videophone number communication.
                    TEL-AV:(123) 555-5832;
        URL	        A URL pointing to a website that represents the person in some way.
                    URL:https://www.johndoe.com/;
        """
        result = "MECARD:"
        vcardname = self.text_vcard_name.GetValue().strip()
        vcardtel = self.text_vcard_tel.GetValue().strip()
        vcardadr = self.text_vcard_address.GetValue().strip()
        vcardemail = self.text_vcard_email.GetValue().strip()
        vcardurl = self.text_vcard_url.GetValue().strip()
        if vcardname != "":
            result += f"N:{vcardname};"
        if vcardadr != "":
            result += f"ADR:{vcardadr};"
        if vcardemail != "":
            result += f"EMAIL:{vcardemail};"
        if vcardtel != "":
            result += f"TEL:{vcardtel};"
        if vcardurl != "":
            result += f"URL:{vcardurl};"

        while not result.endswith(";;"):
            result += ";"
        self.text_code.SetValue(result)
        self.option_qr.SetValue(True)


class QRCodePropertyPanel(wx.Panel):
    """
    Panel for post-creation qrcode text editing
    """

    def __init__(
        self,
        *args,
        context=None,
        node=None,
        **kwds,
    ):
        # begin wxGlade: LayerSettingPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.node = node

        main_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Text to use for QR-Code:")), wx.HORIZONTAL
        )
        self.text_text = wx.TextCtrl(self, wx.ID_ANY, "")
        main_sizer.Add(self.text_text, 1, wx.EXPAND, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.text_text.Bind(wx.EVT_TEXT, self.on_text_change)
        self.set_widgets(self.node)

    def pane_hide(self):
        pass

    def pane_show(self):
        pass

    def accepts(self, node):
        if (
            hasattr(node, "mktext")
            and hasattr(node, "mkbarcode")
            and getattr(node, "mkbarcode") == "qr"
        ):
            return True
        else:
            return False

    def set_widgets(self, node):
        self.node = node
        # print(f"set_widget for {self.attribute} to {str(node)}")
        if self.node is None or not self.accepts(node):
            self.Hide()
            return
        self.text_text.SetValue(str(node.mktext))
        self.Show()

    def update_node(self):
        vtext = self.text_text.GetValue()
        if self.node.mktext == vtext:
            return
        update_qr(self.context, self.node, vtext)
        self.context.signal("element_property_reload", self.node)
        self.context.signal("refresh_scene", "Scene")

    def on_text_change(self, event):
        self.update_node()


class EANCodePropertyPanel(wx.Panel):
    """
    Panel for post-creation eancode text editing
    """

    def __init__(
        self,
        *args,
        context=None,
        node=None,
        **kwds,
    ):
        # begin wxGlade: LayerSettingPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.node = node

        main_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Text to use for Barcode:")), wx.HORIZONTAL
        )
        self.text_text = wx.TextCtrl(self, wx.ID_ANY, "")
        main_sizer.Add(self.text_text, 1, wx.EXPAND, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.text_text.Bind(wx.EVT_TEXT, self.on_text_change)
        self.set_widgets(self.node)

    def pane_hide(self):
        pass

    def pane_show(self):
        pass

    def accepts(self, node):
        if (
            hasattr(node, "mktext")
            and hasattr(node, "mkbarcode")
            and getattr(node, "mkbarcode") == "ean"
        ):
            return True
        else:
            return False

    def set_widgets(self, node):
        self.node = node
        # print(f"set_widget for {self.attribute} to {str(node)}")
        if self.node is None or not self.accepts(node):
            self.Hide()
            return
        self.text_text.SetValue(str(node.mktext))
        self.Show()

    def update_node(self):
        vtext = self.text_text.GetValue()
        if self.node.mktext == vtext:
            return
        self.node.mktext = vtext
        update_barcode(self.context, self.node, vtext)
        self.context.signal("element_property_reload", self.node)
        self.context.signal("refresh_scene", "Scene")

    def on_text_change(self, event):
        self.update_node()
