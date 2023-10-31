"""
This module contains the logic to create the different barcode elements
"""


def PROVIDED_BARCODES():
    import barcode

    result = list(barcode.PROVIDED_BARCODES)
    special = "code39"
    if special in result:
        idx = result.index(special)
        result.insert(idx + 1, special + "+checksum")
    return result


def render_barcode(
    context,
    x_pos=None,
    y_pos=None,
    dimx=None,
    dimy=None,
    btype=None,
    code=None,
    notext=None,
):
    import barcode
    from meerk40t.svgelements import Color, Matrix, Path

    def poor_mans_svg_parser(svg_str, actionable):
        origin_x = float("inf")
        origin_y = float("inf")
        maximum_height = 0
        maximum_width = 0
        data = []
        if actionable:
            # We run through it just to establish
            # the maximum_width and maximum_height
            (
                maximum_width,
                maximum_height,
                origin_x,
                origin_y,
                dummy_data,
            ) = poor_mans_svg_parser(svg_str, False)
            scale_x = 1
            scale_y = 1
            if dimx != "auto":
                if maximum_width - origin_x != 0:
                    scale_x = elements.length_x(dimx) / (maximum_width - origin_x)
            if dimy != "auto":
                if maximum_height - origin_y != 0:
                    scale_y = elements.length_y(dimy) / (maximum_height - origin_y)
            offset_x = elements.length_x(x_pos)
            offset_y = elements.length_y(y_pos)
        barcodepath = None
        pathcode = ""
        pattern_rect = "<rect"
        pattern_text = "<text"
        pattern_group_start = "<g "
        pattern_group_end = "</g>"
        # A barcode just contains a couple of rects and
        # a text inside a group, so no need to get overly fancy...
        # print(svg_str)
        svg_lines = svg_str.split("\r\n")
        if len(svg_lines) <= 1:
            svg_lines = svg_str.split("\n")

        for line in svg_lines:
            # print (f"{line}")
            if pattern_rect in line:
                subpattern = (
                    ('height="', "height"),
                    ('width="', "width"),
                    ('x="', "x"),
                    ('y="', "y"),
                    ('style="', ""),
                )
                line_items = line.strip().split(" ")
                elem = {
                    "type": "elem rect",
                    "x": None,
                    "y": None,
                    "width": None,
                    "height": None,
                    "fill": None,
                    "stroke": None,
                }
                for idx, item in enumerate(line_items):
                    for pattern in subpattern:
                        if item.startswith(pattern[0]):
                            content = item[len(pattern[0]) : -1]
                            # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                            key = pattern[1]
                            if key == "":
                                # Special case fill/stroke
                                if "fill:black" in content:
                                    elem["fill"] = "black"
                                if "stroke:black" in content:
                                    elem["stroke"] = "black"
                            else:
                                elem[pattern[1]] = content
                # print (f"Line {line}")
                # print (f"Decoded {elem['type']}: x={elem['x']}, y={elem['y']}, w={elem['width']}, h={elem['height']}, stroke={elem['stroke']}, fill={elem['fill']}")
                if elem["x"] is None or elem["y"] is None:
                    continue
                if actionable:
                    this_x = offset_x + scale_x * (
                        elements.length_x(elem["x"]) - origin_x
                    )
                    this_y = offset_y + scale_y * (
                        elements.length_y(elem["y"]) - origin_y
                    )
                    this_wd = scale_x * elements.length_x(elem["width"])
                    this_ht = scale_y * elements.length_y(elem["height"])
                    # A direct creation of the path with it's native methods failed for me
                    # so I circumvent this by preparing a valid SVG path definition and let
                    # the path parse it - this works, so I assume a flaw in my coding or
                    # in the underlying application of the matrix (which should be very simple
                    # as I provide all coordinates in base units) - whatever this method
                    # works, the other doesn't....

                    # barcodepath.move(this_x, this_y)
                    # barcodepath.line(this_x + this_wd, this_y)
                    # barcodepath.line(this_x + this_wd, this_y + this_ht)
                    # barcodepath.line(this_x, this_y + this_ht)
                    # barcodepath.line(this_x, this_y)
                    # barcodepath.closed(relative=True)
                    pathcode += f"M {this_x:.1f} {this_y:.1f} "
                    pathcode += f"L {this_x + this_wd:.1f} {this_y:.1f} "
                    pathcode += f"L {this_x + this_wd:.1f} {this_y + this_ht:.1f} "
                    pathcode += f"L {this_x:.1f} {this_y + this_ht:.1f} "
                    pathcode += f"L {this_x:.1f} {this_y:.1f} "
                    pathcode += f"z "
                else:
                    # just establish dimensions
                    # print (f"check rect extent for x={elem['x']}, y={elem['y']}, wd={elem['width']}, ht={elem['height']}")
                    this_extent_x = elements.length_x(elem["x"])
                    this_extent_y = elements.length_y(elem["y"])
                    this_extent_maxx = this_extent_x + elements.length_x(elem["width"])
                    this_extent_maxy = this_extent_y + elements.length_y(elem["height"])
                    origin_x = min(origin_x, this_extent_x)
                    origin_y = min(origin_y, this_extent_y)
                    maximum_width = max(maximum_width, this_extent_maxx)
                    maximum_height = max(maximum_height, this_extent_maxy)
            elif pattern_text in line:
                NATIVE_UNIT_PER_INCH = 65535
                DEFAULT_PPI = 96.0
                UNITS_PER_PIXEL = NATIVE_UNIT_PER_INCH / DEFAULT_PPI
                subpattern = (
                    ('height="', "height"),
                    ('width="', "width"),
                    ('x="', "x"),
                    ('y="', "y"),
                    ('style="', ""),
                )
                stylepattern = (
                    ("fill:", "fill"),
                    ("font-size:", "size"),
                    ("text-anchor:", "anchor"),
                )
                elem = {
                    "type": "elem text",
                    "text": None,
                    "x": None,
                    "y": None,
                    "size": None,
                    "anchor": None,
                    "fill": None,
                    "stroke": None,
                }
                line_items = line.strip().split(" ")
                for idx, item in enumerate(line_items):
                    for pattern in subpattern:
                        if item.startswith(pattern[0]):
                            content = item[len(pattern[0]) : -1]
                            # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                            key = pattern[1]
                            if key == "":
                                style_items = content.strip().split(";")
                                for sidx, sitem in enumerate(style_items):
                                    # print(f"Styleitem: {sitem}")
                                    if sitem.startswith('">'):
                                        content = sitem[2:]
                                        eidx = content.find("</text")
                                        if eidx > 0:
                                            content = content[:eidx]
                                        elem["text"] = content
                                        continue
                                    for spattern in stylepattern:
                                        if sitem.startswith(spattern[0]):
                                            content = sitem[len(spattern[0]) :]
                                            # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                                            key = spattern[1]
                                            if key != "":
                                                elem[spattern[1]] = content
                            else:
                                elem[pattern[1]] = content

                # print (f"Line {line}")
                # print (f"Decoded {elem['type']}: txt='{elem['text']}', x={elem['x']}, y={elem['y']}, anchor={elem['anchor']}, size={elem['size']}, stroke={elem['stroke']}, fill={elem['fill']}")
                if elem["x"] is None or elem["y"] is None:
                    continue
                if actionable and not notext:
                    this_x = offset_x + scale_x * (
                        elements.length_x(elem["x"]) - origin_x
                    )
                    # Y is always too high - we compensate that by bringing it up
                    #
                    compensation = 0
                    if elem["size"] is not None:
                        if elem["size"].endswith("pt"):
                            this_size = float(elem["size"][:-2])
                        else:
                            this_size = float(elem["size"])
                        compensation = 1.25 * this_size * NATIVE_UNIT_PER_INCH / 72
                    # print (f"Size: {this_size:.1f}, Compensation: {compensation:.1f}")
                    this_y = (
                        offset_y
                        - scale_y * compensation
                        + scale_y * (elements.length_y(elem["y"]) - origin_y)
                    )
                    node = elements.elem_branch.create(
                        text=elem["text"],
                        matrix=Matrix(
                            f"translate({this_x}, {this_y}) scale({UNITS_PER_PIXEL})"
                        ),
                        anchor="start" if elem["anchor"] is None else elem["anchor"],
                        type="elem text",
                    )
                    if elem["size"] is not None:
                        font_size = int(this_size * min(scale_x, scale_y))
                        if font_size <= 1:
                            font_size = this_size
                        node.font_size = font_size
                    node.stroke = (
                        None if elem["stroke"] is None else Color(elem["stroke"])
                    )
                    node.fill = None if elem["fill"] is None else Color(elem["fill"])
                    data.append(node)
                else:
                    # We establish dimensions, but we don't apply it
                    # print (f"check text extent for x={elem['x']}, y={elem['y']}")
                    this_extent_x = elements.length_x(elem["x"])
                    this_extent_y = elements.length_y(elem["y"])
                    # maximum_width = max(maximum_width, this_extent_x)
                    # maximum_height = max(maximum_height, this_extent_y)
            elif pattern_group_end in line:
                #  print (f"Group end: '{line}'")
                if actionable:
                    # We need to close and add the path
                    barcodepath = Path(
                        fill=Color("black"),
                        stroke=None,
                        fillrule=0,  # FILLRULE_NONZERO,
                        matrix=Matrix(),
                    )
                    barcodepath.parse(pathcode)
                    node = elements.elem_branch.create(
                        path=abs(barcodepath),
                        stroke_width=0,
                        stroke_scaled=False,
                        type="elem path",
                        fillrule=0,  # nonzero
                        label=f"{btype}={code}",
                    )
                    node.matrix.post_translate(
                        -node.bounds[0] + offset_x, -node.bounds[1] + offset_y
                    )
                    node.modified()
                    node.stroke = (
                        None if elem["stroke"] is None else Color(elem["stroke"])
                    )
                    node.fill = None if elem["fill"] is None else Color(elem["fill"])
                    data.append(node)

            elif pattern_group_start in line:
                # print(f"Group start: '{line}'")
                if actionable:
                    pathcode = ""
        return maximum_width, maximum_height, origin_x, origin_y, data

    elements = context.elements
    special = "code39"
    use_auto_checksum_param = False
    auto_checksum = False
    if btype.startswith(special):
        use_auto_checksum_param = True
        if btype.endswith("+checksum"):
            btype = special
            auto_checksum = True

    bcode_class = barcode.get_barcode_class(btype)
    if hasattr(bcode_class, "digits"):
        digits = getattr(bcode_class, "digits", 0)
        if digits > 0:
            while len(code) < digits:
                code = "0" + code
    writer = barcode.writer.SVGWriter()
    if use_auto_checksum_param:
        try:
            my_barcode = bcode_class(code, writer=writer, add_checksum=auto_checksum)
        except:
            return None
    else:
        try:
            my_barcode = bcode_class(code, writer=writer)
        except:
            return None
    if hasattr(my_barcode, "build"):
        my_barcode.build()
    # print(f"Generated barcode for {code} ({btype})")
    bytes_result = my_barcode.render()
    result = bytes_result.decode("utf-8")
    max_wd, max_ht, ox, oy, data = poor_mans_svg_parser(result, True)
    return data


