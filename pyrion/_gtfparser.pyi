"""Type stubs for _gtfparser C extension."""

from typing import List, Dict, Tuple, Any

def parse_gtf_chunk(lines: List[str]) -> Tuple[List[Any], Dict[str, str], Dict[str, str], Dict[str, str]]:
    """
    Parse GTF chunk into transcripts, gene mapping, biotypes, and gene names.
    
    Args:
        lines: List of GTF lines for a single gene
        
    Returns:
        Tuple of (transcript_objects, gene_mapping_dict, transcript_biotypes_dict, gene_names_dict)
    """
    ... 