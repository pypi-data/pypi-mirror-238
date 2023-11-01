# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#
# This file is part of fscan

import os
import subprocess

from .utils.utils import str_to_bool


def write_sub_file(full_path, subname, executable, acctgroup, acctuser,
                   request_disk, request_memory=2000):

    os.makedirs(os.path.join(full_path, 'logs'), exist_ok=True)

    subcontent = f'universe = vanilla\n' \
        f'executable = {executable}\n' \
        f'arguments = $(arglist)\n' \
        f'accounting_group = {acctgroup}\n' \
        f'accounting_group_user = {acctuser}\n' \
        f'request_disk = {request_disk}MB\n' \
        f'request_memory = {request_memory}MB\n' \
        f'log = {full_path}/logs/{subname}.log\n' \
        f'error = {full_path}/logs/{subname}_$(tagstring).err\n' \
        f'output = {full_path}/logs/{subname}_$(tagstring).out\n' \
        f'notification = never\n' \
        f'queue 1'

    with open(os.path.join(full_path, f'{subname}.sub'), 'w') as f:
        f.write(subcontent)


def write_dag(args, epseg_info, channels, chvars):
    """
    This writes out a DAG file that contains the full workflow:
    SFT creation and saving, averaging and normalizing SFTs,
    plotting the data, calculating the coherence and plotting
    """
    dag_filename = os.path.join(epseg_info['epoch_path'], 'SUPERDAG.dag')

    # If a SUPERDAG.dag file already exists, we don't want to append to the
    # file, so check if it does exist, and if so, open a file in write mode
    # so that it effectively erases everything in the file
    if os.path.exists(dag_filename):
        with open(dag_filename, 'w') as f:
            pass

    # If making SFTs from lalpulsar_MakeSFTDAG, use SPLICE to get the DAG file
    # within this DAG
    if args.create_sfts:
        with open(dag_filename, 'a') as f:
            for frametype in channels.keys():
                makesftdagfile = os.path.join(epseg_info['epoch_path'],
                                              f'{frametype}_SFT_GEN',
                                              'makesfts.dag')
                f.write(f"SPLICE {frametype}_SFTs {makesftdagfile}\n")

    if args.full_band_avg:
        with open(dag_filename, 'a') as f:
            for idx, (frametype, chans) in enumerate(channels.items()):
                for (ch_idx, ch) in chans:
                    ch_path = os.path.join(epseg_info['epoch_path'],
                                           ch.replace(':', '_'))
                    subfile = os.path.join(ch_path,
                                           'spectrumAverageLong.sub')
                    f.write(f'JOB SpecAvgLong_{ch_idx} {subfile}\n')
                    f.write(f'VARS SpecAvgLong_{ch_idx} arglist="')
                    f.write(f"--startGPS {epseg_info['SFTGPSstart']}")
                    f.write(f" --endGPS {epseg_info['SFTGPSend']}")
                    f.write(f" --IFO {ch[0:2]}")
                    f.write(f" --fMin {args.fmin}")
                    f.write(f" --fMax {args.fmin + args.band}")
                    f.write(f" --timeBaseline {args.Tsft}")
                    f.write(" --outputBname "
                            f"{ch_path}/speclong_{args.fmin:.1f}"
                            f"_{(args.fmin+args.band):.1f}"
                            f"_{ch[0:2]}"
                            f"_{epseg_info['SFTGPSstart']}"
                            f"_{epseg_info['SFTGPSend']}")
                    if 'persist_avg_opt' in chvars[ch_idx]:
                        f.write(" --persistAvgOption "
                                f"{chvars[ch_idx]['persist_avg_opt']}")
                    elif 'persist_avg_sec' in chvars[ch_idx]:
                        f.write(" --persistAvgSeconds "
                                f"{chvars[ch_idx]['persist_avg_sec']}")
                    if 'auto_track' in chvars[ch_idx]:
                        f.write(" --autoTrack "
                                f"{chvars[ch_idx]['auto_track']}")
                    f.write(f' --SFTs={ch_path}/sfts/*.sft"')
                    f.write(' tagstring="0"\n')
                    if args.create_sfts:
                        f.write(f'PARENT {frametype}_SFTs CHILD '
                                f'SpecAvgLong_{ch_idx}\n')

    max_freq = args.fmin + args.band
    this_start_freq = args.fmin
    this_end_freq = this_start_freq + 100  # TODO: hardcoded 100 Hz -- change?
    node_count = 0

    while this_end_freq <= max_freq:
        with open(dag_filename, 'a') as f:
            for idx, (frametype, chans) in enumerate(channels.items()):
                for (ch_idx, ch) in chans:
                    ch_path = os.path.join(epseg_info['epoch_path'],
                                           ch.replace(':', '_'))
                    subfile = os.path.join(ch_path,
                                           'spectrumAverage.sub')
                    f.write(f'JOB SpecAvg_{ch_idx}_{node_count} {subfile}\n')
                    f.write(f'VARS SpecAvg_{ch_idx}_{node_count} arglist="')
                    f.write(f"--startGPS {epseg_info['SFTGPSstart']}")
                    f.write(f" --endGPS {epseg_info['SFTGPSend']}")
                    f.write(f" --IFO {ch[0:2]}")
                    f.write(f' --fMin {this_start_freq}')
                    f.write(f' --fMax {this_end_freq}')
                    f.write(f" --freqRes {chvars[ch_idx]['freq_res']}")
                    f.write(f" --timeBaseline {args.Tsft}")
                    f.write(f' --SFTs={ch_path}/sfts/*.sft')
                    f.write(f" --outputBname={ch_path}/"
                            f"spec_{this_start_freq:.2f}_"
                            f"{this_end_freq:.2f}_{ch[0:2]}_"
                            f"{epseg_info['SFTGPSstart']}_"
                            f"{epseg_info['SFTGPSend']}")
                    f.write('"')
                    f.write(f' tagstring="{node_count}"\n')

                    if args.create_sfts:
                        f.write(f'PARENT {frametype}_SFTs CHILD '
                                f'SpecAvg_{ch_idx}_{node_count}\n')

                    if 'coherence' in chvars[ch_idx]:
                        subfile = os.path.join(ch_path,
                                               'runCoherence.sub')
                        path_to_other_sfts = os.path.join(
                            epseg_info['epoch_path'],
                            chvars[ch_idx]['coherence'].replace(':', '_'))
                        f.write(f'JOB Coh_{ch_idx}_{node_count} {subfile}\n')
                        f.write(f'VARS Coh_{ch_idx}_{node_count} arglist="')
                        f.write(f"-s {epseg_info['SFTGPSstart']}")
                        f.write(f" -e {epseg_info['SFTGPSend']}")
                        f.write(f' -f {this_start_freq}')
                        f.write(f' -F {this_end_freq}')
                        f.write(f" -t {args.Tsft}")
                        f.write(f' --ChASFTs={path_to_other_sfts}/sfts/*.sft')
                        f.write(f' --ChBSFTs={ch_path}/sfts/*.sft')
                        f.write(f" --outputBname={ch_path}/"
                                f"spec_{this_start_freq:.2f}_"
                                f"{this_end_freq:.2f}_{ch[0:2]}_"
                                f"{epseg_info['SFTGPSstart']}_"
                                f"{epseg_info['SFTGPSend']}_coh")
                        f.write('"')
                        f.write(f' tagstring="{node_count}"\n')

                        # TODO: currently the parent child relationship only
                        # works for coherence between channels with the same
                        # frametype
                        if args.create_sfts:
                            f.write(f'PARENT {frametype}_SFTs CHILD '
                                    f'Coh_{ch_idx}_{node_count}\n')

        # increment sub-band analyzed
        this_start_freq += 100
        this_end_freq = this_start_freq + 100
        node_count += 1

        # in case where the band is a non-integer multiple of sub_band
        # default is not to include the extra amount of data
        if (this_start_freq < max_freq and this_end_freq > max_freq and
                str_to_bool(chvars[ch_idx].get('include_extra_sub_band',
                                               'no'))):
            this_end_freq = max_freq

    if args.plot_output:
        with open(dag_filename, 'a') as f:
            for idx, (frametype, chans) in enumerate(channels.items()):
                for (ch_idx, ch) in chans:
                    ch_path = os.path.join(epseg_info['epoch_path'],
                                           ch.replace(':', '_'))
                    subfile = os.path.join(ch_path,
                                           'postProcess.sub')

                    # set up list of dag parents for post processing
                    parentstring = " ".join([
                        f"SpecAvg_{ch_idx}_{n}" for n in range(node_count)])
                    if args.full_band_avg:
                        parentstring += " "+f"SpecAvgLong_{ch_idx}"
                    if 'coherence' in ch:
                        parentstring += " "+" ".join([
                            f"Coh_{ch_idx}_{n}" for n in range(node_count)])

                    f.write(f'JOB PostProcess_{ch_idx} {subfile}\n')
                    f.write(f'VARS PostProcess_{ch_idx} arglist="run --prefix')
                    f.write(f' {args.postproc_path} postProcess')
                    f.write(f" --parentPathInput {ch_path}")
                    f.write(" --plot-sub-band "
                            f"{chvars[ch_idx]['plot_sub_band']}")
                    if args.tracked_line_list:
                        f.write(" --tracked-line-list "
                                f"{args.tracked_line_list}")
                    if args.tracked_line_tag:
                        f.write(f" --tracked-line-tag {args.tracked_line_tag}")
                    if args.LF_emailFrom and args.LF_emailTo:
                        f.write(f" --LF-emailFrom {args.LF_emailFrom}")
                        f.write(f" --LF-emailTo {args.LF_emailTo}")
                    if args.delete_ascii:
                        f.write(" --delete-converted-text True")
                    f.write('\" tagstring="0"\n')
                    f.write(f'PARENT {parentstring} '
                            f'CHILD PostProcess_{ch_idx}\n')

    return


