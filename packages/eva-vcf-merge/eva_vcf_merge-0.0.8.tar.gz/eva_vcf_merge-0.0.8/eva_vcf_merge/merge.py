# Copyright 2021 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil

from ebi_eva_internal_pyutils.nextflow import NextFlowPipeline, NextFlowProcess

from eva_vcf_merge.detect import MergeType
from eva_vcf_merge.multistage import get_multistage_merge_pipeline
from eva_vcf_merge.utils import get_valid_filename, validate_aliases


class VCFMerger:
    def __init__(self, bgzip_binary, bcftools_binary, nextflow_binary, nextflow_config, output_dir):
        self.bgzip_binary = bgzip_binary
        self.bcftools_binary = bcftools_binary
        self.nextflow_binary = nextflow_binary
        self.nextflow_config = nextflow_config
        self.output_dir = output_dir
        self.working_dir = os.path.join(output_dir, 'nextflow')

    def horizontal_merge(self, vcf_groups, chunk_size=500, resume=True):
        return self.common_merge(MergeType.HORIZONTAL, vcf_groups, chunk_size, resume)

    def vertical_merge(self, vcf_groups, chunk_size=500, resume=True):
        return self.common_merge(MergeType.VERTICAL, vcf_groups, chunk_size, resume)

    def common_merge(self, merge_type, vcf_groups, chunk_size=500, resume=True):
        """
        Merge groups of vcfs horizontally or vertically.

        :param merge_type: vertical or horizontal merge
        :param vcf_groups: dict mapping a string (e.g. an analysis alias) to a group of vcf files to be merged
        :param chunk_size: number of vcfs to merge at once (default 500)
        :param resume: whether to resume pipeline (default true)
        :returns: dict of merged filenames
        """
        if not validate_aliases(vcf_groups.keys()):
            raise ValueError('Aliases must be unique when converted to filenames')
        pipeline, merged_filenames = self.generate_merge_pipeline(merge_type, vcf_groups, chunk_size)
        workflow_file = os.path.join(self.working_dir, "merge.nf")

        os.makedirs(self.working_dir, exist_ok=True)
        pipeline.run_pipeline(
            workflow_file_path=workflow_file,
            working_dir=self.working_dir,
            nextflow_binary_path=self.nextflow_binary,
            nextflow_config_path=self.nextflow_config,
            resume=resume
        )
        # move merged files to output directory and rename with alias
        for alias in merged_filenames:
            safe_alias = get_valid_filename(alias)
            target_filename = os.path.join(self.output_dir, f'{safe_alias}_merged.vcf.gz')
            shutil.move(merged_filenames[alias], target_filename)
            shutil.move(merged_filenames[alias] + '.csi', target_filename + '.csi')
            shutil.move(merged_filenames[alias] + '.tbi', target_filename + '.tbi')
            merged_filenames[alias] = target_filename
        return merged_filenames

    def generate_merge_pipeline(self, merge_type, vcf_groups, chunk_size):
        """
        Generate merge pipeline, including compressing and indexing VCFs.

        :param merge_type: vertical or horizontal merge
        :param vcf_groups: dict mapping a string to a group of vcf files to be merged
        :param chunk_size: number of vcfs to merge at once
        :return: complete NextFlowPipeline and dict of merged filenames
        """
        full_pipeline = NextFlowPipeline()
        merged_filenames = {}
        for alias_idx, (alias, vcfs) in enumerate(vcf_groups.items()):
            compress_pipeline, compressed_vcfs = self.compress_and_index(alias_idx, vcfs)
            if merge_type == MergeType.HORIZONTAL:
                merge_pipeline, merged_filename = get_multistage_merge_pipeline(
                    alias=alias_idx,
                    vcf_files=compressed_vcfs,
                    chunk_size=chunk_size,
                    processing_dir=self.working_dir,
                    bcftools_binary=self.bcftools_binary,
                    process_name='merge',
                    process_command=self.merge_command
                )
            else:
                merge_pipeline, merged_filename = get_multistage_merge_pipeline(
                    alias=alias_idx,
                    vcf_files=compressed_vcfs,
                    chunk_size=chunk_size,
                    processing_dir=self.working_dir,
                    bcftools_binary=self.bcftools_binary,
                    process_name='concat',
                    process_command=self.concat_command
                )
            pipeline = NextFlowPipeline.join_pipelines(compress_pipeline, merge_pipeline)
            full_pipeline = NextFlowPipeline.join_pipelines(full_pipeline, pipeline, with_dependencies=False)
            merged_filenames[alias] = merged_filename
        return full_pipeline, merged_filenames

    def compress_and_index(self, alias, vcfs):
        """
        Bgzip-compress and CSI-index VCFs.

        :param alias: name of group of vcf files (used to name Nextflow processes uniquely)
        :param vcfs: list of vcf files
        :return: NextFlow pipeline and list of final filenames
        """
        dependencies = {}
        index_processes = []
        compressed_vcfs = []
        for i, vcf in enumerate(vcfs):
            compress_process = None
            if not vcf.endswith('gz'):
                compress_process = NextFlowProcess(
                    process_name=f'compress_{alias}_{i}',
                    command_to_run=f'{self.bgzip_binary} -c {vcf} > {vcf}.gz'
                )
                vcf = f'{vcf}.gz'
            compressed_vcfs.append(vcf)
            index_process = NextFlowProcess(
                process_name=f'index_{alias}_{i}',
                command_to_run=f'{self.bcftools_binary} index -f -c {vcf}'
            )
            index_processes.append(index_process)
            # each file's index depends only on compress (if present)
            dependencies[index_process] = [compress_process] if compress_process else []
        return NextFlowPipeline(dependencies), compressed_vcfs

    def merge_command(self, files_to_merge_list, output_vcf_file):
        return (f'{self.bcftools_binary} merge --merge all --file-list {files_to_merge_list} --threads 3 '
                f'-O z -o {output_vcf_file}')

    def concat_command(self, files_to_merge_list, output_vcf_file):
        return (f'{self.bcftools_binary} concat --allow-overlaps --remove-duplicates --file-list {files_to_merge_list} '
                f'-O z -o {output_vcf_file}')
