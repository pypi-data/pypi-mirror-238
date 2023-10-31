"""The 'phys2bidscoin' plugin is a wrapper around the phys2bids (https://phys2bids.readthedocs.io) Python library to
interact with and convert physiological source data. Phys2bids currently supports the conversion of labchart
(ADInstruments) and AcqKnowledge (BIOPAC) source files to compressed tab-separated value (``.tsv.gz``) files and
create their json sidecar files, as per BIDS specifications. This plugin has been developed during the OHBM hackathon
2021 (https://github.com/ohbm/hackathon2021/issues/12) and is **not yet functional**"""

try:
    from phys2bids.phys2bids import phys2bids
    from phys2bids.utils import SUPPORTED_FTYPES
except ImportError:
    SUPPORTED_FTYPES = ()   # TODO: handle gracefully
import logging
import shutil
import json
import tempfile
import pandas as pd
import ast
from pathlib import Path
from functools import lru_cache
from bidscoin import bids

LOGGER = logging.getLogger(__name__)

# The default options that are set when installing the plugin
OPTIONS = {}


def test(options: dict) -> int:
    """
    This plugin function tests the working of the plugin + its bidsmap options

    :param options: A dictionary with the plugin options, e.g. taken from the bidsmap['Options']['plugins']['phys2bidscoin']
    :return:        The errorcode (e.g 0 if the tool generated the expected result, > 0 if there was a tool error)
    """

    LOGGER.info(f'This is the phys2bids-plugin WIP test routine')

    return 0


def is_sourcefile(file: Path) -> str:
    """
    This plugin function assesses whether a sourcefile is of a supported dataformat

    :param file:    The sourcefile that is assessed
    :return:        The valid / supported dataformat of the sourcefile
    """

    if file.suffix[1:] in SUPPORTED_FTYPES:
        if file.suffix in ('.txt', '.mat'):
            try:
                phys2bids(file, info=True)
            except Exception as phys2bidserror:
                LOGGER.exception(f'The phys2bids-plugin "is_sourcefile()" routine crashed, assessing whether "{file}" has a valid dataformat:\n{phys2bidserror}')
                return ''
        return 'Physio'

    return ''


@lru_cache(maxsize=4096)
def phys2bids_cache(sourcefile: Path):
    """
    A chached version of phys2bids that reads the info structure

    :param sourcefile:  The sourcefile from which the info needs to be read
    :return:            The retrieved phys2bids info structure
    """

    return phys2bids(str(sourcefile), info=True)


def get_attribute(dataformat: str, sourcefile: Path, attribute: str, options: dict) -> str:
    """
    This plugin function reads attributes from the supported sourcefile

    :param dataformat:  The dataformat of the sourcefile, e.g. DICOM of PAR
    :param sourcefile:  The sourcefile from which key-value data needs to be read
    :param attribute:   The attribute key for which the value needs to be retrieved
    :param options:     A dictionary with the plugin options, e.g. taken from the bidsmap['Options']
    :return:            The retrieved attribute value
    """

    if dataformat == 'Physio':
        LOGGER.verbose(f'This is the phys2bids-plugin get_attribute routine, reading the {dataformat} "{attribute}" attribute value from "{sourcefile}"')
    else:
        return ''

    if not sourcefile.is_file():
        LOGGER.error(f"Could not find {sourcefile}")
        return ''

    phys_info = phys2bids_cache(sourcefile)

    return phys_info.get(attribute, '')


def bidsmapper_plugin(session: Path, bidsmap_new: dict, bidsmap_old: dict, template: dict, store: dict) -> None:
    """
    All the heuristics format phys2bids attributes and properties onto bids labels and meta-data go into this plugin function.
    The function is expected to update / append new runs to the bidsmap_new data structure. The bidsmap options for this plugin
    are stored in:

    bidsmap_new['Options']['plugins']['phys2bidscoin']

    See also the dcm2niix2bids plugin for reference implementation

    :param session:     The full-path name of the subject/session raw data source folder
    :param bidsmap_new: The new study bidsmap that we are building
    :param bidsmap_old: The previous study bidsmap that has precedence over the template bidsmap
    :param template:    The template bidsmap with the default heuristics
    :param store:       The paths of the source- and target-folder
    :return:
    """

    # Get the plugin settings
    plugin = {'phys2bidscoin': bidsmap_new['Options']['plugins']['phys2bidscoin']}

    # Update the bidsmap with the info from the source files
    for sourcefile in [file for file in session.rglob('*') if is_sourcefile(file)]:

        datasource = bids.DataSource(sourcefile, plugin)
        dataformat = datasource.dataformat

        # Input checks
        if not template[dataformat] and not bidsmap_old[dataformat]:
            LOGGER.error(f"No {dataformat} source information found in the bidsmap and template")
            return

        # See if we can find a matching run in the old bidsmap
        run, match = bids.get_matching_run(datasource, bidsmap_old)

        # If not, see if we can find a matching run in the template
        if not match:
            run, _ = bids.get_matching_run(datasource, template)

        # See if we have collected the run somewhere in our new bidsmap
        if not bids.exist_run(bidsmap_new, '', run):

            # Communicate with the user if the run was not present in bidsmap_old or in template, i.e. that we found a new sample
            if not match:
                LOGGER.info(f"Discovered '{datasource.datatype}' {dataformat} sample: {sourcefile}")

            # Now work from the provenance store
            if store:
                targetfile             = store['target']/sourcefile.relative_to(store['source'])
                targetfile.parent.mkdir(parents=True, exist_ok=True)
                LOGGER.verbose(f"Storing the discovered {dataformat} sample as: {targetfile}")
                run['provenance']      = str(shutil.copyfile(sourcefile, targetfile))
                run['datasource'].path = targetfile

            # Copy the filled-in run over to the new bidsmap
            bids.append_run(bidsmap_new, run)


