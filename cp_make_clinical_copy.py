# -*- coding: utf-8 -*-
"""

Make clinical copy of cp-project directory

Use as:
    
    python cp_make_clinical_copy.py "D:\ViconData\Clinical\dp11" "C:\Temp"
    --subj_code D0024_TH --subj_name Tuure

@author: Jussi (jnu@iki.fi)
"""

import os
import os.path as op
import re
import logging
import argparse
import shutil
import glob
import btk

from cp_common import _glob_all
import gaitutils
from gaitutils import sessionutils

logger = logging.getLogger(__name__)


def _find_trials(sessionpath):
    """For CP-project folders, return normal (N) trials only. For any other
    folder, return all dynamic trials. Also return static trials"""
    enfs_ = list(sessionutils.get_session_enfs(sessionpath))
    enfs_dyn = list(sessionutils._filter_by_type(enfs_, 'dynamic'))
    enfs_static = list(sessionutils._filter_by_type(enfs_, 'static'))
    # look for normal trials (N followed by n digits)
    enfs_normal = [enf for enf in enfs_dyn if re.search('\.*N(\d*)\.*', enf)]
    ecl_keys = ['DESCRIPTION', 'NOTES']
    enfs_standing = sessionutils._filter_by_eclipse_keys(enfs_dyn, 'standing', ecl_keys)
    enfs_unipedal = sessionutils._filter_by_eclipse_keys(enfs_dyn, 'unipedal', ecl_keys)
    if not enfs_normal:
        enfs_ret = enfs_dyn + enfs_static
    else:
        enfs_ret = (enfs_normal + enfs_static + list(enfs_standing) +
                    list(enfs_unipedal))
    return [op.split(enf)[-1] for enf in enfs_ret]  # strip path


def _fix_static_subjname(c3dfile, new_name):
    """Fix subject name in static trials"""
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(c3dfile)
    reader.Update()
    acq = reader.GetOutput()
    meta = acq.GetMetaData()
    newmetainfo = btk.btkMetaDataInfo((new_name.ljust(32),))
    meta.GetChild('SUBJECTS').GetChild('NAMES').SetInfo(newmetainfo)
    acq.SetMetaData(meta)
    acq.Update()
    writer = btk.btkAcquisitionFileWriter()
    writer.SetInput(acq)
    writer.SetFilename(c3dfile)
    writer.Update()
    

