#!/usr/bin/env python3
"""
Filename Analysis Script

This script analyzes JSON filenames in a specified directory and generates statistics.
It parses filenames with the pattern: {uuid}_{status}.json where status is either 
"correct" or "incorrect", and outputs a JSON file with UUID->status mapping.

If the same UUID has both "correct" and "incorrect" files, it prioritizes "correct" status.
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional


def parse_filename(filename: str) -> Optional[tuple]:
    """
    Parse a JSON filename to extract UUID and status.
    
    Args:
        filename: The filename to parse
        
    Returns:
        Tuple of (uuid, status) if valid, None otherwise
    """
    # Pattern: {uuid}_{status}.json
    # UUID pattern: 8-4-4-4-12 hex digits separated by hyphens
    pattern = r'^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})_(correct|incorrect)\.json$'
    
    match = re.match(pattern, filename, re.IGNORECASE)
    if match:
        uuid_str = match.group(1).lower()
        status = match.group(2).lower()
        return (uuid_str, status)
    
    return None


def analyze_directory(directory_path: str) -> Dict[str, str]:
    """
    Analyze JSON files in the specified directory.
    
    Args:
        directory_path: Path to the directory to analyze
        
    Returns:
        Dictionary mapping UUID to status
    """
    if not os.path.exists(directory_path):
        print(f"Warning: Directory '{directory_path}' does not exist.")
        return {}
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        return {}
    
    results = {}
    processed_files = 0
    skipped_files = 0
    
    print(f"Scanning directory: {directory_path}")
    
    try:
        for filename in os.listdir(directory_path):
            if not filename.endswith('.json'):
                continue
                
            parsed = parse_filename(filename)
            if parsed:
                uuid_str, status = parsed
                processed_files += 1
                
                # Priority logic: if same UUID exists, prioritize "correct" over "incorrect"
                if uuid_str in results:
                    if results[uuid_str] == "incorrect" and status == "correct":
                        results[uuid_str] = "correct"
                        print(f"Updated {uuid_str}: {results[uuid_str]} -> {status}")
                    else:
                        print(f"Keeping existing status for {uuid_str}: {results[uuid_str]}")
                else:
                    results[uuid_str] = status
                    print(f"Added {uuid_str}: {status}")
            else:
                skipped_files += 1
                print(f"Skipped invalid filename: {filename}")
    
    except PermissionError:
        print(f"Error: Permission denied accessing directory '{directory_path}'")
        return {}
    except Exception as e:
        print(f"Error reading directory '{directory_path}': {e}")
        return {}
    
    print(f"\nProcessing complete:")
    print(f"- Processed files: {processed_files}")
    print(f"- Skipped files: {skipped_files}")
    print(f"- Unique UUIDs: {len(results)}")
    
    return results


def save_results(results: Dict[str, str], output_file: str = "file_statistics.json") -> bool:
    """
    Save results to a JSON file.
    
    Args:
        results: Dictionary of UUID->status mappings
        output_file: Path to output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, sort_keys=True)
        
        print(f"\nResults saved to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
        return True
        
    except Exception as e:
        print(f"Error saving results to '{output_file}': {e}")
        return False


def main():
    """Main function to run the filename analysis."""
    # Default directory path as specified in requirements
    default_directory = "/Users/xiyunli/owl/result/hunyuan/level_1_details"
    
    # Allow command line override
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = default_directory
    
    print("=" * 60)
    print("Filename Analysis Script")
    print("=" * 60)
    
    # Analyze the directory
    results = analyze_directory(directory_path)
    
    if not results:
        print("No valid files found or error occurred.")
        return 1
    
    # Save results
    if save_results(results):
        print("\nAnalysis completed successfully!")
        
        # Display summary statistics
        correct_count = sum(1 for status in results.values() if status == "correct")
        incorrect_count = sum(1 for status in results.values() if status == "incorrect")
        
        print(f"\nSummary Statistics:")
        print(f"- Total UUIDs: {len(results)}")
        print(f"- Correct status: {correct_count}")
        print(f"- Incorrect status: {incorrect_count}")
        
        return 0
    else:
        print("Failed to save results.")
        return 1


if __name__ == "__main__":
    sys.exit(main())