def create_barcode(
    kernel,
    channel,
    x_pos=None,
    y_pos=None,
    dimx=None,
    dimy=None,
    btype=None,
    code=None,
    notext=None,
):
    # ---------------------------------
    _ = kernel.translation
    elements = kernel.elements
    orgcode = code
    if code is not None:
        code = elements.mywordlist.translate(code)
    if btype is None:
        btype = "ean14"
    btype = btype.lower()
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
        return None
    if notext is None:
        notext = False

    data = render_barcode(
        kernel,
        x_pos=x_pos,
        y_pos=y_pos,
        dimx=dimx,
        dimy=dimy,
        btype=btype,
        code=code,
        notext=notext,
    )
    if data is None:
        return None

    groupnode = None
    if len(data) > 0:
        groupnode = elements.elem_branch.add(type="group", label=f"{btype} - {orgcode}")

    for node in data:
        if node.type == "elem path":
            # We store the data for later customisation
            node.mktext = orgcode
            node.mkbarcode = "ean"
            node.mkbcparam = btype
            node._translated_text = code
        elements.elem_branch.add_node(node)
        if groupnode is not None:
            groupnode.append_child(node)
    return data


def update_barcode(context, node, code):
    if node is None:
        return
    if (
        not hasattr(node, "mktext")
        or not hasattr(node, "mkbarcode")
        or getattr(node, "mkbarcode") != "ean"
    ):
        return

    elements = context.elements
    oldcode = node.mktext
    if oldcode is not None:
        oldcode = elements.mywordlist.translate(code)
    orgcode = code
    if code is not None:
        code = elements.mywordlist.translate(code)
    # print(f"ean update called with {code} ({orgcode}) for {node.label}")

    btype = getattr(node, "mkbcparam", "")
    if btype == "":
        btype = "ean14"
    bb = node.path.bbox(False)
    x_pos = bb[0]
    y_pos = bb[1]
    dimx = bb[2] - bb[0]
    dimy = bb[3] - bb[1]
    notext = False
    data = render_barcode(
        context=context,
        x_pos=x_pos,
        y_pos=y_pos,
        dimx=dimx,
        dimy=dimy,
        btype=btype,
        code=code,
        notext=notext,
    )
    if data is None:
        return None
    newcode = None
    for e in data:
        if e.type == "elem path":
            olda = node.path.transform.a
            oldb = node.path.transform.b
            oldc = node.path.transform.c
            oldd = node.path.transform.d
            olde = node.path.transform.e
            oldf = node.path.transform.f
            node.path = abs(e.path)
            node.path.transform.reset()
            node.path.transform.a = olda
            node.path.transform.b = oldb
            node.path.transform.c = oldc
            node.path.transform.d = oldd
            node.path.transform.e = olde
            node.path.transform.f = oldf

            node.mktext = orgcode
            node._translated_text = code
            node.altered()
        elif e.type == "elem text":
            newcode = e.text
    # Let's see if we can find a text node in the same group as this...
    if newcode is None or oldcode is None:
        return
    parent = node.parent
    if parent.type == "group" and len(parent.children) == 2:
        for e in parent.children:
            if e.type == "elem text":
                e.text = newcode
                e.modified()


