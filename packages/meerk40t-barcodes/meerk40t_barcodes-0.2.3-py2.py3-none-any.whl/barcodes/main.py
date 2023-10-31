def module_plugin(module, lifecycle):
    """
    This plugin attaches to the module/wxMeerK40t for the opening and closing of the gui. If the gui is never
    launched this plugin is never activated. wxMeerK40t is the gui wx.App object. If the module is loaded several times
    each module will call this function with the specific `module`

    :param module: Specific module this lifecycle event is for.
    :param lifecycle: lifecycle event being regarded.
    :return:
    """
    # print(f"module:barcode {lifecycle}")
    if lifecycle == "module":
        # Responding to "module" makes this a module plugin for the specific module replied.
        return "module/wxMeerK40t"
    elif lifecycle == "module_open":
        # This is relevant the GUI has launched and we want to add some stuff to it
        # print("wxMeerK40t App was lauched.")
        # print("Properties of module:")
        # print(vars(module))
        has_qr_code_module = False
        try:
            import qrcode

            has_qr_code_module = True
        except ModuleNotFoundError:
            pass

        has_bar_code_module = False
        try:
            import barcode

            has_bar_code_module = True
        except ModuleNotFoundError:
            pass

        if has_qr_code_module and has_bar_code_module:
            register_gui_stuff(module)

        # The interface for adhoc updating in code

    elif lifecycle == "module_close":
        # print("wxMeerK40t App was closed.")
        # Nothing particular needs to be done here so we just ignore it...
        pass
    elif lifecycle == "shutdown":
        # print("wxMeerK40t App shutdown.")
        # Nothing particular needs to be done here so we just ignore it...
        pass


def bcode_plugin(kernel, lifecycle):
    """
    Barcode plugin. Catches the lifecycle it needs registers some values.

    @param kernel:
    @param lifecycle:
    @return:
    """
    if lifecycle == "register":
        has_qr_code_module = False
        try:
            import qrcode

            has_qr_code_module = True
        except ModuleNotFoundError:
            pass

        has_bar_code_module = False
        try:
            import barcode

            has_bar_code_module = True
        except ModuleNotFoundError:
            pass

        if has_qr_code_module:
            register_qr_code_stuff(kernel)
            kernel.register("path_updater/qrcode", update_qr)
        if has_bar_code_module:
            register_bar_code_stuff(kernel)
            kernel.register("path_updater/eancode", update_barcode)