def bidscoiner_plugin(session: Path, bidsmap: dict, bidsses: Path) -> None:
    """
    This wrapper funtion around phys2bids converts the physio data in the session folder and saves it in the bidsfolder.
    Each saved datafile should be accompanied by a json sidecar file. The bidsmap options for this plugin can be found in:

    bidsmap_new['Options']['plugins']['phys2bidscoin']

    See also the dcm2niix2bids plugin for reference implementation

    :param session:     The full-path name of the subject/session raw data source folder
    :param bidsmap:     The full mapping heuristics from the bidsmap YAML-file
    :param bidsses:     The full-path name of the BIDS output `sub-/ses-` folder
    :return:            Nothing
    """

    # Get the subject identifiers and the BIDS root folder from the bidsses folder
    if bidsses.name.startswith('ses-'):
        bidsfolder = bidsses.parent.parent
        subid      = bidsses.parent.name
        sesid      = bidsses.name
    else:
        bidsfolder = bidsses.parent
        subid      = bidsses.name
        sesid      = ''

    # Get started
    plugin      = {'phys2bidscoin': bidsmap['Options']['plugins']['phys2bidscoin']}
    datasource  = bids.get_datasource(session, plugin)
    sourcefiles = [file for file in session.rglob('*') if is_sourcefile(file)]
    if not sourcefiles:
        LOGGER.info(f"--> No {__name__} sourcedata found in: {session}")
        return

    # Loop over all source data files and convert them to BIDS
    for sourcefile in sourcefiles:

        # Get a data source, a matching run from the bidsmap
        datasource = bids.DataSource(sourcefile, plugin, datasource.dataformat)
        run, match = bids.get_matching_run(datasource, bidsmap, runtime=True)

        # Check if we should ignore this run
        if datasource.datatype in bidsmap['Options']['bidscoin']['ignoretypes']:
            LOGGER.info(f"--> Leaving out: {sourcefile}")
            continue

        # Check that we know this run
        if not match:
            LOGGER.error(f"Skipping unknown '{datasource.datatype}' run: {sourcefile}\n-> Re-run the bidsmapper and delete the physiological output data in {bidsses} to solve this warning")
            continue

        LOGGER.info(f"--> Coining: {sourcefile}")

        # Get an ordered list of the func runs from the scans.tsv file (which should have a standardized datetime format)
        scans_tsv = bidsses/f"{subid}{'_'+sesid if sesid else ''}_scans.tsv"
        if scans_tsv.is_file():
            scans_table = pd.read_csv(scans_tsv, sep='\t', index_col='filename')
            scans_table.sort_values(by=['acq_time', 'filename'], inplace=True)
        else:
            LOGGER.error(f"Could not read the TR's for phys2bids due to a missing '{scans_tsv}' file")
            continue
        funcscans = []
        for index, row in scans_table.iterrows():
            if index.startswith('func/'):
                funcscans.append(index)

        # Then read the TR's from the associated func sidecar files
        tr = []
        for funcscan in funcscans:
            with (bidsses/funcscan).with_suffix('.json').open('r') as json_fid:
                jsondata = json.load(json_fid)
            tr.append(jsondata['RepetitionTime'])

        # Create a heuristic function for phys2bids
        heur_str = ('def heur(physinfo, run=""):\n'
                    '    info = {}\n'
                   f'    if physinfo == "{sourcefile.name}":')
        for key, val in run['bids'].items():
            heur_str = (f'{heur_str}'
                        f'\n        info["{key}"] = "{val}"')
        heur_str = f'{heur_str}\n    return info'

        # Write heuristic function as file in temporary folder
        heur_file = Path(tempfile.mkdtemp())/f'heuristic_sub-{subid}_ses-{sesid}.py'
        heur_file.write_text(heur_str)

        # Run phys2bids
        physiofiles = phys2bids(filename                = str(sourcefile),
                                outdir                  = str(bidsfolder),
                                heur_file               = str(heur_file),
                                sub                     = subid,
                                ses                     = sesid,
                                chtrig                  = int(run['meta'].get('TriggerChannel', 0)),
                                num_timepoints_expected = run['meta'].get('ExpectedTimepoints', None),
                                tr                      = tr,
                                pad                     = run['meta'].get('Pad', 9),
                                ch_name                 = run['meta'].get('ChannelNames', []),
                                yml                     = '',
                                debug                   = True,
                                quiet                   = False)

        # Add user-specified meta-data to the newly produced json files (NB: assumes every physio-file comes with a json-file)
        for physiofile in physiofiles:
            jsonfile = Path(physiofile).with_suffix('.json')
            if not jsonfile.is_file():
                LOGGER.error(f"Could not find the expected json sidecar-file: '{jsonfile}'")
                continue
            with jsonfile.open('r') as json_fid:
                jsondata = json.load(json_fid)
            for metakey, metaval in run['meta'].items():
                metaval = datasource.dynamicvalue(metaval, cleanup=False, runtime=True)
                try: metaval = ast.literal_eval(str(metaval))            # E.g. convert stringified list or int back to list or int
                except (ValueError, SyntaxError): pass
                LOGGER.verbose(f"Adding '{metakey}: {metaval}' to: {jsonfile}")
                if not metaval:
                    metaval = None
                jsondata[metakey] = metaval
            with jsonfile.open('w') as json_fid:
                json.dump(jsondata, json_fid, indent=4)
