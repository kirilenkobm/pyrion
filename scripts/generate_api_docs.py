#!/usr/bin/env python3
"""Generate comprehensive API documentation for pyrion package."""

import inspect
import pkgutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Set
from datetime import datetime
import importlib

# Add pyrion to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyrion


class APIDocGenerator:
    """Generate both detailed API reference and concise API index."""
    
    def __init__(self):
        self.detailed_docs = []
        self.index_docs = []
        self.processed_modules: Set[str] = set()
        
    def generate_all(self):
        """Generate both API reference and index files."""
        print("🔍 Scanning pyrion package...")

        # Process the main pyrion package
        self._process_module(pyrion, "pyrion")

        # Write detailed API reference
        print("📝 Writing detailed API reference...")
        self._write_detailed_reference()

        # Write concise API index
        print("📋 Writing concise API index...")
        self._write_concise_index()

        # Update agent-focused docs with fresh imports
        print("🤖 Updating agent documentation with fresh imports...")
        self._update_agent_docs()

        print("✅ API documentation generated successfully!")
    
    def _process_module(self, module: Any, module_name: str, prefix: str = ""):
        """Recursively process a module and its submodules."""
        if module_name in self.processed_modules:
            return
            
        self.processed_modules.add(module_name)
        
        try:
            # Get module info
            module_doc = inspect.getdoc(module) or ""
            
            # Add to detailed docs
            self.detailed_docs.append(f"# {module_name}\n")
            if module_doc:
                self.detailed_docs.append(f"{module_doc}\n")
            self.detailed_docs.append("")
            
            # Add to index
            self.index_docs.append(f"MODULE {module_name}")
            
            # Get all classes and functions in this module
            members = inspect.getmembers(module)
            
            classes = []
            functions = []
            
            for name, obj in members:
                if name.startswith('_'):
                    continue
                    
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    classes.append((name, obj))
                elif inspect.isfunction(obj) and obj.__module__ == module.__name__:
                    functions.append((name, obj))
            
            # Process classes
            if classes:
                self.detailed_docs.append("## Classes\n")
                for class_name, class_obj in sorted(classes):
                    self._process_class(class_obj, class_name, module_name)
                    
            # Process functions
            if functions:
                self.detailed_docs.append("## Functions\n")
                for func_name, func_obj in sorted(functions):
                    self._process_function(func_obj, func_name, module_name)
            
            self.detailed_docs.append("---\n")
            
            # Process submodules
            if hasattr(module, '__path__'):
                for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
                    try:
                        full_name = f"{module_name}.{modname}"
                        submodule = importlib.import_module(full_name)
                        self._process_module(submodule, full_name, prefix + "  ")
                    except (ImportError, AttributeError) as e:
                        print(f"⚠️  Skipping {full_name}: {e}")
                        
        except Exception as e:
            print(f"⚠️  Error processing {module_name}: {e}")
    
    def _process_class(self, class_obj: type, class_name: str, module_name: str):
        """Process a class and its methods."""
        class_doc = inspect.getdoc(class_obj) or ""
        signature = self._get_class_signature(class_obj)
        
        # Detailed docs
        self.detailed_docs.append(f"### {class_name}\n")
        if class_doc:
            self.detailed_docs.append(f"{class_doc}\n")
        if signature:
            self.detailed_docs.append(f"**Signature:** `{signature}`\n")
        
        # Index
        self.index_docs.append(f"  CLASS {class_name}")
        if signature:
            self.index_docs.append(f"    __init__{signature}")
        
        # Get methods and properties
        methods = []
        properties = []
        
        for name, method in inspect.getmembers(class_obj):
            if name.startswith('_') and name not in ['__init__', '__str__', '__repr__']:
                continue
                
            if inspect.ismethod(method) or inspect.isfunction(method):
                methods.append((name, method))
            elif isinstance(method, property):
                properties.append((name, method))
        
        # Process methods
        if methods:
            self.detailed_docs.append("#### Methods\n")
            for method_name, method_obj in sorted(methods):
                self._process_method(method_obj, method_name, class_name)
                
        # Process properties  
        if properties:
            self.detailed_docs.append("#### Properties\n")
            for prop_name, prop_obj in sorted(properties):
                self._process_property(prop_obj, prop_name, class_name)
                
        self.detailed_docs.append("")
    
    def _process_function(self, func_obj: callable, func_name: str, module_name: str):
        """Process a standalone function."""
        func_doc = inspect.getdoc(func_obj) or ""
        signature = self._get_function_signature(func_obj)
        
        # Detailed docs
        self.detailed_docs.append(f"### {func_name}\n")
        if signature:
            self.detailed_docs.append(f"**Signature:** `{signature}`\n")
        if func_doc:
            self.detailed_docs.append(f"{func_doc}\n")
        
        # Index
        self.index_docs.append(f"  FUNCTION {func_name}{signature}")
        
        self.detailed_docs.append("")
    
    def _process_method(self, method_obj: callable, method_name: str, class_name: str):
        """Process a class method."""
        method_doc = inspect.getdoc(method_obj) or ""
        signature = self._get_function_signature(method_obj)
        
        # Detailed docs
        self.detailed_docs.append(f"**{method_name}**\n")
        if signature:
            self.detailed_docs.append(f"*Signature:* `{signature}`\n")
        if method_doc:
            self.detailed_docs.append(f"{method_doc}\n")
        
        # Index
        self.index_docs.append(f"    {method_name}{signature}")
        
        self.detailed_docs.append("")
    
    def _process_property(self, prop_obj: property, prop_name: str, class_name: str):
        """Process a class property."""
        prop_doc = inspect.getdoc(prop_obj) or ""
        
        # Try to get type annotation
        prop_type = "Any"
        try:
            if hasattr(prop_obj.fget, '__annotations__'):
                return_annotation = prop_obj.fget.__annotations__.get('return', 'Any')
                prop_type = self._format_annotation(return_annotation)
        except:
            pass
        
        # Detailed docs
        self.detailed_docs.append(f"**{prop_name}** -> `{prop_type}`\n")
        if prop_doc:
            self.detailed_docs.append(f"{prop_doc}\n")
        
        # Index
        self.index_docs.append(f"    {prop_name} -> {prop_type}")
        
        self.detailed_docs.append("")
    
    def _get_class_signature(self, class_obj: type) -> str:
        """Get class constructor signature."""
        try:
            if hasattr(class_obj, '__init__'):
                sig = inspect.signature(class_obj.__init__)
                return str(sig)
        except:
            pass
        return ""
    
    def _get_function_signature(self, func_obj: callable) -> str:
        """Get function signature."""
        try:
            sig = inspect.signature(func_obj)
            return str(sig)
        except:
            return ""
    
    def _format_annotation(self, annotation: Any) -> str:
        """Format type annotation for display."""
        if hasattr(annotation, '__name__'):
            return annotation.__name__
        return str(annotation)
    
    def _write_detailed_reference(self):
        """Write the detailed API reference file."""
        output_path = Path("API_REFERENCE.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Pyrion API Reference\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Complete API reference with full docstrings and signatures.\n\n")
            
            # Table of contents
            f.write("## Table of Contents\n\n")
            for line in self.detailed_docs[:50]:  # First few modules for TOC
                if line.startswith("# "):
                    module_name = line[2:].strip()
                    f.write(f"- [{module_name}](#{module_name.replace('.', '').lower()})\n")
                elif line.startswith("### "):
                    class_name = line[4:].strip()
                    f.write(f"  - [{class_name}](#{class_name.lower()})\n")
            f.write("\n---\n\n")
            
            # Content
            for line in self.detailed_docs:
                f.write(line + "\n")
        
        print(f"📄 API reference written to: {output_path}")
    
    def _write_concise_index(self):
        """Write the concise API index file."""
        output_path = Path("api-index.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"PYRION API INDEX\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Concise reference with type signatures only.\n")
            f.write("=" * 60 + "\n\n")
            
            # Content
            for line in self.index_docs:
                f.write(line + "\n")
        
        print(f"📋 API index written to: {output_path}")

    def _update_agent_docs(self):
        """Update AGENTS.md and CLAUDE.md with fresh import statements."""
        import pyrion
        import pyrion.ops

        # Generate import blocks from actual __all__
        main_imports = self._generate_import_block(pyrion, "pyrion")
        ops_imports = self._generate_import_block(pyrion.ops, "pyrion.ops")

        # Update AGENTS.md
        self._update_agents_md(main_imports, ops_imports)

        # Update CLAUDE.md
        self._update_claude_md(main_imports, ops_imports)

        print("📝 Agent documentation updated with current imports")

    def _generate_import_block(self, module: Any, module_name: str) -> List[str]:
        """Generate a sorted list of public exports from a module."""
        if hasattr(module, '__all__'):
            # Filter out version/internal stuff for cleaner agent docs
            skip_items = {'__version__', '__version_info__', '__author__', '__github__',
                         '__license__', '__copyright__', 'get_version', 'get_version_info',
                         'quick_start', 'cite', 'SequenceType', 'FaiEntry', 'FaiStore',
                         'TranslationTable', 'ExonType', 'Metadata', 'BlockArray',
                         'ChainBlockArray', 'get_available_cores', 'get_max_cores',
                         'set_max_cores', 'get_min_items_for_parallel',
                         'set_min_items_for_parallel', 'disable_parallel',
                         'enable_parallel', 'is_multiprocessing_available',
                         'get_config_summary', 'set_loglevel'}

            items = [item for item in module.__all__ if item not in skip_items]
            return sorted(items)
        return []

    def _update_agents_md(self, main_imports: List[str], ops_imports: List[str]):
        """Update AGENTS.md with fresh import statements."""
        agents_path = Path("AGENTS.md")
        if not agents_path.exists():
            print(f"⚠️  {agents_path} not found, skipping")
            return

        with open(agents_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Format imports nicely (max ~80 chars per line)
        main_block = self._format_imports("pyrion", main_imports)
        ops_block = self._format_imports("pyrion.ops", ops_imports)

        new_imports = f'''```python
{main_block}

# I/O
from pyrion import (
    read_bed12_file,
    read_narrow_bed_file,
    read_chain_file,
    read_gene_data,
    read_fasta,
    write_fasta,
    read_dna_fasta,
    FastaAccessor,
    read_gtf,
)

# Operations
{ops_block}
```'''

        # Replace between "## Canonical imports" and next "##"
        import re
        pattern = r'(## Canonical imports\s*\n\n)```python\n.*?```(\s*\n## )'
        replacement = r'\1' + new_imports + r'\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Add reference link if not present
        if 'API_REFERENCE.md' not in new_content:
            footer = "\n\n**For complete API signatures, see [API_REFERENCE.md](API_REFERENCE.md) or [api-index.txt](api-index.txt)**\n"
            # Add before "## Where to find docs"
            new_content = new_content.replace('## Where to find docs', footer + '## Where to find docs')

        with open(agents_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Updated {agents_path}")

    def _update_claude_md(self, main_imports: List[str], ops_imports: List[str]):
        """Update CLAUDE.md with fresh import statements."""
        claude_path = Path("CLAUDE.md")
        if not claude_path.exists():
            print(f"⚠️  {claude_path} not found, skipping")
            return

        with open(claude_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pick most commonly used items for CLAUDE.md (keep it concise)
        essential_main = [
            'GenomicInterval', 'GenomicIntervalsCollection',
            'Transcript', 'TranscriptsCollection', 'Gene', 'GeneData',
            'GenomeAlignment', 'GenomeAlignmentsCollection',
            'NucleotideSequence', 'AminoAcidSequence', 'Strand',
            'TwoBitAccessor', 'FastaAccessor',
            'read_bed12_file', 'read_chain_file', 'read_gene_data',
            'read_fasta', 'write_fasta'
        ]

        essential_ops = [
            'project_transcript_through_chain',
            'project_intervals_through_genome_alignment',
            'extract_cds_sequence', 'extract_exon_sequence',
            'merge_intervals', 'intersect_intervals', 'subtract_intervals',
            'slice_transcript', 'transcript_to_bed12_string',
            'save_transcripts_collection_to_bed12'
        ]

        main_block = self._format_imports("pyrion", essential_main)
        ops_block = self._format_imports("pyrion.ops", essential_ops)

        new_imports = f'''```python
{main_block}
{ops_block}
```'''

        # Replace between "## Core imports" and next "##"
        import re
        pattern = r'(## Core imports\s*\n\n)```python\n.*?```(\s*\n## )'
        replacement = r'\1' + new_imports + r'\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Add reference link to Docs section if not present
        if 'API_REFERENCE.md' not in new_content:
            docs_section = new_content.find('## Docs')
            if docs_section != -1:
                # Find the end of the list
                end_of_list = new_content.find('\n\n', docs_section)
                if end_of_list != -1:
                    insert_point = end_of_list
                    new_content = (new_content[:insert_point] +
                                 "\n- `API_REFERENCE.md` — complete auto-generated API reference" +
                                 "\n- `api-index.txt` — concise type signatures index" +
                                 new_content[insert_point:])

        with open(claude_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Updated {claude_path}")

    def _format_imports(self, module_name: str, items: List[str]) -> str:
        """Format import statements with nice line wrapping."""
        if not items:
            return f"from {module_name} import ()"

        # Group items to fit ~80 chars per line
        lines = [f"from {module_name} import ("]
        current_line = "    "

        for i, item in enumerate(items):
            if i == len(items) - 1:
                # Last item
                current_line += item + ","
                lines.append(current_line)
            else:
                # Check if adding this item would exceed ~75 chars
                test_line = current_line + item + ", "
                if len(test_line) > 75:
                    # Start new line
                    lines.append(current_line.rstrip())
                    current_line = "    " + item + ", "
                else:
                    current_line += item + ", "

        lines.append(")")
        return "\n".join(lines)


def main():
    """Main entry point."""
    print("🚀 Generating Pyrion API documentation...")
    
    generator = APIDocGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()