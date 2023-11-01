"""
scores need to be sequential so that it can easily be aggregated based on a polca flag or not - otherwise I need another rule
"""


rule assess_chrom_pre_polish:
    """
    Run ALE on chrom_pre_polish - post dnaapler
    """
    input:
        r1=os.path.join(dir.out.fastp, "{sample}_1.fastq.gz"),
        fasta=os.path.join(dir.out.dnaapler, "{sample}", "{sample}_reoriented.fasta"),
    output:
        score=os.path.join(
            dir.out.ale_scores_complete, "{sample}", "chrom_pre_polish.score"
        ),
        ale=temp(
            os.path.join(dir.out.ale_out_files, "{sample}", "chrom_pre_polish.ale")
        ),
        sam1=temp(os.path.join(dir.out.ale_sams, "{sample}_chrom_pre_polish_1.sam")),
    conda:
        os.path.join(dir.env, "ale.yaml")
    resources:
        mem_mb=config.resources.med.mem,
        mem=str(config.resources.med.mem) + "MB",
        time=config.resources.med.time,
    threads: config.resources.big.cpu
    benchmark:
        os.path.join(dir.out.bench, "ale", "{sample}_chrom_pre_polish.txt")
    log:
        os.path.join(dir.out.stderr, "ale", "{sample}_chrom_pre_polish.log"),
    shell:
        """
        bwa index {input.fasta}
        bwa mem -t {threads} -a {input.fasta} {input.r1} > {output.sam1} 2> {log}
        ALE {output.sam1} {input.fasta} {output.ale} 2> {log}
        grep "# ALE_score: " {output.ale} | sed 's/# ALE_score: //' > {output.score}
        rm {log}
        """


rule assess_polypolish:
    """
    Run ALE on polypolish
    """
    input:
        r1=os.path.join(dir.out.fastp, "{sample}_1.fastq.gz"),
        fasta=os.path.join(dir.out.polypolish, "{sample}.fasta"),
        score=os.path.join(
            dir.out.ale_scores_complete, "{sample}", "chrom_pre_polish.score"
        ),
    output:
        score=os.path.join(dir.out.ale_scores_complete, "{sample}", "polypolish.score"),
        ale=temp(os.path.join(dir.out.ale_out_files, "{sample}", "polypolish.ale")),
        sam1=temp(os.path.join(dir.out.ale_sams, "{sample}_polypolish.sam")),
    conda:
        os.path.join(dir.env, "ale.yaml")
    resources:
        mem_mb=config.resources.med.mem,
        mem=str(config.resources.med.mem) + "MB",
        time=config.resources.med.time,
    threads: config.resources.big.cpu
    benchmark:
        os.path.join(dir.out.bench, "ale", "{sample}_polypolish.txt")
    log:
        os.path.join(dir.out.stderr, "ale", "{sample}_polypolish.log"),
    shell:
        """
        bwa index {input.fasta}
        bwa mem -t {threads} -a {input.fasta} {input.r1} > {output.sam1} 2> {log}
        ALE {output.sam1} {input.fasta} {output.ale} 2> {log}
        grep "# ALE_score: " {output.ale} | sed 's/# ALE_score: //' > {output.score}
        rm {log}
        """


rule assess_pypolca:
    """
    Run ALE on pypolca
    """
    input:
        r1=os.path.join(dir.out.fastp, "{sample}_1.fastq.gz"),
        fasta=os.path.join(dir.out.pypolca, "{sample}", "{sample}_corrected.fasta"),
        score=os.path.join(dir.out.ale_scores_complete, "{sample}", "polypolish.score"),
    output:
        score=os.path.join(dir.out.ale_scores_complete, "{sample}", "pypolca.score"),
        ale=temp(os.path.join(dir.out.ale_out_files, "{sample}", "pypolca.ale")),
        sam1=temp(os.path.join(dir.out.ale_sams, "{sample}_pypolca.sam")),
    conda:
        os.path.join(dir.env, "ale.yaml")
    resources:
        mem_mb=config.resources.med.mem,
        mem=str(config.resources.med.mem) + "MB",
        time=config.resources.big.time,
    threads: config.resources.big.cpu
    benchmark:
        os.path.join(dir.out.bench, "ale", "{sample}_pypolca.txt")
    log:
        os.path.join(dir.out.stderr, "ale", "{sample}_pypolca.log"),
    shell:
        """
        bwa index {input.fasta}
        bwa mem -t {threads} -a {input.fasta} {input.r1} > {output.sam1} 2> {log}
        ALE {output.sam1} {input.fasta} {output.ale} 2> {log}
        grep "# ALE_score: " {output.ale} | sed 's/# ALE_score: //' > {output.score}
        rm {log}
        """