def render_qr(context, version, errc, boxsize, border, wd, code):
    import qrcode
    import qrcode.image.svg
    from meerk40t.core.units import Length
    from meerk40t.svgelements import Matrix, Path

    path = None
    elements = context.elements
    if version is None:
        version = 1
    qr = qrcode.QRCode(
        version=version,
        error_correction=errc,
        box_size=boxsize,
        border=border,
    )

    qr.add_data(code)
    factory = qrcode.image.svg.SvgPathImage
    qr.image_factory = factory
    if version is None:
        img = qr.make_image(fit=True)
    else:
        img = qr.make_image()
    # We do get a ready to go svg string, but let's try to
    # extract some basic information
    # 1) Dimension

    dim_x = "3cm"
    dim_y = "3cm"
    test = Length(wd)
    txt = str(img.to_string())
    pattern = 'viewBox="'
    idx = txt.find(pattern)
    if idx >= 0:
        txt = txt[idx + len(pattern) :]
        idx = txt.find('"')
        if idx >= 0:
            txt = txt[:idx]
            vp = txt.split(" ")
            dim_x = str(float(vp[2]) - 2 * border) + "mm"
            dim_y = str(float(vp[3]) - 2 * border) + "mm"
    svg_x = elements.length_x(dim_x)
    svg_y = elements.length_y(dim_y)
    # 2) Path definition
    txt = str(img.to_string())
    pathstr = ""
    pattern = '<path d="'
    idx = txt.find(pattern)
    if idx >= 0:
        txt = txt[idx + len(pattern) :]
        idx = txt.find(" id=")
        if idx >= 0:
            txt = txt[: idx - 1]
            pathstr = txt
    if len(pathstr):
        mm = elements.length("1mm")
        sx = mm
        sy = mm

        sx *= wd / svg_x
        sy *= wd / svg_y
        # px = -border * mm + xp
        # py = -border * mm + yp
        matrix = Matrix(f"scale({sx},{sy})")
        # channel(f"scale({sx},{sy})")
        path = Path(
            fill="black",
            stroke=None,
            width=dim_x,
            height=dim_y,
            matrix=Matrix(),
        )
        path.parse(pathstr)
        matrix = Matrix(f"scale({sx},{sy})")
        path.transform *= matrix
        # channel(f"pathstr={pathstr[:10]}...{pathstr[-10:]}")
        # channel(f"x={dim_x}, y={dim_y},")
    return path


