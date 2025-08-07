#!/usr/bin/env python3
"""
BMAD Extraction Plan Executor
Executes approved extraction operations from extraction plans
"""

import os
import sys
import json
import hashlib
import shutil
import datetime
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class ExtractionPlanExecutor:
    """Executes extraction plans with safety checks and logging"""
    
    def __init__(self, plan_file: str):
        self.plan_file = Path(plan_file)
        self.backup_dir = Path(".ai/backups")
        self.execution_logs_dir = Path(".ai/execution-logs")
        
        # Create necessary directories
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.execution_logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for this execution
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.execution_id = f"{self.plan_file.stem}_{self.timestamp}"
        
        # Initialize logging
        self.log_file = self.execution_logs_dir / f"{self.execution_id}-execution-log.md"
        self.log_entries = []
        
    def parse_plan_file(self) -> Dict[str, Any]:
        """Parse extraction plan markdown file"""
        if not self.plan_file.exists():
            raise FileNotFoundError(f"Plan file not found: {self.plan_file}")
        
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise Exception(f"Failed to read plan file: {e}")
        
        plan_data = {
            'safe_operations': [],
            'risky_operations': [],
            'metadata': {}
        }
        
        # Parse safe operations
        safe_ops_section = self._extract_section(content, "SAFE OPERATIONS")
        if safe_ops_section:
            plan_data['safe_operations'] = self._parse_operations(safe_ops_section, is_safe=True)
        
        # Parse risky operations
        risky_ops_section = self._extract_section(content, "REQUIRES USER APPROVAL")
        if risky_ops_section:
            plan_data['risky_operations'] = self._parse_operations(risky_ops_section, is_safe=False)
        
        # Extract metadata
        plan_data['metadata'] = self._extract_metadata(content)
        
        return plan_data
    
    def _extract_section(self, content: str, section_name: str) -> Optional[str]:
        """Extract a specific section from markdown content"""
        pattern = rf"### {re.escape(section_name)}.*?\n(.*?)(?=\n### |\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _parse_operations(self, section_content: str, is_safe: bool) -> List[Dict[str, Any]]:
        """Parse operation entries from section content"""
        operations = []
        
        # Split by operation numbers (1., 2., etc.)
        op_pattern = r'\n(\d+)\.\s\*\*Target Location\*\*:'
        op_parts = re.split(op_pattern, section_content)
        
        # Process each operation (skip first empty part)
        for i in range(1, len(op_parts), 2):
            op_num = int(op_parts[i])
            op_content = op_parts[i + 1] if i + 1 < len(op_parts) else ""
            
            operation = self._parse_single_operation(op_content, is_safe)
            if operation:
                operation['operation_number'] = op_num
                operation['is_safe'] = is_safe
                operations.append(operation)
        
        return operations
    
    def _parse_single_operation(self, op_content: str, is_safe: bool) -> Optional[Dict[str, Any]]:
        """Parse a single operation from its content"""
        operation = {}
        
        # Extract fields using regex patterns
        fields = {
            'target_location': r'\*\*Target Location\*\*:\s*([^\n]+)',
            'operation': r'\*\*Operation\*\*:\s*([^\n]+)',
            'rationale': r'\*\*Rationale\*\*:\s*([^\n]+)',
        }
        
        if is_safe:
            fields.update({
                'content_to_add': r'\*\*Content to Add\*\*:\s*```\s*(.*?)\s*```',
                'dependencies': r'\*\*Dependencies\*\*:\s*([^\n]+)',
            })
        else:
            fields.update({
                'current_content': r'\*\*Current Content\*\*:\s*```\s*(.*?)\s*```',
                'proposed_content': r'\*\*Proposed Content\*\*:\s*```\s*(.*?)\s*```',
                'risk_assessment': r'\*\*Risk Assessment\*\*:\s*([^\n]+)',
                'approval_status': r'\*\*Approval Status\*\*:\s*([^\n]+)',
            })
        
        # Extract each field
        for field, pattern in fields.items():
            match = re.search(pattern, op_content, re.DOTALL | re.IGNORECASE)
            if match:
                operation[field] = match.group(1).strip()
        
        return operation if operation else None
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract plan metadata from content"""
        metadata = {}
        
        # Extract document type, summary, etc.
        patterns = {
            'document_type': r'\*\*Document Type\*\*:\s*([^\n]+)',
            'content_summary': r'\*\*Content Summary\*\*:\s*([^\n]+)',
            'safe_operations_count': r'\*\*Safe Operations\*\*:\s*(\d+)',
            'approval_required_count': r'\*\*Approval Required\*\*:\s*(\d+)',
            'estimated_time': r'\*\*Estimated Completion Time\*\*:\s*([^\n]+)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata[field] = match.group(1).strip()
        
        return metadata
    
    def validate_plan(self, plan_data: Dict[str, Any]) -> List[str]:
        """Validate extraction plan and return any issues"""
        issues = []
        
        # Check for required approvals
        for op in plan_data['risky_operations']:
            approval_status = op.get('approval_status', '').upper()
            if approval_status != 'APPROVED':
                issues.append(f"Operation {op.get('operation_number', '?')} requires approval (Status: {approval_status})")
        
        # Validate target paths for safe operations
        for op in plan_data['safe_operations']:
            target = op.get('target_location', '')
            if target:
                target_path = Path(target)
                parent_dir = target_path.parent
                if not parent_dir.exists() and str(parent_dir) != '.':
                    # Check if we need to create directories
                    self.log(f"Warning: Target directory does not exist: {parent_dir}")
        
        return issues
    
    def create_backups(self, operations: List[Dict[str, Any]]) -> str:
        """Create backups of files that will be modified"""
        backup_timestamp_dir = self.backup_dir / self.timestamp
        backup_timestamp_dir.mkdir(exist_ok=True)
        
        backed_up_files = []
        
        for op in operations:
            target_location = op.get('target_location', '')
            if target_location and Path(target_location).exists():
                target_path = Path(target_location)
                
                # Create backup path maintaining directory structure
                relative_path = target_path
                if target_path.is_absolute():
                    relative_path = target_path.relative_to(target_path.anchor)
                
                backup_path = backup_timestamp_dir / relative_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(target_path, backup_path)
                    backed_up_files.append(str(target_path))
                    self.log(f"✓ Backed up: {target_path} -> {backup_path}")
                except Exception as e:
                    self.log(f"❌ Backup failed for {target_path}: {e}")
        
        # Generate rollback script
        rollback_script = backup_timestamp_dir / "rollback.sh"
        rollback_commands = ["#!/bin/bash\n", "# Rollback script for extraction plan execution\n\n"]
        
        for original_file in backed_up_files:
            relative_path = Path(original_file).relative_to(Path.cwd()) if Path(original_file).is_absolute() else Path(original_file)
            backup_path = backup_timestamp_dir / relative_path
            rollback_commands.append(f'cp "{backup_path}" "{original_file}"\n')
        
        with open(rollback_script, 'w') as f:
            f.writelines(rollback_commands)
        
        rollback_script.chmod(0o755)  # Make executable
        
        self.log(f"✓ Created rollback script: {rollback_script}")
        return str(backup_timestamp_dir)
    
    def execute_safe_operations(self, safe_operations: List[Dict[str, Any]]) -> int:
        """Execute safe operations (auto-approved)"""
        success_count = 0
        
        self.log("### Executing Safe Operations")
        
        for op in safe_operations:
            try:
                self.log(f"Executing operation {op.get('operation_number', '?')}: {op.get('operation', 'UNKNOWN')}")
                
                if self._execute_single_operation(op):
                    success_count += 1
                    self.log(f"✅ Operation {op.get('operation_number', '?')} completed successfully")
                else:
                    self.log(f"❌ Operation {op.get('operation_number', '?')} failed")
                    
            except Exception as e:
                self.log(f"❌ Error executing operation {op.get('operation_number', '?')}: {e}")
        
        return success_count
    
    def execute_approved_operations(self, risky_operations: List[Dict[str, Any]]) -> int:
        """Execute approved risky operations"""
        success_count = 0
        
        self.log("### Executing Approved Operations")
        
        approved_ops = [op for op in risky_operations if op.get('approval_status', '').upper() == 'APPROVED']
        
        if not approved_ops:
            self.log("No approved operations to execute")
            return 0
        
        for op in approved_ops:
            try:
                self.log(f"Executing approved operation {op.get('operation_number', '?')}: {op.get('operation', 'UNKNOWN')}")
                
                if self._execute_single_operation(op):
                    success_count += 1
                    self.log(f"✅ Operation {op.get('operation_number', '?')} completed successfully")
                else:
                    self.log(f"❌ Operation {op.get('operation_number', '?')} failed")
                    
            except Exception as e:
                self.log(f"❌ Error executing operation {op.get('operation_number', '?')}: {e}")
        
        return success_count
    
    def _execute_single_operation(self, operation: Dict[str, Any]) -> bool:
        """Execute a single operation"""
        op_type = operation.get('operation', '').upper()
        target_location = operation.get('target_location', '')
        
        if not target_location:
            self.log(f"❌ No target location specified for operation")
            return False
        
        target_path = Path(target_location)
        
        try:
            if op_type in ['ADD', 'CREATE']:
                return self._execute_add_operation(operation, target_path)
            elif op_type == 'MODIFY':
                return self._execute_modify_operation(operation, target_path)
            elif op_type == 'DELETE':
                return self._execute_delete_operation(operation, target_path)
            elif op_type == 'RESTRUCTURE':
                return self._execute_restructure_operation(operation, target_path)
            else:
                self.log(f"❌ Unsupported operation type: {op_type}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error executing {op_type} operation: {e}")
            return False
    
    def _execute_add_operation(self, operation: Dict[str, Any], target_path: Path) -> bool:
        """Execute ADD or CREATE operation"""
        content_to_add = operation.get('content_to_add', '')
        
        if not content_to_add:
            self.log(f"❌ No content specified for ADD operation")
            return False
        
        # Create parent directories if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if operation.get('operation', '').upper() == 'CREATE' or not target_path.exists():
            # Create new file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content_to_add)
            self.log(f"✓ Created file: {target_path}")
        else:
            # Append to existing file
            with open(target_path, 'a', encoding='utf-8') as f:
                f.write('\n' + content_to_add)
            self.log(f"✓ Added content to: {target_path}")
        
        return True
    
    def _execute_modify_operation(self, operation: Dict[str, Any], target_path: Path) -> bool:
        """Execute MODIFY operation"""
        current_content = operation.get('current_content', '')
        proposed_content = operation.get('proposed_content', '')
        
        if not target_path.exists():
            self.log(f"❌ Target file does not exist: {target_path}")
            return False
        
        # Read current file content
        with open(target_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Replace content if current_content matches
        if current_content in file_content:
            updated_content = file_content.replace(current_content, proposed_content)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.log(f"✓ Modified content in: {target_path}")
            return True
        else:
            self.log(f"❌ Current content not found in file: {target_path}")
            return False
    
    def _execute_delete_operation(self, operation: Dict[str, Any], target_path: Path) -> bool:
        """Execute DELETE operation"""
        if target_path.exists():
            if target_path.is_file():
                target_path.unlink()
                self.log(f"✓ Deleted file: {target_path}")
            elif target_path.is_dir():
                shutil.rmtree(target_path)
                self.log(f"✓ Deleted directory: {target_path}")
            return True
        else:
            self.log(f"❌ Target does not exist: {target_path}")
            return False
    
    def _execute_restructure_operation(self, operation: Dict[str, Any], target_path: Path) -> bool:
        """Execute RESTRUCTURE operation"""
        # This is a complex operation that would need specific implementation
        # For now, log that it's not fully implemented
        self.log(f"⚠️ RESTRUCTURE operation not fully implemented for: {target_path}")
        return False
    
    def log(self, message: str):
        """Add entry to execution log"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_entries.append(log_entry)
        print(log_entry)
    
    def save_execution_log(self, plan_data: Dict[str, Any], backup_dir: str, 
                          safe_success: int, risky_success: int) -> str:
        """Save execution log to file"""
        log_content = f"""# Extraction Plan Execution Log

## Execution Details
- **Plan File**: {self.plan_file}
- **Execution ID**: {self.execution_id}
- **Backup Directory**: {backup_dir}
- **Execution Time**: {datetime.datetime.now().isoformat()}

## Plan Summary
- **Safe Operations**: {len(plan_data['safe_operations'])} ({safe_success} successful)
- **Risky Operations**: {len(plan_data['risky_operations'])} ({risky_success} successful)

## Execution Log
"""
        
        for entry in self.log_entries:
            log_content += f"{entry}\n"
        
        log_content += f"\n## Summary\n"
        log_content += f"- Total operations executed: {safe_success + risky_success}\n"
        log_content += f"- Safe operations success rate: {safe_success}/{len(plan_data['safe_operations'])}\n"
        log_content += f"- Risky operations success rate: {risky_success}/{len(plan_data['risky_operations'])}\n"
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        return str(self.log_file)
    
    def execute_plan(self) -> Dict[str, Any]:
        """Main execution method"""
        self.log(f"Starting execution of extraction plan: {self.plan_file}")
        
        # Phase 1: Parse and validate plan
        plan_data = self.parse_plan_file()
        self.log(f"Parsed plan with {len(plan_data['safe_operations'])} safe and {len(plan_data['risky_operations'])} risky operations")
        
        # Phase 2: Validate plan
        issues = self.validate_plan(plan_data)
        if issues:
            for issue in issues:
                self.log(f"❌ Validation issue: {issue}")
            return {
                'success': False,
                'issues': issues,
                'log_file': str(self.log_file)
            }
        
        # Phase 3: Create backups
        all_operations = plan_data['safe_operations'] + [
            op for op in plan_data['risky_operations'] 
            if op.get('approval_status', '').upper() == 'APPROVED'
        ]
        backup_dir = self.create_backups(all_operations)
        
        # Phase 4: Execute operations
        safe_success = self.execute_safe_operations(plan_data['safe_operations'])
        risky_success = self.execute_approved_operations(plan_data['risky_operations'])
        
        # Phase 5: Generate execution log
        log_file = self.save_execution_log(plan_data, backup_dir, safe_success, risky_success)
        
        self.log("✅ Extraction plan execution completed")
        
        return {
            'success': True,
            'safe_operations_executed': safe_success,
            'risky_operations_executed': risky_success,
            'backup_directory': backup_dir,
            'log_file': log_file
        }

