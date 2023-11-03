# creates a mapfile from index

from importlib.resources import path
from copy import deepcopy
from decimal import *
import mappyfile, click, yaml
import os, time, sys, re, math
import pprint
import urllib.request
from geodatacrawler.utils import indexFile, dict_merge
from geodatacrawler.metadata import load_default_metadata, merge_folder_metadata
from geodatacrawler import GDCCONFIG
from yaml.loader import SafeLoader
import importlib.resources as pkg_resources
from urllib.parse import urlparse
from . import templates
from pathlib import Path

@click.command()
@click.option('--dir', nargs=1, type=click.Path(exists=True),
              required=True, help="Directory as source for mapfile")
@click.option('--dir-out', nargs=1, type=click.Path(exists=True),
              required=False, help="Directory as target for the generated mapfiles")
@click.option('--dir-out-mode', nargs=1, required=False, help="flat|nested indicates if files in output folder are nested")
@click.option('--recursive', nargs=1, required=False, help="False|True, should script recurse into subfolders")
def mapForDir(dir, dir_out, dir_out_mode, recursive):
    if not dir:
        dir = "."
    if not dir_out:
        dir_out = dir
    if not dir_out_mode or dir_out_mode not in ["flat","nested"]:
        dir_out_mode = "flat"
    if recursive and recursive.lower()=='true':
        recursive = True
    else:
        recursive = False
    print(f'Creating a mapfile for dir {dir} to {dir_out} as {dir_out_mode}, recursive: {recursive}')

    # core metadata gets populated by merging the index.yaml content from parent folders
    initialMetadata = load_default_metadata("update")

    # initial config (from program folder)
    config = initialMetadata.get('robot',{})
    config['rootDir'] = dir   
    config['outDir'] = os.getenv('pgdc_dir_out') or dir_out
    config['mdUrlPattern'] = os.getenv('pgdc_md_url') or ''
    config['msUrl'] = os.getenv('pgdc_ms_url') or ''
    config['webdavUrl'] = os.getenv('pgdc_webdav_url') or ''
    config['mdLinkTypes'] = os.getenv('pgdc_md_link_types') or ['OGC:WMS','OGC:WFS','OGC:WCS']
    config['gridColors'] = "#56a1b3,#80bfab,#abdda4,#c7e8ad,#e3f4b6,#ffffbf,#fee4a0,#fec980,#fdae61,#f07c4a,#e44b33,#d7191c"

    initialMetadata['robot'] = config

    processPath("", initialMetadata, dir_out, dir_out_mode, recursive)