class MakeSFTJob(object):

    def __init__(self, args, epseg_info, fr_chans):
        self.args = args
        self.epseg_info = epseg_info
        self.frametype = fr_chans[0]
        self.channels = [ch for (idx, ch) in fr_chans[1]]
        self.channel_sft_paths = [
            os.path.join(self.epseg_info['epoch_path'],
                         ch.replace(':', '_'),
                         'sfts') for ch in self.channels]

    def setup_output(self):
        """
        This makes the directories from the full path:
        SFT path/SFT duration/seg type/epoch type/epoch/channels/sfts
        """
        for p in self.channel_sft_paths:
            os.makedirs(p, exist_ok=True)

        return

    def validate_segments(self):
        """
        This just checks that we have at least one segment with duration Tsft
        """
        assert os.path.exists(self.epseg_info['segfile'])

        seg_list = []
        with open(self.epseg_info['segfile']) as f:
            for idx, seg in enumerate(f):
                seg = seg.split()
                if int(seg[1]) - int(seg[0]) >= self.args.Tsft:
                    seg_list.append([seg[0], seg[1]])

        if len(seg_list) < 1:
            raise ValueError(
                f"No segment found in {self.epseg_info['segfile']}")

        return

    def run_make_sft_dag(self):
        """
        This runs the whole making of SFTs
        """
        self.setup_output()

        try:
            self.validate_segments()
        except ValueError:
            print(f"No segments found for {self.epseg_info['epoch_path']}. "
                  "Skipping this epoch.")
            return 1

        sft_dag_file = os.path.join(self.epseg_info['epoch_path'],
                                    f'{self.frametype}_SFT_GEN',
                                    'makesfts.dag')
        cache_dir = os.path.join(os.path.dirname(sft_dag_file), 'cache')
        logs_dir = os.path.join(os.path.dirname(sft_dag_file), 'logs')

        os.makedirs(os.path.dirname(sft_dag_file), exist_ok=True)

        make_dag_cmd = os.path.join(self.args.make_sft_dag_path,
                                    'lalpulsar_MakeSFTDAG')
        make_dag_cmd += f' -m 1 -G fscan_{self.frametype}'
        make_dag_cmd += f' -O {self.args.observing_run}'
        make_dag_cmd += f' -K {self.args.observing_kind}'
        make_dag_cmd += f' -R {self.args.observing_revision}'
        make_dag_cmd += f' -w {self.args.window_type}'
        make_dag_cmd += f' -P {self.args.overlap_fraction}'
        make_dag_cmd += f' -A {self.args.accounting_group}'
        make_dag_cmd += f' -U {self.args.accounting_group_user}'
        make_dag_cmd += f' -Y {self.args.request_memory}'
        make_dag_cmd += f' -s {self.args.request_disk}'
        make_dag_cmd += f' -d {self.frametype}'
        make_dag_cmd += f' -k {self.args.hp_filter_knee_freq}'
        make_dag_cmd += f' -T {self.args.Tsft}'
        make_dag_cmd += f' -F {self.args.fmin}'
        make_dag_cmd += f' -B {self.args.band}'
        make_dag_cmd += f" -N {','.join(self.channels)}"
        make_dag_cmd += f" -p {','.join(self.channel_sft_paths)}"
        make_dag_cmd += f" -C {cache_dir}"
        make_dag_cmd += f" -o {logs_dir}"
        make_dag_cmd += f" -g {self.epseg_info['segfile']}"
        make_dag_cmd += f' -f {sft_dag_file}'
        make_dag_cmd += f' -j {self.args.datafind_path}'
        make_dag_cmd += f' -J {self.args.make_sft_path}'

        if self.args.misc_desc:
            make_dag_cmd += ' -X {self.args.misc_desc}'

        subprocess.run(make_dag_cmd.split(), check=True)

        return 0

    def write_make_sft_dag_sub(self):
        write_sub_file(
            full_path=self.full_ch_path,
            subname='datafind',
            executable=os.path.join(self.args.datafind_path,
                                    'gw_data_find'),
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=5)
        write_sub_file(
            full_path=self.full_ch_path,
            subname='MakeSFTs',
            executable=os.path.join(self.args.make_sft_path,
                                    'lalpulsar_MakeSFTs'),
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=self.args.request_disk)