def main():
    """Command line interface for extraction plan executor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Execute BMAD extraction plan')
    parser.add_argument('plan_file', help='Path to extraction plan file')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Validate plan without executing operations')
    
    args = parser.parse_args()
    
    try:
        executor = ExtractionPlanExecutor(args.plan_file)
        
        if args.dry_run:
            plan_data = executor.parse_plan_file()
            issues = executor.validate_plan(plan_data)
            
            print(f"✅ Plan validation completed")
            print(f"   Safe operations: {len(plan_data['safe_operations'])}")
            print(f"   Risky operations: {len(plan_data['risky_operations'])}")
            
            if issues:
                print(f"❌ Issues found:")
                for issue in issues:
                    print(f"   - {issue}")
            else:
                print(f"✅ No issues found - plan ready for execution")
        else:
            result = executor.execute_plan()
            
            if result['success']:
                print(f"✅ Extraction plan executed successfully")
                print(f"   Safe operations: {result['safe_operations_executed']}")
                print(f"   Risky operations: {result['risky_operations_executed']}")
                print(f"   Backup directory: {result['backup_directory']}")
                print(f"   Execution log: {result['log_file']}")
            else:
                print(f"❌ Extraction plan execution failed")
                for issue in result.get('issues', []):
                    print(f"   - {issue}")
                print(f"   Log file: {result['log_file']}")
                sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error executing extraction plan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()