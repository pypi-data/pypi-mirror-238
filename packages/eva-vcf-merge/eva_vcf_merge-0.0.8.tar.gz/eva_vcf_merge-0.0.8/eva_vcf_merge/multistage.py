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

import math
import os

from ebi_eva_internal_pyutils.nextflow import NextFlowPipeline, NextFlowProcess


def get_multistage_merge_pipeline(
        alias,
        vcf_files,
        processing_dir,
        chunk_size,
        bcftools_binary,
        process_name,
        process_command,
        stage=0,
        prev_stage_processes=None,
        pipeline=None
):
    """
    Generate Nextflow pipeline for multi-stage VCF merging or concatenation.

    # As an example, below is multi-stage VCF concatenation of 5 VCF files with 2-VCFs concatenated at a time (CHUNK_SIZE=2)
    # For illustration purposes only. Usually the CHUNK_SIZE is much higher (ex: 500).
    #
    #		    vcf1		    vcf2		vcf3		    vcf4		vcf5
    #               \		     /		       \		      /
    # Stage0:	     \		   /		        \		    /
    # -------	      \	     /		             \	      /
    #	    	vcf1_2=concat(vcf1,vcf2)	vcf3_4=concat(vcf3,vcf4)	vcf5    <---- 3 batches of concat in stage 0
    #		 		    \ 		                /
    # Stage1:	  		 \		              /
    # -------	   		  \	                /
    #				vcf1_2_3_4=concat(vcf1_2,vcf3_4)		            vcf5    <---- 2 batches of concat in stage 1
    #	 					      \ 		                            /
    # Stage2:	  		 		   \		 	                      /
    # -------	   		  			\	                            /
    #						      vcf1_2_3_4_5=concat(vcf1_2_3_4,vcf5)          <----- Final result
    """
    if not pipeline:
        pipeline = NextFlowPipeline()
        prev_stage_processes = []
    # If we are left with only one file, this means we have reached the last merge stage
    if len(vcf_files) == 1:
        # Add last indexing using tbi
        index_process = NextFlowProcess(
            process_name=f"final_index_tbi_{alias}",
            command_to_run=f"{bcftools_binary} index --tbi {vcf_files[0]}"
        )
        pipeline.add_dependencies({index_process: prev_stage_processes[-1:]})
        return pipeline, vcf_files[0]

    num_batches_in_stage = math.ceil(len(vcf_files) / chunk_size)
    curr_stage_processes = []
    output_vcf_files_from_stage = []
    for batch in range(0, num_batches_in_stage):
        # split files in the current stage into chunks based on chunk_size
        files_in_batch = vcf_files[(chunk_size * batch):(chunk_size * (batch + 1))]
        files_to_merge_list = write_files_to_merge_list(process_name, alias, files_in_batch, stage, batch, processing_dir)
        output_vcf_file = get_output_vcf_file_name(process_name, alias, stage, batch, processing_dir)

        # separate merge & index processes
        merge_process = NextFlowProcess(
            process_name=f"{process_name}{alias}_stage{stage}_batch{batch}",
            command_to_run=process_command(files_to_merge_list, output_vcf_file)
        )
        index_process = NextFlowProcess(
            process_name=f"index{alias}_stage{stage}_batch{batch}",
            command_to_run=f"{bcftools_binary} index --csi {output_vcf_file}"
        )
        # index depends only on this batch's merge
        pipeline.add_dependencies({index_process: [merge_process]})
        # next stage requires indexing to be complete from this stage
        curr_stage_processes.append(index_process)
        output_vcf_files_from_stage.append(output_vcf_file)

        # Merge batch in a given stage will have to wait until the completion of
        # n batches in the previous stage where n = chunk_size
        # Ex: In the illustration above stage 1/batch 0 depends on completion of stage 0/batch 0 and stage 0/batch 1
        # While output of any n batches from the previous stage can be worked on as they become available,
        # having a predictable formula simplifies pipeline generation and troubleshooting
        prev_stage_dependencies = prev_stage_processes[(chunk_size * batch):(chunk_size * (batch + 1))]
        pipeline.add_dependencies({merge_process: prev_stage_dependencies})
    prev_stage_processes = curr_stage_processes

    return get_multistage_merge_pipeline(
        alias, output_vcf_files_from_stage,
        processing_dir, chunk_size,
        bcftools_binary,
        process_name,
        process_command,
        stage=stage+1,
        prev_stage_processes=prev_stage_processes,
        pipeline=pipeline
    )


def write_files_to_merge_list(process_name, alias, files_to_merge, stage, batch, processing_dir):
    """
    Write the list of files to be merged for a given stage and batch
    """
    output_dir = get_output_dir(process_name, alias, stage, processing_dir)
    list_filename = os.path.join(output_dir, f"batch{batch}_files.list")
    os.makedirs(os.path.dirname(list_filename), exist_ok=True)
    with open(list_filename, "w") as handle:
        for filename in files_to_merge:
            handle.write(filename + "\n")
    return list_filename


def get_output_dir(process_name, alias, stage_index, processing_dir):
    """
    Get the file name with the list of files to be merged for a given stage and batch in the merge process
    """
    return os.path.join(processing_dir, f'{process_name}_{alias}', f"stage_{stage_index}")


def get_output_vcf_file_name(process_name, alias, stage_index, batch_index, processing_dir):
    return os.path.join(get_output_dir(process_name, alias, stage_index, processing_dir),
                        f"{process_name}{alias}_output_stage{stage_index}_batch{batch_index}.vcf.gz")