class NormSFT(object):

    def __init__(self, args, epseg_info, ch):
        self.args = args
        self.epseg_info = epseg_info
        self.ch = ch
        self.full_ch_path = os.path.join(self.epseg_info['epoch_path'],
                                         self.ch['channel'].replace(':', '_'))

    def write_condor_work_sub(self):

        """
        Write the submit file for computing the normalized, averaged spectra
        and the spectrograms using lalpulsar_spec_avg
        """

        write_sub_file(
            full_path=self.full_ch_path,
            subname='spectrumAverage',
            executable=os.path.join(self.args.spec_tools_path,
                                    'lalpulsar_spec_avg'),
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=500)

    def write_condor_full_band_sub(self):

        """
        Write the submit file for computing the normalized, averaged spectra
        using lalpulsar_spec_avg_long
        """

        write_sub_file(
            full_path=self.full_ch_path,
            subname='spectrumAverageLong',
            executable=os.path.join(self.args.spec_tools_path,
                                    'lalpulsar_spec_avg_long'),
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=2000)

    def write_condor_plots_sub(self):
        """
        Write the submit file for computing the normalized, averaged spectra
        and the spectrograms using plotSpectAvgOutput
        """
        write_sub_file(
            full_path=self.full_ch_path,
            subname='postProcess',
            executable='/cvmfs/software.igwn.org/conda/bin/conda',
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=5000,
            request_memory=5000)


class CoherenceFromSFT(object):

    def __init__(self, args, epseg_info, ch):
        self.args = args
        self.epseg_info = epseg_info
        self.ch = ch
        self.full_ch_path = os.path.join(self.epseg_info['epoch_path'],
                                         self.ch['channel'].replace(':', '_'))

    def write_condor_work_sub(self):
        """
        Write the submit file for computing the coherence from SFTs
        """
        write_sub_file(
            full_path=self.full_ch_path,
            subname='runCoherence',
            executable=os.path.join(self.args.spec_tools_path,
                                    'lalpulsar_spec_coherence'),
            acctgroup=self.args.accounting_group,
            acctuser=self.args.accounting_group_user,
            request_disk=500)
