# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

import os
import numpy as np
from glob import glob
import argparse

from .utils import io
from .plot import static
from .process.linecount import runForestOfLines
from .utils import dtutils as dtl
from .process import autotag, linefinder
from .plot import finetoothplot
from .utils.utils import str_to_bool


def join_subbands(spects, args, metadata):
    '''
    This function is used to join the time-averaged and coherence
    sub-band spectra
    '''
    if len(spects) == 0:
        return

    # sort spectrum files by their minimum frequencies and retain the list of
    #  fmins spectrograms have an extra 0th entry
    if spects[0].endswith("_spectrogram.txt"):
        fmins = [np.loadtxt(s, max_rows=1)[1] for s in spects]
    else:
        fmins = [np.loadtxt(s, max_rows=1)[0] for s in spects]
    sorti = np.argsort(fmins)
    spects = np.array(spects)[sorti]
    fmins = np.array(fmins)[sorti]

    # loop through spectrum files
    for i in range(len(spects)):
        spect = spects[i]

        # handle spectrograms somewhat differently
        if spects[0].endswith("_spectrogram.txt"):
            data = np.loadtxt(spect)
            # gps times are in each row past the 1st at entry 0
            gpstimes = data[1:, 0]
            # select all rows, ignore first entry
            # (which is either a zero or gps time)
            # and transpose so that the frequencies are in
            # the first column (as with other spectral data)
            vals = np.transpose(data[1:, 1:])
            f = data[0, 1:]
        else:
            data = np.loadtxt(spect)
            f = data[:, 0]
            vals = data[:, 1]

        ''' The following lines handle duplicate entries in sub-band files.
        If the last frequency in this file is equal to the first frequency in
        the next file, we simply cut off the last frequency in this file.

        For float comparison, we use the tolerance df/100.
        '''
        df = f[1]-f[0]
        if i < len(spects)-1 and np.isclose(f[-1], fmins[i+1], rtol=df/100):
            vals = vals[:-1]
            f = f[:-1]

        # merge the data from different sub-bands together
        if i == 0:
            knitvals = vals
            knitf = f
        else:
            knitvals = np.append(knitvals, vals, axis=0)
            knitf = np.append(knitf, f, axis=0)

    # check the ordering of the frequencies just to be sure
    assert np.all(np.diff(knitf) > 0)

    # use an input spect file as a template for the output file name
    # (strip the IFO tag, which is not present for coherence, for consistency)
    temp_s = spects[0].replace("_H1_", "_").replace("_L1_", "_")
    n = os.path.basename(temp_s).split("_")
    # replace the label and the frequencies
    n[0] = "fullspect"
    n[1] = metadata['fmin-label']
    n[2] = metadata['fmax-label']

    if temp_s.endswith("_coh.txt"):  # for coherence files
        knitout = os.path.join(args.parentPathInput, "_".join(
            n)).replace("_coh.txt", "_coherence.npz")
        np.savez(knitout, f=knitf, coh=knitvals, metadata=metadata)
    elif temp_s.endswith("_spectrogram.txt"):  # for coherence files
        knitout = os.path.join(args.parentPathInput,
                               "_".join(n).replace(".txt", ".npz"))
        np.savez(knitout, f=knitf, vals=knitvals,
                 gpstimes=gpstimes, metadata=metadata)
    else:  # for regular timeaverage files
        knitout = os.path.join(args.parentPathInput,
                               "_".join(n).replace(".txt", ".npz"))
        np.savez(knitout, f=knitf, normpow=knitvals, metadata=metadata)