def processPath(relPath, parentMetadata, dir_out, dir_out_mode, recursive):

    parentConfig = parentMetadata.get('robot',{})    
    # merge folder metadata
    coreMetadata = merge_folder_metadata(parentMetadata, os.path.join(parentConfig['rootDir'],relPath), "update")
  
    config = coreMetadata.get('robot',{})

    skipSubfolders = False
    if 'skip-subfolders' in config:
        skipSubfolders = config['skip-subfolders']

    # initalise folder mapfile
    tpl = pkg_resources.open_text(templates, 'default.map')
    mf = mappyfile.load(tpl)
    lyrs = mf['layers']

    # set up header
    mf["name"] = list(filter(None, str(config['rootDir'] + os.sep + relPath).split(os.sep))).pop()

    mf["web"]["metadata"]["ows_title"] = coreMetadata.get('identification').get("title", mf["name"])
    mf["web"]["metadata"]["ows_abstract"] = coreMetadata.get('identification').get("abstract", "")
    kw = []
    for k,v in coreMetadata.get('identification',{}).get('keywords',{}).items():
            if v.get('keywords') and len(v.get('keywords')) > 0 :
                if isinstance(v.get('keywords'), list):
                    kw += v.get('keywords')
                else: #string
                    kw.append(v.get('keywords'))
    mf["web"]["metadata"]["ows_keywordlist"] = ','.join(kw)
    # todo: by thesaurus
    # wms_keywordlist_vocabulary
    # wms_keywordlist_[vocabulary’s name]_items

    # todo: wms_identifier_authority, wms_identifier_value
    # wms_authorityurl_name, wms_authorityurl_href

    # takes the first contact (maybe override from robot-section)
    if coreMetadata.get('contact') is not None and len(coreMetadata['contact'].keys()) > 0:
        mf["web"]["metadata"]["ows_role"] = list(coreMetadata.get('contact').keys())[0]
        first = coreMetadata.get('contact')[mf["web"]["metadata"]["ows_role"]]
        mf["web"]["metadata"]["ows_address"] = first.get("address","")
        mf["web"]["metadata"]["ows_city"] = first.get("city","")
        mf["web"]["metadata"]["ows_stateorprovince"] = first.get("administrativearea","")
        mf["web"]["metadata"]["ows_postcode"] = first.get("postalcode","")   
        mf["web"]["metadata"]["ows_country"] = first.get("country","")         
        mf["web"]["metadata"]["ows_contactelectronicmailaddress"] = first.get("email","")
        mf["web"]["metadata"]["ows_contactperson"] = first.get("individualname","")
        mf["web"]["metadata"]["ows_contactorganization"] = first.get("organization","")
        mf["web"]["metadata"]["ows_contactposition"] = first.get("positionname","")
        mf["web"]["metadata"]["ows_contactvoicetelephone"] = first.get("phone","")
        mf["web"]["metadata"]["ows_attribution_onlineresource"] = first.get("url","")
    mf["web"]["metadata"]["ows_fees"] = coreMetadata.get('identification').get("fees","")
    mf["web"]["metadata"]["ows_accessconstraints"] = coreMetadata.get('identification').get("accessconstraints","") 
    mf["web"]["metadata"]["ows_onlineresource"] = config['msUrl'] + '/' + mf["name"]
    mf["web"]["metadata"]["oga_onlineresource"] = mf["web"]["metadata"]["ows_onlineresource"] + '/ogcapi'

    for file in Path(os.path.join(config['rootDir'],relPath)).iterdir():
        fname = str(file).split(os.sep).pop()
        if file.is_dir() and recursive and not fname.startswith('.'):
            if skipSubfolders:
                print('Skip path: '+ str(file))
            else:
                # go one level deeper
                print('Process path: '+ str(file))
                processPath(os.path.join(relPath,fname), deepcopy(coreMetadata), dir_out, dir_out_mode, recursive)
        else:
            if 'skip-files' in config and config['skip-files'] != '' and re.search(config['skip-files'], fname):
                print('Skip file',fname)
            # process the file
            elif '.' in str(file):
                base, extension = str(file).rsplit('.', 1)
                fn = base.split(os.sep).pop()
                # do we trigger on ymls only, or also on spatial files? to go back to the file from the yml works via distribution(s)?
                if extension.lower() in ["yml","yaml"] and fn != "index":
                    # todo: operational metadata contains information on how to process the folder
                    
                    # process the layer
                    #try:
                    if os.path.exists(str(file)):
                        with open(str(file), mode="r", encoding="utf-8") as f:
                            cnf = yaml.load(f, Loader=SafeLoader)
                            cnt = deepcopy(coreMetadata)
                            dict_merge(cnt,cnf)

                            ly = cnt.get('robot',{}).get('map',{})

                            # prepare layer(s)
                            # print('Found',len(cnt.get('distribution',{}).items()),'existing disributions in',fname)

                            for d,v in cnt.get('distribution',{}).items():
                                # for each link check if local file exists
                                parsed = urlparse(v.get('url',''))
                                fn = str(parsed.path).split('/').pop()
                                sf = os.path.join(config['rootDir'], relPath , fn)
                                if not v.get('type','').startswith('OGC:') and os.path.exists(sf):
                                    print('processing file' + sf)
                                    fb,e = str(fn).rsplit('.', 1)
                                    if e and e.lower() in GDCCONFIG["SPATIAL_FILE_TYPES"]:
                                    # we better index the file again... to get band info etc
                                        fileinfo = indexFile(sf, e)

                                        if (fileinfo.get('datatype','').lower() == "raster"):
                                            fileinfo['type'] = 'raster'
                                        elif (fileinfo.get('geomtype','').lower() in ["linestring", "line", "multiline", "polyline", "wkblinestring"]):
                                            fileinfo['type'] = 'line'
                                        elif (fileinfo.get('geomtype','') in ["point", "multipoint", "wkbpoint",
                                                                    'table']):  # table is suggested for CSV, which is usually point (or none)
                                            fileinfo['type'] = 'point'
                                        else:
                                            fileinfo['type'] = 'polygon'

                                        # bounds_wgs84 also exists, but often empty
                                        # else cnt.get('identification').get('extents',{}).get('spatial',[{}])[0].get('bbox')
                                        if not 'bounds' in fileinfo.keys():
                                            fileinfo['bounds'] = [-180,-90,180,90]
                                        
                                        # first take override value from index.yml, else take value from file, else 4326
                                        # else cnt['crs'] = cnt.get('identification').get('extents',{}).get('spatial',[{}])[0].get('crs')
                                        fileinfo['crs'] = ly.get('crs',fileinfo.get('crs'))
                                        if fileinfo.get('crs') in [None,'']:
                                            fileinfo['crs'] = "epsg:4326"

                                        # evaluate if a custom style is defined
                                        style_reference = ly.get("style", '')

                                        if style_reference=='':
                                            if fileinfo['type']=='raster': # set colors for range
                                                band1 = fileinfo.get('content_info',{}).get('dimensions',[{}])[0];
                                                new_class_string2 = colorCoding(band1.get('min',0), band1.get('max',0),config['gridColors'].split(','))
                                                # fetch nodata from meta in file properties
                                                new_class_string2 = 'PROCESSING "NODATA=' + str(
                                                    fileinfo.get('meta', {}).get('nodata', -32768)) + '"\n' + new_class_string2
                                            else: # vector
                                                new_class_string2 = pkg_resources.read_text(templates, 'class-' + fileinfo['type'] + '.tpl')
                                        else: 
                                            stylefile = os.path.join(config['rootDir'],relPath,style_reference)
                                            if os.path.exists(stylefile):
                                                with open(stylefile) as f1:
                                                    new_class_string2 = f1.read()
                                                    print("Failed opening '{0}', use default style for '{1}'".format(ly.get("style", ""), fileinfo['type']))
                                            else:
                                                print(f'Stylefile {stylefile} does not exist')
                                                new_class_string2 = ""
                                                
                                        new_layer_string = pkg_resources.read_text(templates, 'layer.tpl')

                                        strLr = new_layer_string.format(name=fb,
                                                    title='"'+cnt.get('identification',{}).get('title', '')+'"',
                                                    abstract='"'+cnt.get('identification',{}).get('abstract', '')+'"',
                                                    type=fileinfo['type'],
                                                    path=os.path.join('' if dir_out_mode == 'nested' else relPath,fn), # nested or flat
                                                    template=ly.get('template', 'info.html'),
                                                    projection=fileinfo['crs'],
                                                    projections=ly.get('projections', 'epsg:4326 epsg:3857'),
                                                    extent=" ".join(map(str,fileinfo['bounds'])),
                                                    id="fid", # todo, use field from attributes, config?
                                                    mdurl=config['mdUrlPattern'].format(cnt.get('metadata',{}).get('identifier',fb)) if config['mdUrlPattern'] != '' else '', # or use the externalid here (doi)
                                                    classes=new_class_string2)
                                        #except Exception as e:
                                        #    print("Failed creation of layer {0}; {1}".format(cnt['name'], e))
                                            
                                        try:
                                            mslr = mappyfile.loads(strLr)

                                            lyrs.insert(len(lyrs) + 1, mslr)
                                        except Exception as e:
                                            print("Failed creation of layer {0}; {1}".format(fb, e))

                                        # does metadata already include a link to wms/wfs? else add it.
                                        for mdlinktype in config['mdLinkTypes']:
                                            relPath2 = relPath if dir_out_mode == 'nested' else ''
                                            if mdlinktype in ['OGC:WMS']:
                                                if not checkLink(cnt, mdlinktype, config):
                                                    addLink(mdlinktype, fb, file, relPath2, mf['name'], config)
                                            elif fileinfo['datatype'] == 'raster' and mdlinktype == 'OGC:WCS':
                                                if not checkLink(cnt, mdlinktype, config):
                                                    addLink(mdlinktype, fb, file, relPath2, mf['name'], config)
                                            elif fileinfo['datatype'] == 'vector' and mdlinktype == 'OGC:WFS' :
                                                if not checkLink(cnt, mdlinktype, config):
                                                    addLink(mdlinktype, fb, file, relPath2, mf['name'], config)

    # map should have initial layer, remove it
    lyrs.pop(0)

    # print(mappyfile.dumps(mf))
    # write to parent folder as {folder}.map
    if len(lyrs) > 0: # do not create mapfile if no layers
        do = os.path.join(dir_out,(relPath if dir_out_mode == 'nested' else ''))
        mapfile =  os.path.join(do,mf['name'] + ".map")
        
        # check if folder exists
        if not os.path.exists(do):
            print('create folder',do)
            os.makedirs(do)
            
        print(f'writing mapfile {mapfile}')
        mappyfile.save(mf, mapfile, 
            indent=4, spacer=' ', quote='"', newlinechar='\n',
            end_comment=False, align_values=False)
    else:
        print('Map empty, skip creation')