def plugin(kernel, lifecycle):
    """
    This is our main plugin. It provides examples of every lifecycle event and what they do and are used for. Many of
    these events are simply to make sure some module events occur after or before other module events. The lifecycles
    also permit listeners to attach and detach during the lifecycle of a module, and insures everything can interact
    smoothly.

    :param kernel:
    :param lifecycle:
    :return:
    """
    # print(f"Kernel plugin calling lifecycle: {lifecycle}")
    if lifecycle == "plugins":
        """
        All plugins including ones added with this call are added to the kernel. A list of additions plugins will add
        those to the list of plugins.
        """
        return [module_plugin, bcode_plugin]
    if lifecycle == "service":
        """
        Responding to this with a service provider makes this plugin a service plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a service plugin, check service_plugin for an example of that.
    if lifecycle == "module":
        """
        Responding to a registered module provider makes this plugin a module plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a module plugin, check module_plugin for an example of this.
    if lifecycle == "precli":
        """
        This lifecycle occurs before the command line options are processed. Anything part of the main CLI is processed
        after this.
        """
    if lifecycle == "cli":
        """
        This life cycle is intended to process command line information. It is sometimes used to register features or
        other flags that could be used during the invalidate.
        """
        if kernel.lookup("invalidating_plugin_existed"):
            print("Our invalidating plugin existed and put this here.")
    if lifecycle == "invalidate":
        """
        Invalidate is called with a "True" response if this plugin isn't valid or cannot otherwise execute. This is
        often useful if a plugin is only valid for a particular OS. For example `winsleep` serve no purpose for other
        operating systems, so it invalidates itself.
        """
        # Let's test for the existence of our two main components:
        has_qr_code_module = False
        try:
            import qrcode

            has_qr_code_module = True
        except ModuleNotFoundError:
            pass

        has_bar_code_module = False
        try:
            import barcode

            has_bar_code_module = True
        except ModuleNotFoundError:
            pass
        if has_bar_code_module and has_qr_code_module:
            return False  # We are valid.
        else:
            return True  # We are lacking central components

    if lifecycle == "preregister":
        """
        During the pre-register phase the module wxMeerK40t is registered and opened in gui mode.
        """
        pass
    if lifecycle == "register":
        """
        Register our various processes. These should modify the registered values within meerk40t. This stage is
        used for general purpose lookup registrations.
        """
        # See simple plugin for examples of registered objects.
        pass

    if lifecycle == "configure":
        """
        Configure is a preboot stage where everything is registered but elements are not yet booted.
        """
        pass
    elif lifecycle == "boot":
        """
        Start all services.

        The kernel strictly registers the lookup_listeners and signal_listeners during this stage. This permits modules
        and services to listen for signals and lookup changes during the active phases of their lifecycles.
        """
        pass
    elif lifecycle == "postboot":
        """
        Registers some additional choices such as some general preferences.
        """
    elif lifecycle == "prestart":
        """
        CLI specified input file is loading during the pre-start phase.
        """
        pass
    elif lifecycle == "start":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "poststart":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "ready":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "finished":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "premain":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "mainloop":
        """
        This is the start of the gui and will capture the default thread as gui thread. If we are writing a new gui
        system and we need this thread to do our work. It should be captured here. This is the main work of the program.

        You cannot ensure that more than one plugin can catch the mainloop. Capture of the mainloop happens for the
        duration of the gui app, if one exists.
        """
        pass
    elif lifecycle == "postmain":
        """
        Everything that was to grab the mainloop thread has finished. We are fully booted. However in most cases since
        the gui has been killed, the kernel has likely been told to shutdown too and will end shortly.
        """
        pass
    elif lifecycle == "preshutdown":
        """
        Preshutdown saves the current activated device to the kernel.root to ensure it has the correct last value.
        """
        pass

    elif lifecycle == "shutdown":
        """
        Meerk40t's closing down. Our plugin should adjust accordingly. All registered meerk40t processes will be stopped
        any plugin processes should also be stopped so the program can close correctly. Depending on the order of
        operations some operations might not be possible at this stage since the kernel will be in a partially shutdown
        stage.
        """
        pass


def register_bar_code_stuff(kernel):
    """
    We use the python-barcode library (https://github.com/WhyNotHugo/python-barcode)
    """
    _ = kernel.translation
    import barcode

    from .bcode_logic import PROVIDED_BARCODES, create_barcode

    @kernel.console_option(
        "notext", "n", type=bool, action="store_true", help=_("suppress text display")
    )
    @kernel.console_argument("x_pos", type=str, help=_("X-Position of barcode"))
    @kernel.console_argument("y_pos", type=str, help=_("Y-Position of barcode"))
    @kernel.console_argument(
        "dimx", type=str, help=_("Width of barcode, may be 'auto' to keep native width")
    )
    @kernel.console_argument(
        "dimy",
        type=str,
        help=_("Height of barcode, may be 'auto' to keep native height"),
    )
    @kernel.console_argument("btype", type=str, help=_("Barcode type"))
    @kernel.console_argument("code", type=str, help=_("The code to process"))
    @kernel.console_command(
        "barcode",
        help=_("Creates a barcode."),
        input_type=("elements", None),
        output_type="elements",
    )
    def create_barcode_command(
        command,
        channel,
        _,
        x_pos=None,
        y_pos=None,
        dimx=None,
        dimy=None,
        btype=None,
        code=None,
        notext=None,
        asgroup=None,
        data=None,
        **kwargs,
    ):
        elements = kernel.elements
        if btype is None:
            btype = "ean14"
        btype = btype.lower()
        if (
            x_pos is None
            or y_pos is None
            or dimx is None
            or dimy is None
            or code is None
            or code == ""
        ):
            params = "barcode x_pos y_pos dimx dimy btype code"
            channel(_("Please provide all parameters: {params}").format(params=params))
            channel(
                _("Supported formats: {all}").format(all=",".join(PROVIDED_BARCODES()))
            )
            return
        if btype not in PROVIDED_BARCODES():
            channel(
                _("Invalid format, supported: {all}").format(
                    all=",".join(PROVIDED_BARCODES())
                )
            )
            return
        # Check lengths for validity
        try:
            if dimx != "auto":
                __ = elements.length_x(dimx)
            if dimy != "auto":
                __ = elements.length_x(dimy)
            __ = elements.length_x(x_pos)
            __ = elements.length_y(y_pos)
        except ValueError:
            channel(_("Invalid dimensions provided"))
            return

        data = create_barcode(
            kernel=kernel,
            channel=channel,
            x_pos=x_pos,
            y_pos=y_pos,
            dimx=dimx,
            dimy=dimy,
            btype=btype,
            code=code,
            notext=notext,
        )
        if data is not None:
            if elements.classify_new:
                elements.classify(data)

            elements.signal("element_added", data)
            return "elements", data


