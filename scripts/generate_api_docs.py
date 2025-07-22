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


def main():
    """Main entry point."""
    print("🚀 Generating Pyrion API documentation...")
    
    generator = APIDocGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()