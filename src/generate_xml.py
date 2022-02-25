from ome_types import to_xml, OME
from ome_types.model import Project, ProjectRef
from ome_types.model import Dataset, DatasetRef
from ome_types.model import Image, ImageRef, Pixels
from ome_types.model import TagAnnotation, MapAnnotation, ROI
from ome_types.model import AnnotationRef, ROIRef, Map
from ome_types.model import CommentAnnotation, LongAnnotation
from ome_types.model import Point, Line, Rectangle, Ellipse, Polygon
from ome_types.model import Polyline, Label
from ome_types.model.map import M
from omero.model import TagAnnotationI, MapAnnotationI
from omero.model import CommentAnnotationI, LongAnnotationI
from omero.model import PointI, LineI, RectangleI, EllipseI, PolygonI
from omero.model import PolylineI, LabelI
import pkg_resources
import ezomero
import os
from uuid import uuid4
from datetime import datetime
from pathlib import Path


def create_proj_and_ref(**kwargs):
    proj = Project(**kwargs)
    proj_ref = ProjectRef(id=proj.id)
    return proj, proj_ref


def create_dataset_and_ref(**kwargs):
    ds = Dataset(**kwargs)
    ds_ref = DatasetRef(id=ds.id)
    return ds, ds_ref


def create_pixels(obj):
    # we're assuming a single Pixels object per image
    pix_obj = obj.getPrimaryPixels()
    pixels = Pixels(
        id=obj.getId(),
        dimension_order=pix_obj.getDimensionOrder().getValue(),
        size_c=pix_obj.getSizeC(),
        size_t=pix_obj.getSizeT(),
        size_x=pix_obj.getSizeX(),
        size_y=pix_obj.getSizeY(),
        size_z=pix_obj.getSizeZ(),
        type=pix_obj.getPixelsType().getValue(),
        metadata_only=True)
    return pixels


def create_image_and_ref(**kwargs):
    img = Image(**kwargs)
    img_ref = ImageRef(id=img.id)
    return img, img_ref


def create_tag_and_ref(**kwargs):
    tag = TagAnnotation(**kwargs)
    tagref = AnnotationRef(id=tag.id)
    return tag, tagref


def create_comm_and_ref(**kwargs):
    tag = CommentAnnotation(**kwargs)
    tagref = AnnotationRef(id=tag.id)
    return tag, tagref


def create_kv_and_ref(**kwargs):
    kv = MapAnnotation(**kwargs)
    kvref = AnnotationRef(id=kv.id)
    return kv, kvref


def create_long_and_ref(**kwargs):
    long = LongAnnotation(**kwargs)
    longref = AnnotationRef(id=long.id)
    return long, longref


def create_roi_and_ref(**kwargs):
    roi = ROI(**kwargs)
    roiref = ROIRef(id=roi.id)
    return roi, roiref