def create_qr(
    kernel,
    channel,
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
    import qrcode

    _ = kernel.translation
    elements = kernel.elements
    data = []
    orgcode = code
    # Make sure we translate any patterns if needed
    if code is not None:
        code = elements.mywordlist.translate(orgcode)
    # - version=None    We don't preestablish the size but let the routine decide
    # - box_size        controls how many pixels each “box” of the QR code is.
    # - border          how many boxes thick the border should be (the default
    #                   is 4, which is the minimum according to the specs).
    if errcode is None:
        errcode = "M"
    errcode = errcode.upper()
    if errcode == "L":
        errc = qrcode.constants.ERROR_CORRECT_L
    elif errcode == "Q":
        errc = qrcode.constants.ERROR_CORRECT_Q
    elif errcode == "H":
        errc = qrcode.constants.ERROR_CORRECT_H
    else:
        errc = qrcode.constants.ERROR_CORRECT_M
    if border is None or border < 4:
        border = 4
    if boxsize is None:
        boxsize = 10
    try:
        xp = elements.length_x(x_pos)
        yp = elements.length_y(y_pos)
        wd = elements.length(dim)
    except ValueError:
        channel(_("Invalid dimensions provided"))
        return None
    path = render_qr(kernel, version, errc, boxsize, border, wd, code)
    if path is None:
        return None
    node = elements.elem_branch.add(
        path=abs(path),
        stroke_width=0,
        stroke_scaled=False,
        type="elem path",
        fillrule=0,  # nonzero
        label=f"qr={code}",
    )
    node.matrix.post_translate(-node.bounds[0] + xp, -node.bounds[1] + yp)
    node.modified()
    node.mktext = orgcode
    node._translated_text = code
    node.mkbarcode = "qr"
    node.mkbcparam = (version, errc, boxsize, border)

    data = [node]
    return data


def update_qr(context, node, code):
    import qrcode

    if node is None:
        return
    if (
        not hasattr(node, "mktext")
        or not hasattr(node, "mkbarcode")
        or getattr(node, "mkbarcode") != "qr"
    ):
        return
    elements = context.elements
    orgcode = code
    if code is not None:
        code = elements.mywordlist.translate(orgcode)
    # print(f"qr update called with {code} ({orgcode}) for {node.label}")

    version = None
    errcode = "M"
    if errcode == "L":
        errc = qrcode.constants.ERROR_CORRECT_L
    elif errcode == "Q":
        errc = qrcode.constants.ERROR_CORRECT_Q
    elif errcode == "H":
        errc = qrcode.constants.ERROR_CORRECT_H
    else:
        errc = qrcode.constants.ERROR_CORRECT_M

    boxsize = 10
    border = 4
    if hasattr(node, "mkbcparam"):
        valu = node.mkbcparam
        if isinstance(valu, (list, tuple)) and len(valu) > 3:
            version = valu[0]
            errc = valu[1]
            boxsize = valu[2]
            border = valu[3]

    bb = node.path.bbox(False)
    wd = bb[2] - bb[0]
    path = render_qr(context, version, errc, boxsize, border, wd, code)

    # DEBUG CODE
    # bb = node.bounds
    # oldwd1 = bb[2] - bb[0]
    # bb = node.path.bbox(False)
    # oldwd2 = bb[2] - bb[0]
    # bb = path.bbox(False)
    # midwd2 = bb[2] - bb[0]
    # olds = str(node.path)[0:50]
    # news = str(path)[0:50]

    olda = node.path.transform.a
    oldb = node.path.transform.b
    oldc = node.path.transform.c
    oldd = node.path.transform.d
    olde = node.path.transform.e
    oldf = node.path.transform.f
    np = abs(path)
    from copy import copy

    node.path = copy(np)
    node.path.transform.reset()
    node.path.transform.a = olda
    node.path.transform.b = oldb
    node.path.transform.c = oldc
    node.path.transform.d = oldd
    node.path.transform.e = olde
    node.path.transform.f = oldf
    # print (f"x={node.mkcoordx}, y={node.mkcoordy}")

    # oldtext = node.mktext
    # old_trans = getattr(node, "_translated_text", "")

    node.mktext = orgcode
    node._translated_text = code
    node.altered()

    # DEBUG CODE
    # bb = node.bounds
    # newwd1 = bb[2] - bb[0]
    # bb = node.path.bbox(False)
    # newwd2 = bb[2] - bb[0]

    # print(f"Updated: from {oldtext} ({old_trans}) -> {orgcode} ({code})")
    # print(f"Old width: {oldwd1:.2f} ({oldwd2:.2f}), mid: ({midwd2:.2f}), new:{newwd1:.2f} ({newwd2:.2f})")
    # print(f"Old: {olds}")
    # print(f"New: {news}")