def main():
    parser = argparse.ArgumentParser()
    parser.register('type', 'bool', str_to_bool)
    parser.add_argument("--delete-converted-text", type='bool', default=False)
    parser.add_argument("--parentPathInput", type=str)
    parser.add_argument("--plot-sub-band", type=int, default=100,
                        help="Plot frequency bands are rounded to nearest"
                             " integer of this size")
    parser.add_argument("--LF-emailFrom", type=str, default=None,
                        help="Sender email address for LineForest alerts")
    parser.add_argument("--LF-emailTo", type=str, default=None,
                        help="Recipient email address for LineForest alerts")
    parser.add_argument("--tracked-line-list", type=str, nargs="+",
                        default=None, help="Reference list for line tracking")
    parser.add_argument("--tracked-line-tag", type=str, default=None)
    args = parser.parse_args()

    metadata = dtl.parse_filepath(args.parentPathInput)

    # Make the file path nicer
    args.parentPathInput = os.path.abspath(
        os.path.expanduser(args.parentPathInput))

    # ==============================
    # Save NPZ data for the spectra
    # ==============================

    # for output of spec_avg_long (no need to join subbands)
    spectlongs = glob(args.parentPathInput+"/speclong_*.txt")
    for spectlong in spectlongs:
        data = np.transpose(np.loadtxt(spectlong))
        temp_s = spectlong.replace("_H1_", "_").replace(
            "_L1_", "_").strip(".txt").strip("_PWA")
        n = os.path.basename(temp_s).split("_")
        # replace the label and the frequencies
        n[0] = "fullspect"
        n[1] = metadata['fmin-label']
        n[2] = metadata['fmax-label']

        if spectlong.endswith("_PWA.txt"):
            spectlongout = os.path.join(
                args.parentPathInput, f"{'_'.join(n)}_speclongPWA.npz")
            f, pwa_tavgwt, pwa_sumwt = data
            np.savez(spectlongout,
                     f=f,
                     pwa_tavgwt=pwa_tavgwt,
                     pwa_sumwt=pwa_sumwt,
                     metadata=metadata)

        else:
            spectlongout = os.path.join(
                args.parentPathInput, f"{'_'.join(n)}_speclong.npz")
            f, psd, amppsd, psdwt, amppsdwt, persist = data
            np.savez(spectlongout,
                     f=f,
                     psd=psd,
                     amppsd=amppsd,
                     psdwt=psdwt,
                     amppsdwt=amppsdwt,
                     persist=persist,
                     metadata=metadata)

        if args.delete_converted_text:
            os.remove(spectlong)

    # for time-averaged normalized data (must join sub-band files)
    spects = glob(os.path.join(args.parentPathInput, "spec_*_timeaverage.txt"))
    join_subbands(spects, args, metadata)
    if args.delete_converted_text:
        for spect in spects:
            os.remove(spect)

    # for coherence data (must join sub-bands)
    spects = glob(os.path.join(args.parentPathInput, "spec_*_coh.txt"))
    join_subbands(spects, args, metadata)
    if args.delete_converted_text:
        for spect in spects:
            os.remove(spect)

    # for spectrogram data
    spects = glob(os.path.join(args.parentPathInput, "spec_*_spectrogram.txt"))
    join_subbands(spects, args, metadata)
    if args.delete_converted_text:
        for spect in spects:
            os.remove(spect)

    # ==========
    # Make plots
    # ==========

    static.make_all_plots(args.parentPathInput,
                          args.plot_sub_band, ptype='timeaverage')
    # if coherence data:
    if len(glob(f"{args.parentPathInput}/fullspect_*_coherence.npz")) > 0:
        static.make_all_plots(args.parentPathInput,
                              args.plot_sub_band, ptype='coherence')
    static.make_all_plots(args.parentPathInput,
                          args.plot_sub_band, ptype='spectrogram')
    if len(spectlongs) > 0:  # if the spec_avg_long output was generated
        static.make_all_plots(args.parentPathInput,
                              args.plot_sub_band, ptype='persist')

    if "STRAIN" in metadata['channel'] or "DELTAL" in metadata['channel']:

        # ===============
        # Forest of lines
        # ===============

        runForestOfLines(
            args.parentPathInput,
            minEpochs=7,
            maxEpochs=30,
            probCut=1e-6,
            fmax=args.plot_sub_band,
            emailFrom=args.LF_emailFrom,
            emailTo=args.LF_emailTo)

        # =====================
        # Line and comb finding
        # =====================

        autoTagArgs = argparse.Namespace(
            npz_spectfile=glob(
                os.path.join(
                    args.parentPathInput,
                    "fullspect*_timeaverage.npz"))[0],
            data_colname='normpow',
            freq_colname='f',
            fmin=metadata['fmin'],
            fmax=metadata['fmax'],
            tracked_list=args.tracked_line_list,
            autofound_tag="NEW "+metadata['epoch-label'],
            annotated_only_outfile=os.path.join(
                args.parentPathInput,
                "autolines_annotated_only.txt"),
            complete_outfile=os.path.join(
                args.parentPathInput,
                "autolines_complete.txt"),
            find_combs_from_list=None,
            tracked_combs=None,
            tracked_tag=args.tracked_line_tag,
            autoline_FAR=0.001,
            autoline_window=0.05,
            neighbors=50,
            requirelen=5
        )

        autotag.main(autoTagArgs)

        # ===============================================
        # Interactive plotting - normalized average power
        # ===============================================

        fstep = 300
        for fmin in np.arange(0, metadata['fmax'], fstep):
            ftag = f"{int(fmin):04}to{int(fmin+fstep):04}Hz"
            plotArgs = argparse.Namespace(
                spectfile=autoTagArgs.npz_spectfile,
                fmin=fmin,
                fmax=fmin+fstep,
                outfile=os.path.join(
                    args.parentPathInput,
                    f"visual_overview_{ftag}.html"),
                datacolname='normpow',
                freqcolname='f',
                legend=True,
                title=(
                    f"{metadata['channel']}"
                    f" {metadata['epoch'].strftime('%Y-%m-%d')}"),
                yaxlabel="Normalized average power",
                ylog=True,
                annotate=False,
                linesfile=autoTagArgs.annotated_only_outfile,
                plotcombs=None,
                intersect_linefinder=False,
                colorcode='autocolor',
                colorcode_group_min=3
            )

            finetoothplot.main(plotArgs)

        # ==================================
        # Interactive plotting - persistence
        # ==================================

        plotArgs = argparse.Namespace(
            spectfile=glob(
                os.path.join(
                    args.parentPathInput,
                    "fullspect*_speclong.npz"))[0],
            fmin=autoTagArgs.fmin,
            fmax=autoTagArgs.fmax,
            outfile=os.path.join(
                args.parentPathInput,
                "visual_overview_persist.html"),
            datacolname='persist',
            freqcolname='f',
            legend=True,
            title=(
                f"{metadata['channel']}"
                f" {metadata['epoch'].strftime('%Y-%m-%d')}"),
            yaxlabel="Persistence",
            ylog=False,
            annotate=False,
            linesfile=autoTagArgs.annotated_only_outfile,
            plotcombs=None,
            intersect_linefinder=False,
            colorcode='autocolor',
            colorcode_group_min=3
        )

        finetoothplot.main(plotArgs)

    elif metadata['coherence-ref-channel']:

        # ================
        # linefinding only
        # ================
        f, coh = io.load_spect_from_fscan_npz(
            glob(os.path.join(
                args.parentPathInput,
                "fullspect*_coherence.npz"))[0],
            dataname='coh')
        line_locs = linefinder.peaks(coh, 0.001, 0.05/(f[1]-f[0]))
        coh_linefile = os.path.join(
            args.parentPathInput,
            "autolines_complete_coherence.txt")
        with open(coh_linefile, 'w') as cohf:
            for lloc in line_locs:
                cohf.write(f"{f[lloc]},coherence {coh[lloc]}\n")

        # ================================
        # Interactive plotting - coherence
        # ================================

        ref_linesfile = os.path.join(
            metadata['epoch-folder'],
            metadata['coherence-ref-channel'].replace(":", "_"),
            "autolines_annotated_only.txt")
        if not os.path.isfile(ref_linesfile):
            raise Exception(f"Couldn't find line file at {ref_linesfile}")

        plotArgs = argparse.Namespace(
            spectfile=glob(
                os.path.join(
                    args.parentPathInput,
                    "fullspect*_coherence.npz"))[0],
            fmin=0,
            fmax=300,
            outfile=os.path.join(
                args.parentPathInput,
                "visual_overview_coherence.html"),
            datacolname='coh',
            freqcolname='f',
            legend=True,
            title=(
                f"{metadata['channel']}"
                f" {metadata['epoch'].strftime('%Y-%m-%d')}"),
            yaxlabel=f"Coherence with {metadata['coherence-ref-channel']}",
            ylog=False,
            annotate=False,
            linesfile=ref_linesfile,
            plotcombs=None,
            intersect_linefinder=False,
            colorcode='autocolor',
            colorcode_group_min=3
        )
        print(plotArgs.outfile)

        finetoothplot.main(plotArgs)