def create_point(shape):
    args = {'id': shape.getId().val, 'x': shape.getX().val,
            'y': shape.getY().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    pt = Point(**args)
    return pt


def create_line(shape):
    args = {'id': shape.getId().val, 'x1': shape.getX1().val,
            'y1': shape.getY1().val, 'x2': shape.getX2().val,
            'y2': shape.getY2().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    if shape.getMarkerStart() is not None:
        args['marker_start'] = shape.getMarkerStart().val
    if shape.getMarkerEnd() is not None:
        args['marker_end'] = shape.getMarkerEnd().val
    ln = Line(**args)
    return ln


def create_rectangle(shape):
    args = {'id': shape.getId().val, 'x': shape.getX().val,
            'y': shape.getY().val, 'height': shape.getHeight().val,
            'width': shape.getWidth().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    rec = Rectangle(**args)
    return rec


def create_ellipse(shape):
    args = {'id': shape.getId().val, 'x': shape.getX().val,
            'y': shape.getY().val, 'radius_x': shape.getRadiusX().val,
            'radius_y': shape.getRadiusY().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    ell = Ellipse(**args)
    return ell


def create_polygon(shape):
    args = {'id': shape.getId().val, 'points': shape.getPoints().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    pol = Polygon(**args)
    return pol


def create_polyline(shape):
    args = {'id': shape.getId().val, 'points': shape.getPoints().val}
    args['text'] = ''
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTextValue() is not None:
        args['text'] = shape.getTextValue().val
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    pol = Polyline(**args)
    return pol


def create_label(shape):
    args = {'id': shape.getId().val, 'x': shape.getX().val,
            'y': shape.getY().val}
    args['text'] = shape.getTextValue().val
    args['font_size'] = shape.getFontSize().getValue()
    args['the_c'] = 0
    args['the_z'] = 0
    args['the_t'] = 0
    if shape.getTheC() is not None:
        args['the_c'] = max(shape.getTheC().val, 0)
    if shape.getTheZ() is not None:
        args['the_z'] = shape.getTheZ().val
    if shape.getTheT() is not None:
        args['the_t'] = shape.getTheT().val
    if shape.getFillColor() is not None:
        args['fill_color'] = shape.getFillColor().val
    if shape.getLocked() is not None:
        args['locked'] = shape.getLocked().val
    if shape.getStrokeColor() is not None:
        args['stroke_color'] = shape.getStrokeColor().val
    pt = Label(**args)
    return pt


def create_shapes(roi):
    shapes = []
    for s in roi.iterateShapes():
        if isinstance(s, PointI):
            p = create_point(s)
            shapes.append(p)
        elif isinstance(s, LineI):
            line = create_line(s)
            shapes.append(line)
        elif isinstance(s, RectangleI):
            r = create_rectangle(s)
            shapes.append(r)
        elif isinstance(s, EllipseI):
            e = create_ellipse(s)
            shapes.append(e)
        elif isinstance(s, PolygonI):
            pol = create_polygon(s)
            shapes.append(pol)
        elif isinstance(s, PolylineI):
            pol = create_polyline(s)
            shapes.append(pol)
        elif isinstance(s, LabelI):
            pol = create_label(s)
            shapes.append(pol)
        else:
            print("not a real thing")
            continue
    return shapes


def create_filepath_annotations(id, conn):
    ns = f'Image:{id}'
    anns = []
    refs = []
    fpaths = ezomero.get_original_filepaths(conn, id)
    if len(fpaths) > 1:
        allpaths = []
        for f in fpaths:
            f = Path(f)
            allpaths.append(f.parts)
        common_root = Path(*os.path.commonprefix(allpaths))
        path = os.path.join(common_root, 'mock_folder')
        id = (-1) * uuid4().int
        an = CommentAnnotation(id=id,
                               namespace=ns,
                               value=str(path)
                               )
        anns.append(an)
        anref = ROIRef(id=an.id)
        refs.append(anref)
    else:
        if fpaths:
            f = fpaths[0]
        else:
            f = f'pixel_images/{id}.tiff'

        id = (-1) * uuid4().int
        an = CommentAnnotation(id=id,
                               namespace=ns,
                               value=f
                               )
        anns.append(an)
        anref = ROIRef(id=an.id)
        refs.append(anref)
    return anns, refs


def create_provenance_metadata(id, hostname):
    software = "omero-cli-transfer"
    version = pkg_resources.get_distribution(software).version
    date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    md_dict = {'origin_image_id': id, 'origin_hostname': hostname,
               'packing_timestamp': date_time,
               'software': software, 'version': version}
    ns = 'openmicroscopy.org/cli/transfer'
    id = (-1) * uuid4().int
    mmap = []
    for _key, _value in md_dict.items():
        if _value:
            mmap.append(M(k=_key, value=str(_value)))
        else:
            mmap.append(M(k=_key, value=''))
    kv, ref = create_kv_and_ref(id=id,
                                namespace=ns,
                                value=Map(m=mmap))
    return kv, ref


def populate_roi(obj, roi_obj, ome):
    id = obj.getId().getValue()
    name = obj.getName()
    if name is not None:
        name = name.getValue()
    desc = obj.getDescription()
    if desc is not None:
        desc = desc.getValue()
    shapes = create_shapes(obj)
    if not shapes:
        return None
    roi, roi_ref = create_roi_and_ref(id=id, name=name, description=desc,
                                      union=shapes)
    for ann in roi_obj.listAnnotations():
        add_annotation(roi, ann, ome)
    if roi not in ome.rois:
        ome.rois.append(roi)
    return roi_ref


def populate_image(obj, ome, conn, hostname):
    id = obj.getId()
    name = obj.getName()
    desc = obj.getDescription()
    img_id = f"Image:{str(id)}"
    if img_id in [i.id for i in ome.images]:
        img_ref = ImageRef(id=img_id)
        return img_ref
    pix = create_pixels(obj)
    img, img_ref = create_image_and_ref(id=id, name=name,
                                        description=desc, pixels=pix)
    for ann in obj.listAnnotations():
        add_annotation(img, ann, ome)

    kv, ref = create_provenance_metadata(id, hostname)
    kv_id = f"Annotation:{str(kv.id)}"
    if kv_id not in [i.id for i in ome.structured_annotations]:
        ome.structured_annotations.append(kv)
    img.annotation_ref.append(ref)
    filepath_anns, refs = create_filepath_annotations(id, conn)
    for i in range(len(filepath_anns)):
        ome.structured_annotations.append(filepath_anns[i])
        img.annotation_ref.append(refs[i])
    roi_service = conn.getRoiService()
    rois = roi_service.findByImage(id, None).rois
    for roi in rois:
        roi_obj = conn.getObject('Roi', roi.getId().getValue())
        roi_ref = populate_roi(roi, roi_obj, ome)
        if not roi_ref:
            continue
        img.roi_ref.append(roi_ref)
    img_id = f"Image:{str(img.id)}"
    if img_id not in [i.id for i in ome.datasets]:
        ome.images.append(img)
    if obj.getFileset():
        for fs_image in obj.getFileset().copyImages():
            fs_img_id = f"Image:{str(fs_image.getId())}"
            if fs_img_id not in [i.id for i in ome.images]:
                populate_image(fs_image, ome, conn, hostname)
    return img_ref


def populate_dataset(obj, ome, conn, hostname):
    id = obj.getId()
    name = obj.getName()
    desc = obj.getDescription()
    ds, ds_ref = create_dataset_and_ref(id=id, name=name,
                                        description=desc)
    for ann in obj.listAnnotations():
        add_annotation(ds, ann, ome)
    for img in obj.listChildren():
        img_obj = conn.getObject('Image', img.getId())
        img_ref = populate_image(img_obj, ome, conn, hostname)
        ds.image_ref.append(img_ref)
    ds_id = f"Dataset:{str(ds.id)}"
    if ds_id not in [i.id for i in ome.datasets]:
        ome.datasets.append(ds)
    return ds_ref


def populate_project(obj, ome, conn, hostname):
    id = obj.getId()
    name = obj.getName()
    desc = obj.getDescription()
    proj, _ = create_proj_and_ref(id=id, name=name, description=desc)
    for ann in obj.listAnnotations():
        add_annotation(proj, ann, ome)
    for ds in obj.listChildren():
        ds_obj = conn.getObject('Dataset', ds.getId())
        ds_ref = populate_dataset(ds_obj, ome, conn, hostname)
        proj.dataset_ref.append(ds_ref)
    ome.projects.append(proj)


def add_annotation(obj, ann, ome):
    if ann.OMERO_TYPE == TagAnnotationI:
        tag, ref = create_tag_and_ref(id=ann.getId(),
                                      value=ann.getTextValue())
        if tag.id not in [i.id for i in ome.structured_annotations]:
            ome.structured_annotations.append(tag)
        obj.annotation_ref.append(ref)

    elif ann.OMERO_TYPE == MapAnnotationI:
        mmap = []
        for _key, _value in ann.getMapValueAsMap().items():
            if _value:
                mmap.append(M(k=_key, value=str(_value)))
            else:
                mmap.append(M(k=_key, value=''))
        kv, ref = create_kv_and_ref(id=ann.getId(),
                                    namespace=ann.getNs(),
                                    value=Map(
                                    m=mmap))
        if kv.id not in [i.id for i in ome.structured_annotations]:
            ome.structured_annotations.append(kv)
        obj.annotation_ref.append(ref)

    elif ann.OMERO_TYPE == CommentAnnotationI:
        comm, ref = create_comm_and_ref(id=ann.getId(),
                                        value=ann.getTextValue())
        if comm.id not in [i.id for i in ome.structured_annotations]:
            ome.structured_annotations.append(comm)
        obj.annotation_ref.append(ref)

    elif ann.OMERO_TYPE == LongAnnotationI:
        long, ref = create_long_and_ref(id=ann.getId(),
                                        namespace=ann.getNs(),
                                        value=ann.getValue())
        if long.id not in [i.id for i in ome.structured_annotations]:
            ome.structured_annotations.append(long)
        obj.annotation_ref.append(ref)


def list_image_ids(ome):
    id_list = {}
    for ann in ome.structured_annotations:
        clean_id = int(ann.id.split(":")[-1])
        if isinstance(ann, CommentAnnotation) and clean_id < 0:
            id_list[ann.namespace] = ann.value
    return id_list


def populate_xml(datatype, id, filepath, conn, hostname):
    ome = OME()
    obj = conn.getObject(datatype, id)
    if datatype == 'Project':
        populate_project(obj, ome, conn, hostname)
    if datatype == 'Dataset':
        populate_dataset(obj, ome, conn, hostname)
    if datatype == 'Image':
        populate_image(obj, ome, conn, hostname)
    with open(filepath, 'w') as fp:
        print(to_xml(ome), file=fp)
        fp.close()
    path_id_dict = list_image_ids(ome)
    return path_id_dict