def make_clinical_copy(subjdir, dest_root, subj_code, subj_name, meas_type):
    """ destdir is destination root dir (=subject will appear under it) """

    subj_orig = op.split(subjdir)[-1].lower()
    logger.debug('original subject %s' % subj_orig)
    
    extra_codes = ['tuet', 'paljal', 'tuet_pohjallinen', 'tuet_pohjalliset']
    
    if not op.isdir(subjdir):
        raise ValueError('Subject dir %s not found' % subjdir)

    sessiondirs = [dirn for dirn in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, dirn))]

    if not sessiondirs:
        raise ValueError('Subject dir %s does not contain any sessions'
                         % subjdir)

    if subj_code is None:
        subj_code = 'Unknown_NN'

    if subj_name is None:
        subj_code = 'Anonymous'
    
    if meas_type is None:
        meas_type = 'seur'

    destdir = op.join(dest_root, subj_code)
    if op.isdir(destdir):
        raise Exception('Destination subject dir exists!')
    os.mkdir(destdir)
    
    # patient enf
    f_enf = glob.glob(op.join(subjdir, '*Patient.enf'))
    if len(f_enf) == 1:
        f_enf = f_enf[0]
    elif len(f_enf) == 0:
        f_enf = None
    else:
        raise Exception('Too many patient .enf files')
    if f_enf:
        target = op.join(destdir, subj_code+'.Patient.enf')
        logger.debug('copying: %s->%s' % (f_enf, target))
        shutil.copy2(f_enf, target)
        
    for sessiondir in sessiondirs:
        sessiondir_full = op.join(subjdir, sessiondir)
        sessiontime = gaitutils.sessionutils.get_session_date(sessiondir_full)
        sessiondate = sessiontime.strftime('%Y_%m_%d')
        initials = subj_code[-2:]

        extra_code = ''
        for code in extra_codes:
            if code in sessiondir.lower():
                extra_code = '_%s' % code
        sessiondir_dest_ = '%s_%s%s_%s' % (sessiondate, meas_type, extra_code,
                                            initials)
        sessiondir_dest = op.join(destdir, sessiondir_dest_)
        if op.isdir(sessiondir_dest):
            raise Exception('Target session dir already exists!')
        os.mkdir(sessiondir_dest)

        # these do not need to be renamed
        f_no_renames = _glob_all(['*sup', '*mkr'], prefix=sessiondir_full)
        for f in f_no_renames:
            logger.debug('copying: %s->%s' % (f, op.join(sessiondir_dest, f)))
            shutil.copy2(f, sessiondir_dest)

        # session enf
        f_session_enf = glob.glob(op.join(sessiondir_full, '*Session.enf'))
        if len(f_session_enf) == 1:
            f_session_enf = f_session_enf[0]
        elif len(f_session_enf) == 0:
            f_session_enf = None
        else:
            raise Exception('Too many session .enf files')
        if f_session_enf:
            target = op.join(sessiondir_dest, sessiondir_dest_+'.Session.enf')
            logger.debug('copying: %s->%s' % (f, target))
            shutil.copy2(f_session_enf, target)

        # renamed according to subject
        f_renames = _glob_all(['*mp', '*vsk'], prefix=sessiondir_full)
        for f in f_renames:
            ext = op.splitext(f)[-1]
            target = op.join(sessiondir_dest, subj_name+ext)
            logger.debug('copying: %s->%s' % (f, target))
            shutil.copy2(f, target)

        # copy trial files
        f_trials = _find_trials(sessiondir_full)
        for n, f_trial in enumerate(f_trials):
            basename = gaitutils.sessionutils._enf2other(f_trial, '')
            glob_ = op.join(sessiondir_full, basename+'*')
            trial_files_all = glob.glob(glob_)
            for f in trial_files_all:
                """ We want to write new filename + old extension, but some
                files need special treatment (e.g. need to preserve camera
                number for avi files) """
                ext = op.splitext(f)[-1]
                if ext == '.enf':
                    ext = '.Trial.enf'
                if ext == '.avi':
                    ext = f[f.find('.'):]  # FIXME: bit hackish  
                nstr = str(n).zfill(2)
                target_file = '%s%s%s' % (sessiondir_dest_, nstr, ext)
                logger.debug(target_file)
                target = op.join(sessiondir_dest, target_file)
                logger.debug('copying: %s->%s' % (f, target))
                shutil.copy2(f, target)
                
        # rewrite enfs with correct subj info
        trial_enfs = gaitutils.sessionutils.get_session_enfs(sessiondir_dest)
        for f in trial_enfs:
            f_full = op.join(sessiondir_dest, f)
            di = {'SUBJECTS': subj_name}
            gaitutils.eclipse.set_eclipse_keys(f_full, di,
                                               update_existing=True)
        # fix static 
        static_c3ds = gaitutils.sessionutils.get_c3ds(sessiondir_dest,
                                                      trial_type='static')
        for c3dfile in static_c3ds:
            _fix_static_subjname(c3dfile, subj_name)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()

    parser.add_argument('subjdir', help='source subject directory')
    parser.add_argument('destdir', help='destination root directory')
    parser.add_argument('--subj_code', type=str)
    parser.add_argument('--subj_name', type=str)
    parser.add_argument('--meas_type', type=str)

    args = parser.parse_args()

    make_clinical_copy(args.subjdir, args.destdir, args.subj_code,
                       args.subj_name, args.meas_type)
    