'''
Verify if this metadata already has a link to this service
'''
def checkLink(md, type, config):
    for k,v in md.get('distribution',{}).items():
        if v.get('type','').upper() == type and v.get('url','').startswith(config['msUrl']):
            return True
    return False
 
'''
Append a link to this service
'''
def addLink(type, layer, file, relPath, map, config):
    print(f'Add link {type} to {str(file)}')
    # read file
    with open(str(file), mode="r", encoding="utf-8") as f:
        orig = yaml.load(f, Loader=SafeLoader)
    # add link
        if 'distribution' not in orig.keys():
            orig['distribution'] = {}
        msUrl2 = config['msUrl'] + ('/'+ relPath if relPath != '' else '')
        orig['distribution'][type.split(':').pop()] = {
            'url':  msUrl2 + '/' + map +'?service='+type.split(':').pop()+'&amp;request=GetCapabilities',
            'type': type,
            'name': layer,
            'description': ''
        } 
    # write file
    with open(str(file), 'w') as f:
        yaml.dump(orig, f, sort_keys=False)

'''
sets a color coding for a layer
'''
def colorCoding(min,max,colors):
    try: 
        getcontext().prec = 4 # set precision of decimals, so classes are not too specific
        rng = Decimal(max - min)
        if rng > 0:
            sgmt =  Decimal(rng/len(colors))
            cur =  Decimal(min)
            clsstr = ""
            for clr in colors:
                clsstr += "CLASS\nNAME '{0} - {1}'\nEXPRESSION ( [pixel] >= {0} AND [pixel] <= {1} )\nSTYLE\nCOLOR '{2}'\nEND\nEND\n\n".format(cur,(cur+sgmt),clr)
                cur += sgmt
            return clsstr
        else:
            return ""
    except Exception as e:
        print('WARNING: Unable to assign colors to band range',str(e))
        return ""