def register_qr_code_stuff(kernel):
    """
    We use the qrcode library (https://github.com/lincolnloop/python-qrcode)
    """
    _ = kernel.translation
    _kernel = kernel
    _ = kernel.translation
    from .bcode_logic import create_qr

    # QR-Code generation
    @kernel.console_option(
        "errcorr",
        "e",
        type=str,
        help=_("error correction, one of L (7%), M (15%), Q (25%), H (30%)"),
    )
    @kernel.console_option("boxsize", "x", type=int, help=_("Boxsize (default 10)"))
    @kernel.console_option(
        "border", "b", type=int, help=_("Border around qr-code (default 4)")
    )
    @kernel.console_option("version", "v", type=int, help=_("size (1..40)"))
    @kernel.console_argument("x_pos", type=str, help=_("X-position of qr-code"))
    @kernel.console_argument("y_pos", type=str, help=_("Y-position of qr-code"))
    @kernel.console_argument("dim", type=str, help=_("Width/length of qr-code"))
    @kernel.console_argument("code", type=str, help=_("Text to create qr-code from"))
    @kernel.console_command(
        "qrcode",
        help=_("Creates a qr code."),
        input_type=("elements", None),
        output_type="elements",
    )
    def create_qr_command(
        command,
        channel,
        _,
        x_pos=None,
        y_pos=None,
        dim=None,
        code=None,
        errcode=None,
        boxsize=None,
        border=None,
        version=None,
        data=None,
        **kwargs,
    ):
        elements = _kernel.elements
        if x_pos is None or y_pos is None or dim is None or code is None or code == "":
            params = "qrcode x_pos y_pos dim code"
            channel(_("Please provide all parameters: {params}").format(params=params))
            return
        data = create_qr(
            kernel=kernel,
            channel=channel,
            x_pos=x_pos,
            y_pos=y_pos,
            dim=dim,
            code=code,
            errcode=errcode,
            boxsize=boxsize,
            border=border,
            version=version,
        )
        if data is not None:
            if elements.classify_new:
                elements.classify(data)
            elements.signal("element_added", data)
            return "elements", data


def update_qr(context, node):
    # We need to check for the validity ourselves...
    if (
        hasattr(node, "mktext")
        and hasattr(node, "mkbarcode")
        and getattr(node, "mkbarcode") == "qr"
    ):
        from .bcode_logic import update_qr

        update_qr(context, node, node.mktext)


def update_barcode(context, node):
    # We need to check for the validity ourselves...
    if (
        hasattr(node, "mktext")
        and hasattr(node, "mkbarcode")
        and getattr(node, "mkbarcode") == "ean"
    ):
        from .bcode_logic import update_barcode

        update_barcode(context, node, node.mktext)


def register_gui_stuff(module):
    import wx

    from .gui import BarcodeDialog, EANCodePropertyPanel, QRCodePropertyPanel
    from .tools.icons import STD_ICON_SIZE, icons8_barcode_50

    context = module.context
    kernel = context._kernel
    _ = context._
    # app = context.app
    # print (f"Received context: {vars(context)}")
    # The main interface for creation
    kernel.register(
        "button/extended_tools/barcode",
        {
            "label": _("Barcode"),
            "icon": icons8_barcode_50,
            "tip": _("Create an ean-barcode or a qr-code"),
            "action": lambda v: display_barcode_dialog(context=context),
            "size": STD_ICON_SIZE,
            "identifier": "barcode",
        },
    )
    # The interface for later customisation
    kernel.register("path_attributes/qrcode", QRCodePropertyPanel)
    kernel.register("path_attributes/eancode", EANCodePropertyPanel)

    def display_barcode_dialog(context):
        dialog = BarcodeDialog(context, None, wx.ID_ANY, "")
        if dialog.ShowModal() == wx.ID_OK:
            context(dialog.command + "\n")
        dialog.Destroy()
