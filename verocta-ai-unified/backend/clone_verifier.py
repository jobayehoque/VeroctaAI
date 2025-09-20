"""
FinDash Clone Verification System
Checksum-based hash verification to ensure project integrity
"""

import os
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any
import difflib

class CloneVerifier:
    """Clone integrity verification system"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.integrity_report = {
            'timestamp': datetime.now().isoformat(),
            'project_root': self.project_root,
            'status': 'unknown',
            'files_checked': 0,
            'files_matched': 0,
            'files_modified': 0,
            'files_missing': 0,
            'deviations': [],
            'checksums': {}
        }
        
    def calculate_file_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of a file"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logging.error(f"Error calculating hash for {filepath}: {str(e)}")
            return ""
    
    def get_project_files(self) -> List[str]:
        """Get list of all project files to verify"""
        exclude_patterns = {
            '__pycache__', '.git', '.vscode', 'node_modules',
            '.env', 'outputs', 'uploads', '.DS_Store',
            '*.pyc', '*.log', '*.tmp'
        }
        
        project_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            
            for file in files:
                # Skip excluded file patterns
                if any(pattern in file for pattern in exclude_patterns):
                    continue
                    
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.project_root)
                project_files.append(rel_path)
        
        return sorted(project_files)
    
    def create_baseline_checksums(self) -> Dict[str, str]:
        """Create baseline checksums for all project files"""
        checksums = {}
        files = self.get_project_files()
        
        for rel_path in files:
            full_path = os.path.join(self.project_root, rel_path)
            if os.path.exists(full_path):
                checksum = self.calculate_file_hash(full_path)
                if checksum:
                    checksums[rel_path] = checksum
        
        # Save baseline
        baseline_path = os.path.join(self.project_root, 'integrity_baseline.json')
        with open(baseline_path, 'w') as f:
            json.dump({
                'created': datetime.now().isoformat(),
                'files_count': len(checksums),
                'checksums': checksums
            }, f, indent=2)
        
        logging.info(f"Created baseline with {len(checksums)} files")
        return checksums
    
    def load_baseline_checksums(self) -> Dict[str, str]:
        """Load baseline checksums"""
        baseline_path = os.path.join(self.project_root, 'integrity_baseline.json')
        
        if not os.path.exists(baseline_path):
            logging.warning("No baseline found, creating new baseline")
            return self.create_baseline_checksums()
        
        try:
            with open(baseline_path, 'r') as f:
                baseline_data = json.load(f)
                return baseline_data.get('checksums', {})
        except Exception as e:
            logging.error(f"Error loading baseline: {str(e)}")
            return {}
    
    def verify_file_integrity(self, rel_path: str, expected_checksum: str) -> Dict[str, Any]:
        """Verify integrity of a specific file"""
        full_path = os.path.join(self.project_root, rel_path)
        
        if not os.path.exists(full_path):
            return {
                'status': 'missing',
                'expected': expected_checksum,
                'actual': None,
                'message': f"File missing: {rel_path}"
            }
        
        actual_checksum = self.calculate_file_hash(full_path)
        
        if actual_checksum == expected_checksum:
            return {
                'status': 'matched',
                'expected': expected_checksum,
                'actual': actual_checksum,
                'message': f"File integrity verified: {rel_path}"
            }
        else:
            return {
                'status': 'modified',
                'expected': expected_checksum,
                'actual': actual_checksum,
                'message': f"File modified: {rel_path}"
            }
    
    def get_file_diff(self, rel_path: str) -> List[str]:
        """Get line-by-line differences for a modified file"""
        full_path = os.path.join(self.project_root, rel_path)
        
        if not os.path.exists(full_path):
            return ["File does not exist"]
        
        try:
            # For now, we'll return a placeholder since we don't have original content
            # In a real implementation, you'd compare with the original source
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            return [f"File has {len(lines)} lines (detailed diff requires original source)"]
            
        except Exception as e:
            return [f"Error reading file: {str(e)}"]
    
    def verify_clone_integrity(self) -> Dict[str, Any]:
        """Perform complete clone integrity verification"""
        logging.info("Starting clone integrity verification...")
        
        # Load baseline checksums
        baseline_checksums = self.load_baseline_checksums()
        
        if not baseline_checksums:
            logging.error("No baseline checksums available")
            self.integrity_report['status'] = 'error'
            self.integrity_report['message'] = 'No baseline checksums available'
            return self.integrity_report
        
        # Verify each file
        for rel_path, expected_checksum in baseline_checksums.items():
            self.integrity_report['files_checked'] += 1
            verification_result = self.verify_file_integrity(rel_path, expected_checksum)
            
            status = verification_result['status']
            
            if status == 'matched':
                self.integrity_report['files_matched'] += 1
            elif status == 'modified':
                self.integrity_report['files_modified'] += 1
                # Get detailed diff
                diff_lines = self.get_file_diff(rel_path)
                deviation = {
                    'file': rel_path,
                    'type': 'modified',
                    'expected_checksum': expected_checksum,
                    'actual_checksum': verification_result['actual'],
                    'diff_preview': diff_lines[:10]  # First 10 lines of diff
                }
                self.integrity_report['deviations'].append(deviation)
            elif status == 'missing':
                self.integrity_report['files_missing'] += 1
                deviation = {
                    'file': rel_path,
                    'type': 'missing',
                    'expected_checksum': expected_checksum,
                    'message': 'File is missing from the project'
                }
                self.integrity_report['deviations'].append(deviation)
        
        # Check for new files not in baseline
        current_files = set(self.get_project_files())
        baseline_files = set(baseline_checksums.keys())
        new_files = current_files - baseline_files
        
        for new_file in new_files:
            full_path = os.path.join(self.project_root, new_file)
            if os.path.exists(full_path):
                checksum = self.calculate_file_hash(full_path)
                deviation = {
                    'file': new_file,
                    'type': 'new',
                    'checksum': checksum,
                    'message': 'New file not in baseline'
                }
                self.integrity_report['deviations'].append(deviation)
        
        # Determine overall status
        total_issues = self.integrity_report['files_modified'] + self.integrity_report['files_missing'] + len(new_files)
        
        if total_issues == 0:
            self.integrity_report['status'] = 'clean'
            self.integrity_report['message'] = 'All files match baseline - clone integrity verified'
        elif total_issues <= 5:
            self.integrity_report['status'] = 'minor_deviations'
            self.integrity_report['message'] = f'{total_issues} minor deviations detected'
        else:
            self.integrity_report['status'] = 'major_deviations'
            self.integrity_report['message'] = f'{total_issues} significant deviations detected - clone integrity compromised'
        
        # Save report
        report_path = os.path.join(self.project_root, 'integrity_report.json')
        with open(report_path, 'w') as f:
            json.dump(self.integrity_report, f, indent=2)
        
        logging.info(f"Verification complete: {self.integrity_report['status']}")
        return self.integrity_report
    
    def get_verification_summary(self) -> str:
        """Get human-readable verification summary"""
        if self.integrity_report['status'] == 'unknown':
            return "Verification not yet performed"
        
        summary_lines = [
            f"📊 Clone Integrity Report - {self.integrity_report['timestamp']}",
            f"📁 Project: {self.project_root}",
            f"📋 Status: {self.integrity_report['status'].replace('_', ' ').title()}",
            f"📄 Files Checked: {self.integrity_report['files_checked']}",
            f"✅ Files Matched: {self.integrity_report['files_matched']}",
            f"⚠️  Files Modified: {self.integrity_report['files_modified']}",
            f"❌ Files Missing: {self.integrity_report['files_missing']}",
            f"📝 Total Deviations: {len(self.integrity_report['deviations'])}"
        ]
        
        if self.integrity_report['deviations']:
            summary_lines.append("\n🔍 Deviation Details:")
            for deviation in self.integrity_report['deviations'][:5]:  # Show first 5
                summary_lines.append(f"  • {deviation['file']} - {deviation['type']}")
            
            if len(self.integrity_report['deviations']) > 5:
                summary_lines.append(f"  ... and {len(self.integrity_report['deviations']) - 5} more")
        
        return "\n".join(summary_lines)


def verify_project_integrity(project_root: str = ".") -> Dict[str, Any]:
    """Main function to verify project integrity"""
    verifier = CloneVerifier(project_root)
    return verifier.verify_clone_integrity()


def create_project_baseline(project_root: str = ".") -> Dict[str, str]:
    """Create baseline checksums for the project"""
    verifier = CloneVerifier(project_root)
    return verifier.create_baseline_checksums()


if __name__ == "__main__":
    # CLI interface for verification
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create-baseline":
        print("Creating project baseline...")
        checksums = create_project_baseline()
        print(f"✅ Baseline created with {len(checksums)} files")
    else:
        print("Verifying project integrity...")
        verifier = CloneVerifier()
        report = verifier.verify_clone_integrity()
        print(verifier.get_verification_summary())
